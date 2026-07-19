# Table Format Standard — Table 2, Table 3, and Planned Supplementary Tables

**Round:** Water Research compression, post-Phase 3C non-evidence work. 2026-07-19. Defines one consistent formatting standard applied retroactively to Table 2 and Table 3 (in `WBE_Review_WR_Condensed_Draft.md`) and prospectively to the planned Supplementary Tables (`WBE_Review_Supplementary_Outline.md` §S8a "Table S5," and any future SI table), so that all in-text and SI tables in this manuscript look and read as one designed system rather than as separately drafted artifacts. **No table content, row, or cell value is changed by this document** — only formatting/labeling conventions.

## 1. Caption format

- **Pattern:** `Table N. <Descriptive title, sentence case except proper nouns> — synthesized by this review` for any table whose column judgments (not just row content) reflect this review's own classification rather than a verbatim reproduction of a single source's table.
- **Applied this round:** Table 2 and Table 3 both already carry this pattern (added Phase 3C). Confirmed consistent; no change needed.
- **For a future SI table** (e.g., Table S5, "Uncertainty Sources, Propagation Methods, Validation Requirements and Residual Limitations," per `WBE_Review_Supplementary_Outline.md` §S8a): use the same pattern once drafted, since it is likewise this review's own consolidation of Table 6's source-draft content, not a single external table reproduced verbatim.

## 2. Column header style

- **Title Case** for every column header (e.g., "Required assumption" should be "Required Assumption" for full consistency — see §5 below for the one exception found and left as-is pending a content-neutral formatting pass).
- No abbreviations in column headers unless the abbreviation is defined in running text before the table appears (per `WBE_Review_Abbreviation_Audit.csv`'s existing discipline) — checked: neither Table 2 nor Table 3 currently uses an undefined abbreviation in a header.
- Column order follows a consistent logic across both tables: identifying column first (Strategy / Model family), then what it targets or corrects, then the evidentiary/methodological requirement, then the uncertainty or risk consequence. Confirmed both Table 2 and Table 3 already follow this order; no reordering needed.

## 3. Evidence-tier footnote convention (new this round)

Every table whose cells state a performance comparison, mechanism direction, quantitative figure, or cross-scenario conclusion — rather than a purely definitional or structural point — must carry an explicit footnote immediately below the table, in italics, naming which `WBE_Review_Critical_Claim_Verification_Queue.csv` row(s) govern that table's outstanding evidence gap, and stating that the flagged content is pending full-text verification.

- **Applied this round:** the footnote text itself, inside the manuscript, names only the affected column(s) and states the pending-verification status in plain language — it does **not** cite an internal filename or claim-ID, consistent with this project's standing discipline (Phase 2B, Task #92) of keeping project-management/internal-tracking language out of the manuscript body. The mapping from each footnote to its governing internal tracking row is recorded here, in this project-internal design document, not inline in the manuscript:
  - Table 2's footnote (affecting the "Residual/introduced uncertainty" column) is governed by `WBE_Review_Critical_Claim_Verification_Queue.csv` row **P4-10**.
  - Table 3's footnote (affecting the "Dominant uncertainty," "Minimum validation," and "Principal failure mode" columns) is governed by queue row **P5-10**.
- **Convention for future SI tables:** the same footnote pattern (plain-language pending-verification statement in the manuscript; internal row mapping tracked separately in project documents, never inline) applies to Table S5 once drafted (governed by the same P5-10 row, since Table S5 is Table 3's full-detail source material per the Compression Log's Table 6 disposition) and to any other SI table carrying a comparative or performance judgment.
- **What does not need this footnote:** purely structural/definitional columns (e.g., Table 2's "Strategy" and "Corrects" columns, which name a method and what it targets, not a performance judgment) and Table 3's "Model family" and "Inferential target" columns (naming, not judging). This distinction was checked cell-by-cell for both tables during this pass — see `WBE_Review_Table_Design_Brief.md` for the original per-cell audit this builds on.

## 4. Hedge-language conventions

- Consistent verb choices across both tables' prose-adjacent captions/footnotes: "pending full-text evidence verification" (not "unverified," "unconfirmed," or "provisional," which were used inconsistently across earlier project rounds) is now the standard phrase for this specific status, matching the phrase already used throughout `WBE_Review_Critical_Claim_Verification_Queue.csv` and `WBE_Review_Evidence_Recovery_Plan.md`.
- "Synthesized by this review" (not "proposed by this review," "this review's framework," or other variants) is the standard caption suffix for a table whose column structure is original — checked: both Table 2 and Table 3 already use this exact phrase consistently.

## 5. One formatting inconsistency found and left unfixed this round

Table 2's header row reads "Strategy | Corrects | Required assumption | Residual/introduced uncertainty" (sentence-case headers) while this standard's §2 recommends Title Case. **Not changed this round** because a header-casing change would need to be applied identically to Table 3 and any future SI table in the same commit to avoid creating a new inconsistency, and the net reader-facing value of this specific casing change is low compared to the risk of an unreviewed formatting-only edit touching table structure right before this round's evidence-tagging edits. Flagged here as a deferred, purely cosmetic item for the next presentation pass, not forgotten.

## 6. Planned Supplementary Tables — format template (structure only)

For **Table S5** (§S8a, Uncertainty Sources, Propagation Methods, Validation Requirements and Residual Limitations) and any other future SI table, the column template should be:

| Column | Purpose | Evidence-tier footnote required? |
|---|---|---|
| Uncertainty source | Names the source (identifying, not judging) | No |
| Type | Classifies the uncertainty type (structural point) | No |
| Typical distribution / representation | States how the source is typically modeled | Yes, if stated as a general finding rather than a definitional convention |
| Propagation method | Names the applicable method(s) | No (naming only) |
| Mitigation | States what reduces this uncertainty source | Yes, if framed as an effectiveness claim |
| Residual effect | States what remains after mitigation | Yes — this is the column most likely to carry an unverified performance judgment |

This template is provided so that whoever drafts Table S5 in a future round starts from a format-consistent design rather than inventing a new column convention, but **no data has been entered into this template** — it is structure only, consistent with this round's constraint against filling in unverified content.

## Summary

Format unified across Table 2, Table 3, and the planned SI table template: consistent caption pattern, consistent column-header case (with one deferred exception, §5), a new evidence-tier footnote convention now applied to both existing tables, and consistent hedge-language phrasing. No table's row content, cell values, or evidentiary claims were changed — only presentation and the addition of explicit "pending full-text evidence verification" footnotes, which is itself the primary substantive output of this document.
