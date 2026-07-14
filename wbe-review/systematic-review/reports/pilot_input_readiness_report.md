# Pilot Input Readiness Report

Generated: 2026-07-14T13:39:35.301378

## STATUS: PILOT_NOT_READY
## PRODUCTION STATUS (informational only, not blocking this pilot): PRODUCTION_NOT_READY

- Pilot combinations checked: pubmed_core, scopus_module05, wos_module02
- Pilot combinations missing from templates/search_log.csv: 3
- Search log rows populated (all): 0 of expected 24 (8 searches x 3 databases)
- Missing (database, search_id) combinations (full 24-search plan): 24
- Raw export files found under data/raw: 0
- Blocking issues (pilot scope): 4
- Warnings: 0

**One or more of the 3 named pilot files/search-log rows is missing, unreadable, or inconsistent. Do not proceed past Section 1 of the pilot workflow until this is resolved — see Issues below.**

**This is a partial, 3-of-24-search pilot run. It never establishes PRODUCTION_READY status and must not be used to justify skipping the remaining 21 searches.**

## Issues

- **[BLOCKING]** templates/search_log.csv has no populated rows (database + search_id). No real search has been logged yet.
- **[INFO]** (database=wos, search_id=core) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module02) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module03) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module04) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module05) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module06) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module07) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=wos, search_id=module08) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=core) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module02) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module03) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module04) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module05) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module06) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module07) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=scopus, search_id=module08) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=core) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module02) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module03) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module04) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module05) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module06) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module07) not in search log — not part of this pilot run, not blocking.
- **[INFO]** (database=pubmed, search_id=module08) not in search log — not part of this pilot run, not blocking.
- **[BLOCKING]** Pilot combination (database=pubmed, search_id=core) has no corresponding row in templates/search_log.csv.
- **[BLOCKING]** Pilot combination (database=scopus, search_id=module05) has no corresponding row in templates/search_log.csv.
- **[BLOCKING]** Pilot combination (database=wos, search_id=module02) has no corresponding row in templates/search_log.csv.
