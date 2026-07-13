#!/usr/bin/env python3
"""Deduplicate bibliographic records exported from Web of Science, Scopus, and PubMed.

Reads RIS (.ris), Scopus CSV (.csv), BibTeX (.bib), and PubMed NBIB (.nbib) files from
an input directory tree, normalizes them to a common schema, and deduplicates by DOI,
then PMID, then normalized title, then title+year+first-author. Fuzzy title matches are
flagged as possible_duplicate and are never auto-removed.

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
from datetime import datetime
from pathlib import Path

SUPPORTED_EXTENSIONS = {".ris", ".csv", ".bib", ".nbib"}

UNIFIED_FIELDS = [
    "record_id", "title", "abstract", "authors", "year", "journal",
    "DOI", "PMID", "database_source", "search_module", "source_file",
]

REQUIRED_FOR_DEDUP = ["title"]  # a record with no title at all cannot be deduplicated meaningfully


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = log_dir / f"deduplicate_records_{timestamp}.log"
    logger = logging.getLogger("deduplicate_records")
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


def infer_database_from_path(path: Path) -> str:
    parts = {p.lower() for p in path.parts}
    if "wos" in parts:
        return "wos"
    if "scopus" in parts:
        return "scopus"
    if "pubmed" in parts:
        return "pubmed"
    return "unknown"


def infer_module_from_filename(path: Path) -> str:
    m = re.search(r"(core|module\d{2})", path.stem, re.IGNORECASE)
    return m.group(1).lower() if m else "unknown"


def parse_ris(text: str, source_file: str, database: str, module: str) -> list:
    """Minimal RIS parser: TAG  - value, records separated by ER  -."""
    records = []
    current = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Z0-9]{2})\s*-\s*(.*)$", line.strip())
        if not m:
            continue
        tag, value = m.group(1), m.group(2).strip()
        if tag == "TY":
            current = {}
        elif tag == "ER":
            if current:
                records.append(_ris_record_to_unified(current, source_file, database, module))
            current = {}
        elif tag == "TI" or tag == "T1":
            current["title"] = value
        elif tag == "AB" or tag == "N2":
            current["abstract"] = value
        elif tag == "AU" or tag == "A1":
            current.setdefault("authors", []).append(value)
        elif tag == "PY" or tag == "Y1":
            year_match = re.search(r"\d{4}", value)
            if year_match:
                current["year"] = year_match.group(0)
        elif tag == "JO" or tag == "T2" or tag == "JF":
            current["journal"] = value
        elif tag == "DO":
            current["DOI"] = value.strip()
        elif tag == "AN" and re.match(r"^\d+$", value):
            current.setdefault("PMID", value)
    if current:
        records.append(_ris_record_to_unified(current, source_file, database, module))
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


def parse_nbib(text: str, source_file: str, database: str, module: str) -> list:
    """Minimal PubMed NBIB parser: tag- value pairs, blank line separates records."""
    records = []
    current = {}
    for line in text.splitlines():
        if not line.strip():
            if current:
                records.append(_nbib_record_to_unified(current, source_file, database, module))
                current = {}
            continue
        m = re.match(r"^([A-Z]{2,4})\s*-\s*(.*)$", line)
        if not m:
            # continuation line of the previous tag
            if current.get("_last_tag") and line.startswith("      "):
                key = current["_last_tag"]
                if key in ("TI", "AB"):
                    current[key] = current.get(key, "") + " " + line.strip()
            continue
        tag, value = m.group(1), m.group(2).strip()
        current["_last_tag"] = tag
        if tag == "TI":
            current["TI"] = value
        elif tag == "AB":
            current["AB"] = value
        elif tag == "FAU":
            current.setdefault("FAU", []).append(value)
        elif tag == "DP":
            year_match = re.search(r"\d{4}", value)
            if year_match:
                current["DP"] = year_match.group(0)
        elif tag == "JT":
            current["JT"] = value
        elif tag == "LID" and "[doi]" in value:
            current["DOI"] = value.replace("[doi]", "").strip()
        elif tag == "AID" and "[doi]" in value:
            current["DOI"] = value.replace("[doi]", "").strip()
        elif tag == "PMID":
            current["PMID"] = value.strip()
    if current:
        records.append(_nbib_record_to_unified(current, source_file, database, module))
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


def parse_bibtex(text: str, source_file: str, database: str, module: str) -> list:
    """Minimal BibTeX parser: handles @type{key, field = {value}, ...} entries."""
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


def normalize_title(title: str) -> str:
    t = title.lower().strip()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


def first_author_surname(authors: str) -> str:
    if not authors:
        return ""
    first = authors.split(";")[0].strip()
    # handle "Surname, Given" or "Given Surname"
    if "," in first:
        return first.split(",")[0].strip().lower()
    parts = first.split()
    return parts[-1].strip().lower() if parts else ""


def load_all_records(input_dir: Path, logger: logging.Logger) -> list:
    records = []
    files_found = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if path.name == ".gitkeep":
            continue
        files_found.append(path)

    if not files_found:
        return records

    for path in files_found:
        database = infer_database_from_path(path)
        module = infer_module_from_filename(path)
        text = read_text_safely(path, logger)
        source_file = str(path)
        try:
            if path.suffix.lower() == ".ris":
                recs = parse_ris(text, source_file, database, module)
            elif path.suffix.lower() == ".nbib":
                recs = parse_nbib(text, source_file, database, module)
            elif path.suffix.lower() == ".bib":
                recs = parse_bibtex(text, source_file, database, module)
            elif path.suffix.lower() == ".csv":
                recs = parse_csv_export(path, text, source_file, database, module, logger)
            else:
                continue
        except Exception as exc:  # noqa: BLE001 - we want to log and continue, not crash the whole run
            logger.error("Failed to parse %s: %s", path, exc)
            continue

        missing_required = [r for r in recs if not all(r.get(f) for f in REQUIRED_FOR_DEDUP)]
        if missing_required:
            logger.warning("%d record(s) in %s are missing a title and cannot be reliably "
                            "deduplicated; they are still included in master_records.csv "
                            "but excluded from DOI/PMID/title matching.", len(missing_required), path)

        logger.info("Parsed %d record(s) from %s (database=%s, module=%s)",
                    len(recs), path, database, module)
        records.extend(recs)

    return records


def deduplicate(records: list, logger: logging.Logger):
    for i, r in enumerate(records, start=1):
        raw_id = f"{r['database_source']}|{r['search_module']}|{r['source_file']}|{i}"
        r["record_id"] = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:12]
        r["_norm_title"] = normalize_title(r.get("title", ""))
        r["_first_author"] = first_author_surname(r.get("authors", ""))

    doi_index, pmid_index, title_index, tya_index = {}, {}, {}, {}
    master = []
    confirmed_duplicates = []
    possible_duplicates = []

    for r in records:
        match_id = None
        match_basis = None

        doi = (r.get("DOI") or "").strip().lower()
        pmid = (r.get("PMID") or "").strip()
        norm_title = r.get("_norm_title", "")
        tya_key = (norm_title, r.get("year", ""), r.get("_first_author", ""))

        if doi and doi in doi_index:
            match_id, match_basis = doi_index[doi], "DOI"
        elif pmid and pmid in pmid_index:
            match_id, match_basis = pmid_index[pmid], "PMID"
        elif norm_title and norm_title in title_index:
            match_id, match_basis = title_index[norm_title], "normalized_title"
        elif norm_title and tya_key in tya_index:
            match_id, match_basis = tya_index[tya_key], "title_year_first_author"

        if match_id is not None:
            r["duplicate_of_record_id"] = match_id
            r["duplicate_match_basis"] = match_basis
            confirmed_duplicates.append(r)
            continue

        # not a confirmed duplicate by exact-match rules; check fuzzy title similarity
        # against existing master records as a possible_duplicate flag only.
        fuzzy_hit = None
        if norm_title:
            title_tokens = set(norm_title.split())
            if len(title_tokens) >= 4:
                for m in master:
                    m_tokens = set(m.get("_norm_title", "").split())
                    if not m_tokens:
                        continue
                    overlap = len(title_tokens & m_tokens) / max(len(title_tokens | m_tokens), 1)
                    if overlap >= 0.8 and r.get("year") == m.get("year"):
                        fuzzy_hit = m["record_id"]
                        break

        if fuzzy_hit:
            r["possible_duplicate_of_record_id"] = fuzzy_hit
            r["duplicate_match_basis"] = "fuzzy_title_overlap_ge_0.8_same_year"
            possible_duplicates.append(r)
            # possible duplicates are NOT auto-removed: they still go into master
            master.append(r)
        else:
            master.append(r)

        if doi:
            doi_index.setdefault(doi, r["record_id"])
        if pmid:
            pmid_index.setdefault(pmid, r["record_id"])
        if norm_title:
            title_index.setdefault(norm_title, r["record_id"])
            tya_index.setdefault(tya_key, r["record_id"])

    logger.info("Deduplication complete: %d input records -> %d master, %d confirmed duplicates, "
                "%d flagged possible duplicates (retained in master, not removed)",
                len(records), len(master), len(confirmed_duplicates), len(possible_duplicates))

    return master, confirmed_duplicates, possible_duplicates


def write_csv(path: Path, rows: list, fieldnames: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_database_module_summary(path: Path, master: list, confirmed_duplicates: list):
    summary = {}
    for r in master + confirmed_duplicates:
        key = (r["database_source"], r["search_module"])
        summary.setdefault(key, {"database": key[0], "search_module": key[1],
                                   "records_in_master": 0, "records_as_duplicates": 0})
    for r in master:
        key = (r["database_source"], r["search_module"])
        summary[key]["records_in_master"] += 1
    for r in confirmed_duplicates:
        key = (r["database_source"], r["search_module"])
        summary[key]["records_as_duplicates"] += 1

    rows = sorted(summary.values(), key=lambda x: (x["database"], x["search_module"]))
    write_csv(path, rows, ["database", "search_module", "records_in_master", "records_as_duplicates"])


def main():
    parser = argparse.ArgumentParser(
        description="Deduplicate WoS/Scopus/PubMed bibliographic exports (RIS/CSV/BibTeX/NBIB).",
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

    records = load_all_records(args.input_dir, logger)

    if not records:
        logger.warning(
            "No real export files (.ris/.csv/.bib/.nbib) were found under %s. "
            "This script will not fabricate deduplication results. Populate "
            "data/raw/{wos,scopus,pubmed}/ with real database exports and re-run. "
            "Exiting safely with no output written.",
            args.input_dir,
        )
        sys.exit(0)

    master, confirmed_duplicates, possible_duplicates = deduplicate(records, logger)

    fieldnames = UNIFIED_FIELDS + ["duplicate_of_record_id", "duplicate_match_basis",
                                    "possible_duplicate_of_record_id"]

    write_csv(args.output_dir / "master_records.csv", master, fieldnames)
    write_csv(args.output_dir / "confirmed_duplicates.csv", confirmed_duplicates, fieldnames)
    write_csv(args.output_dir / "possible_duplicates.csv", possible_duplicates, fieldnames)
    write_database_module_summary(args.output_dir / "database_module_summary.csv",
                                   master, confirmed_duplicates)

    log_summary_path = args.output_dir / "deduplication_log.txt"
    with open(log_summary_path, "w", encoding="utf-8") as f:
        f.write(f"Deduplication run: {datetime.now().isoformat()}\n")
        f.write(f"Input directory: {args.input_dir}\n")
        f.write(f"Total input records parsed: {len(records)}\n")
        f.write(f"Master (unique) records: {len(master)}\n")
        f.write(f"Confirmed duplicates removed from master: {len(confirmed_duplicates)}\n")
        f.write(f"Possible duplicates flagged (retained in master, NOT auto-removed): "
                f"{len(possible_duplicates)}\n")

    logger.info("Wrote outputs to %s", args.output_dir)
    logger.info("master_records.csv: %d rows", len(master))
    logger.info("confirmed_duplicates.csv: %d rows", len(confirmed_duplicates))
    logger.info("possible_duplicates.csv: %d rows (flagged only, retained in master)",
                len(possible_duplicates))
    logger.info("deduplicate_records.py finished successfully")


if __name__ == "__main__":
    main()
