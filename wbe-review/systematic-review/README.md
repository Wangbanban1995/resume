# Systematic Review Execution Toolkit — WBE Review

**Status: execution toolkit only. No database search has been run. No screening decision has been made. No PRISMA number in this toolkit is real.** This directory exists so that a person with Web of Science, Scopus, and PubMed access can execute the search strategy defined in `../WBE_Review_Systematic_Search_Strategy.md` and feed the results through a reproducible, auditable pipeline back into the review. Nothing in this directory should be read as reporting an actual search result unless it was produced by running the scripts here against real exported data.

---

## 1. How to execute the eight searches

The search strategy (one core search + seven complementary modules, eight searches total) is fully specified in `../WBE_Review_Systematic_Search_Strategy.md`, Sections 2–9. For each of the three databases (Web of Science, Scopus, PubMed):

1. Log into the database with institutional access.
2. Copy the exact query string for the search you are running (core, or Module 2 through Module 8) from the corresponding section of the strategy document. Do not paraphrase or retype it — copy/paste to avoid transcription errors.
3. Apply the date-range and language settings per Section 11 of the strategy document (run the no-date-restriction sensitivity pass first, as instructed there, before applying the final date floor).
4. Run the search and record the **raw hit count** immediately, before any de-duplication the database interface itself might apply.
5. Export the full result set (see Section 2 below for format/naming).
6. Fill in one row of `templates/search_log.csv` for this search **before moving to the next one** — the log is your record of what was actually run, since database interfaces can silently normalize or truncate a pasted query string.
7. Repeat for all 8 searches × 3 databases = up to 24 export operations (fewer if a given module is judged not applicable to a particular database's syntax, which should still be logged as such).

## 2. Official production export format per database

These are the **fixed, required** formats for real search execution — not a preference among interchangeable options:

| Database | Required export format | Rationale |
|---|---|---|
| Web of Science | **RIS** (`.ris`, Tagged/RIS export with full record) | RIS preserves author lists, multi-line abstracts, DOI, and WoS accession number cleanly for downstream parsing; this toolkit's RIS parser is hardened against continuation lines, multiple DO fields, and files missing a terminal ER tag |
| Scopus | **CSV** (`.csv`, Scopus's own "all available information" export) | Scopus's native CSV includes DOI, EID, and abstract in a stable column layout that this toolkit's CSV parser reads directly |
| PubMed | **NBIB** (`.nbib`, PubMed's own citation export format) | NBIB preserves PMID, MeSH terms, and multi-paragraph abstracts in a structured, parseable format; this toolkit's NBIB parser is hardened against continuation lines and DOI recovery from AID/LID fields |

**BibTeX (`.bib`) is supported only as a fallback/experimental parser, not the preferred production import format.** It exists for occasional one-off records exported from a reference manager, not as a substitute for RIS/CSV/NBIB when running the actual 8×3 search plan. The BibTeX parser in `scripts/deduplicate_records.py` uses a simple regex-based reader with no external dependency; it has known gaps (nested braces, multi-line unquoted field values, and unusual entry syntax are not guaranteed to parse correctly), and every BibTeX file processed is logged with an explicit warning identifying it as fallback/experimental output requiring manual verification. Do not treat successfully-parsed BibTeX records as having the same reliability as RIS/CSV/NBIB records without spot-checking them against the source.

## 3. File naming convention

```
<database>_<search_id>_<short_topic>_<YYYYMMDD>.<ext>
```

Examples (all illustrative — do not create these until a real search has been run):

```
wos_core_YYYYMMDD.ris
wos_module02_sewer_YYYYMMDD.ris
wos_module03_rainfall_YYYYMMDD.ris
wos_module04_sampling_YYYYMMDD.ris
wos_module05_normalization_YYYYMMDD.ris
wos_module06_chemical_YYYYMMDD.ris
wos_module07_pathogen_YYYYMMDD.ris
wos_module08_uncertainty_YYYYMMDD.ris
scopus_core_YYYYMMDD.csv
scopus_module02_sewer_YYYYMMDD.csv
scopus_module05_normalization_YYYYMMDD.csv
... (same module numbering for scopus_* and pubmed_*)
pubmed_core_YYYYMMDD.nbib
pubmed_module07_pathogen_YYYYMMDD.nbib
```

`database` ∈ {`wos`, `scopus`, `pubmed`}. `search_id` ∈ {`core`, `module02`, `module03`, `module04`, `module05`, `module06`, `module07`, `module08`} — module numbers match the strategy document's own section numbering (Module 2 = sewer transport, ... Module 8 = uncertainty/identifiability), so a filename's module number can always be traced back to its exact query string. `YYYYMMDD` is the date the search was actually run, not the date the file was saved or renamed later.

## 4. Where exported files go

Place the raw, unmodified export exactly as downloaded into:

```
data/raw/wos/       — all wos_*.ris files
data/raw/scopus/    — all scopus_*.csv files
data/raw/pubmed/    — all pubmed_*.nbib files
```

**Never edit a raw export file in place.** If a file needs correction (e.g., re-exporting because a field was missing), save the corrected file as a new export with a new date stamp and note the reason in `templates/search_log.csv`'s `notes` field for that row. `data/interim/` holds intermediate working files the scripts produce (e.g., format-normalized copies before merging); `data/processed/` holds the final merged/deduplicated outputs described in Section 6 below.

## 5. Fields that must be preserved in every export

At minimum, every exported record must retain: title, abstract, full author list, publication year, journal/source name, DOI (if assigned), PMID (PubMed records), and the database's own internal accession/record ID. Do not use an export option that strips the abstract or author list to save space — both are required for title/abstract screening (`templates/title_abstract_screening.csv`) and cannot be reconstructed later without re-fetching the record.

## 6. How to run the readiness check, then the deduplication script

**Run `validate_search_inputs.py` first, every time**, before deduplication:

```bash
cd systematic-review
python3 scripts/validate_search_inputs.py --help
python3 scripts/validate_search_inputs.py \
    --search-log templates/search_log.csv \
    --raw-dir data/raw \
    --output-dir reports
```

This checks that all 8×3=24 searches are logged, filenames follow the naming convention, every logged export file actually exists and parses to roughly the count logged in `search_log.csv`, zero-hit searches have an explanatory note, and no unreferenced or duplicate files are sitting in `data/raw/`. It writes `reports/input_readiness_report.md`/`.csv` with a status of `READY`, `READY_WITH_WARNINGS`, or `NOT_READY`. **Do not proceed to deduplication while the status is `NOT_READY`** — resolve every blocking issue first, since a `NOT_READY` state usually means the deduplication counts that follow would be built on an incomplete or inconsistent input set.

Then run the deduplication script:

```bash
python3 scripts/deduplicate_records.py --help
python3 scripts/deduplicate_records.py \
    --input-dir data/raw \
    --output-dir data/processed \
    --log-dir logs
```

The script reads every `.ris`, `.csv`, `.nbib` (and, as a fallback/experimental parser only, `.bib`) file under `data/raw/{wos,scopus,pubmed}/`, normalizes them to a common schema, and applies **only three auto-merge rules** — everything else is left for human review, never silently merged:

1. **Canonical-DOI exact match → confirmed duplicate, always merged.** DOI strings are normalized for case, whitespace, `doi:`/URL prefixes, URL-encoding, trailing punctuation, and a trailing `[doi]` tag before comparison. If the merged pair's titles differ, a metadata-discrepancy note is logged, but the merge still proceeds — DOI is authoritative.
2. **Canonical-PMID exact match → confirmed duplicate, always merged**, on the same basis. A value is only ever treated as a PMID if it comes from an explicit `PMID`/`PM` tag (RIS) or a `PMID:`-prefixed value — a plain numeric RIS `AN` field (a database accession number, not a PMID) is never misread as one; see `wos_accession_number`/`scopus_eid`/`source_accession_id` below.
3. **Normalized title + publication year + first-author surname exact match → confirmed duplicate, but only if two further checks both pass:** (a) **no identifier conflict** — if both records carry a non-empty DOI or PMID and those values differ, the match is downgraded to `possible_duplicate` with `possible_version_relation=conflicting_persistent_identifiers`, never merged; (b) **no version conflict** — if one record's title/journal suggests a correction/erratum, protocol, preprint, or conference abstract while the other looks like a primary/journal record, the match is downgraded to `possible_duplicate` (e.g. `primary_or_unclassified_vs_preprint`), never merged.

**Everything weaker than rule 3 is possible-duplicate-only and is never auto-merged**, each producing its own separate master record flagged against its closest candidate: title+year alone (author missing or different), title+first-author alone (year missing or different), title alone with insufficient other metadata, and finally a fuzzy title-overlap fallback (Jaccard token overlap ≥ 0.8, same year). A title that exactly matches an existing record but whose year and first author **both** differ is always `possible_duplicate`, never merged, regardless of how it was found. All of these route to `templates/manual_duplicate_review.csv` for a human decision — **no script in this toolkit ever automatically applies a decision from that file**; doing so would require a separate, explicit, auditable "apply" step that does not currently exist.

A confirmed duplicate is merged into its master record's provenance rather than discarded: `master_records.csv` gains `database_sources`, `search_modules`, `source_files`, `duplicate_record_ids`, and `occurrence_count` columns that fully aggregate every database and module a given paper was actually found under, plus empty-field backfill (if the first-seen copy is missing an abstract, DOI, etc. that a later duplicate has, the master record is filled in). **After every backfill, the master record is re-indexed** so a later, still-unprocessed record can chain-match it via a newly-available DOI/PMID/title/author — e.g., record A (no DOI) merges with record B (same title/year/author, has a DOI) via rule 3, backfilling the DOI onto the shared master; record C (a differently-worded title, but the same DOI as B) then matches that master via rule 1, arriving at one master record with `occurrence_count=3`.

Multiple DOI-like values on a single record (multiple RIS `DO` tags, or multiple NBIB `AID`/`LID` `[doi]` values) are canonicalized, deduplicated, and checked against the standard DOI pattern (`^10\.\d{4,9}/\S+$`); if two or more **distinct, valid** DOIs remain, the record's `DOI` field is left blank (never silently guessed), `multiple_conflicting_dois=TRUE`, and all candidates are retained in `doi_candidates` for manual review, with a prominent warning in both the log and `parsing_quality_report.csv`.

Outputs written to `data/processed/`: `master_records.csv`, `confirmed_duplicates.csv`, `possible_duplicates.csv`, `database_module_summary.csv` (derived from the *original input records*, each counted exactly once, to avoid double-counting a record that both contributed to a master's aggregated provenance and has its own confirmed-duplicate row), `deduplication_log.txt`, `parsing_quality_report.csv`, and **`deduplication_integrity_report.md`/`.csv`** — an automatic post-run consistency check (input records = master + confirmed duplicates; every input record accounted for exactly once; no duplicate points to a nonexistent or chained master; each master's `occurrence_count` matches its aggregated sources; the database/module summary reconciles with the original input) that reports `PASS`, `PASS_WITH_WARNINGS`, or `FAIL`. **A `FAIL` status makes the script exit with a non-zero status code, and that output must not be used for screening or PRISMA counting until resolved.** See `scripts/deduplicate_records.py --help` for full option documentation. The script refuses to run and exits with a clear message if `data/raw/` contains no real export files.

## 6b. How to check seed recall

After deduplication, confirm the search actually recalled this review's own 44 already-known references before moving on to screening:

```bash
python3 scripts/check_seed_recall.py --help
python3 scripts/check_seed_recall.py \
    --seed-csv templates/seed_studies.csv \
    --master-csv data/processed/master_records.csv \
    --output-dir reports
```

Four status categories, and **two recall rates that must not be conflated**:

- **`RECALLED_CONFIRMED`** — matched by canonical DOI, canonical PMID, or normalized title+year+first-author, **and** resolved to exactly one master record. If a "confirmed-tier" basis still resolves to more than one distinct master record (e.g. a genuine DOI collision), it is *not* auto-resolved to the first — it is downgraded to `POSSIBLE_RECALL_MULTIPLE_MATCHES` instead.
- **`POSSIBLE_RECALL`** (including `POSSIBLE_RECALL_MULTIPLE_MATCHES`) — matched by title alone, by a fuzzy title match, or matched to more than one candidate record. **Never counted as confirmed** — every match is listed in full (`matched_record_ids`, `matched_titles`), never silently narrowed to "the first one."
- **`NOT_RECALLED`** — no match on any basis.
- **`UNTESTABLE`** — the seed itself has neither a DOI/PMID nor a usable title (in practice, none of the 44 real seeds fall into this category).

Two rates are reported in `reports/seed_recall_summary.md`, and only one of them may be quoted as "the search recalled this literature":

- **`confirmed_recall_rate = RECALLED_CONFIRMED / testable seeds`** — the only rate safe to cite without further manual work.
- `provisional_recall_rate = (RECALLED_CONFIRMED + POSSIBLE_RECALL) / testable seeds` — includes unconfirmed candidates; useful for gauging how much manual-review work remains, not as a recall figure.

Outputs: `reports/seed_recall_report.csv` (per-seed detail, including `match_basis`, `matched_record_ids`, `matched_titles`, `matched_database_sources`, `matched_search_modules`, `manual_confirmation_required`) and `reports/seed_recall_summary.md`. Every `POSSIBLE_RECALL*` seed should be transferred into `templates/manual_duplicate_review.csv` for a human decision. Per Section 13 of the search strategy document, any seed marked `NOT_RECALLED` means the corresponding module's search string should be revised and re-tested before treating the search as final.

## 7. How to generate the screening tables

`templates/title_abstract_screening.csv` and `templates/full_text_screening.csv` are empty templates with the required columns. After deduplication, copy `data/processed/master_records.csv`'s `record_id`, `title`, `abstract`, `year`, `journal`, and `DOI` columns into a fresh copy of `templates/title_abstract_screening.csv` (e.g., save as `data/processed/title_abstract_screening_YYYYMMDD.csv`) for reviewers to fill in. Do this with a spreadsheet tool or a short script — no script for this specific step is provided in this toolkit because the "how many reviewers, in what tool" decision is a human process choice this toolkit does not make for you.

## 8. How to fill in screening decisions

Both screening templates use a controlled decision vocabulary (`include` / `exclude` / `uncertain`) and a controlled exclusion-reason vocabulary (see the templates themselves and Sections 6–7 of the outer instruction this toolkit implements). Two independent reviewers fill `reviewer_1_decision` and `reviewer_2_decision` per record; if they disagree, `conflict` = `TRUE` and `final_decision` is resolved by discussion or a third reviewer, then recorded. Do not leave `final_decision` blank for any record marked `conflict = TRUE`.

## 9. How to generate PRISMA numbers

```bash
python3 scripts/generate_prisma_counts.py --help
python3 scripts/generate_prisma_counts.py \
    --search-log templates/search_log.csv \
    --dedup-dir data/processed \
    --title-abstract-screening data/processed/title_abstract_screening_YYYYMMDD.csv \
    --full-text-screening data/processed/full_text_screening_YYYYMMDD.csv \
    --output-dir reports
```

This computes every PRISMA flow-diagram number (identified, duplicates removed, screened, excluded, sought, not retrieved, assessed, excluded-by-reason, included) directly from the files above and writes `reports/prisma_counts.json` and `reports/prisma_counts.md`. If any required input file is missing or contains no real records, the script writes `STATUS: NOT EXECUTED — awaiting database exports and screening decisions.` instead of a number — it will not estimate, interpolate, or use placeholder counts.

## 10. How to update the review's citation verification table and Evidence Freeze Audit

Once `full_text_screening.csv` records real `full_text_obtained = TRUE` rows with `final_decision = include`:

1. For each included record already cited in the review (cross-reference by DOI/PMID against `../WBE_Review_Citation_Verification_Table.md`), fill in a row of `templates/data_extraction.csv` and `templates/chapter_claim_audit.csv` documenting exactly what page/table/figure supports which claim.
2. Update the corresponding row's "Claim status" column in `../WBE_Review_Citation_Verification_Table.md` from "pending full-text verification" to a specific verified status, citing the page/table/figure recorded in step 1.
3. Update `../WBE_Review_Ch8_Evidence_Freeze_Audit.md`'s full-text-read count — it currently reports 0/51 truthfully; increment it only by the number of records for which `full_text_screening.csv` shows `full_text_obtained = TRUE` AND a corresponding `data_extraction.csv` row exists with populated `supporting_page`/`supporting_table`/`supporting_figure` fields. Do not increment the count based on title/abstract screening alone — only genuine full-text extraction counts.
4. For any of the review's 51 existing references that the formal search fails to recall or that full-text access fails to obtain, record this explicitly in `templates/seed_studies.csv`'s `failure_reason` column rather than silently dropping the reference.

---

## Directory map

```
systematic-review/
├── README.md                  — this file
├── data/
│   ├── raw/                   — untouched database exports, organized by database
│   │   ├── wos/
│   │   ├── scopus/
│   │   └── pubmed/
│   ├── interim/                — intermediate working files produced by scripts
│   └── processed/              — master_records.csv, confirmed/possible_duplicates.csv,
│                                 parsing_quality_report.csv, and
│                                 deduplication_integrity_report.md/.csv
├── templates/                  — CSV templates (seed_studies.csv pre-populated with the
│                                 review's 44 real seeds; manual_duplicate_review.csv for
│                                 human resolution of every possible_duplicate; all others
│                                 header-only) plus CONTROLLED_VOCABULARIES.md
├── scripts/                    — validate_search_inputs.py, deduplicate_records.py,
│                                 check_seed_recall.py, generate_prisma_counts.py
├── reports/                    — script-generated reports (readiness, seed recall, PRISMA)
├── logs/                       — script run logs
└── tests/                      — synthetic test fixtures and TEST_RESULTS.md; never
                                  real data, kept fully separate from data/, reports/, logs/
```

Run order, once real database access is available: `validate_search_inputs.py` (must not be `NOT_READY`) → `deduplicate_records.py` (check `deduplication_integrity_report.md` is `PASS`/`PASS_WITH_WARNINGS`, never proceed past a `FAIL`) → `check_seed_recall.py` → resolve every `possible_duplicate`/`POSSIBLE_RECALL*` entry in `templates/manual_duplicate_review.csv` (manual step) → title/abstract and full-text screening (manual steps) → `generate_prisma_counts.py`.

## What this toolkit is not

This toolkit does not itself search any database, does not fabricate hit counts, does not estimate PRISMA numbers, and does not mark any of the review's 51 existing references as full-text-verified. Every number this toolkit's scripts can produce depends entirely on real files placed into `data/raw/` by someone with actual database access. Until that happens, every report this toolkit generates will say so explicitly rather than presenting a plausible-looking placeholder as if it were real.
