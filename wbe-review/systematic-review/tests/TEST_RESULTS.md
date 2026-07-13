# Test Results — Systematic Review Execution Toolkit

**Latest round: 2026-07-13, final deduplication safety patch.** This document supersedes the previous round's report; §1–§4 below are this round's new/re-verified results, §5 briefly retains the prior round's still-valid coverage for continuity. All fixtures under `tests/` are explicitly synthetic (fabricated for script-testing purposes only, clearly labeled `SYNTHETIC TEST RECORD`/`Casetest`/etc.) and must never be treated as, or quoted as, a real search result. The only real data used anywhere in this test suite is the 44-row `templates/seed_studies.csv` metadata (title/year/author/DOI/PMID), used strictly to test whether the *matching logic* recognizes a real seed against synthetic master records — never to claim a real recall rate.

**Status after this round: the toolkit is ready for its first real database import**, subject to the known limitations in §6.

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

1. Place raw exports into `data/raw/{wos,scopus,pubmed}/` following the naming convention in `README.md` §3, and fill in every row of `templates/search_log.csv`.
2. Run `python3 scripts/validate_search_inputs.py` — do not proceed while the status is `NOT_READY`.
3. Run `python3 scripts/deduplicate_records.py` — **check `data/processed/deduplication_integrity_report.md` is `PASS` or `PASS_WITH_WARNINGS`, never proceed past a `FAIL`** (the script itself exits non-zero on `FAIL`). Also inspect `parsing_quality_report.csv` for zero-record or high-missing-title warnings, and check for any `multiple_conflicting_dois` records needing manual resolution.
4. Run `python3 scripts/check_seed_recall.py` — if `confirmed_recall_rate` is unsatisfactory or any seed is `NOT_RECALLED`, revise and re-run the corresponding module's search (back to step 1). Transfer every `possible_duplicates.csv` row and every `POSSIBLE_RECALL*` seed into `templates/manual_duplicate_review.csv` for human resolution — do not treat `provisional_recall_rate` as a real recall figure.
5. Perform title/abstract screening, then full-text screening (both manual steps).
6. Run `python3 scripts/generate_prisma_counts.py` against the completed screening files.
7. Populate `templates/data_extraction.csv` and `templates/chapter_claim_audit.csv` for every included, full-text-obtained record, then update `../WBE_Review_Citation_Verification_Table.md` and `../WBE_Review_Ch8_Evidence_Freeze_Audit.md` per `README.md` §10.
