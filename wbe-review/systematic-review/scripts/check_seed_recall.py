#!/usr/bin/env python3
"""Check whether the review's 44 seed references are recalled by the executed searches.

Reads templates/seed_studies.csv (the 44-reference seed set, with DOI/PMID metadata and
each seed's expected module) and cross-checks it against a real, deduplicated master
record set (normally data/processed/master_records.csv, produced by
deduplicate_records.py). A seed is considered "recalled" if a master record matches its
DOI or PMID exactly.

This script produces NO recall statistics of any kind when no real master record file is
supplied or when that file contains no records — it will not report a plausible-looking
recall rate for data it has not actually seen.

Usage:
    python3 check_seed_recall.py --help
    python3 check_seed_recall.py \
        --seed-csv templates/seed_studies.csv \
        --master-csv data/processed/master_records.csv \
        --output-dir reports
"""

import argparse
import csv
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = log_dir / f"check_seed_recall_{timestamp}.log"
    logger = logging.getLogger("check_seed_recall")
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
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(
        description="Check recall of the review's 44 seed references against a real "
                    "deduplicated master record set. Produces no output if no real "
                    "master record data is supplied.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--seed-csv", type=Path, default=Path("templates/seed_studies.csv"),
                        help="Path to the seed reference list")
    parser.add_argument("--master-csv", type=Path, default=Path("data/processed/master_records.csv"),
                        help="Path to the deduplicated master record set produced by "
                             "deduplicate_records.py")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"),
                        help="Directory to write seed_recall_report.csv and "
                             "seed_recall_summary.md")
    parser.add_argument("--log-dir", type=Path, default=Path("logs"),
                        help="Directory to write the run log")
    args = parser.parse_args()

    logger = setup_logger(args.log_dir)
    logger.info("check_seed_recall.py starting")

    if not args.seed_csv.exists():
        logger.error("Seed CSV %s not found.", args.seed_csv)
        sys.exit(1)
    seeds = load_csv(args.seed_csv)
    logger.info("Loaded %d seed references from %s", len(seeds), args.seed_csv)

    if not args.master_csv.exists():
        logger.warning(
            "Master record file %s does not exist. No real search has been executed and "
            "deduplicated yet. This script will NOT produce a recall report or recall "
            "rate against nonexistent data. Run deduplicate_records.py against real "
            "database exports first.", args.master_csv,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        status_path = args.output_dir / "seed_recall_summary.md"
        with open(status_path, "w", encoding="utf-8") as f:
            f.write("# Seed Recall Summary\n\n"
                    "STATUS: NOT EXECUTED — no master record file found at "
                    f"`{args.master_csv}`. Run the eight searches, then "
                    "`deduplicate_records.py`, then re-run this script.\n")
        logger.info("Wrote NOT EXECUTED status to %s", status_path)
        sys.exit(0)

    master = load_csv(args.master_csv)
    if not master:
        logger.warning(
            "Master record file %s exists but contains zero records. Treating this the "
            "same as 'no real search executed yet' — no recall report will claim a "
            "result against an empty dataset.", args.master_csv,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        status_path = args.output_dir / "seed_recall_summary.md"
        with open(status_path, "w", encoding="utf-8") as f:
            f.write("# Seed Recall Summary\n\n"
                    f"STATUS: NOT EXECUTED — `{args.master_csv}` contains zero records.\n")
        sys.exit(0)

    logger.info("Loaded %d master records from %s", len(master), args.master_csv)

    doi_index = {}
    pmid_index = {}
    for m in master:
        doi = (m.get("DOI") or "").strip().lower()
        pmid = (m.get("PMID") or "").strip()
        if doi:
            doi_index.setdefault(doi, []).append(m)
        if pmid:
            pmid_index.setdefault(pmid, []).append(m)

    results = []
    n_recalled = 0
    for seed in seeds:
        seed_doi = (seed.get("DOI") or "").strip().lower()
        seed_pmid = (seed.get("PMID") or "").strip()

        matches = []
        basis = ""
        if seed_doi and seed_doi in doi_index:
            matches = doi_index[seed_doi]
            basis = "DOI"
        elif seed_pmid and seed_pmid in pmid_index:
            matches = pmid_index[seed_pmid]
            basis = "PMID"

        if matches:
            n_recalled += 1
            databases = sorted({m.get("database_source", "") for m in matches})
            modules = sorted({m.get("search_module", "") for m in matches})
            seed["retrieved_by_core"] = "TRUE" if "core" in modules else "FALSE"
            seed["retrieved_by_module"] = ";".join(m for m in modules if m != "core")
            seed["retrieved_database"] = ";".join(databases)
            seed["recall_status"] = f"RECALLED ({basis})"
            seed["failure_reason"] = ""
        else:
            if not seed_doi and not seed_pmid:
                seed["recall_status"] = "UNTESTABLE"
                seed["failure_reason"] = "Seed record has neither DOI nor PMID in seed_studies.csv"
            else:
                seed["recall_status"] = "NOT_RECALLED"
                seed["failure_reason"] = (
                    "No master record matched this seed's DOI/PMID. Revise the "
                    f"'{seed.get('expected_module', 'unknown')}' search string and re-run."
                )

        results.append(seed)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "seed_recall_report.csv"
    fieldnames = list(seeds[0].keys())
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    n_total = len(seeds)
    n_untestable = sum(1 for r in results if r["recall_status"] == "UNTESTABLE")
    n_not_recalled = sum(1 for r in results if r["recall_status"] == "NOT_RECALLED")
    testable = n_total - n_untestable

    summary_path = args.output_dir / "seed_recall_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Seed Recall Summary\n\n")
        f.write(f"Run date: {datetime.now().isoformat()}\n\n")
        f.write(f"- Total seed references: {n_total}\n")
        f.write(f"- Untestable (no DOI/PMID recorded for the seed itself): {n_untestable}\n")
        f.write(f"- Testable: {testable}\n")
        f.write(f"- Recalled: {n_recalled}\n")
        f.write(f"- Not recalled: {n_not_recalled}\n")
        if testable > 0:
            rate = 100.0 * n_recalled / testable
            f.write(f"- Recall rate (of testable seeds): {rate:.1f}%\n\n")
        else:
            f.write("- Recall rate: undefined (no testable seeds)\n\n")
        if n_not_recalled > 0:
            f.write("## Seeds not recalled — revise the corresponding module search string\n\n")
            for r in results:
                if r["recall_status"] == "NOT_RECALLED":
                    f.write(f"- {r.get('ref_number', '')} (expected module: "
                            f"{r.get('expected_module', '')}): {r.get('citation', '')[:100]}\n")

    logger.info("Wrote %s and %s", report_path, summary_path)
    logger.info("Recalled %d / %d testable seeds", n_recalled, testable)
    if n_not_recalled > 0:
        logger.warning("%d seed reference(s) were NOT recalled — see %s for the list. "
                       "Per Section 13 of the search strategy, revise and re-test the "
                       "affected module string(s) before treating the search as final.",
                       n_not_recalled, summary_path)
    logger.info("check_seed_recall.py finished")


if __name__ == "__main__":
    main()
