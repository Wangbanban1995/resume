# Input Readiness Report

Generated: 2026-07-13T15:29:53.179998

## STATUS: NOT_READY

- Search log rows populated: 1 of expected 24 (8 searches x 3 databases)
- Missing (database, search_id) combinations: 23
- Raw export files found under tests/case07_missing_files/data/raw: 0
- Blocking issues: 24
- Warnings: 0

**Real search execution and/or export collection is incomplete. Do not proceed to deduplicate_records.py / generate_prisma_counts.py expecting real numbers until this is resolved.**

## Issues

- **[BLOCKING]** No search log row for (database=wos, search_id=module02) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module03) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module04) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module05) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module06) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module07) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=wos, search_id=module08) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=core) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module02) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module03) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module04) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module05) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module06) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module07) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=scopus, search_id=module08) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=core) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module02) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module03) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module04) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module05) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module06) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module07) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** No search log row for (database=pubmed, search_id=module08) — the full 8x3=24-search plan is not yet complete.
- **[BLOCKING]** (wos, core): referenced export file 'wos_core_case07_20260713.ris' was not found under tests/case07_missing_files/data/raw.
