#!/usr/bin/env python3
"""Builds WBE_Review_Full_Text_Request_List.csv -- the first-batch full-text
acquisition list: the 21 references already used in the condensed draft, the
7 already-known-but-not-yet-cited source-draft references needed to close
citation-attribution gaps flagged in the Critical/High queue, and 3 genuinely
new search candidates (no real paper identified yet -- placeholders only,
never fabricated titles/authors) for gaps with no existing citable source.
Does NOT record 'visible in a search summary' as 'full text obtained' --
every row's obtained/read fields are 'no' as of this round."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "WBE_Review_Full_Text_Request_List.csv"

FIELDS = ["priority", "reference_number_or_candidate_id", "title", "first_author", "year",
          "journal_or_platform", "DOI_or_identifier", "publication_type", "cited_claim",
          "full_text_source", "access_status", "obtained", "read", "relevant_pages",
          "relevant_table_or_figure", "support_outcome", "notes"]

NOT_OBTAINED = {
    "obtained": "no", "read": "no", "relevant_pages": "N/A -- full text not obtained",
    "support_outcome": "N/A -- not yet assessed",
}

# The 21 references already cited in the condensed draft.
USED = [
    {"priority": "P0", "reference_number_or_candidate_id": "16",
     "title": "The reduction of SARS-CoV-2 RNA concentration in the presence of sewer biofilms",
     "first_author": "Zhang, S.", "year": "2023", "journal_or_platform": "Water",
     "DOI_or_identifier": "10.3390/w15112132", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P3-3 -- biofilm RNA loss mechanism (§3.2)",
     "full_text_source": "MDPI open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": "Open-access journal; acquisition should be straightforward once formal search phase begins."},
    {"priority": "P0", "reference_number_or_candidate_id": "9",
     "title": "Environmental and microbial factors shaping SARS-CoV-2 RNA decay in wastewater: Insights from batch tests and a lab-scale sewer pipeline simulator",
     "first_author": "Jung, J.", "year": "2026", "journal_or_platform": "Scientific Reports",
     "DOI_or_identifier": "10.1038/s41598-026-44857-y", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P3-3 -- biofilm/pipeline-simulator decay mechanism (§3.2)",
     "full_text_source": "Nature Scientific Reports open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P0", "reference_number_or_candidate_id": "8",
     "title": "SARS-CoV-2 surveillance in Belgian wastewaters", "first_author": "Janssens, R.", "year": "2022",
     "journal_or_platform": "Viruses", "DOI_or_identifier": "10.3390/v14091950",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P3-7 -- rainfall/correlation-improvement finding (§3.4)",
     "full_text_source": "MDPI open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P0", "reference_number_or_candidate_id": "13",
     "title": "A multistate assessment of population normalization factors for wastewater-based epidemiology of COVID-19",
     "first_author": "Rainey, A. L.", "year": "2023", "journal_or_platform": "PLOS ONE",
     "DOI_or_identifier": "10.1371/journal.pone.0284370", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P3-9, P4-5, P4-10 -- cross-hydrologic-condition and flow-normalization findings (§3.5, §4.2, Table 2)",
     "full_text_source": "PLOS ONE open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "Table 2 (flow-normalization row)", "notes": "Supports 3 separate Critical rows -- high-value acquisition target."},
    {"priority": "P0", "reference_number_or_candidate_id": "3",
     "title": "Comparative assessment of wastewater-based surveillance normalization methods to improve pathogen monitoring in rural sewersheds",
     "first_author": "Darling, A.", "year": "2025", "journal_or_platform": "Environmental Science & Technology",
     "DOI_or_identifier": "10.1021/acs.est.4c14485", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P3-9, P4-5, P4-10 -- cross-hydrologic-condition and flow-normalization findings (§3.5, §4.2, Table 2)",
     "full_text_source": "ACS Publications (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 2 (flow-normalization row)", "notes": "Supports 3 separate Critical rows -- high-value acquisition target."},
    {"priority": "P0", "reference_number_or_candidate_id": "35",
     "title": "Wastewater-based estimation of the effective reproductive number of SARS-CoV-2",
     "first_author": "Huisman, J. S.", "year": "2022", "journal_or_platform": "Environmental Health Perspectives",
     "DOI_or_identifier": "PMID 35617001 (DOI not independently confirmed)", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- deconvolution/reconstruction-model row (§5.5, Table 3)",
     "full_text_source": "EHP open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "Table 3 (deconvolution row)", "notes": "DOI needs independent confirmation before citing formally."},
    {"priority": "P0", "reference_number_or_candidate_id": "44",
     "title": "A Bayesian framework for modeling COVID-19 case numbers through longitudinal monitoring of SARS-CoV-2 RNA in wastewater",
     "first_author": "Dai, X.", "year": "2024", "journal_or_platform": "Statistics in Medicine",
     "DOI_or_identifier": "10.1002/sim.10009", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- Bayesian/state-space row and identifiability/observability discussion (§5.5, Table 3)",
     "full_text_source": "Wiley (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 3 (Bayesian/state-space row)", "notes": "Also the source of the absence-of-evidence claim (\"no formal observability analysis accompanies those estimates\") -- full text needed to confirm this absence is genuine, not a search-summary omission."},
    {"priority": "P0", "reference_number_or_candidate_id": "38",
     "title": "Application of machine learning for multi-community COVID-19 outbreak predictions with wastewater surveillance",
     "first_author": "Ai, Y.", "year": "2022", "journal_or_platform": "PLOS ONE",
     "DOI_or_identifier": "10.1371/journal.pone.0277154 (pattern-inferred, not independently confirmed)",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- hybrid/ML row, implied (§5.5, Table 3)",
     "full_text_source": "PLOS ONE open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "Table 3 (hybrid/ML row)", "notes": "⚠ author-list metadata partially unresolved (see References.md) -- resolve before formal citation, independent of full-text read."},
    {"priority": "P0", "reference_number_or_candidate_id": "57",
     "title": "Wastewater surveillance as an event detection system: Outbreak and peak detection of SARS-CoV-2 across 281 U.S. counties",
     "first_author": "Link, N. B.", "year": "2026", "journal_or_platform": "medRxiv (preprint)",
     "DOI_or_identifier": "medRxiv 2026.05.14.26353186", "publication_type": "Non-peer-reviewed preprint",
     "cited_claim": "P6-1 -- threshold-transportability conclusion (§6.1)",
     "full_text_source": "medRxiv open access (preprint text itself readable now; formal version not yet identified)",
     "access_status": "Preprint openly accessible; formal peer-reviewed version status unknown -- not yet searched",
     "relevant_table_or_figure": "N/A", "notes": "See also candidate row CAND-P6-1-FORMAL below for the formal-version search target."},
    {"priority": "P1", "reference_number_or_candidate_id": "2",
     "title": "Current state and future perspectives on de facto population markers for normalization in wastewater-based epidemiology: A systematic literature review",
     "first_author": "Boogaerts, T.", "year": "2024", "journal_or_platform": "Science of the Total Environment",
     "DOI_or_identifier": "10.1016/j.scitotenv.2024.173223", "publication_type": "Peer-reviewed systematic review",
     "cited_claim": "Background -- population-marker landscape (Part 4 general background)",
     "full_text_source": "ScienceDirect (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "6",
     "title": "Effects of temperature and water types on the decay of coronavirus: A review", "first_author": "Guo, Y.",
     "year": "2023", "journal_or_platform": "Water", "DOI_or_identifier": "10.3390/w15061051",
     "publication_type": "Peer-reviewed review article", "cited_claim": "Background -- temperature-decay review (Part 3 general background)",
     "full_text_source": "MDPI open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "11",
     "title": "Wastewater-based disease surveillance for public health action", "first_author": "NASEM",
     "year": "2023", "journal_or_platform": "National Academies Press",
     "DOI_or_identifier": "10.17226/26767", "publication_type": "Institutional report",
     "cited_claim": "Background -- institutional framing citation (Part 1/6 general background)",
     "full_text_source": "National Academies Press open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "46",
     "title": "Illicit and pharmaceutical drug consumption estimated via wastewater analysis. Part B: Placing back-calculations in a formal statistical framework",
     "first_author": "Jones, H. E.", "year": "2014", "journal_or_platform": "Science of the Total Environment",
     "DOI_or_identifier": "not independently confirmed", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "Background -- source-end uncertainty exemplar (Part 5 general background)",
     "full_text_source": "ScienceDirect (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "51",
     "title": "Advancing health equity in wastewater-based epidemiology: A global critical review and conceptual framework",
     "first_author": "Moallef, S.", "year": "2025", "journal_or_platform": "SSM - Population Health",
     "DOI_or_identifier": "10.1016/j.ssmph.2025.101786", "publication_type": "Peer-reviewed critical review",
     "cited_claim": "P6-4 -- equity/re-identification example (§6.3)",
     "full_text_source": "ScienceDirect (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": "Phase 2B already corrected a plural/singular overextension for this reference (\"documented instances\" -> \"a documented instance\"); full text still needed to confirm the single example's details."},
    {"priority": "P1", "reference_number_or_candidate_id": "52",
     "title": "Assessment of sewer connectivity in the United States and its implications for equity in wastewater-based epidemiology",
     "first_author": "Yu, Q.", "year": "2024", "journal_or_platform": "PLOS Global Public Health",
     "DOI_or_identifier": "10.1371/journal.pgph.0003039", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P6-4 -- structural sewer-connectivity coverage-gap argument (§6.3)",
     "full_text_source": "PLOS open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "55",
     "title": "Wastewater surveillance can function as an early warning system for COVID-19 in low-incidence settings",
     "first_author": "Assoum, M.", "year": "2023", "journal_or_platform": "Tropical Medicine and Infectious Disease",
     "DOI_or_identifier": "10.3390/tropicalmed8040211", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P6-2 -- surveillance-objective distinction example (§6.1)",
     "full_text_source": "MDPI open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "58",
     "title": "Comparative performance of wastewater, clinical, and digital surveillance indicators for COVID-19 monitoring in routine practice: Retrospective observational study",
     "first_author": "Zhang, X.", "year": "2025", "journal_or_platform": "Journal of Medical Internet Research",
     "DOI_or_identifier": "10.2196/70232", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P6-2 -- multi-source data-fusion study (§6.2)",
     "full_text_source": "JMIR open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "60",
     "title": "Passive sampling of SARS-CoV-2 for wastewater surveillance", "first_author": "Schang, C.",
     "year": "2021", "journal_or_platform": "Environmental Science & Technology",
     "DOI_or_identifier": "10.1021/acs.est.1c01530", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "Part 7.1 -- process-resolving infrastructure example (§7.1)",
     "full_text_source": "ACS Publications (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": "Author-attribution correction already applied in References.md (citogenesis-artifact catch, not a full-text issue)."},
    {"priority": "P1", "reference_number_or_candidate_id": "61",
     "title": "Digital twin applications in the water sector: A review", "first_author": "Bam, P. G.", "year": "2025",
     "journal_or_platform": "Water", "DOI_or_identifier": "N/A (MDPI web page)",
     "publication_type": "Peer-reviewed review article", "cited_claim": "Part 7.1 -- process-resolving infrastructure trend evidence (§7.1)",
     "full_text_source": "MDPI open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "63",
     "title": "Coupling wastewater-based epidemiology with data-driven machine learning for managing public health risks",
     "first_author": "Pagsuyoin, S.", "year": "2025", "journal_or_platform": "Risk Analysis",
     "DOI_or_identifier": "10.1111/risa.70075", "publication_type": "Peer-reviewed narrative review",
     "cited_claim": "Part 7.2 -- process-informed analytics background (§7.2)",
     "full_text_source": "Wiley (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": ""},
    {"priority": "P1", "reference_number_or_candidate_id": "64",
     "title": "Optimizing wastewater surveillance: The necessity of standardized reporting and proficiency for public health",
     "first_author": "Keenum, I.", "year": "2024", "journal_or_platform": "American Journal of Public Health",
     "DOI_or_identifier": "10.2105/AJPH.2024.307760", "publication_type": "Peer-reviewed position paper",
     "cited_claim": "P7-2 -- standardization/proficiency-testing conclusion (§7.3)",
     "full_text_source": "AJPH (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A", "notes": "⚠ duplicated-surname author-list inconsistency unresolved -- resolve independent of full-text read."},
]

# 7 citation-restoration candidates: already in References.md, already used in the
# source draft's evidence base, but not currently inline-cited in the condensed draft.
RESTORATION = [
    {"priority": "P0", "reference_number_or_candidate_id": "30",
     "title": "Towards finding a population biomarker for wastewater epidemiology studies",
     "first_author": "Chen, C.", "year": "2014", "journal_or_platform": "Science of the Total Environment",
     "DOI_or_identifier": "10.1016/j.scitotenv.2013.11.075 (pattern-inferred, not independently confirmed)",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P4-6, P4-10 -- creatinine/cotinine biomarker performance (§4.3, Table 2)",
     "full_text_source": "ScienceDirect (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 2 (biomarker row)",
     "notes": "Citation-attribution gap, not a full-text gap: already in the source draft's evidence base (References.md [30]), simply not carried into the condensed draft's inline prose/table. Independently fixable now regardless of full-text outcome."},
    {"priority": "P0", "reference_number_or_candidate_id": "28",
     "title": "Does normalization of SARS-CoV-2 concentrations by Pepper Mild Mottle Virus improve correlations and lead time between wastewater surveillance and clinical data in Alberta (Canada): Comparing twelve SARS-CoV-2 normalization approaches",
     "first_author": "Maal-Bared, R.", "year": "2023", "journal_or_platform": "Science of the Total Environment",
     "DOI_or_identifier": "not independently confirmed (ScienceDirect ID S0048969722060636)",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P4-6, P4-10 -- PMMoV normalization performance (§4.3, Table 2)",
     "full_text_source": "ScienceDirect (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 2 (biomarker row)",
     "notes": "Citation-attribution gap, not a full-text gap -- see [30]'s note; same fix applies."},
    {"priority": "P0", "reference_number_or_candidate_id": "29",
     "title": "Assessment of seasonality and normalization techniques for wastewater-based surveillance in Ontario, Canada",
     "first_author": "Dhiyebi, H. A.", "year": "2023", "journal_or_platform": "Frontiers in Public Health",
     "DOI_or_identifier": "10.3389/fpubh.2023.1186525", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P4-6, P4-10 -- crAssphage normalization performance (§4.3, Table 2)",
     "full_text_source": "Frontiers open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "Table 2 (biomarker row)",
     "notes": "Citation-attribution gap, not a full-text gap -- see [30]'s note; same fix applies."},
    {"priority": "P0", "reference_number_or_candidate_id": "41",
     "title": "Estimating community drug abuse by wastewater analysis", "first_author": "Zuccato, E.", "year": "2008",
     "journal_or_platform": "Environmental Health Perspectives", "DOI_or_identifier": "not independently confirmed",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- direct mass-balance row anchor (§5.5, Table 3)",
     "full_text_source": "EHP open access", "access_status": "Open access -- not yet retrieved this round",
     "relevant_table_or_figure": "Table 3 (direct mass-balance row)",
     "notes": "Citation-attribution gap, not a full-text gap: already in the source draft's evidence base (References.md [41]) as the foundational mass-balance example, simply not carried into the condensed Table 3."},
    {"priority": "P0", "reference_number_or_candidate_id": "43",
     "title": "SARS-CoV-2 RNA wastewater settled solids surveillance frequency and impact on predicted COVID-19 incidence using a distributed lag model",
     "first_author": "Schoen, M. E.", "year": "2022", "journal_or_platform": "ACS ES&T Water",
     "DOI_or_identifier": "not independently confirmed", "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- empirical-regression row anchor (§5.5, Table 3)",
     "full_text_source": "ACS Publications (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 3 (empirical-regression row)",
     "notes": "Citation-attribution gap, not a full-text gap -- see [41]'s note; same fix applies."},
    {"priority": "P0", "reference_number_or_candidate_id": "42",
     "title": "COVID-19 wastewater epidemiology: A model to estimate infected populations", "first_author": "McMahan, C. S.",
     "year": "2021", "journal_or_platform": "The Lancet Planetary Health", "DOI_or_identifier": "not independently confirmed",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P5-10 -- mechanistic transport-decay row anchor (§5.5, Table 3)",
     "full_text_source": "The Lancet (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "Table 3 (mechanistic transport-decay row)",
     "notes": "Citation-attribution gap, not a full-text gap -- see [41]'s note; same fix applies."},
    {"priority": "P1", "reference_number_or_candidate_id": "24",
     "title": "Reproducibility and sensitivity of 36 methods to quantify the SARS-CoV-2 genetic signal in raw wastewater: Findings from an interlaboratory methods evaluation in the U.S.",
     "first_author": "Pecson, B. M.", "year": "2021", "journal_or_platform": "Environmental Science: Water Research & Technology",
     "DOI_or_identifier": "10.1039/D0EW00946F (pattern-inferred, not independently confirmed)",
     "publication_type": "Peer-reviewed primary study",
     "cited_claim": "P4-2 -- 36-SOP interlaboratory recovery/inhibition finding (§4.1)",
     "full_text_source": "RSC Publishing (subscription likely required)", "access_status": "Not yet checked",
     "relevant_table_or_figure": "N/A",
     "notes": "Citation-attribution gap, not a full-text gap: already in the source draft's evidence base (References.md [24]), simply not carried into the condensed draft's §4.1 as an inline citation."},
]

# 3 genuinely new search candidates -- no real paper identified yet. Titles/authors are
# deliberately NOT filled in to avoid fabricating a source; these are placeholders naming
# only the evidence gap and the search module that should resolve them.
NEW_CANDIDATES = [
    {"priority": "P0", "reference_number_or_candidate_id": "CAND-P3-6-A",
     "title": "Not yet identified -- pending search", "first_author": "Not yet identified",
     "year": "N/A", "journal_or_platform": "N/A", "DOI_or_identifier": "N/A",
     "publication_type": "Unknown -- target: peer-reviewed hydraulic/sewer-hydrology primary study",
     "cited_claim": "P3-6 -- sediment resuspension, retention-time shortening, sub-catchment weight shift during storms (§3.4), currently entirely uncited",
     "full_text_source": "N/A -- not yet searched",
     "access_status": "Not yet searched (see Targeted Search Addendum module 2: rainfall/infiltration/hydraulic disturbance)",
     "relevant_table_or_figure": "N/A",
     "notes": "No existing citable source in References.md for this specific sub-mechanism claim -- a genuine new-search gap, not a citation-restoration gap."},
    {"priority": "P0", "reference_number_or_candidate_id": "CAND-P4-5-B",
     "title": "Not yet identified -- pending search", "first_author": "Not yet identified",
     "year": "N/A", "journal_or_platform": "N/A", "DOI_or_identifier": "N/A",
     "publication_type": "Unknown -- target: peer-reviewed study on industrial/non-domestic discharge limits on flow-based normalization",
     "cited_claim": "P4-5 -- industrial/non-domestic-discharge-limits-on-normalization claim (§4.2), currently entirely uncited",
     "full_text_source": "N/A -- not yet searched",
     "access_status": "Not yet searched (see Targeted Search Addendum module 4: wastewater normalization biomarkers)",
     "relevant_table_or_figure": "N/A",
     "notes": "No existing citable source in References.md for this specific claim -- a genuine new-search gap."},
    {"priority": "P0", "reference_number_or_candidate_id": "CAND-P6-1-FORMAL",
     "title": "Not yet identified -- pending search for a formal peer-reviewed version of [57] (Link, Garrido, et al., 2026 medRxiv preprint), or an independent second study",
     "first_author": "Not yet identified", "year": "N/A", "journal_or_platform": "N/A", "DOI_or_identifier": "N/A",
     "publication_type": "Unknown -- target: peer-reviewed event/outbreak-detection performance study",
     "cited_claim": "P6-1 -- threshold-transportability conclusion (§6.1); Option A/B resolution for the [57] single-preprint issue",
     "full_text_source": "N/A -- not yet searched",
     "access_status": "Not yet searched (see Targeted Search Addendum module 9: alert thresholds and transportability)",
     "relevant_table_or_figure": "N/A",
     "notes": "This round applied Option C (narrowing) to §6.1 in the absence of this source -- see WBE_Review_Evidence_Recovery_Plan.md §3. This row remains open for a future round's Option A/B search."},
]


def main():
    rows = USED + RESTORATION + NEW_CANDIDATES
    for r in rows:
        r.update({k: v for k, v in NOT_OBTAINED.items() if k not in r})
        missing = [f for f in FIELDS if f not in r]
        if missing:
            raise SystemExit(f"Row {r.get('reference_number_or_candidate_id')} missing fields: {missing}")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in FIELDS})

    print(f"Wrote {len(rows)} rows to {OUT}")
    print(f"  Already-used references: {len(USED)}")
    print(f"  Citation-restoration candidates (existing refs, not yet inline-cited): {len(RESTORATION)}")
    print(f"  New search candidates (no source identified yet): {len(NEW_CANDIDATES)}")
    print(f"  obtained=yes count (should be 0): {sum(1 for r in rows if r['obtained'] == 'yes')}")
    print(f"  read=yes count (should be 0): {sum(1 for r in rows if r['read'] == 'yes')}")


if __name__ == "__main__":
    main()
