# Post-Evidence-Recovery Checklist — Formal Search, PDF Acquisition, and Full-Text Verification

**Round:** Water Research compression, post-Phase 3C non-evidence work. 2026-07-19. Consolidates `WBE_Review_Full_Text_Request_List.csv` (31 rows) and `WBE_Review_Targeted_Search_Addendum.md` (11 search modules) into one ordered, actionable checklist, so that whoever next has real database or full-text access can execute directly from this document without cross-referencing three separate files first. **This document adds no new evidence, resolves no claim, and changes no count** — it is a work plan only.

**Evidence status, unchanged:**

```text
Full-text obtained: 0/67
Full-text read: 0/67
Critical claims resolved: 0/9
Submission ready: No
```

---

## Step 1 — Acquire the 14 open-access PDFs first (no institutional access required)

These are already identified in `WBE_Review_Full_Text_Request_List.csv` as openly accessible; no paywall, login, or institutional subscription should be needed. Ordered by priority (P0 = Critical-claim-supporting, P1 = High):

| Order | Ref. | Author, Year | Journal/platform | Governs claim(s) |
|---|---|---|---|---|
| 1 | [16] | Zhang, S. et al. 2023 | *Water* (MDPI) | P3-3 |
| 2 | [9] | Jung, J. et al. 2026 | *Scientific Reports* | P3-3 |
| 3 | [8] | Janssens, R. et al. 2022 | *Viruses* (MDPI) | P3-7 |
| 4 | [13] | Rainey, A. L. et al. 2023 | *PLOS ONE* | P3-9, P4-5, P4-10 |
| 5 | [35] | Huisman, J. S. et al. 2022 | *Environmental Health Perspectives* | P5-10 |
| 6 | [38] | Ai, Y. et al. 2022 | *PLOS ONE* | P5-10 |
| 7 | [41] | Zuccato, E. et al. 2008 | *Environmental Health Perspectives* | P5-10 (citation restoration) |
| 8 | [29] | Dhiyebi, H. A. et al. 2023 | *Frontiers in Public Health* | P4-6, P4-10 (citation restoration) |
| 9 | [6] | Guo, Y. et al. 2023 | *Water* (MDPI) | Background |
| 10 | [11] | NASEM 2023 | National Academies Press | Background |
| 11 | [52] | Yu, Q. et al. 2024 | *PLOS Global Public Health* | P6-4 |
| 12 | [55] | Assoum, M. et al. 2023 | *Tropical Medicine and Infectious Disease* (MDPI) | P6-2 |
| 13 | [58] | Zhang, X. et al. 2025 | *Journal of Medical Internet Research* | P6-2 |
| 14 | [61] | Bam, P. G. et al. 2025 | *Water* (MDPI) | Background |

**Action:** download each via its DOI/URL in `WBE_Review_References.md`; save into this session's `data/fulltext/` (not tracked by git — see `.gitignore`); verify each against `WBE_Review_Full_Text_Request_List.csv`'s identity-confirmation fields (title/author/year/journal/DOI on the PDF's own first page) before treating it as "obtained."

## Step 2 — Attempt the remaining citation-restoration references (likely require institutional access)

| Order | Ref. | Author, Year | Journal | Access note |
|---|---|---|---|---|
| 15 | [3] | Darling, A. et al. 2025 | *Environmental Science & Technology* (ACS) | Subscription likely required |
| 16 | [44] | Dai, X. et al. 2024 | *Statistics in Medicine* (Wiley) | Subscription likely required |
| 17 | [30] | Chen, C. et al. 2014 | *Science of the Total Environment* (ScienceDirect) | Subscription likely required |
| 18 | [28] | Maal-Bared, R. et al. 2023 | *Science of the Total Environment* (ScienceDirect) | Subscription likely required |
| 19 | [43] | Schoen, M. E. et al. 2022 | *ACS ES&T Water* | Subscription likely required |
| 20 | [42] | McMahan, C. S. et al. 2021 | *The Lancet Planetary Health* | Subscription likely required |
| 21 | [24] | Pecson, B. M. et al. 2021 | *Environmental Science: Water Research & Technology* (RSC) | Subscription likely required |
| 22 | [2] | Boogaerts, T. et al. 2024 | *Science of the Total Environment* (ScienceDirect) | Subscription likely required |
| 23 | [46] | Jones, H. E. et al. 2014 | *Science of the Total Environment* (ScienceDirect) | Subscription likely required |
| 24 | [51] | Moallef, S. et al. 2025 | *SSM - Population Health* (ScienceDirect) | Subscription likely required |
| 25 | [60] | Schang, C. et al. 2021 | *Environmental Science & Technology* (ACS) | Subscription likely required |
| 26 | [63] | Pagsuyoin, S. et al. 2025 | *Risk Analysis* (Wiley) | Subscription likely required |
| 27 | [64] | Keenum, I. et al. 2024 | *American Journal of Public Health* | Subscription likely required |

**Action:** attempt via institutional access, interlibrary loan, or author-accepted-manuscript repositories (per Phase 3D's lawful-access-order instructions: publisher page → PMC → Europe PMC → OA-flagged PDF → institutional repository → author-accepted manuscript → government/public database → author's institutional repository). Record `PAYWALLED — FULL TEXT NOT OBTAINED` for any that fail after a genuine attempt — never substitute an abstract or search-summary preview.

## Step 3 — [57] formal-version / independent-second-source search (Module 9)

Per `WBE_Review_Targeted_Search_Addendum.md` module 9: search `("event detection" OR "outbreak detection" OR "alert threshold") AND (wastewater) AND (sensitivity OR "predictive value")` across Web of Science, Scopus, PubMed, and directly check medRxiv for a published version of Link, Garrido, et al.'s 2026 preprint (same DOI/author pair). Resolve per the standing rule (§7 of the original Phase 3B instructions, still in force): do not restore the "281-county" figure unless a formal version or an independent second source is found.

## Step 4 — Run the remaining 10 search modules (Targeted Search Addendum)

Modules 1, 2, 3, 4 (partial — the P4-5 industrial-discharge sub-item only), 5, 6, 7, 8, 10, 11 remain to be executed against Web of Science, Scopus, and PubMed using the candidate search strings already specified in `WBE_Review_Targeted_Search_Addendum.md`. These are lower-urgency than Steps 1-3 (which target sources already identified for existing claims) but necessary for the 3 genuinely-new-search claims (P3-6, the P4-5 industrial-discharge sub-item, and [57]'s Option A/B resolution, already covered in Step 3).

## Step 5 — Full-text verification (once PDFs are in hand)

For every PDF reaching `identity_match_status = Confirmed`:

1. Read Methods, Results, relevant tables/figures, Discussion, Limitations, and Supplementary Information (not abstract-only, not keyword-search-only).
2. Record study setting, sample/site count, sampling design, and validation design.
3. Complete one row per claim in `WBE_Review_Full_Text_Verification_Records.csv` (fields and `support_outcome`/`required_manuscript_action` value sets are fixed by the standing Phase 3B/3D specification — reuse it verbatim, do not redefine).
4. Apply the manuscript-revision rule matching the outcome (Retain / Narrow / Qualify / Replace citation / Add second citation / Move to SI / Convert to author synthesis / Remove / Obtain additional evidence).
5. Update, in this order: `WBE_Review_Critical_Claim_Verification_Queue.csv` → `WBE_Review_Full_Text_Request_List.csv` (`obtained`/`read` fields) → `WBE_Review_Reference_Use_Map.csv` → `WBE_Review_Condensed_Claim_Map.csv` → `WBE_Review_Condensed_Citation_Audit.csv` → `WBE_Review_Evidence_Recovery_Plan.md` → the condensed draft itself (only for the specific sentence/table cell the resolved claim affects) → `WBE_Review_Ch8_Evidence_Freeze_Audit.md` (recompute the denominator).
6. Recompute and report: `Full texts obtained: X/67`, `Full texts read: Y/67`, `Condensed-draft cited references read: Z/21`, `Critical claims resolved: A/9`, `Critical claims remaining: B/9`.

## What this checklist does not do

It does not run any search, download any PDF, or read any full text — it is a plan, executable the moment real database or full-text access exists in a session. It does not change any evidentiary count, and it does not itself require full-text access to exist (compiling this checklist from the already-built `WBE_Review_Full_Text_Request_List.csv` and `WBE_Review_Targeted_Search_Addendum.md` required no new evidence).
