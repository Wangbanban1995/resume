# Evidence Recovery Plan — Critical and High Claim Verification

**Round:** Water Research compression, Phase 3A. 2026-07-18. **This document is a readable narrative wrapper around `WBE_Review_Critical_Claim_Verification_Queue.csv`, not a separate source of truth.** Every claim block below is generated directly from that CSV's rows; if the two ever appear to disagree, the CSV is authoritative and this file is stale and should be regenerated via `scripts/build_evidence_recovery_plan.py`.

**What this document is not:** it is not a completed search, not a full-text verification report, and not a claim-revision record. It converts the condensed draft's 9 Critical and 7 High evidence gaps (per `WBE_Review_Condensed_Claim_Map.csv`'s `evidence_gap_priority` column — the authoritative count; see `WBE_Review_Phase2B_Risk_Log.md`'s Phase 3A addendum for the reconciliation against an earlier, less precise chat-summary framing) into an executable plan: what to search for, what evidence would resolve each gap, and what happens if that evidence is never found.

## 1. Priority tiers

- **P0 (Critical, 9 claims):** the claim map's `Critical` rows — quantitative, mechanistic, or cross-population conclusions currently resting on single-study, abstract-checked, or otherwise thin evidence, where an unresolved gap would require a real change to the manuscript's argument (not just a citation swap) if the evidence cannot be found.
- **P1 (High, 7 claims):** the claim map's `High` rows — similar in kind but judged less load-bearing, or already partly self-hedged in the condensed text.
- **P2 (not itemized as individual rows this round):** all remaining quantitative, table-performance, cross-city/climate/population, model-superiority, normalizer-performance, threshold-transportability, and ethics/equity/privacy empirical claims not already captured in P0/P1 — i.e., the Moderate-tier empirical rows in the Claim Map. These are lower urgency than P0/P1 but share the same evidence thresholds (§2) and should be queued the same way once P0/P1 recovery work is underway.
- **P3 (not itemized as individual rows this round):** the remaining Moderate/Low evidence gaps and the Author-synthesis rows, which by definition need no external citation and are out of scope for full-text recovery.

## 2. Minimum evidence thresholds by claim type

These thresholds govern when a Critical or High claim can be marked resolved, and were applied when drafting each claim's `evidence_needed` / `preferred_evidence_type` fields below:

- **Quantitative / performance conclusions** (e.g., normalizer performance, model accuracy, sensitivity/specificity figures) require the original full text, with an explicit sample, scenario, and method described — an abstract, a search-engine summary, or another review's paraphrase of the same number does not qualify.
- **Cross-city / cross-climate / cross-population conclusions** require either at least two independent settings, or one study that explicitly tested multiple sites itself; absent that, the claim must be narrowed to an explicit "in the studied setting..." framing rather than presented as general.
- **Mechanistic conclusions** (biofilm transformation, sediment/sewer memory, rainfall-dependent fate, temperature-sensitive decay) require direct observational or experimental verification of the mechanism itself. A correlational study cannot be silently upgraded to mechanistic evidence.
- **Model / validation conclusions** require that the source actually checked recovery of the target state (the quantity the model claims to infer), not merely predictive fit to the observed signal.
- **Ethics / equity / privacy conclusions** may draw on guidance documents, ethical analyses, deployment case studies, or governance research, but each such claim must be tagged as one of: a normative recommendation, a documented empirical harm, or a theoretical/anticipated risk. A guidance document's existence does not by itself prove a risk has actually occurred.

## 3. [57] (Link, Garrido, et al. 2026) handling this round

Per this round's instruction, one of three options was to be applied to the single-preprint claim at §6.1 (P6-1): (A) find a formal peer-reviewed version and record the version relationship without auto-replacing; (B) find independent second evidence from a different team or scenario; (C) if neither is available this round, narrow the text to an explicit "a recent preprint suggests/reports..." framing with single-study, non-peer-reviewed, and scenario-limited caveats, and, if the specific "281-county" figure is not essential to the argument, prioritize removing that number while keeping the general threshold-transfer question.

**No new formal-version or independent second-source search was run this round** (this round has no environment access to Web of Science, Scopus, or PubMed — see `WBE_Review_Targeted_Search_Addendum.md`, which is search-reinforcement design only, not an executed search), so Options A and B were not available. **Option C was applied directly to `WBE_Review_WR_Condensed_Draft.md` §6.1**: the sentence was edited from a load-bearing "an event-detection framework evaluated across 281 U.S. counties reports..." framing to an explicitly hedged "a recent preprint reports a sensitivity advantage... across a large U.S. county sample..., but this is a single, non-peer-reviewed study set in one national context..." framing, with the specific 281-county figure removed as non-essential to the general threshold-transportability argument the sentence is actually making. This edit is reflected in the P6-1 claim block below, in `WBE_Review_Condensed_Claim_Map.csv`, and in `WBE_Review_Condensed_Citation_Audit.csv`'s [57] row. Options A and B remain open items for a future round with real database access; see the corresponding row in `WBE_Review_Full_Text_Request_List.csv` and module 9 of `WBE_Review_Targeted_Search_Addendum.md`.

## 4. P0 — Critical claims (9)

#### P3-3 — §3.2

> Sewer biofilms are an active sink for viral RNA rather than an inert surface; laboratory reactor studies report substantial RNA loss within hours of biofilm exposure, and combined batch-decay/pipeline-simulator work identifies microbial activity, rather than chemical hydrolysis, as the dominant driver of that loss, with decay increasing measurably as a function of transport distance.

- **Claim type:** Mechanistic
- **Current reference(s):** [16] Zhang et al. 2023; [9] Jung et al. 2026
- **Current evidence level:** Abstract-checked
- **Current support scope:** Each study supports its own lab-reactor/simulator finding; not yet confirmed this generalizes beyond the specific conditions tested
- **Identified overextension:** None found -- condensed text already avoids the unconfirmed 90%-in-2-hours figure; the mechanistic claim itself needs direct experimental confirmation, not just abstract-level trust
- **Evidence needed:** Full text confirming experimental design, biofilm colonization method, and whether microbial-activity-dominance was directly measured (e.g., biocide-inhibition control) rather than inferred
- **Preferred evidence type / study design:** Primary experimental study with direct mechanistic manipulation (biocide/sterilization control arm); Controlled laboratory reactor or pipeline-simulator experiment with a microbial-activity-inhibited control arm
- **Minimum number of settings:** 1 (mechanism); 2+ preferred for triangulation
- **Database search concepts:** sewer biofilm; SARS-CoV-2 RNA decay; wastewater pipe reactor; microbial degradation wastewater
- **Candidate search query:** `("sewer biofilm" OR "pipe biofilm") AND ("RNA decay" OR "viral RNA degradation") AND (wastewater OR sewer)`
- **Full text required:** yes
- **Decision if unresolved:** narrow -- if full text not obtained, narrow to 'laboratory studies report...' explicitly flagged as lab-condition-specific, not confirmed generalizable to field sewers
- **Status:** Pending full-text acquisition

#### P3-6 — §3.4

> Rainfall is not merely dilution. It enters sewer networks through two structurally different pathways... that together dilute measured concentration, but also resuspend settled sediment, shorten hydraulic retention time..., and shift the relative contribution of different sub-catchments to the composite signal.

- **Claim type:** Mechanistic
- **Current reference(s):** None directly cited in this paragraph (evidence follows in P3-7)
- **Current evidence level:** Conceptual synthesis based on preceding process evidence
- **Current support scope:** Not applicable -- mechanism statement, not yet evidence-anchored in this specific paragraph
- **Identified overextension:** None identified -- paragraph is explicitly a mechanism statement, not a citation-bearing empirical claim
- **Evidence needed:** Direct hydraulic/water-quality studies demonstrating each named sub-mechanism (sediment resuspension during storms; retention-time shortening; sub-catchment weight shift) individually
- **Preferred evidence type / study design:** Field hydraulic monitoring study with paired dry/wet-weather sampling; Paired or multi-event field study measuring flow, retention time, and sediment resuspension under both dry and wet conditions
- **Minimum number of settings:** 2 (to distinguish general mechanism from one network's specific behavior)
- **Database search concepts:** combined sewer overflow; inflow infiltration; sediment resuspension storm; hydraulic retention time rainfall
- **Candidate search query:** `("inflow and infiltration" OR "combined sewer overflow") AND ("sediment resuspension" OR "retention time") AND (wastewater OR sewer)`
- **Full text required:** yes
- **Decision if unresolved:** retain -- this is an established sanitary/environmental engineering mechanism independent of WBE-specific literature; if WBE-specific confirmation is not found, cite general hydraulic-engineering literature explicitly rather than implying WBE-specific validation
- **Status:** Pending targeted search (Addendum module 2)

#### P3-7 — §3.4

> A large multi-plant national wastewater surveillance program found that explicitly correcting concentration data for rainfall impact substantially improved correlation with independent clinical case counts relative to uncorrected data... direct evidence that rainfall behaves as a correctable, structured bias.

- **Claim type:** Empirical/performance
- **Current reference(s):** [8] Janssens et al. 2022
- **Current evidence level:** Abstract-checked
- **Current support scope:** Single national program (Belgium); 'substantially improved' not quantified in condensed text; generalizability to other countries/climates not established
- **Identified overextension:** None found in current text (already hedged as 'one case in this evidence base'); but the underlying single-study status is a structural gap given this is the review's single strongest process-informed-correction evidence anchor
- **Evidence needed:** Full text confirming actual correlation-improvement magnitude, statistical significance, and whether the finding replicates in a second country/climate
- **Preferred evidence type / study design:** Primary empirical study, ideally 2+ independent countries/programs; Before/after or paired comparison of rainfall-corrected vs. uncorrected wastewater-clinical correlation
- **Minimum number of settings:** 2 (currently only 1 -- Belgium)
- **Database search concepts:** rainfall correction wastewater surveillance; wet weather wastewater signal correction; SARS-CoV-2 wastewater rainfall
- **Candidate search query:** `(wastewater surveillance) AND (rainfall OR "wet weather") AND (correction OR adjustment) AND (correlation OR validation)`
- **Full text required:** yes
- **Decision if unresolved:** narrow -- if no second setting is found, narrow text to 'In the studied Belgian program...' per the cross-city evidentiary rule
- **Status:** Pending full-text acquisition + targeted search for a second setting

#### P3-9 — §3.5

> ...flow normalization outperforming biomarker normalization in some large multi-site comparisons... while becoming unreliable under substantial inflow and infiltration in others...: the two findings together indicate that no single fixed correction factor is identifiable across all hydraulic conditions.

- **Claim type:** Cross-site generalization
- **Current reference(s):** [13] Rainey et al. 2023; [3] Darling et al. 2025
- **Current evidence level:** Abstract-checked
- **Current support scope:** Each study supports its own single condition (Rainey: 182 communities/6 states; Darling: rural, high-I&I sewersheds); 'no single fixed factor identifiable across all conditions' is this review's own synthesis across exactly 2 studies
- **Identified overextension:** 'All hydraulic conditions' risks overgeneralizing from 2 studies; already softened by 'in some... in others' framing but should be checked against full text
- **Evidence needed:** Full text of both studies to confirm exact site counts, I&I severity classification, and whether findings are as cleanly complementary as summarized
- **Preferred evidence type / study design:** Multi-site comparative study explicitly varying hydraulic/I&I conditions; Multi-site (3+) comparison spanning a documented range of I&I severity
- **Minimum number of settings:** 2 minimum (met: Rainey + Darling); 3+ preferred for a 'no universal fixed factor' claim
- **Database search concepts:** flow normalization performance; inflow infiltration wastewater surveillance; population normalization comparison multi-site
- **Candidate search query:** `("flow normalization" OR "population normalization") AND (wastewater) AND ("inflow and infiltration" OR "multi-site" OR "multi-community")`
- **Full text required:** yes
- **Decision if unresolved:** qualify -- if full text does not confirm the complementary reading, qualify to 'these findings are not necessarily contradictory, since...' rather than asserting the synthesis as established
- **Status:** Pending full-text acquisition (both studies)

#### P4-5 — §4.2

> Rainfall, infiltration, and industrial or non-domestic discharge each limit what flow normalization alone can fix... Comparative evidence shows flow normalization outperforming biomarker alternatives in some large multi-site studies... while becoming unreliable under substantial inflow and infiltration in others -- a context-dependent applicability condition, not a universal ranking.

- **Claim type:** Cross-site generalization + performance comparison
- **Current reference(s):** [13] Rainey et al. 2023; [3] Darling et al. 2025
- **Current evidence level:** Abstract-checked
- **Current support scope:** Same underlying pair as P3-9; industrial/non-domestic discharge limitation is asserted without any specific citation
- **Identified overextension:** The industrial/non-domestic-discharge clause has NO citation at all in the condensed text -- an uncited mechanistic assertion, distinct from the Rainey/Darling pairing's evidence gap
- **Evidence needed:** (1) Same as P3-9 for the Rainey/Darling pairing; (2) a specific citation for the industrial/non-domestic-discharge-limits-normalization claim, currently entirely uncited
- **Preferred evidence type / study design:** Primary study documenting industrial/non-domestic flow contribution's effect on normalization validity; Field study in a mixed residential/industrial sewershed comparing normalization performance
- **Minimum number of settings:** 1 for the industrial-discharge clause specifically (currently 0)
- **Database search concepts:** industrial discharge wastewater normalization; non-domestic flow contribution sewer; trade waste wastewater surveillance
- **Candidate search query:** `("industrial discharge" OR "non-domestic wastewater" OR "trade waste") AND ("wastewater surveillance" OR "wastewater normalization")`
- **Full text required:** yes
- **Decision if unresolved:** remove -- if no citation can be found for the industrial/non-domestic-discharge clause specifically, remove that clause; the rainfall/infiltration portion can retain the existing Rainey/Darling citations
- **Status:** Pending targeted search (Addendum module 2); industrial-discharge clause currently has zero supporting citation

#### P4-6 — §4.3

> No single population biomarker has been validated as universally reliable... Creatinine... disqualified by in-sewer instability; cotinine... confounded by geographically variable smoking prevalence; PMMoV and crAssphage... show inconsistent, often neutral-or-negative, performance across independent multi-site validation studies.

- **Claim type:** Performance comparison, cross-study generalization
- **Current reference(s):** Chen et al. 2014 (creatinine/cotinine); Maal-Bared et al. 2023, Dhiyebi et al. 2023 (PMMoV/crAssphage) -- none named inline in condensed prose
- **Current evidence level:** Abstract-checked
- **Current support scope:** Each named biomarker's performance pattern rests on 1-3 single-site or few-site studies per the source draft's fuller §6.4-§6.5 narrative; 'no biomarker universally validated' is this review's own synthesis, not directly demonstrated by any one source
- **Identified overextension:** The condensed text does not name the supporting studies inline -- readers cannot trace 'PMMoV... inconsistent' to its source from the condensed prose alone (citation-attribution gap)
- **Evidence needed:** Full text of Chen et al. 2014, Maal-Bared et al. 2023, and Dhiyebi et al. 2023 to confirm the specific site counts and performance directions summarized
- **Preferred evidence type / study design:** Multi-site comparative validation studies (already the design of the 3 underlying studies); Multi-site (10+) biomarker performance comparison against independent clinical reference data
- **Minimum number of settings:** 3+ (multiple biomarkers, multiple studies already implied; full text needed to confirm exact counts)
- **Database search concepts:** PMMoV normalization performance; crAssphage wastewater normalization; fecal indicator biomarker wastewater validation
- **Candidate search query:** `(PMMoV OR crAssphage OR "fecal indicator") AND (wastewater) AND (normalization) AND (validation OR correlation)`
- **Full text required:** yes
- **Decision if unresolved:** retain with citation restored -- add inline citations (Chen et al. 2014; Maal-Bared et al. 2023; Dhiyebi et al. 2023) to the condensed text regardless of full-text-verification outcome; narrow specific performance claims only if full text contradicts the abstract-level summary
- **Status:** Pending full-text acquisition (3 studies); immediate citation-attribution fix recommended

#### P4-10 — §4.4 / Table 2

> Table 2's four rows (flow, census population, dynamic population, biomarker ratio) against corrected mechanism, required assumption, and residual uncertainty.

- **Claim type:** Table performance judgment (consolidated)
- **Current reference(s):** [3],[13] (flow rows); Chen/Maal-Bared/Dhiyebi implied for biomarker row, not cited in the table itself
- **Current evidence level:** Abstract-checked
- **Current support scope:** Table cells synthesize the same underlying single-study findings named in P4-3 through P4-7; the biomarker-ratio row's residual-uncertainty cell is a general synthesis not tied to any specific named study in the table
- **Identified overextension:** Table 2 carries NO citation column at all -- a reader cannot trace any cell's claim to a specific source without cross-referencing prose elsewhere. Structural evidentiary-transparency gap in the table's own design.
- **Evidence needed:** Same as P4-5 and P4-6 combined, since Table 2 consolidates both
- **Preferred evidence type / study design:** Same as P4-5/P4-6; Same as P4-5/P4-6
- **Minimum number of settings:** Varies by row -- see P4-5/P4-6
- **Database search concepts:** Combines Addendum modules 2 (rainfall/hydraulic), 4 (normalization biomarkers), 5 (fate matching)
- **Candidate search query:** `See P4-5 and P4-6 queries combined`
- **Full text required:** yes
- **Decision if unresolved:** qualify -- add a citation column to Table 2 regardless of full-text outcome (a table-design fix, independent of new evidence); qualify individual cells per each row's underlying claim's resolution
- **Status:** Pending full-text acquisition (aggregates P4-5/P4-6); table-design fix (citation column) can proceed independently

#### P5-10 — §5.5 / Table 3

> Table 3's six model-family rows (direct mass balance, empirical regression, convolution/deconvolution, mechanistic transport-decay, Bayesian/state-space, hybrid process-informed) against identifiability requirement, dominant uncertainty, minimum validation, and failure mode.

- **Claim type:** Table performance/validation judgment (consolidated)
- **Current reference(s):** [35] Huisman et al. 2022; [44] Dai et al. 2024; [38] Ai et al. 2022 (implied); 3 of 6 rows uncited
- **Current evidence level:** Abstract-checked
- **Current support scope:** Only 3 of 6 rows have an explicit citation elsewhere in Part 5's prose; the mass-balance, empirical-regression, and mechanistic-transport-decay rows' cells are this review's own synthesis without a named illustrative study in the condensed text
- **Identified overextension:** 3 of 6 rows (mass balance, empirical regression, mechanistic transport-decay) have NO citation at all in the condensed draft -- same structural gap as P4-10's Table 2
- **Evidence needed:** Named illustrative studies to properly anchor all 6 rows -- the source draft already identifies candidates (Zuccato et al. 2008 for mass balance, Schoen et al. 2022 for empirical regression, McMahan et al. 2021 for mechanistic transport-decay) that were not carried into the condensed Table 3
- **Preferred evidence type / study design:** One representative primary study per model family, full text; Varies by family -- see source draft §7.4 Table 4/5 for full candidate list
- **Minimum number of settings:** 1 per row minimum for citation-attribution; 2+ for full generalization
- **Database search concepts:** WBE mass balance back-calculation; empirical regression wastewater case prediction; SEIR wastewater compartmental model
- **Candidate search query:** `("wastewater-based epidemiology" OR WBE) AND ("mass balance" OR "back-calculation" OR "compartmental model" OR "SEIR")`
- **Full text required:** yes
- **Decision if unresolved:** qualify -- restore citations for all 6 rows from the source draft's existing Table 4/5 (Zuccato et al. 2008, Schoen et al. 2022, McMahan et al. 2021 are already in the source draft's evidence base, just not carried into the condensed Table 3) -- a citation-restoration fix independent of new full-text verification
- **Status:** Pending full-text acquisition; 3-row citation-attribution gap can be partially fixed immediately by restoring existing source-draft citations

#### P6-1 — §6.1

> ...a recent preprint reports a sensitivity advantage for an event-detection framework over a clinical-data baseline across a large U.S. county sample (Link, Garrido, et al., 2026), but this is a single, non-peer-reviewed study set in one national context, and threshold transportability across populations and sewersheds cannot be assumed from it and must be re-validated in each new deployment context.

- **Claim type:** Performance + cross-population generalization (already self-limited in text)
- **Current reference(s):** [57] Link, Garrido et al. 2026 (medRxiv preprint)
- **Current evidence level:** Abstract-checked, non-peer-reviewed preprint, metadata only partially corroborated
- **Current support scope:** Single preprint, single country (U.S.), single disease (SARS-CoV-2) -- already explicitly flagged as single-study and non-transferable in the same sentence; the specific 281-county figure was removed from the condensed text this round as not essential to the argument
- **Identified overextension:** The underlying source is a preprint, not a peer-reviewed publication -- per this round's rule, a preprint must not alone support a core claim. Addressed directly this round via Option C narrowing (Task 99): condensed draft §6.1 edited to an explicit 'a recent preprint reports...' framing, the specific 281-county number removed as non-essential, and single-study/non-peer-reviewed/single-national-context caveats added in the same sentence.
- **Evidence needed:** Either (a) the formal peer-reviewed version of this preprint, or (b) a second, independent peer-reviewed study of wastewater-based event/outbreak detection performance
- **Preferred evidence type / study design:** Peer-reviewed primary study; Multi-site event-detection performance evaluation against a clinical baseline
- **Minimum number of settings:** 2 (currently 1, and that 1 is unpublished)
- **Database search concepts:** wastewater outbreak detection sensitivity; event detection SARS-CoV-2 wastewater; alert threshold wastewater surveillance performance
- **Candidate search query:** `("event detection" OR "outbreak detection" OR "alert threshold") AND (wastewater) AND (sensitivity OR "predictive value")`
- **Full text required:** yes (for formal version if found; otherwise second independent study)
- **Decision if unresolved:** narrow -- Option C narrowing applied this round (verified in condensed draft §6.1); general threshold-transportability point retained as this review's own inference, decoupled from the 281-county figure, which is no longer cited in the text
- **Status:** Option C narrowing applied and verified in WBE_Review_WR_Condensed_Draft.md §6.1 this round; formal-version / independent second-study search still pending (see Full Text Request List and Search Addendum module 9)

## 5. P1 — High claims (7)

#### P4-2 — §4.1

> Recovery... and inhibition or matrix suppression... are mechanistically distinct amplitude-loss terms... which is why they require separate quality-control checks rather than one combined correction factor.

- **Claim type:** Mechanistic + method-performance comparison
- **Current reference(s):** Pecson et al. 2021 (referenced qualitatively, not inline-cited)
- **Current evidence level:** Abstract-checked
- **Current support scope:** Pecson et al. supports the interlaboratory-variability finding generally (36-SOP comparison); not cited inline in the condensed paragraph
- **Identified overextension:** Pecson et al. is referenced only in the Claim Map, not as an inline citation in the condensed draft -- same attribution-gap pattern as P4-6
- **Evidence needed:** Full text of Pecson et al. 2021 to confirm the 36-SOP interlaboratory finding's magnitude and whether recovery/inhibition were separately, not jointly, characterized
- **Preferred evidence type / study design:** Interlaboratory comparison study; Multi-laboratory, multi-SOP comparison with recovery and inhibition measured as separate QC metrics
- **Minimum number of settings:** 1 (interlaboratory study inherently multi-site)
- **Database search concepts:** wastewater qPCR interlaboratory comparison; recovery efficiency PCR inhibition wastewater
- **Candidate search query:** `("interlaboratory" OR "inter-laboratory") AND (wastewater) AND (recovery OR inhibition) AND (SARS-CoV-2 OR qPCR)`
- **Full text required:** yes
- **Decision if unresolved:** retain with citation restored -- add inline citation to Pecson et al. 2021 regardless of full-text outcome; the six-concept taxonomy itself is this review's own framework, not dependent on this citation
- **Status:** Pending full-text acquisition; citation-attribution fix recommended immediately

#### P5-2 — §5.1

> A deconvolution approach that grounds its shedding kernel in independently collected clinical data... (Huisman et al., 2022), is this evidence base's clearest example of a method deliberately designed around state observability rather than fit quality alone.

- **Claim type:** Performance comparison, evidence-anchored
- **Current reference(s):** [35] Huisman et al. 2022
- **Current evidence level:** Abstract-checked
- **Current support scope:** Huisman et al. genuinely supports the state-observability-design claim for that one study; 'no family satisfies every target' is this review's own broader synthesis
- **Identified overextension:** None identified beyond the general single-study-generalization caution already applied throughout
- **Evidence needed:** Full text of Huisman et al. 2022 to confirm the externally-grounded-kernel design and its actual state-observability implications as described
- **Preferred evidence type / study design:** Primary methodological study; Deconvolution/back-calculation method paper with external kernel validation
- **Minimum number of settings:** 1 (sufficient for the specific method-design claim; full generalization not claimed)
- **Database search concepts:** wastewater deconvolution shedding kernel; effective reproduction number wastewater
- **Candidate search query:** `(wastewater) AND (deconvolution OR "shedding kernel") AND ("reproduction number" OR Rt)`
- **Full text required:** yes
- **Decision if unresolved:** retain -- claim is already appropriately scoped to one study; if full text contradicts, downgrade to 'was reported to' framing
- **Status:** Pending full-text acquisition

#### P5-4 — §5.2

> ...no formal observability analysis or synthetic-state recovery test accompanies those estimates, so the posterior's narrowness should not, by itself, be read as demonstrated observability (Dai et al., 2024).

- **Claim type:** Model validation-tier judgment
- **Current reference(s):** [44] Dai et al. 2024
- **Current evidence level:** Abstract-checked, illustrative example
- **Current support scope:** Dai et al. supports only the specific claim that no formal observability test was confirmed via this review's search; does not itself claim the general principle
- **Identified overextension:** The claim that 'no formal observability analysis... accompanies those estimates' is an absence-of-evidence claim based on this review's own search not finding one -- a meaningfully weaker evidentiary basis than a positive finding
- **Evidence needed:** Full text of Dai et al. 2024 to directly confirm whether an observability analysis is or is not present (absence claims based on abstract/search alone are the least reliable claim type)
- **Preferred evidence type / study design:** Primary methodological study, full text specifically checked for a validation/observability section; Bayesian/state-space WBE model paper
- **Minimum number of settings:** 1
- **Database search concepts:** Bayesian wastewater case prediction; state-space model wastewater surveillance validation
- **Candidate search query:** `(Bayesian OR "state-space") AND (wastewater) AND ("case count" OR prediction) AND (validation OR observability)`
- **Full text required:** yes
- **Decision if unresolved:** qualify -- if full text cannot be obtained, reword from 'no formal observability analysis... accompanies' (an absence claim) to 'no formal observability analysis was identified in this review's search of the available abstract/summary' -- a precision fix independent of new evidence
- **Status:** Pending full-text acquisition; wording-precision fix recommended regardless

#### P5-6 — §5.3

> ...a machine-learning approach achieving useful short-horizon predictive performance across several sewersheds, evaluated on a genuine train/test split, still contains no individually interpretable parameter and no explicit latent-state representation at all... (Ai et al., 2022).

- **Claim type:** Model validation-tier judgment
- **Current reference(s):** [38] Ai et al. 2022 (⚠ metadata partially unresolved)
- **Current evidence level:** Abstract-checked, metadata incomplete
- **Current support scope:** Ai et al. supports the specific study-design characterization; the general principle is this review's own
- **Identified overextension:** [38]'s own author-list metadata is unresolved (⚠ flag) -- a metadata gap layered on top of the full-text gap
- **Evidence needed:** (1) full-text confirmation of study design; (2) independent confirmation of full author list
- **Preferred evidence type / study design:** Primary ML/WBE study; Multi-community ML prediction study with explicit train/test split
- **Minimum number of settings:** 1 (already multi-community within the one study)
- **Database search concepts:** machine learning wastewater outbreak prediction; multi-community wastewater ML train test
- **Candidate search query:** `("machine learning" OR "random forest" OR "neural network") AND (wastewater) AND (outbreak OR prediction) AND (community)`
- **Full text required:** yes
- **Decision if unresolved:** retain -- claim is well-scoped already (a logical, not empirical, point); resolve the author-list metadata gap independently of the full-text question
- **Status:** Pending full-text acquisition + independent author-list re-verification

#### P6-2 — §6.2

> A four-system integration of hospital, wastewater, meteorological, and internet-search data into one shared time series found a substantial subset of the fused variables correlating significantly with clinical case counts (Zhang et al., 2025), illustrating that fusion can outperform any single stream.

- **Claim type:** Performance comparison
- **Current reference(s):** [58] Zhang et al. 2025
- **Current evidence level:** Abstract-checked (metadata-verified)
- **Current support scope:** Single study, single city (southern China per source draft); 'illustrating that fusion can outperform any single stream' is this review's own generalization from one study
- **Identified overextension:** 'Illustrating that fusion can outperform any single stream' risks reading as a general finding when it rests on one city's data; should be checked against full text for how directly the study itself makes this comparative claim
- **Evidence needed:** Full text of Zhang et al. 2025 to confirm the actual correlation-improvement magnitude and whether the study itself claims fusion outperforms single streams, or whether that is this review's inference
- **Preferred evidence type / study design:** Primary multi-source data-fusion study; Multi-city or multi-site data-fusion comparison against single-stream baselines
- **Minimum number of settings:** 2 (currently 1 -- one Chinese city)
- **Database search concepts:** multi-source surveillance data fusion; wastewater hospital search-query integration
- **Candidate search query:** `(wastewater) AND (fusion OR integration OR "multi-source") AND (hospital OR clinical) AND (surveillance)`
- **Full text required:** yes
- **Decision if unresolved:** narrow -- if full text does not directly support the 'outperform any single stream' framing, narrow to 'in the studied Chinese city...' per the cross-city evidentiary rule
- **Status:** Pending full-text acquisition + targeted search for a second city/setting

#### P6-4 — §6.3

> ...non-sewered populations are structurally, not merely incidentally, invisible to this method, and a national assessment finds sewer connectivity systematically, not randomly, associated with specific demographic and geographic factors (Yu et al., 2024)... a documented instance exists of a wastewater detection being traced upstream to a specific residence (Moallef et al., 2025).

- **Claim type:** Ethics/equity -- empirical + documented-instance
- **Current reference(s):** [52] Yu et al. 2024; [51] Moallef et al. 2025
- **Current evidence level:** Abstract-checked (both metadata-verified)
- **Current support scope:** Yu et al. supports the connectivity-inequity finding specifically for the U.S. only; Moallef et al. supports one documented re-identification instance (already correctly singular after this round's fix), not a rate or frequency claim
- **Identified overextension:** None remaining after this round's fix (see Phase 2B Risk Log); U.S.-only scope of Yu et al. should be made explicit if not already
- **Evidence needed:** Full text of both studies; confirm Yu et al.'s finding is U.S.-specific and not implicitly generalized; confirm Moallef et al.'s re-identification example's actual documentation quality
- **Preferred evidence type / study design:** Yu et al.: primary field/data-analysis study (already appropriate design). Moallef et al.: verify whether the re-identification example is the review's own primary finding or a citation to a third source; National infrastructure/connectivity assessment (Yu et al.); critical review methodology (Moallef et al.)
- **Minimum number of settings:** Not applicable for the documented-instance claim (n=1 is the claim itself); Yu et al.'s U.S.-only scope should be flagged explicitly if ever generalized
- **Database search concepts:** sewer connectivity equity; wastewater surveillance health equity; wastewater re-identification privacy case
- **Candidate search query:** `("sewer connectivity" OR "sanitation access") AND (equity OR disparities); ("wastewater surveillance") AND (privacy OR "re-identification") AND (case OR incident)`
- **Full text required:** yes
- **Decision if unresolved:** qualify -- add explicit '(U.S.-specific finding)' qualifier to the Yu et al. citation if full text confirms U.S.-only scope, per this review's own cross-population generalizability rule
- **Status:** Pending full-text acquisition (both studies)

#### P7-2 — §7.2

> ...a national metrology working group argues standardized reporting and proficiency testing are necessary, not merely desirable, preconditions for cross-laboratory data to be used reliably in public-health decisions (Keenum et al., 2024).

- **Claim type:** Methodological/policy argument, evidence-anchored
- **Current reference(s):** [64] Keenum et al. 2024 (⚠ duplicated-surname flag); [63] Pagsuyoin et al. 2025
- **Current evidence level:** Abstract-checked
- **Current support scope:** Already correctly framed as 'a national metrology working group argues' (one group's position, not consensus) -- confirmed non-overextended in Phase 2B's citation audit
- **Identified overextension:** None in the claim itself; the [64] author-list inconsistency (duplicated 'Gushgari' surname) remains an unresolved metadata gap independent of the claim's framing
- **Evidence needed:** (1) full text of Keenum et al. 2024 to resolve the author-list duplication and confirm the position paper's actual scope/authority; (2) full text of Pagsuyoin et al. 2025
- **Preferred evidence type / study design:** Position paper (already identified); independent confirmation of author list; Not applicable (position/policy paper, not an empirical study)
- **Minimum number of settings:** Not applicable
- **Database search concepts:** wastewater surveillance standardization; interlaboratory proficiency testing wastewater; reference materials wastewater qPCR
- **Candidate search query:** `(wastewater) AND (standardization OR "proficiency testing" OR "reference material") AND (surveillance OR qPCR)`
- **Full text required:** yes
- **Decision if unresolved:** retain -- claim is already appropriately hedged; resolve the author-list metadata issue independently via a targeted re-search (not a full-text question)
- **Status:** Pending full-text acquisition + independent author-list re-verification for [64]

## 6. What this plan does not do

- It does not run any database search — no Web of Science, Scopus, or PubMed query has been executed, and no hit counts are reported or fabricated anywhere in this document.
- It does not obtain or read any full text — `full_text_read` remains `no` for all 67 active references; the 0/67 full-text-verification denominator is unchanged by this document's existence.
- It does not revise, narrow, or remove any claim beyond the single [57] edit described in §3, which was a clear single-preprint overextension already identified and authorized for correction this round, not a new full-text-driven revision.
- It does not constitute or imply submission readiness. Full-text verified: 0/67. Submission ready: No.
