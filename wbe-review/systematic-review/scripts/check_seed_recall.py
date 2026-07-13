#!/usr/bin/env python3
"""Check whether the review's 44 seed references are recalled by the executed searches.

Reads templates/seed_studies.csv (44 references, with DOI/PMID/title/year/first_author
metadata and each seed's expected module) and cross-checks it against a real,
deduplicated master record set (normally data/processed/master_records.csv, produced by
deduplicate_records.py).

Match priority (per instruction):
    1. Exact canonical-DOI match
    2. Exact canonical-PMID match
    3. Normalized title + year + first author match
    4. Normalized title match alone -> flagged RECALLED but manual_confirmation_required=TRUE
       (title-only matches are not treated as fully confirmed automatically)

A seed is marked UNTESTABLE only when it lacks enough bibliographic information to
attempt any of the four match bases above (i.e., no DOI, no PMID, AND no usable title).
A seed with only a title (no DOI/PMID) is still testable via basis 3 or 4.

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
import re
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


def canonicalize_doi(value: str) -> str:
    if not value:
        return ""
    v = value.strip()
    if not v:
        return ""
    import urllib.parse
    v = urllib.parse.unquote(v)
    v = re.sub(r"(?i)^doi:\s*", "", v.strip())
    v = re.sub(r"(?i)^https?://(dx\.)?doi\.org/", "", v.strip())
    v = re.sub(r"(?i)\s*\[doi\]\s*$", "", v)
    v = v.strip()
    v = re.sub(r"[.,;\)\]]+$", "", v)
    return v.strip().lower()


def canonicalize_pmid(value: str) -> str:
    if not value:
        return ""
    v = value.strip()
    v = re.sub(r"(?i)^pmid:?\s*", "", v).strip()
    return v if re.fullmatch(r"\d+", v) else ""


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
    parser.add_argument("--seed-csv", type=Path, default=Path("templates/seed_studies.csv"))
    parser.add_argument("--master-csv", type=Path, default=Path("data/processed/master_records.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    parser.add_argument("--log-dir", type=Path, default=Path("logs"))
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
        with open(args.output_dir / "seed_recall_summary.md", "w", encoding="utf-8") as f:
            f.write("# Seed Recall Summary\n\nSTATUS: NOT EXECUTED — no master record "
                    f"file found at `{args.master_csv}`. Run the eight searches, then "
                    "`deduplicate_records.py`, then re-run this script.\n")
        sys.exit(0)

    master = load_csv(args.master_csv)
    if not master:
        logger.warning(
            "Master record file %s exists but contains zero records. Treating this the "
            "same as 'no real search executed yet'.", args.master_csv,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with open(args.output_dir / "seed_recall_summary.md", "w", encoding="utf-8") as f:
            f.write(f"# Seed Recall Summary\n\nSTATUS: NOT EXECUTED — "
                    f"`{args.master_csv}` contains zero records.\n")
        sys.exit(0)

    logger.info("Loaded %d master records from %s", len(master), args.master_csv)

    doi_index, pmid_index = {}, {}
    title_year_author_index, title_only_index = {}, {}
    for m in master:
        m_doi = canonicalize_doi(m.get("DOI", ""))
        m_pmid = canonicalize_pmid(m.get("PMID", ""))
        m_title = normalize_title(m.get("title", ""))
        m_author = first_author_surname(m.get("authors", ""))
        m_year = (m.get("year") or "").strip()
        if m_doi:
            doi_index.setdefault(m_doi, []).append(m)
        if m_pmid:
            pmid_index.setdefault(m_pmid, []).append(m)
        if m_title:
            title_only_index.setdefault(m_title, []).append(m)
            if m_year and m_author:
                title_year_author_index.setdefault((m_title, m_year, m_author), []).append(m)

    def matched_fields(matches, basis, manual_confirm):
        databases, modules = set(), set()
        for m in matches:
            for db in (m.get("database_sources") or m.get("database_source", "")).split(";"):
                if db:
                    databases.add(db)
            for mod in (m.get("search_modules") or m.get("search_module", "")).split(";"):
                if mod:
                    modules.add(mod)
        first = matches[0]
        return {
            "match_basis": basis,
            "matched_record_id": first.get("record_id", ""),
            "matched_title": first.get("title", ""),
            "matched_database_sources": ";".join(sorted(databases)),
            "matched_search_modules": ";".join(sorted(modules)),
            "manual_confirmation_required": "TRUE" if manual_confirm else "FALSE",
        }

    results = []
    n_recalled = 0
    n_manual = 0
    for seed in seeds:
        seed_doi = canonicalize_doi(seed.get("DOI", ""))
        seed_pmid = canonicalize_pmid(seed.get("PMID", ""))
        seed_title = normalize_title(seed.get("title", ""))
        seed_year = (seed.get("year") or "").strip()
        seed_author = first_author_surname(seed.get("first_author", "")) or \
            (seed.get("first_author") or "").strip().lower()

        if not seed_doi and not seed_pmid and not seed_title:
            seed["recall_status"] = "UNTESTABLE"
            seed["failure_reason"] = "Seed has neither DOI, PMID, nor a usable title recorded"
            for k in ("match_basis", "matched_record_id", "matched_title",
                     "matched_database_sources", "matched_search_modules",
                     "manual_confirmation_required"):
                seed[k] = ""
            results.append(seed)
            continue

        matches, basis, manual_confirm = None, None, False

        if seed_doi and seed_doi in doi_index:
            matches, basis = doi_index[seed_doi], "DOI"
        elif seed_pmid and seed_pmid in pmid_index:
            matches, basis = pmid_index[seed_pmid], "PMID"
        elif seed_title and seed_year and seed_author and \
                (seed_title, seed_year, seed_author) in title_year_author_index:
            matches, basis = title_year_author_index[(seed_title, seed_year, seed_author)], "title_year_first_author"
        elif seed_title and seed_title in title_only_index:
            matches, basis, manual_confirm = title_only_index[seed_title], "title_only", True

        if matches:
            n_recalled += 1
            if manual_confirm:
                n_manual += 1
            seed["recall_status"] = f"RECALLED ({basis})"
            seed["failure_reason"] = ""
            seed.update(matched_fields(matches, basis, manual_confirm))
            databases = seed["matched_database_sources"]
            modules = seed["matched_search_modules"]
            seed["retrieved_by_core"] = "TRUE" if "core" in modules.split(";") else "FALSE"
            seed["retrieved_by_module"] = ";".join(m for m in modules.split(";") if m != "core")
            seed["retrieved_database"] = databases
        else:
            seed["recall_status"] = "NOT_RECALLED"
            seed["failure_reason"] = (
                "No master record matched this seed by DOI, PMID, or title(+year/author). "
                f"Revise the '{seed.get('expected_module', 'unknown')}' search string and re-run."
            )
            for k in ("match_basis", "matched_record_id", "matched_title",
                     "matched_database_sources", "matched_search_modules",
                     "manual_confirmation_required"):
                seed[k] = ""

        results.append(seed)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "seed_recall_report.csv"
    fieldnames = list(seeds[0].keys())
    for extra in ("match_basis", "matched_record_id", "matched_title",
                  "matched_database_sources", "matched_search_modules",
                  "manual_confirmation_required"):
        if extra not in fieldnames:
            fieldnames.append(extra)
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
        f.write(f"- Untestable (no DOI/PMID/title recorded for the seed itself): {n_untestable}\n")
        f.write(f"- Testable: {testable}\n")
        f.write(f"- Recalled: {n_recalled} (of which {n_manual} matched by title alone "
                f"and require manual confirmation)\n")
        f.write(f"- Not recalled: {n_not_recalled}\n")
        if testable > 0:
            rate = 100.0 * n_recalled / testable
            f.write(f"- Recall rate (of testable seeds): {rate:.1f}%\n\n")
        else:
            f.write("- Recall rate: undefined (no testable seeds)\n\n")
        if n_manual > 0:
            f.write("## Recalled by title only — require manual confirmation\n\n")
            for r in results:
                if r.get("manual_confirmation_required") == "TRUE":
                    f.write(f"- {r.get('ref_number', '')}: matched master record "
                            f"{r.get('matched_record_id', '')} by title alone — confirm "
                            "this is genuinely the same paper (not a same-titled different "
                            "study, correction, or version) before treating as verified.\n")
        if n_not_recalled > 0:
            f.write("\n## Seeds not recalled — revise the corresponding module search string\n\n")
            for r in results:
                if r["recall_status"] == "NOT_RECALLED":
                    f.write(f"- {r.get('ref_number', '')} (expected module: "
                            f"{r.get('expected_module', '')}): {r.get('citation', '')[:100]}\n")

    logger.info("Wrote %s and %s", report_path, summary_path)
    logger.info("Recalled %d / %d testable seeds (%d require manual confirmation)",
               n_recalled, testable, n_manual)
    if n_not_recalled > 0:
        logger.warning("%d seed reference(s) were NOT recalled — see %s. Per Section 13 "
                       "of the search strategy, revise and re-test the affected module "
                       "string(s) before treating the search as final.",
                       n_not_recalled, summary_path)
    logger.info("check_seed_recall.py finished")


if __name__ == "__main__":
    main()
