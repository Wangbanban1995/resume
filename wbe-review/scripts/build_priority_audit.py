#!/usr/bin/env python3
"""
Builds WBE_Review_Content_Priority_Audit.csv from a hand-curated judgment
table (PRIORITY, below) joined against the actual current word counts in
WBE_Review_Section_Word_Count.csv, so target-word and compression-ratio
numbers are computed from the real current counts rather than typed by hand
and potentially inconsistent with them.

PRIORITY entries are keyed by (chapter_prefix, section_prefix) substring
match against the word-count CSV's own chapter/section strings, since the
CSV's chapter/section text is long and this keeps the table readable.
Every one of the 105 rows in the word-count CSV must get exactly one match;
the script errors loudly if a row is unmatched or double-matched, so this
file cannot silently drift from the actual document structure.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
WC = BASE / "WBE_Review_Section_Word_Count.csv"
OUT = BASE / "WBE_Review_Content_Priority_Audit.csv"

# (chapter_substring, section_substring, category, supports_throughline,
#  must_retain, compressible_pct, needs_fulltext, si_destination, note)
# supports_throughline in {"yes","partial","no"}; must_retain in {"yes","no"}
# compressible_pct is an integer 0-100 (0 = cannot be shortened further without
# losing the point; not the same as "delete").
P = [
("FRONT_MATTER","Title and status note","Internal audit material","no","no",70,"no","not applicable (deleted/replaced by a short submission-standard evidence statement)","Project-management status note; a submission manuscript needs a one-paragraph evidence-transparency statement, not this document's full internal audit trail."),

("1. Introduction","(chapter preamble)","Core theoretical contribution","yes","yes",15,"no","none","States the inverse-problem framing and the three organizing arguments; this is the paper's thesis statement and must survive compression almost intact."),

("2. Review Methodology","(chapter preamble)","Internal audit material","no","no",100,"no","Supplementary Methods","Empty preamble (0 body words); heading only."),
("2. Review Methodology","2.1 Review type and scope","Internal audit material","no","yes",50,"no","Supplementary Methods (full search-limitation account)","A 1-2 sentence honest-limitations statement is needed in the submission main text; the full narrative-vs-systematic distinction belongs in SI."),
("2. Review Methodology","2.2 Search process","Internal audit material","no","no",70,"no","Supplementary Methods / full search strategy document","Search-process narrative; a submission methods section needs a compressed 2-3 sentence version, full detail belongs in SI alongside the search-strategy file."),
("2. Review Methodology","2.3 Source verification","Internal audit material","no","yes",60,"no","Supplementary Methods","The 0/N full-text-verification disclosure itself must stay in the main text in some compressed form (a journal reviewer needs it); the internal Miura/Kitajima inconsistency anecdote is SI-level detail."),
("2. Review Methodology","2.4 Terminology and developmental background","General background","partial","yes",60,"no","Supplementary Table (developmental phases)","Table 1's 5-phase history is background scene-setting, not part of the four original contributions; compress to 2-3 sentences in main text, full phase table to SI."),
("2. Review Methodology","2.5 Application taxonomy","General background","partial","yes",50,"no","Supplementary Table (application taxonomy)","Table 2 is useful orientation but not load-bearing for the four contributions; shorten substantially."),
("2. Review Methodology","2.6 Scope boundaries","General background","no","yes",40,"no","none","Short scoping statement; keep briefly, low word count already (64 words)."),

("3. WBE as an Inverse Problem","(chapter preamble)","Core theoretical contribution","yes","yes",0,"no","none","Heading-only preamble; no content to compress."),
("3. WBE as an Inverse Problem","3.0 Formal problem statement","Core theoretical contribution","yes","yes",10,"no","none","Defines X(tau), Y(t), A(t), K(t,tau), and the amplitude/temporal/spatial taxonomy — this is contribution #2 (the distortion framework) in its entirety. Must be preserved almost verbatim."),
("3. WBE as an Inverse Problem","3.1 Source-End Biological","Necessary methodological support","yes","yes",35,"no","Supplementary Table (biomarker/source-variability evidence)","Illustrates the framework with real evidence (shedding heterogeneity, PK correction-factor uncertainty); needed as the framework's first worked application but individual study details can compress."),
("3. WBE as an Inverse Problem","3.2 Building and Local Drainage","Detailed example","partial","yes",50,"no","Supplementary Table","Building-scale distortion catalog; useful but lower-priority than source-end and transport chapters — compress to the amplitude/spatial mapping sentence plus one example."),

("4. Signal Distortion in Sewer Transport","(chapter preamble)","Core theoretical contribution","yes","yes",30,"no","none","Short chapter-framing paragraph."),
("4. Signal Distortion in Sewer Transport","4.1 Physical, Chemical, and Biological Transformation","Essential evidence","yes","yes",30,"no","Supplementary Table (decay/transformation evidence)","Direct empirical support for the distortion framework (biofilm decay rate-constant studies); Jung et al./Zhang et al. findings are load-bearing evidence, keep the core finding, compress the mechanistic enumeration."),
("4. Signal Distortion in Sewer Transport","4.2 Rainfall- and Warm-Season-Induced Distortion","Essential evidence","yes","yes",25,"no","Supplementary Table","The Janssens et al. rainfall-correction finding is this review's clearest single piece of evidence that distortion is a correctable, structured bias — central to contribution #3 (normalization as mechanism-specific causal correction). Keep prominently."),
("4. Signal Distortion in Sewer Transport","4.3 Identifiability and the Case for Process-Informed Correction","Core theoretical contribution","yes","yes",10,"no","none","States the identifiability argument and process-informed-correction thesis directly — contribution #2/#3's connective tissue. Must be preserved."),

("5. Sampling, Analytical Methods","(chapter preamble)","Necessary methodological support","partial","no",100,"no","none","Empty preamble, heading only."),
("5. Sampling, Analytical Methods","5.0 Bridge from Chapters 1", "Necessary methodological support","yes","yes",20,"no","none","Defines the two observation models (molecular-target, chemical-biomarker) — necessary scaffolding for everything downstream in Ch5-8. Keep, but the 'conceptual scaffold not validated model' disclaimer can be centralized per the Overlap Audit."),
("5. Sampling, Analytical Methods","5.1 Sampling Location","Necessary methodological support","yes","yes",40,"no","Supplementary Table (sampling design evidence)","Real methodological content but largely standard sampling-design material; compress substantially, keep the spatial-distortion/identifiability link."),
("5. Sampling, Analytical Methods","5.2 Sampling Mode","Necessary methodological support","yes","yes",40,"no","Supplementary Table","Grab-vs-composite distinction; standard content, compress."),
("5. Sampling, Analytical Methods","5.3 Sample Matrix","General background","partial","yes",55,"no","Supplementary Table","Matrix-selection background; keep the matrix-partitioning point that feeds §6.5/§6.6, compress the rest."),
("5. Sampling, Analytical Methods","5.4 Preservation, Pre-Treatment","General background","no","yes",55,"no","Supplementary Methods","Standard lab-methods background, not specific to this review's original contributions; compress heavily."),
("5. Sampling, Analytical Methods","5.5 Six Concepts","Core theoretical contribution","yes","yes",20,"no","Supplementary Table (interlaboratory evidence detail)","The six-concept disambiguation (representativeness/recovery/precision/sensitivity/censoring/replicates) is genuinely original organizing work this review relies on repeatedly (Ch6, Ch8); keep the taxonomy in full, move the Pecson/Ahmed et al. evidence detail to SI."),
("5. Sampling, Analytical Methods","5.6 Differential Behavior Across Target Classes","Necessary methodological support","yes","yes",35,"no","Supplementary Table","Applies the two observation models across target classes; needed but compressible to the core distinction plus one example (Elbait et al. qPCR-vs-metagenomics)."),
("5. Sampling, Analytical Methods","5.7 Carrying Sampling and Analytical Uncertainty Forward","Core theoretical contribution","yes","yes",15,"no","none","The systematic-bias/random-error/information-loss three-way split is used throughout Ch6-8; core organizing contribution, keep in full."),

("6. Normalization","(chapter preamble)","Necessary methodological support","yes","no",100,"no","none","Empty preamble, heading only."),
("6. Normalization","6.0 Normalization Within the Inverse-Problem Framework","Core theoretical contribution","yes","yes",15,"no","none","States contribution #3 directly (normalization as conditional statistical adjustment, not source-state reconstruction) with the 'Normalization ≠ reconstruction' proposition. Must be preserved near-verbatim."),
("6. Normalization","6.1 What Is Normalization Intended to Correct","Core theoretical contribution","yes","yes",20,"no","none","The five-goal taxonomy is original, load-bearing organizing work referenced throughout the rest of the chapter; keep."),
("6. Normalization","6.2 Flow-Based Normalization","Essential evidence","yes","yes",40,"no","Supplementary Table (normalization method evidence)","Real comparative evidence (Langeveld, Rainey, Darling) grounding the normalization-is-conditional thesis; keep the applicability-condition finding, move individual-study detail to SI/Table."),
("6. Normalization","6.3 Census Population and Dynamic Population Estimates","Essential evidence","yes","yes",45,"no","Supplementary Table","Supports the five-goal taxonomy's population-correction goal; compress the Baz-Lomba/Thomas et al. narrative to the core finding."),
("6. Normalization","6.4 Chemical Population Biomarkers","Essential evidence","partial","yes",55,"no","Supplementary Table (biomarker validation matrix)","Detailed per-biomarker narrative (creatinine, cotinine, caffeine, ammonium); the *pattern* (proposed-then-mixed-evidence) is load-bearing, individual biomarker paragraphs are compressible into Table 3, which already exists to hold this detail."),
("6. Normalization","6.5 Microbial and Molecular Population Biomarkers","Essential evidence","partial","yes",55,"no","Supplementary Table (biomarker validation matrix)","Same pattern as §6.4 for PMMoV/crAssphage/HF183; compress narrative into Table 3, which already exists."),
("6. Normalization","6.6 Ratio Normalization and Error Propagation","Core theoretical contribution","yes","yes",10,"no","none","This chapter's stated 'principal original contribution' (the joint-condition proposition for when ratio normalization helps vs. hurts) — the paper's clearest original methodological claim in Chapter 6. Must be preserved in full."),
("6. Normalization","6.7 Target- and Purpose-Specific Normalization","Core theoretical contribution","yes","yes",25,"no","none","The two-dimensional (target-type x purpose) framework is original synthesis; compress the enumeration, keep the framework."),
("6. Normalization","6.8 When Normalization Fails","Core theoretical contribution","yes","yes",20,"no","Supplementary Table","The failure-mode catalog is original and directly supports contribution #3's boundary conditions; keep the taxonomy, the eight bullet items can compress into a table."),
("6. Normalization","6.9 Decision Framework","Core theoretical contribution","yes","yes",15,"no","none","The eight-question decision tree (Figure 1) is an original deliverable explicitly named as a required retained figure; keep the framework, the figure carries most of the content."),
("6. Normalization","6.10 Link to Chapters 7 and 8","Necessary methodological support","yes","no",60,"no","none","Chapter-transition prose; per the Overlap Audit, largely restated by the end-matter Structural Bridge sections. Compress to 2-3 sentences."),

("7. From Normalized Wastewater Signals","(chapter preamble)","Necessary methodological support","yes","no",100,"no","none","Empty preamble, heading only."),
("7. From Normalized Wastewater Signals","7.0 Bridge from Chapter 6","Core theoretical contribution","yes","yes",10,"no","none","States the five-way evidentiary distinction (association/predictive performance/parameter identifiability/state observability/structural adequacy) — this chapter's, and one of the review's, central original contributions. Must be preserved in full."),
("7. From Normalized Wastewater Signals","7.1 Two Reconstruction Goals","Essential evidence","yes","yes",45,"no","Supplementary Table (method-family evidence, extends Table 4/5)","Surveys 9 method families against the five-way framework with real citations; the *application* of the framework to each family is essential, the narrative detail per family (Zuccato, Ramin, Huisman, Dai, McMahan, Ai, Alhassan) is largely already captured in Tables 4-5 and can compress substantially in prose."),
("7. From Normalized Wastewater Signals","7.2 A Worked Illustration","Core theoretical contribution","yes","yes",20,"no","none","Explicitly conceptual (not citing a specific study), demonstrates why the five distinctions come apart; keep as the framework's clarifying example, compress the two-failure-mode walkthrough."),
("7. From Normalized Wastewater Signals","7.3 The Five Distinctions, Developed Formally","Core theoretical contribution","yes","yes",15,"no","none","Full formal development of contribution #4 (identifiability/observability-aware reconstruction); must largely survive compression."),
("7. From Normalized Wastewater Signals","7.4 Evaluating Back-Calculation Method Families","Essential evidence","yes","yes",25,"no","Supplementary Table (expanded Table 5 detail)","Table 4 and Table 5 are named required-retained tables (Model-identifiability-validation matrix); keep both tables, compress the surrounding prose synthesis paragraph."),
("7. From Normalized Wastewater Signals","7.5 Validation","Core theoretical contribution","yes","yes",20,"no","none","The internal/external/mechanistic validation three-way split is original and reused via cross-reference in Ch8/Ch9/Ch10; keep, candidate to MERGE with §8.16 per the Overlap Audit rather than compress independently."),
("7. From Normalized Wastewater Signals","7.6 When State Observability Fails","Core theoretical contribution","yes","yes",25,"no","Supplementary Table","Extends §5.7/§6.8's failure-taxonomy pattern to reconstruction; keep the taxonomy, compress the five bullet explanations."),
("7. From Normalized Wastewater Signals","7.7 Reporting Framework","Necessary methodological support","yes","yes",30,"no","Supplementary checklist (expanded reporting checklist)","One of five chapter-closing reporting-standard devices (§5.7,§6.9,§7.7,§8.15,§9.8); keep a compressed version in main text, full checklist to SI's expanded reporting checklist."),
("7. From Normalized Wastewater Signals","7.8 Link to Chapter 8","Necessary methodological support","yes","no",60,"no","none","Chapter-transition prose, largely restated in end-matter Structural Bridge section; compress."),

("8. Uncertainty Propagation","(chapter preamble)","Core theoretical contribution","yes","yes",20,"no","none","States the chapter's framing (uncertainty entering/interacting/propagating, not a catalog)."),
("8. Uncertainty Propagation","8.0 Uncertainty Within the Complete Inverse Pipeline","Core theoretical contribution","yes","yes",15,"no","none","The marginalization integral and 'propagation ≠ bias correction ≠ identifiability restoration' distinction is contribution #4's formal core; must be preserved."),
("8. Uncertainty Propagation","8.1 Variability, Uncertainty, Bias, and Information Loss","Core theoretical contribution","yes","yes",20,"no","none","Eight-way uncertainty-type taxonomy used throughout the rest of the chapter; keep."),
("8. Uncertainty Propagation","8.2 Source-End Uncertainty","Essential evidence","yes","yes",40,"no","Supplementary Table (Table 6 already holds most of this)","Distributional treatment of §3.1's qualitative claims; Table 6 already consolidates this, so prose can compress substantially without losing content."),
("8. Uncertainty Propagation","8.3 Sewer-Process Uncertainty","Essential evidence","yes","yes",40,"no","Supplementary Table (Table 6)","Same pattern as §8.2 — Table 6 already holds the consolidated version; compress prose."),
("8. Uncertainty Propagation","8.4 Sampling and Analytical Uncertainty","Necessary methodological support","yes","yes",50,"no","Supplementary Table (Table 6)","Per the Overlap Audit, this section re-lists §5.5's six concepts rather than only referencing them; largest single compression opportunity in Chapter 8 alongside Table 6 redundancy."),
("8. Uncertainty Propagation","8.5 Normalization Uncertainty","Core theoretical contribution","yes","yes",25,"no","none","The target/normalizer non-independence point is a genuinely new addition beyond §6.6 (not just a restatement); keep, moderate compression only."),
("8. Uncertainty Propagation","8.6 Analytical Error Propagation and the Delta Method","Necessary methodological support","yes","yes",30,"no","Supplementary Methods (formal propagation methods)","Standard method exposition; keep the applicability-conditions point (original framing), compress the general delta-method explanation which is textbook material."),
("8. Uncertainty Propagation","8.7 Monte Carlo Propagation","Essential evidence","yes","yes",30,"no","Supplementary Methods","Real WBE-specific MC studies (Jones, Pei, Croft) plus original critique of common misuse; keep the critique, compress the method description and study narrative."),
("8. Uncertainty Propagation","8.8 Global Sensitivity Analysis","Necessary methodological support","no","yes",50,"no","Supplementary Methods","Largely standard sensitivity-analysis-methods taxonomy (OAT/Morris/Sobol/PRCC/VoI); compress to the one original point (sensitivity ≠ uncertainty contribution)."),
("8. Uncertainty Propagation","8.9 Bayesian Hierarchical Uncertainty Propagation","Core theoretical contribution","yes","yes",25,"no","none","The narrow-posterior-≠-certainty critique is central and reused via cross-reference in Ch7 Table 5 and Ch9; keep, but per the Overlap Audit this is the canonical location — the Table 5 cell should shorten instead."),
("8. Uncertainty Propagation","8.10 Correlated and Dependent Uncertainties","Core theoretical contribution","yes","yes",15,"no","none","Explicitly named as 'this chapter's most consequential subsection'; the 7 named dependencies are original synthesis. Keep in full, compress only the per-dependency one-line explanations."),
("8. Uncertainty Propagation","8.11 Censoring, Nondetects, and Missingness","Essential evidence","yes","yes",35,"no","Supplementary Methods (censoring-methods box already exists)","Safford et al. head-to-head comparison is genuine WBE-specific comparative evidence; keep the finding, the box already summarizes the practical guidance so prose can compress."),
("8. Uncertainty Propagation","8.12 Structural Uncertainty and Model Ensembles","Core theoretical contribution","yes","yes",20,"no","none","Explains why Monte Carlo alone cannot address structural uncertainty — central to contribution #4; keep, moderate compression."),
("8. Uncertainty Propagation","8.13 Uncertainty Decomposition Across the WBE Chain","Core theoretical contribution","yes","yes",15,"no","none","The law-of-total-variance decomposition and the 'uncertainty budget' (Figure 3) is a named original deliverable; keep in full."),
("8. Uncertainty Propagation","8.14 From Scientific Uncertainty to Decision Uncertainty","Core theoretical contribution","yes","yes",15,"no","none","Introduces the decision-theoretic vocabulary reused in Ch9; canonical location per the Overlap Audit (§9.2 should shorten instead). Keep in full."),
("8. Uncertainty Propagation","8.15 Minimum Reporting Requirements","Necessary methodological support","yes","yes",30,"no","Supplementary checklist","One of five chapter-closing reporting-standard devices; compress to main text summary, full list to SI's expanded reporting checklist."),
("8. Uncertainty Propagation","8.16 Link to Validation and Public-Health Interpretation","Core theoretical contribution","yes","yes",25,"no","none","Candidate to MERGE with §7.5 per the Overlap Audit (both address validation) rather than compress independently; conceptually necessary either way."),
("8. Uncertainty Propagation","Table 6.","Essential evidence","yes","yes",5,"no","none","Named required-retained table (Model-identifiability-validation-adjacent; maps to target Table 3, 'Normalization-assumption-residual-uncertainty' family). Keep intact — this is where §8.2-8.4's prose detail should live instead of being duplicated in both places."),
("8. Uncertainty Propagation","Box — Why Monte Carlo Simulation Does Not Solve","Core theoretical contribution","yes","yes",10,"no","none","Sharp, quotable statement of a core original point; boxes are cheap in word count relative to their clarity value, keep."),
("8. Uncertainty Propagation","Box — How to Report Nondetects","Necessary methodological support","yes","yes",15,"no","Supplementary checklist","Practical checklist; keep condensed in main text, full version to SI reporting checklist."),
("8. Uncertainty Propagation","Figure 2 and Figure 3","Core theoretical contribution","yes","yes",10,"no","none","Both figures are named required-retained deliverables (target Figure 3: process-informed reconstruction/uncertainty framework); keep the reference text minimal."),

("9. Integration with Public-Health Surveillance","(chapter preamble)","Internal audit material","no","no",75,"no","not applicable","Chapter-specific evidentiary status note; a submission version needs one sentence, not this full four-tier redefinition (already flagged as partially redundant with front matter in the Overlap Audit)."),
("9. Integration with Public-Health Surveillance","9.0 What Chapter 8 Hands to Chapter 9","Core theoretical contribution","yes","yes",30,"no","none","States the translation-layer framing (epistemic object -> institutional object); compress, largely restated in end-matter bridge section."),
("9. Integration with Public-Health Surveillance","9.1 Three Surveillance Objectives, One Signal","Core theoretical contribution","yes","yes",20,"no","none","Trend/anomaly/absolute-magnitude as three institutional design problems is original and load-bearing for the rest of Ch9; keep."),
("9. Integration with Public-Health Surveillance","9.2 Alert-Threshold Design","Essential evidence","yes","yes",35,"no","Supplementary Table","The Link/Garrido detection-performance example and the transfer-validation caution are essential; per the Overlap Audit this is the canonical transfer-validation statement (§10.5/§10.9 should shorten instead). Compress the case-study narrative, keep the general point."),
("9. Integration with Public-Health Surveillance","9.3 Multi-Source Data Fusion","Essential evidence","yes","yes",35,"no","Supplementary Table","The weather-double-role point (confounder AND corroborating stream) is original and important; keep, compress the general fusion-rationale narrative."),
("9. Integration with Public-Health Surveillance","9.4 Why Fusion Is Not Free","Core theoretical contribution","yes","yes",20,"no","none","Extends §8.10's correlated-uncertainty argument to cross-stream fusion; original and needed, keep with light compression."),
("9. Integration with Public-Health Surveillance","9.5 The Boundary","Core theoretical contribution","yes","yes",25,"no","Supplementary Table (non-sewered-population evidence)","States WBE's structural exclusion of non-sewered populations, a required focus area per the compression brief's original Ch9 audit; keep the boundary statement, compress the Yu et al. demographic detail to SI."),
("9. Integration with Public-Health Surveillance","9.6 Small-Catchment and Building-Scale Monitoring","Core theoretical contribution","yes","yes",25,"no","Supplementary Table (equity-framework evidence)","Privacy/re-identification/stigma/equity — required focus areas; keep the three-part distinction, compress individual-source detail (Moallef, Kwiatkowska, Thompson) to SI."),
("9. Integration with Public-Health Surveillance","9.7 From Detectable Signal to Actionable Information","Core theoretical contribution","yes","yes",15,"no","none","The four detectable-to-actionable conditions are a named, explicitly-protected original framework; must be preserved in full."),
("9. Integration with Public-Health Surveillance","9.8 Minimum Reporting Requirements","Necessary methodological support","yes","yes",30,"no","Supplementary checklist","Fifth of the chapter-closing reporting-standard devices; compress to main text summary, full checklist to SI."),
("9. Integration with Public-Health Surveillance","Table 7.","Core theoretical contribution","yes","yes",10,"no","none","Named required-retained table; keep intact, it is this chapter's principal organizing deliverable."),
("9. Integration with Public-Health Surveillance","Box — \"Detectable\" Is Not \"Actionable\"","Core theoretical contribution","yes","yes",15,"no","none","Sharp restatement of the four-condition framework; keep, cheap in word count relative to clarity value."),
("9. Integration with Public-Health Surveillance","9.9 Evidentiary Note","Internal audit material","no","no",90,"no","not applicable","Citation-withdrawal documentation; internal evidentiary bookkeeping, not review content. Cut from submission draft entirely, retained only in the project's internal audit files."),

("10. Enabling Technologies","(chapter preamble)","Internal audit material","no","no",70,"no","not applicable","Chapter-specific evidence-discipline status note plus the Schang/Moore citogenesis note; the citogenesis catch is a nice methods-transparency anecdote but is SI/cover-letter material, not main-text review content."),
("10. Enabling Technologies","10.0 What Chapter 9 Hands to Chapter 10","Core theoretical contribution","yes","yes",30,"no","none","States the upstream-vs-downstream boundary between Ch9 and Ch10; compress, largely restated in end-matter bridge section."),
("10. Enabling Technologies","10.1 Distributed Sewer-Network Sensing","Essential evidence","yes","yes",35,"no","Supplementary Table (Table 8 already holds a version of this)","Schang et al. passive-sampling evidence plus the spatial-resolution/signal-stability trade-off (original framing); keep the trade-off statement, compress narrative, Table 8 already consolidates."),
("10. Enabling Technologies","10.2 Near-Real-Time and Online Measurements","Essential evidence","partial","yes",45,"no","Supplementary Table","Sharma et al. biosensor result with an explicit low-TRL classification; keep the TRL classification (supports contribution re: technology-readiness discipline), compress the study narrative."),
("10. Enabling Technologies","10.3 Sewer Digital Twins","Essential evidence","partial","yes",45,"no","Supplementary Table","Bam et al. digital-twin synthesis; keep the 'process-constraint-generating tool, not a validated source signal' distinction (original), compress narrative."),
("10. Enabling Technologies","10.4 Multi-Omics and Expanded Biomarker Panels","Essential evidence","partial","yes",45,"no","Supplementary Table","Malcom & Bowes AMR review; keep the interpretability/reference-database/batch-effect three-challenge framing, compress narrative."),
("10. Enabling Technologies","10.5 Process-Informed Artificial Intelligence","Core theoretical contribution","yes","yes",30,"no","Supplementary Table","Temporal-leakage/cross-population-failure cautions extend the transfer-validation principle; per the Overlap Audit, shorten in favor of §9.2's canonical statement, keep the two named failure modes."),
("10. Enabling Technologies","10.6 Standard Reference Materials","Essential evidence","partial","yes",45,"no","Supplementary Table","Keenum et al. position-paper synthesis, including the flagged author-list inconsistency; keep the standardization-as-precondition argument, compress narrative, keep the flag as a citation-hygiene note in SI not main text."),
("10. Enabling Technologies","10.7 Interoperable Data Infrastructure","Detailed example","partial","yes",50,"no","Supplementary Table","Therrien et al. data-model synthesis plus this review's own reference-management anecdotes (Hsu et al. ambiguity); the self-referential framing is a nice rhetorical device but is compressible — keep the four interoperability requirements, compress the narrative justification."),
("10. Enabling Technologies","10.8 Privacy-Preserving and Equitable Analytics","Essential evidence","partial","yes",45,"no","Supplementary Table","Wang et al. federated-learning example, explicitly non-WBE-scoped; keep the federated-vs-differential-privacy distinction and the 'technical privacy ≠ governance/equity' point, compress narrative."),
("10. Enabling Technologies","10.9 Climate-Resilient WBE Infrastructure","Core theoretical contribution","yes","yes",25,"no","none","Deliberately citation-light, connects Ch4/Ch8 forward; keep as the third transfer-validation instance, shorten per the Overlap Audit."),
("10. Enabling Technologies","10.10 A Technology-Readiness Framework","Core theoretical contribution","yes","yes",15,"no","none","The six-level TRL framework and the analytical-novelty/field-demonstration/operational-readiness distinction is this chapter's principal original deliverable; keep in full."),
("10. Enabling Technologies","Table 8.","Core theoretical contribution","yes","yes",10,"no","none","Named required-retained table; keep intact."),
("10. Enabling Technologies","Box — Why Analytical Innovation Does Not Guarantee","Core theoretical contribution","yes","yes",15,"no","none","Sharp restatement of the TRL framework's central caution; keep."),

("Note on companion files","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Pure project-file-management content; not review text at all. Remove entirely from submission draft (replaced by a short data/code-availability statement)."),
("Editorial self-check","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Author-requested internal audit device (concept-threading table); valuable for this project's own QA, not submission content. Remove entirely."),
("Structural bridge from Chapters 1","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §5.0 bridge per the Overlap Audit; remove entirely, not merely compress."),
("Structural bridge from Chapter 5 to Chapter 6","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §6.0 bridge per the Overlap Audit; remove entirely."),
("Structural bridge from Chapter 6 to Chapter 7","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §7.0 bridge per the Overlap Audit; remove entirely."),
("Structural bridge from Chapter 7 to Chapter 8","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §8.0 bridge per the Overlap Audit; remove entirely."),
("Structural bridge from Chapter 8 to Chapter 9","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §9.0 bridge per the Overlap Audit; remove entirely."),
("Structural bridge from Chapter 9 to Chapter 10","(chapter preamble)","Internal audit material","no","no",100,"no","not applicable","Redundant with inline §10.0 bridge per the Overlap Audit; remove entirely."),
]

def main():
    rows = list(csv.DictReader(open(WC)))
    used = [False] * len(P)
    out_rows = []
    for r in rows:
        matches = [i for i, (cp, sp, *_rest) in enumerate(P) if cp in r["chapter"] and sp in r["section"]]
        if len(matches) != 1:
            raise SystemExit(f"Match error ({len(matches)} matches) for chapter={r['chapter']!r} section={r['section']!r}")
        i = matches[0]
        used[i] = True
        cp, sp, category, throughline, retain, compress_pct, fulltext, si_dest, note = P[i]
        current_words = int(r["section_total_words"])
        target_words = round(current_words * (100 - compress_pct) / 100)
        out_rows.append({
            "chapter": r["chapter"], "section": r["section"], "current_words": current_words,
            "priority_category": category, "supports_original_throughline": throughline,
            "must_retain_in_main_text": retain, "compressible_pct": compress_pct,
            "target_words": target_words, "needs_fulltext_verification": fulltext,
            "si_destination": si_dest, "notes": note,
        })
    unused = [i for i, u in enumerate(used) if not u]
    if unused:
        raise SystemExit(f"Unused P entries: {[P[i][:2] for i in unused]}")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    total_current = sum(r["current_words"] for r in out_rows)
    total_target = sum(r["target_words"] for r in out_rows)
    print(f"Rows: {len(out_rows)}")
    print(f"Total current words (all sections): {total_current}")
    print(f"Total target words (all sections, priority-audit estimate): {total_target}")
    print(f"Implied reduction: {total_current - total_target} words ({100*(total_current-total_target)/total_current:.1f}%)")

if __name__ == "__main__":
    main()
