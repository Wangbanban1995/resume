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

Pilot mode (--mode pilot): checks readiness of only a named subset of (database,
search_id) combinations (e.g. a first real-import trial covering 3 of the full 24
searches), without treating the other, not-yet-provided combinations as blocking. Prints
two status lines at the end:
    PILOT_READY | PILOT_NOT_READY          -- readiness of only the named --expected-search set
    PRODUCTION_READY | PRODUCTION_NOT_READY -- readiness of the full 8x3=24-search plan
                                                (reusing the same completeness check as
                                                production mode, but purely informational
                                                here -- it never blocks the pilot run)

In pilot mode, for every pilot export file found on disk this also writes
logs/pilot_raw_file_checksums.csv (source_file, file_size_bytes, sha256, database,
search_id, imported_at) -- a read-only provenance record. The original export files
themselves are never opened for writing, moved, or modified by this script.

Usage:
    python3 validate_search_inputs.py --help
    python3 validate_search_inputs.py \
        --search-log templates/search_log.csv \
        --raw-dir data/raw \
        --output-dir reports
    python3 validate_search_inputs.py \
        --mode pilot \
        --expected-search pubmed_core \
        --expected-search wos_module02 \
        --expected-search scopus_module05
"""

import argparse
import csv
import hashlib
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
EXPECTED_SEARCH_COMBO_RE = re.compile(
    r"^(?P<database>wos|scopus|pubmed)_(?P<search_id>core|module0[2-8])$",
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


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
    parser.add_argument("--mode", choices=["production", "pilot"], default="production",
                         help="'production' checks the full 8x3=24-search plan and is "
                              "unchanged/default behavior. 'pilot' checks readiness of only "
                              "the (database, search_id) combinations named via "
                              "--expected-search, without blocking on the rest.")
    parser.add_argument("--expected-search", action="append", default=None,
                         metavar="DATABASE_SEARCHID",
                         help="Pilot mode only. A <database>_<search_id> combination to "
                              "check, e.g. pubmed_core, wos_module02, scopus_module05. "
                              "Repeatable.")
    args = parser.parse_args()

    logger = setup_logger(args.log_dir)
    logger.info("validate_search_inputs.py starting (mode=%s)", args.mode)

    pilot_combinations = set()
    if args.mode == "pilot":
        if not args.expected_search:
            logger.error("--mode pilot requires at least one --expected-search "
                          "DATABASE_SEARCHID argument.")
            print("PILOT_NOT_READY")
            print("PRODUCTION_NOT_READY")
            sys.exit(2)
        for combo in args.expected_search:
            m = EXPECTED_SEARCH_COMBO_RE.match(combo.strip().lower())
            if not m:
                logger.error("--expected-search value '%s' is not a valid "
                              "<database>_<search_id> combination (e.g. pubmed_core, "
                              "wos_module02, scopus_module05).", combo)
                print("PILOT_NOT_READY")
                print("PRODUCTION_NOT_READY")
                sys.exit(2)
            pilot_combinations.add((m.group("database").lower(), m.group("search_id").lower()))

    log_rows = load_csv(args.search_log)
    populated_rows = [r for r in log_rows if (r.get("database") or "").strip()
                      and (r.get("search_id") or "").strip()]

    issues = []       # (severity, message) -- severity in {"blocking", "warning", "info"}
    row_reports = []
    pilot_checksum_rows = []  # pilot mode only: source_file, file_size_bytes, sha256, database, search_id, imported_at

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
            if args.mode == "production":
                # Always blocking, not just when the log is entirely empty: an incomplete
                # 8x3 search plan means downstream deduplication/PRISMA counts would be
                # built on a known-partial input set, which is not a "ready with warnings"
                # state — it is not ready.
                issues.append(("blocking",
                              f"No search log row for (database={db}, search_id={sid}) — "
                              "the full 8x3=24-search plan is not yet complete."))
            else:
                # Pilot mode: the other (up to) 21 not-yet-provided searches are expected
                # and must not block this partial trial run. Recorded as "info" only, and
                # only feeds the informational PRODUCTION_READY/PRODUCTION_NOT_READY line.
                issues.append(("info",
                              f"(database={db}, search_id={sid}) not in search log — "
                              "not part of this pilot run, not blocking."))

    production_ready = not missing_combinations

    pilot_missing = []
    if args.mode == "pilot":
        for db, sid in sorted(pilot_combinations):
            if (db, sid) not in seen_combinations:
                pilot_missing.append((db, sid))
                issues.append(("blocking",
                              f"Pilot combination (database={db}, search_id={sid}) has no "
                              f"corresponding row in {args.search_log}."))

    # Build the set of files actually present under data/raw/
    raw_files = [p for p in sorted(args.raw_dir.rglob("*"))
                if p.is_file() and p.suffix.lower() in {".ris", ".csv", ".nbib", ".bib"}
                and p.name != ".gitkeep"]
    raw_by_name = {p.name: p for p in raw_files}
    referenced_filenames = set()

    for row in populated_rows:
        db = (row.get("database") or "").strip().lower()
        sid = (row.get("search_id") or "").strip().lower()

        if args.mode == "pilot" and (db, sid) not in pilot_combinations:
            # This round only processes the named pilot combinations; rows for other
            # searches (even if present in the log) are out of scope for this run and
            # must not be checked or reported on here.
            continue

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
                if args.mode == "pilot":
                    # Read-only provenance record; the original file is never opened for
                    # writing, moved, or modified.
                    try:
                        pilot_checksum_rows.append({
                            "source_file": str(export_path),
                            "file_size_bytes": export_path.stat().st_size,
                            "sha256": sha256_of_file(export_path),
                            "database": db,
                            "search_id": sid,
                            "imported_at": datetime.now().isoformat(),
                        })
                    except OSError as exc:
                        issues.append(("warning", f"{export_filename}: could not be "
                                      f"checksummed: {exc}"))

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
        inferred_db = infer_database_from_path(p)
        inferred_mod = infer_module_from_filename(p)
        if args.mode == "pilot" and inferred_db is not None and inferred_mod is not None \
                and (inferred_db, inferred_mod) not in pilot_combinations:
            # Out-of-scope for this pilot run (belongs to one of the other ~21 not-yet-
            # provided searches) -- not an issue worth reporting here.
            continue
        issues.append(("warning", f"{p} is present under {args.raw_dir} but is not "
                      "referenced by any row in the search log."))
        if inferred_db is None or inferred_mod is None:
            issues.append(("warning", f"{p}: filename/location does not clearly map to "
                          "a recognized (database, module) combination."))

    n_blocking = sum(1 for sev, _ in issues if sev == "blocking")
    n_warning = sum(1 for sev, _ in issues if sev == "warning")

    if args.mode == "pilot":
        pilot_status = "PILOT_NOT_READY" if (n_blocking > 0 or not raw_files) else "PILOT_READY"
        production_status_label = "PRODUCTION_READY" if production_ready else "PRODUCTION_NOT_READY"
        status = pilot_status
    elif n_blocking > 0 or not populated_rows or not raw_files:
        status = "NOT_READY"
    elif n_warning > 0:
        status = "READY_WITH_WARNINGS"
    else:
        status = "READY"

    args.output_dir.mkdir(parents=True, exist_ok=True)

    report_stem = "pilot_input_readiness_report" if args.mode == "pilot" else "input_readiness_report"

    with open(args.output_dir / f"{report_stem}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["severity", "message"])
        for sev, msg in issues:
            writer.writerow([sev, msg])

    with open(args.output_dir / f"{report_stem}.md", "w", encoding="utf-8") as f:
        if args.mode == "pilot":
            f.write("# Pilot Input Readiness Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(f"## STATUS: {pilot_status}\n")
            f.write(f"## PRODUCTION STATUS (informational only, not blocking this pilot): "
                    f"{production_status_label}\n\n")
            f.write(f"- Pilot combinations checked: "
                    f"{', '.join(f'{d}_{s}' for d, s in sorted(pilot_combinations))}\n")
            f.write(f"- Pilot combinations missing from {args.search_log}: {len(pilot_missing)}\n")
            f.write(f"- Search log rows populated (all): {len(populated_rows)} of expected 24 "
                    f"(8 searches x 3 databases)\n")
            f.write(f"- Missing (database, search_id) combinations (full 24-search plan): "
                    f"{len(missing_combinations)}\n")
            f.write(f"- Raw export files found under {args.raw_dir}: {len(raw_files)}\n")
            f.write(f"- Blocking issues (pilot scope): {n_blocking}\n")
            f.write(f"- Warnings: {n_warning}\n\n")
            if pilot_status == "PILOT_NOT_READY":
                f.write("**One or more of the 3 named pilot files/search-log rows is "
                        "missing, unreadable, or inconsistent. Do not proceed past Section 1 "
                        "of the pilot workflow until this is resolved — see Issues below.**\n\n")
            f.write("**This is a partial, 3-of-24-search pilot run. It never establishes "
                    "PRODUCTION_READY status and must not be used to justify skipping the "
                    "remaining 21 searches.**\n\n")
        else:
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

    if args.mode == "pilot":
        args.log_dir.mkdir(parents=True, exist_ok=True)
        checksum_path = args.log_dir / "pilot_raw_file_checksums.csv"
        with open(checksum_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "source_file", "file_size_bytes", "sha256", "database",
                "search_id", "imported_at",
            ])
            writer.writeheader()
            for row in pilot_checksum_rows:
                writer.writerow(row)
        logger.info("Wrote %d checksum row(s) to %s", len(pilot_checksum_rows), checksum_path)

    logger.info("Wrote %s.md/.csv to %s", report_stem, args.output_dir)
    if args.mode == "pilot":
        logger.info("PILOT STATUS: %s (%d blocking, %d warnings) | PRODUCTION STATUS: %s",
                    pilot_status, n_blocking, n_warning, production_status_label)
    else:
        logger.info("STATUS: %s (%d blocking, %d warnings)", status, n_blocking, n_warning)
    logger.info("validate_search_inputs.py finished")

    if args.mode == "pilot":
        print(pilot_status)
        print(production_status_label)

    if args.mode == "pilot" and pilot_status == "PILOT_NOT_READY":
        sys.exit(1)


if __name__ == "__main__":
    main()
