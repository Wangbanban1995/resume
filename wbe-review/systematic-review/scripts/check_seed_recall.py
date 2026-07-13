#!/usr/bin/env python3
"""Check whether the review's 44 seed references are recalled by the executed searches.

Reads templates/seed_studies.csv (44 references, with DOI/PMID/title/year/first_author
metadata and each seed's expected module) and cross-checks it against a real,
deduplicated master record set (normally data/processed/master_records.csv, produced by
deduplicate_records.py).

Recall status categories (per instruction — a title-only match is NEVER treated as
confirmed):

    RECALLED_CONFIRMED  — DOI exact match, PMID exact match, or normalized
                           title+year+first-author exact match
    POSSIBLE_RECALL     — normalized title alone, a fuzzy title match, or more than one
                           master record matching this seed (multiple candidates are
                           NEVER resolved by silently picking the first — every match is
                           listed and the seed is routed to manual review)
    NOT_RECALLED        — no master record matches by any basis
    UNTESTABLE          — the seed itself has neither a DOI/PMID nor a usable title

Two recall rates are reported and must not be conflated:
    confirmed_recall_rate  = RECALLED_CONFIRMED / testable seeds
    provisional_recall_rate = (RECALLED_CONFIRMED + POSSIBLE_RECALL) / testable seeds

Only confirmed_recall_rate may be quoted as "the search recalled this review's known
literature" — title-only/fuzzy/multi-candidate matches require human confirmation
(tracked via templates/manual_duplicate_review.csv) before they count as confirmed.

This script produces NO recall statistics of any kind when no real master record file is
supplied or when that file contains no records.

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
import urllib.parse
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


def summarize_matches(matches: list):
    databases, modules = set(), set()
    for m in matches:
        for db in (m.get("database_sources") or m.get("database_source", "")).split(";"):
            if db:
                databases.add(db)
        for mod in (m.get("search_modules") or m.get("search_module", "")).split(";"):
            if mod:
                modules.add(mod)
    return databases, modules


def main():
    parser = argparse.ArgumentParser(
        description="Check recall of the review's 44 seed references against a real "
                    "deduplicated master record set, using RECALLED_CONFIRMED / "
                    "POSSIBLE_RECALL / NOT_RECALLED / UNTESTABLE status categories.",
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
            "rate against nonexistent data.", args.master_csv,
        )
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with open(args.output_dir / "seed_recall_summary.md", "w", encoding="utf-8") as f:
            f.write("# Seed Recall Summary\n\nSTATUS: NOT EXECUTED — no master record "
                    f"file found at `{args.master_csv}`. Run the eight searches, then "
                    "`deduplicate_records.py`, then re-run this script.\n")
        sys.exit(0)

    master = load_csv(args.master_csv)
    if not master:
        logger.warning("Master record file %s exists but contains zero records.", args.master_csv)
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

    results = []
    n_confirmed = n_possible = n_not_recalled = n_untestable = 0
    n_multi_match = 0

    for seed in seeds:
        seed_doi = canonicalize_doi(seed.get("DOI", ""))
        seed_pmid = canonicalize_pmid(seed.get("PMID", ""))
        seed_title = normalize_title(seed.get("title", ""))
        seed_year = (seed.get("year") or "").strip()
        seed_author = (seed.get("first_author") or "").strip().lower()

        out = {k: seed.get(k, "") for k in seed.keys()}
        out.update({"recall_status": "", "failure_reason": "", "match_basis": "",
                   "matched_record_ids": "", "matched_titles": "",
                   "matched_database_sources": "", "matched_search_modules": "",
                   "manual_confirmation_required": "FALSE"})

        if not seed_doi and not seed_pmid and not seed_title:
            out["recall_status"] = "UNTESTABLE"
            out["failure_reason"] = "Seed has neither DOI, PMID, nor a usable title recorded"
            n_untestable += 1
            results.append(out)
            continue

        # --- RECALLED_CONFIRMED tiers: DOI, then PMID, then title+year+author ---
        matches, basis = None, None
        if seed_doi and seed_doi in doi_index:
            matches, basis = doi_index[seed_doi], "DOI"
        elif seed_pmid and seed_pmid in pmid_index:
            matches, basis = pmid_index[seed_pmid], "PMID"
        elif seed_title and seed_year and seed_author and \
                (seed_title, seed_year, seed_author) in title_year_author_index:
            matches, basis = title_year_author_index[(seed_title, seed_year, seed_author)], "title_year_first_author"

        if matches is not None:
            unique_ids = {m.get("record_id", "") for m in matches}
            if len(unique_ids) > 1:
                # Even a "confirmed-tier" basis can resolve to >1 distinct master record
                # (e.g. a genuinely ambiguous DOI collision) -- never default to the
                # first; always route to manual review instead.
                databases, modules = summarize_matches(matches)
                out["recall_status"] = "POSSIBLE_RECALL_MULTIPLE_MATCHES"
                out["match_basis"] = basis
                out["matched_record_ids"] = ";".join(sorted(unique_ids))
                out["matched_titles"] = ";".join(m.get("title", "") for m in matches)
                out["matched_database_sources"] = ";".join(sorted(databases))
                out["matched_search_modules"] = ";".join(sorted(modules))
                out["manual_confirmation_required"] = "TRUE"
                out["failure_reason"] = (f"{len(unique_ids)} distinct master records matched via "
                                         f"{basis} — must be resolved manually, not defaulted.")
                n_possible += 1
                n_multi_match += 1
                results.append(out)
                continue

            m = matches[0]
            out["recall_status"] = "RECALLED_CONFIRMED"
            out["match_basis"] = basis
            out["matched_record_ids"] = m.get("record_id", "")
            out["matched_titles"] = m.get("title", "")
            databases, modules = summarize_matches(matches)
            out["matched_database_sources"] = ";".join(sorted(databases))
            out["matched_search_modules"] = ";".join(sorted(modules))
            out["retrieved_by_core"] = "TRUE" if "core" in modules else "FALSE"
            out["manual_confirmation_required"] = "FALSE"
            n_confirmed += 1
            results.append(out)
            continue

        # --- POSSIBLE_RECALL tier: title-only match(es), never auto-confirmed ---
        if seed_title and seed_title in title_only_index:
            candidates = title_only_index[seed_title]
            unique_ids = {c.get("record_id", "") for c in candidates}
            databases, modules = summarize_matches(candidates)
            out["recall_status"] = ("POSSIBLE_RECALL_MULTIPLE_MATCHES" if len(unique_ids) > 1
                                    else "POSSIBLE_RECALL")
            out["match_basis"] = "title_only"
            out["matched_record_ids"] = ";".join(sorted(unique_ids))
            out["matched_titles"] = ";".join(c.get("title", "") for c in candidates)
            out["matched_database_sources"] = ";".join(sorted(databases))
            out["matched_search_modules"] = ";".join(sorted(modules))
            out["manual_confirmation_required"] = "TRUE"
            out["failure_reason"] = ("Matched by title alone" +
                                     (f" ({len(unique_ids)} distinct candidates)" if len(unique_ids) > 1 else "") +
                                     " — requires manual confirmation before counting as recalled.")
            n_possible += 1
            if len(unique_ids) > 1:
                n_multi_match += 1
            results.append(out)
            continue

        out["recall_status"] = "NOT_RECALLED"
        out["failure_reason"] = ("No master record matched this seed by DOI, PMID, or "
                                 f"title(+year/author). Revise the "
                                 f"'{seed.get('expected_module', 'unknown')}' search "
                                 "string and re-run.")
        n_not_recalled += 1
        results.append(out)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "seed_recall_report.csv"
    base_fields = list(seeds[0].keys())
    extra_fields = ["recall_status", "failure_reason", "match_basis", "matched_record_ids",
                    "matched_titles", "matched_database_sources", "matched_search_modules",
                    "manual_confirmation_required"]
    fieldnames = base_fields + [f for f in extra_fields if f not in base_fields]
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    n_total = len(seeds)
    testable = n_total - n_untestable
    confirmed_recall_rate = (100.0 * n_confirmed / testable) if testable else None
    provisional_recall_rate = (100.0 * (n_confirmed + n_possible) / testable) if testable else None

    summary_path = args.output_dir / "seed_recall_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Seed Recall Summary\n\n")
        f.write(f"Run date: {datetime.now().isoformat()}\n\n")
        f.write(f"- Total seed references: {n_total}\n")
        f.write(f"- Untestable (no DOI/PMID/title recorded for the seed itself): {n_untestable}\n")
        f.write(f"- Testable: {testable}\n\n")
        f.write(f"- confirmed_recalled (RECALLED_CONFIRMED): {n_confirmed}\n")
        f.write(f"- possible_recalled (POSSIBLE_RECALL, incl. multi-match): {n_possible} "
                f"(of which {n_multi_match} have multiple candidate matches requiring manual resolution)\n")
        f.write(f"- not_recalled (NOT_RECALLED): {n_not_recalled}\n")
        f.write(f"- untestable (UNTESTABLE): {n_untestable}\n\n")
        if testable:
            f.write(f"- **confirmed_recall_rate = {n_confirmed}/{testable} = {confirmed_recall_rate:.1f}%** "
                    "(only DOI/PMID/title+year+author matches — the only rate that may be "
                    "quoted as \"recalled\" without further manual confirmation)\n")
            f.write(f"- provisional_recall_rate = ({n_confirmed}+{n_possible})/{testable} = "
                    f"{provisional_recall_rate:.1f}% (includes unconfirmed title-only/fuzzy/"
                    "multi-match candidates — NOT a confirmed figure)\n\n")
        else:
            f.write("- confirmed_recall_rate / provisional_recall_rate: undefined (no testable seeds)\n\n")

        if n_possible > 0:
            f.write("## Possible recalls requiring manual confirmation "
                    "(see templates/manual_duplicate_review.csv)\n\n")
            for r in results:
                if r["recall_status"] in ("POSSIBLE_RECALL", "POSSIBLE_RECALL_MULTIPLE_MATCHES"):
                    f.write(f"- {r.get('ref_number', '')} [{r['recall_status']}, basis="
                            f"{r['match_basis']}]: candidate record_id(s) "
                            f"{r['matched_record_ids']}\n")
        if n_not_recalled > 0:
            f.write("\n## Not recalled — revise the corresponding module search string\n\n")
            for r in results:
                if r["recall_status"] == "NOT_RECALLED":
                    f.write(f"- {r.get('ref_number', '')} (expected module: "
                            f"{r.get('expected_module', '')}): {r.get('citation', '')[:100]}\n")

    logger.info("Wrote %s and %s", report_path, summary_path)
    logger.info("confirmed=%d possible=%d (multi-match=%d) not_recalled=%d untestable=%d",
               n_confirmed, n_possible, n_multi_match, n_not_recalled, n_untestable)
    if n_not_recalled > 0:
        logger.warning("%d seed reference(s) NOT_RECALLED — revise and re-test the "
                       "affected module string(s) before treating the search as final.",
                       n_not_recalled)
    if n_multi_match > 0:
        logger.warning("%d seed reference(s) matched multiple distinct master records — "
                       "none were auto-resolved; route to manual review via "
                       "templates/manual_duplicate_review.csv.", n_multi_match)
    logger.info("check_seed_recall.py finished")


if __name__ == "__main__":
    main()
