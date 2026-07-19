# Consolidated Pending-Verification List — WBE Review, Chapters 1–10

Every number, coefficient, percentage, or ranking below is currently supported only by search-engine-summarized snippets, not by full-text reading (WebFetch returned HTTP 403 for every publisher/PMC/DOI-resolver/Crossref domain attempted across this entire project — see §2.3 of the main document). **None of these should be quoted in a submission-facing document without independent full-text confirmation.** Organized by chapter; reference numbers match `WBE_Review_References.md` and `WBE_Review_Citation_Verification_Table.md`.

---

## Chapters 1–2 (background, methodology)

- EU Wastewater Surveillance Dashboard: "11 countries" and "over one million measurements" [4]
- WHO WES pilot guidance: full PDF content not read page-by-page beyond release date/existence [15]
- China's national wastewater surveillance system: "roughly doubled" poliovirus isolation figure; 3-component description [7] — **author list for [7] also incomplete**
- Recast UWWTD: "100,000 population-equivalent" AMR-monitoring threshold [5] — **author list for [5] also unconfirmed**
- AMR wastewater scoping review: "177 reports," "76.8% after 2019" [12]
- "247 articles" figure for the normalization systematic review — **now resolved/confirmed**, see [34]; retained here only as a reminder it was previously on this list

## Chapter 3–4 (source signal, sewer transport, rainfall)

- Coronavirus RNA decay acceleration "above ~26 °C" threshold [6]
- Sewer biofilm reactor "~90% reduction within 2 hours" figure [16]
- In-sewer decay rate constants (k ≈ 2.21 d⁻¹ vs. 1.12–0.47 d⁻¹) [9]
- Miura, Kitajima, & Omori (2021) [10] — **internally inconsistent across searches** (3.4 vs. 2.6 log copies/g; 26.0-day vs. 20–32-day range); do not cite either number without reading the primary source directly

## Chapter 5 (sampling and analytical methods)

- RT-qPCR vs. RT-dPCR process-limit-of-detection CVs, "~40–60%" [18]
- Settled-solids enrichment magnitude ("~3 orders of magnitude," "10³–10⁴×") [20] — note main text already flags contradictory partitioning ratios from other studies
- 36-SOP U.S. interlaboratory comparison: "~7 log₁₀" recovery/LOD range; "~2.3 log₁₀ GC" recovery-corrected spread [24]
- Storage/freeze-thaw specific recovery differentials (qualitative direction confirmed; exact percentages not asserted in text) [21]
- PCR-inhibition mitigation-strategy performance figures [22]
- ARG qPCR-vs-metagenomics concordance figures [23]
- Grab (≈30%) vs. flow-proportional composite (<10%) sampling uncertainty — **removed from main-text prose in the 2026-07-12 revision**; retained only in references/verification table, itself a restatement by a preprint survey [25] of an unidentified primary source

## Chapter 6 (normalization)

- Langeveld et al. (2022): exact study-design figures (9 sites, ~1,100 samples) [26]
- Hsu et al. (2022): specific performance-ranking magnitudes for paraxanthine vs. PMMoV/creatinine/5-HIAA across 64 WWTPs [27] — **also: unresolved relationship to a same-author-group medRxiv preprint on Missouri statewide monitoring; treat as possibly one dataset, not two**
- Maal-Bared et al. (2023): "2 of 12 systems" figure; pooled correlation-improvement magnitude for ammonia/TKN/TP [28]
- Dhiyebi et al. (2023): site-specific correlation-reduction magnitudes for PMMoV normalization [29]
- Chen et al. (2014): which 2 of 7 candidate biomarkers were "most promising" (recurred consistently across searches — comparatively higher confidence than most items on this list, but still unread in full text) [30]
- Been et al. (2014): ammonium/drug-metabolite correlation strength [31] — author list **now resolved** (Been, Rossi, Ort, Rudaz, Delémont, Esseiva); the correlation-strength claim itself remains pending
- Oslo mobile-device study: $R^2=0.88$, <10% mean error figures [32] — **author list could not be retrieved despite two separate rounds of repeated attempts across sessions; weakest author-attribution in the entire review to date**
- Southern Ontario 4-biomarker study (PMID 37660819): **now the single least-trustworthy source in this review**, for two independent reasons: (a) author list still unconfirmed after renewed attempts (one name loosely associated, not verified), and (b) a **newly discovered marker-identity discrepancy** — two searches for the same PMID described the four biomarkers studied differently (PMMoV/crAssphage/HF183/BacHuman vs. PMMoV/crAssphage/"Bacteroides rRNA"/"human 18S rRNA"). The main text and Table 3 have been revised (2026-07-12) to no longer assert which specific human-associated marker outperformed which; treat every finding attributed to this source as unresolved pending direct full-text access [33]
- Ahmed, Philo, Boehm, Halden, Bibby, & Delgado Vela (2026): "247 articles" figure and its specific findings on unspecified normalization goals — metadata and topic confirmed, but the review's own summary statistics not confirmed against its abstract/full text. **Evidence type confirmed as systematic/critical review, not a primary validation study — see the verification table's new Evidence Type column** [34]

## Chapter 7 (back-calculation, identifiability, validation)

- Huisman et al. (2022): specific quantitative comparison between wastewater-based and clinical-case-based $R_t$ estimates; whether shedding-kernel shape and $R_t$ trajectory are separably estimable in their model — qualitative method description (deconvolution + EpiEstim) is comparatively well-corroborated across searches, but this specific quantitative comparison is not [35]
- Ramin et al. (2017): specific model-comparison statistics for which transformation-pathway structures fit the heroin/codeine biomarker data and by how much [36]
- Ai et al. (2022): specific forecast error/accuracy metrics for the train/test-split ML models [38]
- Wang, Amarasiri, Oishi, & Sano (2025): the specific methodological-limitation findings this systematic review itself reports, beyond its general taxonomy (which is comparatively well-corroborated) [40]
- **Note on [37] Deva et al. 2021 and [39] Liyanage et al. 2025**: these are not pending in the same sense as the items above — they are general (non-WBE) epidemic-modeling-identifiability papers, correctly cited in §7.3 as general methodology rather than WBE-specific findings, and flagged here only as a reminder that no WBE-specific validation of their applicability to a wastewater observation equation currently exists in this review's evidence base — that gap is itself a documented finding of §7.3, not an oversight.

## Chapter 8 (uncertainty propagation)

No specific numeric probability-distribution parameters (means, standard deviations, shape parameters) are asserted anywhere in Chapter 8 as verified values — the chapter deliberately states distribution *shapes* qualitatively (e.g., "right-skewed, long-tailed," "not established as normal") rather than fitting or citing specific parameter values, and several table cells in Table 6 are explicitly labeled "shape not established in this evidence base" as a documented gap rather than an assumption. The items below are the specific claims and figures that do carry a quantitative or comparative assertion and are not yet full-text-confirmed:

- Jones et al. (2014): the specific posterior distribution/interval this Bayesian framework reports for excretion-fraction uncertainty and its propagated effect on the final per-capita consumption estimate — the qualitative framing (explicit Bayesian prior for excretion fraction, MCMC propagation) is comparatively well-corroborated across searches, but the specific numeric output is not [46]
- Yang et al. (2024): the specific variance-contribution figures for concentration method vs. extraction kit vs. primer-probe set in the factorial analytical-uncertainty comparison (§8.4) — only the qualitative ranking (concentration method contributing comparatively less variability than extraction/amplification choice) recurred across searches [47]
- Safford et al. (2022): the specific comparative-performance figures (e.g., correlation or agreement statistics) for EM-MCMC vs. substitution-based censoring methods against clinical case trends (§8.11) — the qualitative finding (EM-MCMC outperforming substitution methods) is comparatively well-corroborated, but exact figures are not [48]
- Pecson et al. (2021) 36-SOP interlaboratory comparison figures, reused in §8.4 from the existing Chapter 5 pending item — see the Chapter 5 section above [24]
- **Pei et al. (2016)** [49] and **Croft et al. (2020)** [50] (§8.7): identified and named this round, resolving the earlier "unnamed Monte Carlo study" flag on this list. Both studies' existence, authorship (Croft et al.'s fully, Pei et al.'s first 6 of 7 authors), and general design are now confirmed — what remains pending is the *specific numeric output* of each: Pei et al.'s Beijing median 2.6 kg/day methamphetamine consumption estimate and 0.58% 12-month prevalence figure, and Croft et al.'s per-capita consumption figures (e.g., the ~1660 mg/d/1000-people rural-community figure) — none of these numbers have been confirmed against full text.
- The "&gt;60–70% nondetect" heavily-censored threshold cited in the "How to Report Nondetects" box as "general environmental-statistics practice" — not attributed to a specific WBE source and not independently verified this session; stated as a general methodological convention, not a WBE-specific finding
- Jung et al. (2026) rate-constant range, cross-referenced again in §8.3 — see the existing Chapters 3–4 pending item above [9]
- Dai et al. (2024) specific predictive-accuracy figures, cross-referenced again in §8.9 — see the existing Chapter 7 pending item above [44]

## Chapter 9 (public-health integration and decision-making)

- Moallef et al. (2025): the "68 of 145 full-text-screened articles" health-equity count, and the specific content of the proposed 5-consideration conceptual framework beyond the general categories named in-text (§9.6) [51]
- Yu, Olesen, Duvallet, & Grad (2024): the specific ~80% national sewer-connectivity figure and detailed demographic-association statistics (which household characteristics associate with lower connectivity, and by how much) — the qualitative "systematically, not randomly, distributed" finding is treated as comparatively better-supported and is the claim actually relied upon in §9.5–9.6 [52]
- Thompson et al. (2024): full author list beyond the lead author; the specific legal/enforceability argument's detailed content beyond the general "obligations, not just ethics" framing (§9.6) [53]
- Kwiatkowska et al. (2022): **publication venue and peer-review status, not just a specific number** — this is a more fundamental gap than the usual "which figure is unconfirmed" pending item, and the source should be treated with corresponding extra caution until resolved (§9.6) [54]
- Assoum et al. (2023): specific lead-time or detection-sensitivity figures for the low-incidence-setting early-warning finding — no such figure is currently asserted in the main text, deliberately (§9.1, §9.2) [55]
- **[56] — ⛔ DO NOT CITE UNTIL METADATA RESOLVED.** Re-searched 2026-07-18 during the Chapter 9 consistency-audit round: still only a single, non-independently-repeated search result even for a possible co-author's name. **Withdrawn from confident in-text citation and from Table 7** as of this round — see `WBE_Review_Ch9_Claim_Audit.md` and the main text's §9.9 for how the underlying (uncited) design idea is still discussed conceptually. Any future round attempting to re-cite this reference must re-verify its basic identity from scratch, not build on any prior round's partial findings.
- **[57] — upgraded 2026-07-18.** Both named authors (Link, Garrido) now independently corroborated across two separate search results, meeting this review's ordinary citation bar; remains actively cited. What remains pending: full author list beyond these two; **and, independently of author-list completeness, whether the reported sensitivity 0.82/PPV 0.64 detection-performance figures generalize beyond the 281-county calibration set this preprint reports them on** — this second caveat is a transferability question, not merely a confirmation-pending one, and should be treated as a standing limitation even if the figures themselves are later confirmed against full text (§9.2, Table 7)
- Zhang et al. (2025): specific correlation magnitudes and per-system lead/lag relationships from the 4-system (hospital/wastewater/meteorological/internet-search) data-fusion analysis — the qualitative "fused variables correlate significantly with case counts" finding is treated as the better-supported claim (§9.3, Table 7) [58]
- The "detection-to-action timescale of about a week" reporting-timeliness figure referenced in §9.7's third actionability condition — stated explicitly in the main text as an illustrative order of magnitude from the search-derived evidence base, not a precisely established universal standard, and not attributed to a single specific numbered reference
- **No specific numeric claim in Chapter 9's Table 7 or Box is asserted as verified** — Table 7 is a structural/organizational summary of §9.1–9.2's argument, not a data table, and the Box is a purely conceptual, hypothetical illustration containing no borrowed statistics from any source

---

## Chapter 10 (enabling technologies and research infrastructures)

- Schang et al. (2021): the specific low-prevalence detection-floor figures (stated in-text as "roughly 0.03 to 0.3 cases per 10,000," explicitly hedged) — the qualitative "detects at low prevalence across 3 spatial scales" finding is the better-supported claim (§10.1) [60]
- Bam et al. (2025): the specific "58 of 147 studies (40%) apply machine learning" figure — pending full-text confirmation; the qualitative growth-trend finding (near-zero to dozens of publications/year, 2015–2025) is comparatively better corroborated (§10.3) [61]
- Sharma et al. (2024): specific concentration/turnaround figures for the biosensor assay — **explicitly not treated as establishing field or operational readiness in-text, per this chapter's technology-readiness discipline (§10.10)** (§10.2) [62]
- Pagsuyoin et al. (2025): the specific ML architectures and performance comparisons the review itself surveys — only the general hybrid mechanistic-statistical framing is relied upon in-text (§10.5) [63]
- Keenum et al. (2024): **the author list itself, not just a specific claim** — "Gushgari" appears twice with different given-name initials, an internal inconsistency not resolved this session (§10.6) [64]
- Wang et al. (2025): specific privacy-guarantee formalism and performance-vs-centralized-training comparison — **and, independently, whether this water-quality-application demonstration generalizes to epidemiological wastewater surveillance at all, a scope question this review does not claim to have answered** (§10.8) [65]
- Therrien et al. (2026): the specific adoption count and list of adopting national programs for PHES-ODM v3 — pending full-text confirmation (§10.7) [66]
- Malcom & Bowes (2025): specific taxon-prevalence percentages from the 29-paper AMR review — the qualitative *E. coli*/*Enterococcus*/*Pseudomonas* prevalence and hospital-vs-community-effluent distinction are the better-supported claims (§10.4) [67]
- The "climate trends" (nonstationary rainfall, heat, flooding) referenced in §10.9 are treated as general climate-science background not requiring WBE-specific citation, per instruction — no dedicated climate-transfer-validation study for WBE correction models was identified in this review's search, and this gap is stated explicitly in-text and in Table 8 rather than filled with an unrelated citation
- Table 8 and the accompanying Box (§10.10) contain no borrowed statistics from any source — both are explicitly labeled this review's own proposed synthesis, the same disclaimer status as Chapter 9's Table 7

## Sources with unresolved or incomplete author attribution (across all chapters)

- [5] Eurosurveillance (2026) — author list not obtained
- [7] Han et al. (2025) — author list truncated ("et al.")
- [19] Cha et al. (2023) — very long author list, truncated ("and others")
- [20] Kim et al. (2022) — author list truncated ("et al.")
- [23] Elbait et al. (2024) — author list truncated ("et al.")
- ~~[32] Oslo mobile-device study~~ — **RESOLVED 2026-07-19**: identified as Baz-Lomba et al. (2019), full 5-author list confirmed; [32b] Thomas et al. (2017) added separately, lead author only confirmed, cited for context only and not conflated with Baz-Lomba's findings
- ~~[31] Been et al. (2014)~~ — **RESOLVED 2026-07-12**: full 6-author list confirmed (Been, Rossi, Ort, Rudaz, Delémont, Esseiva)
- ~~[33] Southern Ontario 4-biomarker study~~ — **RESOLVED 2026-07-19**: identified as Chettleburgh et al. (2023), full 10-author list confirmed via PubMed's indexed record, and the marker-identity discrepancy retracted as a search-engine-summarization error (confirmed 4 markers: PMMoV, crAssphage, HF183, BacHuman)
- [46] Jones et al. (2014) — 6-author list retained from an earlier retrieval this session, not re-confirmed via a second independent search
- [47] Yang et al. (2024) — 8-author list retained from an earlier retrieval this session, not re-confirmed via a second independent search
- [49] Pei et al. (2016) — first 6 of 7 authors confirmed across 2 searches; final author name not fully confirmed
- [53] Thompson et al. (2024) — only lead author confirmed, full list not obtained
- [54] Kwiatkowska et al. (2022) — full 8-author list found, but from only a single search, not cross-checked; **and, more fundamentally, the venue itself (journal vs. conference proceeding vs. preprint) is unconfirmed**
- [56] Demir et al. (2026, medRxiv preprint) — **⛔ WITHDRAWN (2026-07-18): weakest author attribution in the entire review to date, exceeding even [32]'s previous pre-resolution record**: only the lead author's institutional affiliation is corroborated; a possible co-author's name appeared in exactly one synthesized search result and was not independently confirmed by any second source even on re-search. No longer cited anywhere in the main text or Table 7.
- [57] Link, Garrido, et al. (2026, medRxiv preprint) — **upgraded 2026-07-18**: both named authors now independently confirmed across two separate searches; full list (likely longer, given the scale of a 281-county analysis) still not obtained
- [64] Keenum et al. (2024) — the "Gushgari" surname appears twice in the retrieved author list with different given-name initials (4th and 8th author positions); not independently resolved this session — could reflect two distinct co-authors or a search-summarization duplication error

## Sources considered and explicitly excluded (not cited anywhere in Chapters 1–7)

- PMC8772136 / ScienceDirect S0048969722003813 — "Factors influencing SARS-CoV-2 RNA concentrations in wastewater up to the sampling stage: A systematic review" (~2022) — author list unconfirmed; relevant to §5, and indirectly to §6's analytical-variability discussion. **Single highest-priority gap to resolve with database access.**

## Items from the user's original project outline still not independently checked

- ~~PubMed 41260128 — "From wastewater to epidemiological insights: A systematic..."~~ — **RESOLVED**: identified and cited as [40] Wang, Amarasiri, Oishi, & Sano (2025), *Water Research*, in §7.1.2.
- arXiv 2506.14331 — sampler placement optimization — relevant to §5.1; this review's sampling-location argument was developed independently without drawing on this source, and cross-checking for consistency is recommended once accessible
- ~~PMC12005304 — wastewater-based epidemiology health equity — relevant to the not-yet-drafted §9~~ — **RESOLVED 2026-07-14**: identified and cited as [51] Moallef et al. (2025) in §9.6; see the new Chapter 9 section above for what remains pending about this specific source

---

## How to close this list

Every item above requires one of: (a) direct database/publisher access (Web of Science, Scopus, or institutional access to ScienceDirect/PMC/Water Research/ES&T, since this session's WebFetch and Crossref-API access were both blocked throughout); or (b) the user independently confirming a figure and reporting it back. Until then, this list — not the main text's prose, however confidently worded — is the authoritative record of what remains unverified in this review.
