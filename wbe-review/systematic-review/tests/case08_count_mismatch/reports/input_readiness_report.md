# Input Readiness Report

Generated: 2026-07-13T15:02:38.855722

## STATUS: NOT_READY

- Search log rows populated: 1 of expected 24 (8 searches x 3 databases)
- Missing (database, search_id) combinations: 23
- Raw export files found under tests/case08_count_mismatch/data/raw: 1
- Blocking issues: 23
- Warnings: 1

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
- **[WARNING]** wos_core_case08_20260713.ris: search log says exported_records=5, but the file actually parses to 2 record(s).
