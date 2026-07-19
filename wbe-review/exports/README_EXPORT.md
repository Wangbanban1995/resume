# Export Package — Wastewater-Based Epidemiology Review

**Export date:** 2026-07-19
**Source commit:** `97ef355` (branch `claude/academic-research-skill-98xd40`)

This package is a read-only export for review and annotation. **No manuscript content, Evidence Freeze status, or claim conclusion was modified to produce it.** It packages the canonical project files already committed at the commit above, with a short status label added to the first page of each exported PDF/DOCX (not written into any canonical source file's body).

## Current evidence status (unchanged by this export)

```text
Full-text obtained: 0/67
Full-text read: 0/67
Critical claims resolved: 0/9
Submission ready: No
```

## Condensed manuscript word count

Body-only prose: **7,307 words** (within the 7,200–7,600 target band).
Full drafted total (body + headings + Table 2/Table 3 content): **7,770 words**.
Source: `WBE_Review_Condensed_Draft_Word_Count.csv`, regenerated via `scripts/word_count_condensed.py` at export time.

## What each top-level folder contains

- **`condensed/`** — the submission-length, evidence-recovery-tracked manuscript (`WBE_Review_WR_Condensed_Draft.md/.docx/.pdf`). **This is the file to read and annotate.** It is a critical-review-length synthesis of the source draft, positioned per `WBE_Review_Positioning_Decision_Memo.md` as Route A (Water Research Critical Review), still pending formal database search and full-text verification of its 9 Critical + 7 High evidence gaps.
- **`source-draft/`** — the complete, unabridged 10-chapter conceptual working draft (`WBE_Review_Ch1-10.md/.docx/.pdf`). **This is a full-content archive, not the document to mark up.** It is the pre-compression source the condensed manuscript was derived from; every claim, mechanism, and evidence note in the shorter document traces back to specific passages here (see `WBE_Review_Condensed_Claim_Map.csv` in the main repository for the traceability record — not included in this export, since it is a project-internal tracking file, not reader-facing content).
- **`supporting/`** — 14 design, planning, and status documents supporting either manuscript:
  - `WBE_Review_Figure_Design_Brief.md/.docx` — structural specification and draft captions for the 4 planned figures (none produced as images yet; all author-original, none blocked on full-text evidence).
  - `WBE_Review_Table_Design_Brief.md/.docx` and `WBE_Review_Table_Format_Standard.md` — audit and formatting standard for Table 2/Table 3, including the "pending full-text evidence verification" footnote convention now applied to both tables in the condensed manuscript.
  - `WBE_Review_Supplementary_Outline.md/.docx` — table of contents and content-source plan for the eventual Supplementary Information (not yet drafted as a standalone SI document).
  - `WBE_Review_Positioning_Decision_Memo.md/.docx` — the Route A (Critical Review) vs. Route B (conceptual perspective/framework) comparison; **Route A is the currently retained positioning**, per the most recent explicit decision.
  - `WBE_Review_Post_Evidence_Recovery_Checklist.md` — the ordered next-steps plan for formal database search, PDF acquisition, and full-text verification, once real access exists.
  - `WBE_Review_Terminology_Guide.md` — preferred/avoided-term reference for 12 core concepts.
  - `WBE_Review_Abstract_Outline.md`, `WBE_Review_Highlights_Outline.md`, `WBE_Review_Cover_Letter_Outline.md` — structural placeholders only; **no submittable Abstract, Highlights, or cover letter text exists anywhere in this project.**

## What is not included, and why

- No PDF of any cited literature, no `data/fulltext/`, no `data/evidence/`, and no private full-text extract — this project has never obtained real full text for any of its 67 active references, so there is nothing of that kind to exclude beyond confirming none exists.
- No `.git/` directory or git history.
- No file containing a personal account, API key, or access credential — none exists in this project's tracked files.
- No temporary cache files (`__pycache__/`, `.pyc`, etc.) from this project's Python tooling.

## Outstanding work before this project could be considered submission-ready

Per `WBE_Review_Positioning_Decision_Memo.md` (Route A retained) and `WBE_Review_Post_Evidence_Recovery_Checklist.md`:

1. Execute the formal database search (Web of Science, Scopus, PubMed) — 0 searches run to date.
2. Obtain and read full text for the 9 Critical + 7 High evidence-gap claims — 0/67 obtained, 0/67 read.
3. Resolve [57] (Link, Garrido, et al. 2026)'s single-preprint status — formal version or independent second source not yet found.
4. Draft the SI §S4 existing-review competition matrix (flagged as new content, not yet started).
5. Produce the 4 planned figures as actual images (specified in `WBE_Review_Figure_Design_Brief.md`, not yet drawn).
6. Draft Table 1 and Table 4 (planned in the Target Outline, never drafted — see `WBE_Review_Table_Design_Brief.md`).
7. Renumber references for submission (currently deferred by design, original source-draft numbering retained).
8. Draft the actual Abstract, Highlights, and cover letter (only structural outlines exist).

**This export does not represent a submission-ready manuscript at any stage of either folder.**
