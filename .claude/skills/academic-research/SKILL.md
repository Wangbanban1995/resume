---
name: academic-research
description: Conduct academic and scholarly research - searching for papers, evaluating source credibility, summarizing findings, structuring literature reviews, and formatting citations (APA, MLA, Chicago, IEEE, GB/T 7714). Use this skill whenever the user asks to find research papers, review literature on a topic, summarize academic sources, check citation formatting, build a bibliography, or otherwise do scholarly/academic research, even if they don't use the word "academic" explicitly (e.g. "find papers on X", "what does the literature say about Y", "help me cite this").
---

# Academic Research

A skill for finding, evaluating, synthesizing, and citing scholarly sources.

## When this applies

Use this skill for tasks like:
- Finding papers, articles, or studies on a topic
- Summarizing or synthesizing what the literature says
- Structuring a literature review or related-work section
- Evaluating whether a source is credible/citable
- Formatting citations and building a bibliography
- Extracting key findings, methods, or data from a paper (PDF or web)

For extracting text/tables from PDF files themselves, combine this skill with the `pdf` or `pdf-reading` skill if available — this skill focuses on the research workflow, not file parsing mechanics.

## Workflow

### 1. Clarify the research question

Before searching, make sure you know:
- The specific question or claim being investigated (not just a broad topic)
- Scope: time range, discipline, geographic/population constraints
- Depth needed: a quick answer with a few sources, or a systematic literature review
- Required citation style (ask if unspecified and citations will be delivered to the user)

If the request is vague ("research AI safety"), narrow it with the user rather than guessing — a research task with the wrong scope wastes the most effort of any task type.

### 2. Search strategically

- Prefer searching for the underlying concept and key terms rather than the user's exact phrasing; academic writing uses different vocabulary than conversational questions.
- Use multiple query variations (synonyms, broader/narrower terms) rather than one search — a single query systematically misses relevant work.
- Prioritize, in roughly this order: peer-reviewed journal articles and conference proceedings, official preprint servers (arXiv, bioRxiv, SSRN), university/government/institutional reports, reputable science journalism, then general web content. Note the tier explicitly when it affects how much weight a claim should carry.
- Look for recent review/survey papers first when starting on an unfamiliar topic — they map the field faster than reading primary sources one at a time.
- Track citation counts and publication venue as rough (not definitive) signals of influence and rigor.

### 3. Evaluate sources before relying on them

For each source, note:
- **Authorship & venue**: peer-reviewed journal, reputable preprint server, or unvetted source?
- **Recency**: still current, or superseded by later work? (Matters far more in fast-moving fields.)
- **Methodology**: sample size, study design, potential conflicts of interest or funding bias.
- **Corroboration**: is the finding replicated or contradicted elsewhere in the literature?

Flag single-study findings, small samples, or contested claims explicitly rather than presenting them with the same confidence as well-established consensus.

### 4. Synthesize, don't just list

When summarizing multiple sources:
- Organize by theme, question, or chronology — not just "source 1 says X, source 2 says Y."
- Explicitly surface agreement, disagreement, and open questions across sources.
- Distinguish the source's claims from your own inference or interpretation.
- Attribute specific claims to specific sources inline (e.g., "(Smith et al., 2023)") so the user can trace every claim back to evidence.

### 5. Cite accurately

- Ask which citation style is required if not specified (APA, MLA, Chicago, IEEE, GB/T 7714, etc.) — don't assume.
- Only cite sources actually retrieved/verified this session; never fabricate authors, titles, years, DOIs, or page numbers. If a citation can't be verified, say so instead of inventing plausible-looking details.
- Keep a running bibliography as sources are gathered rather than reconstructing it from memory at the end.

See `references/citation_styles.md` for formatting templates across common styles.

## Output format

Default structure for a research summary (adapt to the request):

```markdown
## Research question
[Restate the question/scope]

## Key findings
- [Finding, attributed inline to source]
- [Finding, attributed inline to source]

## Areas of disagreement / uncertainty
[Where sources conflict, or evidence is thin]

## Sources
[Formatted bibliography in the requested citation style]
```

For a full literature review, use: Introduction/scope → Thematic sections → Synthesis/gaps → Bibliography.
