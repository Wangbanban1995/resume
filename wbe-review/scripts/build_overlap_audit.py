#!/usr/bin/env python3
"""Builds WBE_Review_Overlap_Audit.csv via csv.writer (not hand-typed quoting,
which is error-prone for long free-text fields containing commas/quotes)."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "WBE_Review_Overlap_Audit.csv"

FIELDS = ["source_section", "overlapping_section", "repeated_concept", "overlap_type",
          "estimated_removable_words", "retain_location", "recommended_action", "rationale"]

ROWS = [
{
"source_section": "End-matter: 6x 'Structural bridge from Chapter X to Chapter Y' sections (lines ~1075-1109)",
"overlapping_section": "Each chapter's own §X.0 'Bridge from Chapter X-1' opening subsection and §X.8/§X.10/§X.16 'Link to Chapter Y' closing subsection (e.g. §5.0, §6.10, §7.0, §7.8, §8.0, §8.16, §9.0, §10.0)",
"repeated_concept": "Chapter-to-chapter handoff logic (what the prior chapter produced, what this chapter does with it, why it matters downstream)",
"overlap_type": "near-verbatim restatement",
"estimated_removable_words": 1200,
"retain_location": "Keep the inline §X.0/§X.y bridge language only (it is load-bearing for a reader moving straight through)",
"recommended_action": "delete_as_redundant",
"rationale": "This is the single largest, most mechanically identifiable redundancy in the document: the same handoff argument is made twice - once inline where a reader actually needs it, and again as a separate end-matter section that restates the same content in the same order. The word count is exact (186+174+130+381+312+278=1,461 words; conservatively 1,200 are pure restatement net of the ~20% that adds genuinely new synthesis). This is pure internal-note bloat (already flagged is_internal_note=True in the word-count audit) and can be cut before touching any Chapters 1-10 scientific prose.",
},
{
"source_section": "§3.0 ('conceptual scaffold, not a computational recipe')",
"overlapping_section": "§5.0, §6.0, §8.0 (each restates 'this equation is a conceptual scaffold, not a validated quantitative model' near-verbatim)",
"repeated_concept": "The standing caveat that this review's formal equations are organizing devices, not fitted/validated models",
"overlap_type": "near-verbatim restatement of the same sentence, 4 times",
"estimated_removable_words": 90,
"retain_location": "State once, in §2 (Review Methodology) or §3.0, as a standing convention covering every subsequent formal expression in the document",
"recommended_action": "merge",
"rationale": "The exact phrase 'conceptual scaffold, not a...' (or its close paraphrase) appears at §3.0 (implied), §5.0 (line 194), §6.0 (line 289), and is referenced again structurally at §8.0. This is deliberate authorial consistency, not an accident, but a submission-length manuscript states a global convention once rather than re-asserting it at every occurrence.",
},
{
"source_section": "§9.2 (alert-threshold transfer caution: a published sensitivity/PPV pair does not transfer to a different population/sewershed)",
"overlapping_section": "§10.5 (cross-city/cross-population AI-model validation failure); §10.9 (climate-region transferability of a correction model)",
"repeated_concept": "Transfer validation as a general requirement - a result calibrated on one setting is not evidence it holds in another",
"overlap_type": "same argument restated in full three times, with different surface examples",
"estimated_removable_words": 350,
"retain_location": "Keep §9.2's full argument as the canonical statement (introduced first and most completely)",
"recommended_action": "shorten",
"rationale": "The document's own Editorial self-check (line ~1067) already names this explicitly as 'the same discipline applied a third time' - the redundancy is self-acknowledged, which makes it a clean, low-risk compression target: the general principle needs one full statement, not three.",
},
{
"source_section": "§7.4 Table 5, Dai et al. (2024) row ('a posterior credible interval... is not, by itself, evidence of structural or practical identifiability')",
"overlapping_section": "§8.9 ('a narrow posterior credible interval is not, by itself, evidence of high true certainty')",
"repeated_concept": "Narrow Bayesian posterior width does not imply parameter/state identifiability was actually achieved",
"overlap_type": "same core claim, stated in near-identical language, in two different chapters",
"estimated_removable_words": 120,
"retain_location": "Keep the full explanation in §8.9 (Chapter 8's central methodological point for that subsection)",
"recommended_action": "shorten",
"rationale": "This is a genuine content duplication, not just a cross-reference: both passages independently explain why a narrow interval can be misleading (overconfident prior vs. genuine data informativeness), rather than one stating it and the other pointing to it.",
},
{
"source_section": "§6.6 (ratio-normalization near-LOD instability, denominator approaching zero)",
"overlapping_section": "§8.6 ('a denominator near zero (§6.6's near-LOD ratio-instability problem, restated here in general form)')",
"repeated_concept": "A ratio's variance blows up as its denominator approaches the detection limit",
"overlap_type": "explicit self-labeled restatement ('restated here')",
"estimated_removable_words": 60,
"retain_location": "Keep §6.6's original treatment",
"recommended_action": "shorten",
"rationale": "The source text literally flags itself as a restatement, which makes this the lowest-risk, highest-confidence line item in this audit - no judgment call required, the document already marked it.",
},
{
"source_section": "§5.5 (Six Concepts That Should Not Be Collapsed Into One 'Uncertainty': representativeness, recovery, precision, sensitivity, censoring, replicates)",
"overlapping_section": "§8.4 (Sampling and Analytical Uncertainty, which re-lists the same six concepts as bullet points 'per the six-concept disambiguation §5.5 already established')",
"repeated_concept": "The six-way sampling/analytical uncertainty taxonomy",
"overlap_type": "list re-stated as bullets a second time rather than referenced",
"estimated_removable_words": 180,
"retain_location": "Keep the full six-concept definitions in §5.5 (their natural home and first-use point)",
"recommended_action": "shorten",
"rationale": "§8.4 explicitly says it 'imports §5.0's...models directly' and then re-lists all six items with descriptions rather than only listing what is new for the uncertainty-propagation context; the definitional content is identical to §5.5, only the propagation-method framing differs.",
},
{
"source_section": "§8.14 (From Scientific Uncertainty to Decision Uncertainty: exceedance probability, asymmetric false-alarm/missed-detection cost, decision thresholds)",
"overlapping_section": "§9.2 (Alert-Threshold Design: 'the asymmetric-cost framing from §8.14 is what should set the threshold')",
"repeated_concept": "Asymmetric cost of false alarms vs. missed detections as the basis for setting a decision threshold",
"overlap_type": "vocabulary introduced in full in one chapter, then substantially re-explained (not just applied) in the next",
"estimated_removable_words": 220,
"retain_location": "Keep §8.14 as the conceptual introduction (decision-relevant probability vs. point estimate)",
"recommended_action": "shorten",
"rationale": "This is a case of appropriate build-on that nonetheless re-explains the underlying decision-theory rationale rather than only applying it - the two sections could share one explanation with two illustrations instead of two explanations.",
},
{
"source_section": "§9's Table 7 caption + §9.7's four actionability conditions ('Proposed by this review... not a published, validated, or institutionally endorsed standard')",
"overlapping_section": "§10's Table 8 caption + §10.10's six-level technology-readiness framework (identical disclaimer sentence, and an explicitly parallel level-based structure)",
"repeated_concept": "This review's own proposed-framework disclaimer, and a leveled-readiness/actionability structure used as an organizing device",
"overlap_type": "same disclaimer sentence reused verbatim; structurally parallel framework (conditions vs. levels) explained in full twice",
"estimated_removable_words": 150,
"retain_location": "Keep both frameworks (they organize genuinely different content); state the 'proposed synthesis, not a validated standard' disclaimer once, in a single upfront statement covering every 'Proposed by this review' table/framework",
"recommended_action": "merge",
"rationale": "Not a case for deleting either framework (§9's and §10.10's frameworks are conceptually distinct, both explicitly required to survive compression), but the boilerplate disclaimer sentence itself is repeated near-verbatim 2+ times (also appears at Table 7, Table 8, and implicitly at the Box captions) and can be centralized.",
},
{
"source_section": "§3.1-3.2 (source-end biological/behavioral variation, building/local drainage)",
"overlapping_section": "§7.1.1, §7.2, §8.2 (source-end uncertainty, shedding-kernel discussion)",
"repeated_concept": "Source-end shedding heterogeneity and its consequences for reconstruction/uncertainty",
"overlap_type": "cross-referenced, not restated - each later chapter adds new material rather than re-explaining the underlying biology",
"estimated_removable_words": 0,
"retain_location": "No action needed - retain as-is",
"recommended_action": "retain",
"rationale": "Checked specifically per the compression-planning brief's instruction to examine this pair. Ch7 and Ch8 both cite §3.1 tersely ('per §3.1's discussion of...') rather than re-describing shedding heterogeneity; this is the document's cross-referencing discipline working as intended, not a compression opportunity. Flagged here as a negative finding so the audit is not read as having skipped this required check.",
},
{
"source_section": "§4.1-4.3 (sewer transport: physical/chemical/biological transformation, rainfall/warm-season distortion, identifiability)",
"overlapping_section": "§7 (back-calculation), specifically the CSO-mass-loss and decay-rate references",
"repeated_concept": "Transport-stage distortion mechanisms as inputs to reconstruction",
"overlap_type": "cross-referenced only, never re-explained",
"estimated_removable_words": 0,
"retain_location": "No action needed - retain as-is",
"recommended_action": "retain",
"rationale": "Checked specifically per the compression-planning brief's instruction to examine this pair. Same finding as the Ch3/Ch7 pair: Chapter 7 treats Chapter 4's mechanisms as established background to be pointed at, not restated. This pair is not a compression opportunity.",
},
{
"source_section": "§5.1-5.7 (sampling location/mode/matrix, six-concept disambiguation, bias/error/information-loss classification)",
"overlapping_section": "§6.2-6.6 (flow/population/biomarker normalization, ratio normalization and error propagation)",
"repeated_concept": "Sampling- and analytical-stage error entering the normalization ratio's numerator and denominator",
"overlap_type": "partial, appropriate build-on - §6.6 extends §5.5's precision/recovery distinctions to a ratio's denominator rather than re-deriving them, but restates the LOD-proximity consequence in slightly different words",
"estimated_removable_words": 90,
"retain_location": "Keep as-is structurally (§6.6's ratio-specific argument is genuinely new content, not a restatement)",
"recommended_action": "shorten",
"rationale": "Checked specifically per the compression-planning brief's instruction to examine this pair. Overlap here is modest and mostly appropriate (Chapter 6 is supposed to build on Chapter 5's error taxonomy) - this is the pair with the least real redundancy of the six the brief named, aside from the one LOD-proximity clause also caught under the §6.6/§8.6 row above.",
},
{
"source_section": "Front-matter status note (top of document) - full four-tier metadata/abstract/full-text/claim definition",
"overlapping_section": "§9's chapter-opening status note (full restatement, 'restated from the top-of-document notice because it matters more here'); §10's chapter-opening status note (shorter restatement)",
"repeated_concept": "The four-tier evidentiary-confidence vocabulary (metadata verified / abstract-snippet checked / full-text verified / claim verified)",
"overlap_type": "definition restated in full at least twice (front matter, §9), summarized a third time (§10)",
"estimated_removable_words": 140,
"retain_location": "Keep the front-matter definition as canonical; keep §9's restatement (explicitly justified in-text, 'because it matters more here')",
"recommended_action": "shorten",
"rationale": "Lower-priority than the other rows - §9's restatement is explicitly justified in-text rather than accidental - but still real word count that a length-constrained submission version cannot fully retain in triplicate.",
},
{
"source_section": "Repeated 'X should not be collapsed into / conflated with Y' framing device",
"overlapping_section": "Appears independently at §5.5 (six concepts), §6.1 (normalization-intent framing), §7.0 (five distinctions), §8.1 (variability/uncertainty/bias/information-loss), §8.11 (censoring/missingness categories)",
"repeated_concept": "The rhetorical device of enumerating several superficially-similar concepts and insisting they not be collapsed into one",
"overlap_type": "stylistic pattern repeated 5 times with genuinely different content each time - not a content duplication, but a structural one",
"estimated_removable_words": 0,
"retain_location": "No word-count action - deliberate, effective rhetorical consistency device, not redundant content",
"recommended_action": "retain",
"rationale": "Included because the instruction asked for recurring disclaimers and 'not equal to'-style sentence patterns specifically. Each instance introduces a different concept set - this is a repeated structure, not repeated content, so no words are double-counted here; flagged for the author's awareness that Phase 2 prose tightening could vary the phrasing even where the underlying distinction-drawing device is kept in all five places.",
},
]

def main():
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    print(f"Wrote {len(ROWS)} rows to {OUT}")
    total = sum(r["estimated_removable_words"] for r in ROWS)
    print(f"Total estimated removable words across all rows: {total}")

if __name__ == "__main__":
    main()
