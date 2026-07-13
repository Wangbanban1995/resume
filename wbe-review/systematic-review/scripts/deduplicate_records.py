#!/usr/bin/env python3
"""Deduplicate bibliographic records exported from Web of Science, Scopus, and PubMed.

Reads RIS (.ris), Scopus CSV (.csv), NBIB (.nbib), and BibTeX (.bib, fallback/experimental
parser only) files from an input directory tree, normalizes them to a common schema, and
deduplicates records. ONLY three rules may auto-merge two records into one master record:

    1. Canonical DOI exact match
    2. Canonical PMID exact match
    3. Normalized title + year + first-author exact match, AND no conflicting DOI/PMID

Everything weaker (title+year alone, title+author alone, title alone, or a fuzzy title
match) produces a SEPARATE master record flagged as a `possible_duplicate` pointing at
its closest candidate — never auto-merged, always left for human review via
`templates/manual_duplicate_review.csv`. A title+year+author match is also downgraded to
`possible_duplicate` (not merged) if the two records carry different non-empty DOIs or
PMIDs, or if their publication_version labels suggest a correction/erratum, protocol,
preprint, or conference-abstract pairing with a primary/journal record.

After every field backfill onto a master record, that master is re-indexed so a later
record can still chain-match it via a newly-available DOI/PMID/title/author (see
`reindex_master`).

This script does not invent, estimate, or guess at search results. If no real input
files are found, it exits with a clear message and produces no output claiming to be
real data. After deduplication it runs an internal integrity check
(`deduplication_integrity_report.md/.csv`) and exits non-zero if that check fails.

Usage:
    python3 deduplicate_records.py --input-dir data/raw --output-dir data/processed --log-dir logs
    python3 deduplicate_records.py --help
"""

import argparse
import csv
import hashlib
import logging
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

SUPPORTED_EXTENSIONS = {".ris", ".csv", ".bib", ".nbib"}

UNIFIED_FIELDS = [
    "record_id", "title", "abstract", "authors", "year", "journal",
    "DOI", "PMID", "doi_candidates", "multiple_conflicting_dois",
    "source_accession_id", "wos_accession_number", "scopus_eid",
    "database_source", "search_module", "source_file",
]

MASTER_EXTRA_FIELDS = [
    "database_sources", "search_modules", "source_files",
    "duplicate_record_ids", "occurrence_count",
    "publication_version", "possible_duplicate_of_record_id",
    "possible_version_relation", "duplicate_match_basis",
    "manual_duplicate_decision",
]

REQUIRED_FOR_DEDUP = ["title"]

PREPRINT_MARKERS = ("arxiv", "medrxiv", "biorxiv", "ssrn", "chemrxiv", "researchsquare", "preprint")
CONFERENCE_MARKERS = ("proceedings", "conference", "symposium", "workshop")
CORRECTION_TITLE_RE = re.compile(r"\b(correction|erratum|corrigendum|retraction)\b", re.IGNORECASE)
PROTOCOL_TITLE_RE = re.compile(r"\bprotocol\b", re.IGNORECASE)
DOI_STRICT_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logger(log_dir: Path, name: str = "deduplicate_records") -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = log_dir / f"{name}_{timestamp}.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("Log file: %s", log_path)
    return logger


def read_text_safely(path: Path, logger: logging.Logger) -> str:
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc, errors="strict") as f:
                text = f.read()
            if enc != "utf-8-sig":
                logger.warning("File %s read using fallback encoding %s", path, enc)
            return text
        except (UnicodeDecodeError, UnicodeError):
            continue
    logger.warning("File %s could not be decoded cleanly even with latin-1 fallback; "
                    "reading with errors='replace'", path)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Canonicalization
# ---------------------------------------------------------------------------

def canonicalize_doi(value: str) -> str:
    """Normalize a DOI string to a bare, lowercase, punctuation-stripped canonical form.

    Handles: leading/trailing whitespace, a "doi:" prefix, "https://doi.org/",
    "http://doi.org/", "http://dx.doi.org/", "https://dx.doi.org/", percent-encoding,
    a trailing "[doi]" tag, and trailing "." "," ";" ")" "]" punctuation.
    """
    if not value:
        return ""
    v = value.strip()
    if not v:
        return ""
    v = urllib.parse.unquote(v)
    v = re.sub(r"(?i)^doi:\s*", "", v.strip())
    v = re.sub(r"(?i)^https?://(dx\.)?doi\.org/", "", v.strip())
    v = re.sub(r"(?i)\s*\[doi\]\s*$", "", v)
    v = v.strip()
    v = re.sub(r"[.,;\)\]]+$", "", v)
    return v.strip().lower()


def canonicalize_pmid(value: str) -> str:
    """Normalize a PMID to a bare numeric string, or "" if implausible (e.g. a WoS
    accession number like "WOS:000123456789" must never be read as a PMID)."""
    if not value:
        return ""
    v = value.strip()
    v = re.sub(r"(?i)^pmid:?\s*", "", v).strip()
    if re.fullmatch(r"\d+", v):
        return v
    return ""


def normalize_title(title: str) -> str:
    t = (title or "").lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def first_author_surname(authors: str) -> str:
    if not authors:
        return ""
    first = authors.split(";")[0].strip()
    if "," in first:
        return first.split(",")[0].strip().lower()
    parts = first.split()
    return parts[-1].strip().lower() if parts else ""


def detect_publication_version(title: str, journal: str) -> str:
    t = (title or "").lower()
    j = (journal or "").lower()
    if CORRECTION_TITLE_RE.search(t):
        return "correction_or_erratum"
    if PROTOCOL_TITLE_RE.search(t):
        return "protocol"
    if any(marker in j for marker in PREPRINT_MARKERS):
        return "preprint"
    if any(marker in j for marker in CONFERENCE_MARKERS):
        return "conference_abstract"
    return "primary_or_unclassified"


def version_conflict(version_a: str, version_b: str) -> bool:
    if version_a == version_b:
        return False
    flagged = {"correction_or_erratum", "protocol", "preprint", "conference_abstract"}
    return version_a in flagged or version_b in flagged


def identifier_conflict(record_a: dict, record_b: dict):
    """True + reason if two records carry different non-empty persistent identifiers
    (DOI or PMID) — must block any title-based auto-merge between them, per instruction,
    regardless of how well their title/year/author otherwise match."""
    doi_a, doi_b = record_a.get("_canonical_doi", ""), record_b.get("_canonical_doi", "")
    pmid_a, pmid_b = record_a.get("_canonical_pmid", ""), record_b.get("_canonical_pmid", "")
    if doi_a and doi_b and doi_a != doi_b:
        return True, f"conflicting DOI: '{doi_a}' vs '{doi_b}'"
    if pmid_a and pmid_b and pmid_a != pmid_b:
        return True, f"conflicting PMID: '{pmid_a}' vs '{pmid_b}'"
    return False, ""


def resolve_doi_candidates(raw_candidates: list, source_file: str, warnings: list):
    """Canonicalize and deduplicate a list of raw DOI-like strings found on one record
    (multiple RIS "DO" tags, or multiple NBIB AID/LID "[doi]" values). Returns
    (chosen_doi, all_candidates_list, is_conflicting). `chosen_doi` is "" — left
    deliberately ambiguous, never silently guessed — whenever two or more distinct
    values matching the standard DOI pattern (^10\\.\\d{4,9}/\\S+$) are present."""
    canon_list = []
    seen = set()
    for raw in raw_candidates:
        c = canonicalize_doi(raw)
        if c and c not in seen:
            seen.add(c)
            canon_list.append(c)

    if not canon_list:
        return "", [], False

    valid = [c for c in canon_list if DOI_STRICT_PATTERN.match(c)]

    if len(valid) == 1:
        return valid[0], canon_list, False
    if len(valid) == 0 and len(canon_list) == 1:
        return canon_list[0], canon_list, False

    if len(valid) >= 2:
        warnings.append(f"{source_file}: MULTIPLE CONFLICTING DOIs found on one record "
                        f"({valid}) — DOI left blank pending manual review; all "
                        f"candidates retained in doi_candidates.")
    elif len(canon_list) >= 2:
        warnings.append(f"{source_file}: multiple non-standard-pattern DOI-like values "
                        f"found on one record ({canon_list}), none clearly valid — "
                        f"DOI left blank pending manual review.")
    return "", canon_list, True


# ---------------------------------------------------------------------------
# Format inference
# ---------------------------------------------------------------------------

def infer_database_from_path(path: Path):
    parts = {p.lower() for p in path.parts}
    if "wos" in parts:
        return "wos"
    if "scopus" in parts:
        return "scopus"
    if "pubmed" in parts:
        return "pubmed"
    return None


def infer_module_from_filename(path: Path):
    m = re.search(r"(core|module0[2-8])", path.stem, re.IGNORECASE)
    return m.group(1).lower() if m else None


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

RIS_MULTILINE_TAGS = {"TI", "T1", "AB", "N2"}


def parse_ris(text: str, source_file: str, database: str, module: str, logger: logging.Logger,
              warnings: list) -> list:
    """RIS parser. Supports continuation lines, multiple authors, multiple DO fields
    (resolved via resolve_doi_candidates at flush time, not "first wins"), TI/T1, AB/N2,
    JO/JF/T2, PY/Y1/DA, and a missing terminal ER (a new TY auto-flushes any pending
    record). The "AN" tag is NEVER auto-mapped to PMID (it is a database accession
    number, e.g. a WoS UT) — only an explicit "PMID"/"PM" tag, or a value carrying a
    "PMID:" prefix, populates the PMID field."""
    records = []
    current = {}
    last_tag = None

    def flush():
        if current:
            records.append(_ris_record_to_unified(dict(current), source_file, database,
                                                   module, warnings))

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            last_tag = None
            continue

        m = re.match(r"^([A-Z][A-Z0-9])\s{0,2}-\s?(.*)$", line)
        if not m:
            if last_tag in RIS_MULTILINE_TAGS:
                key = "title" if last_tag in ("TI", "T1") else "abstract"
                current[key] = (current.get(key, "") + " " + line.strip()).strip()
            continue

        tag, value = m.group(1), m.group(2).strip()
        last_tag = tag

        if tag == "TY":
            flush()
            current = {}
        elif tag == "ER":
            flush()
            current = {}
            last_tag = None
        elif tag in ("TI", "T1"):
            current["title"] = (current.get("title", "") + (" " if current.get("title") else "") + value).strip()
        elif tag in ("AB", "N2"):
            current["abstract"] = (current.get("abstract", "") + (" " if current.get("abstract") else "") + value).strip()
        elif tag in ("AU", "A1", "A2", "A3"):
            current.setdefault("authors", []).append(value)
        elif tag in ("PY", "Y1", "DA"):
            year_match = re.search(r"\d{4}", value)
            if year_match and not current.get("year"):
                current["year"] = year_match.group(0)
        elif tag in ("JO", "JF", "T2"):
            if not current.get("journal"):
                current["journal"] = value
        elif tag == "DO":
            current.setdefault("DO_list", []).append(value)
        elif tag in ("PMID", "PM"):
            current["PMID"] = value.strip()
        elif tag == "AN":
            if re.match(r"(?i)^pmid:", value.strip()):
                current["PMID"] = canonicalize_pmid(value)
            else:
                current["accession_raw"] = value.strip()

    flush()

    return records


def _ris_record_to_unified(rec: dict, source_file: str, database: str, module: str,
                           warnings: list) -> dict:
    doi, doi_candidates, conflicting = resolve_doi_candidates(
        rec.get("DO_list", []), source_file, warnings)
    accession = rec.get("accession_raw", "")
    return {
        "title": rec.get("title", ""),
        "abstract": rec.get("abstract", ""),
        "authors": "; ".join(rec.get("authors", [])),
        "year": rec.get("year", ""),
        "journal": rec.get("journal", ""),
        "DOI": doi,
        "doi_candidates": ";".join(doi_candidates),
        "multiple_conflicting_dois": conflicting,
        "PMID": rec.get("PMID", ""),
        "source_accession_id": accession if database not in ("wos", "scopus") else "",
        "wos_accession_number": accession if database == "wos" else "",
        "scopus_eid": "",
        "database_source": database,
        "search_module": module,
        "source_file": source_file,
    }


NBIB_MULTILINE_TAGS = {"TI", "AB"}


def parse_nbib(text: str, source_file: str, database: str, module: str, logger: logging.Logger,
               warnings: list) -> list:
    """PubMed NBIB parser. Supports continuation lines for TI/AB, FAU/AU, DP/DEP,
    JT/TA, and DOI recovery from multiple AID/LID "[doi]" values (resolved via
    resolve_doi_candidates, not "first wins")."""
    records = []
    current = {}
    last_tag = None

    def flush():
        if current:
            records.append(_nbib_record_to_unified(dict(current), source_file, database,
                                                    module, warnings))

    for line in text.splitlines():
        if not line.strip():
            flush()
            current.clear()
            last_tag = None
            continue

        m = re.match(r"^([A-Z]{2,4})\s*-\s?(.*)$", line)
        if not m:
            if line.startswith("      ") and last_tag in NBIB_MULTILINE_TAGS:
                key = "TI" if last_tag == "TI" else "AB"
                current[key] = (current.get(key, "") + " " + line.strip()).strip()
            continue

        tag, value = m.group(1), m.group(2).strip()
        last_tag = tag

        if tag == "TI":
            current["TI"] = (current.get("TI", "") + (" " if current.get("TI") else "") + value).strip()
        elif tag == "AB":
            current["AB"] = (current.get("AB", "") + (" " if current.get("AB") else "") + value).strip()
        elif tag in ("FAU", "AU"):
            current.setdefault("FAU", []).append(value)
        elif tag in ("DP", "DEP"):
            year_match = re.search(r"\d{4}", value)
            if year_match and not current.get("DP"):
                current["DP"] = year_match.group(0)
        elif tag in ("JT", "TA"):
            if not current.get("JT"):
                current["JT"] = value
        elif tag in ("LID", "AID") and "[doi]" in value.lower():
            doi_val = re.sub(r"(?i)\s*\[doi\]\s*", "", value).strip()
            current.setdefault("DOI_list", []).append(doi_val)
        elif tag == "PMID":
            current["PMID"] = value.strip()

    flush()

    return records


def _nbib_record_to_unified(rec: dict, source_file: str, database: str, module: str,
                            warnings: list) -> dict:
    doi, doi_candidates, conflicting = resolve_doi_candidates(
        rec.get("DOI_list", []), source_file, warnings)
    return {
        "title": rec.get("TI", ""),
        "abstract": rec.get("AB", ""),
        "authors": "; ".join(rec.get("FAU", [])),
        "year": rec.get("DP", ""),
        "journal": rec.get("JT", ""),
        "DOI": doi,
        "doi_candidates": ";".join(doi_candidates),
        "multiple_conflicting_dois": conflicting,
        "PMID": rec.get("PMID", ""),
        "source_accession_id": "",
        "wos_accession_number": "",
        "scopus_eid": "",
        "database_source": database,
        "search_module": module,
        "source_file": source_file,
    }


def parse_bibtex(text: str, source_file: str, database: str, module: str,
                  warnings: list) -> list:
    """FALLBACK/EXPERIMENTAL parser. Not this toolkit's preferred production import
    format for any of the three target databases (see README §2)."""
    warnings.append(f"{source_file}: parsed with the fallback/experimental BibTeX parser, "
                    "not a preferred production format — verify output manually")
    records = []
    entries = re.findall(r"@\w+\s*\{[^,]+,(.*?)\n\}", text, re.DOTALL)
    for entry in entries:
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", entry, re.DOTALL):
            fields[fm.group(1).lower()] = re.sub(r"\s+", " ", fm.group(2)).strip()
        doi, doi_candidates, conflicting = resolve_doi_candidates(
            [fields["doi"]] if fields.get("doi") else [], source_file, warnings)
        records.append({
            "title": fields.get("title", ""),
            "abstract": fields.get("abstract", ""),
            "authors": fields.get("author", "").replace(" and ", "; "),
            "year": fields.get("year", ""),
            "journal": fields.get("journal", fields.get("booktitle", "")),
            "DOI": doi,
            "doi_candidates": ";".join(doi_candidates),
            "multiple_conflicting_dois": conflicting,
            "PMID": fields.get("pmid", ""),
            "source_accession_id": "", "wos_accession_number": "", "scopus_eid": "",
            "database_source": database,
            "search_module": module,
            "source_file": source_file,
        })
    return records


def parse_csv_export(path: Path, text: str, source_file: str, database: str, module: str,
                      logger: logging.Logger, warnings: list) -> list:
    """Generic CSV parser (used for Scopus exports). Tries common column-name variants,
    including "EID" for the Scopus persistent record identifier."""
    records = []
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        logger.warning("CSV file %s has no header row; skipping", path)
        return records

    def pick(row, *candidates):
        for c in candidates:
            for key in row:
                if key and key.strip().lower() == c.lower():
                    return row[key]
        return ""

    for row in reader:
        raw_doi = pick(row, "DOI", "DO")
        doi, doi_candidates, conflicting = resolve_doi_candidates(
            [raw_doi] if raw_doi else [], source_file, warnings)
        eid = pick(row, "EID")
        records.append({
            "title": pick(row, "Title", "Article Title", "TI"),
            "abstract": pick(row, "Abstract", "AB"),
            "authors": pick(row, "Authors", "Author full names", "AU"),
            "year": pick(row, "Year", "Publication Year", "PY"),
            "journal": pick(row, "Source title", "Journal", "SO"),
            "DOI": doi,
            "doi_candidates": ";".join(doi_candidates),
            "multiple_conflicting_dois": conflicting,
            "PMID": pick(row, "PubMed ID", "PMID"),
            "source_accession_id": "", "wos_accession_number": "",
            "scopus_eid": eid if database == "scopus" else "",
            "database_source": database,
            "search_module": module,
            "source_file": source_file,
        })
    return records


# ---------------------------------------------------------------------------
# Loading + parsing-quality reporting
# ---------------------------------------------------------------------------

def load_all_records(input_dir: Path, logger: logging.Logger):
    records = []
    quality_rows = []
    files_found = [p for p in sorted(input_dir.rglob("*"))
                    if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
                    and p.name != ".gitkeep"]

    if not files_found:
        return records, quality_rows

    for path in files_found:
        database = infer_database_from_path(path)
        module = infer_module_from_filename(path)
        unknown_database = database is None
        unknown_module = module is None
        database = database or "unknown"
        module = module or "unknown"

        if unknown_database:
            logger.warning("Could not infer database (wos/scopus/pubmed) from path %s — "
                           "place exports under data/raw/{wos,scopus,pubmed}/", path)
        if unknown_module:
            logger.warning("Could not infer search module from filename %s — expected "
                           "'core' or 'module02'..'module08' in the filename.", path)

        text = read_text_safely(path, logger)
        source_file = str(path)
        parser_warnings = []
        parse_status = "ok"
        try:
            if path.suffix.lower() == ".ris":
                recs = parse_ris(text, source_file, database, module, logger, parser_warnings)
            elif path.suffix.lower() == ".nbib":
                recs = parse_nbib(text, source_file, database, module, logger, parser_warnings)
            elif path.suffix.lower() == ".bib":
                recs = parse_bibtex(text, source_file, database, module, parser_warnings)
            elif path.suffix.lower() == ".csv":
                recs = parse_csv_export(path, text, source_file, database, module, logger, parser_warnings)
            else:
                continue
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to parse %s: %s", path, exc)
            quality_rows.append({
                "source_file": source_file, "database": database, "search_module": module,
                "records_parsed": 0, "missing_title": 0, "missing_abstract": 0,
                "missing_authors": 0, "missing_year": 0, "missing_DOI": 0, "missing_PMID": 0,
                "multiple_conflicting_dois_count": 0,
                "unknown_database": unknown_database, "unknown_module": unknown_module,
                "parser_warnings": f"PARSE FAILED: {exc}", "parse_status": "failed",
            })
            continue

        for w in parser_warnings:
            logger.warning(w)

        n = len(recs)
        missing_title = sum(1 for r in recs if not r.get("title"))
        missing_abstract = sum(1 for r in recs if not r.get("abstract"))
        missing_authors = sum(1 for r in recs if not r.get("authors"))
        missing_year = sum(1 for r in recs if not r.get("year"))
        missing_doi = sum(1 for r in recs if not r.get("DOI"))
        missing_pmid = sum(1 for r in recs if not r.get("PMID"))
        n_conflicting_doi = sum(1 for r in recs if r.get("multiple_conflicting_dois"))

        if n == 0:
            logger.warning("*** %s parsed to ZERO records. Check the export format and "
                           "that the file is not empty/corrupted. ***", path)
            parse_status = "zero_records"
        elif missing_title / n > 0.05:
            logger.warning("*** %s: %d/%d records (%.1f%%) are missing a title — exceeds "
                           "the 5%% threshold. Check the export's column mapping. ***",
                           path, missing_title, n, 100 * missing_title / n)
            parse_status = "high_missing_title"
        if n_conflicting_doi:
            logger.warning("*** %s: %d record(s) have MULTIPLE CONFLICTING DOI candidates "
                           "— these records' DOI field is left blank pending manual "
                           "review; see doi_candidates. ***", path, n_conflicting_doi)

        quality_rows.append({
            "source_file": source_file, "database": database, "search_module": module,
            "records_parsed": n, "missing_title": missing_title,
            "missing_abstract": missing_abstract, "missing_authors": missing_authors,
            "missing_year": missing_year, "missing_DOI": missing_doi,
            "missing_PMID": missing_pmid,
            "multiple_conflicting_dois_count": n_conflicting_doi,
            "unknown_database": unknown_database,
            "unknown_module": unknown_module, "parser_warnings": "; ".join(parser_warnings),
            "parse_status": parse_status,
        })

        missing_required = [r for r in recs if not all(r.get(f) for f in REQUIRED_FOR_DEDUP)]
        if missing_required:
            logger.warning("%d record(s) in %s are missing a title and cannot be reliably "
                           "deduplicated; they are still included in master_records.csv "
                           "but excluded from title-based matching.", len(missing_required), path)

        logger.info("Parsed %d record(s) from %s (database=%s, module=%s)",
                   n, path, database, module)
        records.extend(recs)

    return records, quality_rows


def write_parsing_quality_report(path: Path, quality_rows: list):
    fieldnames = ["source_file", "database", "search_module", "records_parsed",
                  "missing_title", "missing_abstract", "missing_authors", "missing_year",
                  "missing_DOI", "missing_PMID", "multiple_conflicting_dois_count",
                  "unknown_database", "unknown_module", "parser_warnings", "parse_status"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in quality_rows:
            writer.writerow(row)


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _new_master_record(r: dict) -> dict:
    """Build a fresh master-record view of an input record. Fields that a caller may
    have already populated on `r` BEFORE calling this (specifically the possible-
    duplicate flags set by add_possible_duplicate) are preserved via setdefault, not
    force-reset to empty — this function must not silently discard a flag the caller
    just set."""
    r = dict(r)
    r["database_sources"] = r["database_source"]
    r["search_modules"] = r["search_module"]
    r["source_files"] = r["source_file"]
    r["duplicate_record_ids"] = ""
    r["occurrence_count"] = 1
    r.setdefault("publication_version", detect_publication_version(r.get("title", ""), r.get("journal", "")))
    r.setdefault("possible_duplicate_of_record_id", "")
    r.setdefault("possible_version_relation", "")
    r.setdefault("duplicate_match_basis", "")
    r.setdefault("manual_duplicate_decision", "")
    r["_db_module_pairs"] = [(r["database_source"], r["search_module"])]
    return r


def _merge_into_master(master: dict, dup: dict, basis: str, logger: logging.Logger):
    """Aggregate a confirmed-duplicate record's provenance onto its master record,
    backfill any empty master fields from the duplicate, and log a metadata-discrepancy
    note if the two records' titles differ despite matching on DOI/PMID."""
    sources = set(master["database_sources"].split(";")) | {dup["database_source"]}
    master["database_sources"] = ";".join(sorted(s for s in sources if s))
    modules = set(master["search_modules"].split(";")) | {dup["search_module"]}
    master["search_modules"] = ";".join(sorted(m for m in modules if m))
    files = master["source_files"].split(";") if master["source_files"] else []
    files.append(dup["source_file"])
    master["source_files"] = ";".join(files)
    dup_ids = master["duplicate_record_ids"].split(";") if master["duplicate_record_ids"] else []
    dup_ids.append(dup["record_id"])
    master["duplicate_record_ids"] = ";".join(dup_ids)
    master["occurrence_count"] = int(master["occurrence_count"]) + 1
    master.setdefault("_db_module_pairs", []).append((dup["database_source"], dup["search_module"]))

    if basis in ("DOI", "PMID"):
        m_title = normalize_title(master.get("title", ""))
        d_title = normalize_title(dup.get("title", ""))
        if m_title and d_title and m_title != d_title:
            logger.warning("Metadata discrepancy: merged via %s but titles differ — "
                           "master='%s' vs incoming='%s' (record %s into %s)",
                           basis, master.get("title", ""), dup.get("title", ""),
                           dup["record_id"], master["record_id"])

    for field in ("title", "abstract", "authors", "year", "journal", "DOI", "PMID"):
        if not master.get(field) and dup.get(field):
            master[field] = dup[field]

    master["duplicate_match_basis"] = (master["duplicate_match_basis"] + ";" + basis
                                       if master["duplicate_match_basis"] else basis)


def deduplicate(records: list, logger: logging.Logger):
    for i, r in enumerate(records, start=1):
        raw_id = f"{r['database_source']}|{r['search_module']}|{r['source_file']}|{i}"
        r["record_id"] = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:12]
        r["_canonical_doi"] = canonicalize_doi(r.get("DOI", ""))
        r["_canonical_pmid"] = canonicalize_pmid(r.get("PMID", ""))
        r["_norm_title"] = normalize_title(r.get("title", ""))
        r["_first_author"] = first_author_surname(r.get("authors", ""))

    doi_index, pmid_index = {}, {}
    title_year_author_index = {}          # ONLY this title-based index may auto-merge (rule 3)
    title_year_index = {}                 # rule 4 candidates (possible_duplicate only)
    title_author_index = {}               # rule 5 candidates (possible_duplicate only)
    title_only_index = {}                 # rule 6 candidates + fuzzy-match pool (rule 7)

    master_by_id = {}
    master_order = []
    confirmed_duplicates = []
    possible_duplicates = []

    def index_master(m: dict):
        """Also used as reindex_master(): safe to call repeatedly — setdefault only
        adds keys that are not already claimed, so re-indexing after a backfill only
        adds the newly-available DOI/PMID/title/author keys, never overwrites an
        existing claim (which would indicate a genuine conflict, not a backfill)."""
        master_by_id[m["record_id"]] = m
        doi = canonicalize_doi(m.get("DOI", ""))
        pmid = canonicalize_pmid(m.get("PMID", ""))
        norm_title = normalize_title(m.get("title", ""))
        first_author = first_author_surname(m.get("authors", ""))
        m["_canonical_doi"], m["_canonical_pmid"] = doi, pmid
        m["_norm_title"], m["_first_author"] = norm_title, first_author
        if doi:
            doi_index.setdefault(doi, m["record_id"])
        if pmid:
            pmid_index.setdefault(pmid, m["record_id"])
        if norm_title:
            if m.get("year") and first_author:
                title_year_author_index.setdefault((norm_title, m["year"], first_author), m["record_id"])
            if m.get("year"):
                title_year_index.setdefault((norm_title, m["year"]), []).append(m["record_id"])
            if first_author:
                title_author_index.setdefault((norm_title, first_author), []).append(m["record_id"])
            title_only_index.setdefault(norm_title, []).append(m["record_id"])

    reindex_master = index_master  # explicit alias so call sites read as intent, not accident

    def add_possible_duplicate(r: dict, candidate_id: str, relation: str, basis: str):
        r["possible_duplicate_of_record_id"] = candidate_id
        r["possible_version_relation"] = relation
        r["duplicate_match_basis"] = basis
        r["publication_version"] = detect_publication_version(r.get("title", ""), r.get("journal", ""))
        possible_duplicates.append(r)
        new_master = _new_master_record(r)
        index_master(new_master)
        master_order.append(new_master["record_id"])

    for r in records:
        doi, pmid = r["_canonical_doi"], r["_canonical_pmid"]
        norm_title, year, first_author = r["_norm_title"], r.get("year", ""), r["_first_author"]

        # --- Rule 1: canonical DOI exact match -> always auto-merge ---
        if doi and doi in doi_index:
            master = master_by_id[doi_index[doi]]
            _merge_into_master(master, r, "DOI", logger)
            confirmed_duplicates.append({**r, "duplicate_of_record_id": master["record_id"],
                                        "duplicate_match_basis": "DOI"})
            reindex_master(master)
            continue

        # --- Rule 2: canonical PMID exact match -> always auto-merge ---
        if pmid and pmid in pmid_index:
            master = master_by_id[pmid_index[pmid]]
            _merge_into_master(master, r, "PMID", logger)
            confirmed_duplicates.append({**r, "duplicate_of_record_id": master["record_id"],
                                        "duplicate_match_basis": "PMID"})
            reindex_master(master)
            continue

        # --- Rule 3: title + year + first author -> auto-merge ONLY if no identifier
        #     conflict and no version conflict; otherwise downgrade to possible_duplicate ---
        if norm_title and year and first_author and \
                (norm_title, year, first_author) in title_year_author_index:
            candidate_id = title_year_author_index[(norm_title, year, first_author)]
            candidate = master_by_id[candidate_id]

            conflict, reason = identifier_conflict(r, candidate)
            if conflict:
                logger.warning("Title+year+author match blocked by identifier conflict "
                               "(%s) between incoming record and master %s — flagged "
                               "possible_duplicate, not merged.", reason, candidate_id)
                add_possible_duplicate(r, candidate_id, "conflicting_persistent_identifiers",
                                       "title_year_first_author")
                continue

            r_version = detect_publication_version(r.get("title", ""), r.get("journal", ""))
            c_version = candidate["publication_version"]
            if version_conflict(r_version, c_version):
                add_possible_duplicate(r, candidate_id, f"{c_version}_vs_{r_version}",
                                       "title_year_first_author")
                continue

            _merge_into_master(candidate, r, "title_year_first_author", logger)
            confirmed_duplicates.append({**r, "duplicate_of_record_id": candidate_id,
                                        "duplicate_match_basis": "title_year_first_author"})
            reindex_master(candidate)
            continue

        # --- Rules 4-7: NEVER auto-merge. Each creates its own master record, flagged
        #     possible_duplicate against the strongest-available weaker match. ---
        if norm_title and year and (norm_title, year) in title_year_index:
            add_possible_duplicate(r, title_year_index[(norm_title, year)][0],
                                   "title_year_match_author_missing_or_different", "title_year")
            continue

        if norm_title and first_author and (norm_title, first_author) in title_author_index:
            add_possible_duplicate(r, title_author_index[(norm_title, first_author)][0],
                                   "title_author_match_year_missing_or_different", "title_author")
            continue

        if norm_title and norm_title in title_only_index:
            add_possible_duplicate(r, title_only_index[norm_title][0],
                                   "identical_title_insufficient_other_metadata", "title_only")
            continue

        fuzzy_hit = None
        if norm_title:
            title_tokens = set(norm_title.split())
            if len(title_tokens) >= 4:
                for mid in master_order:
                    m = master_by_id[mid]
                    m_tokens = set(m.get("_norm_title", "").split())
                    if not m_tokens:
                        continue
                    overlap = len(title_tokens & m_tokens) / max(len(title_tokens | m_tokens), 1)
                    if overlap >= 0.8 and r.get("year") == m.get("year"):
                        fuzzy_hit = mid
                        break
        if fuzzy_hit:
            add_possible_duplicate(r, fuzzy_hit, "fuzzy_title_overlap_ge_0.8_same_year", "fuzzy_title")
            continue

        # --- No match at all: brand new master record ---
        new_master = _new_master_record(r)
        index_master(new_master)
        master_order.append(new_master["record_id"])

    master = [master_by_id[mid] for mid in master_order]

    logger.info("Deduplication complete: %d input records -> %d master, %d confirmed "
               "duplicates merged, %d flagged possible duplicates (retained as separate "
               "master entries, NOT auto-merged)",
               len(records), len(master), len(confirmed_duplicates), len(possible_duplicates))

    return master, confirmed_duplicates, possible_duplicates


def write_csv(path: Path, rows: list, fieldnames: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_database_module_summary(path: Path, records: list, master: list,
                                  confirmed_duplicates: list):
    """Derived from the ORIGINAL INPUT records, not from master's aggregated provenance
    fields — each input record is counted exactly once, by its own (database_source,
    search_module) pair, as either "became/contributed to a master record" or "was
    merged away as a confirmed duplicate". This is what makes the §VIII integrity
    cross-check (summary totals == original input counts per pair) hold by
    construction, and avoids double-counting a record that both contributed to a
    master's aggregated database_sources/search_modules AND has its own
    confirmed_duplicates row for the same (database, module) pair."""
    master_ids = {m["record_id"] for m in master}
    summary = {}
    for r in records:
        key = (r["database_source"], r["search_module"])
        summary.setdefault(key, {"database": key[0], "search_module": key[1],
                                  "records_in_master": 0, "records_as_duplicates": 0})
        if r["record_id"] in master_ids:
            summary[key]["records_in_master"] += 1
        else:
            summary[key]["records_as_duplicates"] += 1

    rows = sorted(summary.values(), key=lambda x: (x["database"], x["search_module"]))
    write_csv(path, rows, ["database", "search_module", "records_in_master", "records_as_duplicates"])
    return summary


# ---------------------------------------------------------------------------
# Post-deduplication integrity check
# ---------------------------------------------------------------------------

def run_integrity_check(records: list, master: list, confirmed_duplicates: list,
                        db_module_summary: dict, logger: logging.Logger):
    """Verifies structural invariants that must hold regardless of input content:
        input_records == master_records + confirmed_duplicates   (possible_duplicates
            are a subset of master, already counted there — never added separately)
        every input record appears exactly once across (master U confirmed_duplicates)
        every confirmed_duplicate's duplicate_of_record_id resolves to a real master
        every master's occurrence_count matches its aggregated duplicate_record_ids + 1
        no circular/chained duplicate_of relationships
        the (database, module) summary accounts for exactly the original input records
    Returns (status, issues) where status in {"PASS", "PASS_WITH_WARNINGS", "FAIL"}.
    """
    issues = []  # (severity, message)

    if len(records) != len(master) + len(confirmed_duplicates):
        issues.append(("FAIL", f"input_records ({len(records)}) != master_records "
                       f"({len(master)}) + confirmed_duplicates ({len(confirmed_duplicates)})"))

    master_ids = {m["record_id"] for m in master}
    if len(master_ids) != len(master):
        issues.append(("FAIL", "Duplicate record_id values found within master_records.csv itself."))

    accounted_ids = set(master_ids)
    for d in confirmed_duplicates:
        rid = d["record_id"]
        if rid in accounted_ids:
            issues.append(("FAIL", f"record_id {rid} appears more than once across "
                           "master_records.csv and confirmed_duplicates.csv."))
        accounted_ids.add(rid)

    input_ids = {r["record_id"] for r in records}
    missing_ids = input_ids - accounted_ids
    if missing_ids:
        issues.append(("FAIL", f"{len(missing_ids)} input record(s) are not accounted for "
                       f"in either master_records.csv or confirmed_duplicates.csv: "
                       f"{sorted(missing_ids)[:5]}{'...' if len(missing_ids) > 5 else ''}"))
    extra_ids = accounted_ids - input_ids
    if extra_ids:
        issues.append(("FAIL", f"{len(extra_ids)} record_id(s) in the output do not "
                       f"correspond to any input record (possible corruption): "
                       f"{sorted(extra_ids)[:5]}"))

    for d in confirmed_duplicates:
        target = d.get("duplicate_of_record_id", "")
        if target not in master_ids:
            issues.append(("FAIL", f"confirmed_duplicates row {d['record_id']} points to "
                           f"duplicate_of_record_id='{target}', which is not a real "
                           "master record (dangling or chained reference)."))

    for d in confirmed_duplicates:
        target = d.get("duplicate_of_record_id", "")
        if target in {dd["record_id"] for dd in confirmed_duplicates}:
            issues.append(("FAIL", f"Chained duplicate relationship detected: "
                           f"{d['record_id']} -> {target}, but {target} is itself a "
                           "confirmed_duplicates row, not a master. Duplicates must "
                           "always point directly to a master record."))

    for m in master:
        dup_ids = m["duplicate_record_ids"].split(";") if m["duplicate_record_ids"] else []
        expected_count = len(dup_ids) + 1
        actual_count = int(m["occurrence_count"])
        if expected_count != actual_count:
            issues.append(("FAIL", f"master {m['record_id']}: occurrence_count="
                           f"{actual_count} but duplicate_record_ids implies "
                           f"{expected_count}."))
        cd_for_this_master = {d["record_id"] for d in confirmed_duplicates
                              if d.get("duplicate_of_record_id") == m["record_id"]}
        if cd_for_this_master != set(dup_ids):
            issues.append(("WARNING", f"master {m['record_id']}: duplicate_record_ids "
                           f"{sorted(dup_ids)} does not exactly match the set of "
                           f"confirmed_duplicates rows pointing to it "
                           f"{sorted(cd_for_this_master)}."))

    input_pair_counts = {}
    for r in records:
        key = (r["database_source"], r["search_module"])
        input_pair_counts[key] = input_pair_counts.get(key, 0) + 1
    summary_pair_totals = {}
    for key, v in db_module_summary.items():
        summary_pair_totals[key] = v["records_in_master"] + v["records_as_duplicates"]
    for key, count in input_pair_counts.items():
        summary_count = summary_pair_totals.get(key, 0)
        if summary_count != count:
            issues.append(("WARNING", f"database_module_summary total for {key} "
                           f"({summary_count}) does not match the actual input record "
                           f"count for that pair ({count})."))

    n_fail = sum(1 for sev, _ in issues if sev == "FAIL")
    n_warn = sum(1 for sev, _ in issues if sev == "WARNING")
    if n_fail > 0:
        status = "FAIL"
    elif n_warn > 0:
        status = "PASS_WITH_WARNINGS"
    else:
        status = "PASS"

    for sev, msg in issues:
        (logger.error if sev == "FAIL" else logger.warning)("[INTEGRITY %s] %s", sev, msg)
    logger.info("Integrity check status: %s (%d fail, %d warning)", status, n_fail, n_warn)

    return status, issues


def write_integrity_report(path_md: Path, path_csv: Path, status: str, issues: list,
                           records: list, master: list, confirmed_duplicates: list,
                           possible_duplicates: list):
    path_md.parent.mkdir(parents=True, exist_ok=True)
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["severity", "message"])
        for sev, msg in issues:
            writer.writerow([sev, msg])

    with open(path_md, "w", encoding="utf-8") as f:
        f.write("# Deduplication Integrity Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"## STATUS: {status}\n\n")
        f.write(f"- Input records: {len(records)}\n")
        f.write(f"- Master records: {len(master)}\n")
        f.write(f"- Confirmed duplicates (merged): {len(confirmed_duplicates)}\n")
        f.write(f"- Possible duplicates (retained as separate flagged master entries, "
                f"NOT additive to the input=master+confirmed equation): {len(possible_duplicates)}\n")
        f.write(f"- input_records == master_records + confirmed_duplicates: "
                f"{len(records) == len(master) + len(confirmed_duplicates)}\n\n")
        if status == "FAIL":
            f.write("**This output FAILED its internal integrity check and must NOT be "
                    "used for screening, PRISMA counting, or any downstream step until "
                    "the issues below are resolved.**\n\n")
        if issues:
            f.write("## Issues\n\n")
            for sev, msg in issues:
                f.write(f"- **[{sev}]** {msg}\n")
        else:
            f.write("No issues found.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate WoS/Scopus/PubMed bibliographic exports (RIS/CSV/NBIB; "
                    "BibTeX supported only as a fallback/experimental parser). Only "
                    "DOI-exact, PMID-exact, and title+year+first-author-exact (with no "
                    "identifier or version conflict) matches are auto-merged.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--log-dir", type=Path, default=Path("logs"))
    args = parser.parse_args()

    logger = setup_logger(args.log_dir)
    logger.info("deduplicate_records.py starting")
    logger.info("input-dir=%s output-dir=%s", args.input_dir, args.output_dir)

    if not args.input_dir.exists():
        logger.error("Input directory %s does not exist. Nothing to do.", args.input_dir)
        sys.exit(1)

    records, quality_rows = load_all_records(args.input_dir, logger)

    if not records:
        logger.warning(
            "No real export files (.ris/.csv/.nbib/.bib) were found under %s. This "
            "script will not fabricate deduplication results. Populate "
            "data/raw/{wos,scopus,pubmed}/ with real database exports and re-run. "
            "Exiting safely with no output written.",
            args.input_dir,
        )
        sys.exit(0)

    write_parsing_quality_report(args.output_dir / "parsing_quality_report.csv", quality_rows)

    master, confirmed_duplicates, possible_duplicates = deduplicate(records, logger)

    master_fieldnames = UNIFIED_FIELDS + MASTER_EXTRA_FIELDS
    dup_fieldnames = UNIFIED_FIELDS + ["duplicate_of_record_id", "duplicate_match_basis"]
    possible_fieldnames = UNIFIED_FIELDS + MASTER_EXTRA_FIELDS

    write_csv(args.output_dir / "master_records.csv", master, master_fieldnames)
    write_csv(args.output_dir / "confirmed_duplicates.csv", confirmed_duplicates, dup_fieldnames)
    write_csv(args.output_dir / "possible_duplicates.csv", possible_duplicates, possible_fieldnames)
    db_module_summary = write_database_module_summary(
        args.output_dir / "database_module_summary.csv", records, master, confirmed_duplicates)

    log_summary_path = args.output_dir / "deduplication_log.txt"
    with open(log_summary_path, "w", encoding="utf-8") as f:
        f.write(f"Deduplication run: {datetime.now().isoformat()}\n")
        f.write(f"Input directory: {args.input_dir}\n")
        f.write(f"Total input records parsed: {len(records)}\n")
        f.write(f"Master (unique) records: {len(master)}\n")
        f.write(f"Confirmed duplicates merged into master: {len(confirmed_duplicates)}\n")
        f.write(f"Possible duplicates flagged (retained as separate master entries, "
                f"NOT auto-merged): {len(possible_duplicates)}\n")
        n_multi_source = sum(1 for m in master if int(m["occurrence_count"]) > 1)
        f.write(f"Master records confirmed present in more than one source file/database: "
                f"{n_multi_source}\n")

    status, issues = run_integrity_check(records, master, confirmed_duplicates,
                                         db_module_summary, logger)
    write_integrity_report(args.output_dir / "deduplication_integrity_report.md",
                           args.output_dir / "deduplication_integrity_report.csv",
                           status, issues, records, master, confirmed_duplicates,
                           possible_duplicates)

    logger.info("Wrote outputs to %s", args.output_dir)
    logger.info("master_records.csv: %d rows", len(master))
    logger.info("confirmed_duplicates.csv: %d rows", len(confirmed_duplicates))
    logger.info("possible_duplicates.csv: %d rows (flagged only, retained, not auto-merged)",
               len(possible_duplicates))
    logger.info("parsing_quality_report.csv written for %d source file(s)", len(quality_rows))

    if status == "FAIL":
        logger.error("Deduplication integrity check FAILED — see "
                     "deduplication_integrity_report.md. This output must not be used "
                     "for screening or PRISMA counting until resolved.")
        sys.exit(2)

    logger.info("deduplicate_records.py finished successfully")


if __name__ == "__main__":
    main()
