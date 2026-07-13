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

The script reads every `.ris`, `.csv`, `.nbib` (and, as a fallback/experimental parser only, `.bib`) file under `data/raw/{wos,scopus,pubmed}/`, normalizes them to a common schema, and deduplicates in this priority order:

1. Canonical-DOI exact match (DOI strings are normalized for case, whitespace, `doi:`/URL prefixes, URL-encoding, trailing punctuation, and a trailing `[doi]` tag before comparison)
2. Canonical-PMID exact match (a value is only treated as a PMID if, after stripping an optional `PMID:` prefix, it is purely numeric — a WoS accession number like `WOS:000123456789` is never misread as a PMID)
3. Normalized title + publication year
4. Normalized title + first-author surname
5. Normalized title + publication year + first-author surname

Matches found only via rules 3–5 (title-based, not DOI/PMID) are additionally screened for a likely **different-version pair** — a correction/erratum, a protocol vs. a results paper, a conference abstract vs. the eventual journal article, or a preprint vs. its published version — using title and journal/source-name heuristics. A detected version conflict downgrades what would otherwise be an automatic merge to a `possible_duplicate` entry instead, with `publication_version` and `possible_version_relation` recorded and `manual_duplicate_decision` left blank for a human reviewer to resolve — **the script never auto-decides which version to keep.** A record whose title exactly matches an existing record but whose year and first author **both** differ is, per the same rule, always treated as a `possible_duplicate`, never auto-merged.

A record confirmed as a duplicate is merged into its master record's provenance rather than discarded: `master_records.csv` gains `database_sources`, `search_modules`, `source_files`, `duplicate_record_ids`, and `occurrence_count` columns that fully aggregate every database and module a given paper was actually found under (a paper retrieved by WoS/core, Scopus/module05, and PubMed/module07 shows all three, not just its first-seen source), plus empty-field backfill (if the first-seen copy is missing an abstract, DOI, etc. that a later duplicate has, the master record is filled in rather than left blank).

Outputs written to `data/processed/`: `master_records.csv`, `confirmed_duplicates.csv`, `possible_duplicates.csv`, `database_module_summary.csv`, `deduplication_log.txt`, and `parsing_quality_report.csv` (per-source-file parse statistics — records parsed, missing-field counts, and prominent warnings for a file parsing to zero records, more than 5% of records missing a title, or an unrecognized database/module in the filename/directory). See `scripts/deduplicate_records.py --help` for full option documentation. The script refuses to run and exits with a clear message if `data/raw/` contains no real export files (it will not silently produce empty or synthetic-looking output framed as real).

## 6b. How to check seed recall

After deduplication, confirm the search actually recalled this review's own 44 already-known references before moving on to screening:

```bash
python3 scripts/check_seed_recall.py --help
python3 scripts/check_seed_recall.py \
    --seed-csv templates/seed_studies.csv \
    --master-csv data/processed/master_records.csv \
    --output-dir reports
```

Matching priority: (1) canonical DOI, (2) canonical PMID, (3) normalized title + year + first author, (4) normalized title alone — a title-only match is still reported as `RECALLED` but with `manual_confirmation_required=TRUE`, since a shared title alone is not sufficient to auto-confirm two records are the same paper. A seed is marked `UNTESTABLE` only when it has neither a DOI/PMID nor a usable title recorded in `seed_studies.csv` (in practice, none of the 44 real seeds fall into this category — all have titles). Outputs: `reports/seed_recall_report.csv` (per-seed detail, including `match_basis`, `matched_record_id`, `matched_title`, `matched_database_sources`, `matched_search_modules`) and `reports/seed_recall_summary.md`. Per Section 13 of the search strategy document, any seed marked `NOT_RECALLED` means the corresponding module's search string should be revised and re-tested before treating the search as final.

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
│   └── processed/              — final merged/deduplicated/screened outputs
├── templates/                  — CSV templates (seed_studies.csv pre-populated with the
│                                 review's 44 real seeds; all others header-only)
├── scripts/                    — validate_search_inputs.py, deduplicate_records.py,
│                                 check_seed_recall.py, generate_prisma_counts.py
├── reports/                    — script-generated reports (readiness, seed recall, PRISMA)
├── logs/                       — script run logs
└── tests/                      — synthetic test fixtures and TEST_RESULTS.md; never
                                  real data, kept fully separate from data/, reports/, logs/
```

Run order, once real database access is available: `validate_search_inputs.py` → `deduplicate_records.py` → `check_seed_recall.py` → (screening, a manual step) → `generate_prisma_counts.py`.

## What this toolkit is not

This toolkit does not itself search any database, does not fabricate hit counts, does not estimate PRISMA numbers, and does not mark any of the review's 51 existing references as full-text-verified. Every number this toolkit's scripts can produce depends entirely on real files placed into `data/raw/` by someone with actual database access. Until that happens, every report this toolkit generates will say so explicitly rather than presenting a plausible-looking placeholder as if it were real.
