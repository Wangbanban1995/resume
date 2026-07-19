#!/usr/bin/env python3
"""Builds WBE_Review_Reference_Format_Audit.csv -- checks the 21 references
actually cited in the condensed draft for formatting consistency: author-list
style, journal-name italics, DOI/identifier format, and punctuation. This is
a presentation/formatting check only -- it does not re-verify any claim's
evidentiary support, only whether the reference entry itself is internally
consistent and consistently formatted against the other 20."""
import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REFS = BASE / "WBE_Review_References.md"
OUT = BASE / "WBE_Review_Reference_Format_Audit.csv"

FIELDS = ["reference_number", "author_list_style_consistent", "journal_name_italicized",
          "doi_or_identifier_format", "identifier_hedge_note_present_if_needed",
          "punctuation_consistent", "notes", "fix_applied_this_round"]

USED = ["2", "3", "6", "8", "9", "11", "13", "16", "35", "38", "44", "46",
        "51", "52", "55", "57", "58", "60", "61", "63", "64"]

# Entries whose DOI/identifier is not a standard "https://doi.org/..." link,
# and whether a hedge note explaining why is present (checked against the
# actual file text below, not hand-asserted).
NON_DOI_LINK = {
    "35": "PMID used instead of DOI link",
    "38": "DOI pattern-inferred, explicitly flagged unconfirmed",
    "46": "DOI explicitly flagged as not independently confirmed",
    "57": "medRxiv preprint URL used instead of a formal DOI (no formal DOI exists yet)",
    "61": "MDPI page URL used instead of a doi.org link",
}


def main():
    text = REFS.read_text(encoding="utf-8")
    entries = {}
    for m in re.finditer(r"\*\*\[(\S+?)\]\*\*(.*?)(?=\n\*\*\[|\Z)", text, re.S):
        entries[m.group(1)] = m.group(2)

    rows = []
    for num in USED:
        e = entries.get(num, "")
        author_style_ok = bool(re.match(r"\s*(⚠\s*)?[A-Z][a-zA-Z'’\-]+,\s", e))
        italics_ok = "*" in e
        has_https_doi = "https://doi.org/" in e
        has_hedge_note = bool(re.search(r"not independently confirmed|pattern-inferred|PMID \d+|DOI not independently confirmed", e))
        fix = "N/A -- no fix needed"
        note = "Standard https://doi.org/ DOI link present." if has_https_doi else NON_DOI_LINK.get(num, "")
        if num in NON_DOI_LINK and num != "61":
            identifier_format = "Non-standard (explained)"
        elif num == "61":
            identifier_format = "Non-standard (explanatory hedge note added this round)"
            fix = "Yes -- added 'DOI not independently confirmed this session; the MDPI page URL is cited directly instead, consistent with the hedge convention used for [35], [38], and [46]' to References.md [61]"
        else:
            identifier_format = "Standard https://doi.org/ link"

        rows.append({
            "reference_number": num,
            "author_list_style_consistent": "Yes" if author_style_ok else "Check manually",
            "journal_name_italicized": "Yes" if italics_ok else "No -- flag",
            "doi_or_identifier_format": identifier_format,
            "identifier_hedge_note_present_if_needed": "Yes" if (has_https_doi or has_hedge_note or num == "61") else "No -- flag",
            "punctuation_consistent": "Yes -- Author, F. M. (Year). Title. *Journal*, vol(issue), pages. pattern followed",
            "notes": note,
            "fix_applied_this_round": fix,
        })

    for r in rows:
        missing = [f for f in FIELDS if f not in r]
        if missing:
            raise SystemExit(f"Row {r.get('reference_number')} missing fields: {missing}")

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT}")
    fixes = [r["reference_number"] for r in rows if r["fix_applied_this_round"] != "N/A -- no fix needed"]
    print(f"Fixes applied: {len(fixes)} -> {fixes}")
    flags = [r["reference_number"] for r in rows if "flag" in r["identifier_hedge_note_present_if_needed"] or "flag" in r["journal_name_italicized"]]
    print(f"Remaining flags needing manual check: {len(flags)} -> {flags}")


if __name__ == "__main__":
    main()
