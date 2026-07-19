#!/usr/bin/env python3
"""Builds WBE_Review_Cross_Reference_Audit.csv -- checks every in-text
section/table/figure/SI pointer in WBE_Review_WR_Condensed_Draft.md against
the manuscript's actual heading structure and WBE_Review_Supplementary_Outline.md's
actual SI section list. Findings are hand-verified against both files, not
inferred from the reference string alone."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "WBE_Review_Cross_Reference_Audit.csv"

FIELDS = ["reference_text", "location_in_draft", "reference_type", "target_exists",
          "target_content_matches_claim", "notes", "status", "fix_applied_this_round"]

ROWS = [
    {"reference_text": "§3.2 (in §3.4, \"Jung et al., 2026, §3.2\")", "location_in_draft": "line 67",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §3.2 exists (\"Transformation, partitioning and biological interactions\")",
     "target_content_matches_claim": "Yes -- §3.2 does cite Jung et al. 2026 for biofilm/decay",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§4 (in §2, \"developed later in this review (§4)\")", "location_in_draft": "line 35",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- Part 4 exists (\"Observation and normalization\")",
     "target_content_matches_claim": "Yes -- §4.2 discusses dynamic/static population correction, matching the pointer's subject (population fluctuation)",
     "notes": "Points to the whole Part rather than the more specific §4.2 -- acceptable style, not an error.", "status": "Valid",
     "fix_applied_this_round": "N/A"},
    {"reference_text": "§5.2 (in §5.1, \"the distinction §5.2 develops formally\")", "location_in_draft": "line 124",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §5.2 exists (\"Identifiability and observability\")",
     "target_content_matches_claim": "Yes -- §5.2 is exactly where observability vs. fit quality is formally distinguished",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§5.4 (in §7.1, \"the scenario uncertainty named in §5.4\")", "location_in_draft": "line 183",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §5.4 exists (\"Uncertainty propagation\")",
     "target_content_matches_claim": "Yes -- §5.4 explicitly names \"scenario uncertainty\" as one of seven propagation-input categories",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§5.5 (in §6.1, \"asymmetric costs... (§5.5)\")", "location_in_draft": "line 165",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §5.5 exists (\"From uncertainty intervals to defensible inference\")",
     "target_content_matches_claim": "Yes -- §5.5 states \"Decision thresholds should be set from the asymmetric costs of false alarms against missed detections\" verbatim",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§6.1 (in §7.2, \"the same... transfer requirement §6.1 sets\")", "location_in_draft": "line 187",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §6.1 exists (\"Surveillance objectives and decision thresholds\")",
     "target_content_matches_claim": "Yes -- §6.1 is where threshold cross-population transportability is discussed",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§6.3 (in §7.1, \"detection-to-action timescale named in §6.3\")", "location_in_draft": "line 183",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §6.3 exists (\"Actionability, limits and ethics\")",
     "target_content_matches_claim": "Yes -- §6.3 names \"the detection-to-action interval\" as one of the four actionability conditions",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "§6.3 (in §7.3, \"structural-equity problem named in §6.3\")", "location_in_draft": "line 191",
     "reference_type": "in-text section pointer", "target_exists": "Yes -- §6.3 exists",
     "target_content_matches_claim": "Yes -- §6.3 names \"structural equity\" explicitly as one of three privacy/equity problems",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Part 2 (in §7.1, \"aleatory variability Part 2 already established\")", "location_in_draft": "line 183",
     "reference_type": "in-text part pointer", "target_exists": "Yes -- Part 2 exists (\"From population states to wastewater signals\")",
     "target_content_matches_claim": "Yes -- Part 2 establishes source-end shedding heterogeneity (aleatory variability)",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Part 3 (in §6.2, \"per Part 3, a direct confounder\")", "location_in_draft": "line 169",
     "reference_type": "in-text part pointer", "target_exists": "Yes -- Part 3 exists (\"Sewers as information filters\")",
     "target_content_matches_claim": "Yes -- §3.4 establishes rainfall as a signal confounder",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Part 3 (in §7.1, \"Part 3's process-informed correction argument\")", "location_in_draft": "line 183",
     "reference_type": "in-text part pointer", "target_exists": "Yes -- Part 3 exists",
     "target_content_matches_claim": "Yes -- §3.5 develops the process-informed-correction argument",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Part 5 (in §4.1, \"Part 5 propagates each through to a final uncertainty estimate\")", "location_in_draft": "line 85",
     "reference_type": "in-text part pointer", "target_exists": "Yes -- Part 5 exists (\"Reconstruction, identifiability and uncertainty\")",
     "target_content_matches_claim": "Yes -- §5.4 is exactly the uncertainty-propagation section this forward-points to",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "\"Supplementary Table S4\" (in §4.4, eight-mode normalization-failure catalog pointer)", "location_in_draft": "line 103 (original)",
     "reference_type": "SI pointer", "target_exists": "No -- WBE_Review_Supplementary_Outline.md has no section or table numbered S4 that covers this content. §S4 in the outline is \"Existing-Review Competition Matrix\" (an unrelated reviewer-differentiation table); the actual eight-mode normalization-failure catalog is §S6a (\"Normalization Failure Modes, Full Catalog\"), which the outline explicitly identifies as this pointer's intended target but which was never assigned a \"Table S4\" label anywhere.",
     "target_content_matches_claim": "No -- mismatch between the number cited in the manuscript and the outline's actual section numbering",
     "notes": "Genuine cross-reference bug, caught this round. The condensed draft and the Supplementary Outline were drafted in different Phase 2B sessions and the pointer text was never checked against the outline's final section numbering.",
     "status": "Fixed", "fix_applied_this_round": "Yes -- §4.4 now reads \"given in Supplementary Section S6a\", matching the outline's actual section label"},
    {"reference_text": "\"Supplementary Methods\" (in §1.2, source-verification-limitation pointer)", "location_in_draft": "line 15",
     "reference_type": "SI pointer", "target_exists": "Yes -- §S1 \"Supplementary Methods\" exists in the outline",
     "target_content_matches_claim": "Yes -- §S1 covers the search-process narrative and source-verification-limitation detail the pointer refers to",
     "notes": "Correct.", "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Table 1 / Table 4 / Table 5 / Table 6 / Figure 1-3 (dropped tables/figures)", "location_in_draft": "N/A -- checked for absence",
     "reference_type": "stale-reference check", "target_exists": "N/A",
     "target_content_matches_claim": "N/A",
     "notes": "Confirmed none of these appear anywhere in the condensed draft body -- no leftover pointer to a table dropped from the main text during compression (Table 1, 4, 5, 6 were all moved to SI per the Compression Map; the condensed draft correctly uses only \"Table 2\" and \"Table 3\" as its two in-text table numbers).",
     "status": "Valid -- no stale references found", "fix_applied_this_round": "N/A"},
    {"reference_text": "Table 2 / Table 3 caption numbering", "location_in_draft": "lines 107, 148",
     "reference_type": "table numbering", "target_exists": "Yes -- exactly two in-text tables, numbered 2 and 3 with no gap or duplicate",
     "target_content_matches_claim": "N/A", "notes": "Sequential and non-duplicated. No prose sentence elsewhere cites \"(Table 2)\" or \"(Table 3)\" parenthetically outside the tables' own captions -- not an error, simply means no additional cross-reference to check for these two.",
     "status": "Valid", "fix_applied_this_round": "N/A"},
    {"reference_text": "Box numbering", "location_in_draft": "N/A", "reference_type": "box numbering",
     "target_exists": "N/A -- no numbered \"Box\" elements exist anywhere in the condensed draft",
     "target_content_matches_claim": "N/A", "notes": "The source draft's two uncertainty boxes were compressed into main prose during Phase 2A/2B and not carried forward as numbered boxes; nothing in the condensed draft refers to a \"Box N,\" so there is no dangling box cross-reference to fix.",
     "status": "N/A -- no boxes in condensed draft", "fix_applied_this_round": "N/A"},
    {"reference_text": "Markdown heading numbers vs. .docx heading numbers", "location_in_draft": "whole document",
     "reference_type": "md/docx consistency", "target_exists": "N/A",
     "target_content_matches_claim": "Yes -- WBE_Review_WR_Condensed_Draft.docx is regenerated directly from the .md via pandoc after every edit this round, so heading text and numbering are identical by construction",
     "notes": "Verified via zipfile inspection of word/document.xml after each regeneration this round (heading text present, no literal '$' artifacts, table elements present).",
     "status": "Valid", "fix_applied_this_round": "N/A -- consistency maintained by the regeneration workflow, not a one-time fix"},
]


def main():
    for r in ROWS:
        missing = [f for f in FIELDS if f not in r]
        if missing:
            raise SystemExit(f"Row {r.get('reference_text')} missing fields: {missing}")
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    print(f"Wrote {len(ROWS)} rows to {OUT}")
    bugs = [r["reference_text"] for r in ROWS if r["status"] == "Fixed"]
    print(f"Genuine cross-reference bugs found and fixed: {len(bugs)} -> {bugs}")


if __name__ == "__main__":
    main()
