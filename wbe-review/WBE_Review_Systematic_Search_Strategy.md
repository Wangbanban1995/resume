# Systematic Search Strategy — WBE Review (revised, still NOT executed)

**Status.** This document specifies ready-to-run search strategies for Web of Science, Scopus, and PubMed, restructured this round into one core search plus seven complementary module searches (eight searches total) per instruction. It has not been executed. This session has no access to Web of Science, Scopus, or any bibliographic-database API, and WebFetch returns HTTP 403 for every publisher, PMC, and PubMed URL tested — see Section 12 for the tested basis of that statement. Someone with institutional database access must run these strategies and return the outputs listed in Section 13.

---

## 1. Why one core search plus seven complementary modules, not one combined string

The previous version of this document used a single string (`WBE core AND at least one methodological block`). That structure silently excludes any record that describes a mechanistic, chemical, or analytical WBE-relevant finding without using an explicit WBE label — for example, an in-sewer biofilm decay study, a drug-excretion pharmacokinetics paper, or a pre-2010s sewage chemistry paper that predates the term "wastewater-based epidemiology" entirely. Running eight separate searches (one core search plus seven complementary modules) and merging afterward, rather than one narrow AND-combined string, is the correct way to avoid that recall failure. Each module below is self-contained: its own concept terms, its own Web of Science / Scopus / PubMed syntax, and its own hit-count row to be filled in by the person who executes it. Do not combine modules into a single string at execution time — run all eight, export all eight result sets, and deduplicate afterward (Section 10).

---

## 2. Core search — WBE terminology and population inference

### 2.1 Expanded core synonym set

In addition to the terms already used in the previous version, the following were evaluated and are included below: *wastewater epidemiology; sewage-based epidemiology; sewer epidemiology; sewage surveillance; wastewater monitoring; community wastewater; municipal wastewater; wastewater biomarker; sewage biomarker;* and three compound phrases — *(wastewater analysis AND population); (wastewater AND community health); (wastewater AND population consumption); (wastewater AND infection incidence/prevalence)*.

**"Environmental surveillance" is deliberately excluded as a standalone term.** Used alone it retrieves air, soil, and general environmental-monitoring literature far outside this review's scope. It is used only in the fixed phrase "wastewater environmental surveillance" or paired with wastewater/sewage/sewer, consistent with instruction.

### 2.2 Web of Science

```
TS=("wastewater-based epidemiology" OR "wastewater-based surveillance"
     OR "wastewater surveillance" OR "wastewater epidemiology"
     OR "sewage epidemiology" OR "sewage-based epidemiology"
     OR "sewer epidemiology" OR "sewage surveillance"
     OR "wastewater monitoring" OR "community wastewater"
     OR "municipal wastewater" OR "wastewater biomarker*"
     OR "sewage biomarker*"
     OR (wastewater NEAR/3 (population OR "community health"
         OR consumption OR incidence OR prevalence)))
```

### 2.3 Scopus

```
TITLE-ABS-KEY("wastewater-based epidemiology" OR "wastewater-based surveillance"
     OR "wastewater surveillance" OR "wastewater epidemiology"
     OR "sewage epidemiology" OR "sewage-based epidemiology"
     OR "sewer epidemiology" OR "sewage surveillance"
     OR "wastewater monitoring" OR "community wastewater"
     OR "municipal wastewater" OR "wastewater biomarker*"
     OR "sewage biomarker*"
     OR (wastewater W/3 (population OR "community health"
         OR consumption OR incidence OR prevalence)))
```

### 2.4 PubMed

PubMed has no native proximity operator comparable to NEAR/W — phrase and MeSH combinations substitute for it, per instruction.

```
("wastewater-based epidemiology"[tiab] OR "wastewater-based surveillance"[tiab]
 OR "wastewater surveillance"[tiab] OR "wastewater epidemiology"[tiab]
 OR "sewage epidemiology"[tiab] OR "sewage-based epidemiology"[tiab]
 OR "sewer epidemiology"[tiab] OR "sewage surveillance"[tiab]
 OR "wastewater monitoring"[tiab] OR "community wastewater"[tiab]
 OR "municipal wastewater"[tiab] OR "wastewater biomarker*"[tiab]
 OR "sewage biomarker*"[tiab]
 OR ("wastewater"[tiab] AND (population[tiab] OR "community health"[tiab]
     OR consumption[tiab] OR incidence[tiab] OR prevalence[tiab]))
 OR "Wastewater-Based Epidemiological Monitoring"[mh])
```

**This core search block is itself Module 1** (WBE core and population inference) — it is run and exported on its own, not only as a filter for the other eight.

---

## 3. Module 2 — Sewer transport and in-sewer transformation

Built as an **independent** search that does not require a WBE label, per instruction — otherwise foundational sewer-process literature that never uses "wastewater-based epidemiology" is missed entirely.

### Web of Science
```
TS=((sewer* OR "wastewater network*" OR "sewer system*")
     NEAR/5 (biomarker* OR virus* OR pathogen* OR pharmaceutical* OR metabolite*))
AND
TS=(decay OR degradation OR transformation OR sorption OR partition*
     OR sediment* OR resuspension OR biofilm* OR "residence time" OR "travel time")
```

### Scopus
```
TITLE-ABS-KEY((sewer* OR "wastewater network*" OR "sewer system*")
     W/5 (biomarker* OR virus* OR pathogen* OR pharmaceutical* OR metabolite*))
AND
TITLE-ABS-KEY(decay OR degradation OR transformation OR sorption OR partition*
     OR sediment* OR resuspension OR biofilm* OR "residence time" OR "travel time")
```

### PubMed
```
((sewer*[tiab] OR "wastewater network*"[tiab] OR "sewer system*"[tiab])
 AND (biomarker*[tiab] OR virus*[tiab] OR pathogen*[tiab] OR pharmaceutical*[tiab] OR metabolite*[tiab]))
AND
(decay[tiab] OR degradation[tiab] OR transformation[tiab] OR sorption[tiab] OR partition*[tiab]
 OR sediment*[tiab] OR resuspension[tiab] OR biofilm*[tiab] OR "residence time"[tiab] OR "travel time"[tiab])
```

Title/abstract screening decides relevance to WBE signal interpretation specifically — this module is intentionally broader than Chapters 3–4's scope at the search stage, per instruction, so genuine sewer-process studies are not pre-filtered out by requiring a WBE label they were never written with.

---

## 4. Module 3 — Rainfall, infiltration/inflow, and CSO

Standalone, and deliberately not limited to "rainfall dilution" — rainfall affects wastewater signals through multiple, distinct mechanisms (dilution, resuspension, network hydraulics, overflow bypass), not dilution alone.

### Web of Science
```
TS=(sewer* OR wastewater OR sewage)
AND
TS=(rainfall OR precipitation OR "wet weather" OR "storm event*" OR "first flush"
     OR "infiltration and inflow" OR "inflow and infiltration"
     OR "combined sewer overflow*" OR "sanitary sewer overflow*"
     OR dilution OR "antecedent dry period" OR "hydraulic residence time")
```

### Scopus
```
TITLE-ABS-KEY(sewer* OR wastewater OR sewage)
AND
TITLE-ABS-KEY(rainfall OR precipitation OR "wet weather" OR "storm event*" OR "first flush"
     OR "infiltration and inflow" OR "inflow and infiltration"
     OR "combined sewer overflow*" OR "sanitary sewer overflow*"
     OR dilution OR "antecedent dry period" OR "hydraulic residence time")
```

### PubMed
```
(sewer*[tiab] OR wastewater[tiab] OR sewage[tiab])
AND
(rainfall[tiab] OR precipitation[tiab] OR "wet weather"[tiab] OR "storm event*"[tiab]
 OR "first flush"[tiab] OR "infiltration and inflow"[tiab] OR "inflow and infiltration"[tiab]
 OR "combined sewer overflow*"[tiab] OR "sanitary sewer overflow*"[tiab]
 OR dilution[tiab] OR "antecedent dry period"[tiab] OR "hydraulic residence time"[tiab])
```

---

## 5. Module 4 — Sampling and analytical uncertainty

### Web of Science
```
TS=(wastewater OR sewage OR sewer*)
AND
TS=("grab sampl*" OR "composite sampl*" OR "recovery efficiency" OR "PCR inhibition"
     OR "limit of detection" OR "limit of quantification" OR "matrix effect*"
     OR "process control*" OR "extraction efficiency")
```

### Scopus
```
TITLE-ABS-KEY(wastewater OR sewage OR sewer*)
AND
TITLE-ABS-KEY("grab sampl*" OR "composite sampl*" OR "recovery efficiency" OR "PCR inhibition"
     OR "limit of detection" OR "limit of quantification" OR "matrix effect*"
     OR "process control*" OR "extraction efficiency")
```

### PubMed
```
(wastewater[tiab] OR sewage[tiab] OR sewer*[tiab])
AND
("grab sampl*"[tiab] OR "composite sampl*"[tiab] OR "recovery efficiency"[tiab] OR "PCR inhibition"[tiab]
 OR "limit of detection"[tiab] OR "limit of quantification"[tiab] OR "matrix effect*"[tiab]
 OR "process control*"[tiab] OR "extraction efficiency"[tiab])
```

---

## 6. Module 5 — Normalization and population biomarkers

### Web of Science
```
TS=(wastewater OR sewage)
AND
TS=("flow normaliz*" OR "population normaliz*" OR PMMoV OR crAssphage
     OR "biomarker normaliz*" OR "fecal indicator*" OR "population biomarker*"
     OR creatinine OR caffeine OR paraxanthine OR ammonia OR "dynamic population")
```

### Scopus
```
TITLE-ABS-KEY(wastewater OR sewage)
AND
TITLE-ABS-KEY("flow normaliz*" OR "population normaliz*" OR PMMoV OR crAssphage
     OR "biomarker normaliz*" OR "fecal indicator*" OR "population biomarker*"
     OR creatinine OR caffeine OR paraxanthine OR ammonia OR "dynamic population")
```

### PubMed
```
(wastewater[tiab] OR sewage[tiab])
AND
("flow normaliz*"[tiab] OR "population normaliz*"[tiab] OR PMMoV[tiab] OR crAssphage[tiab]
 OR "biomarker normaliz*"[tiab] OR "fecal indicator*"[tiab] OR "population biomarker*"[tiab]
 OR creatinine[tiab] OR caffeine[tiab] OR paraxanthine[tiab] OR ammonia[tiab] OR "dynamic population"[tiab])
```

---

## 7. Module 6 — Chemical WBE and back-calculation

### Web of Science
```
TS=(wastewater OR sewage)
AND
TS=("illicit drug*" OR pharmaceutical* OR "drug consumption" OR "human metabolite*"
     OR "exposure biomarker*" OR "excretion factor*" OR "correction factor*"
     OR "back calculation" OR "back-calculation" OR "mass balance"
     OR "population size estimation")
```

### Scopus
```
TITLE-ABS-KEY(wastewater OR sewage)
AND
TITLE-ABS-KEY("illicit drug*" OR pharmaceutical* OR "drug consumption" OR "human metabolite*"
     OR "exposure biomarker*" OR "excretion factor*" OR "correction factor*"
     OR "back calculation" OR "back-calculation" OR "mass balance"
     OR "population size estimation")
```

### PubMed
```
(wastewater[tiab] OR sewage[tiab])
AND
("illicit drug*"[tiab] OR pharmaceutical*[tiab] OR "drug consumption"[tiab] OR "human metabolite*"[tiab]
 OR "exposure biomarker*"[tiab] OR "excretion factor*"[tiab] OR "correction factor*"[tiab]
 OR "back calculation"[tiab] OR "back-calculation"[tiab] OR "mass balance"[tiab]
 OR "population size estimation"[tiab])
```

---

## 8. Module 7 — Pathogen reconstruction and epidemiological modelling

### Web of Science
```
TS=(wastewater OR sewage)
AND
TS=("pathogen shedding" OR "viral shedding" OR "fecal shedding"
     OR "shedding distribution" OR "shedding kernel" OR "incidence estimation"
     OR "prevalence estimation" OR deconvolution OR "reproduction number"
     OR nowcast* OR "state-space" OR "compartmental model*" OR SEIR
     OR "latent infection state")
```

### Scopus
```
TITLE-ABS-KEY(wastewater OR sewage)
AND
TITLE-ABS-KEY("pathogen shedding" OR "viral shedding" OR "fecal shedding"
     OR "shedding distribution" OR "shedding kernel" OR "incidence estimation"
     OR "prevalence estimation" OR deconvolution OR "reproduction number"
     OR nowcast* OR "state-space" OR "compartmental model*" OR SEIR
     OR "latent infection state")
```

### PubMed
```
(wastewater[tiab] OR sewage[tiab])
AND
("pathogen shedding"[tiab] OR "viral shedding"[tiab] OR "fecal shedding"[tiab]
 OR "shedding distribution"[tiab] OR "shedding kernel"[tiab] OR "incidence estimation"[tiab]
 OR "prevalence estimation"[tiab] OR deconvolution[tiab] OR "reproduction number"[tiab]
 OR nowcast*[tiab] OR "state-space"[tiab] OR "compartmental model*"[tiab] OR SEIR[tiab]
 OR "latent infection state"[tiab])
```

---

## 9. Module 8 — Uncertainty, identifiability, and validation

### Web of Science
```
TS=(wastewater OR sewage)
AND
TS=("uncertainty propagat*" OR "Monte Carlo" OR "error propagat*" OR "sensitivity analysis"
     OR "censored data" OR nondetect OR "parameter identifiability"
     OR "structural identifiability" OR "practical identifiability"
     OR "state observability" OR validation)
```

### Scopus
```
TITLE-ABS-KEY(wastewater OR sewage)
AND
TITLE-ABS-KEY("uncertainty propagat*" OR "Monte Carlo" OR "error propagat*" OR "sensitivity analysis"
     OR "censored data" OR nondetect OR "parameter identifiability"
     OR "structural identifiability" OR "practical identifiability"
     OR "state observability" OR validation)
```

### PubMed
```
(wastewater[tiab] OR sewage[tiab])
AND
("uncertainty propagat*"[tiab] OR "Monte Carlo"[tiab] OR "error propagat*"[tiab] OR "sensitivity analysis"[tiab]
 OR "censored data"[tiab] OR nondetect[tiab] OR "parameter identifiability"[tiab]
 OR "structural identifiability"[tiab] OR "practical identifiability"[tiab]
 OR "state observability"[tiab] OR validation[tiab])
```

---

## 10. Proximity operators — database-specific syntax used above

| Concept | Web of Science | Scopus | PubMed substitute |
|---|---|---|---|
| Sewer transport terms near degradation terms | `NEAR/5` | `W/5` | phrase + AND (no native proximity) |
| Population near normalization | `NEAR/3` | `W/3` | `"population normaliz*"` as a fixed phrase instead |
| Wastewater near back-calculation | not used directly — Module 6 uses plain AND | not used directly | plain AND |
| Uncertainty near propagation | folded into fixed phrase `"uncertainty propagat*"` | same | same |

Truncation (`*`) is used throughout for word-ending variants (e.g., `sewer*` = sewer/sewers/sewershed; `pharmaceutical*` = pharmaceutical/pharmaceuticals). No module relies on a single, fully-fixed phrase alone — every module combines at least 6–10 term variants per concept to avoid the narrow-single-phrase failure mode flagged in the review of the prior version.

---

## 11. Date and language scope — sensitivity check required at execution

The previous version fixed 2000–present, English-only, without testing that choice. At execution, run in this order:

1. **First, run each module with no date restriction ("earliest available" to present)** and record the year of the earliest 20 hits for each module.
2. **Inspect whether pre-2000 records include substantively relevant environmental-monitoring or wastewater-inference studies** (e.g., early poliovirus environmental surveillance, pre-1990s sewage chemistry). If yes, lower the date floor accordingly rather than assuming 2000 is safe.
3. **Record the non-English hit count separately** for every module (Web of Science and Scopus both support a language facet without excluding at query time; PubMed's `[la]` filter can be run as a second, comparison query). Do not discard this count — report it.
4. **If non-English records are ultimately excluded from full-text review**, state this explicitly as a documented **language bias** in the review's limitations section, with the excluded count named, not merely implied.

---

## 12. Preprint and conference-paper stratification

Do not merge these three evidence tiers when reporting search results or building the final citation set:

- **Peer-reviewed journal articles** — eligible for the review's primary evidence base without further flagging beyond this review's existing evidence-type classification (primary WBE study / systematic review / general methodology).
- **Preprints** (arXiv, medRxiv, bioRxiv, SSRN, ChemRxiv) — tag separately at export. At screening, search for a subsequently published peer-reviewed version by title and author list; if found, use the published version and drop the preprint from the counted total (retain a note of the correspondence, as this review already does for [27] Hsu et al.'s possible medRxiv counterpart and [22] Zafeiriadou et al.'s SSRN-to-published-version correction). If no published version exists, retain the preprint but keep its "preprint, not peer-reviewed" tag through every downstream table — this review already does this for [37], [39], and [45].
- **Conference proceedings papers** — treat as method-discovery sources only (i.e., useful for finding that a technique exists or a group is working on a problem), not as standalone support for a specific quantitative or comparative finding in the main text, consistent with how this review already treats non-primary sources.

---

## 13. Citation tracking (backward, forward, and seed recall)

Formal database searching alone is not sufficient and must be paired with:

- **Backward citation searching**: pull the reference lists of the review's existing systematic reviews already in evidence ([2] Boogaerts et al., [12] Punch et al., [17] Zhu et al., [34] Ahmed et al., [40] Wang et al.) and check their cited primary studies against the search results — any primary study cited by an existing systematic review that the new search did not retrieve is a specific, checkable recall failure.
- **Forward citation searching ("cited by")**: for the same five reviews plus the highest-value primary studies ([13] Rainey et al., [35] Huisman et al., [44] Dai et al.), pull papers that cite them and screen for relevance.
- **Seed-recall check against this review's existing 51 references**: run the finished search strategy and confirm it retrieves the peer-reviewed/preprint items already cited in this review. Institutional/policy/news sources ([1], [4], [5], [11], [14], [15]) and one institutional program report ([7]) are excluded from this check since they are not indexed journal records a bibliographic-database search would be expected to return.

**Recall test set (44 of 51 references; 7 institutional/policy/program-report sources excluded per above), tagged by primary module.** This table is also machine-readable as `systematic-review/templates/seed_studies.csv`, which is the authoritative, executable version of this list — use the CSV with `scripts/check_seed_recall.py`, not manual transcription from this table.

| Module | Seed references to confirm are recalled |
|---|---|
| 1 — WBE core | [2] Boogaerts et al. (2024); [12] Punch et al. (2025); [17] Zhu et al. (2025); [25] Chen et al. (2024); [34] Ahmed et al. (2026) |
| 2 — Sewer transport | [6] Guo et al. (2023); [9] Jung et al. (2026); [10] Miura et al. (2021); [16] Zhang et al. (2023) |
| 3 — Rainfall/CSO | [3] Darling et al. (2025); [8] Janssens et al. (2022) |
| 4 — Sampling/analytical | [18] Ahmed et al. (2022); [19] Cha et al. (2023); [20] Kim et al. (2022); [21] Williams et al. (2024); [22] Zafeiriadou et al. (2024); [23] Elbait et al. (2024); [24] Pecson et al. (2021) |
| 5 — Normalization | [13] Rainey et al. (2023); [26] Langeveld et al. (2022); [27] Hsu et al. (2022); [28] Maal-Bared et al. (2023); [29] Dhiyebi et al. (2023); [30] Chen et al. (2014); [31] Been et al. (2014); [32] Baz-Lomba et al. (2019); [32b] Thomas et al. (2017); [33] Chettleburgh et al. (2023) |
| 6 — Chemical back-calculation | [36] Ramin et al. (2017); [41] Zuccato et al. (2008); [46] Jones et al. (2014); [49] Pei et al. (2016); [50] Croft et al. (2020) |
| 7 — Pathogen reconstruction | [35] Huisman et al. (2022); [38] Ai et al. (2022); [40] Wang et al. (2026); [42] McMahan et al. (2021); [43] Schoen et al. (2022); [44] Dai et al. (2024); [45] Alhassan et al. (2025) |
| 8 — Uncertainty/identifiability | [37] Deva et al. (2021); [39] Liyanage et al. (2025); [47] Yang et al. (2024); [48] Safford et al. (2022) |

**Correction (this round):** [13] Rainey et al. (2023) — a flow-vs-biomarker normalization comparison across 182 U.S. communities, this review's strongest-corroborated normalization finding — was omitted from this table in the prior version despite clearly belonging to Module 5. It is added here and in `seed_studies.csv`, bringing the normalization module's seed count from 9 to 10 and the total from the previously-miscounted "45 of 51" to the correct **44 of 51** (51 total − 7 excluded institutional/policy/program-report sources, not 6 — the prose above already named 7: six institutional/policy/news sources plus [7], one institutional program report).

**If any of the 45 seed references above is not retrieved by its assigned module's search string, the string must be revised and re-tested before the search is considered final** — a formal search strategy that fails to recall its own review's already-identified core evidence is not fit for use, regardless of how comprehensive its terminology otherwise looks on paper.

---

## 14. Peer review of the search strategy (PRESS)

Before execution, the strategy above should be checked by at least one person familiar with systematic-review search methodology (a research librarian or equivalent), against the **PRESS** (Peer Review of Electronic Search Strategies) checklist:

- Concept coverage — are the core search's and all 7 complementary modules' concept blocks complete relative to the review's actual scope (Chapters 3–8)?
- Boolean and proximity logic — correct nesting, no unintended AND/OR precedence errors
- Spelling and truncation — correct truncation symbols per database (`*` here; confirm no database-specific deviation, e.g., Ovid platforms use different wildcard characters if PubMed is later run via Ovid MEDLINE instead of PubMed directly)
- Line/syntax translation — correct field-tag translation across the three databases (Section 10's table)
- Over-restriction — no unnecessary limits beyond Section 11's date/language plan
- Missed limiters — check whether document-type or subject-area limiters are silently over- or under-inclusive
- **Seed recall** — confirm Section 13's 45-reference recall check was actually run and passed, not merely planned

This review does not have a research librarian available in-session; this checklist is provided so the eventual executor (or their institution) can apply it before results are treated as final.

---

## 15. Merging, deduplication, and PRISMA (to be performed after execution, not now)

1. Export all 8 search result sets (Section 2 core search + Modules 2–8 complementary searches) separately, in RIS or CSV, each retaining its module tag.
2. Merge into one master list; deduplicate first by DOI, then by normalized title+year+first-author for records lacking a DOI.
3. Record, per module: raw hit count, and post-dedup unique contribution (i.e., how many records that module uniquely contributed that no other module also retrieved) — this quantifies whether the 8-module restructuring actually captured records the single-string approach would have missed, which is the entire point of this round's revision.
4. Only after deduplication does formal PRISMA counting begin (identified → duplicates removed → title/abstract screened → full texts sought → full texts assessed → included), with exclusion reasons logged at each stage.
5. **No PRISMA numbers are produced by this document or by this session** — Section 16 states why.

---

## 16. What could not be done and why (tested this session)

This section states plainly what this review's environment can and cannot do:

- **No Web of Science or Scopus access exists in this environment.** A tool-registry search for any such connector returned none. There is no institutional login, API key, or MCP connector available to this session for either database.
- **PubMed's own search interface is not reachable either.** WebFetch was re-tested against `pubmed.ncbi.nlm.nih.gov` and a DOI-resolved publisher link and returned HTTP 403 Forbidden both times, consistent with every attempt made throughout this project across Chapters 1–8.
- **Consequently, no genuine hit count, deduplication count, or PRISMA number can be produced without fabricating it**, and none is presented in this document. Any hit-count or PRISMA figure attributed to this session should be treated as unverified.
- **Full-text retrieval remains blocked for all 51 existing references**, for the same reason.

## 17. What this session can still do without database or full-text access

- Maintain and further refine this strategy so it is ready to execute the moment access exists.
- Screen titles/abstracts if the user or an executor supplies the raw RIS/CSV/BibTeX export from running Sections 2–9 above.
- Perform the seed-recall check in Section 13 manually against a supplied export.
- Read and audit full text directly for any paper the user supplies as a PDF or pasted text — this session can do genuine page-level verification for anything provided directly, even though it cannot fetch it independently.

---

## 18. Deliverables expected back from whoever executes this strategy

- Raw export files (RIS, BibTeX, or CSV) for the core search and all 7 complementary modules (8 searches total), kept separate before merging
- Per-module raw hit count and post-dedup unique-contribution count (Section 15.3)
- Full search history log or screenshots showing the exact string executed per database (query strings can silently auto-correct or truncate in some database interfaces — a log confirms what was actually run, not just what was intended)
- Pre- and post-deduplication total record counts
- Confirmation of the Section 13 seed-recall check outcome (pass/fail per module, with any string revisions made in response)
- A list of records for which full text could not be obtained even with institutional access, and why (paywall beyond subscription, retracted, no digital copy, etc.)

Until these are returned, per instruction: Chapters 1–8 remain frozen, Chapter 9 does not start, no further Word/layout work is performed, no hypothetical PRISMA numbers are generated, and the Evidence Freeze Audit continues to report the true 0/51 full-text-verification state.
