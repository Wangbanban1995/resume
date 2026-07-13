#!/usr/bin/env python3
"""Deduplicate bibliographic records exported from Web of Science, Scopus, and PubMed.

Reads RIS (.ris), Scopus CSV (.csv), NBIB (.nbib), and BibTeX (.bib, fallback/experimental
parser only) files from an input directory tree, normalizes them to a common schema, and
deduplicates by canonical DOI, then canonical PMID, then normalized-title+year, then
normalized-title+first-author, then normalized-title+year+first-author. Matches based on
title alone (not DOI/PMID) are screened for likely different-version pairs (correction/
erratum, protocol vs. results, conference abstract vs. journal article, preprint vs.
published) before being auto-merged; a version conflict signal downgrades an otherwise-
matching pair to a flagged `possible_duplicate` instead of an automatic merge. Records
matching by title alone with mismatched year AND mismatched first author are also never
auto-merged.

This script does not invent, estimate, or guess at search results. If no real input
files are found, it exits with a clear message and produces no output claiming to be
real data.

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
FALLBACK_EXTENSIONS = {".bib"}  # BibTeX: fallback/experimental parser, not a preferred format

UNIFIED_FIELDS = [
    "record_id", "title", "abstract", "authors", "year", "journal",
    "DOI", "PMID", "database_source", "search_module", "source_file",
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
    """Read a file trying utf-8-sig, then utf-8, then latin-1, logging what happened."""
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
    a trailing "[doi]" tag (as seen in NBIB AID/LID fields), and trailing
    "." "," ";" ")" "]" punctuation. Returns "" for an empty/missing input.
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
    """Normalize a PMID to a bare numeric string, or "" if the value is not a plausible
    PMID (e.g., a WoS accession number like "WOS:000123456789" must NOT be misread as a
    PMID — this function requires the cleaned value to be purely numeric).
    """
    if not value:
        return ""
    v = value.strip()
    v = re.sub(r"(?i)^pmid:?\s*", "", v).strip()
    if re.fullmatch(r"\d+", v):
        return v
    return ""


def normalize_title(title: str) -> str:
    t = (title or "").lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)  # punctuation (including hyphens) becomes a space, not deleted
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
    """Classify a record's likely version/type from title and journal/source text alone.

    This is a heuristic safety net for avoiding false merges, not a definitive
    classification — real screening should confirm it (see `manual_duplicate_decision`).
    """
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
    """True if two publication_version labels indicate records that should NOT be
    silently auto-merged even if their titles (and possibly year/author) match."""
    if version_a == version_b:
        return False
    # Any pairing where exactly one side is flagged as a distinct version type
    # (and the other is an unclassified/primary record) is a potential different-version
    # pair, per instruction: correction/erratum, protocol/results, conference/journal,
    # preprint/published must never be silently merged.
    flagged = {"correction_or_erratum", "protocol", "preprint", "conference_abstract"}
    if version_a in flagged or version_b in flagged:
        return True
    return False


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
    return None  # unknown - caller must log this prominently


def infer_module_from_filename(path: Path):
    m = re.search(r"(core|module0[2-8])", path.stem, re.IGNORECASE)
    return m.group(1).lower() if m else None  # unknown - caller must log this prominently


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

RIS_MULTILINE_TAGS = {"TI", "T1", "AB", "N2"}


def parse_ris(text: str, source_file: str, database: str, module: str, logger: logging.Logger,
              warnings: list) -> list:
    """RIS parser supporting continuation lines (title/abstract wrapped across multiple
    physical lines), multiple authors, multiple DO fields (first non-empty wins, later
    ones logged), TI/T1, AB/N2, JO/JF/T2, PY/Y1/DA, and a missing terminal ER tag (a new
    TY flushes any pending record automatically rather than losing it)."""
    records = []
    current = {}
    last_tag = None

    def flush():
        if current:
            records.append(_ris_record_to_unified(dict(current), source_file, database, module))

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if not line.strip():
            last_tag = None
            continue

        m = re.match(r"^([A-Z][A-Z0-9])\s{0,2}-\s?(.*)$", line)
        if not m:
            # Continuation line: append to the last multi-line-capable field, if any.
            if last_tag in RIS_MULTILINE_TAGS:
                key = "title" if last_tag in ("TI", "T1") else "abstract"
                current[key] = (current.get(key, "") + " " + line.strip()).strip()
            elif last_tag is not None:
                pass  # continuation of a non-multiline field (e.g., a wrapped author list); ignore safely
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
            if not current.get("DOI"):
                current["DOI"] = value.strip()
            else:
                warnings.append(f"{source_file}: multiple DO fields encountered for one "
                                f"record; kept the first ('{current['DOI']}'), ignored "
                                f"subsequent value ('{value.strip()}')")
        elif tag == "AN" and re.match(r"^\d+$", value):
            current.setdefault("PMID", value)

    flush()  # handle a file missing its final ER tag

    return records


def _ris_record_to_unified(rec: dict, source_file: str, database: str, module: str) -> dict:
    return {
        "title": rec.get("title", ""),
        "abstract": rec.get("abstract", ""),
        "authors": "; ".join(rec.get("authors", [])),
        "year": rec.get("year", ""),
        "journal": rec.get("journal", ""),
        "DOI": rec.get("DOI", ""),
        "PMID": rec.get("PMID", ""),
        "database_source": database,
        "search_module": module,
        "source_file": source_file,
    }


NBIB_MULTILINE_TAGS = {"TI", "AB"}


def parse_nbib(text: str, source_file: str, database: str, module: str, logger: logging.Logger,
               warnings: list) -> list:
    """PubMed NBIB parser. Supports continuation lines for TI/AB (PubMed wraps long
    values onto subsequent lines indented with 6 spaces, no tag), FAU/AU, DP/DEP,
    JT/TA, DOI recovery from AID or LID ("... [doi]"), and multi-paragraph abstracts
    (consecutive AB-tagged lines within one record are concatenated, not overwritten)."""
    records = []
    current = {}
    last_tag = None

    def flush():
        if current:
            records.append(_nbib_record_to_unified(dict(current), source_file, database, module))

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
            if not current.get("DOI"):
                current["DOI"] = doi_val
            elif current["DOI"] != doi_val:
                warnings.append(f"{source_file}: multiple distinct DOI-like values in "
                                f"AID/LID fields for one record; kept the first "
                                f"('{current['DOI']}'), ignored ('{doi_val}')")
        elif tag == "PMID":
            current["PMID"] = value.strip()

    flush()  # handle a file whose last record has no trailing blank line

    return records


def _nbib_record_to_unified(rec: dict, source_file: str, database: str, module: str) -> dict:
    return {
        "title": rec.get("TI", ""),
        "abstract": rec.get("AB", ""),
        "authors": "; ".join(rec.get("FAU", [])),
        "year": rec.get("DP", ""),
        "journal": rec.get("JT", ""),
        "DOI": rec.get("DOI", ""),
        "PMID": rec.get("PMID", ""),
        "database_source": database,
        "search_module": module,
        "source_file": source_file,
    }


def parse_bibtex(text: str, source_file: str, database: str, module: str,
                  warnings: list) -> list:
    """FALLBACK/EXPERIMENTAL parser. BibTeX is not this toolkit's preferred production
    import format (see README) — it is not guaranteed to handle every real-world BibTeX
    export correctly (nested braces, multi-line unquoted fields, and unusual entry
    syntax are known gaps). Use RIS (WoS), CSV (Scopus), or NBIB (PubMed) instead
    whenever the source system offers them."""
    warnings.append(f"{source_file}: parsed with the fallback/experimental BibTeX parser, "
                    "not a preferred production format — verify output manually")
    records = []
    entries = re.findall(r"@\w+\s*\{[^,]+,(.*?)\n\}", text, re.DOTALL)
    for entry in entries:
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", entry, re.DOTALL):
            fields[fm.group(1).lower()] = re.sub(r"\s+", " ", fm.group(2)).strip()
        records.append({
            "title": fields.get("title", ""),
            "abstract": fields.get("abstract", ""),
            "authors": fields.get("author", "").replace(" and ", "; "),
            "year": fields.get("year", ""),
            "journal": fields.get("journal", fields.get("booktitle", "")),
            "DOI": fields.get("doi", ""),
            "PMID": fields.get("pmid", ""),
            "database_source": database,
            "search_module": module,
            "source_file": source_file,
        })
    return records


def parse_csv_export(path: Path, text: str, source_file: str, database: str, module: str,
                      logger: logging.Logger) -> list:
    """Generic CSV parser (used for Scopus exports). Tries common column-name variants."""
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
        records.append({
            "title": pick(row, "Title", "Article Title", "TI"),
            "abstract": pick(row, "Abstract", "AB"),
            "authors": pick(row, "Authors", "Author full names", "AU"),
            "year": pick(row, "Year", "Publication Year", "PY"),
            "journal": pick(row, "Source title", "Journal", "SO"),
            "DOI": pick(row, "DOI", "DO"),
            "PMID": pick(row, "PubMed ID", "PMID"),
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
                           "'core' or 'module02'..'module08' in the filename per the "
                           "naming convention in README.md", path)

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
                recs = parse_csv_export(path, text, source_file, database, module, logger)
            else:
                continue
        except Exception as exc:  # noqa: BLE001 - log and continue, don't crash the whole run
            logger.error("Failed to parse %s: %s", path, exc)
            quality_rows.append({
                "source_file": source_file, "database": database, "search_module": module,
                "records_parsed": 0, "missing_title": 0, "missing_abstract": 0,
                "missing_authors": 0, "missing_year": 0, "missing_DOI": 0, "missing_PMID": 0,
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

        if n == 0:
            logger.warning("*** %s parsed to ZERO records. Check the export format and "
                           "that the file is not empty/corrupted. ***", path)
            parse_status = "zero_records"
        elif missing_title / n > 0.05:
            logger.warning("*** %s: %d/%d records (%.1f%%) are missing a title — exceeds "
                           "the 5%% threshold. Check the export's column mapping. ***",
                           path, missing_title, n, 100 * missing_title / n)
            parse_status = "high_missing_title"

        quality_rows.append({
            "source_file": source_file, "database": database, "search_module": module,
            "records_parsed": n, "missing_title": missing_title,
            "missing_abstract": missing_abstract, "missing_authors": missing_authors,
            "missing_year": missing_year, "missing_DOI": missing_doi,
            "missing_PMID": missing_pmid, "unknown_database": unknown_database,
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
                  "missing_DOI", "missing_PMID", "unknown_database", "unknown_module",
                  "parser_warnings", "parse_status"]
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
    r = dict(r)
    r["database_sources"] = r["database_source"]
    r["search_modules"] = r["search_module"]
    r["source_files"] = r["source_file"]
    r["duplicate_record_ids"] = ""
    r["occurrence_count"] = 1
    r["publication_version"] = detect_publication_version(r.get("title", ""), r.get("journal", ""))
    r["possible_duplicate_of_record_id"] = ""
    r["possible_version_relation"] = ""
    r["duplicate_match_basis"] = ""
    r["manual_duplicate_decision"] = ""
    # Internal-only (not written to CSV): exact (database, module) pairs this master
    # record was actually seen under, preserving correct pairwise attribution — do NOT
    # derive this from the cartesian product of database_sources x search_modules,
    # since a record present via wos/core and scopus/module05 is NOT also evidence of
    # a wos/module05 or scopus/core occurrence.
    r["_db_module_pairs"] = [(r["database_source"], r["search_module"])]
    return r


def _merge_into_master(master: dict, dup: dict, basis: str):
    """Aggregate a confirmed-duplicate record's provenance onto its master record and
    backfill any empty master fields from the duplicate (richer-record backfill)."""
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
    title_year_index, title_author_index, title_year_author_index = {}, {}, {}
    title_only_index = {}  # norm_title -> list of master record_ids sharing this exact title

    master_by_id = {}
    master_order = []
    confirmed_duplicates = []
    possible_duplicates = []

    def index_master(m: dict):
        master_by_id[m["record_id"]] = m
        if m["_canonical_doi"]:
            doi_index.setdefault(m["_canonical_doi"], m["record_id"])
        if m["_canonical_pmid"]:
            pmid_index.setdefault(m["_canonical_pmid"], m["record_id"])
        if m["_norm_title"]:
            if m.get("year"):
                title_year_index.setdefault((m["_norm_title"], m["year"]), m["record_id"])
            if m.get("_first_author"):
                title_author_index.setdefault((m["_norm_title"], m["_first_author"]), m["record_id"])
            if m.get("year") and m.get("_first_author"):
                title_year_author_index.setdefault(
                    (m["_norm_title"], m["year"], m["_first_author"]), m["record_id"])
            title_only_index.setdefault(m["_norm_title"], []).append(m["record_id"])

    for r in records:
        doi, pmid = r["_canonical_doi"], r["_canonical_pmid"]
        norm_title, year, first_author = r["_norm_title"], r.get("year", ""), r["_first_author"]

        match_id, basis, title_based = None, None, False

        if doi and doi in doi_index:
            match_id, basis = doi_index[doi], "DOI"
        elif pmid and pmid in pmid_index:
            match_id, basis = pmid_index[pmid], "PMID"
        elif norm_title and year and (norm_title, year) in title_year_index:
            match_id, basis, title_based = title_year_index[(norm_title, year)], "title_year", True
        elif norm_title and first_author and (norm_title, first_author) in title_author_index:
            match_id, basis, title_based = title_author_index[(norm_title, first_author)], "title_first_author", True
        elif norm_title and year and first_author and (norm_title, year, first_author) in title_year_author_index:
            match_id, basis, title_based = title_year_author_index[(norm_title, year, first_author)], "title_year_first_author", True

        if match_id is not None:
            master = master_by_id[match_id]

            if title_based:
                r_version = detect_publication_version(r.get("title", ""), r.get("journal", ""))
                m_version = master["publication_version"]
                if version_conflict(r_version, m_version):
                    r["possible_duplicate_of_record_id"] = match_id
                    r["possible_version_relation"] = f"{m_version}_vs_{r_version}"
                    r["duplicate_match_basis"] = basis
                    r["publication_version"] = r_version
                    possible_duplicates.append(r)
                    index_master(_new_master_record(r))
                    master_order.append(r["record_id"])
                    continue

            _merge_into_master(master, r, basis)
            confirmed_duplicates.append({**r, "duplicate_of_record_id": match_id,
                                        "duplicate_match_basis": basis})
            continue

        # No DOI/PMID/title+field match. Check: same exact title, but neither year nor
        # first_author matched anything on file for that title -> if the title is known
        # under a DIFFERENT year+author combination, this is the explicit
        # "title identical, year AND author both differ" case: never auto-merge.
        if norm_title and norm_title in title_only_index:
            existing_id = title_only_index[norm_title][0]
            existing = master_by_id[existing_id]
            r["possible_duplicate_of_record_id"] = existing_id
            r["possible_version_relation"] = "identical_title_year_and_author_both_differ"
            r["duplicate_match_basis"] = "title_only"
            r["publication_version"] = detect_publication_version(r.get("title", ""), r.get("journal", ""))
            possible_duplicates.append(r)
            index_master(_new_master_record(r))
            master_order.append(r["record_id"])
            continue

        # Fuzzy title overlap against existing masters (kept as final fallback), still
        # possible_duplicate only, never auto-removed.
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

        new_master = _new_master_record(r)
        if fuzzy_hit:
            new_master["possible_duplicate_of_record_id"] = fuzzy_hit
            new_master["possible_version_relation"] = "fuzzy_title_overlap_ge_0.8_same_year"
            new_master["duplicate_match_basis"] = "fuzzy_title"
            possible_duplicates.append(new_master)

        index_master(new_master)
        master_order.append(new_master["record_id"])

    master = [master_by_id[mid] for mid in master_order]

    n_possible = len(possible_duplicates)
    logger.info("Deduplication complete: %d input records -> %d master, %d confirmed "
               "duplicates merged, %d flagged possible duplicates (retained in master, "
               "NOT auto-removed, NOT auto-merged)",
               len(records), len(master), len(confirmed_duplicates), n_possible)

    return master, confirmed_duplicates, possible_duplicates


def write_csv(path: Path, rows: list, fieldnames: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_database_module_summary(path: Path, master: list, confirmed_duplicates: list):
    """Uses each master record's exact (database, module) occurrence pairs, NOT the
    cartesian product of its database_sources and search_modules lists — a record seen
    via wos/core and scopus/module05 must not be counted as evidence of a wos/module05
    or scopus/core occurrence, which never happened."""
    summary = {}
    for r in master:
        pairs = r.get("_db_module_pairs") or [(r["database_source"], r["search_module"])]
        for db, mod in set(pairs):  # a record counts once per distinct (db, module) pair
            key = (db, mod)
            summary.setdefault(key, {"database": db, "search_module": mod,
                                      "records_in_master": 0, "records_as_duplicates": 0})
            summary[key]["records_in_master"] += 1
    for r in confirmed_duplicates:
        key = (r["database_source"], r["search_module"])
        summary.setdefault(key, {"database": key[0], "search_module": key[1],
                                  "records_in_master": 0, "records_as_duplicates": 0})
        summary[key]["records_as_duplicates"] += 1

    rows = sorted(summary.values(), key=lambda x: (x["database"], x["search_module"]))
    write_csv(path, rows, ["database", "search_module", "records_in_master", "records_as_duplicates"])


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate WoS/Scopus/PubMed bibliographic exports (RIS/CSV/NBIB; "
                    "BibTeX supported only as a fallback/experimental parser).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input-dir", type=Path, default=Path("data/raw"),
                        help="Directory tree containing raw exports (searched recursively)")
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"),
                        help="Directory to write master_records.csv and related outputs")
    parser.add_argument("--log-dir", type=Path, default=Path("logs"),
                        help="Directory to write the run log")
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
    write_database_module_summary(args.output_dir / "database_module_summary.csv",
                                   master, confirmed_duplicates)

    log_summary_path = args.output_dir / "deduplication_log.txt"
    with open(log_summary_path, "w", encoding="utf-8") as f:
        f.write(f"Deduplication run: {datetime.now().isoformat()}\n")
        f.write(f"Input directory: {args.input_dir}\n")
        f.write(f"Total input records parsed: {len(records)}\n")
        f.write(f"Master (unique) records: {len(master)}\n")
        f.write(f"Confirmed duplicates merged into master: {len(confirmed_duplicates)}\n")
        f.write(f"Possible duplicates flagged (retained as separate master entries, "
                f"NOT auto-merged, NOT auto-removed): {len(possible_duplicates)}\n")
        n_multi_source = sum(1 for m in master if int(m["occurrence_count"]) > 1)
        f.write(f"Master records confirmed present in more than one source file/database: "
                f"{n_multi_source}\n")

    logger.info("Wrote outputs to %s", args.output_dir)
    logger.info("master_records.csv: %d rows", len(master))
    logger.info("confirmed_duplicates.csv: %d rows", len(confirmed_duplicates))
    logger.info("possible_duplicates.csv: %d rows (flagged only, retained, not auto-merged)",
               len(possible_duplicates))
    logger.info("parsing_quality_report.csv written for %d source file(s)", len(quality_rows))
    logger.info("deduplicate_records.py finished successfully")


if __name__ == "__main__":
    main()
