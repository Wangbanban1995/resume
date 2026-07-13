# Test Results — Systematic Review Execution Toolkit

Run date: 2026-07-13 (real-data-readiness hardening round). All fixtures under
`tests/` are explicitly synthetic (fabricated for script-testing purposes only,
clearly labeled `SYNTHETIC TEST RECORD`/`Casetest`/etc. in every abstract or author
field) and must never be treated as, or quoted as, a real search result. None of the
review's 51 real references were used to simulate a real search result anywhere in
this test suite — the only real data used is the 44-row `templates/seed_studies.csv`
metadata (title/year/author/DOI/PMID), used strictly to test whether the *matching
logic* correctly recognizes a real seed against synthetic master records, never to
claim a real recall rate.

---

## 1. Unit tests — canonicalization functions

| Test name | Expected result | Actual result | Status |
|---|---|---|---|
| `canonicalize_doi`: bare DOI | `10.1016/j.watres.2025.124977` | `10.1016/j.watres.2025.124977` | PASS |
| `canonicalize_doi`: `https://doi.org/` prefix | same canonical DOI | same canonical DOI | PASS |
| `canonicalize_doi`: `DOI: ... .` prefix + trailing period | same canonical DOI | same canonical DOI | PASS |
| `canonicalize_doi`: `http://dx.doi.org/` prefix | same canonical DOI | same canonical DOI | PASS |
| `canonicalize_doi`: mixed case + whitespace | same canonical DOI, lowercased | same canonical DOI, lowercased | PASS |
| `canonicalize_doi`: trailing `[doi]` tag | same canonical DOI | same canonical DOI | PASS |
| `canonicalize_doi`: empty string | `""` | `""` | PASS |
| `canonicalize_pmid`: bare digits | `12345678` | `12345678` | PASS |
| `canonicalize_pmid`: `PMID:`/`PMID: ` prefix | `12345678` | `12345678` | PASS |
| `canonicalize_pmid`: WoS accession number `WOS:000123456789` | `""` (must NOT be read as a PMID) | `""` | PASS |
| `canonicalize_pmid`: empty string | `""` | `""` | PASS |

## 2. `--help` and safe-exit (no real data) — all four scripts

| Test name | Expected result | Actual result | Status |
|---|---|---|---|
| `deduplicate_records.py --help` | prints usage, exit 0 | prints usage, exit 0 | PASS |
| `deduplicate_records.py` against empty `data/raw/` | warns, writes nothing, exit 0 | warns, writes nothing, exit 0 | PASS |
| `check_seed_recall.py --help` | prints usage, exit 0 | prints usage, exit 0 | PASS |
| `check_seed_recall.py` with no `master_records.csv` | `STATUS: NOT EXECUTED`, exit 0 | `STATUS: NOT EXECUTED`, exit 0 | PASS |
| `generate_prisma_counts.py --help` | prints usage, exit 0 | prints usage, exit 0 | PASS |
| `generate_prisma_counts.py` with only empty templates | `STATUS: NOT EXECUTED` + itemized reasons, exit 0 | `STATUS: NOT EXECUTED` + itemized reasons, exit 0 | PASS |
| `validate_search_inputs.py --help` | prints usage, exit 0 | prints usage, exit 0 | PASS |
| `validate_search_inputs.py` against empty `data/raw/` and empty search log | `STATUS: NOT_READY`, exit 0 | `STATUS: NOT_READY` (25 blocking issues), exit 0 | PASS |

## 3. General smoke test (`tests/synthetic_fixtures/`, re-run against the hardened script)

9 synthetic records across 4 formats (RIS ×3, CSV ×3, NBIB ×2, BibTeX ×1).

| Test name | Expected result | Actual result | Status |
|---|---|---|---|
| Parse all 4 formats | 9 records parsed (3+3+2+1) | 9 records parsed (3+3+2+1) | PASS |
| Exact-DOI duplicate across WoS RIS (×2) and Scopus CSV (×1), same DOI | 1 master + 2 confirmed duplicates | 1 master (`dd3f7aa3f89f`, occurrence_count=3, database_sources=`scopus;wos`) + 2 confirmed duplicates | PASS |
| Near-duplicate title, hyphen vs. space ("Fuzzy-Match" vs. "Fuzzy Match"), same year, no DOI | merged via `title_year` (hyphens now normalize to spaces, resolving the prior round's known gap) | merged via `title_year` | PASS — **previously-documented limitation now resolved** (see §6) |
| `parsing_quality_report.csv` generated | one row per source file with parse stats | 4 rows, all `parse_status=ok` except the BibTeX fallback-parser warning correctly logged | PASS |
| BibTeX file with no recognizable module in filename | `unknown_module=True`, warning logged | `unknown_module=True`, warning logged, fallback-parser notice logged | PASS |
| PRISMA counts computed from synthetic screening files derived from this run | records_identified=10, duplicates_removed=3, records_screened=3, excluded=1 (not_WBE), reports_sought=2, not_retrieved=1, assessed=1, excluded_by_reason={full_text_unavailable:1}, included=1 | exactly as expected, independently re-verified against the input files by hand | PASS |

## 4. Seed recall — real seeds against synthetic master data

| Test name | Expected result | Actual result | Status |
|---|---|---|---|
| Load 44 real seeds | 44 rows loaded | 44 rows loaded | PASS |
| Seed [48] Safford et al. — synthetic master record carries the real DOI | `RECALLED (DOI)`, `manual_confirmation_required=FALSE` | `RECALLED (DOI)`, `manual_confirmation_required=FALSE` | PASS |
| Remaining 43 seeds against unrelated synthetic data | `NOT_RECALLED` | 43× `NOT_RECALLED` | PASS |
| Untestable count | 0 (all 44 seeds have a title on file) | 0 | PASS — **improved from the prior round**, which incorrectly marked 15 title-having seeds `UNTESTABLE` |

## 5. New hardening test cases (10 required)

| # | Test name | Expected result | Actual result | Status |
|---|---|---|---|---|
| 1 | **DOI variants merge correctly** — bare DOI, `https://doi.org/...`, and `DOI: ... .` all referring to the same paper (`tests/case01_doi_variants/`) | All 3 records merge into 1 master record | 1 master record, `occurrence_count=3`, both variant-DOI records in `confirmed_duplicates.csv` with `duplicate_match_basis=DOI` | PASS |
| 2 | **Multi-line RIS title/abstract not lost** (`tests/case02_multiline_ris/`) — title wraps 3 physical lines, abstract wraps 5 | Full title and full abstract text preserved, no truncation | Title and abstract both fully concatenated, verified by direct string inspection | PASS |
| 3 | **Multi-line NBIB abstract not lost** (`tests/case03_multiline_nbib/`) — title and abstract both wrap across indented continuation lines | Full title and abstract preserved | Both fully concatenated | PASS |
| 4 | **Same paper from 3 databases + 3 modules aggregates fully** (`tests/case04_three_db_aggregation/`) — identical DOI in WoS/core, Scopus/module05, PubMed/module07 | 1 master record with `database_sources=pubmed;scopus;wos`, `search_modules=core;module05;module07`, `occurrence_count=3`, PMID backfilled from the PubMed copy | Exactly as expected | PASS |
| 5 | **Same title, different year AND different author — never auto-merged** (`tests/case05_version_conflict/`) — identical title, 2018/Firstauthor vs. 2023/Secondauthor | 2 separate master records, 0 confirmed duplicates, the second flagged `possible_duplicate` with `possible_version_relation=identical_title_year_and_author_both_differ` | Exactly as expected | PASS |
| 6 | **Seed without DOI/PMID recalled via title+year+author** (`tests/case06_title_year_author_recall/`) — synthetic master record for [41] Zuccato et al. with matching title/year/author, no DOI/PMID | `RECALLED (title_year_first_author)`, `manual_confirmation_required=FALSE` | Exactly as expected | PASS |
| 7 | **Missing export file → `NOT_READY`** (`tests/case07_missing_files/`) — search log references a file that was never created | `STATUS: NOT_READY` with a blocking issue naming the missing file | `NOT_READY` (24 blocking: 1 missing-file + 23 missing search-log combinations) | PASS |
| 8 | **Search-log count vs. actual parsed count mismatch → warning** (`tests/case08_count_mismatch/`) — log says `exported_records=5`, file actually contains 2 records | A warning naming the exact logged-vs-actual mismatch | `"wos_core_case08_20260713.ris: search log says exported_records=5, but the file actually parses to 2 record(s)."` | PASS |
| 9 | **Wrong module number in filename detected** (`tests/case09_wrong_module/`) — file named with an invalid `module99` | Warnings for both the naming-convention mismatch and the search-log/filename module mismatch | Both warnings fired exactly as expected; overall `NOT_READY` (the invalid combination cannot satisfy the 8×3 plan) | PASS |
| 10 | **All real data directories remain empty throughout** | `data/raw/{wos,scopus,pubmed}/`, `data/processed/`, `reports/`, `logs/` contain only `.gitkeep` after the full test run | Confirmed empty (one stray log file from an earlier default-path smoke test was found and removed before this report was finalized) | PASS |

## 6. Bugs found and fixed during this hardening round (via testing, not by inspection alone)

1. **Cross-attribution bug in `database_module_summary.csv`.** The first implementation computed the summary as the cartesian product of a master record's `database_sources` and `search_modules` lists, which fabricated attributions that never occurred (e.g., a record seen only via `scopus/module05` and `wos/core` was incorrectly also counted under `scopus/core` and `wos/module05`). Fixed by tracking exact `(database, module)` occurrence pairs internally (`_db_module_pairs`, not written to the output CSV) rather than deriving them from the two flattened lists. Caught by inspecting `tests/case04_three_db_aggregation/`'s output during this round, before it was reported as complete.
2. **`validate_search_inputs.py` under-reported severity for incomplete search plans.** The first implementation only treated a missing (database, search_id) combination as `blocking` when the search log was entirely empty, and as a mere `warning` otherwise — so a log with, e.g., 1 of 24 required rows populated would incorrectly report `READY_WITH_WARNINGS`. Fixed so a missing combination is always `blocking`, since an incomplete 8×3 search plan should never be treated as ready for downstream deduplication/PRISMA counting. Caught while building test case 8.
3. **Title-normalization hyphen handling** (carried over from the previous round's documented limitation): punctuation, including hyphens, is now replaced with a space rather than deleted during title normalization, so "Fuzzy-Match" and "Fuzzy Match" normalize identically. This resolves the near-duplicate-title gap flagged in the prior round's test report (see §3) as a side effect of the DOI/PMID canonicalization work, not a separate fix.

## 7. Known limitations carried forward

- **Fuzzy title matching (Jaccard token overlap ≥ 0.8, same year)** remains the final fallback for records with no DOI/PMID, no exact title+year, no exact title+author, and no exact title+year+author match. It has not been tuned against a large real-world near-duplicate sample, since none exists yet. Revisit once real WoS/Scopus/PubMed exports are available.
- **BibTeX parsing remains fallback/experimental** (see `README.md` §2) — not hardened to the same degree as RIS/NBIB/CSV in this round, per instruction, since it is not the production import path for any of the three target databases.
- **Version-conflict detection (correction/erratum, protocol, preprint, conference abstract) is heuristic**, based on title keywords and journal/source-name substrings. It will not catch every real-world case (e.g., a correction with a title that doesn't contain the word "correction") and may occasionally over-flag (e.g., a legitimate primary study with "protocol" in its title). It is deliberately biased toward flagging for manual review rather than silently auto-merging, consistent with instruction.
- **`validate_search_inputs.py`'s duplicate-filename check** compares filenames only, not file content — two different files that happen to share a name in different directories are flagged, but a byte-identical file saved under two different names is not currently caught. Not required by the current instruction; noted for a future round if needed.

---

## Exact run order for real data import (once WoS/Scopus/PubMed exports are available)

1. Place raw exports into `data/raw/{wos,scopus,pubmed}/` following the naming convention in `README.md` §3, and fill in every row of `templates/search_log.csv` as each search is run (`README.md` §1).
2. Run `python3 scripts/validate_search_inputs.py` — do not proceed while the status is `NOT_READY`.
3. Run `python3 scripts/deduplicate_records.py` — inspect `data/processed/parsing_quality_report.csv` for any zero-record or high-missing-title warnings before trusting `master_records.csv`.
4. Run `python3 scripts/check_seed_recall.py` — if any of the 44 seeds is `NOT_RECALLED`, revise and re-run the corresponding module's search (back to step 1) before treating the search as final, per Section 13 of `WBE_Review_Systematic_Search_Strategy.md`.
5. Perform title/abstract screening (`templates/title_abstract_screening.csv`), then full-text screening (`templates/full_text_screening.csv`) — both manual steps.
6. Run `python3 scripts/generate_prisma_counts.py` against the completed screening files.
7. Populate `templates/data_extraction.csv` and `templates/chapter_claim_audit.csv` for every included, full-text-obtained record, then update `../WBE_Review_Citation_Verification_Table.md` and `../WBE_Review_Ch8_Evidence_Freeze_Audit.md` per `README.md` §10.
