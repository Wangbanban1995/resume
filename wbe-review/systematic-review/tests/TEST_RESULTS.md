# Test Results — Systematic Review Execution Toolkit

**Latest round: 2026-07-14, pilot-mode CLI addition (first real database import trial run).** This document supersedes the previous round's report; §0 below is this round's new coverage, §1–§5 retain the 2026-07-13 "final deduplication safety patch" round's results for continuity (all still valid and re-verified — see §0.3). All fixtures under `tests/` are explicitly synthetic (fabricated for script-testing purposes only, clearly labeled `SYNTHETIC TEST RECORD`/`Casetest`/`Pilottest`/etc.) and must never be treated as, or quoted as, a real search result. The only real data used anywhere in this test suite is the 44-row `templates/seed_studies.csv` metadata (title/year/author/DOI/PMID), used strictly to test whether the *matching logic* recognizes a real seed against synthetic master records — never to claim a real recall rate.

**Status after this round: as of 2026-07-14, an actual pilot readiness check was run against the real (empty) `data/raw/` and `templates/search_log.csv` — see §0.4. No real pilot files (PubMed core NBIB, WoS Module 2 RIS, Scopus Module 5 CSV) have been supplied to this toolkit yet; Sections 4–9 of the pilot import workflow (manual spot-check, pilot dedup, pilot manual-duplicate-review pre-fill, pilot seed recall, `pilot_import_report.md`) remain not started, pending those real files.**

---

## 0. This round (2026-07-14): pilot-mode CLI for `validate_search_inputs.py` and `deduplicate_records.py`

### 0.1 `validate_search_inputs.py --mode pilot`

New `--mode {production,pilot}` (default `production`, unchanged behavior) and repeatable `--expected-search DATABASE_SEARCHID` arguments (`tests/case20_pilot_mode/`).

| # | Test | Expected | Actual | Status |
|---|---|---|---|---|
| 1 | **Complete pilot fixture (3/3 files + search log rows present)** — `pubmed_core`, `wos_module02`, `scopus_module05` synthetic exports | `PILOT_READY` / `PRODUCTION_NOT_READY`, exit 0, `logs/pilot_raw_file_checksums.csv` has 3 real SHA-256 rows | Exactly as expected; checksums independently verified against `sha256sum` | PASS |
| 2 | **One pilot combination missing from search log** (`wos_module02` row removed) | `PILOT_NOT_READY`, exit 1, a `blocking` issue naming the missing combination, the other 21 non-pilot combinations reported as non-blocking `info` only | Exactly as expected (`tests/case20_pilot_mode/search_log_missing_wos.csv`) | PASS |
| 3 | **`--mode pilot` with no `--expected-search`** | Clear error, `PILOT_NOT_READY`/`PRODUCTION_NOT_READY` printed, exit 2 | Exactly as expected | PASS |
| 4 | **`--mode pilot --expected-search notadatabase_core`** (malformed combo) | Clear error naming the invalid value, exit 2 | Exactly as expected | PASS |
| 5 | **Production mode (default, no `--mode` flag) unchanged** — reran against the existing `case07_missing_files` fixture | Same blocking-issue count (24) as the original 2026-07-13 recorded run | Exactly matched (24 blocking in both runs); the only difference was warning count, traced to this ad hoc rerun pointing `--raw-dir` at a differently-populated directory than the original run, not a code change — confirmed by inspecting the actual code path, which is untouched for `--mode production` | PASS |

### 0.2 `deduplicate_records.py --mode pilot --parse-only`

New `--mode {production,pilot}`, `--parse-only`, `--search-log`, and `--interim-dir` arguments. Parses real files without ever calling `deduplicate()`.

| # | Test | Expected | Actual | Status |
|---|---|---|---|---|
| 6 | **Complete pilot fixture, 3 files, 4 records total** | `data/interim/pilot_parsed_records.csv` (4 rows, real `record_id`s), `pilot_parsing_quality_report.csv` with `exported_records` from the search log matching `records_parsed` (`diff=0` for all 3 files), `logs/pilot_parse_log.txt` states "NO DEDUPLICATION HAS BEEN RUN" | Exactly as expected | PASS |
| 7 | **`unknown_fields` detection** — ad hoc probe fixture with an unrecognized RIS tag (`C1`) and two unrecognized CSV columns (`Funding Details`, `Cited by`) | `unknown_fields` column lists exactly the unrecognized tag/column names, `unknown_fields_count` correct | Exactly as expected (`C1` for RIS; `Cited by;Funding Details` for CSV) | PASS |
| 8 | **No search log at all** (nonexistent `--search-log` path) | `exported_records` and `diff_parsed_minus_exported` left blank (not fabricated), parsing still succeeds | Exactly as expected | PASS |
| 9 | **`--mode pilot` without `--parse-only`** | Clear error explaining pilot deduplication is a separate, later, human-gated step; exit 2; `deduplicate()` never called | Exactly as expected | PASS |
| 10 | **Production mode (default) regression** — reran all of `case01`–`case18` (excluding the `validate_search_inputs.py`-only cases) against clean copies of their original fixtures | Field-for-field identical output to the 2026-07-13 recorded runs (record_id and any embedded duplicate_record_ids necessarily differ, since that hash is derived from the full file path and this rerun used a different temp path — confirmed by direct inspection that this is the *only* difference in every case) | Confirmed identical on titles/abstracts/authors/years/DOIs/PMIDs/merge decisions/`duplicate_match_basis`/`occurrence_count` for all 15 re-run cases; integrity status `PASS` in every case that produces one | PASS |

### 0.3 Regression re-verification

All of §1–§5 below (the 2026-07-13 round's 11 named test cases plus the general smoke test) were re-run against this round's code with the new `--mode`/`--parse-only`/`unknown_fields`-tracking additions in place, confirming zero behavioral change to the default (production) code path — see test 5 and test 10 above for the verification method.

### 0.4 Real pilot readiness check against actual repository state (2026-07-14)

Per this round's task, `validate_search_inputs.py --mode pilot --expected-search pubmed_core --expected-search wos_module02 --expected-search scopus_module05` was run against the **real** `data/raw/` and `templates/search_log.csv` (no synthetic substitution). Result: `PILOT_NOT_READY` / `PRODUCTION_NOT_READY`, exit 1. `data/raw/{wos,scopus,pubmed}/` contain only `.gitkeep`; `templates/search_log.csv` has zero populated rows; all 3 named pilot combinations are reported as blocking (`no corresponding row in templates/search_log.csv`). `logs/pilot_raw_file_checksums.csv` was written with 0 rows (header only) — no files existed to checksum. This is the genuine, un-fabricated Section-1 stop condition: **no real pilot files have been supplied to this toolkit yet.** See `reports/pilot_input_readiness_report.md` for the full issue list.

---

## 1. Auto-merge rule rewrite — only 3 rules may auto-merge

The prior round auto-merged on title+year OR title+author alone, which was too permissive. This round restricts auto-merging to exactly three rules; everything weaker is `possible_duplicate`-only.

| # | Test name | Expected result | Actual result | Status |
|---|---|---|---|---|
| 1 | **Title+year match, different author never auto-merges** (`tests/case10_title_year_diff_author/`) | 2 master records, 0 confirmed duplicates, 2nd flagged `possible_duplicate` (`title_year_match_author_missing_or_different`) | Exactly as expected (after fixing a bug — see §4.1) | PASS |
| 2 | **Title+author match, different year never auto-merges** (`tests/case11_title_author_diff_year/`) | 2 master records, 0 confirmed duplicates, 2nd flagged `possible_duplicate` (`title_author_match_year_missing_or_different`) | Exactly as expected | PASS |
| 3 | **Title+year+author exact match → confirmed duplicate** (`tests/case12_tya_confirmed/`) | 1 master, 1 confirmed duplicate, `duplicate_match_basis=title_year_first_author` | Exactly as expected | PASS |
| 4 | **Title+year+author match but conflicting DOI → possible duplicate, not merged** (`tests/case13_tya_doi_conflict/`) | 2 master records, 0 confirmed duplicates, 2nd flagged `conflicting_persistent_identifiers` | Exactly as expected | PASS |
| 14 | **Correction/protocol/preprint/conference never auto-merge with a primary record** (`tests/case18_version_types/`) | 5 distinct master records (primary, correction, protocol, preprint, conference), 0 confirmed duplicates | Exactly as expected — each correctly classified by `publication_version`; the correction and protocol variants were caught via fuzzy/no-match paths (title differs enough that they didn't reach rule 3 at all) rather than the version-conflict guard specifically, but the required invariant (never auto-merge a different version) held in every sub-case | PASS |

## 2. Identifier-conflict guard, reindexing, and chain-backfill

| # | Test name | Expected result | Actual result | Status |
|---|---|---|---|---|
| 5 | **Chain backfill via DOI** — record A (title/year/author, no DOI) → record B (same title/year/author, has DOI, merges via rule 3, backfills DOI onto master, master re-indexed) → record C (differently-worded title, same DOI as B, merges via rule 1) (`tests/case14_chain_doi_backfill/`) | 1 master record, `occurrence_count=3` | Exactly as expected | PASS |
| 6 | **Chain backfill via PMID** — same pattern with PMID instead of DOI (`tests/case15_chain_pmid_backfill/`) | 1 master record, `occurrence_count=3` | Exactly as expected | PASS |
| — | **DOI-match with differing titles logs a metadata-discrepancy note, still merges** (exercised by case01/case04's DOI-variant fixtures, which have slightly different titles per record) | Warning logged, merge proceeds | Confirmed in log output | PASS |
| — | **PMID-match with a missing DOI on one side backfills the DOI** (exercised by `tests/case04_three_db_aggregation/`) | DOI backfilled from the PubMed copy onto the master | `PMID (backfilled from pubmed dup): 66666666` and DOI present on master | PASS |

## 3. RIS PMID/accession fix and multi-DOI handling

| # | Test name | Expected result | Actual result | Status |
|---|---|---|---|---|
| 7 | **RIS `AN` (plain numeric) is never read as PMID** (`tests/case16_ris_an_not_pmid/`) — 4 sub-cases: plain numeric `AN`, explicit `PM` tag, WoS-style `AN` string, `AN` with a `PMID:` prefix | Only the `PM`-tagged and `PMID:`-prefixed values populate `PMID`; plain numeric/WoS-style `AN` values populate `wos_accession_number` instead | All 4 sub-cases exactly as expected | PASS |
| 8 | **Multiple identical DOI candidates (different notations) dedupe to one clean value** (`tests/case17_multidoi/`, record 1: bare DOI + `https://doi.org/...` form of the same DOI) | `DOI` populated with the single canonical value, `multiple_conflicting_dois=FALSE` | Exactly as expected | PASS |
| 9 | **Multiple distinct valid DOIs on one record produce a prominent warning, DOI left blank** (`tests/case17_multidoi/`, record 2: two different valid-pattern DOIs) | `DOI=""`, `multiple_conflicting_dois=TRUE`, both candidates in `doi_candidates`, warning in log and `parsing_quality_report.csv` | Exactly as expected | PASS |

## 4. Seed recall status rewrite

| # | Test name | Expected result | Actual result | Status |
|---|---|---|---|---|
| 10 | **Title-only match never enters `confirmed_recall_rate`** (`tests/case19_seed_recall_categories/`) | Title-only match reported as `POSSIBLE_RECALL*`, excluded from `confirmed_recalled` count | [48] Safford (title-only match against 2 synthetic candidates) correctly excluded from `confirmed_recalled` (stayed at 1, only the genuine title+year+author match for [41] Zuccato) | PASS |
| 11 | **Seed matching multiple master records is never defaulted to the first** (same fixture, [48] matches 2 distinct synthetic records sharing its exact title) | `POSSIBLE_RECALL_MULTIPLE_MATCHES`, both `matched_record_ids` listed, `manual_confirmation_required=TRUE` | `matched_record_ids: m002;m003` — both listed, not just one | PASS |

## 4.1 Bugs found and fixed during this round (via testing, not inspection alone)

1. **`database_module_summary.csv` double-counted merged-in duplicates.** The prior round's per-master `_db_module_pairs` aggregation, when combined with a separate pass over `confirmed_duplicates`, double-counted a record that both contributed to a master's aggregated provenance *and* had its own confirmed-duplicate row for the same (database, module) pair (caught by `tests/case04_three_db_aggregation/`'s integrity check reporting `PASS_WITH_WARNINGS` with a specific count mismatch). Fixed by deriving the summary directly from the *original input records* — each counted exactly once, by its own origin pair, as either "became/contributed to a master" or "was merged away" — which is also what makes the integrity check's cross-validation of this table hold by construction.
2. **`_new_master_record()` silently discarded possible-duplicate flags.** `add_possible_duplicate()` set `possible_duplicate_of_record_id`/`possible_version_relation`/`duplicate_match_basis` on a record, then called `_new_master_record()` to build its master-record view — but that function unconditionally reset those same four fields back to `""`, so every `possible_duplicate` appeared correctly flagged in `possible_duplicates.csv` but *unflagged* in `master_records.csv` (caught by `tests/case10_title_year_diff_author/`, where the flag was visibly missing from the master output on first run). Fixed by using `setdefault` for those fields instead of unconditional assignment, so a caller-set value is preserved rather than clobbered.
3. **`validate_search_inputs.py` broke against the updated `parse_csv_export()` signature.** This round's `deduplicate_records.py` changes added a `warnings` parameter to `parse_csv_export()` (needed for multi-DOI-candidate reporting); `validate_search_inputs.py` imports and calls that function directly and was not updated to match, which would have raised a `TypeError` the first time a real Scopus CSV export was readiness-checked. Caught by re-running the case07–09 regression suite after this round's parser changes, before reporting completion.

## 5. Prior round's coverage (2026-07-13, real-data-readiness hardening) — still valid, re-verified this round

Full detail in git history; summary: DOI/PMID canonicalization unit tests (11 cases), `--help`/safe-exit behavior for all 4 scripts, general 4-format smoke test (RIS/CSV/NBIB/BibTeX), multi-line RIS/NBIB title+abstract preservation, 3-database/3-module source aggregation, `validate_search_inputs.py`'s missing-file/count-mismatch/wrong-module-filename detection, and confirmation that all real data directories (`data/raw/`, `data/processed/`, `reports/`, `logs/`) remain empty except `.gitkeep`. All re-run against this round's updated scripts in §1–§4 above (the general smoke test, seed recall against real synthetic master data, and PRISMA counts were all re-executed end-to-end with the same expected results, confirming no regression — see the commit's raw test logs for the full re-run output).

## 6. Known limitations carried forward or newly identified

- **Fuzzy title matching (Jaccard token overlap ≥ 0.8, same year)** remains untuned against real-world data and is, as of this round, explicitly possible-duplicate-only (never auto-merges) — this is now stricter than the prior round by design, not a regression.
- **Version-conflict detection is heuristic** (title keywords + journal/source-name substrings) and will miss cases with no matching keyword (e.g., a correction whose title doesn't contain the word "correction") — as seen in test 14's "Correction to: ..." sub-case, which ended up correctly *unmerged* but via the fuzzy/no-match path rather than the version-conflict path specifically, since the title differed enough not to reach rule 3 at all. The safety property (never auto-merge) held regardless of which path caught it.
- **`manual_duplicate_review.csv` decisions are never auto-applied.** This is by design per instruction, but it means every `possible_duplicate` and `POSSIBLE_RECALL*` seed genuinely requires a human pass before the citation set can be considered final — this toolkit does not, and should not, attempt to close that loop automatically.
- **BibTeX parsing remains fallback/experimental**, unaffected by this round's RIS/NBIB hardening.
- **`identifier_conflict()` only compares DOI and PMID.** Per-database accession numbers (`wos_accession_number`, `scopus_eid`, `source_accession_id`) are captured and retained but not currently used as a conflict signal — two records with the same title/year/author and different WoS accession numbers, for instance, would still be evaluated only on DOI/PMID conflict. Not required by this round's instruction; noted for a possible future round.
- **The RIS PMID fix is deliberately conservative** and may miss a legitimate PMID in a non-standard RIS export that encodes it under a tag other than `PMID`/`PM` or without a `PMID:` prefix — this trades recall for avoiding the more serious accession-number misidentification problem, per instruction.

---

## Exact run order for real data import (updated this round)

0. **Optional pilot trial** (recommended for the very first real files received, e.g. before all 24 searches are done): see `README.md` §6c — `validate_search_inputs.py --mode pilot --expected-search ...` then `deduplicate_records.py --mode pilot --parse-only`. Stops automatically (non-zero exit / explanatory error) rather than proceeding on missing or unreviewed input, per Sections 1–3 of the pilot import workflow.
1. Place raw exports into `data/raw/{wos,scopus,pubmed}/` following the naming convention in `README.md` §3, and fill in every row of `templates/search_log.csv`.
2. Run `python3 scripts/validate_search_inputs.py` — do not proceed while the status is `NOT_READY`.
3. Run `python3 scripts/deduplicate_records.py` — **check `data/processed/deduplication_integrity_report.md` is `PASS` or `PASS_WITH_WARNINGS`, never proceed past a `FAIL`** (the script itself exits non-zero on `FAIL`). Also inspect `parsing_quality_report.csv` for zero-record or high-missing-title warnings, and check for any `multiple_conflicting_dois` records needing manual resolution.
4. Run `python3 scripts/check_seed_recall.py` — if `confirmed_recall_rate` is unsatisfactory or any seed is `NOT_RECALLED`, revise and re-run the corresponding module's search (back to step 1). Transfer every `possible_duplicates.csv` row and every `POSSIBLE_RECALL*` seed into `templates/manual_duplicate_review.csv` for human resolution — do not treat `provisional_recall_rate` as a real recall figure.
5. Perform title/abstract screening, then full-text screening (both manual steps).
6. Run `python3 scripts/generate_prisma_counts.py` against the completed screening files.
7. Populate `templates/data_extraction.csv` and `templates/chapter_claim_audit.csv` for every included, full-text-obtained record, then update `../WBE_Review_Citation_Verification_Table.md` and `../WBE_Review_Ch8_Evidence_Freeze_Audit.md` per `README.md` §10.
