#!/usr/bin/env python3
"""
Phase 2B: extends WBE_Review_Condensed_Claim_Map.csv (built in Phase 2A for
Parts 1-4 only) with:
  (a) four new fields for all existing rows: claim_type, evidence_status,
      citation_support_scope, evidence_gap_priority
  (b) 20 new rows covering Parts 5-8 (drafted this round)

Reads the existing 33-row CSV, applies a per-paragraph-id lookup table of
new-field values (hand-assessed, not inferred by pattern-matching, since
evidence_gap_priority specifically requires judgment about which claims are
quantitative/cross-city/method-comparison/rainfall-temperature-RTD/
normalizer-performance/validation-tier/actionability/equity claims per this
round's instruction), then appends the Part 5-8 rows and rewrites the file.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CSV_PATH = BASE / "WBE_Review_Condensed_Claim_Map.csv"

NEW_FIELDS = ["claim_type", "evidence_status", "citation_support_scope", "evidence_gap_priority"]

# Per-paragraph-id new-field values for the existing 33 Parts 1-4 rows.
EXISTING_EXTRA = {
    "P1-1": ("Motivating/mechanistic argument", "Abstract-checked", "Each cited finding supports only its own narrow claim (no consensus marker; flow sometimes outperforms; biofilm decay significant) -- not generalized beyond that", "Moderate"),
    "P1-2": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- no external citation, this review's own formalization", "Author synthesis, no external citation needed"),
    "P1-3": ("Methodological guidance", "Author conceptual synthesis", "Not applicable -- internal methods statement, no external citation", "Author synthesis, no external citation needed"),
    "P1-4": ("Methodological guidance", "Author conceptual synthesis", "Not applicable -- internal scope statement", "Author synthesis, no external citation needed"),
    "P1-5": ("Original synthesis/proposition", "Author conceptual synthesis", "Not applicable -- this review's own four-proposition thesis statement, no single external source", "Author synthesis, no external citation needed"),
    "P2-1": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- no external citation", "Author synthesis, no external citation needed"),
    "P2-2": ("Empirical finding, evidence-anchored", "Abstract-checked; internally flagged inconsistent (Miura et al.)", "Miura et al. supports only the qualitative shedding-heterogeneity direction, not any specific number (numbers deliberately omitted)", "Moderate"),
    "P2-3": ("Institutional/guidance framing", "Institutional guidance (NASEM)", "NASEM supports the general asymptomatic-capture framing, not a specific quantitative claim", "Low"),
    "P2-4": ("Mechanistic argument, evidence-anchored", "Conceptual synthesis based on preceding process evidence", "General distributional-shape claim, not attributed to one specific study's number", "Moderate"),
    "P2-5": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- phenomenon-level statement, methods deferred to Part 4", "Author synthesis, no external citation needed"),
    "P2-6": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- no external citation for this paragraph", "Low"),
    "P2-7": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- no external citation", "Low"),
    "P2-8": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- this review's own organizing distinction", "Author synthesis, no external citation needed"),
    "P3-1": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- mechanistic restatement of §3.0's formal framework", "Low"),
    "P3-2": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- logical consequence of P3-1's residence-time-distribution definition, no external citation", "Author synthesis, no external citation needed"),
    "P3-3": ("Empirical finding, evidence-anchored", "Abstract-checked", "Zhang et al./Jung et al. support the qualitative biofilm-decay/distance-dependence finding; specific magnitude figures deliberately omitted as pending full-text confirmation", "**Critical** -- rainfall/temperature/RTD-adjacent mechanistic finding, currently only abstract-level"),
    "P3-4": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- logical extension of P3-3's mechanisms to network-level controls, no new external citation", "Author synthesis, no external citation needed"),
    "P3-5": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- logical consequence of established sedimentation/resuspension mechanism, no external citation for this specific paragraph", "Moderate"),
    "P3-6": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable in this specific paragraph -- mechanism description precedes the Janssens et al. citation in the next paragraph", "**Critical** -- rainfall/temperature/RTD core mechanism, evidence follows in P3-7"),
    "P3-7": ("Empirical finding, evidence-anchored", "Abstract-checked", "Janssens et al. genuinely supports the rain-correction-improves-correlation finding at the scale described (large multi-plant program); Guo et al.'s specific temperature threshold is deliberately not restated as a number", "**Critical** -- this review's single strongest rainfall/temperature process-informed-correction evidence anchor, still abstract-level only"),
    "P3-8": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- logical argument from the preceding four subsections", "Author synthesis, no external citation needed"),
    "P3-9": ("Empirical finding, evidence-anchored", "Abstract-checked", "Rainey et al. and Darling et al. each support only their own single-study finding; the 'no universal fixed factor' synthesis is this review's own inference from the pair, not either study's own claim", "**Critical** -- cross-city/cross-hydrologic-condition generalizability claim resting on two single-study abstract-checked findings"),
    "P3-10": ("Original synthesis/proposition", "Author conceptual synthesis", "Not applicable -- this review's own framing statement, closes Part 3", "Author synthesis, no external citation needed"),
    "P4-1": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- standard sampling-design distinction, no external citation in this paragraph", "Low"),
    "P4-2": ("Definitional/framework, evidence-anchored", "Abstract-checked (Pecson et al., referenced qualitatively)", "Pecson et al. supports the interlaboratory-variability finding generally; not cited as supporting the specific six-concept taxonomy itself, which is this review's own", "**High** -- method-performance-comparison-adjacent (interlaboratory variability), currently only qualitatively referenced"),
    "P4-3": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- general measurement-theory point, no external citation", "Low"),
    "P4-4": ("Definitional/framework", "Author conceptual synthesis", "Not applicable -- no external citation used in this paragraph (dynamic-population evidence deliberately not repeated from Part 2)", "Moderate"),
    "P4-5": ("Empirical finding, evidence-anchored", "Abstract-checked", "Rainey et al. and Darling et al. each support only their own single-study/single-condition finding; 'context-dependent, not universal ranking' is this review's own synthesis of the pair", "**Critical** -- normalizer-performance comparison claim, cross-site generalizability implied, currently abstract-level only"),
    "P4-6": ("Empirical finding, evidence-anchored", "Abstract-checked", "Each named biomarker's performance pattern is a single- or few-study finding (Chen et al., Maal-Bared et al., Dhiyebi et al.); 'no biomarker universally validated' is this review's own synthesis across many single-site studies", "**Critical** -- normalizer-performance comparison, the single highest citation-density paragraph in the manuscript, currently abstract-level only"),
    "P4-7": ("Original synthesis/proposition", "Author conceptual synthesis", "Not applicable -- explicitly this review's own principal original claim for this chapter, not sourced to any external study", "Author synthesis, no external citation needed"),
    "P4-8": ("Mechanistic argument", "Conceptual synthesis based on preceding process evidence", "Not applicable -- no external citation, logical consequence of established mechanisms", "Moderate"),
    "P4-9": ("Original synthesis/proposition", "Author conceptual synthesis", "Not applicable -- this review's own central proposition, explicitly protected, not sourced externally", "Author synthesis, no external citation needed"),
    "P4-10": ("Empirical finding, evidence-anchored (table)", "Abstract-checked", "Table cells summarize the same single-study findings named in P4-3 through P4-7; no cell asserts a cross-study consensus beyond what the underlying citations individually support", "**Critical** -- consolidates all of Part 4's normalizer-performance and rainfall/infiltration findings into one table; highest-density evidence-gap location in the manuscript"),
}

# 20 new rows for Parts 5-8, drafted this round.
NEW_ROWS = [
{"target_section": "5.1", "paragraph_id": "P5-1", "condensed_claim": "Five inferential targets (trend, relative change, anomaly, absolute load, prevalence/incidence/consumption/exposure) require different evidentiary bars; trend/anomaly tolerate mere covariance, absolute/prevalence require model correctness.",
 "source_sections": "Ch7 §7.1.2 (three-output distinction, extended to five targets)", "source_references": "none",
 "evidence_level": "Conceptual synthesis (original taxonomy, extending Ch7's three-way distinction to five)", "compression_action": "merge",
 "omitted_detail": "none material -- this is an original extension, not an omission", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "yes -- confirm the extension from three to five targets (adding relative change and splitting prevalence/incidence/consumption/exposure) matches intended scope",
 "claim_type": "Definitional/framework", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- original organizing taxonomy", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "5.1", "paragraph_id": "P5-2", "condensed_claim": "Six reconstruction method families exist on a mechanistic-commitment spectrum; appropriateness depends on inferential target, not popularity; Huisman et al.'s externally-grounded-kernel deconvolution is the clearest state-observability-designed example.",
 "source_sections": "Ch7 §7.1.2, §7.4 (method-family survey, heavily condensed)", "source_references": "Huisman et al. 2022",
 "evidence_level": "Conceptual synthesis, anchored by abstract-checked finding", "compression_action": "shorten",
 "omitted_detail": "Per-study narrative for Zuccato, Ramin, Schoen, Dai, McMahan, Ai, Alhassan (all moved to SI Table S-model-families / expanded Table 3 audit)", "SI_destination": "S7 Reconstruction-model evidence",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Empirical finding, evidence-anchored", "evidence_status": "Abstract-checked", "citation_support_scope": "Huisman et al. genuinely supports the state-observability-design claim for that one study; 'no family satisfies every target' is this review's own synthesis across the full method-family survey", "evidence_gap_priority": "**High** -- method-performance-comparison claim spanning 7+ studies, all still abstract-level"},
{"target_section": "5.2", "paragraph_id": "P5-3", "condensed_claim": "Six concepts distinguished: structural identifiability, practical identifiability, parameter uncertainty, state observability, equifinality, informative data design -- each a genuinely different question.",
 "source_sections": "Ch7 §7.0, §7.3 (five-way distinction, extended with equifinality and informative data design)", "source_references": "none directly cited in this paragraph (general epidemic-modeling-identifiability literature referenced only structurally)",
 "evidence_level": "Conceptual synthesis (original taxonomy)", "compression_action": "merge",
 "omitted_detail": "Liyanage et al. 2025 and Deva et al. 2021's full general (non-WBE) identifiability-literature discussion, moved to SI", "SI_destination": "S7 Reconstruction-model evidence",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Definitional/framework", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable in this paragraph -- the six-concept taxonomy itself is original; general identifiability literature (Liyanage, Deva) supports the individual concept definitions but is not cited inline here", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "5.2", "paragraph_id": "P5-4", "condensed_claim": "Central judgment, argued once: a model may fit while the target state remains non-identifiable; narrow posterior/low error is not by itself evidence of identifiability. Dai et al.'s Bayesian framework illustrates: posterior state estimates without formal observability/synthetic-recovery testing.",
 "source_sections": "Ch7 §7.0 boxed proposition; Ch8 §8.9 (narrow-posterior critique, canonical merge per Overlap Audit)", "source_references": "Dai et al. 2024",
 "evidence_level": "Original synthesis + Abstract-checked illustrative example", "compression_action": "merge",
 "omitted_detail": "The full prior-sensitivity/posterior-predictive-check diagnostic list (moved to SI); the general overconfident-prior-vs-genuine-informativeness mechanism explanation, retained in compressed form only", "SI_destination": "S8 Uncertainty methods and evidence",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Original synthesis/proposition, evidence-illustrated", "evidence_status": "Abstract-checked (Dai et al. illustrative example); Author conceptual synthesis (the central judgment itself)", "citation_support_scope": "Dai et al. supports only the specific claim that no formal observability test was confirmed for that one study; the general 'model may fit while non-identifiable' principle is this review's own, illustrated but not proven by the example", "evidence_gap_priority": "**High** -- model-validation-tier claim, central to Part 5's thesis"},
{"target_section": "5.3", "paragraph_id": "P5-5", "condensed_claim": "Six validation levels distinguished: internal fit, temporal holdout, external site validation, event-based validation, synthetic-state recovery, decision-value validation -- external site validation is where transferability is actually tested.",
 "source_sections": "Ch7 §7.5 (three-level validation, expanded to six) + Ch8 §8.16 (coverage/posterior-predictive-check content merged in per Overlap Audit)", "source_references": "none directly cited in this paragraph",
 "evidence_level": "Conceptual synthesis (original taxonomy, extending Ch7's three-way split)", "compression_action": "merge",
 "omitted_detail": "none material -- extension is original, executes the Overlap Audit's flagged §7.5/§8.16 merge", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "yes -- confirm the three-to-six-level extension (adding event-based, synthetic-state-recovery, decision-value as named levels) matches intended granularity",
 "claim_type": "Definitional/framework", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- original taxonomy", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "5.3", "paragraph_id": "P5-6", "condensed_claim": "Predictive performance != source-state recovery: Ai et al.'s ML model forecasts well with no interpretable parameter or state representation. Validation level reported should match inferential target claimed.",
 "source_sections": "Ch7 §7.1.2, §7.3, §7.4 Table 4 (Ai et al. cell)", "source_references": "Ai et al. 2022",
 "evidence_level": "Abstract-checked (⚠ metadata partially unresolved, same tier as prior use elsewhere in this review)", "compression_action": "shorten",
 "omitted_detail": "The 70/30 train/test split's specific performance-metric figures, deliberately omitted as pending full-text confirmation", "SI_destination": "S7 Reconstruction-model evidence",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Empirical finding, evidence-anchored", "evidence_status": "Abstract-checked", "citation_support_scope": "Ai et al. genuinely supports the no-interpretable-parameter/no-state-representation claim for that specific study design; does not itself claim the general principle this review draws from it", "evidence_gap_priority": "**High** -- model-validation-tier claim"},
{"target_section": "5.4", "paragraph_id": "P5-7", "condensed_claim": "Seven uncertainty sources must be propagated together, not separately: input uncertainty, correlated parameters, ratio uncertainty, censoring/LOD, temporal dependence, structural uncertainty, scenario uncertainty.",
 "source_sections": "Ch8 §8.0-§8.3, §8.5, §8.10-§8.13 (heavily condensed; §8.4's six-concept re-listing cut entirely per Overlap Audit, cross-referenced to Part 4.1 instead)", "source_references": "none directly cited in this paragraph",
 "evidence_level": "Conceptual synthesis (original taxonomy, Original Contribution #4's formal core)", "compression_action": "merge",
 "omitted_detail": "The marginalization-integral formal notation; the full named-dependency list (rainfall-flow, flow-retention-time, etc.) from §8.10, moved to SI Table S5", "SI_destination": "S8 Uncertainty methods and evidence (full Table S5)",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Definitional/framework", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- original taxonomy, Table S5 in SI carries the evidence-anchored version of these sources", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "5.4", "paragraph_id": "P5-8", "condensed_claim": "Three propagation-method families solve different problems: delta method (linear, symmetric), Monte Carlo (nonlinear, resampled, correlation-aware -- Jones et al.'s MCMC excretion-fraction framework as example), Bayesian/ensemble (additionally addresses structural uncertainty).",
 "source_sections": "Ch8 §8.6-§8.9, §8.12 (mechanics condensed to what-each-solves; technical derivations moved to SI per this round's explicit instruction)", "source_references": "Jones et al. 2014",
 "evidence_level": "Conceptual synthesis + Abstract-checked illustrative example", "compression_action": "shorten",
 "omitted_detail": "Full delta-method Jacobian derivation; Monte Carlo procedural steps; Bayesian-model-averaging/scenario-envelope mechanics -- all moved to Supplementary Methods per this round's explicit instruction not to repeat technical mechanics", "SI_destination": "S1 Supplementary Methods; S8 Uncertainty methods and evidence",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Methodological guidance, evidence-illustrated", "evidence_status": "Abstract-checked (Jones et al. illustrative example)", "citation_support_scope": "Jones et al. supports only that one formal Bayesian MCMC framework exists for excretion-fraction uncertainty; general method-family characterization is this review's own", "evidence_gap_priority": "Moderate"},
{"target_section": "5.5", "paragraph_id": "P5-9", "condensed_claim": "Six concepts for defensible inference: calibrated coverage (rarely reported), sensitivity analysis (!= mathematical sensitivity), value of information, uncertainty communication, decision thresholds, irreducible uncertainty.",
 "source_sections": "Ch8 §8.8, §8.14-§8.15 (condensed; canonical location for exceedance-probability/asymmetric-cost vocabulary per Overlap Audit, Part 6.1 shortens instead)", "source_references": "none directly cited in this paragraph",
 "evidence_level": "Conceptual synthesis (original taxonomy)", "compression_action": "merge",
 "omitted_detail": "Full minimum-reporting-requirement checklist (moved to SI expanded reporting checklist)", "SI_destination": "S10 Expanded reporting checklist",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Definitional/framework", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- original taxonomy", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "5.5 / Table 3", "paragraph_id": "P5-10", "condensed_claim": "Table 3 consolidates 6 model families against inferential target, identifiability requirement, dominant uncertainty, minimum validation, and failure mode -- absorbing 4-6 items selected from the former Table 6 per this round's Table-6 disposition decision.",
 "source_sections": "Ch7 Tables 4-5 (method families, per-study audit) + up to 6 selected items from Ch8 Table 6 (uncertainty source matrix)", "source_references": "Zuccato et al. 2008 (implied); Ramin et al. 2017 (implied); Huisman et al. 2022; Dai et al. 2024; McMahan et al. 2021 (implied); Ai et al. 2022 (implied) -- via the six model-family rows",
 "evidence_level": "Abstract-checked (table synthesizes P5-1 through P5-9's paragraphs)", "compression_action": "merge",
 "omitted_detail": "Full Table 4 (8-row method-family evidence table) and Table 5 (10-row per-study audit), and full Table 6 (12-row uncertainty-source matrix) -- consolidated here to 6 rows and 6 columns; full detail in SI Table S5 and S7", "SI_destination": "S7 Reconstruction-model evidence (Tables 4-5 full); S8 Uncertainty methods and evidence (Table S5 full)",
 "full_text_verification_required": "yes", "author_review_required": "yes -- confirm the 6-row/6-column table density does not lose a model family or evidentiary distinction the author considers essential",
 "claim_type": "Empirical finding, evidence-anchored (table)", "evidence_status": "Abstract-checked", "citation_support_scope": "Each row's citation supports only that row's specific study; 'principal failure mode' column entries are this review's own synthesis, not asserted by the cited studies themselves", "evidence_gap_priority": "**Critical** -- highest-density evidence-gap location in Part 5, consolidating method-performance-comparison and validation-tier claims across 6 model families"},
{"target_section": "6.1", "paragraph_id": "P6-1", "condensed_claim": "Three surveillance objectives require different threshold logic; threshold set from asymmetric cost (§5.5), not convention; Link/Garrido's 281-county sensitivity advantage does not establish transferability -- threshold transportability must be re-validated per deployment.",
 "source_sections": "Ch9 §9.1-§9.2 (heavily condensed; asymmetric-cost re-explanation removed per Overlap Audit, references Part 5.5 instead)", "source_references": "Assoum et al. 2023; Link, Garrido et al. 2026",
 "evidence_level": "Abstract-checked", "compression_action": "shorten",
 "omitted_detail": "Full statistical-process-control detection-rule discussion (§9.2's withdrawn-source design-philosophy point, per [56]'s withdrawal, not re-introduced); specific sensitivity 0.82/PPV 0.64 figures retained qualitatively only as 'substantial advantage', not restated as precise numbers", "SI_destination": "S10 Expanded reporting checklist",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Empirical finding, evidence-anchored", "evidence_status": "Abstract-checked", "citation_support_scope": "Link/Garrido genuinely supports the 281-county sensitivity comparison for that one study; 'cannot be assumed transferable' is this review's own inference, explicitly flagged as such in the source draft's own §9.2 argument", "evidence_gap_priority": "**Critical** -- cross-city/cross-population transferability claim, single-study evidence, [57] itself still preprint (non-peer-reviewed)"},
{"target_section": "6.2", "paragraph_id": "P6-2", "condensed_claim": "No stream is ground truth; Zhang et al.'s four-system fusion shows fusion can outperform single streams, but does not automatically remove shared confounding/lag/selection bias; weather is a confounder needing correction, not just a corroborating stream.",
 "source_sections": "Ch9 §9.3-§9.4 (weather's double role, shared-confound and lag-structure fusion-failure mechanisms)", "source_references": "Zhang et al. 2025",
 "evidence_level": "Abstract-checked", "compression_action": "shorten",
 "omitted_detail": "Specific per-system correlation-magnitude and lead/lag figures, deliberately omitted as pending full-text confirmation", "SI_destination": "none (Ch9 has no dedicated SI section named; content is argument-dense per Target Outline's own note)",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Empirical finding + mechanistic argument", "evidence_status": "Abstract-checked (Zhang et al.); Author conceptual synthesis (weather's double role, shared-confound mechanism)", "citation_support_scope": "Zhang et al. supports only that one 4-system fusion study's qualitative finding; the general fusion-failure-mechanism argument is this review's own, illustrated but not proven by that example", "evidence_gap_priority": "**High** -- method-performance-comparison-adjacent (fusion vs. single-stream), single-study evidence"},
{"target_section": "6.3", "paragraph_id": "P6-3", "condensed_claim": "Four actionability conditions govern the detectable-to-actionable gap: uncertainty translated to decision terms, named actor/protocol exists, detection-to-action interval adequate, threshold validated against specific deployment cost.",
 "source_sections": "Ch9 §9.7 (four-condition framework, explicitly protected original)", "source_references": "none directly cited in this paragraph",
 "evidence_level": "Conceptual synthesis (original framework)", "compression_action": "shorten",
 "omitted_detail": "The illustrative box example (§9.7's Box); the ~1-week reporting-timeliness figure, omitted as illustrative-only per source draft's own flag", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Original synthesis/proposition", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- explicitly this review's own protected original framework", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "6.3", "paragraph_id": "P6-4", "condensed_claim": "WBE cannot provide individual diagnosis; non-sewered populations structurally invisible (Yu et al.'s systematic-not-random connectivity finding); three distinct fine-resolution problems: re-identification risk (Moallef et al.'s documented instance), group stigmatization, structural equity.",
 "source_sections": "Ch9 §9.5-§9.6 (three-way privacy/stigma/equity distinction, required to survive compression per Phase 1 Content Priority Audit)", "source_references": "Yu et al. 2024; Moallef et al. 2025",
 "evidence_level": "Abstract-checked (both metadata-verified per Citation Verification Table)", "compression_action": "shorten",
 "omitted_detail": "Yu et al.'s specific ~80% connectivity figure and detailed demographic associations, omitted per source draft's own flag that the qualitative finding is more load-bearing; Kwiatkowska et al. and Thompson et al.'s group-stigmatization-framing detail, moved to SI", "SI_destination": "none (ethics/equity content is argument-dense, not SI-friendly per Target Outline)",
 "full_text_verification_required": "yes", "author_review_required": "no",
 "claim_type": "Empirical finding + ethics/equity framework", "evidence_status": "Abstract-checked (Yu et al., Moallef et al.); Author conceptual synthesis (the three-way distinction itself)", "citation_support_scope": "Yu et al. supports the connectivity-inequity finding specifically for the U.S.; Moallef et al. supports one documented re-identification instance, not a general re-identification-risk rate", "evidence_gap_priority": "**High** -- ethics-and-equity claim with cross-population generalizability implications, U.S.-specific evidence only"},
{"target_section": "7.1", "paragraph_id": "P7-1", "condensed_claim": "Distributed sampling trades spatial resolution for signal stability (Schang et al.'s nested-scale validation); online covariates/near-real-time compress latency but a faster wrong number is not an improvement; digital twins (Bam et al.) are process-constraint generators, not automatic validators; event-responsive monitoring targets scenario uncertainty.",
 "source_sections": "Ch10 §10.1-§10.4 (heavily condensed)", "source_references": "Schang et al. 2021; Bam et al. 2025",
 "evidence_level": "Abstract-checked", "compression_action": "shorten",
 "omitted_detail": "Schang et al.'s specific low-prevalence detection-floor figure (0.03-0.3 cases/10,000), omitted as pending full-text confirmation; Bam et al.'s 147-study synthesis detail, moved to SI; Sharma et al.'s near-real-time biosensor turnaround-time example, cut entirely from Part 7 for space (was in Phase 1 plan)", "SI_destination": "S9 Technology-readiness evidence",
 "full_text_verification_required": "yes", "author_review_required": "yes -- confirm dropping the Sharma et al. biosensor example entirely (not just compressing it) does not lose a required focus area",
 "claim_type": "Empirical finding, evidence-anchored", "evidence_status": "Abstract-checked", "citation_support_scope": "Schang et al. supports the nested-scale early-detection finding for that one study; Bam et al. supports the growing-research-area characterization, not a specific performance claim", "evidence_gap_priority": "Moderate"},
{"target_section": "7.2", "paragraph_id": "P7-2", "condensed_claim": "Hybrid mechanistic-statistical/physics-informed ML (Pagsuyoin et al.) incorporates structure as constraint, not replacement; same transfer requirement as §6.1 applies without modification; temporal-leakage check is minimum requirement; standardization (Keenum et al.) is precondition for cross-site validation.",
 "source_sections": "Ch10 §10.5-§10.7 (temporal-leakage/cross-population failure modes, standardization argument)", "source_references": "Pagsuyoin et al. 2025; Keenum et al. 2024",
 "evidence_level": "Abstract-checked (Keenum et al. ⚠ flagged duplicated-surname author-list inconsistency)", "compression_action": "shorten",
 "omitted_detail": "Full temporal-leakage/cross-population-failure-mode dual explanation (compressed to one sentence, cross-referencing Part 3.5/6.1's transfer-validation principle rather than re-arguing it, per Overlap Audit); Therrien et al.'s data-interoperability detail, cut from Part 7 for space", "SI_destination": "S9 Technology-readiness evidence",
 "full_text_verification_required": "yes", "author_review_required": "yes -- confirm dropping Therrien et al./interoperable-data-infrastructure content entirely (not just compressing it) is acceptable, or whether a one-sentence mention should be restored",
 "claim_type": "Empirical finding + mechanistic argument", "evidence_status": "Abstract-checked", "citation_support_scope": "Pagsuyoin et al. supports the hybrid-model-framing characterization generally; Keenum et al. supports the standardization-as-precondition argument for that one working group's position paper, not a field-wide consensus", "evidence_gap_priority": "**High** -- method-performance/standardization claim with an unresolved author-list flag on its primary citation (Keenum et al.)"},
{"target_section": "7.3", "paragraph_id": "P7-3", "condensed_claim": "A single favorable result is evidence for that level only. Five-level readiness hierarchy retained; core proposition: analytical novelty != epidemiological validity, operational readiness, or demonstrated decision value. No surveyed technology confidently above hierarchy midpoint. Equitable deployment is a readiness dimension, not an afterthought.",
 "source_sections": "Ch10 §10.10 (six-level TRL framework, condensed to five named stages; principal original deliverable)", "source_references": "none directly cited in this paragraph",
 "evidence_level": "Conceptual synthesis (original framework, explicitly protected)", "compression_action": "shorten",
 "omitted_detail": "The full six-level-to-five-stage mapping detail; Table 8's full technology-by-technology readiness assessment, moved to SI; the equitable-deployment extension is new synthesis this round, connecting §10.10's technology-readiness framework to §9.6's equity argument explicitly for the first time", "SI_destination": "S9 Technology-readiness evidence",
 "full_text_verification_required": "no", "author_review_required": "yes -- confirm the six-level-to-five-stage compression (merging levels) and the new equitable-deployment connective sentence match intended emphasis",
 "claim_type": "Original synthesis/proposition", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- explicitly this review's own protected original framework", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "8.1", "paragraph_id": "P8-1", "condensed_claim": "Six testable research priorities, each naming an unresolved question, required design, and expected inferential gain (paired source-sewer-outlet observations; rainfall-event mass-balance experiments; fate-matching studies; synthetic-state recovery tests; cross-city/cross-climate validation; uncertainty-coverage and decision-value trials).",
 "source_sections": "New content, synthesized from gaps documented across Ch3-Ch10 (each priority cites its source gap internally)", "source_references": "none (forward-looking research-gap statements, not evidence-dependent claims)",
 "evidence_level": "Author conceptual synthesis", "compression_action": "merge",
 "omitted_detail": "none -- new content per this round's explicit Part 8.1 instruction, capped at 6 items with no 'more research is needed' boilerplate", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "yes -- confirm these 6 priorities are the correct highest-value set, not merely the first 6 gaps identified",
 "claim_type": "Original synthesis/proposition (forward-looking)", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- research-priority statements, not empirical claims", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "8.2", "paragraph_id": "P8-2", "condensed_claim": "Four original contributions recapped with one implication each; no new claim introduced beyond what Parts 1-7 already established.",
 "source_sections": "New content (no current chapter is a 'conclusions' chapter), recapping Part 1.3's four propositions", "source_references": "none (no citations permitted in Conclusions per this round's explicit instruction)",
 "evidence_level": "Author conceptual synthesis", "compression_action": "merge",
 "omitted_detail": "none -- this is a recap, not a new claim; deliberately introduces nothing beyond Parts 1-7", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Original synthesis/proposition (recap)", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- no citations by instruction", "evidence_gap_priority": "Author synthesis, no external citation needed"},
{"target_section": "8.2", "paragraph_id": "P8-3", "condensed_claim": "The four propositions target one recurring overclaiming failure mode; closing evidentiary gaps stage-by-stage is the review's central contribution; every claim in this synthesis remains pending formal systematic verification.",
 "source_sections": "New content, closing statement", "source_references": "none",
 "evidence_level": "Author conceptual synthesis", "compression_action": "merge",
 "omitted_detail": "none", "SI_destination": "none",
 "full_text_verification_required": "no", "author_review_required": "no",
 "claim_type": "Original synthesis/proposition (recap)", "evidence_status": "Author conceptual synthesis", "citation_support_scope": "Not applicable -- no citations by instruction", "evidence_gap_priority": "Author synthesis, no external citation needed"},
]

ORIGINAL_FIELDS = ["target_section", "paragraph_id", "condensed_claim", "source_sections", "source_references",
                    "evidence_level", "compression_action", "omitted_detail", "SI_destination",
                    "full_text_verification_required", "author_review_required"]
ALL_FIELDS = ORIGINAL_FIELDS + NEW_FIELDS


def main():
    existing = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    for row in existing:
        pid = row["paragraph_id"]
        if pid not in EXISTING_EXTRA:
            raise SystemExit(f"No new-field mapping for existing row {pid}")
        ct, es, css, egp = EXISTING_EXTRA[pid]
        row["claim_type"] = ct
        row["evidence_status"] = es
        row["citation_support_scope"] = css
        row["evidence_gap_priority"] = egp

    all_rows = existing + NEW_ROWS
    for r in all_rows:
        missing = [f for f in ALL_FIELDS if f not in r]
        if missing:
            raise SystemExit(f"Row {r.get('paragraph_id')} missing fields: {missing}")

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ALL_FIELDS)
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r[k] for k in ALL_FIELDS})

    print(f"Wrote {len(all_rows)} rows ({len(existing)} Parts 1-4 + {len(NEW_ROWS)} Parts 5-8) to {CSV_PATH}")
    from collections import Counter
    prio = Counter(r["evidence_gap_priority"].split(" --")[0].replace("**", "") for r in all_rows)
    for k, v in sorted(prio.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
