# Terminology Guide — Preferred and Avoided Terms

**Round:** Water Research compression, Phase 3C (manuscript presentation and internal-consistency refinement). 2026-07-19. This guide documents the terminology already in consistent use in `WBE_Review_WR_Condensed_Draft.md` as of this round, so future edits do not silently drift into a synonym the manuscript does not otherwise use. It is a style-consistency reference, not a glossary of technical definitions — the definitions themselves live in the manuscript body (§1.1–1.3 for the core taxonomy, §5.2 for identifiability/observability, §5.3 for validation).

Each entry lists the **preferred term**, terms to **avoid**, and the **usage context** actually found in the current draft. Where a term the instructions asked to check (e.g. "observed concentration") does not appear verbatim in the draft, this is stated explicitly rather than silently introducing a new synonym.

## 1. Wastewater-based epidemiology / wastewater surveillance

- **Preferred:** "wastewater-based epidemiology (WBE)" on first use per major section grouping (title, §1.1); "WBE" thereafter as the established abbreviation; "wastewater surveillance" when the emphasis is on the monitoring *activity/program* rather than the *epidemiological inference method* (e.g. §6–7's public-health-action and infrastructure discussion, where "surveillance system," "surveillance objective," and "surveillance program" are the natural collocations).
- **Avoid:** switching between "WBE" and "wastewater surveillance" within the same paragraph for the same referent; "wastewater-based disease surveillance" (used only in the NASEM 2023 citation's own title, not as this review's running term).
- **Current usage:** consistent — "WBE" (3 spelled-out + abbreviated instances) is used for the inferential framework, "wastewater surveillance" (2 instances) for the activity/system, matching the distinction above.

## 2. Source state

- **Preferred:** "source state" — the true, unmeasured population-level quantity (infection status, consumption, exposure) that WBE aims to recover, established in §2 and used consistently through §5.
- **Avoid:** "true state," "underlying state," or "ground truth" as substitutes in running prose (these appear only inside Table 3 cells or in the validation-methodology discussion of §5.3, where "known ground truth" specifically names a synthetic-validation design element, not the source state itself — keep that distinction).
- **Current usage:** 7 instances, consistent.

## 3. Sewer-entry load

- **Preferred:** "sewer-entry load" — the mass of analyte actually entering the public sewer network, already distorted relative to the source state, per §2's closing paragraph. This is a deliberately narrow, single-purpose term and should not be loosely substituted for "source state" or "excreted mass."
- **Avoid:** introducing a second name for the same concept (e.g. "entry load," "network-entry mass") elsewhere in the manuscript.
- **Current usage:** 2 instances, both in §2, where the term is defined and then immediately used — correct, minimal usage; no drift elsewhere in the draft.

## 4. Observed concentration / observed load

- **Note:** neither "observed concentration" nor "observed load" appears verbatim anywhere in the current draft. The manuscript's actual preferred terms for this concept are **"measured concentration"** (used in §1.1, §3.3, §3.4, §4.2) and **"[flow-normalized / mass] load"** (used in §4.2), consistently paired with a qualifier (measured, flow-normalized) rather than used as a bare "load."
- **Recommendation:** continue using "measured concentration" rather than introducing "observed concentration" as a synonym; the manuscript's own inverse-problem framing (§1.1) already uses "observation" as the general term for what is measured, so "measured concentration" avoids a needless second word for the same idea. No change made to the draft for this entry — it already reflects the recommended usage.

## 5. Normalization

- **Preferred:** "normalization" (not "normalisation") throughout — confirmed consistent (24 instances, all American spelling).
- **Avoid:** using "normalization" and "correction" interchangeably as if synonymous; the draft is careful to treat normalization as one specific *kind* of correction (mechanism-specific, per §4.4's core proposition), so "correction" remains the broader term and "normalization" the narrower one. This distinction is already respected in the current text and should be preserved in any future edit.

## 6. Reconstruction

- **Preferred:** "reconstruction" for the general act of recovering a source-state estimate from an observed signal (§5.1's title and framing).
- **Avoid:** "recovery" as a bare synonym for reconstruction in running prose — "recovery" is already a reserved, narrower technical term in this manuscript (the fraction of true target mass surviving concentration/extraction, §4.1) and using it loosely for "state recovery" risks colliding with that definition. Where the draft does pair "recovery" with "state" (e.g. "source-state recovery," "synthetic-state recovery," "state recovery") the compound phrasing keeps the two senses distinct; a bare "recovery" should always mean the analytical-recovery sense unless immediately qualified.
- **Current usage:** consistent — checked directly; every instance of bare "recovery" refers to analytical recovery, every state-level use is compounded ("state recovery," "source-state recovery").

## 7. Inference

- **Preferred:** "inference" for the overall epidemiological conclusion-drawing process (title, §1.1's "epidemiological inference"); "inferential target" (§5.1) for the specific quantity a reconstruction is asked to estimate.
- **Avoid:** using "inference" and "reconstruction" as interchangeable — inference is the broader downstream use of a reconstructed signal, not the reconstruction step itself.
- **Current usage:** consistent, 5 instances.

## 8. Identifiability

- **Preferred:** "identifiability" as the general term; "structural identifiability" and "practical identifiability" (§5.2) as the two named, formally distinguished sub-types. Do not use "identifiability" unqualified when a claim specifically concerns only one of the two sub-types.
- **Avoid:** "identifiable" as a loose synonym for "accurate" or "reliable" — it has the specific technical meaning defined in §5.2 throughout this manuscript and should not be used more casually elsewhere.
- **Current usage:** 20 instances, all consistent with the §5.2 definitions once introduced; §1.1–§3 use "identifiable"/"identifiability" informally ahead of the formal §5.2 definition, which is an intentional and clearly-signaled forward reference ("the distinction §5.2 develops formally," §5.1), not an inconsistency.

## 9. Observability

- **Preferred:** "state observability" or "observability" per §5.2's definition — whether the underlying latent state is recoverable from the observed signal at all.
- **Avoid:** conflating observability with identifiability; the manuscript is explicit (§5.2) that a model can have every parameter identified and still have an unobservable state, and vice versa. Keep the two terms doing separate work.
- **Current usage:** 10 instances, consistent.

## 10. Uncertainty

- **Preferred:** "uncertainty" as the general term, with the specific sub-types named explicitly where relevant (input, correlated-parameter, ratio, censoring, temporal, structural, scenario — §5.4's enumerated list). Avoid using bare "uncertainty" where a specific sub-type is actually meant and the distinction matters to the argument.
- **Current usage:** 42 instances — the manuscript's single most common technical term, consistent with its central role; no drift detected between sections.

## 11. Validation

- **Preferred:** "validation" as the general term, with the six specific levels named per §5.3 (internal fit, temporal holdout, external site, event-based, synthetic-state recovery, decision-value) used explicitly whenever a specific level, rather than validation in general, is meant.
- **Avoid:** describing a study as "validated" without specifying which of the six levels was actually met — this is precisely the conflation §5.3 warns against (predictive performance is not source-state recovery), and the manuscript's own prose is checked to avoid it (see `WBE_Review_Full_Text_Verification_Records.csv` once full-text verification resumes, for confirmation that a validation-outcome claim's level is checked against the actual study, not asserted).
- **Current usage:** 20 instances, consistent with the six-level taxonomy once §5.3 introduces it.

## 12. Decision readiness

- **Note:** "decision-readiness" as a compound noun does not appear verbatim; the manuscript's actual usage is **"decision-ready"** (adjective, 2 instances: §5.5's discussion of translating uncertainty into decision-relevant terms, and §6.3's "a decision-ready signal, at minimum, should disclose...") and **"decision value"** (noun phrase, used in §5.3's validation-level taxonomy and §7.3's readiness hierarchy and research-priority 6).
- **Recommendation:** continue using "decision-ready" (adjective) and "decision value" (noun) as the two forms already in use; do not introduce "decision readiness" as a third variant for the same concept.

## Summary of changes made this round

No changes to claim content, scope, or citation support were made as part of this terminology review. This document is a reference audit of existing usage; no term substitutions were applied to the manuscript body under this item — every "current usage: consistent" entry above reflects a check that found no fix needed, and the two-entry exceptions (§4 "observed concentration/load," §12 "decision readiness") are recommendations to *avoid introducing* a new synonym, not corrections of an existing inconsistency.
