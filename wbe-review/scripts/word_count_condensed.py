#!/usr/bin/env python3
"""
Word counts for WBE_Review_WR_Condensed_Draft.md, using the same counting
method as scripts/word_count.py (strip citation markers, math, markdown
control chars; count table words separately from body words), applied to
the condensed draft's own structure: Parts are ## headings, subsections
are ### headings. Placeholder Parts 5-8 are reported but excluded from the
"drafted total" figure since they are not prose.
"""
import re
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "WBE_Review_WR_Condensed_Draft.md"

CITATION_RE = re.compile(r"\[\d+[a-z]?(?:\s*[,\-–]\s*\d+[a-z]?)*\]")
CITATION_PROSE_RE = re.compile(
    r"[A-Z][a-zA-Z]+(?:,? (?:and|&) [A-Z][a-zA-Z]+)?,? et al\.?,? \(?20\d{2}[a-z]?\)?"
    r"|[A-Z][a-zA-Z]+ (?:and|&) [A-Z][a-zA-Z]+ \(?20\d{2}[a-z]?\)?"
    r"|\([A-Z][a-zA-Z]+,? 20\d{2}[a-z]?\)"
)
MATH_RE = re.compile(r"\$[^$\n]+\$")
MD_CONTROL_RE = re.compile(r"[*_`#>]")
TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$")


def strip_for_wordcount(line: str) -> str:
    s = CITATION_RE.sub(" ", line)
    s = CITATION_PROSE_RE.sub(" ", s)
    s = MATH_RE.sub(" ", s)
    s = MD_CONTROL_RE.sub(" ", s)
    s = s.replace("|", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def count_words(s: str) -> int:
    s = strip_for_wordcount(s)
    return len(s.split()) if s else 0


def main():
    lines = SRC.read_text(encoding="utf-8").splitlines()
    part = "FRONT_MATTER"
    section = "(preamble)"
    rows = []

    def new_acc():
        return {"body": 0, "heading": 0, "table": 0}

    acc = new_acc()

    def flush():
        if acc["body"] or acc["heading"] or acc["table"]:
            rows.append({"part": part, "section": section, **acc, "total": acc["body"] + acc["heading"] + acc["table"]})

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if re.match(r"^##\s+\S", line) and not line.startswith("###"):
            flush()
            acc = new_acc()
            part = re.sub(r"^##\s+", "", line).strip()
            section = "(preamble)"
            acc["heading"] += count_words(part)
            continue
        if re.match(r"^###\s+\S", line):
            flush()
            acc = new_acc()
            section = re.sub(r"^###\s+", "", line).strip()
            acc["heading"] += count_words(section)
            continue
        if re.match(r"^-{3,}$", stripped) or stripped == "":
            continue
        if stripped.startswith("|"):
            if TABLE_SEP_RE.match(stripped):
                continue
            acc["table"] += count_words(stripped)
            continue
        acc["body"] += count_words(stripped)
    flush()

    # aggregate by part
    part_totals = {}
    order = []
    for r in rows:
        if r["part"] not in part_totals:
            part_totals[r["part"]] = {"body": 0, "heading": 0, "table": 0, "total": 0}
            order.append(r["part"])
        for k in ("body", "heading", "table", "total"):
            part_totals[r["part"]][k] += r[k]

    print(f"{'Part':60s} {'body':>6s} {'heading':>8s} {'table':>6s} {'total':>7s}")
    grand_total = 0
    drafted_total = 0
    for p in order:
        t = part_totals[p]
        print(f"{p[:58]:60s} {t['body']:6d} {t['heading']:8d} {t['table']:6d} {t['total']:7d}")
        grand_total += t["total"]
        if p.split(".")[0].strip().isdigit() and int(p.split(".")[0].strip()) <= 8:
            drafted_total += t["total"]
        elif p == "FRONT_MATTER":
            pass

    print(f"\nGrand total (all parts + front matter, incl. placeholders' brief text): {grand_total}")
    print(f"Drafted Parts 1-8 total (body+heading+table): {drafted_total}")

    out_csv = BASE / "WBE_Review_Condensed_Draft_Word_Count.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["part", "section", "body_words", "heading_words", "table_words", "section_total"])
        for r in rows:
            w.writerow([r["part"], r["section"], r["body"], r["heading"], r["table"], r["total"]])
    print(f"\nWrote per-section detail to {out_csv}")


if __name__ == "__main__":
    main()
