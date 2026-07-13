# Synthetic Test Results — Systematic Review Execution Toolkit

Run date: 2026-07-13. All test data in `tests/synthetic_fixtures/` is explicitly synthetic
(fabricated for script-testing purposes only, clearly labeled `SYNTHETIC TEST RECORD` in
every abstract field) and is not, and must never be treated as, a real search result.
One fixture record intentionally reuses the real DOI of reference [48] (Safford et al.,
2022) specifically to test the seed-recall script's "RECALLED" code path — this is a test
of script logic, not a claim that a real database search retrieved anything.

## 1. `--help` output

Confirmed all three scripts (`deduplicate_records.py`, `check_seed_recall.py`,
`generate_prisma_counts.py`) print usage/argument help via `--help` and exit 0.

## 2. Safe-exit behavior with no real data

| Script | Behavior with no real input | Result |
|---|---|---|
| `deduplicate_records.py` | Run against empty `data/raw/` | Logged a warning, wrote no output files, exited 0 — PASS |
| `check_seed_recall.py` | Run with no `master_records.csv` present | Wrote `seed_recall_summary.md` with `STATUS: NOT EXECUTED`, exited 0 — PASS |
| `generate_prisma_counts.py` | Run with only the empty templates present | Wrote `prisma_counts.md`/`.json` with `STATUS: NOT EXECUTED` and an itemized list of which inputs were missing, exited 0 — PASS |

None of the three scripts produced a fabricated number, an empty-but-plausible-looking
report, or a silent failure in the no-data case.

## 3. Synthetic-data execution test

Fixtures: `tests/synthetic_fixtures/{wos,scopus,pubmed}/` — 4 files (RIS, CSV, NBIB,
BibTeX), 9 synthetic records total, including one intentional exact-DOI duplicate pair
(to test `confirmed_duplicates`) and one near-duplicate title pair with no DOI ("Fuzzy-Match"
vs "Fuzzy Match" — see note below).

`deduplicate_records.py --input-dir tests/synthetic_fixtures --output-dir
tests/synthetic_output`:
- Parsed 9 records across all 4 formats correctly (RIS: 3, CSV: 3, NBIB: 2, BibTeX: 1) — PASS, confirms all four required formats parse.
- Correctly identified 2 confirmed duplicates by exact DOI match, across two different source files/databases (Scopus CSV record treated as master since files are processed in alphabetical directory order; both WoS RIS copies correctly matched to it as duplicates) — PASS.
- The near-duplicate "Fuzzy-Match" vs "Fuzzy Match" title pair was **not** flagged as `possible_duplicate` — computed token overlap was 0.727, just below the script's 0.8 threshold (hyphens are stripped rather than treated as spaces during normalization, so "Fuzzy-Match" becomes one token, "Fuzzy Match" becomes two). This is a known, documented limitation of the current normalization approach, not a crash or silent failure — the 0.8 threshold is intentionally conservative to avoid falsely flagging distinct titles, per the instruction that fuzzy matches must never be auto-removed. Recommend revisiting the threshold or the hyphen-handling rule once real data shows how often this pattern occurs in practice.
- `database_module_summary.csv` correctly attributed records per database/module.

`check_seed_recall.py --seed-csv templates/seed_studies.csv --master-csv
tests/synthetic_output/master_records.csv`:
- Loaded all 44 real seed references — PASS.
- Correctly recalled exactly 1 of 29 testable seeds ([48] Safford et al., via the intentionally-matching synthetic DOI) — PASS, confirms the DOI-matching logic works against the review's real seed list.
- Correctly reported 15 "UNTESTABLE" seeds (no DOI/PMID on file for that seed) and 28 "NOT_RECALLED" (expected, since the other 28 have no corresponding synthetic record) — PASS.
- This 3.4% "recall rate" is a synthetic-data artifact, not a real recall rate, and must not be quoted as one.

`generate_prisma_counts.py` with synthetic search-log/screening files:
- Correctly computed records_identified=10, duplicates_removed=2, records_screened=3, records_excluded_title_abstract=1 (reason: not_WBE), reports_sought=2, reports_not_retrieved=1, reports_assessed=1, reports_excluded_by_reason={full_text_unavailable: 1}, studies_included=1 — PASS, all arithmetic independently verified against the synthetic input files.

## 4. Template integrity check

All 7 CSV templates in `templates/` open correctly via Python's `csv` module with the
expected column counts (`chapter_claim_audit.csv`: 12, `data_extraction.csv`: 65,
`full_text_screening.csv`: 15, `search_log.csv`: 14, `seed_studies.csv`: 11 (44 real
seed rows, all other real templates 0 data rows as required), `table_cell_evidence_audit.csv`: 10,
`title_abstract_screening.csv`: 12) — PASS.

## 5. Known limitation carried forward

The fuzzy-title-matching threshold (token Jaccard overlap ≥ 0.8, same year) is a
reasonable conservative default but was not tuned against a large real-world duplicate
sample, since none exists yet. Revisit once real WoS/Scopus/PubMed exports are available
and `possible_duplicates.csv` can be reviewed against genuine near-duplicate records.

## 6. Cleanup

`tests/synthetic_output/` and `tests/synthetic_logs/` (script-generated outputs from this
test run) are retained alongside this report for inspection but are clearly separate from
`data/raw/`, `data/processed/`, `reports/`, and `logs/` (which remain real-data-only and
currently empty except for `.gitkeep` files).
