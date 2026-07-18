# Supplementary Information Outline — Water Research Submission (Planning Document Only)

**Round:** Water Research compression, Phase 1. 2026-07-18. This plans what the Supplementary Information (SI) accompanying the eventual submission-length manuscript would contain, drawing on the "SI destination" column already assigned per-section in `WBE_Review_Content_Priority_Audit.csv` and `WBE_Review_Compression_Map.md`. **No SI document has been written — this is a table of contents and content-source plan only.**

**Internal-audit-file boundary, stated explicitly per instruction:** this project's internal claim audits (`WBE_Review_Ch9_Claim_Audit.md`, `WBE_Review_Table7_Evidence_Audit.md`), the Citation Verification Table, the Evidence Freeze Audit, the Pending Verification List, the Ch10 Evidence Note, and the Rename/Crossref Log remain **project-internal working documents** and are **not** listed as SI sections below. They serve this project's own evidence-discipline process, not a journal's supplementary-material requirements — a submission's SI should contain finished, reader-facing supplementary content, not this project's internal audit trail. Where an internal audit file's *findings* are relevant to SI content (e.g., which claims still need full-text verification), that information feeds into SI section content rather than the audit file itself being attached.

## SI Table of Contents

### S1. Supplementary Methods
**Source:** Current §2.2 (search process), §2.4 (terminology/developmental background), §2.6 (scope boundaries); §5.1-§5.4 (sampling location/mode/matrix/preservation detail cut from Part 4.1); §8.6-§8.8, §8.11 (delta method, Monte Carlo mechanics, sensitivity-analysis method taxonomy, censoring-method detail cut from Part 5.4).
**Content:** The full search-process narrative (queries issued, sources prioritized, known under-sampling risks); standard sampling/analytical methods background not specific to this review's original contributions; formal uncertainty-propagation method exposition (delta method derivation, Monte Carlo procedure, sensitivity-analysis method comparison, censored-data-handling methods) at full technical depth, for a reader who wants the mechanics the main text only references.
**Note:** This section should NOT include the full source-verification-limitation narrative (§2.3) beyond what the main text's compressed version already states — the *fact* that 0/N references are full-text verified belongs in the main text (Part 1.2), not buried in SI where a reviewer might miss it.

### S2. Full Search Strategies
**Source:** `WBE_Review_Systematic_Search_Strategy.md` (existing project file, one directory up from `wbe-review/`).
**Content:** The complete core-search-plus-seven-complementary-module Boolean query set for Web of Science, Scopus, and PubMed, as already drafted in the existing search-strategy document — reproduced or referenced in SI once the formal search is actually run, per this project's still-pending "Track 2" (formal evidence remediation).
**Status flag:** As of this round, the formal search has not been executed. If the manuscript is submitted before Track 2 completes, this SI section should state that explicitly rather than imply a completed search, consistent with the standing instruction never to fabricate PRISMA numbers or claim a systematic search was run.

### S3. PRISMA Materials (placeholder)
**Source:** `systematic-review/scripts/generate_prisma_counts.py` and its templates (existing, tested-on-synthetic-data-only toolkit).
**Content:** PRISMA flow diagram (records identified/screened/included/excluded at each stage) and the PRISMA checklist, populated only once a real database search has actually been run through the existing toolkit.
**Status flag, stated as directly as possible:** **This section is empty in the current project state and must remain empty, or explicitly marked "not yet available," until a genuine search is executed.** Per this round's standing constraint ("不生成PRISMA数字"), no placeholder numbers, example counts, or illustrative figures should ever be entered here even provisionally — an empty, explicitly-labeled placeholder is the only acceptable state before Track 2 completes.

### S4. Existing-Review Competition Matrix
**Source:** New content — not present in any current project file.
**Content:** A table comparing this review against other recent WBE reviews already cited in the current draft as covering adjacent ground (e.g., Zhu et al. 2025 on methodological frameworks generally, Punch et al. 2025 on AMR specifically, Wang/Amarasiri/Oishi/Sano 2026 on modeling-strategy taxonomy) — scope, method, and what this review's four original contributions add that those reviews do not already cover. This is standard practice for a Water Research review submission (reviewers routinely ask "how does this differ from review X") and does not currently exist anywhere in this project; **flagged as new SI content to be drafted, not extracted from the existing source draft.**

### S5. Biomarker Characteristics
**Source:** Current §6.4 (chemical population biomarkers) and §6.5 (microbial/molecular population biomarkers) — the per-biomarker narrative detail identified in the Content Priority Audit and Compression Map as compressing into Table 2 for the main text, expanded back out to full detail here.
**Content:** The full seven-criterion (human specificity, excretion variability, dietary/behavioral dependence, in-sewer stability, non-human sources, analytical compatibility, rainfall/dilution sensitivity) evaluation for every candidate biomarker discussed (creatinine, cotinine, 5-HIAA, caffeine/paraxanthine, artificial sweeteners, ammonium/TKN/TP, PMMoV, crAssphage, HF183/BacHuman/mtDNA), including every named study's specific finding, exactly as currently written in §6.4-§6.5.

### S6. Normalization Evidence
**Source:** Current §6.2-§6.3 (flow-based and population-based normalization evidence), Table 3's full current form.
**Content:** The full comparative-study narrative currently in §6.2 (Langeveld et al., Rainey et al., Darling et al.) and §6.3 (Been et al., Baz-Lomba et al., Thomas et al.), and the current, non-redesigned version of Table 3 at full density (before the main-text redesign compresses it for Table 2).

### S7. Reconstruction-Model Evidence
**Source:** Current §7.1-§7.2, §7.4 full text; current Table 4 and Table 5 at full, non-merged density.
**Content:** The complete per-method-family, per-study narrative (Zuccato et al. 2008 through Alhassan et al. 2025) currently in §7.1.1-7.1.2, the full worked conceptual illustration currently in §7.2, and Tables 4 and 5 in their current, separate, full-detail form (before the main-text merge into Table 3).

### S8. Uncertainty Methods and Evidence
**Source:** Current §8.2-§8.5 (source/sewer/sampling/normalization uncertainty detail), current Table 6 at full density, the two current uncertainty boxes.
**Content:** The full distributional/evidentiary detail currently in §8.2-§8.5 (Jones et al. 2014, Pei et al. 2016, Croft et al. 2020, Yang et al. 2024, Safford et al. 2022), and Table 6 in its current, full-density, non-redesigned form.

### S9. Technology-Readiness Evidence
**Source:** Current §10.1-§10.9 full text; current Table 8 at full density.
**Content:** The complete per-technology narrative currently in Chapter 10 (Schang et al. 2021 through Wang et al. 2025), retained at full detail for a reader wanting the full evidentiary basis behind the main text's compressed technology-readiness assessments.

### S10. Expanded Reporting Checklist
**Source:** The five scattered minimum-reporting-requirement devices currently at the close of §5.7, §6.9 (via the decision framework), §7.7, §8.15, and §9.8, consolidated.
**Content:** A single, comprehensive, checkbox-style reporting checklist covering every item any of the five current chapter-closing reporting standards specify — sampling location/mode/matrix disclosure (§5.7); normalization strategy and goal disclosure (§6.9); back-calculation evidentiary-criteria disclosure (§7.7); uncertainty-propagation method and distribution disclosure (§8.15); and surveillance-objective/threshold/decision-protocol disclosure (§9.8) — presented as one unified, submission-ready checklist a reader could actually use, rather than five separate prose paragraphs scattered across the manuscript. This is the fullest expansion of what the main text's Table 4 (Minimum reporting and decision-readiness framework) summarizes.

## What is explicitly NOT included in SI (and why)

| Excluded content | Reason |
|---|---|
| `WBE_Review_Ch9_Claim_Audit.md`, `WBE_Review_Table7_Evidence_Audit.md` | Internal claim-support audits for this project's own QA process; not reader-facing supplementary content. |
| `WBE_Review_Citation_Verification_Table.md`, `WBE_Review_Ch8_Evidence_Freeze_Audit.md`, `WBE_Review_Pending_Verification_List.md` | Internal evidentiary-status tracking; a submission's reference list and any required data-availability statement serve the equivalent reader-facing purpose. |
| `WBE_Review_Ch10_Evidence_Note.md`, `WBE_Review_Rename_Crossref_Log.md` | Project development-process records; not applicable to any journal's SI requirements. |
| The 6 "Structural bridge" end-matter sections, the "Editorial self-check," "Note on companion files" | Internal document-management content (per the Content Priority Audit and Overlap Audit); has no SI role since it describes this project's own file structure, not the science. |
| `systematic-review/` toolkit itself (scripts, templates) | Code/tooling, not manuscript SI; if ever relevant, would be a code-availability-statement link (e.g., to a repository), not embedded SI content. |

## Word-count note

SI content is not counted against the ~8,850-word prose-body target or the ~10,875-word full-submission estimate in `WBE_Review_Target_Outline.md`, consistent with standard journal practice of not counting supplementary material against the main-text word limit. No SI-specific word budget is set in this Phase 1 round; SI length should be whatever is needed to preserve the evidentiary and methodological detail identified as compressible-but-not-deletable across the Content Priority Audit, Compression Map, and Target Outline.
