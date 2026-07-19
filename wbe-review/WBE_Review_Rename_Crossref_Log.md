# File Rename and Cross-Reference Verification Log

**Round:** Chapter 9 consistency-and-evidence-status audit, followed by Chapter 10 drafting (2026-07-18).

## What was renamed

| Step | Old filename | New filename |
|---|---|---|
| 1 (prior round, for reference) | `WBE_Review_Ch1-8.md` / `.docx` | `WBE_Review_Ch1-9.md` / `.docx` |
| 2 (this round) | `WBE_Review_Ch1-9.md` / `.docx` | `WBE_Review_Ch1-10.md` / `.docx` |

Both renames were performed via `git mv`, preserving file history. **The old filenames no longer exist anywhere in the repository** — verified by a repository-wide search (see below) — eliminating the version-ambiguity risk named in this round's instruction.

## Files checked and updated for cross-references to the renamed file

| File | Reference found | Action |
|---|---|---|
| `WBE_Review_Ch1-10.md` (self) | No internal self-references to old filenames found | None needed |
| `README.md` | `WBE_Review_Ch1-9.md` in "what exists" list | Updated to `WBE_Review_Ch1-10.md`; historical mention of both prior names retained intentionally in prose, labeled as history |
| `WBE_Review_References.md` | `WBE_Review_Ch1-9.md` in opening description | Updated to `WBE_Review_Ch1-10.md` |
| `WBE_Review_Ch7_Model_Audit_Table.md` | `WBE_Review_Ch1-9.md` in extraction note | Updated to `WBE_Review_Ch1-10.md` |
| `WBE_Review_Ch8_Parameter_Distribution_Table.md` | `WBE_Review_Ch1-9.md` in extraction note | Updated to `WBE_Review_Ch1-10.md` |
| `WBE_Review_Citation_Verification_Table.md` | Title only said "Chapters 1–9" | Updated to "Chapters 1–10" (via chapter-count sweep, not filename sweep, since this file does not name the main file directly) |
| `WBE_Review_Pending_Verification_List.md` | Title only said "Chapters 1–9" | Updated to "Chapters 1–10" |
| `WBE_Review_Ch8_Evidence_Freeze_Audit.md` | Title and body referenced "Chapters 1–9" and `WBE_Review_Ch1-9.md` | Fully rewritten this round (see below) |
| `WBE_Review_Ch9_Claim_Audit.md` | Referenced a now-stale "0/59" headline figure | Updated to reference the Evidence Freeze Audit's recomputed-each-round figure rather than a hardcoded number |
| `WBE_Review_Systematic_Search_Strategy.md` | Stale "Chapters 1–8 remain frozen, Chapter 9 does not start" and "0/51" instruction, predating this project's resumption of chapter drafting | Updated to note the superseded instruction and point to the Evidence Freeze Audit for the current figure, rather than hardcoding a new one that would itself go stale |
| `systematic-review/README.md` | Contains a "0/51" reference | **Deliberately not modified** — this file is part of the pilot-mode execution toolkit, explicitly out of scope this round per instruction ("不修改pilot工具包和真实数据状态") |
| `systematic-review/templates/seed_studies.csv` and its references in `WBE_Review_Systematic_Search_Strategy.md` (the "44 of 51 references" seed-recall test set) | Contains "51" | **Deliberately not modified** — this is a fixed, historically-anchored methodological test set (which references the search strategy should recall), not a live "current reference count" claim, and is part of the toolkit ecosystem this round leaves untouched |

## Repository-wide verification (commands actually run)

```
grep -rn "WBE_Review_Ch1-8\.\|WBE_Review_Ch1-9\." wbe-review/ --include="*.md"
```
Result after this round's fixes: only two matches remain, both intentional historical-record prose (README.md's "renamed this round from..." sentence, and the main document's own "Note on companion files" entry #1 describing its own rename history) — neither is a live, unresolved reference to a nonexistent file.

```
ls wbe-review/WBE_Review_Ch1-8.* wbe-review/WBE_Review_Ch1-9.*
```
Result: no such files (confirms the old files were fully removed by `git mv`, not merely superseded by a duplicate).

## Chapter-count consistency check across the four core tracking files

| File | Title says | Reference count stated |
|---|---|---|
| `WBE_Review_Ch1-10.md` | Chapters 1–10 | N/A (main text) |
| `WBE_Review_References.md` | Chapters 1–10 | 68 issued, 67 active |
| `WBE_Review_Citation_Verification_Table.md` | Chapters 1–10 | 68 issued, 67 active (matches) |
| `WBE_Review_Pending_Verification_List.md` | Chapters 1–10 | N/A (organized by chapter, not a running total) |
| `WBE_Review_Ch8_Evidence_Freeze_Audit.md` | Chapters 1–10 | 68 issued, 67 active, 0 full-text read (matches) |

**All four counts agree: 68 reference numbers issued, 67 active/citable, 1 withdrawn ([56]), 0 full-text read.** This is the authoritative, cross-verified state as of this round.
