# Phase 2B Risk Log — Disposition of Phase 2A's Five Flagged Risk Points

**Round:** Water Research compression, Phase 2B. 2026-07-18. Documents how each of the five highest-risk compression points flagged at the end of Phase 2A was addressed this round, plus the status-note wording correction requested at the start of this round.

## 0. [56]/[57] status-note wording correction

**Finding:** Every project file (`WBE_Review_References.md`, `WBE_Review_Citation_Verification_Table.md`, `WBE_Review_Pending_Verification_List.md`, `WBE_Review_Ch8_Evidence_Freeze_Audit.md`, `WBE_Review_Rename_Crossref_Log.md`) has consistently and correctly shown [56] withdrawn and [57] active throughout every round. The grep audit run at the start of this round confirms this. **No project file contained an error.** The Phase 2A round's final chat-summary sentence — "withdrawn [56] and [57] not used" — was ambiguous prose that could be misread as claiming [57] was also withdrawn, when it meant only that neither was cited in Parts 1–4.

**Action taken:** Added a short clarification note to `README.md`'s reference-count bullet, explicitly restating [57]'s active status and naming the prior round's wording as the source of the ambiguity, not a file error. Authoritative state reconfirmed: issued 68, active 67, withdrawn 1 ([56]), full-text read 0/67. This round additionally **used [57] directly** (Link, Garrido et al. 2026, in condensed Part 6.1), demonstrating its active status in practice, not merely in the reference list.

## 1. Part 4's ~89% compression ratio

**Disposition:** Accepted as-is, per this round's explicit instruction not to restore the long per-biomarker narrative. **Confirmed** (not merely asserted) that all five required categories are present in the SI planning:
- All candidate population markers → `WBE_Review_Supplementary_Outline.md` §S5 (9 named biomarkers, full seven-criterion detail)
- The original 8 normalization failure modes → new §S6a added this round, explicitly named as the target of the condensed draft's "three particularly consequential... complete eight-mode catalog... given in Supplementary Table S4" pointer (§4.4)
- Extended method comparisons → §S6 (full Table 3 narrative, Langeveld/Rainey/Darling/Been/Baz-Lomba/Thomas)
- Detailed performance/applicability conditions → §S6, explicitly expanded this round to state it carries "every candidate normalizer's full applicability-condition and performance detail"
- Full normalizer evidence matrix → §S6's full current Table 3, pre-redesign

## 2. Six-concept taxonomy over-compression in §4.1

**Disposition:** Fixed. Added a 60-word compact clause to §4.1 (within the ≤70-word limit) explicitly naming all six concepts: systematic bias, random error, information loss, recovery loss, inhibition, temporal or compositional representativeness — closing with an explicit forward-pointer ("Part 5 propagates each through to a final uncertainty estimate") so Part 5's uncertainty discussion has the conceptual interface it needs without re-deriving the taxonomy from scratch. Verified the clause does not expand into a full re-explanation.

## 3. Part 1.3's four-contribution framing

**Disposition:** Fixed. Reworded the opening sentence to "This review advances four linked propositions, offered as this review's own organizing synthesis rather than as an existing consensus," matching the requested "This review advances four linked propositions..." pattern. Removed language that could read as claiming established fact (e.g., changed "it formalizes" framing to "is usefully formalized as," "normalization should be understood as," etc. — softened verb choices throughout the paragraph to keep the propositional, authorial framing consistent). Updated the Condensed Claim Map's P1-5 row: `evidence_level = "Conceptual synthesis (original framework)"` — consistent with, though not verbatim, the requested `Author conceptual synthesis` tag (the Claim Map's `evidence_status` field, added this round, uses the exact string "Author conceptual synthesis" for this row).

## 4. Part 3's new connective paragraphs

**Disposition:** Checked and confirmed no citation-scope expansion. The two paragraphs in question (P3-2, residence-time-distribution consequences; and the expanded P3-4/P3-5 network-level-controls and memory-effect-detection material) carry **no external citations at all** — they are pure logical derivations from mechanisms already established with citations elsewhere in Part 3 (§3.2's Zhang et al./Jung et al. biofilm findings; §3.3's sedimentation/resuspension mechanism). Because they cite nothing, they cannot have broadened any citation's support scope. Per instruction, their `evidence_level`/`evidence_status` fields in the Condensed Claim Map were updated this round from generic "Conceptual synthesis" to the specific tag **"Conceptual synthesis based on preceding process evidence"** for P3-2, P3-4, and P3-5, making this status explicit and auditable rather than implicit.

## 5. Eight-to-three normalization failure modes

**Disposition:** Fixed. §4.4 now opens: "Normalization fails through several mechanisms; **three particularly consequential failure modes** are highlighted here, with the complete eight-mode catalog (including irreversible degradation, unknown non-human sources, and structural model misspecification) given in Supplementary Table S4." This explicitly signals (a) three is a selection, not the complete set, (b) the complete set has eight members, (c) three of the five omitted modes are named directly so a reader is not left guessing, and (d) the SI location is named. The complete 8-item catalog is preserved verbatim in `WBE_Review_Supplementary_Outline.md` §S6a, added this round specifically to be this pointer's target.

## Summary

All five Phase 2A risk points and the status-note wording issue are resolved this round. None required reversing a compression decision — all five were addressed by adding precise, bounded clarifying language (the six-concept clause, the "three of eight" framing, the propositional reframing of Part 1.3) or by confirming/extending SI coverage that was already substantively planned but not yet explicitly cross-referenced. No word-count target was missed as a result of these fixes; see `WBE_Review_Compression_Log.md` for the final per-part word counts.
