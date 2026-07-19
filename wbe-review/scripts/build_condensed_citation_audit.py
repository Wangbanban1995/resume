#!/usr/bin/env python3
"""Builds WBE_Review_Condensed_Citation_Audit.csv: bidirectional citation
check for WBE_Review_WR_Condensed_Draft.md against WBE_Review_References.md.

Covers all 68 issued reference numbers (67 active + withdrawn [56]), not
just the ones actually cited this round -- unused active references are
recorded as such (not assumed to need future citation), per instruction
that active references need not all be used but their unused status must
be recorded.
"""
import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "WBE_Review_Condensed_Citation_Audit.csv"

FIELDS = ["reference_number", "active_or_withdrawn", "cited_in_condensed_draft", "cited_section",
          "claim_supported", "evidence_level", "possible_overextension", "full_text_priority",
          "phase3c_technical_check"]

# Phase 3C (2026-07-19): technical citation-consistency check only -- confirms every in-text
# citation exists in References.md with matching author/year, no duplicate reference numbering,
# [56] absent from the main text, and [57] still hedged as an active preprint. Does NOT re-verify
# evidentiary support (that is a full-text-verification task, tracked separately) -- citation
# existence is not claim verification.
PHASE3C_CHECK_USED = ("Confirmed 2026-07-19: author-year citation in condensed draft matches this "
                       "reference's entry in References.md; no duplicate reference numbering found "
                       "in References.md; this is a technical-consistency check only, not a "
                       "re-verification of evidentiary support")
PHASE3C_CHECK_WITHDRAWN = "Confirmed 2026-07-19: [56] does not appear anywhere in the condensed draft body"
PHASE3C_CHECK_UNUSED = "N/A -- not cited in the condensed draft, no in-text citation to check"

# All 68 issued reference numbers (from References.md), withdrawn status.
ALL_REFS = [str(i) for i in range(1, 68)] + ["32b"]
WITHDRAWN = {"56"}

# Citations actually used in the condensed draft this round: ref_number -> details.
USED = {
    "2": {"section": "1.1", "claim": "No consensus on best population-normalization marker", "evidence": "Abstract-checked", "overext": "No"},
    "3": {"section": "3.5, 4.2", "claim": "Flow normalization unreliable under substantial inflow/infiltration", "evidence": "Abstract-checked", "overext": "No -- single-study finding correctly scoped as 'in others', not generalized"},
    "6": {"section": "3.4", "claim": "Temperature independently accelerates target decay", "evidence": "Abstract-checked", "overext": "No -- specific 26C threshold correctly omitted, only qualitative direction retained"},
    "8": {"section": "3.4, 3.5", "claim": "Explicit rainfall correction substantially improved correlation with clinical data", "evidence": "Abstract-checked", "overext": "No -- this review's strongest single rainfall-correction evidence anchor, correctly scoped to 'one case in this evidence base'"},
    "9": {"section": "3.2, 3.4", "claim": "Microbial activity is dominant driver of RNA loss, distance-dependent", "evidence": "Abstract-checked", "overext": "No -- specific rate-constant figures correctly omitted"},
    "11": {"section": "2", "claim": "WBE captures asymptomatic/undiagnosed infections clinical surveillance misses", "evidence": "Institutional guidance", "overext": "No -- general framing claim, not a specific number"},
    "13": {"section": "3.5, 4.2", "claim": "Flow normalization outperformed 3 fecal biomarkers in a 182-community, 6-state study", "evidence": "Abstract-checked", "overext": "No -- correctly paired with Darling et al. [3] as context-dependent, not a universal ranking"},
    "16": {"section": "3.2", "claim": "Sewer biofilms cause substantial RNA loss within hours", "evidence": "Abstract-checked", "overext": "No -- specific 90%-in-2-hours figure correctly omitted"},
    "35": {"section": "5.1", "claim": "Externally-grounded shedding kernel improves state-observability of deconvolution-based reconstruction", "evidence": "Abstract-checked", "overext": "No"},
    "38": {"section": "5.3", "claim": "ML model achieves useful short-horizon predictive performance across sewersheds without interpretable parameters", "evidence": "Abstract-checked (⚠ metadata partially unresolved)", "overext": "No -- correctly framed as a legitimate design choice, not a criticism of the study itself"},
    "44": {"section": "5.2", "claim": "Bayesian functional-data framework reports posterior state estimates without formal observability testing", "evidence": "Abstract-checked", "overext": "No -- correctly framed as illustrative, not as a criticism of the study's stated goals"},
    "46": {"section": "5.4", "claim": "Formal Bayesian MCMC framework for excretion-fraction uncertainty", "evidence": "Abstract-checked", "overext": "No"},
    "51": {"section": "6.3", "claim": "Documented instance of wastewater detection traced to a specific residence", "evidence": "Abstract-checked (metadata-verified)", "overext": "Fixed this round: condensed text originally read 'documented instances exist' (plural), overstating a single cited example; corrected to singular 'a documented instance exists'"},
    "52": {"section": "6.3", "claim": "Sewer connectivity systematically, not randomly, associated with demographic/geographic factors", "evidence": "Abstract-checked (metadata-verified)", "overext": "No -- specific ~80% figure correctly omitted, only the qualitative systematic-distribution finding used"},
    "55": {"section": "6.1", "claim": "Anomaly detection is a formal statistical-process-control problem distinct from trend monitoring", "evidence": "Abstract-checked (metadata-verified)", "overext": "No"},
    "57": {"section": "6.1", "claim": "Event-detection framework reports sensitivity advantage over clinical-data baseline in a large U.S. county sample", "evidence": "Abstract-checked (⚠ preprint, metadata partial)", "overext": "No -- Phase 3A Option C edit removed the specific 281-county figure and reframed as 'a recent preprint reports...' with explicit single-study/non-peer-reviewed/single-national-context caveats in the same sentence"},
    "58": {"section": "6.2", "claim": "Four-system (hospital/wastewater/weather/search) fusion outperforms single streams in one study", "evidence": "Abstract-checked (metadata-verified)", "overext": "No"},
    "60": {"section": "7.1", "claim": "Passive-sampler validation across nested spatial scales demonstrates fine-scale early-detection capability", "evidence": "Abstract-checked", "overext": "No -- specific low-prevalence detection-floor figure correctly omitted"},
    "61": {"section": "7.1", "claim": "Digital twin research is a rapidly growing area with substantial recent growth", "evidence": "Abstract-checked", "overext": "No"},
    "63": {"section": "7.2", "claim": "Hybrid mechanistic-statistical/physics-informed ML frames structure as constraint on, not replacement for, learned component", "evidence": "Abstract-checked", "overext": "No"},
    "64": {"section": "7.2", "claim": "Standardized reporting/proficiency testing are necessary preconditions for reliable cross-lab public-health decisions", "evidence": "Abstract-checked (⚠ duplicated-surname author-list flag)", "overext": "Checked, no fix needed: condensed text already reads 'a national metrology working group argues...', correctly attributing this as one group's position rather than a field-wide consensus; the unresolved author-list flag is noted here for full-text-verification priority tracking, not because the claim itself is overextended"},
}


def main():
    rows = []
    for num in ALL_REFS:
        status = "WITHDRAWN" if num in WITHDRAWN else "active"
        if num in USED:
            u = USED[num]
            rows.append({
                "reference_number": num, "active_or_withdrawn": status,
                "cited_in_condensed_draft": "yes",
                "cited_section": u["section"], "claim_supported": u["claim"],
                "evidence_level": u["evidence"], "possible_overextension": u["overext"],
                "full_text_priority": "See WBE_Review_Condensed_Claim_Map.csv evidence_gap_priority for the specific paragraph(s)",
                "phase3c_technical_check": PHASE3C_CHECK_USED,
            })
        elif status == "WITHDRAWN":
            rows.append({
                "reference_number": num, "active_or_withdrawn": status,
                "cited_in_condensed_draft": "no",
                "cited_section": "N/A -- withdrawn, correctly not cited",
                "claim_supported": "N/A", "evidence_level": "N/A",
                "possible_overextension": "N/A -- confirmed absent from condensed draft body (see grep check in Compression Log)",
                "full_text_priority": "N/A -- do not cite until metadata resolved, per standing project rule",
                "phase3c_technical_check": PHASE3C_CHECK_WITHDRAWN,
            })
        else:
            rows.append({
                "reference_number": num, "active_or_withdrawn": status,
                "cited_in_condensed_draft": "no",
                "cited_section": "N/A -- not used in Parts 1-8 this round",
                "claim_supported": "N/A",
                "evidence_level": "N/A (active, available for future use)",
                "possible_overextension": "N/A",
                "full_text_priority": "Low priority for this round; available if Phase 2C prose expansion needs it",
                "phase3c_technical_check": PHASE3C_CHECK_UNUSED,
            })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    used_count = len(USED)
    unused_active = sum(1 for r in rows if r["active_or_withdrawn"] == "active" and r["cited_in_condensed_draft"] == "no")
    print(f"Total rows: {len(rows)}")
    print(f"Active references used in condensed draft: {used_count}")
    print(f"Active references NOT used: {unused_active}")
    print(f"Withdrawn: {len(WITHDRAWN)}")
    overext_flags = [r for r in rows if r["possible_overextension"].startswith("**Yes")]
    print(f"Flagged for possible overextension review: {len(overext_flags)}")
    for r in overext_flags:
        print(f"  [{r['reference_number']}]: {r['possible_overextension'][:80]}")


if __name__ == "__main__":
    main()
