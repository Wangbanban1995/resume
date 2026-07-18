#!/usr/bin/env python3
"""Builds WBE_Review_Evidence_Recovery_Plan.md from
WBE_Review_Critical_Claim_Verification_Queue.csv, so the narrative plan and the
machine-readable queue never drift apart -- every per-claim sentence below is
generated from the same CSV row a reader can open directly."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
QUEUE_CSV = BASE / "WBE_Review_Critical_Claim_Verification_Queue.csv"
OUT_MD = BASE / "WBE_Review_Evidence_Recovery_Plan.md"


def claim_block(r):
    lines = []
    lines.append(f"#### {r['paragraph_id']} — §{r['target_section']}")
    lines.append("")
    lines.append(f"> {r['exact_claim']}")
    lines.append("")
    lines.append(f"- **Claim type:** {r['claim_type']}")
    lines.append(f"- **Current reference(s):** {r['current_reference']}")
    lines.append(f"- **Current evidence level:** {r['current_evidence_level']}")
    lines.append(f"- **Current support scope:** {r['current_support_scope']}")
    lines.append(f"- **Identified overextension:** {r['identified_overextension']}")
    lines.append(f"- **Evidence needed:** {r['evidence_needed']}")
    lines.append(f"- **Preferred evidence type / study design:** {r['preferred_evidence_type']}; {r['preferred_study_design']}")
    lines.append(f"- **Minimum number of settings:** {r['minimum_number_of_settings']}")
    lines.append(f"- **Database search concepts:** {r['database_search_concepts']}")
    lines.append(f"- **Candidate search query:** `{r['candidate_search_query']}`")
    lines.append(f"- **Full text required:** {r['full_text_required']}")
    lines.append(f"- **Decision if unresolved:** {r['decision_if_unresolved']}")
    lines.append(f"- **Status:** {r['status']}")
    lines.append("")
    return "\n".join(lines)


def main():
    rows = list(csv.DictReader(open(QUEUE_CSV, encoding="utf-8")))
    p0 = [r for r in rows if r["priority"] == "P0"]
    p1 = [r for r in rows if r["priority"] == "P1"]
    assert len(p0) == 9 and len(p1) == 7, f"Expected 9 P0 + 7 P1, got {len(p0)} + {len(p1)}"

    md = []
    md.append("# Evidence Recovery Plan — Critical and High Claim Verification")
    md.append("")
    md.append(
        "**Round:** Water Research compression, Phase 3A. 2026-07-18. **This document is a readable "
        "narrative wrapper around `WBE_Review_Critical_Claim_Verification_Queue.csv`, not a separate source "
        "of truth.** Every claim block below is generated directly from that CSV's rows; if the two ever "
        "appear to disagree, the CSV is authoritative and this file is stale and should be regenerated via "
        "`scripts/build_evidence_recovery_plan.py`."
    )
    md.append("")
    md.append(
        "**What this document is not:** it is not a completed search, not a full-text verification report, "
        "and not a claim-revision record. It converts the condensed draft's 9 Critical and 7 High evidence "
        "gaps (per `WBE_Review_Condensed_Claim_Map.csv`'s `evidence_gap_priority` column — the authoritative "
        "count; see `WBE_Review_Phase2B_Risk_Log.md`'s Phase 3A addendum for the reconciliation against an "
        "earlier, less precise chat-summary framing) into an executable plan: what to search for, what "
        "evidence would resolve each gap, and what happens if that evidence is never found."
    )
    md.append("")

    md.append("## 1. Priority tiers")
    md.append("")
    md.append(
        "- **P0 (Critical, 9 claims):** the claim map's `Critical` rows — quantitative, mechanistic, or "
        "cross-population conclusions currently resting on single-study, abstract-checked, or otherwise "
        "thin evidence, where an unresolved gap would require a real change to the manuscript's argument "
        "(not just a citation swap) if the evidence cannot be found.\n"
        "- **P1 (High, 7 claims):** the claim map's `High` rows — similar in kind but judged less "
        "load-bearing, or already partly self-hedged in the condensed text.\n"
        "- **P2 (not itemized as individual rows this round):** all remaining quantitative, table-performance, "
        "cross-city/climate/population, model-superiority, normalizer-performance, threshold-transportability, "
        "and ethics/equity/privacy empirical claims not already captured in P0/P1 — i.e., the Moderate-tier "
        "empirical rows in the Claim Map. These are lower urgency than P0/P1 but share the same evidence "
        "thresholds (§2) and should be queued the same way once P0/P1 recovery work is underway.\n"
        "- **P3 (not itemized as individual rows this round):** the remaining Moderate/Low evidence gaps and "
        "the Author-synthesis rows, which by definition need no external citation and are out of scope for "
        "full-text recovery."
    )
    md.append("")

    md.append("## 2. Minimum evidence thresholds by claim type")
    md.append("")
    md.append(
        "These thresholds govern when a Critical or High claim can be marked resolved, and were applied "
        "when drafting each claim's `evidence_needed` / `preferred_evidence_type` fields below:\n\n"
        "- **Quantitative / performance conclusions** (e.g., normalizer performance, model accuracy, "
        "sensitivity/specificity figures) require the original full text, with an explicit sample, scenario, "
        "and method described — an abstract, a search-engine summary, or another review's paraphrase of the "
        "same number does not qualify.\n"
        "- **Cross-city / cross-climate / cross-population conclusions** require either at least two "
        "independent settings, or one study that explicitly tested multiple sites itself; absent that, the "
        "claim must be narrowed to an explicit \"in the studied setting...\" framing rather than presented as "
        "general.\n"
        "- **Mechanistic conclusions** (biofilm transformation, sediment/sewer memory, rainfall-dependent "
        "fate, temperature-sensitive decay) require direct observational or experimental verification of the "
        "mechanism itself. A correlational study cannot be silently upgraded to mechanistic evidence.\n"
        "- **Model / validation conclusions** require that the source actually checked recovery of the "
        "target state (the quantity the model claims to infer), not merely predictive fit to the observed "
        "signal.\n"
        "- **Ethics / equity / privacy conclusions** may draw on guidance documents, ethical analyses, "
        "deployment case studies, or governance research, but each such claim must be tagged as one of: a "
        "normative recommendation, a documented empirical harm, or a theoretical/anticipated risk. A "
        "guidance document's existence does not by itself prove a risk has actually occurred."
    )
    md.append("")

    md.append("## 3. [57] (Link, Garrido, et al. 2026) handling this round")
    md.append("")
    md.append(
        "Per this round's instruction, one of three options was to be applied to the single-preprint claim "
        "at §6.1 (P6-1): (A) find a formal peer-reviewed version and record the version relationship without "
        "auto-replacing; (B) find independent second evidence from a different team or scenario; (C) if "
        "neither is available this round, narrow the text to an explicit \"a recent preprint suggests/reports...\" "
        "framing with single-study, non-peer-reviewed, and scenario-limited caveats, and, if the specific "
        "\"281-county\" figure is not essential to the argument, prioritize removing that number while keeping "
        "the general threshold-transfer question.\n\n"
        "**No new formal-version or independent second-source search was run this round** (this round has no "
        "environment access to Web of Science, Scopus, or PubMed — see `WBE_Review_Targeted_Search_Addendum.md`, "
        "which is search-reinforcement design only, not an executed search), so Options A and B were not available. "
        "**Option C was applied directly to `WBE_Review_WR_Condensed_Draft.md` §6.1**: the sentence was edited "
        "from a load-bearing \"an event-detection framework evaluated across 281 U.S. counties reports...\" "
        "framing to an explicitly hedged \"a recent preprint reports a sensitivity advantage... across a large "
        "U.S. county sample..., but this is a single, non-peer-reviewed study set in one national context...\" "
        "framing, with the specific 281-county figure removed as non-essential to the general "
        "threshold-transportability argument the sentence is actually making. This edit is reflected in the "
        "P6-1 claim block below, in `WBE_Review_Condensed_Claim_Map.csv`, and in "
        "`WBE_Review_Condensed_Citation_Audit.csv`'s [57] row. Options A and B remain open items for a future "
        "round with real database access; see the corresponding row in "
        "`WBE_Review_Full_Text_Request_List.csv` and module 9 of `WBE_Review_Targeted_Search_Addendum.md`."
    )
    md.append("")

    md.append(f"## 4. P0 — Critical claims ({len(p0)})")
    md.append("")
    for r in p0:
        md.append(claim_block(r))

    md.append(f"## 5. P1 — High claims ({len(p1)})")
    md.append("")
    for r in p1:
        md.append(claim_block(r))

    md.append("## 6. What this plan does not do")
    md.append("")
    md.append(
        "- It does not run any database search — no Web of Science, Scopus, or PubMed query has been "
        "executed, and no hit counts are reported or fabricated anywhere in this document.\n"
        "- It does not obtain or read any full text — `full_text_read` remains `no` for all 67 active "
        "references; the 0/67 full-text-verification denominator is unchanged by this document's existence.\n"
        "- It does not revise, narrow, or remove any claim beyond the single [57] edit described in §3, which "
        "was a clear single-preprint overextension already identified and authorized for correction this "
        "round, not a new full-text-driven revision.\n"
        "- It does not constitute or imply submission readiness. Full-text verified: 0/67. Submission ready: No."
    )
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {len(p0)} P0 + {len(p1)} P1 claim blocks to {OUT_MD}")


if __name__ == "__main__":
    main()
