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

## 2. Recommended export formats per database

| Database | Recommended export format | Rationale |
|---|---|---|
| Web of Science | `.ris` (Tagged/RIS) or Fast5000/plain-text export with full record | RIS preserves author lists, abstract, DOI, and WoS accession number cleanly for downstream parsing |
| Scopus | `.csv` (Scopus's own CSV export, "all available information") | Scopus's native CSV includes DOI, EID, and abstract in a stable column layout |
| PubMed | `.nbib` (PubMed's own citation export format) | NBIB preserves PMID, MeSH terms, and abstract in a structured, parseable format; `.ris` also acceptable if `.nbib` is unavailable in your interface |

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

## 6. How to run the deduplication script

```bash
cd systematic-review
python3 scripts/deduplicate_records.py --help
python3 scripts/deduplicate_records.py \
    --input-dir data/raw \
    --output-dir data/processed \
    --log-dir logs
```

The script reads every `.ris`, `.csv`, `.bib`, and `.nbib` file under `data/raw/{wos,scopus,pubmed}/`, normalizes them to a common schema, deduplicates by DOI → PMID → normalized title → title+year+first-author (in that priority order), and writes `master_records.csv`, `confirmed_duplicates.csv`, `possible_duplicates.csv`, `database_module_summary.csv`, and `deduplication_log.txt` into `data/processed/`. See Section 5 of `scripts/deduplicate_records.py`'s own `--help` output for full option documentation. The script refuses to run and exits with a clear message if `data/raw/` contains no real export files (it will not silently produce empty or synthetic-looking output framed as real).

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
├── templates/                  — empty CSV templates, ready to populate with real data
├── scripts/                    — Python scripts (deduplication, seed recall, PRISMA counts)
├── reports/                    — script-generated reports (seed recall, PRISMA counts)
└── logs/                       — script run logs
```

## What this toolkit is not

This toolkit does not itself search any database, does not fabricate hit counts, does not estimate PRISMA numbers, and does not mark any of the review's 51 existing references as full-text-verified. Every number this toolkit's scripts can produce depends entirely on real files placed into `data/raw/` by someone with actual database access. Until that happens, every report this toolkit generates will say so explicitly rather than presenting a plausible-looking placeholder as if it were real.
