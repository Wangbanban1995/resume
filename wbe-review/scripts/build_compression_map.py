#!/usr/bin/env python3
"""
Builds WBE_Review_Compression_Map.md: a section-level (not chapter-level)
mapping from the current 10-chapter draft to the 8-part target submission
structure, with per-section target words computed (not hand-typed) by
rescaling WBE_Review_Content_Priority_Audit.csv's per-section target_words
so each target part's sub-total lands within the Phase-1 target range the
task specified.

Method: each current section is assigned to exactly one target part (below).
Within a target part, every section that is NOT "Internal audit material"
keeps its priority-audit target_words as a *relative weight*; those weights
are then rescaled (uniformly, within that part only) so the part's total
lands on the midpoint of its assigned target range. Internal-audit-material
sections get 0 target words in the submission body by construction (they
move to SI/removed, per the priority audit's own si_destination column) and
are listed in the map with target_words=0, action=move_to_SI or delete.

This keeps the word arithmetic auditable: nothing here is asserted from
memory, every number is either read from the priority audit or computed by
one explicit rescaling step from it.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
AUDIT = BASE / "WBE_Review_Content_Priority_Audit.csv"
OUT_MD = BASE / "WBE_Review_Compression_Map.md"

TARGET_PARTS = {
    1: ("Introduction and review approach", 900),
    2: ("From population states to wastewater signals", 1000),
    3: ("Sewers as information filters", 1400),
    4: ("Observation and normalization", 1300),
    5: ("Reconstruction, identifiability and uncertainty", 1750),
    6: ("From wastewater signals to public-health action", 1000),
    7: ("Enabling infrastructure and technology readiness", 800),
    8: ("Research priorities and conclusions", 700),
}

# (chapter_substring, section_substring) -> target part number
ASSIGN = {
    ("FRONT_MATTER", "Title and status note"): 1,
    ("1. Introduction", "(chapter preamble)"): 1,
    ("2. Review Methodology", None): 1,  # all §2.x sections -> part 1
    ("3. WBE as an Inverse Problem", None): 2,
    ("4. Signal Distortion in Sewer Transport", None): 3,
    ("5. Sampling, Analytical Methods", None): 4,
    ("6. Normalization", None): 4,
    ("7. From Normalized Wastewater Signals", None): 5,
    ("8. Uncertainty Propagation", None): 5,
    ("9. Integration with Public-Health Surveillance", None): 6,
    ("10. Enabling Technologies", None): 7,
    ("Note on companion files", None): None,   # internal, not mapped to any part
    ("Editorial self-check", None): None,
    ("Structural bridge", None): None,
}


def assign_part(chapter, section):
    for (cp, sp), part in ASSIGN.items():
        if cp in chapter and (sp is None or sp in section):
            return part
    raise SystemExit(f"No assignment for chapter={chapter!r} section={section!r}")


def main():
    rows = list(csv.DictReader(open(AUDIT)))
    for r in rows:
        r["part"] = assign_part(r["chapter"], r["section"])
        r["weight"] = int(r["target_words"])
        r["current_words"] = int(r["current_words"])

    # rescale within each part
    for part_num in TARGET_PARTS:
        part_rows = [r for r in rows if r["part"] == part_num and r["priority_category"] != "Internal audit material"]
        total_weight = sum(r["weight"] for r in part_rows)
        _, budget = TARGET_PARTS[part_num]
        for r in part_rows:
            r["final_target_words"] = round(budget * r["weight"] / total_weight) if total_weight else 0
        for r in rows:
            if r["part"] == part_num and r["priority_category"] == "Internal audit material":
                r["final_target_words"] = 0

    lines = []
    lines.append("# Compression Map — Current Draft (Chapters 1–10) to Target 8-Part Submission Structure\n")
    lines.append("**Round:** Water Research compression, Phase 1 (mapping only — this file plans the cut, it does not perform it). 2026-07-18.\n")
    lines.append("## Method\n")
    lines.append(
        "Every one of the 105 sections tracked in `WBE_Review_Content_Priority_Audit.csv` is assigned to exactly one "
        "of the 8 target parts below (never split across parts, and never left unassigned — this script errors if any "
        "section has no assignment). Within a target part, every non-internal-audit section's priority-audit "
        "`target_words` value is used as a *relative weight*, and those weights are rescaled, once, uniformly within "
        "that part, so the part's total lands exactly on the midpoint of the word-count range specified in the task's "
        "§7 target-length table. This is a computed allocation, not a hand-typed one — re-running "
        "`python3 scripts/build_compression_map.py` regenerates this table deterministically from the priority audit. "
        "Internal-audit-material sections (front matter status note, the 'Note on companion files' and 'Editorial "
        "self-check' end-matter, all six 'Structural bridge' sections, and each chapter's own evidentiary status-note "
        "preamble in Ch9/Ch10) are excluded from the target-word pool entirely and shown with `final_target_words=0`, "
        "`action=move_to_SI` or `delete_as_redundant` per the priority audit's own disposition — they were never "
        "candidates for main-text survival regardless of chapter-part assignment.\n"
    )
    lines.append("## Part budgets (midpoint of the task's §7 target range, used as the rescaling target)\n")
    lines.append("| # | Target part | Budget (midpoint, prose body only) |")
    lines.append("|---|---|---:|")
    for n, (name, budget) in TARGET_PARTS.items():
        lines.append(f"| {n} | {name} | {budget} |")
    lines.append("")
    lines.append(
        "**Note on Part 8 (Research priorities and conclusions):** no current section of Chapters 1-10 maps to Part 8, "
        "because Chapters 11-12 (research gaps, conclusions) have not been drafted yet — this is expected, not an "
        "error, and is why Part 8 does not appear in the section-mapping table below. Its 700-word budget is reserved "
        "for future drafting per `WBE_Review_Target_Outline.md`, and per the task's explicit instruction, Research "
        "priorities is capped at 5-7 testable tasks (not a full Chapter 11) and Conclusions at 300-400 words (not a "
        "full Chapter 12).\n"
    )

    lines.append("## Full section-level mapping (105 rows — every current section, no chapter-level shortcuts)\n")
    lines.append("| Current chapter | Current section | Current words | Target part | Retain/merge/move/delete | Target words | Key claim retained | Evidence status | SI destination |")
    lines.append("|---|---|---:|---|---|---:|---|---|---|")

    def action_for(r):
        if r["priority_category"] == "Internal audit material":
            return "move_to_SI" if r["si_destination"] not in ("not applicable",) else "delete_as_redundant"
        if float(r["compressible_pct"]) >= 50:
            return "merge/shorten"
        return "retain (light compression)"

    for r in rows:
        part_num = r["part"]
        part_name = TARGET_PARTS[part_num][0] if part_num else "— (not part of submission body)"
        target_words = r.get("final_target_words", 0)
        action = action_for(r)
        claim = r["notes"].split(";")[0].split(" — ")[0][:140]
        evidence = "pending full-text verification" if r["needs_fulltext_verification"] == "yes" else "conceptual synthesis / metadata-or-abstract-level (see Evidence Freeze Audit)"
        si = r["si_destination"]
        chapter_short = r["chapter"][:60].replace("|", "/")
        section_short = r["section"][:70].replace("|", "/")
        claim = claim.replace("|", "/")
        lines.append(f"| {chapter_short} | {section_short} | {r['current_words']} | {part_name} | {action} | {target_words} | {claim} | {evidence} | {si} |")

    lines.append("")
    lines.append("## Part-by-part subtotal check (computed, not asserted)\n")
    lines.append("| # | Target part | Sum of final_target_words | Budget midpoint | Match |")
    lines.append("|---|---|---:|---:|---|")
    for n, (name, budget) in TARGET_PARTS.items():
        s = sum(r.get("final_target_words", 0) for r in rows if r["part"] == n)
        if n == 8:
            match = "N/A — Chapters 11-12 (research gaps, conclusions) are not yet drafted in the source document, so there is no current content to map; this budget is reserved for future drafting, not derived from existing text"
        elif s == budget:
            match = "exact (by construction of the rescaling step)"
        else:
            match = f"off by {s - budget} (rounding)"
        lines.append(f"| {n} | {name} | {s} | {budget} | {match}")
    total_current = sum(r["current_words"] for r in rows)
    total_target = sum(r.get("final_target_words", 0) for r in rows)
    lines.append("")
    lines.append(f"**Total current words across all 105 sections: {total_current}.** **Total target prose-body words across the 8 parts: {total_target}.** "
                  f"This is the prose-body reduction only — it excludes Tables, Abstract, Highlights, and References, which are budgeted separately in "
                  f"`WBE_Review_Target_Outline.md` per the task's §7 instruction to cost those out independently.")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Total current: {total_current}, total target: {total_target}")


if __name__ == "__main__":
    main()
