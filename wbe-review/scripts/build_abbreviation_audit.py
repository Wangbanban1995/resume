#!/usr/bin/env python3
"""Builds WBE_Review_Abbreviation_Audit.csv by checking every capitalized
abbreviation actually found in WBE_Review_WR_Condensed_Draft.md against:
first-use definition, duplicate definitions, multiple abbreviations for the
same concept, single-use candidates for removal, and table/text consistency.
Findings are hand-verified against the draft text, not inferred from the
abbreviation string alone."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "WBE_Review_Abbreviation_Audit.csv"

FIELDS = ["abbreviation", "expansion", "first_occurrence_section", "occurrence_count",
          "defined_at_first_use", "duplicate_definition", "multiple_abbreviations_for_concept",
          "single_use_candidate_for_removal", "table_text_consistency", "notes", "recommended_action",
          "fix_applied_this_round"]

ROWS = [
    {"abbreviation": "WBE", "expansion": "wastewater-based epidemiology",
     "first_occurrence_section": "Title; §1.1 (line 9)", "occurrence_count": "6",
     "defined_at_first_use": "Yes -- \"Wastewater-based epidemiology (WBE)\" at first use in §1.1",
     "duplicate_definition": "No", "multiple_abbreviations_for_concept": "No",
     "single_use_candidate_for_removal": "No -- used 6 times, warrants the abbreviation",
     "table_text_consistency": "N/A -- not used in Table 2/Table 3",
     "notes": "Correctly defined and consistently used throughout.",
     "recommended_action": "None -- already correct", "fix_applied_this_round": "N/A -- no fix needed"},
    {"abbreviation": "RNA", "expansion": "ribonucleic acid",
     "first_occurrence_section": "§1.1 (line 9, \"viral RNA loss\")", "occurrence_count": "3",
     "defined_at_first_use": "No -- used unexpanded from first occurrence",
     "duplicate_definition": "N/A (never defined)", "multiple_abbreviations_for_concept": "No",
     "single_use_candidate_for_removal": "No -- used 3 times",
     "table_text_consistency": "N/A -- not used in Table 2/Table 3",
     "notes": "RNA is a near-universal life-science abbreviation; many journals exempt it from first-use definition. Water Research's exact house style on this was not checked this round.",
     "recommended_action": "Low priority -- confirm Water Research's abbreviation-exemption list at final formatting; define as \"ribonucleic acid (RNA)\" at first use only if the journal does not exempt it", "fix_applied_this_round": "Yes -- defined at first use in §1.1 as a precaution, pending final house-style confirmation"},
    {"abbreviation": "PMMoV", "expansion": "Pepper Mild Mottle Virus",
     "first_occurrence_section": "§4.3 (line 97)", "occurrence_count": "1",
     "defined_at_first_use": "No -- used unexpanded",
     "duplicate_definition": "N/A (never defined)", "multiple_abbreviations_for_concept": "No",
     "single_use_candidate_for_removal": "No -- it is a specific named biomarker, not a generic term with a plain-language substitute",
     "table_text_consistency": "N/A -- not used in Table 2/Table 3 (Table 2's biomarker row is generic, does not name PMMoV specifically)",
     "notes": "A specific, commonly-used WBE biomarker name; readers in this specific sub-field will recognize it, but a Water Research general readership may not.",
     "recommended_action": "Define at first use: \"Pepper Mild Mottle Virus (PMMoV)\"", "fix_applied_this_round": "Yes -- §4.3 now reads \"Pepper Mild Mottle Virus (PMMoV) and crAssphage...\""},
    {"abbreviation": "PRISMA", "expansion": "Preferred Reporting Items for Systematic Reviews and Meta-Analyses",
     "first_occurrence_section": "§1.2 (line 15, \"PRISMA-ScR\")", "occurrence_count": "2 (\"PRISMA-ScR\", \"PRISMA flow diagram\")",
     "defined_at_first_use": "No -- used unexpanded both times",
     "duplicate_definition": "N/A (never defined)", "multiple_abbreviations_for_concept": "No",
     "single_use_candidate_for_removal": "No -- used twice, and specifically to state this review is NOT a PRISMA-compliant scoping review",
     "table_text_consistency": "N/A",
     "notes": "Used only to disclaim the review's own methodology (\"not yet a formal systematic or scoping review... none of which has been performed\"), not to claim PRISMA compliance -- per Phase 3A/3C constraints, no PRISMA numbers are generated or implied anywhere in this manuscript.",
     "recommended_action": "Define at first use: \"PRISMA-ScR (Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews)\"", "fix_applied_this_round": "Yes -- §1.2 now expands PRISMA-ScR at first use"},
    {"abbreviation": "NASEM", "expansion": "National Academies of Sciences, Engineering, and Medicine",
     "first_occurrence_section": "§2 (line 31, citation \"(NASEM, 2023)\")", "occurrence_count": "1",
     "defined_at_first_use": "N/A -- functions as an institutional-author citation key, matching the author-year format of every other citation in this manuscript, not as a running-text abbreviation",
     "duplicate_definition": "N/A", "multiple_abbreviations_for_concept": "No",
     "single_use_candidate_for_removal": "N/A -- it is a citation, not a prose abbreviation",
     "table_text_consistency": "N/A",
     "notes": "The full name \"National Academies of Sciences, Engineering, and Medicine (NASEM)\" is spelled out in WBE_Review_References.md's [11] entry, which is the correct location for this per standard citation practice.",
     "recommended_action": "None -- correct as a citation key; do not expand inline in running prose", "fix_applied_this_round": "N/A -- no fix needed"},
    {"abbreviation": "AI", "expansion": "artificial intelligence",
     "first_occurrence_section": "§8.1 (line 203, research priority 5, \"AI models\")", "occurrence_count": "1",
     "defined_at_first_use": "No -- used unexpanded, and only here",
     "duplicate_definition": "N/A (never defined)",
     "multiple_abbreviations_for_concept": "Yes -- the manuscript's own model-family taxonomy in §5.1/Table 3 never uses \"AI\"; it consistently uses \"machine-learning\" (§5.3, Ai et al. 2022 discussion) and \"hybrid process-informed\" (§5.1, §7.2, Table 3's sixth row). \"AI models\" in the research-priorities list is therefore a one-off term not tied to the manuscript's controlled vocabulary.",
     "single_use_candidate_for_removal": "Yes -- single use, and inconsistent with the rest of the manuscript's terminology",
     "table_text_consistency": "Inconsistent with Table 3's \"Hybrid process-informed\" row label and §5.1's method-family list, which does not use \"AI\" as a category name",
     "notes": "This is a genuine terminology inconsistency, not merely an undefined abbreviation.",
     "recommended_action": "Replace \"AI models\" with \"machine-learning and hybrid process-informed models\" to match the terminology already established in §5.1 and Table 3", "fix_applied_this_round": "Yes -- §8.1 research priority 5 updated"},
]


def main():
    for r in ROWS:
        missing = [f for f in FIELDS if f not in r]
        if missing:
            raise SystemExit(f"Row {r.get('abbreviation')} missing fields: {missing}")
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(ROWS)
    print(f"Wrote {len(ROWS)} rows to {OUT}")
    fixes = [r["abbreviation"] for r in ROWS if r["recommended_action"] != "None -- already correct" and not r["recommended_action"].startswith("None")]
    print(f"Rows recommending a change: {len(fixes)} -> {fixes}")


if __name__ == "__main__":
    main()
