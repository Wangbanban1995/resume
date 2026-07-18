# Evidence Freeze Audit — WBE Review, Chapters 1–10 (updated 2026-07-18)

**What is, and is not, frozen.** This file's name retains "freeze audit" from when it was first created (2026-07-13, before Chapter 9 existed), but its counts are recomputed every round a chapter adds references — this round covers Chapter 10's eight additional sources. What *is* frozen, permanently, as a documented fact about this review's methodology, is the **full-text-verification status**: this review has never read a single source in full text, at any point, in any chapter, and that fact does not change as chapters are added — only the denominator it is reported against grows. Do not read "0/51" or "0/59" anywhere in this project's history as a claim that has since become false; each was the correct count *as of that round*, superseded here by the correct count as of this round: **0 of 67 active references full-text read.**

This note counts, per chapter: primary WBE original studies, systematic reviews, general (non-WBE) methodological literature, institutional/policy sources, conceptual/ethics/policy-analysis sources (introduced by Chapter 9); full-text-read sources, abstract/metadata-only sources, metadata-verified vs. metadata-unresolved sources, preprints, and paragraphs without a specific citation. Counts are derived from `WBE_Review_References.md` and `WBE_Review_Citation_Verification_Table.md` and a structured scan of `WBE_Review_Ch1-10.md`.

---

## 0. Headline numbers (recomputed this round)

| Metric | Count |
|---|---|
| **Total reference numbers issued** ([1]–[67], plus [32b]) | **68** |
| **Withdrawn from active citation** (metadata unresolved below this review's citation bar — see §5) | 1 ([56]) |
| **Active / citable references** | **67** |
| Full text obtained | 0 / 67 |
| **Full text read** | **0 / 67** |
| Claim-level verified (the specific quantitative/comparative claim independently confirmed, not just the source's existence) | 0 / 67 |
| Abstract/snippet checked | 67 / 67 (100%) |
| Metadata verified (author, year, venue, and DOI/identifier cross-confirmed, or a high-confidence single institutional record) | 54 / 67 |
| Metadata incomplete/unresolved (cited anyway, per this review's "confirmed lead author(s), et al." convention) | 13 / 67 |
| Preprints (non-peer-reviewed) | 4 / 67 (excludes the withdrawn preprint, [56]; **zero** of Chapter 10's 8 additions are preprints, a deliberate improvement) |
| Institutional / organizational-authored or policy-secondary sources | 9 / 67 |

**This table's "N" is 67 — not 51, not 59, and not 68.** 51 was correct through Chapter 8; 59 was correct through Chapter 9; 68 is the total count of reference *numbers issued* including the one withdrawn; 67 is the count of references this review actually treats as active evidence as of Chapter 10. Any future round should use its own recomputed figure as the reporting denominator, never revert to a prior round's number.

## 1. Reference counts by chapter and evidence type

| Chapter | Primary WBE original study | Systematic review / secondary evidence | General (non-WBE) methodological literature | Institutional / policy / secondary source | Conceptual / ethics / policy-analysis | Total references (first cited in this chapter) |
|---|---|---|---|---|---|---|
| 1–2 (Introduction, Methodology) | 0 | 3 ([2],[12],[17]) | 0 | 7 ([1],[4],[5],[7],[11],[14],[15]) | 0 | 10 |
| 3–4 (Inverse problem, sewer transport) | 6 ([3],[8],[9],[10],[13],[16]) | 0 | 1 ([6] Guo) | 0 | 0 | 7 |
| 5 (Sampling/analytical) | 7 ([18]–[24]) | 1 ([25]) | 0 | 0 | 0 | 8 |
| 6 (Normalization) | 9 ([26]–[33], [32b]) | 1 ([34]) | 0 | 0 | 0 | 10 |
| 7 (Back-calculation/identifiability) | 7 ([35],[36],[38],[41]–[44]) | 1 ([40]) | 3 ([37],[39],[45]) | 0 | 0 | 11 |
| 8 (Uncertainty propagation) | 4 ([46],[48]–[50]) | 1 ([47]) | 0 | 0 | 0 | 5 |
| 9 (Public-health integration) | 4 ([52],[55],[57],[58]) | 1 ([51]) | 0 | 1 ([59]) | 2 ([53],[54]) | 9 issued, 8 active ([56] withdrawn) |
| 10 (Enabling technologies, new this round) | 3 ([60],[62],[66]) | 3 ([61],[63],[67]) | 1 ([65]) | 1 ([64]) | 0 | 8 |
| **Total (68 issued, 67 active)** | **40** | **11** | **5** | **9** | **2** | **67 active** |

**Cross-chapter reuse (not double-counted above, listed for transparency):** [9] Jung et al. (Ch3–4→Ch8 §8.3); [13] Rainey et al. and [28] Maal-Bared et al. (Ch3–4/Ch6→Ch7 Table 5); [24] Pecson et al. (Ch5→Ch8 §8.4); [44] Dai et al. and [45] Alhassan et al. (Ch7→Ch8 §8.9/§8.12); [8] Janssens et al. (Ch3–4→Ch9 Table 7); [11] NASEM and [14] WHO (Ch1–2→Ch9 §9.3/§9.5/§9.8, and [11]→Ch10 §10.10's institutional-coordination framing is a restatement, not a new citation instance); [44] Dai et al. and [46] Jones et al. (Ch7/Ch8→Ch9 Table 7). **No Chapter 1–9 reference is directly reused as a new citation instance in Chapter 10** — Chapter 10's evidence base is entirely new sources ([60]–[67]), consistent with its subject matter (technologies not previously discussed) rather than reinterpretation of already-cited findings.

## 2. Full-text-read vs. abstract/metadata-only vs. metadata-verified

**Full-text-read sources: 0 of 67 active references, across every chapter including Chapter 10.** WebFetch returned HTTP 403 for every publisher, PMC, DOI-resolver, and Crossref-API domain attempted throughout this entire project. No exception exists anywhere in the evidence base.

**Abstract/metadata-only sources: 67 of 67 active references (100%).**

**Metadata verified vs. unresolved:** 54 of 67 active references have author list, year, venue, and DOI/identifier cross-confirmed across independent search results (or, for institutional sources, a single high-confidence official record). The remaining 13 — [5], [7], [19], [20], [23], [32b], [46], [47], [49], [53], [54], [57], **[64] (new this round)** — carry some form of incomplete author attribution. [64]'s specific issue (a duplicated "Gushgari" surname with two different given-name initials) is a new sub-type of this general problem, distinct from the more common "truncated et al." pattern — flagged in `WBE_Review_Pending_Verification_List.md` accordingly.

**Chapter 10's specific contribution to this section**: 7 of its 8 references are fully metadata-verified on first search (a notably higher hit rate than Chapter 9's, where several sources required a second, dedicated re-search round) — and **one metadata error was caught and corrected before entering the main text**: an initial search summary attributed [60] to "Moore et al.," conflating the historically-named "Moore swab" sampling method with the paper's actual authorship; a dedicated re-search confirmed the correct first author as Schang. This is recorded as a positive instance of this review's verification discipline working as intended, not merely a limitation to disclose.

**2026-07-13 retest and access-failure log (retained, still current).** WebFetch was re-tested against representative targets from Chapters 8 and 9; both returned **HTTP 403 Forbidden**, the same failure mode documented at every full-text attempt across this entire project, including Chapter 10's sources (not independently re-tested this specific round, since the structural failure mode — a blocked outbound-fetch capability — has been confirmed repeatedly and does not vary by source). **Remediation requires one of:** (a) database/full-text access being granted to this session, or (b) the user supplying PDFs, exports, or pasted full text for specific papers. Until either occurs, 0/67 is the correct and honest count.

## 3. Paragraphs without a specific citation — methodology and approximate counts

**Methodology unchanged, re-run fresh against Chapter 10 specifically.** Chapter 10 shows the highest flag rate of any chapter to date (56%), for the same structural reason identified for Chapter 9 (§-cross-references not recognized as citations by this pattern-match) plus one additional Chapter-10-specific factor: **§10.10's technology-readiness framework and Table 8/Box are entirely original synthesis, explicitly labeled as such, and correctly carry no external citation** — a larger share of Chapter 10's text is this kind of original framework content than in any prior chapter, mechanically inflating the flag rate without indicating a real evidentiary gap.

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
| 9 | 44 | 16 | 36% |
| 10 (re-run fresh this round) | 27 | 15 | 56% |
| **Total** | **414** | **106** | **26%** |

**Manual spot-check of Chapter 10's 15 flagged items confirms the same over-flagging pattern**: e.g., §10.5's "process-informed AI is not permitted, anywhere in this review, to substitute for the mechanistic understanding Chapters 3–8 developed" is flagged only because it doesn't match the citation-pattern regex, not because it lacks support — it is this review's own stated instruction/argument, internally consistent with everything since Chapter 3. Table 8 and the Box are both explicitly self-labeled original content. **No item in Chapter 10's flagged list was found, on this spot-check, to assert an external empirical finding without a supporting citation.**

## 4. What this audit does and does not establish

This audit **does** establish: the review's evidence base leans heavily on primary WBE studies (40 of 67 active references, 60%); Chapter 10 is the first chapter to cite **zero preprints**, a deliberate evidentiary improvement over Chapter 9's necessarily preprint-inclusive alert-detection literature; Chapter 10's metadata-verification hit rate (7 of 8 on first search) is higher than Chapter 9's; and zero sources have been read in full text at any point in this project, across all 67 active references.

This audit does **not** establish freedom from unsupported claims (§3's heuristic is imprecise), nor does it substitute for the systematic database search this review has never had access to. Chapter 10 does not have its own dedicated paragraph-by-paragraph claim audit the way Chapter 9 does (`WBE_Review_Ch9_Claim_Audit.md`) — per this round's request, Chapter 10 instead has a lighter-weight `WBE_Review_Ch10_Evidence_Note.md` — consult that file for Chapter 10's evidence-base summary beyond this file's aggregate counts.

## 5. Withdrawn and flagged references, and why

- **[56]** (a proposed EWMA-based early-warning index, Chapter 9) remains **withdrawn from active citation**: even a possible co-author's name could not be independently corroborated beyond a single, non-independently-repeated search result. It remains numbered [56] to avoid disrupting downstream numbering, marked **"WITHDRAWN — do not cite until metadata resolved"** in `WBE_Review_References.md` and the Citation Verification Table, and excluded from every "67" or "active" count in this file.
- **[64]** (Keenum et al., Chapter 10) is **not withdrawn** but carries a distinct new flag: its retrieved author list contains "Gushgari" twice with different given-name initials, an internal inconsistency (not merely an incomplete list) not resolved this session. Unlike [56], a clearly-identified lead author (Keenum) exists with reasonable confidence, so this is treated as a "metadata incomplete/unresolved" case (§0, §2) rather than a withdrawal — consistent with how this review distinguished [56]'s weaker position from ordinary "et al." sources in the prior round.

## 6. Execution toolkit status (unchanged this round — the pilot toolkit was not modified)

A systematic-review execution toolkit exists at `systematic-review/` (README, standard directory structure, CSV templates, and tested Python scripts including pilot-mode support). This toolkit changes what this review is *able to do* once real data arrives; it changes **nothing** about the review's current evidentiary state, and was not touched this round:

- **The formal database search has still not been executed.** No Web of Science, Scopus, or PubMed query has been run against a real database from within this session.
- **Full-text verification remains 0/67** (updated denominator this round; was 0/51 through Chapter 8, 0/59 through Chapter 9). The toolkit's scripts have been exercised only against clearly-labeled synthetic test fixtures and genuine (still-negative) pilot-readiness checks against real, empty directories.
- **No real PRISMA number exists**, and none was generated this round.
- **Next-state trigger, unchanged:** this review's evidence base moves out of its current state only when real Web of Science, Scopus, and PubMed export files are supplied into `systematic-review/data/raw/{wos,scopus,pubmed}/`. Until that happens, every chapter's prose continues to carry the "pending full-text verification" hedge documented throughout, and this file's role is to keep the *denominator* honest as chapters are added — 67 today, whatever the true count is after Chapter 11, and so on — never to imply that adding chapters or references brings the review closer to formal verification by itself.
