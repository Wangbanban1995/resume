# WBE Review — Project Status

**Beyond Detection in Wastewater-Based Epidemiology: Sewer Processes, Signal Distortion, Normalization, and Epidemiological Inference**

## Current phase: conceptual chapter drafting continues (Chapters 1–10 drafted), formal evidence remediation still pending

This project is a working-draft academic review of wastewater-based epidemiology (WBE). **Status as of 2026-07-18: Chapters 1–10 are drafted as a conceptual working draft; Chapters 11–12 remain undrafted.** An earlier phase of this project (2026-07-13) paused chapter drafting for a systematic-review evidence-remediation effort; the user has since explicitly resumed chapter drafting, on the explicit condition that every chapter continues to carry this review's standing evidentiary discipline: web-search-derived sources only, no full-text reads, every specific number hedged as pending full-text verification or omitted where not corroborated, and formal PRISMA numbers never generated. **Do not read this README's earlier "frozen" language as still in force — it described a phase that ended when Chapter 9 drafting was authorized.**

### What exists and is considered stable

- `WBE_Review_Ch1-10.md` / `.docx` — the 10-chapter draft text (renamed this round from `WBE_Review_Ch1-9.md`, and before that `WBE_Review_Ch1-8.md` — see `WBE_Review_Rename_Crossref_Log.md`)
- `WBE_Review_References.md` / `.docx` — 68 reference numbers issued ([1]–[67], plus [32b]); 67 active/citable (one, [56], withdrawn — see the Evidence Freeze Audit)
- `WBE_Review_Citation_Verification_Table.md` / `.docx` — per-reference evidence-type and verification-status table
- `WBE_Review_Pending_Verification_List.md` / `.docx` — consolidated list of every unverified number/claim
- `WBE_Review_Ch7_Model_Audit_Table.md` / `.docx`, `WBE_Review_Ch8_Parameter_Distribution_Table.md` / `.docx` — standalone table extracts
- `WBE_Review_Ch8_Uncertainty_Audit.md` / `.docx` — Chapter 8 sourcing/evidence-balance audit
- `WBE_Review_Ch9_Claim_Audit.md` / `.docx` — paragraph-level claim-support audit specific to Chapter 9
- `WBE_Review_Table7_Evidence_Audit.md` / `.docx` — cell-by-cell audit of Chapter 9's Table 7
- `WBE_Review_Ch10_Evidence_Note.md` / `.docx` — evidence-base summary specific to Chapter 10
- `WBE_Review_Ch8_Evidence_Freeze_Audit.md` / `.docx` — the authoritative statement of the review's current evidentiary state, recomputed each round a chapter is added (see below)
- `WBE_Review_Rename_Crossref_Log.md` — file-rename and cross-reference verification log
- `WBE_Fig1_Normalization_Decision_Tree.png`, `WBE_Fig2_Uncertainty_Chain.png`, `WBE_Fig3_Uncertainty_Budget_Network.png` — the review's three original figures (no new figure added for Chapter 10 — see the Ch10 Evidence Note for why)

### The single most important fact about this project right now

**0 of 67 active references have been read in full text. 67 of 67 are supported only by search-engine-summarized abstracts or metadata.** No Web of Science, Scopus, or PubMed search has been executed. This denominator changes every time a chapter adds references (51 through Ch8, 59 through Ch9, 67 as of Ch10) — the fact that stays constant is the numerator: 0. It is retested and reconfirmed every round this status changes, and it is documented, with the specific tested reason, in `WBE_Review_Ch8_Evidence_Freeze_Audit.md`. **Never quote a prior round's denominator (51 or 59) as current.**

### `systematic-review/` — the remediation toolkit

`systematic-review/` contains a complete, tested execution toolkit — search strategy, directory structure, CSV templates, and Python scripts — for someone with institutional Web of Science/Scopus/PubMed access to run the review's formal search strategy and feed the results back into this review through a reproducible pipeline (deduplication → screening → PRISMA counting → claim/table-cell audit). See `systematic-review/README.md` for the step-by-step execution guide, and `WBE_Review_Systematic_Search_Strategy.md` (one directory up) for the actual search strings (one core search + seven complementary module searches, eight searches total, across all three databases).

**The toolkit is built and tested (against clearly-labeled synthetic data only — see `systematic-review/tests/TEST_RESULTS.md`). It has not been run against any real search.**

### What happens next

Two independent tracks exist in this project, and progress on one does not imply progress on the other:

1. **Conceptual chapter drafting** (Chapters 1–12) continues at the user's direction, each new chapter subject to this review's standing evidentiary discipline (hedged, web-search-derived, never claiming full-text verification). This is the track currently active — Chapters 1–10 are drafted; Chapters 11–12 remain.
2. **Formal evidence remediation** — converting the review from search-engine-summary-driven to full-text-evidence-driven — is triggered only by **the user (or someone with institutional access) supplying real Web of Science, Scopus, and PubMed export files** into `systematic-review/data/raw/{wos,scopus,pubmed}/`, or a genuine pilot import (see `systematic-review/`'s pilot-mode tooling, built and tested but not yet run against real data as of this round). Until that happens:
   - No hypothetical PRISMA numbers, hit counts, or full-text-verification claims are generated
   - `WBE_Review_Ch8_Evidence_Freeze_Audit.md` continues to report the true, current state, recomputed as each new chapter's references are added
   - Every chapter, however many are eventually drafted, continues to carry the same "conceptual working draft, not submission-ready" status until this track closes it out

### Files awaited from the user / a database-access holder

- Raw exports (`.ris`/`.csv`/`.nbib`) for the core search and all 7 complementary modules, across Web of Science, Scopus, and PubMed (24 files if all are run; see `systematic-review/README.md` §1–§3 for naming/placement)
- The completed `systematic-review/templates/search_log.csv` (one row per search actually run)
- Title/abstract and full-text screening decisions once screening is performed
- Any full-text PDFs the user can supply directly for specific high-priority references, even before a full database search is completed — this review can audit any paper supplied directly regardless of the database-access question
