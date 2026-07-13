# Evidence Freeze Audit — WBE Review, Chapters 1–8 (2026-07-13)

This note takes a snapshot ("freeze") of the review's current evidence base before Chapter 9 begins, per instruction. It counts, per chapter: primary WBE original studies, systematic reviews, general (non-WBE) methodological literature, full-text-read sources, abstract/metadata-only sources, and paragraphs lacking a specific citation. Counts are derived from `WBE_Review_Citation_Verification_Table.md` (51 rows, references [1]–[50] plus [32b]) and a structured scan of `WBE_Review_Ch1-8.md`.

---

## 1. Reference counts by chapter and evidence type

"Institutional/policy/secondary" is used as a fourth category, not requested explicitly but necessary for honesty: WHO, EU, NASEM, Eurosurveillance, and news-commentary sources are neither primary WBE studies, systematic reviews, nor general methodological literature, and forcing them into one of those three would misrepresent them.

| Chapter | Primary WBE original study | Systematic review / secondary evidence | General (non-WBE) methodological literature | Institutional / policy / secondary source | Total references (first cited in this chapter) |
|---|---|---|---|---|---|
| 1–2 (Introduction, Methodology) | 0 | 3 ([2] Boogaerts, [12] Punch, [17] Zhu) | 0 | 7 ([1],[4],[5],[7],[11],[14],[15]) | 10 |
| 3–4 (Inverse problem, sewer transport) | 6 ([3],[8],[9],[10],[13],[16]) | 0 | 1 ([6] Guo — general coronavirus-decay review, not WBE-specific) | 0 | 7 |
| 5 (Sampling/analytical) | 7 ([18]–[24]) | 1 ([25] Chen et al., preprint survey) | 0 | 0 | 8 |
| 6 (Normalization) | 9 ([26]–[33], [32b]) | 1 ([34] Ahmed et al.) | 0 | 0 | 10 |
| 7 (Back-calculation/identifiability) | 7 ([35],[36],[38],[41],[42],[43],[44]) | 1 ([40] Wang et al.) | 3 ([37] Deva, [39] Liyanage, [45] Alhassan) | 0 | 11 |
| 8 (Uncertainty propagation, new this chapter) | 4 ([46],[48],[49],[50]) | 1 ([47] Yang et al.) | 0 | 0 | 5 |
| **Total (unique, 51 entries)** | **33** | **7** | **4** | **7** | **51** |

**Cross-chapter reuse (not double-counted above, listed for transparency):** [9] Jung et al. (Ch3–4 origin, reused Ch8 §8.3); [13] Rainey et al. and [28] Maal-Bared et al. (Ch3–4/Ch6 origin, reused in Ch7's Table 5 as normalization-stage comparison studies); [24] Pecson et al. (Ch5 origin, reused Ch8 §8.4); [44] Dai et al. and [45] Alhassan et al. (Ch7 origin, reused Ch8 §8.9/§8.12).

## 2. Full-text-read vs. abstract/metadata-only

**Full-text-read sources: 0 of 51, across every chapter.** WebFetch returned HTTP 403 for every publisher, PMC, DOI-resolver, and Crossref-API domain attempted throughout this entire project (§2.3 of the main document; confirmed repeatedly, including a dedicated Crossref-API retry). No exception exists anywhere in the evidence base.

**Abstract/metadata-only sources: 51 of 51 (100%).** Every citation in this review — including the ones with the highest metadata confidence (e.g., [13] Rainey et al., [33] Chettleburgh et al., [48] Safford et al., all resolved via PubMed-indexed records or dedicated author-list searches) — is supported only by search-engine-summarized abstracts, snippets, or metadata records, never by the full text of the source itself. This is stated once here as a blanket fact rather than re-flagged per source, consistent with the main document's practice, but is restated explicitly in this audit because it is the single most consequential limitation of the entire review to date.

## 3. Paragraphs without a specific citation — methodology and approximate counts

**Methodology and its limits, stated honestly:** an automated heuristic scan flagged paragraphs (a) longer than ~150 characters, (b) containing an evidentiary-sounding word ("found," "reported," "showed," "documented," "study," "evidence," etc.), and (c) lacking a bracketed reference number or an "et al./(year)" pattern nearby. This heuristic substantially **over-flags**: most of what it catches is this review's own original conceptual, definitional, or argumentative content — formal equations, the five-way identifiability distinction (§7.0), the uncertainty-type taxonomy (§8.1), section-bridge paragraphs, table/box framing sentences — which correctly carries no citation because it is the review's analytical contribution, not an empirical claim borrowed from a source. It is not a reliable count of actual evidentiary gaps, and manual review of the flagged list is required before treating any specific paragraph as an uncited claim needing a citation.

| Chapter | Total paragraphs (approx.) | Flagged by heuristic | Flagged as share of total |
|---|---|---|---|
| 1 | 12 | 1 | 8% |
| 2 | 23 | 4 | 17% |
| 3 | 20 | 2 | 10% |
| 4 | 16 | 1 | 6% |
| 5 | 46 | 10 | 22% |
| 6 | 78 | 21 | 27% |
| 7 | 51 | 14 | 27% |
| 8 | 97 | 22 | 23% |
| **Total** | **343** | **75** | **22%** |

**Manual spot-check of the flagged list (not exhaustive) confirms the over-flagging pattern:** e.g., the Chapter 6 item "This is not merely a theoretical risk. A 2026 systematic review of 247 published articles..." is in fact citing [34] Ahmed et al. in the same paragraph (the automated pattern simply didn't match this particular in-text citation format); most Chapter 7–8 flagged items are the chapters' own organizing-framework sentences (§7.0's five-way distinction restated, §8.0's marginalization-equation gloss, structural-bridge paragraphs), not empirical claims. **No paragraph identified in this pass was found, on manual spot-check, to assert a specific quantitative or comparative empirical finding without a supporting citation** — the review's practice of flagging every quantitative claim explicitly (per the Pending Verification List) appears, on this spot-check, to hold. This is a spot-check, not an exhaustive line-by-line audit, and should not be read as a guarantee that zero such gaps exist.

## 4. What this audit does and does not establish

This audit **does** establish, as a documented fact rather than an impression: the review's evidence base leans heavily on primary WBE studies (33 of 51, 65%) with a meaningful general-methodology contribution specifically in Chapter 7 (identifiability theory, 3 of 11 chapter references), that institutional/secondary sources are concentrated entirely in the introductory chapters (7 of 7 in Ch. 1–2, 0 elsewhere), and that zero sources have been read in full text at any point in this project.

This audit does **not** establish that the review is free of unsupported claims — the paragraph-level heuristic is too imprecise for that, and a genuine claim-by-claim audit would require reading every paragraph against its nearest citation manually, which has not been done here. It also does not substitute for the systematic database search (Web of Science, Scopus) this review has never had access to (§2.1–§2.3) — the counts above describe the shape of *this* review's self-selected, search-engine-derived evidence base, not the shape of the WBE literature as a whole.
