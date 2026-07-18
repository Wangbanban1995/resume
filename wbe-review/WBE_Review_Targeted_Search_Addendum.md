# Targeted Search Addendum — 11 Modules for Critical/High Evidence Recovery

**Round:** Water Research compression, Phase 3A. 2026-07-18. **This document is search-reinforcement design only.** No search has been run against Web of Science, Scopus, PubMed, or any other database this round — this environment has no such access. No hit counts, screening numbers, or PRISMA figures appear anywhere below, and none should be inferred from this document. Each module states a gap, a search design, and the specific Critical/High claim IDs (from `WBE_Review_Critical_Claim_Verification_Queue.csv`) it is meant to resolve, so that whoever runs the eventual formal search (see `systematic-review/README.md` for the execution pipeline) can proceed directly from this document without re-deriving the rationale.

This addendum supplements, and does not replace, `WBE_Review_Systematic_Search_Strategy.md`'s existing core-plus-seven-module search strategy built for the full source draft. These 11 modules are narrower and specific to the 9 Critical + 7 High claims this round identified; several overlap conceptually with the earlier strategy's modules and should be reconciled with it, not run twice from scratch, when a real search is eventually executed.

---

## Module 1 — Sewer transformation / biofilm

- **Evidence gap:** P3-3's claim that microbial activity, not chemical hydrolysis, dominates viral-RNA loss in sewer biofilms rests on two abstract-checked sources ([16] Zhang et al. 2023, [9] Jung et al. 2026); full text is needed to confirm the mechanism was directly measured (e.g., via a biocide-inhibition control) rather than inferred from decay kinetics alone.
- **Database:** Web of Science, Scopus (biology/environmental-microbiology coverage), PubMed (secondary).
- **Core concept groups:** (sewer biofilm OR biofilm-associated) AND (SARS-CoV-2 OR viral RNA OR enteric virus) AND (decay OR degradation OR persistence) AND (mechanism OR microbial activity OR enzymatic OR hydrolysis).
- **Candidate search string:** `("sewer biofilm" OR "biofilm-associated") AND ("viral RNA" OR "SARS-CoV-2" OR "enteric virus") AND (decay OR degradation OR persistence) AND (mechanism OR "microbial activity" OR enzymatic)`.
- **Evidence types to include:** laboratory reactor studies, pipeline/sewer simulator studies, controlled decay-kinetics experiments with an explicit inhibition or sterilization control arm.
- **Exclusion conditions:** studies reporting decay without a biofilm-specific or mechanism-isolating experimental arm (e.g., bulk-liquid-only decay studies); non-peer-reviewed sources unless no peer-reviewed alternative exists.
- **Minimum acceptable evidence:** at least one peer-reviewed study with a direct experimental (not purely correlational) mechanism test.
- **Claim IDs to resolve:** P3-3.

## Module 2 — Rainfall / infiltration / hydraulic disturbance

- **Evidence gap:** P3-7's correlation-improvement finding ([8] Janssens et al. 2022) and P3-9's cross-hydrologic-condition synthesis ([13] Rainey et al. 2023, [3] Darling et al. 2025) both need full text to confirm effect magnitude, statistical significance, replication across a second country/climate, and exact site counts and infiltration/inflow (I&I) severity classifications.
- **Database:** Web of Science, Scopus.
- **Core concept groups:** (rainfall OR precipitation OR "wet weather") AND (infiltration OR inflow OR I&I) AND (wastewater OR sewer OR sewershed) AND (surveillance OR normalization OR correlation) AND (SARS-CoV-2 OR COVID-19).
- **Candidate search string:** `(rainfall OR precipitation OR "wet weather" OR infiltration OR "inflow and infiltration") AND (wastewater-based epidemiology OR WBE OR "sewage surveillance") AND (correlation OR normalization OR dilution)`.
- **Evidence types to include:** multi-site field studies explicitly comparing wet- and dry-weather performance; hydraulic/hydrologic studies with paired wastewater-surveillance outcomes.
- **Exclusion conditions:** single-site studies presented as if generalizable without an explicit generalization caveat; studies that measure rainfall only as a covariate without reporting the correlation-improvement magnitude itself.
- **Minimum acceptable evidence:** for P3-9's cross-hydrologic claim specifically, at least two independent settings or one explicit multi-site study (per this round's cross-population evidence threshold); for P3-7, the original full text with the actual reported statistic.
- **Claim IDs to resolve:** P3-7, P3-9 (primary); P3-6 (secondary — see Module 3 for the sub-mechanism-specific search).

## Module 3 — Sedimentation / resuspension / sewer memory

- **Evidence gap:** P3-6 asserts three specific sub-mechanisms by which rainfall affects wastewater signals beyond simple dilution — sediment resuspension during storms, retention-time shortening, and sub-catchment weight shift — with **no citation currently supporting any of the three** individually. This is a genuine new-search gap, not a citation-restoration gap (see `WBE_Review_Full_Text_Request_List.csv` row `CAND-P3-6-A`).
- **Database:** Web of Science, Scopus (civil/environmental engineering and sewer-hydraulics coverage).
- **Core concept groups:** (sediment resuspension OR "sewer sediment") AND (storm OR "wet weather" OR rainfall) AND (retention time OR hydraulic residence time) AND (sewershed OR sub-catchment OR "contributing area").
- **Candidate search string:** `("sewer sediment" OR "in-sewer sediment") AND (resuspension OR remobilization) AND (storm OR rainfall OR "wet weather")` — run as a separate query from `(hydraulic retention time OR residence time) AND (sewer OR wastewater collection system) AND (storm OR rainfall)`.
- **Evidence types to include:** sewer-hydraulics field or modeling studies; sediment-transport studies in combined or separate sewer systems, ideally with a wastewater-quality or pathogen-signal outcome.
- **Exclusion conditions:** general urban-drainage hydraulics studies with no wastewater-quality or signal-interpretation link; studies limited to stormwater-only systems with no sanitary/combined-sewer relevance.
- **Minimum acceptable evidence:** direct observational or experimental verification per mechanism (this is a mechanistic claim type — correlational evidence alone does not qualify, per this round's evidence thresholds).
- **Claim IDs to resolve:** P3-6.

## Module 4 — Wastewater normalization biomarkers

- **Evidence gap:** P4-6/P4-10's biomarker-performance claims (creatinine/cotinine via Chen et al. 2014 [30]; PMMoV via Maal-Bared et al. 2023 [28]; crAssphage via Dhiyebi et al. 2023 [29]) are citation-attribution gaps, not full-text gaps — these sources already exist in `WBE_Review_References.md` and need only full-text confirmation of the specific site counts and performance directions already summarized. P4-5's industrial/non-domestic-discharge-limits-on-flow-normalization claim is a genuine new-search gap with no existing citation at all.
- **Database:** Web of Science, Scopus, PubMed.
- **Core concept groups:** (population biomarker OR PMMoV OR crAssphage OR creatinine OR cotinine) AND (wastewater-based epidemiology OR normalization) AND (performance OR correlation OR lead time); separately, (industrial discharge OR non-domestic discharge OR trade waste) AND (flow normalization OR flow-based) AND (wastewater surveillance).
- **Candidate search string:** `(PMMoV OR crAssphage OR creatinine OR cotinine OR "population biomarker") AND ("wastewater-based epidemiology" OR normalization) AND (performance OR correlation)` — plus `("industrial discharge" OR "non-domestic discharge" OR "trade waste") AND ("flow normalization" OR "wastewater surveillance")` for the P4-5 sub-item.
- **Evidence types to include:** multi-site or multi-method comparative biomarker-performance studies; utility/engineering studies quantifying industrial-discharge effects on flow-based population estimates.
- **Exclusion conditions:** single-biomarker studies with no comparative baseline (for the performance-direction claim specifically); conference abstracts or non-peer-reviewed grey literature unless no alternative exists for the industrial-discharge sub-claim.
- **Minimum acceptable evidence:** original full text with explicit sample/scenario/method for the three named biomarker studies (a citation-restoration task, addressable immediately per `WBE_Review_Evidence_Recovery_Plan.md`); at least one peer-reviewed source, of any design, for the previously entirely-uncited industrial-discharge sub-claim.
- **Claim IDs to resolve:** P4-6, P4-10 (citation restoration); P4-5 (new search, industrial-discharge sub-item only).

## Module 5 — Target-normalizer fate matching

- **Evidence gap:** the broader Part 4/SI argument (not itself a single Critical/High row, but the evidentiary basis underlying P4-10's Table 2 and the SI's normalizer-performance detail) that a normalizer should share transport and decay characteristics with its target analyte. This module supports the general evidence base rather than a single named claim.
- **Database:** Web of Science, Scopus.
- **Core concept groups:** (fate OR transport OR decay) AND (target analyte OR pathogen) AND (normalizer OR population marker) AND (matching OR co-behavior OR "differential decay").
- **Candidate search string:** `(fate OR transport OR decay) AND ("target analyte" OR pathogen OR biomarker) AND (normalizer OR "population marker") AND (matching OR "co-behavior" OR "differential decay")`.
- **Evidence types to include:** comparative fate/decay studies measuring both a target pathogen/analyte and a candidate normalizer under matched conditions.
- **Exclusion conditions:** studies measuring only one of the target or the normalizer, with no direct comparison.
- **Minimum acceptable evidence:** at least one comparative fate study per major normalizer class named in `WBE_Review_Supplementary_Outline.md` §S5/§S6.
- **Claim IDs to resolve:** none individually (background support for P4-10 and the SI normalizer catalog).

## Module 6 — Identifiability and observability

- **Evidence gap:** P5-2's and P5-10's claims about non-identifiability (a model may fit observations while the target state remains non-identifiable) and the specific claim that "no formal observability analysis accompanies" the Dai et al. 2024 [44] Bayesian estimates — the latter is an absence-of-evidence claim based on this review's own search not finding something, and needs the full text checked directly to confirm the absence is genuine rather than a search-summary omission.
- **Database:** Web of Science, Scopus (applied mathematics/systems-engineering cross-listing likely needed).
- **Core concept groups:** (identifiability OR observability) AND (state-space OR Bayesian OR compartmental model) AND (wastewater-based epidemiology OR epidemiological inference).
- **Candidate search string:** `(identifiability OR observability OR "parameter identifiability") AND ("state-space model" OR "Bayesian model" OR compartmental) AND ("wastewater-based epidemiology" OR "wastewater surveillance")`.
- **Evidence types to include:** methodological/statistical papers directly addressing identifiability or observability in epidemiological state-space or Bayesian models; the full text of [44] Dai et al. 2024 itself, checked specifically for any observability analysis the abstract-level summary may have omitted.
- **Exclusion conditions:** papers using "identifiability" informally without a structural or practical identifiability analysis.
- **Minimum acceptable evidence:** the source actually checked recovery of the target state, not merely predictive fit to the observed signal (per this round's model/validation evidence threshold).
- **Claim IDs to resolve:** P5-2, P5-10.

## Module 7 — Uncertainty propagation and coverage

- **Evidence gap:** P5-4's and P5-6's claims about uncertainty-propagation methods and interval coverage across the six model families in Table 3.
- **Database:** Web of Science, Scopus.
- **Core concept groups:** (uncertainty propagation OR uncertainty quantification) AND (wastewater-based epidemiology) AND (coverage OR "confidence interval" OR "credible interval") AND (validation).
- **Candidate search string:** `("uncertainty propagation" OR "uncertainty quantification") AND ("wastewater-based epidemiology" OR "wastewater surveillance") AND (coverage OR "prediction interval" OR "credible interval")`.
- **Evidence types to include:** methodological studies reporting actual interval-coverage validation (e.g., against held-out data), not just point-estimate accuracy.
- **Exclusion conditions:** studies reporting only point estimates with no uncertainty interval at all.
- **Minimum acceptable evidence:** per the model/validation threshold, confirmation that reported intervals were checked against actual outcomes, not just internally generated.
- **Claim IDs to resolve:** P5-4, P5-6.

## Module 8 — Cross-site model validation

- **Evidence gap:** P5-10's Table 3 claims about each model family's "minimum validation" and "principal failure mode" require confirmation that the underlying studies validated across more than one site where a cross-site claim is implied.
- **Database:** Web of Science, Scopus.
- **Core concept groups:** (model validation OR external validation) AND (multi-site OR cross-site OR "multiple sewersheds") AND (wastewater-based epidemiology).
- **Candidate search string:** `("external validation" OR "multi-site validation") AND ("wastewater-based epidemiology" OR "wastewater surveillance model") AND (sewershed OR "treatment plant")`.
- **Evidence types to include:** studies validating a reconstruction or inference model against held-out sites or held-out time periods.
- **Exclusion conditions:** studies validating only in-sample (same site, same period as calibration).
- **Minimum acceptable evidence:** at least one explicit multi-site validation per model family claimed as broadly applicable in Table 3, or an explicit single-site caveat added if none is found.
- **Claim IDs to resolve:** P5-10 (secondary to Module 6); P3-9 (secondary to Module 2).

## Module 9 — Alert thresholds and transportability

- **Evidence gap:** P6-1's threshold-transportability conclusion currently rests on a single non-peer-reviewed preprint ([57] Link, Garrido, et al. 2026). This round applied Option C (narrowing the condensed-draft text; see `WBE_Review_Evidence_Recovery_Plan.md` §3) in the absence of a formal version or independent second source. This module is the target search for Options A/B in a future round. P6-2's multi-source objective-distinction example ([55] Assoum et al. 2023) also benefits from this module's search.
- **Database:** Web of Science, Scopus, PubMed, and a direct medRxiv/preprint-server check for a published version of the same DOI/author pair.
- **Core concept groups:** (event detection OR outbreak detection OR alert threshold) AND (wastewater) AND (sensitivity OR "predictive value" OR performance).
- **Candidate search string:** `("event detection" OR "outbreak detection" OR "alert threshold") AND (wastewater) AND (sensitivity OR "predictive value")` — the same string already recorded in `WBE_Review_Critical_Claim_Verification_Queue.csv`'s P6-1 row, repeated here for the module-level record.
- **Evidence types to include:** peer-reviewed event/outbreak-detection performance studies against a clinical baseline, in any country or disease context; a formal published version of the Link/Garrido preprint specifically, if one exists.
- **Exclusion conditions:** preprints (already the current evidence base and insufficient alone); studies reporting only trend-monitoring correlation without an explicit event/outbreak-detection framing.
- **Minimum acceptable evidence:** either the formal peer-reviewed version of [57] (with the version relationship to the preprint recorded, not silently substituted) or at least one independent peer-reviewed study of comparable event-detection performance from a different team/scenario — i.e., Option A or B as originally specified.
- **Claim IDs to resolve:** P6-1 (primary); P6-2 (secondary).

## Module 10 — Ethics / privacy / equity

- **Evidence gap:** P6-4's equity and re-identification claims ([51] Moallef et al. 2025, [52] Yu et al. 2024) need full text to confirm the single re-identification example's details and the sewer-connectivity coverage-gap statistics, and to classify each supporting source correctly as normative recommendation, documented empirical harm, or theoretical/anticipated risk (per this round's ethics-claim evidence threshold — guidance documents alone cannot prove a risk has actually occurred).
- **Database:** Web of Science, Scopus, PubMed (public-health-ethics and health-equity coverage).
- **Core concept groups:** (wastewater-based epidemiology OR wastewater surveillance) AND (equity OR ethics OR privacy) AND (re-identification OR "individual privacy" OR "community stigma") AND (sewer connectivity OR coverage gap).
- **Candidate search string:** `("wastewater-based epidemiology" OR "wastewater surveillance") AND (equity OR privacy OR ethics) AND ("re-identification" OR "sewer connectivity" OR "coverage gap" OR stigma)`.
- **Evidence types to include:** empirical case studies documenting an actual re-identification or coverage-gap event; governance and guidance literature, explicitly tagged as normative rather than empirical; critical reviews synthesizing equity considerations.
- **Exclusion conditions:** normative or theoretical-risk sources cited as if they were documented empirical harms without the type distinction made explicit in the text.
- **Minimum acceptable evidence:** each cited source classified as normative-recommendation, documented-empirical-harm, or theoretical-risk, with the classification stated in the manuscript text, not left implicit.
- **Claim IDs to resolve:** P6-4.

## Module 11 — Reference materials and interlaboratory standardization

- **Evidence gap:** P4-2's interlaboratory recovery/inhibition finding ([24] Pecson et al. 2021, a citation-restoration gap) and P7-2's standardized-reporting/proficiency-testing conclusion ([64] Keenum et al. 2024, which also carries an unresolved duplicated-surname author-list inconsistency, independent of the full-text question).
- **Database:** Web of Science, Scopus.
- **Core concept groups:** (interlaboratory OR proficiency testing OR reference material) AND (wastewater-based epidemiology OR SARS-CoV-2 quantification) AND (standardization OR harmonization OR reporting).
- **Candidate search string:** `(interlaboratory OR "proficiency testing" OR "reference material") AND ("wastewater-based epidemiology" OR "SARS-CoV-2 quantification") AND (standardization OR harmonization)`.
- **Evidence types to include:** interlaboratory comparison/method-evaluation studies; standardization working-group position papers, tagged as normative rather than empirical where applicable.
- **Exclusion conditions:** single-laboratory method papers presented as if establishing an interlaboratory finding.
- **Minimum acceptable evidence:** the original Pecson et al. 2021 full text for P4-2 (citation restoration); for P7-2, confirmation that the standardization argument is corroborated by more than the one position paper, or an explicit single-source caveat if not.
- **Claim IDs to resolve:** P4-2, P7-2.

---

## Summary

Eleven modules, covering all 9 Critical and 7 High claims from `WBE_Review_Critical_Claim_Verification_Queue.csv` (several claims appear in more than one module where the evidence gap has more than one facet — e.g., P3-6 spans Modules 2 and 3, P5-10 spans Modules 6 and 8). No search was executed to produce this document; it is a design artifact only, meant to be handed directly to whoever runs the next formal search round using `systematic-review/`'s existing toolkit.
