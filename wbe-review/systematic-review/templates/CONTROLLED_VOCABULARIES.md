# Controlled Vocabularies for Screening and Audit Templates

These are the fixed value sets to use when filling in the templates in this directory. Do not invent new values without updating this file first, so every reviewer uses the same terms.

## `manual_duplicate_review.csv` — `final_decision`

Populated by a human reviewer for every `possible_duplicate` group flagged by `deduplicate_records.py` (rules 4–7: title+year alone, title+author alone, title alone, or fuzzy title match) or by `check_seed_recall.py` (title-only or multi-candidate seed matches). Options:

- `same_record_merge` — the two records are genuinely the same publication; they should be merged (record which `preferred_record_id` to keep as the canonical entry)
- `related_version_keep_both` — related but legitimately distinct records (e.g., a preprint and its published version, both worth citing for different reasons) — keep both, but note the relationship in `decision_reason`
- `superseded_version` — one record supersedes the other (e.g., a correction supersedes the original, or a published version supersedes its preprint) — `preferred_record_id` names the one to keep as primary; the other is retained in the record set but flagged, not deleted
- `distinct_records` — coincidentally similar title/metadata but genuinely different studies — keep both, no relationship implied
- `uncertain` — cannot be resolved from title/abstract alone; requires full-text comparison before a decision can be made

**No script in this toolkit automatically applies any decision recorded in this file.** `deduplicate_records.py` and `check_seed_recall.py` only ever flag candidates into this template — reading a `final_decision` back out and acting on it (e.g., actually merging two master records, or removing a superseded one from the citation set) is a separate, explicit, auditable step that does not yet exist in this toolkit and must be added deliberately (with its own before/after diff and log) if and when it is needed, not silently folded into the deduplication script's normal run.

## `title_abstract_screening.csv` and `full_text_screening.csv`

`reviewer_1_decision`, `reviewer_2_decision`, `final_decision` (title/abstract stage only — full-text stage uses the same three-way decision for `reviewer_1_decision`/`reviewer_2_decision`/`final_decision` as well):
- `include`
- `exclude`
- `uncertain`

## `title_abstract_screening.csv` — `exclusion_reason`

- `not_WBE` — not about wastewater-based epidemiology/surveillance at all
- `treatment_removal_only` — about wastewater treatment/pathogen removal efficiency, not signal interpretation or population inference
- `environmental_water_only` — surface water, groundwater, or drinking water, not sewage/wastewater
- `analytical_method_only` — a pure analytical-chemistry or assay-development paper with no WBE application context
- `no_population_inference` — describes wastewater detection without any population-, exposure-, or epidemiological-inference component
- `unrelated_sewer_process` — sewer-infrastructure engineering unrelated to biomarker/pathogen signal fate
- `conference_abstract_only` — abstract-only record with no accessible full paper
- `duplicate_publication` — a later-discovered duplicate that the automated deduplication step did not catch
- `other` — record why in `notes`

## `full_text_screening.csv` — `primary_exclusion_reason` and `secondary_exclusion_reason`

- `wrong_population_scope` — not a human-community wastewater-epidemiology context (e.g., purely animal/agricultural)
- `wrong_matrix` — sample matrix outside this review's scope (e.g., air, soil, food) despite a wastewater-adjacent title
- `no_WBE_inference` — full text reveals no actual population/exposure/epidemiological inference step
- `treatment_removal_only` — full text is about treatment-process removal efficiency, not signal interpretation
- `no_relevant_process_or_model` — no sewer-transport, sampling/analytical, normalization, back-calculation, or uncertainty content relevant to Chapters 3–8
- `insufficient_methods_or_results` — methods/results too sparse to extract any data-extraction field
- `duplicate_or_superseded` — a preprint superseded by a later peer-reviewed version already included, or another duplicate found only at full-text stage
- `full_text_unavailable` — could not obtain full text despite institutional access (log the specific reason in `exclusion_detail`)
- `non_peer_reviewed_not_eligible` — a preprint/conference paper excluded per this review's evidence-tier rules (see Section 12 of the search strategy document) where no published version exists and the finding needed cannot rely on a preprint alone
- `other` — record why in `exclusion_detail`

## `chapter_claim_audit.csv` — `support_status`

- `Verified` — the claim is directly, specifically supported by full text at the cited page/table/figure
- `Partially verified` — full text supports the general claim but not every specific number/detail in the paragraph
- `Unsupported` — full text does not support the claim as written, or full text contradicts it
- `Conceptual synthesis` — this is the review's own original analytical content (a definition, a framework distinction, a bridging argument), not an empirical claim requiring a citation
- `Requires additional evidence` — full text has not yet been obtained/read for the cited source(s)

## `chapter_claim_audit.csv` — `claim_type` (suggested, not exhaustive — extend as needed and note additions here)

- `quantitative_finding` — a specific number, percentage, coefficient, or statistic
- `qualitative_finding` — a directional or comparative finding without a specific number
- `method_description` — describes what a method does, not a specific result
- `framework_definition` — this review's own conceptual/formal contribution
- `evidence_gap_statement` — a claim that evidence is absent/mixed/contested

## `table_cell_evidence_audit.csv` — `evidence_strength`

- `strong` — directly stated in cited source's results/tables, page/table/figure identified
- `moderate` — inferable from cited source but not stated in exactly this form
- `weak` — abstract/snippet-derived only, not yet confirmed against full text
- `contradicted` — a different source, or the same source read in full, contradicts this cell
- `unsupported` — no citation currently supports this cell as written

## `table_cell_evidence_audit.csv` and `chapter_claim_audit.csv` — `retain_revise_remove` / `required_action`

- `retain` — no change needed
- `revise_wording` — claim is directionally correct but wording overstates/understates it
- `revise_citation` — needs a different or additional citation
- `remove` — claim cannot be supported and should be deleted from the main text
- `flag_pending` — cannot resolve until full text is obtained; leave as-is with the pending flag intact
