# Systematic Search Strategy — WBE Review (drafted, NOT executed)

**Status: this document specifies formal, ready-to-run search strategies for Web of Science, Scopus, and PubMed. It has not been executed. This session has no access to Web of Science, Scopus, or any bibliographic database API — see the "What could not be done and why" section at the end of this file for the specific, tested basis for that statement. These strategies are provided so that a person or system with institutional database access can run them and return the export files this review needs.**

---

## 1. Scope and PICO-style framing

This review spans five methodological domains (Chapters 3–8): source-to-sample signal formation and sewer transformation (Ch. 3–4); sampling and analytical methods (Ch. 5); normalization (Ch. 6); back-calculation/identifiability/validation (Ch. 7); and uncertainty propagation (Ch. 8). A single search strategy covering all five is used, with chapter-relevance taggable via the concept blocks below, rather than five independent searches — consistent with how the review itself is organized around one inverse-problem framework rather than five disconnected topics.

- **Population/setting:** municipal or community wastewater/sewershed systems
- **Exposure/method:** wastewater-based epidemiology, surveillance, or monitoring — sampling, analysis, normalization, back-calculation, or uncertainty quantification applied to it
- **Outcome:** any of — signal fate/transport, sampling/analytical performance, normalization performance, back-calculation/reconstruction method, or uncertainty-propagation method
- **Study types:** primary research articles, systematic reviews, and methodological/modelling studies; conference proceedings and non-peer-reviewed preprints included but flagged separately at screening

## 2. Concept blocks (used identically across all three databases, translated into each syntax below)

- **Block A — WBE core:** wastewater-based epidemiology; wastewater surveillance; sewage epidemiology; environmental surveillance (wastewater-specific only)
- **Block B — Signal/transport:** sewer transport; in-sewer decay; RNA/biomarker degradation; sewershed; catchment; combined sewer overflow; rainfall dilution; inflow infiltration
- **Block C — Sampling/analytical:** grab sampling; composite sampling; recovery efficiency; PCR inhibition; limit of detection; limit of quantification; matrix effect
- **Block D — Normalization:** flow normalization; population normalization; PMMoV; crAssphage; biomarker normalization; fecal indicator
- **Block E — Back-calculation/identifiability:** back-calculation; deconvolution; shedding kernel; parameter identifiability; state-space model; Bayesian reconstruction; effective reproduction number wastewater
- **Block F — Uncertainty:** uncertainty propagation; Monte Carlo; error propagation; sensitivity analysis; censored data; nondetect

A record is eligible if it matches Block A AND at least one of Blocks B–F.

## 3. Web of Science (Core Collection) — full search string

Field tags: TS = Topic (title, abstract, author keywords, Keywords Plus).

```
TS=("wastewater-based epidemiology" OR "wastewater surveillance" OR "sewage epidemiology"
    OR "wastewater-based surveillance")
AND
TS=("sewer transport" OR "in-sewer decay" OR "biomarker degradation" OR sewershed OR catchment
    OR "combined sewer overflow" OR "rainfall dilution" OR "inflow and infiltration"
    OR "grab sampling" OR "composite sampling" OR "recovery efficiency" OR "PCR inhibition"
    OR "limit of detection" OR "limit of quantification" OR "matrix effect"
    OR "flow normalization" OR "population normalization" OR PMMoV OR crAssphage
    OR "biomarker normalization" OR "fecal indicator"
    OR "back-calculation" OR deconvolution OR "shedding kernel" OR "parameter identifiability"
    OR "state-space model" OR "Bayesian reconstruction" OR "effective reproduction number"
    OR "uncertainty propagation" OR "Monte Carlo" OR "error propagation" OR "sensitivity analysis"
    OR "censored data" OR nondetect)
```

- **Refined by:** Document Types = Article OR Review Article OR Proceedings Paper OR Early Access
- **Language:** English (with a documented, unsearched exclusion count for non-English records)
- **Timespan:** 2000-01-01 to present (2026-07-13) — 2000 chosen as a conservative lower bound predating modern WBE's post-2010s growth, to avoid an artificial recency cutoff
- **Database:** Web of Science Core Collection (SCI-EXPANDED, SSCI; Conference Proceedings Citation Index optional second pass)
- **Search date field to record at execution:** exact run date/time, database version/coverage date, and the searcher's institution (coverage varies by subscription)

## 4. Scopus — full search string

Field tags: TITLE-ABS-KEY.

```
TITLE-ABS-KEY("wastewater-based epidemiology" OR "wastewater surveillance" OR "sewage epidemiology"
    OR "wastewater-based surveillance")
AND
TITLE-ABS-KEY("sewer transport" OR "in-sewer decay" OR "biomarker degradation" OR sewershed OR catchment
    OR "combined sewer overflow" OR "rainfall dilution" OR "inflow and infiltration"
    OR "grab sampling" OR "composite sampling" OR "recovery efficiency" OR "PCR inhibition"
    OR "limit of detection" OR "limit of quantification" OR "matrix effect"
    OR "flow normalization" OR "population normalization" OR PMMoV OR crAssphage
    OR "biomarker normalization" OR "fecal indicator"
    OR "back-calculation" OR deconvolution OR "shedding kernel" OR "parameter identifiability"
    OR "state-space model" OR "Bayesian reconstruction" OR "effective reproduction number"
    OR "uncertainty propagation" OR "Monte Carlo" OR "error propagation" OR "sensitivity analysis"
    OR "censored data" OR nondetect)
AND PUBYEAR > 1999
AND (LIMIT-TO(DOCTYPE,"ar") OR LIMIT-TO(DOCTYPE,"re") OR LIMIT-TO(DOCTYPE,"cp"))
AND (LIMIT-TO(LANGUAGE,"English"))
```

## 5. PubMed — full search string

Field tags: [tiab] = title/abstract, [mh] = MeSH term.

```
("wastewater-based epidemiology"[tiab] OR "wastewater surveillance"[tiab] OR "sewage epidemiology"[tiab]
    OR "wastewater-based surveillance"[tiab] OR "Wastewater-Based Epidemiological Monitoring"[mh])
AND
("sewer transport"[tiab] OR "in-sewer decay"[tiab] OR "biomarker degradation"[tiab] OR sewershed[tiab]
    OR catchment[tiab] OR "combined sewer overflow"[tiab] OR "rainfall dilution"[tiab]
    OR "inflow and infiltration"[tiab] OR "grab sampling"[tiab] OR "composite sampling"[tiab]
    OR "recovery efficiency"[tiab] OR "PCR inhibition"[tiab] OR "limit of detection"[tiab]
    OR "limit of quantification"[tiab] OR "matrix effect"[tiab] OR "flow normalization"[tiab]
    OR "population normalization"[tiab] OR PMMoV[tiab] OR crAssphage[tiab]
    OR "biomarker normalization"[tiab] OR "fecal indicator"[tiab] OR "back-calculation"[tiab]
    OR deconvolution[tiab] OR "shedding kernel"[tiab] OR "parameter identifiability"[tiab]
    OR "state-space model"[tiab] OR "Bayesian reconstruction"[tiab]
    OR "effective reproduction number"[tiab] OR "uncertainty propagation"[tiab]
    OR "Monte Carlo"[tiab] OR "error propagation"[tiab] OR "sensitivity analysis"[tiab]
    OR "censored data"[tiab] OR nondetect[tiab])
AND ("2000/01/01"[dp] : "3000"[dp])
AND (english[la])
NOT (comment[pt] OR editorial[pt])
```

- **PubMed-specific note:** MeSH term "Wastewater-Based Epidemiological Monitoring" was introduced 2023 and will not tag pre-2023 records retrospectively in all cases — the [tiab] terms are the primary recall mechanism, MeSH is supplementary.

## 6. What could not be done and why (tested this session, 2026-07-13)

This section states plainly what this review's environment can and cannot do, so the remediation plan below is built on a real, tested constraint rather than an assumption:

- **No Web of Science or Scopus access exists in this environment.** A tool-registry search for any Web of Science, Scopus, or bibliographic-database connector returned no such tool. There is no institutional login, API key, or MCP connector available to this session for either database. This is not a permissions issue that can be worked around — the capability simply is not present.
- **PubMed's own search/E-utilities interface is not reachable either.** WebFetch — the only tool capable of retrieving a live web page's content — was re-tested against `pubmed.ncbi.nlm.nih.gov` and a DOI-resolved publisher link immediately before this document was written, and both returned HTTP 403 Forbidden, consistent with every attempt made throughout this entire project (Chapters 1–8). This means this session cannot execute the PubMed string above and retrieve a real hit count, cannot page through PubMed results, and cannot retrieve PubMed's structured XML/CSV export.
- **Consequently, no genuine hit count, deduplication count, or PRISMA flow-diagram number can be produced for any of the three databases without fabricating it.** Per this review's standing rule against fabrication, no such numbers are presented here. Any document showing specific hit counts for these three searches, produced by this session, should be treated as unverified until someone with actual database access runs the strings above and reports the real numbers back.
- **Full-text retrieval remains blocked for all 51 references already in this review**, for the same reason (WebFetch 403 on every publisher/PMC/DOI-resolver domain, retested this session). This means items 4–6 of the requested remediation (full-text verification table, paragraph-level claim audit against page numbers, and cell-level Table 3–6 evidence audit) cannot be produced with real page/table/figure citations by this session under current tool access.

## 7. What this session can still do without database or full-text access

- Maintain and refine the search strategy above so it is ready to execute the moment access exists.
- Screen titles/abstracts of records if the user (or someone with access) supplies the raw export (RIS/CSV/BibTeX) from running the searches above — title/abstract screening does not require full-text access.
- Continue flagging every quantitative claim in Chapters 1–8 as "pending full-text verification," which the review already does systematically via the Citation Verification Table and Pending Verification List.
- Read and audit full text directly if the user supplies PDFs or pasted full text for specific papers — this session can do genuine page-level verification for any paper the user provides directly, even though it cannot fetch that paper itself.
