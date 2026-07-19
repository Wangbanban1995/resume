# Chapter 9 Claim Audit — WBE Review

**Purpose and scope.** This file records, paragraph by paragraph, every distinct claim made in Chapter 9 ("Integration with Public-Health Surveillance and Decision-Making"), its type, its citation (if any), its evidence level, and its support status, using the six-category vocabulary specified for this audit: **Conceptual synthesis** (this review's own analytical/organizational contribution, not an empirical claim borrowed from a source); **Metadata-level support** (a source's existence, authorship, and bibliographic identity are confirmed, but the specific claim attributed to it is not independently confirmed beyond a search-engine snippet); **Abstract-level support** (a search-engine-summarized abstract or snippet was reviewed and supports the claim as paraphrased); **Institutional guidance support** (an official institutional/organizational document, e.g. WHO/NASEM/ECDC, is the source); **Unsupported** (no citation exists and none should be inferred); **Pending full-text verification** (the specific number/figure requires primary-source confirmation this review does not have). Every source cited anywhere in this file carries, at most, Metadata-level, Abstract-level, or Institutional-guidance support — **no claim in this entire chapter, or this entire review, has Full-text-verified or Claim-verified support**, consistent with `WBE_Review_Ch8_Evidence_Freeze_Audit.md`'s headline full-text-read figure (0 of the review's active references, recomputed each round a chapter is added — 0/59 at the time this file was first written, 0/67 as of Chapter 10; the denominator changes, the numerator does not).

This audit does **not** re-derive `WBE_Review_Table7_Evidence_Audit.md`'s cell-by-cell review of Table 7 — see that file directly for Table 7 detail; this file covers Table 7 only as a single summary row pointing there, to avoid duplicating the same audit in two places.

---

## §9.0 — Bridge framing

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.0-P1 | Chapter 8 closes with a full posterior/interval distribution over $X(\tau)$, not a point estimate | Framework definition | Internal (§8.0, §7.0, §8.14) | N/A — internal cross-reference | Conceptual synthesis | No | None |
| §9.0-P2 | This distribution is a scientific output, not a public-health action by itself; Chapter 9 is a translation layer, not a sixth distortion type | Framework definition | Internal (§3.0) | N/A | Conceptual synthesis | No | None |

## §9.1 — Three surveillance objectives, one signal

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.1-P1 | §7.1.2 already distinguished three output kinds (trend/anomaly/absolute) | Framework definition | Internal (§7.1.2) | N/A | Conceptual synthesis | No | None |
| §9.1-P2 | Trend monitoring is comparatively robust to a *stable* bias but not to a bias correlated with the trend itself (rainfall/seasonality example) | Qualitative/mechanistic reasoning | Internal (§4.2, §5.5) | N/A | Conceptual synthesis (deductive argument from Ch4/Ch5's own established mechanisms) | No | None |
| §9.1-P3 | A field study found wastewater surveillance could function as an early-warning system in low-incidence settings | Qualitative empirical finding | Assoum et al. 2023 [55] | Metadata-verified (full author list confirmed) | Abstract-level support | Yes — specific lead-time/sensitivity figures explicitly not asserted | None; text already correctly hedges by omitting numbers |
| §9.1-P4 | Anomaly detection is a formal statistical-process-control problem sensitive to noise-distribution shape and censoring | Framework/mechanistic reasoning | Internal (§8.4, §8.11) | N/A | Conceptual synthesis | No | None |
| §9.1-P5 | An EWMA-based transparent design idea exists in the literature (design philosophy only, not attributed to any numbered reference) | Conceptual mention, explicitly uncited | None (deliberately) | N/A | Conceptual synthesis — **explicitly not tied to [56], which is withdrawn** | No (no number asserted) | None; this is the correct handling per Section 四's Option-B requirement |
| §9.1-P6 | Absolute-magnitude estimation requires a meaningful subset of §7.0's five criteria; Table 5 found no method family achieves all five | Empirical finding, self-referential | Internal (§7.0, §7.4, Table 5) | N/A — this review's own prior audit | Conceptual synthesis (restating this review's own Chapter 7 finding, not a new external claim) | No | None |
| §9.1-P7 (operational-consequence paragraph) | A surveillance program should name its objective before setting a threshold or fusing data | Recommendation / conceptual synthesis | None | N/A | Conceptual synthesis | No | None |

## §9.2 — Alert-threshold design and asymmetric cost [FOCUS AREAS 1 & 2]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.2-P1 | An "alert" is the output of a detection rule applied to a signal already carrying every upstream distortion/uncertainty source | Framework/mechanistic reasoning | Internal (Ch3–8) | N/A | Conceptual synthesis | No | None |
| §9.2-P2 | A transparent EWMA design idea favors auditability over forecasting complexity (design philosophy, explicitly uncited per §9.1-P5's resolution) | Conceptual mention, explicitly uncited | None (deliberately) | N/A | Conceptual synthesis | No | None |
| §9.2-P3 | A classification-based event-detection framework reports sensitivity 0.82/PPV 0.64 (wastewater) vs. 0.58/0.19 ($R_t$ baseline) across 281 U.S. counties | Quantitative empirical finding | Link, Garrido, et al. 2026 [57] | Metadata-verified at partial-list tier (two authors confirmed, 2026-07-18) | Abstract-level support | **Yes — explicitly and prominently hedged in-text** | None; already correctly hedged, including the transferability caution below |
| §9.2-P4 **[FOCUS AREA 2 — threshold non-transferability]** | A detection rule's performance is a property of the joint system (signal + noise + threshold), not the signal alone; a figure calibrated on 281 counties is not established to transfer to a different population/sewershed/season | Conceptual argument, explicitly original to this review | Internal (§7.1.1, §8.7, §8.12 cross-referenced by analogy) | N/A | Conceptual synthesis — **this is this review's own inferential argument, not a finding reported by [57] itself; [57] is the illustrative example the argument is applied to, not the source of the argument** | No | **Verify this distinction reads clearly to an outside reader**: confirmed on re-read — the paragraph explicitly says "per §9.2's own argument," correctly signaling this is the review's inference, not [57]'s claim |
| §9.2-P5 **[FOCUS AREA 1 — asymmetric cost]** | An unnecessarily sensitive threshold generates false alarms that erode institutional trust "over time" (general early-warning-system literature) | General/background empirical claim | None specific — explicitly flagged as unverified | N/A | **Unsupported, and explicitly labeled as such in-text** ("though this review has not independently verified a WBE-specific study quantifying that trust-erosion effect") | N/A — no specific source claimed | None; this is a model instance of correct handling — a plausible claim is stated but honestly flagged as unsupported rather than given a false citation |
| §9.2-P6 | Neither error rate (false alarm/missed detection) can be minimized without raising the other, for fixed information content | Formal/statistical reasoning | Internal (§8.14) | N/A | Conceptual synthesis (a standard detection-theory principle, correctly treated as this review's own restatement rather than requiring external citation) | No | None |

## §9.3 — Multi-source data fusion [FOCUS AREAS 3 & 4a]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.3-P1 | WHO frames WES as complementary to, not a replacement for, conventional surveillance | Institutional framing claim | WHO 2025a [14] | Institutional-verified (official WHO page) | Institutional guidance support | No — framing-level claim, low distortion risk (consistent with [14]'s existing Ch1 classification) | None |
| §9.3-P2 | A comparative study integrated 4 systems (hospital, wastewater, meteorological, internet-search) into a daily time series for a Chinese city; a substantial subset of fused variables correlated significantly with case counts | Quantitative empirical finding, reported qualitatively | Zhang et al. 2025 [58] | Metadata-verified (full 8-author list confirmed) | Abstract-level support | **Yes — specific correlation magnitudes and per-system lead/lag explicitly not asserted, only the qualitative finding retained** | None; already correctly hedged |
| §9.3-P3 **[FOCUS AREA 3 — weather's double role]** | Weather is not merely an independent fusion covariate; it is simultaneously (a) a corroborating signal and (b) the confounding covariate needed to correct the wastewater signal's own amplitude distortion (§4.2, §6.2) | Conceptual argument, explicitly original to this review | Internal (§4.2, §6.2) | N/A | **Conceptual synthesis — explicitly this review's own analytical point, not attributed to any external source** | No | None; this is correctly presented as the review's own contribution, not smuggled in as an external finding |
| §9.3-P4 | A fusion pipeline treating weather only as (a) risks double-counting rainfall's effect | Conceptual/mechanistic reasoning, deduced from §9.3-P3 | Internal | N/A | Conceptual synthesis | No | None |
| §9.3-P5 | Clinical/mobility/pharmacy/hospital data each carry distinct, known distortions (ascertainment bias, behavioral proxy, prescription-fill lag, severity bias) | Conceptual/domain-knowledge synthesis | Internal (§1, [11]) partially; general public-health domain knowledge otherwise | N/A | Conceptual synthesis | No | None — these are standard, non-controversial characterizations of each data type's known limitation, not claims requiring a dedicated citation beyond the [11]/[14] framing already established |
| §9.3-P6 | None of the four fusion streams is "ground truth"; each is itself uncertain and differently biased | Conceptual argument, extends §8.16 | Internal (§8.16) | N/A | Conceptual synthesis | No | None |

## §9.4 — Why fusion is not free [FOCUS AREA 4b]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.4-P1 | §8.10 already established that treating upstream sources as independent when they are not produces a systematically wrong interval | Framework restatement | Internal (§8.10) | N/A | Conceptual synthesis | No | None |
| §9.4-P2 **[FOCUS AREA 4b — fusion failure mode 1]** | Shared external drivers (a public event, policy change, media shift) can move multiple "independent" streams together under a common confound, so averaging them doesn't reduce noise the way genuinely independent measurements would | Conceptual/statistical argument | None — general statistical reasoning | N/A | Conceptual synthesis | No | None — this is a standard statistical argument (confounding vs. independence), does not require an external empirical citation to state as a logical point |
| §9.4-P3 **[FOCUS AREA 4b — fusion failure mode 2]** | Wastewater signal has been reported to lead clinical/hospitalization data by an interval that is itself uncertain and setting-dependent | Empirical claim, self-referential to this review's own prior citations | Internal (§7.1.2, §9.2, referencing [35] Huisman et al. and [57] indirectly) | N/A — restates already-cited findings | Conceptual synthesis restating prior Abstract-level-supported claims | Yes, inherited from the underlying sources' own pending status | None; no new citation burden introduced, correctly traced to already-audited sources |
| §9.4-P4 | The defensible response is joint state-space/Bayesian modeling of correlated uncertainty, extending §8.9's machinery, or explicit disclosure of the limitation, per §8.15's discipline | Recommendation, extends internal framework | Internal (§8.9, §8.15) | N/A | Conceptual synthesis | No | None |

## §9.5 — The boundary: what WBE cannot replace [FOCUS AREA 5]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.5-P1 | WBE cannot produce individual-level diagnosis; this is structural (aggregation), not a modeling gap | Conceptual/definitional argument | Internal (§3.0, [11]) | N/A | Conceptual synthesis | No | None |
| §9.5-P2 | Variant/strain-specific clinical severity cannot be inferred from bulk concentration alone; requires sequencing | Domain-knowledge claim | None specific | N/A | Conceptual synthesis (standard, non-controversial domain fact; not asserting a specific study's finding) | No | None |
| §9.5-P3 **[FOCUS AREA 5 — structural exclusion of non-sewered populations]** | Roughly one-fifth of the U.S. population is not connected to a centrally monitored sewer system, and this gap is not randomly distributed (specific demographic/geographic associations named) | Quantitative + qualitative empirical finding | Yu, Olesen, Duvallet, & Grad 2024 [52] | Metadata-verified (full 4-author list confirmed) | Abstract-level support | **Yes — the ~80% connectivity figure and demographic-association statistics explicitly flagged pending; only the qualitative "systematic, not random" finding is relied upon** | None; already correctly hedged, with the weaker/stronger claim distinction stated explicitly in-text |
| §9.5-P4 | This coverage gap cannot be closed by better modeling of Ch3–8's signal-formation chain — it is a sampling-universe gap, not a signal-processing one | Conceptual argument | Internal | N/A | Conceptual synthesis | No | None |
| §9.5-P5 | A rising signal does not identify *why* it is rising without additional information (new infections vs. testing-policy shift vs. population change vs. storm artifact) | Conceptual/mechanistic argument | Internal (§4.2, §6.3, §7) | N/A | Conceptual synthesis | No | None |
| §9.5-P6 | The correct institutional framing follows WHO's complementary-not-replacement position | Recommendation, extends institutional source | WHO 2025a [14] | Institutional-verified | Institutional guidance support | No | None |

## §9.6 — Small-catchment/building-scale monitoring: privacy, stigma, equity [FOCUS AREAS 6 & 7]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.6-P1 | Aggregation degrades structurally, not gracefully, as spatial resolution narrows toward building/facility scale | Conceptual argument, extends §9.5 | Internal | N/A | Conceptual synthesis | No | None |
| §9.6-P2 **[FOCUS AREA 6 — re-identification risk]** | A wastewater sample can in principle be traced to a single household/toilet; documented instances of upstream tracing to a specific residence are cited as illustration | Empirical example + conceptual argument | Moallef et al. 2025 [51] | Metadata-verified (full 8-author list confirmed) | Abstract-level support | **Yes — the 68/145 equity-study count explicitly flagged pending; the illustrative re-identification example is treated as the source's own cited example, at abstract-level confidence** | None; already hedged |
| §9.6-P3 | Aggregation-level design is a context-specific judgment trading off against early-warning value, not a fixed technical parameter | Conceptual argument, deduced from §9.6-P2 | Internal | N/A | Conceptual synthesis | No | None |
| §9.6-P4 **[FOCUS AREA 7 — group stigmatization]** | Group-level stigmatization is a harm distinct from individual re-identification; flagging a defined group as "diseased" has social/institutional consequences an individual-privacy framework doesn't capture | Conceptual argument + empirical framing | Kwiatkowska et al. 2022 [54] | **Venue/peer-review status unconfirmed — flagged explicitly in-text** | Abstract-level support, **explicitly downgraded** — this is this review's lowest-confidence Chapter 9 citation on evidence-type grounds, independent of the argument's plausibility | No specific number asserted | None beyond the existing in-text flag; the argument itself is separable from the citation's weakness, and the text already states this |
| §9.6-P5 | A separate analysis argues for enforceable legal "obligations" rather than ethics/rights framing alone, for governance | Conceptual/policy argument | Thompson et al. 2024 [53] | Metadata-verified at partial tier (lead author only) | Abstract-level support | No specific number asserted | None; already correctly hedged on author-list completeness |
| §9.6-P6 **[FOCUS AREA 7 — structural equity in deployment]** | Structural equity in *who* is monitored is a distinct problem from coverage gaps (§9.5); deployment choices redistribute both benefit and risk unevenly and require deliberate justification | Conceptual argument, extends [51] | Moallef et al. 2025 [51] | Metadata-verified | Abstract-level support (framework-level claim, not a specific statistic) | No | None |
| §9.6-P7 (closing conclusion) | Building/small-catchment monitoring is not "the same method at finer resolution" and needs its own explicit privacy/stigma/equity review, not inherited from a citywide program's assessment | Recommendation / conceptual synthesis | Internal, synthesizing §9.6-P1–P6 | N/A | Conceptual synthesis | No | None |

## §9.7 — From detectable signal to actionable information [FOCUS AREA 8]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.7-P1 | A signal can be scientifically detectable (above LOD, statistically distinguishable, correctly attributable) and still not be actionable | Conceptual argument, this chapter's central original contribution | Internal (§5.5, §8.11, §9.2, §7) | N/A | Conceptual synthesis | No | None |
| §9.7-P2, condition 1 **[FOCUS AREA 8]** | Actionability requires uncertainty translated into decision-relevant probability, not left as a bare point estimate | Conceptual argument, extends §8.14 | Internal (§8.14) | N/A | Conceptual synthesis | No | None |
| §9.7-P3, condition 2 **[FOCUS AREA 8]** | Actionability requires an institutional response protocol with a named actor/action/resource | Conceptual argument + institutional-source support | NASEM 2023 [11] | Institutional-verified | Institutional guidance support (NASEM names coordination as a precondition) | No | None |
| §9.7-P4, condition 3 **[FOCUS AREA 8]** | Actionability requires detection-to-action timescale shorter than the condition's own timescale; "about a week" cited as an illustrative order of magnitude | Conceptual argument + quantitative figure | None specific — explicitly flagged as illustrative, not attributed to a numbered reference | N/A | **Pending full-text verification, explicitly labeled in-text as "not a precisely established universal standard"** | **Yes — this is the one quantitative figure in §9.7 not tied to a specific numbered source** | Consider whether to trace this to a specific source (an ECDC/WHO reporting-timeliness document) in a future round, or continue presenting it as an unattributed illustrative order of magnitude — currently handled honestly but could be strengthened |
| §9.7-P5, condition 4 **[FOCUS AREA 8]** | Actionability requires the alert threshold validated against the deployment-specific cost structure, not borrowed from elsewhere | Conceptual argument, restates §9.2 | Internal (§9.2) | N/A | Conceptual synthesis | No | None |
| §9.7-P6 (closing) | A signal failing any of the four conditions is not a failure of Ch3–8's science but an unfinished translation | Conceptual synthesis, chapter's thesis statement | Internal | N/A | Conceptual synthesis | No | None |

## §9.8 — Minimum reporting requirements for a decision-ready signal

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.8-P1 | A decision-ready signal should disclose objective, threshold basis, deployment-specific error rates, incorporated uncertainty sources, fusion status, spatial resolution/equity review status, and decision protocol | Recommendation, extends §5.7/§6.9/§7.7/§8.15 pattern | Internal | N/A | Conceptual synthesis | No | None |
| §9.8-P2 | This is not a regulatory/accreditation checklist; WHO, NASEM, and ECDC are the actual authoritative sources for that purpose | Framing/disclaimer | WHO 2025b [15]; NASEM 2023 [11]; ECDC 2025 [59] | Institutional-verified (all three) | Institutional guidance support | No | None |

## Table 7 and Box [FOCUS AREA 9 — see separate file]

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| Table 7 (all cells) | Surveillance-objective × decision-requirement × uncertainty-sensitivity × fusion-role × representative-citation matrix | Original framework proposal, explicitly labeled as such in-text | Multiple, cell-dependent | Mixed | **See `WBE_Review_Table7_Evidence_Audit.md` for the required cell-by-cell audit — not duplicated here** | Mixed, see other file | See other file |
| Box | "Detectable ≠ Actionable" illustrative walkthrough | Original, explicitly hypothetical/illustrative, no borrowed statistics | None | N/A | Conceptual synthesis, explicitly labeled in-text as "this review's own illustrative construction" | No | None |

## §9.9 — Evidentiary note

| Paragraph ID | Claim | Claim type | Citation | Evidence level | Support status | Pending full-text? | Action required |
|---|---|---|---|---|---|---|---|
| §9.9-P1 | [56] is withdrawn from citation; its underlying design idea is retained conceptually without evidentiary attribution | Meta-evidentiary statement about this review's own practice | [56] (withdrawn) | N/A | Conceptual synthesis (a statement about this review's sourcing discipline, not an external claim) | No | None — this is the audit trail entry itself |

---

## Summary

- **Total claims audited:** 44 (matching the paragraph-unit count in `WBE_Review_Ch8_Evidence_Freeze_Audit.md` §3)
- **Conceptual synthesis:** 27 — this review's own analytical/organizational contribution, correctly uncited
- **Abstract-level support:** 10 — [51], [52], [53], [54], [55], [57], [58] each supporting at least one claim
- **Institutional guidance support:** 6 — [11], [14] (×2), [15], [59]
- **Metadata-level support only (no abstract content relied upon):** 0 — every cited claim in Chapter 9 draws at minimum on an abstract/snippet, not merely a source's bare existence
- **Unsupported (explicitly flagged as such in-text, not silently asserted):** 1 (§9.2-P5's trust-erosion claim)
- **Pending full-text verification (a specific number requiring primary-source confirmation):** every Abstract-level row above additionally carries this flag for its specific figures; §9.7-P4's "about a week" figure is the one claim without even a numbered-source attribution and is flagged for follow-up
- **No claim in this chapter is Full-text-verified or Claim-verified.** This matches the review's standing 0/N full-text-read status exactly — Chapter 9 introduces no exception.

**What this audit found, stated directly:** Chapter 9's nine focus areas (false-alarm/missed-detection cost, threshold non-transferability, weather's double role, fusion benefits/failure modes, structural exclusion of non-sewered populations, small-catchment re-identification risk, group stigmatization/structural equity, the four actionability conditions, and Table 7) are each supported by a mix of Abstract-level citations (correctly hedged) and this review's own explicitly-labeled conceptual synthesis — no focus area was found resting on an Unsupported or silently-asserted claim, with the single explicit exception of §9.2-P5, which the main text itself already flags as unverified rather than smoothing over. The one prior weakness this audit surfaces and corrects is the now-withdrawn [56] (§9.1-P5, §9.2-P2, §9.9), where the underlying conceptual point is retained but decoupled from an evidentiary attribution that could not clear this review's citation bar.
