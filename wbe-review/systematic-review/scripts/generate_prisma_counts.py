#!/usr/bin/env python3
"""Generate PRISMA flow-diagram counts from real search logs, deduplication output, and
screening decisions.

This script computes:
    records_identified, duplicates_removed, records_screened,
    records_excluded_title_abstract, reports_sought, reports_not_retrieved,
    reports_assessed, reports_excluded_by_reason, studies_included

directly from --search-log, --dedup-dir, --title-abstract-screening, and
--full-text-screening. If any required input is missing, empty, or contains no real
records, this script writes STATUS: NOT EXECUTED and computes no numbers — it does not
estimate, interpolate, or use placeholder counts under any circumstance.

Usage:
    python3 generate_prisma_counts.py --help
    python3 generate_prisma_counts.py \
        --search-log templates/search_log.csv \
        --dedup-dir data/processed \
        --title-abstract-screening data/processed/title_abstract_screening_YYYYMMDD.csv \
        --full-text-screening data/processed/full_text_screening_YYYYMMDD.csv \
        --output-dir reports
"""

import argparse
import csv
import json
import logging
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

NOT_EXECUTED_MESSAGE = "STATUS: NOT EXECUTED — awaiting database exports and screening decisions."


def setup_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    log_path = log_dir / f"generate_prisma_counts_{timestamp}.log"
    logger = logging.getLogger("generate_prisma_counts")
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


def write_not_executed(output_dir: Path, logger: logging.Logger, reasons: list):
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "NOT_EXECUTED",
        "message": NOT_EXECUTED_MESSAGE,
        "reasons": reasons,
        "generated_at": datetime.now().isoformat(),
    }
    with open(output_dir / "prisma_counts.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    with open(output_dir / "prisma_counts.md", "w", encoding="utf-8") as f:
        f.write("# PRISMA Counts\n\n")
        f.write(f"{NOT_EXECUTED_MESSAGE}\n\n")
        f.write("## Why\n\n")
        for r in reasons:
            f.write(f"- {r}\n")
    for r in reasons:
        logger.warning(r)
    logger.info("Wrote NOT_EXECUTED status to %s", output_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Compute real PRISMA flow-diagram counts from search logs, "
                    "deduplication output, and screening decisions. Writes an explicit "
                    "NOT EXECUTED status instead of a number when real data is absent.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--search-log", type=Path, default=Path("templates/search_log.csv"))
    parser.add_argument("--dedup-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--title-abstract-screening", type=Path, default=None,
                        help="Path to a completed title/abstract screening CSV "
                             "(not the empty template)")
    parser.add_argument("--full-text-screening", type=Path, default=None,
                        help="Path to a completed full-text screening CSV "
                             "(not the empty template)")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--log-dir", type=Path, default=Path("logs"))
    args = parser.parse_args()

    logger = setup_logger(args.log_dir)
    logger.info("generate_prisma_counts.py starting")

    reasons = []

    search_log_rows = load_csv(args.search_log)
    real_search_rows = [r for r in search_log_rows if (r.get("raw_hits") or "").strip()]
    if not real_search_rows:
        reasons.append(f"No search has a populated raw_hits value in {args.search_log} "
                       "(the template is header-only until real searches are logged).")

    master_path = args.dedup_dir / "master_records.csv"
    confirmed_dup_path = args.dedup_dir / "confirmed_duplicates.csv"
    master_rows = load_csv(master_path)
    confirmed_dup_rows = load_csv(confirmed_dup_path)
    if not master_rows:
        reasons.append(f"{master_path} does not exist or is empty — run "
                       "deduplicate_records.py against real database exports first.")

    ta_rows = load_csv(args.title_abstract_screening) if args.title_abstract_screening else []
    ta_decided = [r for r in ta_rows if (r.get("final_decision") or "").strip()]
    if not args.title_abstract_screening:
        reasons.append("No --title-abstract-screening file supplied.")
    elif not ta_decided:
        reasons.append(f"{args.title_abstract_screening} has no rows with a populated "
                       "final_decision.")

    ft_rows = load_csv(args.full_text_screening) if args.full_text_screening else []
    ft_decided = [r for r in ft_rows if (r.get("final_decision") or "").strip()]
    if not args.full_text_screening:
        reasons.append("No --full-text-screening file supplied.")
    elif not ft_decided:
        reasons.append(f"{args.full_text_screening} has no rows with a populated "
                       "final_decision.")

    if reasons:
        write_not_executed(args.output_dir, logger, reasons)
        sys.exit(0)

    # Only reached if every input above contains real, decided data.
    records_identified = sum(int(r["raw_hits"]) for r in real_search_rows if r["raw_hits"].isdigit())
    duplicates_removed = len(confirmed_dup_rows)
    records_screened = len(ta_rows)
    excluded_ta = [r for r in ta_rows if r.get("final_decision") == "exclude"]
    records_excluded_title_abstract = len(excluded_ta)
    ta_exclusion_reasons = Counter(r.get("exclusion_reason", "") for r in excluded_ta)

    reports_sought = sum(1 for r in ft_rows if (r.get("full_text_sought") or "").strip().upper() == "TRUE")
    reports_not_retrieved = sum(
        1 for r in ft_rows
        if (r.get("full_text_sought") or "").strip().upper() == "TRUE"
        and (r.get("full_text_obtained") or "").strip().upper() != "TRUE"
    )
    reports_assessed = sum(1 for r in ft_rows if (r.get("full_text_obtained") or "").strip().upper() == "TRUE")
    excluded_ft = [r for r in ft_rows if r.get("final_decision") == "exclude"]
    reports_excluded_by_reason = Counter(r.get("primary_exclusion_reason", "") for r in excluded_ft)
    studies_included = sum(1 for r in ft_rows if r.get("final_decision") == "include")

    counts = {
        "status": "EXECUTED",
        "generated_at": datetime.now().isoformat(),
        "records_identified": records_identified,
        "duplicates_removed": duplicates_removed,
        "records_screened": records_screened,
        "records_excluded_title_abstract": records_excluded_title_abstract,
        "records_excluded_title_abstract_by_reason": dict(ta_exclusion_reasons),
        "reports_sought": reports_sought,
        "reports_not_retrieved": reports_not_retrieved,
        "reports_assessed": reports_assessed,
        "reports_excluded_by_reason": dict(reports_excluded_by_reason),
        "studies_included": studies_included,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with open(args.output_dir / "prisma_counts.json", "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=2)

    with open(args.output_dir / "prisma_counts.md", "w", encoding="utf-8") as f:
        f.write("# PRISMA Counts\n\n")
        f.write(f"Generated: {counts['generated_at']}\n\n")
        f.write(f"- Records identified (sum of raw_hits across all logged searches): {records_identified}\n")
        f.write(f"- Duplicates removed: {duplicates_removed}\n")
        f.write(f"- Records screened (title/abstract): {records_screened}\n")
        f.write(f"- Records excluded (title/abstract): {records_excluded_title_abstract}\n")
        for reason, n in ta_exclusion_reasons.items():
            f.write(f"    - {reason or '(blank)'}: {n}\n")
        f.write(f"- Reports sought for retrieval: {reports_sought}\n")
        f.write(f"- Reports not retrieved: {reports_not_retrieved}\n")
        f.write(f"- Reports assessed for eligibility: {reports_assessed}\n")
        f.write(f"- Reports excluded, by reason:\n")
        for reason, n in reports_excluded_by_reason.items():
            f.write(f"    - {reason or '(blank)'}: {n}\n")
        f.write(f"- Studies included: {studies_included}\n")

    logger.info("Wrote real PRISMA counts to %s", args.output_dir)
    logger.info("generate_prisma_counts.py finished")


if __name__ == "__main__":
    main()
