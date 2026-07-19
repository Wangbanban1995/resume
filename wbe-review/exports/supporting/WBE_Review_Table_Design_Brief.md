# Table Design Brief — In-Text Table Audit and Planned-Table Status

**Round:** Water Research compression, Phase 3C (manuscript presentation and internal-consistency refinement). 2026-07-19. Audits the two tables currently drafted in `WBE_Review_WR_Condensed_Draft.md` (Table 2, Table 3) against redundancy, width, unverifiable comparatives, SI-migration candidacy, and "proposed by this review" labeling, and records the status of the two additional tables named in the Target Outline's 4-table plan (Table 1, Table 4) that have not yet been drafted.

## Table 2. Normalization strategy, corrected mechanism, required assumption and residual uncertainty

- **Repeats main text?** Partially, by design — table content summarizes §4.2-§4.4's argument in scannable form (this is standard practice: a synthesis table restating prose in structured form is not redundancy in the negative sense, since the two serve different reading modes). No sentence in §4.2-§4.4 is copied verbatim into the table; the table's "Required assumption" and "Residual/introduced uncertainty" columns state the same underlying facts in a different, denser form than the prose.
- **Too wide?** No — 4 columns, 4 rows; well within typical journal single-column or double-column table width.
- **Unverifiable comparatives?** Checked directly — no cell uses "best," "most reliable," "universally applicable," "robust across settings," or similar unqualified superlative/ranking language. Every cell states a conditional mechanism ("corrects X," "requires Y," "residual Z"), not a cross-strategy ranking. This is correct and should be preserved in any future edit.
- **Should move to SI?** No — this is exactly the kind of compact, decision-relevant synthesis a main-text table should carry; the full per-study, per-biomarker detail behind it already lives in SI §S5/§S6, so no further migration is needed.
- **Table title labeled "proposed by this review"?** Was not labeled as of the start of this round; **fixed this round** — caption now reads "...synthesized by this review," since the four-row categorization and the specific "required assumption"/"residual uncertainty" framing are this review's own organizing synthesis (per §1.3's own framing), not a pre-existing standard table reproduced from any single cited source.

## Table 3. Model family, identifiability requirement, dominant uncertainty and minimum validation

- **Repeats main text?** Partially, by design — same rationale as Table 2; §5.1-§5.4's prose develops the concepts, the table applies them systematically across the six named model families, which prose alone does not do as scannably.
- **Too wide?** Borderline — 6 columns × 6 rows is the widest table in the manuscript. This is an intentional design outcome (Phase 2A explicitly redesigned it to exactly 6 columns after merging the source draft's Tables 4, 5, and part of 6), not an oversight, but it is worth flagging for final typesetting: some cells (e.g., "Correction-factor components separably justified, not fixed by assumption") are long enough that column width may need adjustment or cell text may need further tightening at final formatting, depending on Water Research's table-width constraints. This is a formatting risk to watch, not a content problem to fix this round.
- **Unverifiable comparatives?** Checked directly — no cell uses unqualified ranking language; every "Principal failure mode" cell states a conditional risk ("confident wrong estimate under X"), not a comparative claim between model families.
- **Should move to SI?** No — this is the manuscript's single densest synthesis of the reconstruction-identifiability-validation argument and belongs in the main text; the full per-study evidence behind each row lives in SI §S7/§S8/§S8a.
- **Table title labeled "proposed by this review"?** Was not labeled as of the start of this round; **fixed this round** — caption now reads "...synthesized by this review." This table is a clear case for the label: columns like "Principal identifiability requirement," "Minimum validation," and "Principal failure mode" represent this review's own judgment applied across six model families, not a pre-existing published matrix being reproduced.

## Table 1 and Table 4 — planned, not yet drafted

The Target Outline's 4-table plan (`WBE_Review_Target_Outline.md`, "Figure and table inventory and disposition plan") names two additional in-text tables that were never actually drafted during Phase 2A/2B and remain **planned only**:

- **Table 1 (planned title: "Process-distortion-observable-correction")** — would consolidate the amplitude/temporal/spatial distortion mechanisms from §1.1-§3 with which correction each admits. Not drafted. Adding it now would be new main-text content, which is outside this round's scope (Phase 3C forbids expanding the main text or adding new content); flagged here so a future content-drafting round has an accurate status rather than assuming it already exists.
- **Table 4 (planned title: "Minimum reporting and decision-readiness framework")** — would consolidate §6.3's actionability conditions, §7.3's readiness hierarchy, and the five scattered source-draft reporting-requirement checklists (already slated for SI §S10 in full) into one framework table. Not drafted, same reasoning as Table 1.

**This is not a defect introduced this round** — both were always "planned" rather than "drafted" per the Target Outline's own status language, and Phase 2A/2B's word-budget accounting never assumed their word cost. This brief simply makes their current undrafted status explicit and auditable, rather than leaving it implicit in a planning document a reader might not cross-check against the actual manuscript.

## Summary of changes made in Phase 3C

Two caption edits applied to `WBE_Review_WR_Condensed_Draft.md` (Table 2 and Table 3 captions, appending "— synthesized by this review"). No table content, row, column, or cell value was changed. No new table was drafted. No unverifiable comparative language was found or needed removal — both existing tables were already correctly hedged.

## Addendum — post-Phase 3C non-evidence work (2026-07-19)

Two further, purely presentational additions this round, per `WBE_Review_Table_Format_Standard.md` (new this round, defining the full formatting standard both tables now follow):

- **Table 2**: an italic footnote was added immediately below the table, naming the "Residual/introduced uncertainty" column specifically and stating that its performance/cross-scenario content (e.g., "unreliable under high inflow/infiltration," "fails outright when fate is mismatched") is pending full-text evidence verification. **Note on a fix made during drafting:** the footnote's first draft also cited `WBE_Review_Critical_Claim_Verification_Queue.csv` row P4-10 by name inline in the manuscript; this was caught and removed before finalizing, since a filename/internal-tracking-ID citation inside the submission manuscript body violates this project's standing Phase 2B discipline against project-management language in the manuscript text. The row mapping (Table 2 ↔ queue row P4-10) is preserved here and in `WBE_Review_Table_Format_Standard.md` instead.
- **Table 3**: an italic footnote was added below the table, naming the "Dominant uncertainty," "Minimum validation," and "Principal failure mode" columns, with the same plain-language pending-verification statement and the same internal-citation removal (Table 3 ↔ queue row P5-10, tracked in `WBE_Review_Table_Format_Standard.md`, not inline).

These footnotes make explicit, at the point a reader encounters the table, exactly what this brief's "unverifiable comparatives" check already established in Phase 3C (no cell uses an unqualified superlative) — that even the *qualified*, conditional statements in these columns are not yet full-text-confirmed. No cell content changed; this is a labeling addition only. See `WBE_Review_Table_Format_Standard.md` for the full formatting rationale, including one deferred cosmetic item (header-casing consistency) intentionally not touched this round.
