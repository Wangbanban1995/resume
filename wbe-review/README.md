# WBE Review — Project Status

**Beyond Detection in Wastewater-Based Epidemiology: Sewer Processes, Signal Distortion, Normalization, and Epidemiological Inference**

## Current phase: evidence remediation (Chapters 1–8 frozen, Chapter 9 not started)

This project is a working-draft academic review of wastewater-based epidemiology (WBE), currently 8 chapters drafted. As of 2026-07-13, the project is **not** in a chapter-writing phase — it is in a systematic-review evidence-remediation phase, per instruction: converting Chapters 1–8 from a search-engine-summary-driven conceptual draft into a full-text-evidence-driven critical review. **Do not resume drafting Chapter 9, and do not expand Chapters 1–8's own prose, until this phase is explicitly closed out by the user.**

### What exists and is considered stable

- `WBE_Review_Ch1-8.md` / `.docx` — the 8-chapter draft text
- `WBE_Review_References.md` / `.docx` — 51 references ([1]–[50], plus [32b])
- `WBE_Review_Citation_Verification_Table.md` / `.docx` — per-reference evidence-type and verification-status table
- `WBE_Review_Pending_Verification_List.md` / `.docx` — consolidated list of every unverified number/claim
- `WBE_Review_Ch7_Model_Audit_Table.md` / `.docx`, `WBE_Review_Ch8_Parameter_Distribution_Table.md` / `.docx` — standalone table extracts
- `WBE_Review_Ch8_Uncertainty_Audit.md` / `.docx` — Chapter 8 sourcing/evidence-balance audit
- `WBE_Review_Ch8_Evidence_Freeze_Audit.md` / `.docx` — the authoritative statement of the review's current evidentiary state (see below)
- `WBE_Fig1_Normalization_Decision_Tree.png`, `WBE_Fig2_Uncertainty_Chain.png`, `WBE_Fig3_Uncertainty_Budget_Network.png` — the review's three original figures

### The single most important fact about this project right now

**0 of 51 references have been read in full text. 51 of 51 are supported only by search-engine-summarized abstracts or metadata.** No Web of Science, Scopus, or PubMed search has been executed. This is not a stale figure — it is retested and reconfirmed every round this status changes, and it is documented, with the specific tested reason, in `WBE_Review_Ch8_Evidence_Freeze_Audit.md`.

### `systematic-review/` — the remediation toolkit

`systematic-review/` contains a complete, tested execution toolkit — search strategy, directory structure, CSV templates, and Python scripts — for someone with institutional Web of Science/Scopus/PubMed access to run the review's formal search strategy and feed the results back into this review through a reproducible pipeline (deduplication → screening → PRISMA counting → claim/table-cell audit). See `systematic-review/README.md` for the step-by-step execution guide, and `WBE_Review_Systematic_Search_Strategy.md` (one directory up) for the actual search strings (one core search + seven complementary module searches, eight searches total, across all three databases).

**The toolkit is built and tested (against clearly-labeled synthetic data only — see `systematic-review/tests/TEST_RESULTS.md`). It has not been run against any real search.**

### What happens next

This project's next state change is triggered by **the user (or someone with institutional access) supplying real Web of Science, Scopus, and PubMed export files** into `systematic-review/data/raw/{wos,scopus,pubmed}/`. Until that happens:

- Chapters 1–8 remain frozen (no further prose expansion)
- Chapter 9 does not begin
- No hypothetical PRISMA numbers, hit counts, or full-text-verification claims are generated
- `WBE_Review_Ch8_Evidence_Freeze_Audit.md` continues to report the true, current state

### Files awaited from the user / a database-access holder

- Raw exports (`.ris`/`.csv`/`.nbib`) for the core search and all 7 complementary modules, across Web of Science, Scopus, and PubMed (24 files if all are run; see `systematic-review/README.md` §1–§3 for naming/placement)
- The completed `systematic-review/templates/search_log.csv` (one row per search actually run)
- Title/abstract and full-text screening decisions once screening is performed
- Any full-text PDFs the user can supply directly for specific high-priority references, even before a full database search is completed — this review can audit any paper supplied directly regardless of the database-access question
