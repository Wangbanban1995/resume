# Chapter 8 Uncertainty Audit — 2026-07-13

This note documents how Chapter 8 ("Uncertainty propagation in wastewater-based epidemiology: from source variability to decision uncertainty") was sourced, per the evidentiary requirements specified for this chapter. It is a companion to, not a replacement for, the Citation Verification Table and the Pending Verification List's new Chapter 8 section.

---

## 1. Chemical-WBE and pathogen-WBE uncertainty literature searched separately

Consistent with this review's practice since Chapter 5 of not collapsing chemical and molecular/pathogen target classes into one evidence base, Chapter 8's searches were run as two separate lines of inquiry:

- **Pathogen/molecular-target uncertainty:** searches centered on SARS-CoV-2 wastewater quantification uncertainty, censoring/nondetect handling, and Bayesian/hierarchical case-count reconstruction, returning [44] Dai et al. (2024), [47] Yang et al. (2024), and [48] Safford et al. (2022) as the primary WBE-specific uncertainty sources.
- **Chemical-target uncertainty:** searches centered on drug-consumption back-calculation uncertainty specifically, returning [46] Jones et al. (2014) as the chapter's clearest formal example, plus the two named-but-unverified Monte Carlo studies on methamphetamine consumption and neuropsychiatric drug prevalence (§8.7) — flagged in the Pending Verification List as identified-but-unconfirmed, not cited as verified sources.

No single source was used to make claims spanning both target classes; where a general point applies to both (e.g., §8.6's delta-method applicability conditions, §8.10's correlation argument), it is presented as general uncertainty-propagation methodology rather than attributed to a target-class-specific study.

## 2. Primary studies prioritized over reviews

- **§8.2 (source-end):** Jones et al. (2014) — a primary formal Bayesian modelling study, not a review.
- **§8.4 (sampling/analytical):** Pecson et al. (2021, carried over from Chapter 5) and Safford et al. (2022) are primary studies; Yang et al. (2024) is used as a systematic review specifically for its synthesis-level uncertainty-magnitude comparison, a purpose reviews are well suited to, and is labeled "systematic review / secondary evidence" in the verification table rather than treated as a primary finding.
- **§8.9 (Bayesian hierarchical propagation):** Dai et al. (2024, carried over from Chapter 7) — a primary WBE study, reused here specifically for its hierarchical/state-space structure rather than its predictive-accuracy claims (already flagged pending in the Chapter 7 section of the Pending Verification List).
- **§8.11 (censoring):** Safford et al. (2022) — a primary comparative study, the strongest single piece of WBE-specific evidence in this chapter because it reports a head-to-head method comparison on real data rather than a theoretical argument alone.
- **§8.12 (structural uncertainty):** Alhassan et al. (2025, carried over from Chapter 7) — used here specifically as an ensemble-comparison example, with the explicit caveat restated that it is a retrospective forecast comparison, not a full structural-uncertainty-quantification exercise.

## 3. Which studies considered parameter correlation — tracked explicitly, per instruction

This is the specific tracking §8.10 required, applied to every WBE study cited in Chapters 7–8:

| Study | Considered parameter correlation/covariance? | Basis for this assessment |
|---|---|---|
| Jones et al. (2014) [46] | Partially — models excretion-fraction uncertainty jointly with other pharmacokinetic parameters within one Bayesian framework, so within-source-stage correlation is represented | Framework description recurred consistently across searches |
| Dai et al. (2024) [44] | Yes — hierarchical/random-effects structure explicitly represents site-level and population-level dependency by construction | Method description confirmed via dedicated search (§7.1.2, §8.9) |
| Safford et al. (2022) [48] | Not established in available search summaries — the comparison is framed around censoring-method choice, not cross-parameter covariance | Full-text not accessible; treat as unconfirmed rather than absent |
| Yang et al. (2024) [47] | No — the factorial design (concentration method × extraction kit × primer-probe set) decomposes variance by *step*, which is a different exercise than testing whether steps' errors are mutually correlated | Explicit in the factorial-design description |
| Pecson et al. (2021) [24] | No — reports within- vs. across-protocol spread, not a correlation structure among specific named parameters | Carried over from Chapter 5 sourcing |
| Alhassan et al. (2025) [45] | No — ensemble members are compared, not decomposed into correlated input parameters | Carried over from Chapter 7 sourcing |

**Finding, stated directly in §8.10 and confirmed by this table:** the majority of this review's own WBE evidence base does *not* formally address parameter correlation, which is the empirical basis for §8.10 being flagged as "this chapter's most consequential subsection" — the gap is demonstrated by this review's own sourcing, not merely asserted in the abstract.

## 4. Which studies propagated structural uncertainty (vs. only parameter uncertainty)

- **Structural uncertainty explicitly addressed:** Alhassan et al. (2025) [45] — the only source in this review's full evidence base (Chapters 7–8 combined) that compares multiple model structures directly (an 11-model ensemble), rather than propagating parameter uncertainty within one fixed structure.
- **Structural uncertainty not addressed (parameter uncertainty only, or point estimates only):** Jones et al. (2014), Dai et al. (2024), Safford et al. (2022), Yang et al. (2024), Pecson et al. (2021), and every back-calculation method-family study cited in §7.4's Table 5.

This asymmetry is the direct evidentiary basis for the Chapter 8 Box "Why Monte Carlo Simulation Does Not Solve Model Misspecification," which states that uncertainty propagation and structural-adequacy testing are performed by "substantially different, and mostly non-overlapping, subsets of studies" — a claim grounded in this specific count (1 of 6+ studies addressing structural uncertainty at all), not a general impression.

## 5. Which studies validated output intervals against coverage or external data

- **Safford et al. (2022) [48]** is the one source in this chapter's evidence base that compares method output against an independent external series (clinical case trends) for the specific purpose of evaluating which censoring-treatment method performs better — the closest this review's evidence base comes to §8.16's coverage/posterior-predictive-check standard, though even this is a comparative-agreement check, not a formal coverage calculation (fraction of true values falling within a stated interval across repeated trials).
- **No source cited in Chapter 8 reports a formal coverage statistic** (e.g., "the 95% interval contained the true/reference value in X% of instances"). This absence is stated as a documented finding in §8.16 ("diagnostics this review's evidence base found rarely reported in applied WBE studies") and is confirmed here as accurate to this chapter's actual source list, not an unsupported generalization.
- Dai et al. (2024) is described in §8.9 as this review's clearest example of the underlying Bayesian machinery that *could* support posterior predictive checking, but no search result confirmed that posterior predictive checks were actually reported in that specific study — this distinction (capability vs. demonstrated practice) is preserved in the main text and repeated here.

## 6. Positive and negative/null findings preserved, not cherry-picked

- Safford et al. (2022)'s finding is presented as comparative-performance evidence (EM-MCMC better than substitution), which is a positive finding for principled censoring methods — no null or negative counter-finding on this specific question was located in searches, and none is fabricated to force balance; the absence of a counter-example is stated as such in the Pending Verification List rather than concealed.
- The Monte Carlo critique in §8.7 is deliberately structured as a critique of common *practice* (arbitrary distributions, default independence, cross-population parameter pooling, interval-only reporting) rather than a claim that Monte Carlo methods themselves are invalid — this preserves the distinction between "a method is unreliable" (not this review's claim) and "a method is frequently misapplied in this literature" (the claim actually made, and the one the evidence supports).
- §8.9's Bayesian-hierarchical section states the narrow-posterior-≠-certainty critique as a general methodological caution applicable to any Bayesian analysis, Dai et al.'s included, rather than exempting the review's own most-cited Bayesian source from the same scrutiny applied to the method in general.

## 7. Reference-count and evidence-base summary

Chapter 8 adds five references in total to a running total of 50 references across the full review: [46]–[48] at first drafting, plus [49]–[50] added in the 2026-07-13 consistency-check round to name the two chemical-WBE Monte Carlo studies §8.7 had previously referenced without citation. Of these five: three ([46], [48], [50]) are classified as primary WBE methodological/modelling studies, one ([47]) as systematic review/secondary evidence, and one ([49]) as a primary WBE methodological/modelling study with an incompletely-confirmed author list. Author-list confirmation status: [48] and [50] are confirmed to the same two-independent-search/PubMed-record standard used for this review's best-supported sources; [46], [47], and [49] carry author lists that are either retained from an earlier retrieval not re-confirmed this round, or (for [49]) confirmed only for 6 of 7 authors — all three are flagged accordingly in the Citation Verification Table and Pending Verification List rather than presented with unwarranted confidence.

---

## How to use this note

Read this alongside §8.10 (correlated uncertainties), the Box on Monte Carlo and model misspecification, and §8.16 (validation) in the main text — those sections state the review's substantive conclusions; this note documents the sourcing basis for those conclusions being an evidence-grounded finding about this review's own literature sample, not a general claim about the entire WBE uncertainty-quantification literature, which was not exhaustively searched (see §2.1–§2.2 of the main document).
