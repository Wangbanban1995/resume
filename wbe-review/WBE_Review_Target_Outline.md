# Target Outline — Water Research Submission-Length Manuscript (Planning Document Only)

**Round:** Water Research compression, Phase 1. 2026-07-18. **This is a target outline for a manuscript that does not yet exist as prose — no submission-length text has been written.** It refines `WBE_Review_Compression_Map.md`'s 105-section, 8-part mapping down to level-3 headings, with per-heading word budgets, and adds the four-original-contribution protection matrix and figure/table disposition plan the compression-planning brief separately requested.

**Word budgets below are hand-set at the subsection level, chosen to sum exactly to each part's task-specified target range midpoint** (per `WBE_Review_Compression_Map.md`'s part-level rescaling, reproduced here); they are informed by, but not mechanically derived from, the compression map's finer 105-row allocation — that file remains the audit trail for the underlying per-current-section arithmetic, this file is the human-organized subsection structure built from it.

## Prose-body budget (8 parts, matches Compression Map exactly)

| # | Part | Budget |
|---|---|---:|
| 1 | Introduction and review approach | 900 |
| 2 | From population states to wastewater signals | 1,000 |
| 3 | Sewers as information filters | 1,400 |
| 4 | Observation and normalization | 1,300 |
| 5 | Reconstruction, identifiability and uncertainty | 1,750 |
| 6 | From wastewater signals to public-health action | 1,000 |
| 7 | Enabling infrastructure and technology readiness | 800 |
| 8 | Research priorities and conclusions | 700 |
| **Prose-body total** | | **8,850** |

## Non-body budget (costed independently, per task §7)

| Element | Budget | Basis |
|---|---:|---|
| Tables (4 retained/redesigned, see disposition plan below) | ~1,600 words (~400 each) | Current Tables 3-8 average ~500-700 words each in the source draft; 4 consolidated tables at a submission-typical density (shorter cell text, more rows) estimated at ~400 words apiece |
| Figures (4, captions only — images are not word-counted) | ~200 words (~50/caption) | Current figure captions in the source draft run 15-30 words; a submission-quality caption with a 1-sentence interpretive note runs longer, budgeted at 50 words each |
| References (list only, not prose) | not word-counted for length purposes (journal reference lists are typically excluded from a Water Research word limit) | 67 active references currently; a full systematic search (not yet run) would likely raise this count — no target ceiling is set here since this is a citation-count, not a word-count, planning question |
| Abstract | 200-250 words | Water Research's stated abstract limit |
| Highlights | 3-5 bullet points, ≤85 characters each | Water Research's stated Highlights format (not prose paragraphs) |
| Graphical abstract | 1 image, no body word count; a 1-sentence caption (~20 words) | Standard Elsevier graphical-abstract requirement |

**Estimated full submission length: ~8,850 (body) + ~1,600 (tables) + ~200 (figure captions) + ~225 (abstract) ≈ 10,875 words, plus references and a graphical abstract**, against Water Research's typical ~8,000-12,000 all-in review-article guidance (author-guidelines figure, not independently verified this session against a current Elsevier source — **flagged as pending verification**, since Water Research's exact current word-limit policy was not confirmed via primary-source lookup this round). This estimate is within a plausible submission range but should not be read as a confirmed compliance guarantee until the actual journal guidelines are checked directly.

---

## Part 1. Introduction and review approach (900 words)

### 1.1 WBE as an inverse problem: motivation and the three organizing arguments (600 words)
- **Core question:** Why should a concentration measured at a treatment-plant inlet be treated as the output of a formal inverse problem rather than a direct public-health indicator?
- **Must-retain arguments:** The three organizing arguments from current §1 (object of monitoring is the encoded information, not the concentration itself; the signal is a joint product requiring process-informed correction; the field's next advance requires identifiability-aware, not just accuracy-aware, inference); the amplitude/temporal/spatial distortion taxonomy definitions (currently §1, formally §3.0).
- **Source chapters:** Current §1 (Introduction), condensed.
- **Suggested figures/tables:** None here — Figure 1 (source-to-inference signal chain, see disposition plan) belongs at the Part 2 opening, not here.
- **Duplication to remove:** The distortion-taxonomy definitions currently appear in both §1 and §3.0 verbatim; state once, here, and do not repeat in Part 2.
- **Evidence needing full-text verification before submission:** Institutional figures cited in current §1 (EU dashboard measurement counts, China's national system description) — currently abstract/metadata-level only.

### 1.2 Review approach and evidence status (300 words)
- **Core question:** What kind of review is this (narrative synthesis vs. systematic), and what is its current evidentiary status?
- **Must-retain arguments:** The narrative-synthesis-not-yet-systematic distinction (current §2.1); a compressed, single-paragraph version of the full-text-verification-status disclosure (current §2.3) — a journal reviewer needs this, in some form, in the main text, not only in supplementary methods.
- **Source chapters:** Current §2.1, §2.3 (compressed); §2.2, §2.4-2.6 move to Supplementary Methods per the Content Priority Audit.
- **Suggested figures/tables:** None (Table 1's developmental-phase history and Table 2's application taxonomy move to SI).
- **Duplication to remove:** None specific to this subsection.
- **Evidence needing full-text verification:** The evidence-status statement itself should reference whatever the Evidence Freeze Audit's then-current denominator is at the time of actual compression (not a number frozen at Phase 1 time).

---

## Part 2. From population states to wastewater signals (1,000 words)

### 2.1 Formal problem statement: source signal, distortion operators, identifiability (550 words)
- **Core question:** What does it mean, formally, for a wastewater sample to be a distorted observation of a true source-end signal?
- **Must-retain arguments:** The $Y(t) \approx A(t)[K(t,\tau)\ast X(\tau)] + \varepsilon(t)$ formalization and the amplitude/temporal/spatial distortion definitions (current §3.0) — this is Original Contribution #2 in its entirety and must survive compression almost intact; the identifiability and process-informed-correction definitions.
- **Source chapters:** Current §3.0.
- **Suggested figures/tables:** **Figure 1 (Source-to-inference signal chain)** belongs here — the single most important figure for orienting a reader to the review's whole framework.
- **Duplication to remove:** The "conceptual scaffold, not a validated quantitative model" disclaimer (repeated at §3.0/§5.0/§6.0/§8.0 in the source draft, per the Overlap Audit) should be centralized as one standing-convention sentence stated once here, not repeated at every later equation.
- **Evidence needing full-text verification:** None specific — this subsection is the review's own formal framework, not an evidence-dependent claim.

### 2.2 Source-end biological and behavioral variation; building and local drainage (450 words)
- **Core question:** What actually drives the source-end signal away from a simple, proportional copy of the epidemiological or consumption quantity of interest?
- **Must-retain arguments:** Shedding heterogeneity as temporal distortion; the asymptomatic/undiagnosed-shedding point as an identifiability (not distortion) issue — this is WBE's core comparative advantage and must survive compression; the pharmacokinetic correction-factor point for chemical targets (parent-compound feed into Part 5's $CF$ discussion).
- **Source chapters:** Current §3.1-§3.2, heavily compressed (from 700 to 450 words) — the building/local-drainage material (§3.2) compresses hardest, retaining only the institutional-source and spatial-distortion point.
- **Suggested figures/tables:** Consider folding the source-end row of the new **Table 1 (Process-distortion-observable-correction matrix, see disposition plan)** here as the only table content this subsection needs; no standalone figure.
- **Duplication to remove:** None significant — this pair was checked specifically in the Overlap Audit and found to have low duplication with later chapters.
- **Evidence needing full-text verification:** Miura, Kitajima & Omori (2021) shedding-duration figures (already flagged internally-inconsistent, pending resolution); Boogaerts et al. (2024) pharmacokinetic correction-factor claims.

---

## Part 3. Sewers as information filters (1,400 words)

### 3.1 Physical, chemical, and biological transformation in transit (450 words, includes chapter-opening framing)
- **Core question:** What does the sewer network itself do to the signal between excretion and sampling?
- **Must-retain arguments:** The sewer-as-active-reactor framing; the biofilm-mediated RNA decay finding (Zhang et al., Jung et al.) as this section's clearest piece of direct mechanistic evidence; the amplitude-loss-is-spatially-heterogeneous point (decay coupled to retention time).
- **Source chapters:** Current §4 preamble + §4.1, compressed from ~490 to 450 words.
- **Suggested figures/tables:** Row(s) of **Table 1 (Process-distortion-observable-correction matrix)**.
- **Duplication to remove:** None significant.
- **Evidence needing full-text verification:** Zhang et al. (2023) 90%-in-2-hours biofilm decay figure; Jung et al. (2026) rate-constant comparisons.

### 3.2 Rainfall- and warm-season-induced distortion as a compound, correctable perturbation (460 words)
- **Core question:** Is weather-driven distortion unstructured noise, or a correctable, structured bias?
- **Must-retain arguments:** The Janssens et al. (2022) rainfall-correction finding — this review's clearest single piece of evidence that distortion is a *correctable* structured bias, and the direct empirical anchor for the process-informed-correction thesis (Original Contribution #3's foundation). This is one of the highest-priority individual findings in the entire document and should not be cut for space.
- **Source chapters:** Current §4.2, compressed from 456 to 460 words (essentially unchanged — flagged in the Content Priority Audit as only 25% compressible).
- **Suggested figures/tables:** Row(s) of Table 1.
- **Duplication to remove:** None.
- **Evidence needing full-text verification:** Guo et al. (2023) 26°C decay-acceleration threshold; the specific Belgian program's rain-correction improvement magnitude (Janssens et al.).

### 3.3 Identifiability and the case for process-informed correction (490 words)
- **Core question:** Why can't a single fixed correction ratio restore identifiability once amplitude, temporal, and spatial distortion are shown to be coupled?
- **Must-retain arguments:** The full identifiability argument (current §4.3) — this is Original Contribution #2/#3's connective tissue and should survive compression nearly verbatim; the Rainey-et-al.-vs-Darling-et-al. "not in tension, evidence of no universally identifiable fixed correction factor" synthesis.
- **Source chapters:** Current §4.3.
- **Suggested figures/tables:** None additional — this subsection is argument, not evidence catalog.
- **Duplication to remove:** None.
- **Evidence needing full-text verification:** None beyond what §3.2/§4.1 already flag.

---

## Part 4. Observation and normalization (1,300 words)

**Explicit compression-risk note:** this part compresses ~11,800 current words (Chapters 5+6 combined) down to 1,300 — an ~89% reduction, the most aggressive of any target part. This is only achievable by (a) moving nearly all per-biomarker narrative detail into the redesigned Table 2 (Normalization-assumption-residual-uncertainty matrix, replacing current Table 3) rather than prose, and (b) accepting that Chapters 5 and 6's current per-target, per-study evidentiary walkthroughs cannot survive in prose form at all. This is flagged here explicitly as a judgment call the author should confirm before Phase 2, not assumed.

### 4.1 Two observation models and the six-concept sampling/analytical taxonomy (500 words)
- **Core question:** What separates the molecular-target and chemical-biomarker observation models, and why must recovery, precision, sensitivity, censoring, representativeness, and replicate-type be kept as six distinct concepts rather than one "uncertainty"?
- **Must-retain arguments:** The two observation-model equations (§5.0); the six-concept taxonomy itself (§5.5) — used repeatedly downstream (Part 5), a genuinely original organizing contribution that must be kept even though its supporting per-study evidence (Pecson et al., Ahmed et al.) compresses into the table.
- **Source chapters:** Current §5.0, §5.5-§5.7, heavily compressed (from ~2,400 to 500 words); §5.1-§5.4, §5.6 detail folds into the table or is cut.
- **Suggested figures/tables:** Table 2 rows.
- **Duplication to remove:** None here (this is the taxonomy's canonical, first-use location).
- **Evidence needing full-text verification:** Pecson et al. (2021) 36-SOP interlaboratory spread figures; Ahmed et al. (2022) process-LOD platform-comparison figures.

### 4.2 Normalization as conditional statistical adjustment, not source-state reconstruction (300 words)
- **Core question:** What is normalization actually correcting, and why is "Normalization ≠ reconstruction of the true source state" the chapter's central proposition?
- **Must-retain arguments:** The $Z(t)=\mathcal{N}[\ldots]$ formalization; the "Normalization ≠ reconstruction" boxed proposition (current §6.0) — this is a direct, quotable statement of Original Contribution #3 and should be retained essentially verbatim; the five-goal taxonomy (§6.1) compressed to a short list.
- **Source chapters:** Current §6.0-§6.1.
- **Suggested figures/tables:** None additional.
- **Duplication to remove:** The equation's "conceptual scaffold" disclaimer — cross-reference Part 2.1's standing convention instead of restating.
- **Evidence needing full-text verification:** Ahmed, Philo et al. (2026) 247-article systematic-review finding (normalization goals frequently unspecified) — keep the qualitative finding, flag the specific article count as pending verification.

### 4.3 Evidence on flow-, population-, and biomarker-based normalization (300 words)
- **Core question:** Does the evidence support any single normalizer as generally superior, or is normalizer performance conditional on hydraulic/population/target-specific context?
- **Must-retain arguments:** The core, load-bearing finding across §6.2-§6.5: normalizer performance is consistently mixed and context-dependent (flow outperforms in one large multi-site study, fails under high I&I in another; PMMoV improves correlation at only 2/12 sites and worsens it at others) — the *pattern*, not the individual-study narrative, is what must survive.
- **Source chapters:** Current §6.2-§6.5, compressed from ~2,900 to 300 words — nearly all per-biomarker narrative moves into Table 2.
- **Suggested figures/tables:** Table 2 (the redesigned, consolidated version of current Table 3) does almost all of this subsection's evidentiary work.
- **Duplication to remove:** None (already the most compressed subsection in the document by design).
- **Evidence needing full-text verification:** Nearly every specific finding in this subsection is currently abstract/metadata-level only (Rainey et al., Darling et al., Maal-Bared et al., Dhiyebi et al., Hsu et al., Chen et al., Chettleburgh et al.) — this subsection carries the highest concentration of pending-verification claims of any part in the target outline, and should be flagged as such in the submission manuscript's own evidence-status statement.

### 4.4 Ratio normalization, the decision framework, and hard failure modes (200 words)
- **Core question:** When does dividing one noisy signal by another help, and when does it actively add uncertainty?
- **Must-retain arguments:** The joint-condition proposition (§6.6) — explicitly named in the source draft as "this chapter's principal original contribution" and must be retained as a standalone, quotable statement even under maximum compression; the eight-question decision framework (§6.9) can be represented almost entirely by its figure rather than by prose.
- **Source chapters:** Current §6.6-§6.9, compressed from ~3,800 to 200 words.
- **Suggested figures/tables:** **Figure 2** could carry the decision-tree content (redesigned/merged from current Figure 1) if the four-figure budget accommodates it — see disposition plan; otherwise reference Table 2's "applicability condition" column.
- **Duplication to remove:** §6.8's failure-mode catalog folds into Table 2's "residual/introduced uncertainty" column rather than standing as separate prose.
- **Evidence needing full-text verification:** None beyond what §4.3 already flags (the joint-condition proposition itself is this review's own original claim, not sourced).

---

## Part 5. Reconstruction, identifiability and uncertainty (1,750 words)

### 5.1 Five distinctions: association, predictive performance, identifiability, observability, structural adequacy (450 words)
- **Core question:** Why is "the back-calculated series correlates with clinical cases" the weakest, not the only, form of evidence a reconstruction claim needs?
- **Must-retain arguments:** The full five-way distinction (§7.0, §7.3) — Original Contribution #4's conceptual core, and the parameter-identifiability/state-observability split specifically, which the source draft revises most substantially from earlier framings; the boxed central-sentence proposition.
- **Source chapters:** Current §7.0, §7.3 (compressed from ~2,500 to 450 words — this is a steep cut for genuinely core material, largely achieved by moving the general, non-WBE-specific epidemic-modeling-identifiability literature discussion to SI).
- **Suggested figures/tables:** **Figure 3 (Process-informed reconstruction and uncertainty framework)** belongs at this subsection's opening.
- **Duplication to remove:** None (canonical location).
- **Evidence needing full-text verification:** Liyanage et al. (2025), Deva et al. (2021) — both general (non-WBE) epidemic-modeling-identifiability sources, currently abstract-level.

### 5.2 Reconstruction method families and the evidence for each (450 words)
- **Core question:** Against the five-way framework, what does each major WBE reconstruction method family (mass-balance, regression, deconvolution, Bayesian/state-space, compartmental, ML, ensemble) actually demonstrate, and what does it not?
- **Must-retain arguments:** The headline finding that no method family achieves all five criteria in the surveyed evidence base — stated once, clearly, rather than re-derived per family in prose.
- **Source chapters:** Current §7.1-§7.2, §7.4, heavily compressed (from ~4,900 to 450 words) — per-study narrative (Zuccato, Ramin, Huisman, Dai, McMahan, Ai, Alhassan) moves almost entirely into **Table 3 (Model-identifiability-validation matrix, consolidating current Tables 4-5)**.
- **Suggested figures/tables:** Table 3 does most of this subsection's evidentiary work; §7.2's worked conceptual illustration compresses to 1-2 sentences or moves to a supplementary box.
- **Duplication to remove:** The Dai et al. (2024) "narrow posterior ≠ identifiability" point currently appears in both the Table 5 cell and in full in §8.9 (Part 5.4 below) — per the Overlap Audit, state it once in 5.4, reference briefly from the table.
- **Evidence needing full-text verification:** Every named study in this subsection (Zuccato et al. 2008, Ramin et al. 2017, Huisman et al. 2022, Schoen et al. 2022, Dai et al. 2024, McMahan et al. 2021, Ai et al. 2022, Alhassan et al. 2025) — currently abstract/metadata-level only; this is the second-highest concentration of pending-verification claims after Part 4.3.

### 5.3 Validation levels and hard reconstruction failure modes (250 words)
- **Core question:** What does "validating" a back-calculation model actually require, and when does no amount of methodological sophistication fix a reconstruction problem?
- **Must-retain arguments:** The internal/external/mechanistic three-level validation distinction (§7.5) merged with §8.16's coverage/posterior-predictive-check validation discussion, per the Overlap Audit's explicit merge recommendation — this pairing should become one subsection, not two; the hard-failure catalog (§7.6) compressed to a short list.
- **Source chapters:** Current §7.5-§7.6 + §8.16 (merged), compressed from ~1,050 to 250 words.
- **Suggested figures/tables:** None additional.
- **Duplication to remove:** This is itself the Overlap Audit's flagged §7.5/§8.16 merge point, executed here.
- **Evidence needing full-text verification:** None beyond what 5.2 already flags.

### 5.4 Uncertainty propagation framework: sources, correlation, structural uncertainty (450 words)
- **Core question:** How does uncertainty enter at each pipeline stage, interact rather than add independently, and propagate to a final confidence statement?
- **Must-retain arguments:** The marginalization-integral formalization and "propagation ≠ bias correction ≠ identifiability restoration" distinction (§8.0) — Original Contribution #4's formal core; the correlated-uncertainty argument (§8.10, explicitly named the chapter's "most consequential subsection"); the narrow-posterior-≠-certainty critique (§8.9, canonical location per the Overlap Audit merge with 5.2); the structural-uncertainty/Monte-Carlo-does-not-fix-misspecification point (§8.12, box).
- **Source chapters:** Current §8.0-§8.3, §8.5, §8.9-§8.13 (compressed from ~4,800 to 450 words) — §8.4's six-concept re-listing is cut entirely per the Overlap Audit (cross-reference Part 4.1 instead); §8.6-§8.8, §8.11 (delta method, Monte Carlo mechanics, sensitivity analysis, censoring methods) move to Supplementary Methods as largely standard technique exposition.
- **Suggested figures/tables:** **Table 4 (Minimum reporting and decision-readiness framework)** could absorb Table 6's uncertainty-source breakdown if space allows, otherwise Table 6 itself is retained in redesigned form as one of the four target tables (see disposition plan — this creates a 5-table tension the author must resolve, flagged explicitly below).
- **Duplication to remove:** §8.4's near-total restatement of §5.5's six concepts (per Overlap Audit) — removed here by construction (not drafted in the first place, only cross-referenced).
- **Evidence needing full-text verification:** Jones et al. (2014) MCMC framework findings; Pei et al. (2016) and Croft et al. (2020) Monte Carlo consumption-estimate figures; Safford et al. (2022) censoring-method comparison.

### 5.5 From scientific to decision uncertainty; minimum reporting (150 words)
- **Core question:** How does a propagated uncertainty distribution become a decision-relevant probability?
- **Must-retain arguments:** The exceedance-probability/asymmetric-cost vocabulary (§8.14) — canonical location per the Overlap Audit (Part 6.1's alert-threshold discussion should reference this rather than re-explain it); a 1-2 sentence compressed reporting-standard statement (§8.15), full checklist to SI.
- **Source chapters:** Current §8.14-§8.15, compressed from ~590 to 150 words.
- **Suggested figures/tables:** None additional.
- **Duplication to remove:** None (canonical location; Part 6.1 is the one that should shorten).
- **Evidence needing full-text verification:** None (this subsection is decision theory, not an evidence-dependent empirical claim).

---

## Part 6. From wastewater signals to public-health action (1,000 words)

### 6.1 Three surveillance objectives and alert-threshold design under asymmetric cost (350 words)
- **Core question:** Why do trend monitoring, anomaly detection, and absolute-magnitude estimation require genuinely different evidentiary standards, and how should an asymmetric false-alarm/missed-detection cost structure set a threshold?
- **Must-retain arguments:** The three-objective distinction (§9.1); a compressed version of the asymmetric-cost point that references Part 5.5 rather than re-explaining exceedance probability and decision thresholds from scratch (per the Overlap Audit); the Link/Garrido 281-county detection-performance example, compressed to its headline sensitivity/PPV comparison and its transfer-validation caveat.
- **Source chapters:** Current §9.1-§9.2, compressed from ~1,290 to 350 words.
- **Suggested figures/tables:** **Table 4 (Minimum reporting and decision-readiness framework)** could absorb a compressed version of Table 7 here.
- **Duplication to remove:** The asymmetric-cost re-explanation (per Overlap Audit, §8.14/§9.2 pairing) — reference Part 5.5, do not restate.
- **Evidence needing full-text verification:** Assoum et al. (2023) early-warning field-study findings; Link, Garrido et al. (2026) 281-county sensitivity/PPV figures.

### 6.2 Multi-source data fusion and its limits (200 words)
- **Core question:** Why is naive averaging across wastewater, clinical, mobility, weather, and pharmacy data streams risky rather than merely suboptimal?
- **Must-retain arguments:** Weather's double role (confounder needing correction AND corroborating stream) — an original, non-obvious point worth keeping explicitly; the shared-external-driver and differential-lag-structure fusion failure mechanisms, compressed to one sentence each.
- **Source chapters:** Current §9.3-§9.4, compressed from ~980 to 200 words.
- **Suggested figures/tables:** None additional.
- **Duplication to remove:** None significant.
- **Evidence needing full-text verification:** Zhang et al. (2025) four-system fusion comparison.

### 6.3 The boundary: what WBE cannot replace, and equity/privacy at fine spatial resolution (300 words)
- **Core question:** What are WBE's structural (not merely practical) limits, and what changes ethically as spatial resolution narrows toward a single building?
- **Must-retain arguments:** The individual-diagnosis-impossibility point; the non-sewered-population structural-exclusion finding (Yu et al.) — a required focus area, must survive compression; the three-way privacy/stigma/equity distinction (§9.6) — re-identification risk, group-level stigmatization, and structural equity-in-who-is-monitored are three different problems requiring different mitigations, and this three-way split must not collapse into one undifferentiated "privacy" sentence even under compression.
- **Source chapters:** Current §9.5-§9.6, compressed from ~1,280 to 300 words.
- **Suggested figures/tables:** None additional (this content is argument-dense, not table-friendly).
- **Duplication to remove:** None significant.
- **Evidence needing full-text verification:** Yu et al. (2024) ~80% sewer-connectivity figure and demographic associations; Moallef et al. (2025) 68/145 health-equity-consideration count; Kwiatkowska et al. (2022) and Thompson et al. (2024) group-stigmatization framing.

### 6.4 From detectable to actionable; minimum reporting (150 words)
- **Core question:** Under what conditions does a scientifically valid signal become institutionally actionable?
- **Must-retain arguments:** The four detectable-to-actionable conditions (§9.7) — a named, explicitly protected original framework (uncertainty translated to decision-relevant terms; institutional response protocol exists; detection-to-action timescale adequate; threshold validated against the specific deployment's cost structure) must be retained as a numbered list even under maximum compression, not paraphrased into prose that loses the four-way structure.
- **Source chapters:** Current §9.7-§9.8, compressed from ~940 to 150 words — §9.8's minimum-reporting list compresses to a cross-reference to the consolidated Table 4.
- **Suggested figures/tables:** Table 4.
- **Duplication to remove:** None (canonical location for this framework).
- **Evidence needing full-text verification:** National strategy guidance's ~1-week reporting-timeliness figure (currently flagged as illustrative order-of-magnitude only, not an established standard).

---

## Part 7. Enabling infrastructure and technology readiness (800 words)

### 7.1 Sensing, measurement, and modeling infrastructure (300 words)
- **Core question:** What infrastructural capabilities determine whether a finer-resolution, lower-latency, mechanistically-grounded signal can be produced at all?
- **Must-retain arguments:** The spatial-resolution/signal-stability trade-off (§10.1, an original framing); the explicit TRL-1-2 classification of near-real-time biosensor results (§10.2) as a demonstration of this chapter's evidentiary discipline; the digital twin as "process-constraint-generating tool, not automatic source-signal validator" distinction (§10.3).
- **Source chapters:** Current §10.1-§10.4, compressed from ~1,460 to 300 words.
- **Suggested figures/tables:** Table 5 rows (Technology-required-evidence-failure-mode-readiness-level matrix, retained/redesigned from current Table 8).
- **Duplication to remove:** None significant.
- **Evidence needing full-text verification:** Schang et al. (2021) low-prevalence detection-floor figures; Sharma et al. (2024) turnaround-time figures; Bam et al. (2025) 147-study digital-twin synthesis.

### 7.2 Process-informed AI, standards, and data interoperability (200 words)
- **Core question:** What distinguishes process-informed AI from purely statistical ML, and what infrastructural gaps (reference materials, data schemas) currently limit cross-study comparability?
- **Must-retain arguments:** Temporal leakage and cross-population validation failure as the two named AI-specific failure modes (§10.5), compressed to one sentence each and referencing Part 3.3's transfer-validation principle rather than re-explaining it (per the Overlap Audit); the standardization-as-precondition argument (§10.6).
- **Source chapters:** Current §10.5-§10.7, compressed from ~1,200 to 200 words.
- **Suggested figures/tables:** Table 5 rows.
- **Duplication to remove:** The transfer-validation re-explanation (per Overlap Audit, argued fully at §9.2/§10.5/§10.9) — reference Part 3.3 or 6.1, do not restate.
- **Evidence needing full-text verification:** Pagsuyoin et al. (2025); Keenum et al. (2024, flagged author-list inconsistency); Therrien et al. (2026) adoption-count claims.

### 7.3 Privacy-preserving analytics, climate resilience, and a technology-readiness framework (300 words)
- **Core question:** What technical (not just policy) responses exist to the privacy/equity tension named in Part 6.3, and how should this review's own evidence base be read for technology maturity?
- **Must-retain arguments:** The federated-analysis-vs-differential-privacy distinction and "technical privacy ≠ governance/equity" point (§10.8); the six-level technology-readiness framework and the analytical-novelty/field-demonstration/operational-readiness three-way distinction (§10.10) — this chapter's principal original deliverable and Original-Contribution-#4-adjacent (applies the same identifiability/evidence discipline to infrastructure rather than statistical models), must be retained in full structure even under compression.
- **Source chapters:** Current §10.8-§10.10, compressed from ~1,130 to 300 words.
- **Suggested figures/tables:** **Figure 4 (Detection-to-decision readiness pathway)** and Table 5 both anchor here.
- **Duplication to remove:** The third transfer-validation instance (§10.9, per Overlap Audit) — shorten to one sentence pointing back to Part 3.3.
- **Evidence needing full-text verification:** Wang et al. (2025) federated-learning water-quality (non-epidemiological) demonstration.

---

## Part 8. Research priorities and conclusions (700 words) — NOT YET DRAFTED

**This part does not exist in the current source draft** (Chapters 11-12 have not been written). The structure below is a target plan for future drafting, not a compression of existing text — no current-draft words map to Part 8 (see Compression Map's explicit note on this).

### 8.1 Research priorities (350 words; capped at 5-7 testable tasks, per instruction — NOT an independent Chapter 11)
- **Core question:** What are the highest-priority, independently testable research tasks this review's evidence base points to?
- **Candidate priorities** (to be finalized when this section is actually drafted; listed here only to confirm the 5-7 cap is achievable from material already in the source draft, not to pre-draft the content):
  1. Cross-population/cross-climate transfer validation of detection thresholds, AI models, and correction models (the three-times-argued transfer-validation principle, §9.2/§10.5/§10.9) — a single, well-designed multi-site transfer study could address all three surface instances at once.
  2. Structural-identifiability and state-observability diagnostics applied specifically to WBE reconstruction models (§7.3's documented gap — general epidemic-modeling identifiability tools exist but are rarely applied to a wastewater observation equation).
  3. A dedicated multi-source (clinical + mobility + genomic + wastewater) fusion study, as opposed to the single-source multi-model ensemble study currently in the evidence base (§7.1.2's named gap).
  4. Formal coverage/posterior-predictive-check validation of propagated uncertainty intervals against independent reference data (§8.16's documented near-absence in applied WBE studies).
  5. A dedicated climate-transfer validation study for process-informed correction models under nonstationary rainfall regimes (§10.9's named gap).
  6. Standardized minimum-reporting-schema adoption testing (§10.7) — does a shared metadata standard actually reduce the ambiguous-dataset-relationship problem this review's own reference management encountered.
  7. *(optional 7th, if space allows)* An operational, decision-value-validated (TRL 6) deployment case study for any of the Chapter 10 technologies — none currently exists in this review's evidence base.
- **Source chapters:** New content, synthesized from gaps already documented across Chapters 3-10 (each candidate above cites its source gap) — not requiring new literature search to identify the gaps themselves, though addressing them would.
- **Must-retain constraint:** Capped at 5-7 items; must not expand into a full standalone chapter.

### 8.2 Conclusions (350 words; 300-400 word range — NOT an independent Chapter 12)
- **Core question:** What does this review establish, and what does it explicitly not establish?
- **Must-retain arguments:** A restatement of the four original contributions (inverse-problem framing; amplitude-temporal-spatial distortion framework; normalization as mechanism-specific causal correction; identifiability- and uncertainty-aware reconstruction from detection to decision) in 1 sentence each; an explicit statement that this remains a conceptual synthesis pending formal systematic search and full-text verification (carried through, in compressed form, from the source draft's standing evidentiary caveat) — this must survive compression, since overstating the manuscript's evidentiary status in the one section most readers finish on is the single highest-risk overclaiming failure mode for this compression effort.
- **Source chapters:** New content — no current chapter is a "conclusions" chapter; loosely informed by current §1's three organizing arguments, restated forward-looking rather than introductory.
- **Must-retain constraint:** 300-400 words; must not expand into a full standalone chapter.

---

## Four original contributions: protection matrix

| Contribution | First defined | Main development | Figure/table carrying it | Final-conclusion location | Duplicate/repeated locations removed by this outline |
|---|---|---|---|---|---|
| **1. WBE as an inverse problem** | Part 1.1 (§1) | Part 2.1 (§3.0) | Figure 1 (source-to-inference signal chain) | Part 8.2 (Conclusions, 1-sentence restatement) | The formal statement currently also appears, restated, in each chapter's own opening bridge language (§5.0, §6.0, §7.0, §8.0, §9.0, §10.0) and again in the 6 end-matter Structural Bridge sections — this outline keeps one canonical statement (Part 2.1) and reduces every other occurrence to a short cross-reference, per the Overlap Audit's largest single finding. |
| **2. Amplitude-temporal-spatial distortion framework** | Part 1.1 / Part 2.1 (§1/§3.0) | Part 2, Part 3 (§3-4) | Figure 2 (distortion framework diagram) | Part 8.2 | The three-term taxonomy is defined once (§3.0/§1, currently duplicated) and then applied, not re-defined, in Chapters 5-10 — this outline preserves that discipline; the one duplication removed is the definition itself appearing twice in the current source (§1 and §3.0). |
| **3. Normalization as mechanism-specific causal correction** | Part 4.2 (§6.0-§6.1) | Part 4 (§6) | Table 2 (normalization-assumption-residual-uncertainty matrix) | Part 8.2 | The "Normalization ≠ reconstruction" proposition and the §6.6 joint-condition proposition are each stated once in the source draft already (no significant duplication found for this contribution specifically) — this outline's main compression action is moving per-biomarker narrative evidence into the table, not removing conceptual duplication. |
| **4. Identifiability- and uncertainty-aware reconstruction from detection to decision** | Part 5.1 (§7.0) | Part 5 (§7-8), extended into Part 6 (§9) and Part 7 (§10.10) | Figure 3 (reconstruction/uncertainty framework), Table 3 (model-identifiability-validation matrix) | Part 8.2 | This is the contribution with the most internal duplication in the current source: the narrow-posterior-≠-identifiability point (Table 5 cell + §8.9), the validation-levels discussion (§7.5 + §8.16), and the transfer-validation principle (§9.2 + §10.5 + §10.9) are each stated in full 2-3 times — this outline consolidates each to one canonical location (Parts 5.2/5.4 merge point, 5.3 merge point, and 3.3/6.1/7.2 cross-reference chain respectively), per the Overlap Audit's specific line items. |

**No compression action in this outline weakens any of the four contributions' full-strength statement** — every reduction applied to these rows is either (a) removal of a self-acknowledged verbatim restatement (the bridge sections, the narrow-posterior duplication, the transfer-validation triplication), or (b) moving *supporting evidence* (per-study narrative) to a table or SI while keeping the *conceptual claim* in full-strength prose. Where a genuine trade-off exists (Part 4's ~89% compression ratio, Part 5.2's dense method-family survey), it is flagged explicitly in that subsection above rather than silently absorbed.

---

## Figure and table inventory and disposition plan

**Current inventory (counted from the source draft, not estimated):** 3 figures (Fig 1 normalization decision tree, Fig 2 uncertainty chain, Fig 3 uncertainty budget network), 8 numbered tables (Table 1 developmental phases, Table 2 application taxonomy, Table 3 normalization matrix, Table 4 back-calculation method families, Table 5 per-study audit, Table 6 uncertainty source matrix, Table 7 surveillance objective matrix, Table 8 technology-readiness matrix), 4 boxes (Monte Carlo misspecification, nondetect reporting, detectable-vs-actionable, analytical-innovation-vs-epidemiological-value), plus 2 internal-audit tables not intended for submission (the Editorial self-check concept-threading table, and Table 5's methodological role overlaps partially with internal audit purposes).

**Target inventory (per task §9, capped at 4 figures + 4 tables):**

| Current element | Disposition | Target element | Rationale |
|---|---|---|---|
| (none currently — new) | redesign | **Figure 1. Source-to-inference signal chain** | No current figure shows the full §3.0→§9.7 pipeline end-to-end; this is the orienting figure a submission review needs and does not yet have as a single image. |
| (none currently — new, though §3.0's amplitude/temporal/spatial prose could source it) | redesign | **Figure 2. Amplitude-temporal-spatial distortion framework** | Makes the three-term taxonomy visual; currently prose-only. |
| Figure 2 (uncertainty chain) + Figure 3 (uncertainty budget network) | merge | **Figure 3. Process-informed reconstruction and uncertainty framework** | The two current uncertainty figures can likely merge into one framework diagram spanning reconstruction (Ch7) and uncertainty (Ch8) jointly, consistent with Part 5's merged treatment. |
| Figure 1 (normalization decision tree) + Table 8's readiness-level concept + §9.7's four actionability conditions | merge/redesign | **Figure 4. Detection-to-decision readiness pathway** | Consolidates the normalization decision tree, the actionability conditions, and the technology-readiness levels into one "what has to be true before this is decision-ready" pathway figure — the single biggest figure-count saving in this plan (3 source concepts into 1 target figure). |
| Table 1 (developmental phases) | move to SI | — | Background scene-setting, not part of the four contributions. |
| Table 2 (application taxonomy) | move to SI | — | Same reasoning as Table 1. |
| Table 3 (normalization matrix) | retain/redesign | **Table 2. Normalization-assumption-residual-uncertainty matrix** | Already close to the target form; redesign for density (shorter cells, since it must absorb §6.4-6.5's per-biomarker narrative that is being cut from prose). |
| Table 4 (back-calculation method families) + Table 5 (per-study audit) | merge | **Table 3. Model-identifiability-validation matrix** | Both tables already assess the same method families against overlapping criteria; a submission version should merge them into one wider table rather than two, consolidating the five-way-framework columns with the per-study evidentiary columns. |
| Table 6 (uncertainty source matrix) | retain/redesign, tension flagged | *(see note below)* | Table 6 is dense and valuable but creates a 5th-table pressure against the 4-table cap — see the explicit flag below. |
| Table 7 (surveillance matrix) + Table 8 (technology-readiness matrix) + the five scattered minimum-reporting-requirement boxes (§5.7, §6.9, §7.7, §8.15, §9.8) | merge | **Table 4. Minimum reporting and decision-readiness framework** | Consolidates two source tables and five scattered "minimum reporting requirements" prose blocks (currently repeated in similar form at the end of five different chapters) into one framework table — this is simultaneously a figure-count reduction and one of the larger word-count savings in the whole compression plan. |
| Boxes (4 total) | 1-2 retained as in-text callouts (not counted against the figure/table cap), rest cut or merged into table footnotes | — | Boxes are cheap in word count and high in clarity; the "Why Monte Carlo does not solve model misspecification" and "Why analytical innovation does not guarantee epidemiological value" boxes are the two strongest candidates to retain as short callouts given they state Original Contribution #4's core caution in its sharpest form. |
| Editorial self-check concept-threading table | delete | — | Pure internal QA device, not submission content. |

**Explicit tension flagged for author decision:** the disposition plan above already merges 8 tables into 4 and 3 figures into 4 (net: figures grow by one, tables shrink by half), but Table 6 (uncertainty source matrix) does not have an obvious merge partner without either (a) folding it into Table 3, producing one very large, dense table that may itself need SI-level expansion, or (b) accepting a 5th table and asking the author whether Water Research's typical table allowance can absorb it. **This is not resolved in Phase 1** — it is named here as one of the "问题需要作者人工决定" items in the final findings summary, consistent with the instruction that Phase 1 plans the cut without performing it.

---

## Research priorities and conclusions word-count discipline (restated from Part 8, per task §11)

Research priorities is capped at 5-7 independently testable tasks (see Part 8.1's 6-item candidate list, with an optional 7th) and does not expand into an independent Chapter 11. Conclusions is capped at 300-400 words (see Part 8.2) and does not expand into an independent Chapter 12. Both caps are structural constraints on the *target* outline, not yet-drafted prose — no Chapter 11 or Chapter 12 content exists anywhere in this round's deliverables, consistent with the task's explicit instruction not to continue drafting either.
