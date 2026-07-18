#!/usr/bin/env python3
"""
WBE_Review_Section_Word_Count.csv generator.

Parses WBE_Review_Ch1-10.md and produces per-chapter, per-section counts of:
  - body words (prose, excluding markdown control chars, table syntax,
    citation markers themselves, and internal-note/meta content)
  - heading words
  - table words (content inside | ... | rows, excluding separator rows)
  - caption/box words (blockquote-style Box content, and Table/Figure/Box
    heading lines are already captured under heading words)
  - citation marker count (regex matches of [12], [7,8], [32b], [1-3] etc.)
  - paragraph count
  - equation count (inline $...$ math spans, a proxy for equation density)

Method and known limitations are documented in WBE_Review_Word_Count_Method.md.
This script is deterministic and re-runnable; it does not depend on any
cached or previously-reported word-count figure.
"""
import re
import csv
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "WBE_Review_Ch1-10.md"
OUT = Path(__file__).resolve().parent.parent / "WBE_Review_Section_Word_Count.csv"

CITATION_RE = re.compile(r"\[\d+[a-z]?(?:\s*[,\-–]\s*\d+[a-z]?)*\]")
# Prose-style citations this document actually uses predominantly:
# "Author et al. (2023)", "Author et al., 2023", "Author & Author 2025",
# "(WHO, 2025a)", "(NASEM, 2023)". These are NOT stripped from body word
# counts (they are ordinary sentence words, not bare reference numbers),
# but ARE counted separately as citation instances alongside bracket refs.
CITATION_PROSE_RE = re.compile(
    r"[A-Z][a-zA-Z]+(?:,? (?:and|&) [A-Z][a-zA-Z]+)?,? et al\.?,? \(?20\d{2}[a-z]?\)?"
    r"|[A-Z][a-zA-Z]+ (?:and|&) [A-Z][a-zA-Z]+ \(?20\d{2}[a-z]?\)?"
    r"|\([A-Z][a-zA-Z]+,? 20\d{2}[a-z]?\)"
)
MATH_RE = re.compile(r"\$[^$\n]+\$")
MD_CONTROL_RE = re.compile(r"[*_`#>]")
HTML_TAG_RE = re.compile(r"<[^>]+>")
TABLE_SEP_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$")


def strip_for_wordcount(line: str) -> str:
    """Remove markdown control chars, citation markers, math spans, HTML tags."""
    s = CITATION_RE.sub(" ", line)
    s = MATH_RE.sub(" ", s)
    s = HTML_TAG_RE.sub(" ", s)
    s = MD_CONTROL_RE.sub(" ", s)
    # remove leading table pipes / cell separators if any slipped through
    s = s.replace("|", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def count_words(s: str) -> int:
    s = strip_for_wordcount(s)
    if not s:
        return 0
    return len(s.split())


def count_citations(line: str) -> int:
    return len(CITATION_RE.findall(line)) + len(CITATION_PROSE_RE.findall(line))


def count_equations(line: str) -> int:
    return len(MATH_RE.findall(line))


META_HEADINGS = {
    "Note on companion files",
    "Editorial self-check (author-requested audit)",
    "Structural bridge from Chapters 1–4 to Chapter 5 (retained from previous delivery)",
    "Structural bridge from Chapter 5 to Chapter 6 (new this round)",
    "Structural bridge from Chapter 6 to Chapter 7 (new this round)",
    "Structural bridge from Chapter 7 to Chapter 8 (new this round)",
    "Structural bridge from Chapter 8 to Chapter 9 (new this round)",
    "Structural bridge from Chapter 9 to Chapter 10 (new this round)",
}


def main():
    lines = SRC.read_text(encoding="utf-8").splitlines()

    rows = []
    # state
    chapter = "FRONT_MATTER"
    chapter_is_meta = True  # title + status note before Chapter 1
    section = "Title and status note"
    section_is_meta = True

    def new_accumulator():
        return {
            "body_words": 0, "heading_words": 0, "table_words": 0,
            "box_words": 0, "citations": 0, "paragraphs": 0, "equations": 0,
        }

    acc = new_accumulator()
    in_paragraph = False
    in_blockquote = False

    def flush(ch, ch_meta, sec, sec_meta, a):
        if a["body_words"] or a["heading_words"] or a["table_words"] or a["box_words"] or a["citations"] or a["paragraphs"] or a["equations"]:
            rows.append({
                "chapter": ch, "section": sec, "is_internal_note": ch_meta or sec_meta,
                **a,
            })

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()

        # chapter-level heading (##, but not ###)
        if re.match(r"^##\s+\S", line) and not line.startswith("###"):
            flush(chapter, chapter_is_meta, section, section_is_meta, acc)
            acc = new_accumulator()
            heading_text = re.sub(r"^##\s+", "", line).strip()
            chapter = heading_text
            chapter_is_meta = heading_text in META_HEADINGS
            section = "(chapter preamble)"
            section_is_meta = chapter_is_meta
            acc["heading_words"] += count_words(heading_text)
            acc["citations"] += count_citations(heading_text)
            in_paragraph = False
            in_blockquote = False
            continue

        # section-level heading (###)
        if re.match(r"^###\s+\S", line):
            flush(chapter, chapter_is_meta, section, section_is_meta, acc)
            acc = new_accumulator()
            heading_text = re.sub(r"^###\s+", "", line).strip()
            section = heading_text
            section_is_meta = chapter_is_meta
            acc["heading_words"] += count_words(heading_text)
            acc["citations"] += count_citations(heading_text)
            in_paragraph = False
            in_blockquote = False
            continue

        # horizontal rule
        if re.match(r"^-{3,}$", stripped):
            in_paragraph = False
            in_blockquote = False
            continue

        # blank line
        if stripped == "":
            in_paragraph = False
            in_blockquote = False
            continue

        # table row (including header/separator)
        if stripped.startswith("|"):
            if TABLE_SEP_RE.match(stripped):
                continue  # separator row carries no words
            acc["table_words"] += count_words(stripped)
            acc["citations"] += count_citations(stripped)
            acc["equations"] += count_equations(stripped)
            in_paragraph = False
            continue

        # blockquote (Box content)
        if stripped.startswith(">"):
            acc["box_words"] += count_words(stripped)
            acc["citations"] += count_citations(stripped)
            acc["equations"] += count_equations(stripped)
            if not in_blockquote:
                acc["paragraphs"] += 1
            in_blockquote = True
            in_paragraph = False
            continue

        # ordinary body text (including list items, numbered items, bold labels)
        acc["body_words"] += count_words(stripped)
        acc["citations"] += count_citations(stripped)
        acc["equations"] += count_equations(stripped)
        if not in_paragraph:
            acc["paragraphs"] += 1
        in_paragraph = True
        in_blockquote = False

    flush(chapter, chapter_is_meta, section, section_is_meta, acc)

    total_body = sum(r["body_words"] for r in rows)
    total_heading = sum(r["heading_words"] for r in rows)
    total_table = sum(r["table_words"] for r in rows)
    total_box = sum(r["box_words"] for r in rows)
    grand_total = total_body + total_heading + total_table + total_box

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "chapter", "section", "is_internal_note",
            "body_words", "heading_words", "table_words", "box_caption_words",
            "citation_marker_count", "paragraph_count", "equation_count",
            "section_total_words", "pct_of_document_total",
        ])
        for r in rows:
            section_total = r["body_words"] + r["heading_words"] + r["table_words"] + r["box_words"]
            pct = 100.0 * section_total / grand_total if grand_total else 0.0
            w.writerow([
                r["chapter"], r["section"], r["is_internal_note"],
                r["body_words"], r["heading_words"], r["table_words"], r["box_words"],
                r["citations"], r["paragraphs"], r["equations"],
                section_total, f"{pct:.2f}",
            ])

    # summary to stdout (also captured into the method file / report)
    print(f"Rows written: {len(rows)}")
    print(f"TOTAL document words (body+heading+table+box): {grand_total}")
    print(f"  body_words:    {total_body}")
    print(f"  heading_words: {total_heading}")
    print(f"  table_words:   {total_table}")
    print(f"  box_words:     {total_box}")
    internal_note_total = sum(
        r["body_words"] + r["heading_words"] + r["table_words"] + r["box_words"]
        for r in rows if r["is_internal_note"]
    )
    chapter_body_total = grand_total - internal_note_total
    print(f"  internal_note_words (meta/status/companion-file sections): {internal_note_total}")
    print(f"  chapter_body_total (Chapters 1-10 only, all categories):   {chapter_body_total}")
    total_citations = sum(r["citations"] for r in rows)
    total_paragraphs = sum(r["paragraphs"] for r in rows)
    total_equations = sum(r["equations"] for r in rows)
    print(f"  total citation markers: {total_citations}")
    print(f"  total paragraphs:       {total_paragraphs}")
    print(f"  total equation spans:   {total_equations}")


if __name__ == "__main__":
    main()
