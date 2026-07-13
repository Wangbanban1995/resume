#!/usr/bin/env python3
"""Pre-flight readiness check for real WoS/Scopus/PubMed search inputs.

Checks, before any deduplication or PRISMA counting is attempted:
    - the search log covers all 8 searches (core + Modules 2-8) x 3 databases (24 rows)
    - filenames follow the <database>_<search_id>_<topic>_<YYYYMMDD>.<ext> convention
    - each (database, search_id) combination appears at most once in the log
    - a search log row's database/search_id are consistent with the directory and
      filename of the export file it references
    - raw_hits and exported_records are populated for every row
    - every referenced export file actually exists in data/raw/
    - the number of records the file actually parses to is reasonably close to the
      logged exported_records count
    - a raw_hits of 0 has an explanatory note, not a silent zero
    - no duplicate export files, and no unrecognized files sitting in data/raw/ that no
      search log row references

Outputs reports/input_readiness_report.md and reports/input_readiness_report.csv with an
overall status of READY, READY_WITH_WARNINGS, or NOT_READY. If the search log has no
real rows or no export files exist, this script reports NOT_READY and computes no
search/PRISMA numbers of any kind.

Usage:
    python3 validate_search_inputs.py --help
    python3 validate_search_inputs.py \
        --search-log templates/search_log.csv \
        --raw-dir data/raw \
        --output-dir reports
"""

import argparse
import csv
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deduplicate_records import (  # noqa: E402
    parse_ris, parse_nbib, parse_bibtex, parse_csv_export,
    infer_database_from_path, infer_module_from_filename, read_text_safely,
)

EXPECTED_SEARCH_IDS = ["core"] + [f"module0{i}" for i in range(2, 9)]
EXPECTED_DATABASES = ["wos", "scopus", "pubmed"]
FILENAME_RE = re.compile(
    r"^(?P<database>wos|scopus|pubmed)_(?P<search_id>core|module0[2-8])_[a-z0-9_]+_(?P<date>\d{8})\.(?P<ext>ris|csv|nbib|bib)$",
    re.IGNORECASE,
)


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = log_dir / f"validate_search_inputs_{timestamp}.log"
    logger = logging.getLogger("validate_search_inputs")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    fh = logging.FileHandler(log_path, encoding="utf-8")
    ch = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info("Log file: %s", log_path)
    return logger


def load_csv(path: Path) -> list:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_export_file(path: Path, database: str, module: str, logger: logging.Logger) -> int:
    text = read_text_safely(path, logger)
    warnings = []
    try:
        if path.suffix.lower() == ".ris":
            return len(parse_ris(text, str(path), database, module, logger, warnings))
        if path.suffix.lower() == ".nbib":
            return len(parse_nbib(text, str(path), database, module, logger, warnings))
        if path.suffix.lower() == ".bib":
            return len(parse_bibtex(text, str(path), database, module, warnings))
        if path.suffix.lower() == ".csv":
            return len(parse_csv_export(path, text, str(path), database, module, logger, warnings))
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to parse %s for readiness count: %s", path, exc)
    return -1  # signals "could not determine"


def main():
    parser = argparse.ArgumentParser(
        description="Pre-flight readiness check for real WoS/Scopus/PubMed search "
                    "inputs before deduplication/PRISMA counting is attempted.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--search-log", type=Path, default=Path("templates/search_log.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--log-dir", type=Path, default=Path("logs"))
    args = parser.parse_args()

    logger = setup_logger(args.log_dir)
    logger.info("validate_search_inputs.py starting")

    log_rows = load_csv(args.search_log)
    populated_rows = [r for r in log_rows if (r.get("database") or "").strip()
                      and (r.get("search_id") or "").strip()]

    issues = []       # (severity, message) -- severity in {"blocking", "warning"}
    row_reports = []

    if not populated_rows:
        issues.append(("blocking", f"{args.search_log} has no populated rows (database + "
                                    "search_id). No real search has been logged yet."))

    # 1. Completeness: all 8 search_ids x 3 databases expected.
    seen_combinations = {}
    for row in populated_rows:
        db = (row.get("database") or "").strip().lower()
        sid = (row.get("search_id") or "").strip().lower()
        key = (db, sid)
        seen_combinations.setdefault(key, []).append(row)

    for db, sid in seen_combinations:
        if seen_combinations[(db, sid)] and len(seen_combinations[(db, sid)]) > 1:
            issues.append(("warning", f"(database={db}, search_id={sid}) appears "
                                       f"{len(seen_combinations[(db, sid)])} times in "
                                       "the search log — each combination should "
                                       "normally appear once; if re-run intentionally, "
                                       "confirm this is expected."))

    missing_combinations = []
    for db in EXPECTED_DATABASES:
        for sid in EXPECTED_SEARCH_IDS:
            if (db, sid) not in seen_combinations:
                missing_combinations.append((db, sid))
    if missing_combinations:
        for db, sid in missing_combinations:
            # Always blocking, not just when the log is entirely empty: an incomplete
            # 8x3 search plan means downstream deduplication/PRISMA counts would be
            # built on a known-partial input set, which is not a "ready with warnings"
            # state — it is not ready.
            issues.append(("blocking",
                          f"No search log row for (database={db}, search_id={sid}) — "
                          "the full 8x3=24-search plan is not yet complete."))

    # Build the set of files actually present under data/raw/
    raw_files = [p for p in sorted(args.raw_dir.rglob("*"))
                if p.is_file() and p.suffix.lower() in {".ris", ".csv", ".nbib", ".bib"}
                and p.name != ".gitkeep"]
    raw_by_name = {p.name: p for p in raw_files}
    referenced_filenames = set()

    for row in populated_rows:
        db = (row.get("database") or "").strip().lower()
        sid = (row.get("search_id") or "").strip().lower()
        export_filename = (row.get("export_filename") or "").strip()
        raw_hits = (row.get("raw_hits") or "").strip()
        exported_records = (row.get("exported_records") or "").strip()
        notes = (row.get("notes") or "").strip()

        row_report = {"database": db, "search_id": sid, "export_filename": export_filename,
                      "checks": []}

        # 2. Filename convention
        if export_filename:
            m = FILENAME_RE.match(export_filename)
            if not m:
                issues.append(("warning", f"{export_filename}: does not match the "
                              "<database>_<search_id>_<topic>_<YYYYMMDD>.<ext> naming "
                              "convention."))
                row_report["checks"].append("filename_convention: FAIL")
            else:
                if m.group("database").lower() != db:
                    issues.append(("warning", f"{export_filename}: filename database "
                                  f"'{m.group('database')}' does not match the search "
                                  f"log's database column '{db}'."))
                if m.group("search_id").lower() != sid:
                    issues.append(("warning", f"{export_filename}: filename search_id "
                                  f"'{m.group('search_id')}' does not match the search "
                                  f"log's search_id column '{sid}'."))
                row_report["checks"].append("filename_convention: OK")
        else:
            issues.append(("blocking", f"({db}, {sid}): export_filename is blank in the "
                          "search log."))
            row_report["checks"].append("filename_convention: MISSING")

        # 5. raw_hits / exported_records populated
        if not raw_hits:
            issues.append(("blocking", f"({db}, {sid}): raw_hits is blank."))
            row_report["checks"].append("raw_hits: MISSING")
        elif raw_hits == "0" and not notes:
            issues.append(("warning", f"({db}, {sid}): raw_hits is 0 with no explanatory "
                          "note in the 'notes' column — confirm this is a genuine "
                          "zero-hit search, not an unlogged failure."))
            row_report["checks"].append("raw_hits: ZERO_UNEXPLAINED")
        else:
            row_report["checks"].append(f"raw_hits: {raw_hits}")

        if not exported_records:
            issues.append(("blocking", f"({db}, {sid}): exported_records is blank."))
            row_report["checks"].append("exported_records: MISSING")

        # 6. Export file exists
        export_path = None
        if export_filename:
            referenced_filenames.add(export_filename)
            export_path = raw_by_name.get(export_filename)
            if export_path is None:
                # also check nested under data/raw/<database>/
                candidate = args.raw_dir / db / export_filename
                if candidate.exists():
                    export_path = candidate
            if export_path is None:
                issues.append(("blocking", f"({db}, {sid}): referenced export file "
                              f"'{export_filename}' was not found under {args.raw_dir}."))
                row_report["checks"].append("file_exists: MISSING")
            else:
                row_report["checks"].append("file_exists: OK")

        # 4. Directory/database/module consistency
        if export_path is not None:
            inferred_db = infer_database_from_path(export_path)
            inferred_mod = infer_module_from_filename(export_path)
            if inferred_db != db:
                issues.append(("warning", f"{export_filename}: located under a directory "
                              f"inferred as database='{inferred_db}', but the search log "
                              f"says database='{db}'."))
            if inferred_mod != sid:
                issues.append(("warning", f"{export_filename}: filename implies search "
                              f"module '{inferred_mod}', but the search log says "
                              f"search_id='{sid}'."))

            # 7. Parsed-count vs. exported_records consistency
            actual_count = parse_export_file(export_path, db, sid, logger)
            if actual_count < 0:
                issues.append(("warning", f"{export_filename}: could not be parsed to "
                              "verify its record count."))
                row_report["checks"].append("parsed_count: PARSE_FAILED")
            elif exported_records.isdigit():
                expected = int(exported_records)
                if actual_count != expected:
                    issues.append(("warning", f"{export_filename}: search log says "
                                  f"exported_records={expected}, but the file actually "
                                  f"parses to {actual_count} record(s)."))
                    row_report["checks"].append(f"parsed_count: MISMATCH (logged={expected}, actual={actual_count})")
                else:
                    row_report["checks"].append(f"parsed_count: OK ({actual_count})")

        row_reports.append(row_report)

    # 9. Duplicate export files / unreferenced files present in data/raw
    seen_names = {}
    for p in raw_files:
        seen_names.setdefault(p.name, []).append(p)
    for name, paths in seen_names.items():
        if len(paths) > 1:
            issues.append(("warning", f"Duplicate filename '{name}' found in multiple "
                          f"locations under {args.raw_dir}: {[str(p) for p in paths]}"))

    # 10. Unrecognized files (present on disk but not referenced by any search log row)
    unreferenced = [p for p in raw_files if p.name not in referenced_filenames]
    for p in unreferenced:
        issues.append(("warning", f"{p} is present under {args.raw_dir} but is not "
                      "referenced by any row in the search log."))
        inferred_db = infer_database_from_path(p)
        inferred_mod = infer_module_from_filename(p)
        if inferred_db is None or inferred_mod is None:
            issues.append(("warning", f"{p}: filename/location does not clearly map to "
                          "a recognized (database, module) combination."))

    n_blocking = sum(1 for sev, _ in issues if sev == "blocking")
    n_warning = sum(1 for sev, _ in issues if sev == "warning")

    if n_blocking > 0 or not populated_rows or not raw_files:
        status = "NOT_READY"
    elif n_warning > 0:
        status = "READY_WITH_WARNINGS"
    else:
        status = "READY"

    args.output_dir.mkdir(parents=True, exist_ok=True)

    with open(args.output_dir / "input_readiness_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["severity", "message"])
        for sev, msg in issues:
            writer.writerow([sev, msg])

    with open(args.output_dir / "input_readiness_report.md", "w", encoding="utf-8") as f:
        f.write("# Input Readiness Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"## STATUS: {status}\n\n")
        f.write(f"- Search log rows populated: {len(populated_rows)} of expected 24 "
                f"(8 searches x 3 databases)\n")
        f.write(f"- Missing (database, search_id) combinations: {len(missing_combinations)}\n")
        f.write(f"- Raw export files found under {args.raw_dir}: {len(raw_files)}\n")
        f.write(f"- Blocking issues: {n_blocking}\n")
        f.write(f"- Warnings: {n_warning}\n\n")
        if status == "NOT_READY":
            f.write("**Real search execution and/or export collection is incomplete. "
                    "Do not proceed to deduplicate_records.py / generate_prisma_counts.py "
                    "expecting real numbers until this is resolved.**\n\n")
        if issues:
            f.write("## Issues\n\n")
            for sev, msg in issues:
                f.write(f"- **[{sev.upper()}]** {msg}\n")

    logger.info("Wrote input_readiness_report.md/.csv to %s", args.output_dir)
    logger.info("STATUS: %s (%d blocking, %d warnings)", status, n_blocking, n_warning)
    logger.info("validate_search_inputs.py finished")


if __name__ == "__main__":
    main()
