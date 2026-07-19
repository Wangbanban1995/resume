# Word-Count Method — WBE Review, Chapters 1–10

**Round:** Water Research compression, Phase 1 (structure and length audit only — no rewriting). 2026-07-18.

## What this file is

This documents exactly how `WBE_Review_Section_Word_Count.csv` was produced, so the numbers in it are reproducible and auditable rather than asserted. The counting script is `scripts/word_count.py`, run against `WBE_Review_Ch1-10.md` at commit `96e7bb2`. Re-running `python3 scripts/word_count.py` from `wbe-review/` regenerates the CSV deterministically — it depends on nothing but the current text of the main document.

## Method

The script walks the document line by line and classifies every line into exactly one of: a chapter heading (`##`), a section heading (`###`), a table row (`|...|`, with dash-only separator rows excluded), a blockquote line (used exclusively for Box content in this document), or ordinary body text (prose paragraphs, including list items and bold-labeled items). Horizontal rules (`---`) and blank lines are counted as structural, not word-bearing.

For each category, word counts are computed after stripping, in order: bracket-style citation markers (`[12]`, `[7,8]`, `[32b]`, `[1–3]`) via regex; inline math spans (`$...$`); any literal HTML tags; and Markdown control characters (`*`, `_`, `` ` ``, `#`, `>`, `|`). What remains is split on whitespace and counted as words — the same basic approach a plain-text word counter uses, applied after removing Markdown/LaTeX syntax that would otherwise inflate the count with formatting tokens rather than prose.

**Two explicit choices affect the numbers, and are stated here rather than left implicit:**

1. **Bracket-style citations `[N]` are stripped from the body-word count** (per the task instruction to exclude "引用编号本身" — the citation number token itself), but **prose-style citations ("Schang et al. (2025)", "(WHO, 2025a)") are *not* stripped from body words**, because these are ordinary sentence words a reader parses as part of the sentence, not bare reference numbers. This document uses prose-style citation almost exclusively (155 of 155 total citation instances counted separately below are either `[N]` or prose form; only 29 are the bracket style, concentrated in Chapter 9's Table 7 and Chapter 10's Table 8, which cross-reference the numbered reference list directly). **Consequence: body-word counts are not artificially deflated by the document's actual citation style, but this also means body-word counts include author-name and year tokens as ordinary words** — a second, citation-only pass (below) reports the true citation density separately so this doesn't understate how citation-heavy any given section is.
2. **Citation marker count is the sum of both forms**: bracket matches (`\[\d+[a-z]?(?:[,\-–]\d+[a-z]?)*\]`) plus prose matches (`Author et al. (YYYY)`, `Author & Author YYYY`, `(Author, YYYY)`). Total: **155** across the document (29 bracket-style, 126 prose-style) — this is the number to cite for "citation density," not the 29-only bracket count, which would understate density roughly 5-fold given this document's dominant citation style.

**Paragraph count**: a new paragraph is counted at the start of each contiguous run of non-blank, non-heading, non-table-row, non-horizontal-rule lines; blockquote runs (Box content) are counted as their own paragraph, separately from the surrounding body text. Total: **312** paragraphs across the document.

**Equation count**: a proxy count of inline math spans (`$...$`) per line, not a count of distinct named equations — several spans can belong to one displayed equation broken across a table row or list item, and a few equations recur (e.g., the observation-model definitions restated with variation across §5.0, §6.0, §7.0). Total: **347** math spans. This should be read as "density of mathematical notation," not "number of unique equations" — a manual count of distinct, semantically new equations (not restatements) would be materially lower and is not attempted here.

**Section attribution**: content between a chapter's `##` heading and its first `###` heading (bridge/status-note paragraphs, e.g. Chapter 9's and Chapter 10's opening status notes) is attributed to a synthetic `(chapter preamble)` section row, not silently dropped or merged into the first numbered subsection.

**Internal-note flag** (`is_internal_note` column): six end-matter sections — "Note on companion files," "Editorial self-check," and the five "Structural bridge from Chapter X to Chapter Y" sections — plus the document's title/status-note front matter, are flagged `True`. These are project-management and self-audit prose, not review content, and are excluded from "chapter body" totals reported below. No content inside Chapters 1–10 proper (§1–§10.10, all tables, boxes, and figures notes) is flagged as internal note, including the evidentiary status notes that open each chapter — those are treated as review content because Water Research (or any journal) reviewers would need an equivalent, if shorter, evidence-transparency statement in a submitted version; they are not pure project-management scaffolding the way the companion-file list or the structural-bridge sections are.

## Headline totals (re-run, not asserted from memory)

| Quantity | Words |
|---|---:|
| **Grand total (Chapters 1–10 + all end-matter/front-matter)** | **44,717** |
| — of which internal-note/meta content (front matter, companion-file list, editorial self-check, six structural-bridge sections) | 3,060 |
| — of which Chapters 1–10 proper (all content types: prose, headings, tables, box captions) | **41,657** |
| Body prose words only (all sections, chapters + meta) | 39,253 |
| Heading words only | 831 |
| Table cell words only | 3,303 |
| Box/blockquote words only | 1,330 |

**This is not "approximately 39,400 words."** The prior round's informal estimate is superseded by this recomputation: body prose alone is 39,253 words, but the manuscript-relevant total (Chapters 1–10, all content types, excluding only the six internal project-management sections) is **41,657 words**, and the absolute grand total including all internal notes is **44,717 words**. Any future reference to "the current draft's length" should cite 41,657 (chapter body) as the operative figure for a compression baseline — internal notes are not part of what would ever be submitted and should not inflate the number the compression target is measured against.

| Other counts | Total |
|---|---:|
| Citation instances (bracket `[N]` + prose `Author et al. (YYYY)` combined) | 155 |
| — bracket-style only | 29 |
| — prose-style only | 126 |
| Paragraphs | 312 |
| Inline math spans (equation-density proxy, not unique-equation count) | 347 |

## Per-chapter totals (all content types, section_total_words summed)

| Chapter | Words | % of grand total (44,717) |
|---|---:|---:|
| Front matter (title + status note) | 317 | 0.71% |
| 1. Introduction | 1,106 | 2.47% |
| 2. Review Methodology and Evidence Synthesis | 1,261 | 2.82% |
| 3. WBE as an Inverse Problem | 1,280 | 2.86% |
| 4. Signal Distortion in Sewer Transport | 1,414 | 3.16% |
| 5. Sampling, Analytical Methods, and QA | 4,351 | 9.73% |
| 6. Normalization | 7,461 | 16.68% |
| 7. Population-Level Reconstruction | 7,241 | 16.19% |
| 8. Uncertainty Propagation | 6,891 | 15.41% |
| 9. Public-Health Surveillance and Decision-Making | 5,859 | 13.10% |
| 10. Enabling Technologies and Research Infrastructures | 4,793 | 10.72% |
| Note on companion files | 600 | 1.34% |
| Editorial self-check | 682 | 1.53% |
| Structural bridge, Ch1–4→5 | 186 | 0.42% |
| Structural bridge, Ch5→6 | 174 | 0.39% |
| Structural bridge, Ch6→7 | 130 | 0.29% |
| Structural bridge, Ch7→8 | 381 | 0.85% |
| Structural bridge, Ch8→9 | 312 | 0.70% |
| Structural bridge, Ch9→10 | 278 | 0.62% |

**Chapters 6, 7, and 8 alone account for 21,593 words — 51.8% of the 41,657-word chapter body.** This is the single most load-bearing fact for Phase 1's compression planning: normalization, reconstruction, and uncertainty propagation are simultaneously this review's three strongest original-contribution chapters and its three longest, and the overlap/priority audits (separate files) are where the actual compression opportunity within them — as opposed to across them — gets identified.

Full per-section detail (105 rows, one per `###` subsection or chapter-level preamble) is in `WBE_Review_Section_Word_Count.csv`.

## Known limitations of this method

- Word counts are whitespace-token counts after Markdown/LaTeX stripping, not a typesetter's or MS Word's line-count-based "word count" — the two typically agree within a few percent for prose-heavy text but are not identical algorithms.
- Table word counts include header-row label text (e.g., "Process", "Distortion type") as words, which a print layout would count differently (a table's visual length depends on column width and wrapping, not raw word count) — table word counts here are a content-density proxy, not a page-length predictor.
- The equation-span proxy count (347) does not distinguish a genuinely new equation from a restatement of an existing one — this matters for Phase 2 planning (an equation repeated three times across chapters is a compression opportunity the word count alone does not surface; the Overlap Audit addresses this qualitatively where it occurs).
- This method file and script were written for this document's specific structure (chapters at `##`, sections at `###`, no `####` level used) — it would need adaptation for a differently-structured document.
