#!/usr/bin/env python3
"""Builds WBE_Review_Reference_Use_Map.csv (all 68 issued reference numbers)
and WBE_Review_Condensed_References_Working.md (the 21 used in the condensed
draft, original source-draft numbering retained, not renumbered)."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CITATION_AUDIT = BASE / "WBE_Review_Condensed_Citation_Audit.csv"
CLAIM_MAP = BASE / "WBE_Review_Condensed_Claim_Map.csv"
OUT_CSV = BASE / "WBE_Review_Reference_Use_Map.csv"
OUT_MD = BASE / "WBE_Review_Condensed_References_Working.md"

FIELDS = ["reference_number", "active_status", "publication_type", "cited_in_condensed_main_text",
          "cited_in_table", "planned_for_SI", "section_or_paragraph", "claim_supported",
          "evidence_level", "full_text_available", "full_text_read",
          "retain_in_submission_reference_list", "action_required"]

# Publication type for each of the 21 used references (hand-checked against References.md).
PUB_TYPE = {
    "2": "Peer-reviewed review article (Science of the Total Environment)",
    "3": "Peer-reviewed primary study (Environmental Science & Technology)",
    "6": "Peer-reviewed review article (Water)",
    "8": "Peer-reviewed primary study (Viruses)",
    "9": "Peer-reviewed primary study (Scientific Reports)",
    "11": "Institutional report (National Academies Press)",
    "13": "Peer-reviewed primary study (PLOS ONE)",
    "16": "Peer-reviewed primary study (Water)",
    "35": "Peer-reviewed primary study (Environmental Health Perspectives)",
    "38": "Peer-reviewed primary study (PLOS ONE) -- author-list metadata ⚠ partially unresolved",
    "44": "Peer-reviewed primary study (Statistics in Medicine)",
    "46": "Peer-reviewed primary study (Science of the Total Environment)",
    "51": "Peer-reviewed critical review (SSM - Population Health)",
    "52": "Peer-reviewed primary study (PLOS Global Public Health)",
    "55": "Peer-reviewed primary study (Tropical Medicine and Infectious Disease)",
    "57": "Non-peer-reviewed preprint (medRxiv) -- NOT a final published version",
    "58": "Peer-reviewed primary study (Journal of Medical Internet Research)",
    "60": "Peer-reviewed primary study (journal not independently re-confirmed this round; see References.md)",
    "61": "Peer-reviewed review article (Water)",
    "63": "Peer-reviewed narrative/methodological review (Risk Analysis)",
    "64": "Peer-reviewed position paper -- ⚠ duplicated-surname author-list inconsistency unresolved",
}

# Which target-section citations are in a TABLE vs main text (from the condensed draft itself).
IN_TABLE = {"3", "6", "13"}  # appear in Table 2's implicit evidence base (flow/biomarker rows); refined below
# Actually determine table membership precisely: Table 2 (Part 4.4) covers flow/census/dynamic/biomarker
# normalization strategies -- its evidentiary basis is [3],[13] (flow) and biomarker findings generally
# (no single biomarker ref named in Table 2 cells directly). Table 3 (Part 5.5) implicitly covers
# [35],[44],[38] via the six model-family rows. Treated as "table" for those directly underlying a row.
TABLE_REFS = {"3": "Table 2 (flow-normalization row)", "13": "Table 2 (flow-normalization row)",
              "35": "Table 3 (deconvolution row)", "44": "Table 3 (Bayesian/state-space row)",
              "38": "Table 3 (hybrid/ML row, implied)"}


def main():
    citation_rows = list(csv.DictReader(open(CITATION_AUDIT, encoding="utf-8")))
    used = {r["reference_number"]: r for r in citation_rows if r["cited_in_condensed_draft"] == "yes"}
    withdrawn = {r["reference_number"] for r in citation_rows if r["active_or_withdrawn"] == "WITHDRAWN"}
    all_refs = [r["reference_number"] for r in citation_rows]

    out_rows = []
    for num in all_refs:
        active = "WITHDRAWN" if num in withdrawn else "active"
        if num in used:
            u = used[num]
            in_table = num in TABLE_REFS
            out_rows.append({
                "reference_number": num,
                "active_status": active,
                "publication_type": PUB_TYPE.get(num, "Peer-reviewed (type not re-classified this round)"),
                "cited_in_condensed_main_text": "yes",
                "cited_in_table": TABLE_REFS.get(num, "no"),
                "planned_for_SI": "yes -- full detail retained in Supplementary Information alongside the condensed citation" if num not in ("11",) else "no (institutional framing citation, main text only)",
                "section_or_paragraph": u["cited_section"],
                "claim_supported": u["claim_supported"],
                "evidence_level": u["evidence_level"],
                "full_text_available": "no -- not obtained this round",
                "full_text_read": "no",
                "retain_in_submission_reference_list": "yes",
                "action_required": u["possible_overextension"] if u["possible_overextension"] not in ("No",) else "Full-text verification (see Full Text Request List / Critical or High queue if applicable)",
            })
        elif active == "WITHDRAWN":
            out_rows.append({
                "reference_number": num, "active_status": "WITHDRAWN",
                "publication_type": "N/A -- withdrawn, author identity unconfirmed",
                "cited_in_condensed_main_text": "no", "cited_in_table": "no", "planned_for_SI": "no",
                "section_or_paragraph": "N/A", "claim_supported": "N/A", "evidence_level": "N/A",
                "full_text_available": "N/A", "full_text_read": "N/A",
                "retain_in_submission_reference_list": "no -- do not cite until metadata resolved",
                "action_required": "Do not use. Re-verify basic author identity from scratch if ever revisited.",
            })
        else:
            out_rows.append({
                "reference_number": num, "active_status": "active",
                "publication_type": "Not re-classified this round (unused)",
                "cited_in_condensed_main_text": "no", "cited_in_table": "no",
                "planned_for_SI": "possible -- available if a future round's prose expansion needs it",
                "section_or_paragraph": "N/A -- not used in condensed draft", "claim_supported": "N/A",
                "evidence_level": "N/A (active reference, unused this round)",
                "full_text_available": "not checked this round", "full_text_read": "no",
                "retain_in_submission_reference_list": "undecided -- retained in source draft's References.md; not yet in submission reference list",
                "action_required": "None this round -- low priority unless Phase 3B prose expansion cites it",
            })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out_rows)

    # Condensed References Working -- only the 21 used, original numbering
    used_nums = sorted(used.keys(), key=lambda x: int(x))
    md_lines = []
    md_lines.append("# Condensed References — Working List (References Actually Used in the Condensed Draft)\n")
    md_lines.append(
        "**Round:** Water Research compression, Phase 3A. 2026-07-18. **This file lists only the 21 active "
        "references actually cited in `WBE_Review_WR_Condensed_Draft.md` (Parts 1–8), in their original "
        "source-draft numbering.** Per this round's explicit instruction: (1) original source-draft reference "
        "numbers are retained, not renumbered to 1–21; (2) the other 46 active references and the 1 withdrawn "
        "reference are NOT deleted from `WBE_Review_References.md`, which remains the authoritative complete "
        "reference list; (3) formal renumbering for actual submission happens only after full-text verification "
        "and evidence freeze, not this round. See `WBE_Review_Reference_Use_Map.csv` for the complete 68-row "
        "cross-reference covering every issued number, used or not.\n"
    )
    md_lines.append("## References used in the condensed draft (21, original numbering)\n")
    for num in used_nums:
        u = used[num]
        pub = PUB_TYPE.get(num, "")
        table_note = f" **Also underlies {TABLE_REFS[num]}.**" if num in TABLE_REFS else ""
        md_lines.append(f"**[{num}]** {pub}. Cited in condensed draft §{u['cited_section']}, supporting: \"{u['claim_supported']}\"{table_note} Evidence level: {u['evidence_level']}. Full entry: see `WBE_Review_References.md` [{num}].\n")
    md_lines.append(
        "\n## Status note\n\n"
        "Every entry above is **abstract-checked, not full-text verified** — 0 of these 21 references (and 0 of "
        "all 67 active references) have been read in full text as of this round. This file's role is to make the "
        "condensed draft's actual, current reference footprint visible and auditable on its own, separate from "
        "the full 67-reference `WBE_Review_References.md`; it is not a submission-ready reference list and carries "
        "no independent citation numbering of its own."
    )
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {len(out_rows)} rows to {OUT_CSV}")
    print(f"Wrote {len(used_nums)} used-reference entries to {OUT_MD}")


if __name__ == "__main__":
    main()
