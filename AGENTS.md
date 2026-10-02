# AI Course Wiki — Schema

This file tells the LLM agent how this wiki is built and maintained. It follows the
"LLM Wiki" pattern from Karpathy's gist (copy in `_meta/llm-wiki.md`). Read this file
fully before doing any work in the repo. The human (Raymond) curates sources and asks
questions; the agent writes and maintains every page in `wiki/`.

## Context

- Course: Artificial Intelligence, Universidad San Francisco de Quito (USFQ), NRC 1651,
  instructor Daniel Riofrío. Student: Raymond Portilla. 7th semester, Fall 2026.
- Purpose: a study wiki for homeworks, two midterms and the final project.
- Language: English. Viewer: Obsidian (vault root = repo root).
- Base textbook: Russell & Norvig, *AIMA* 4th ed., **Global Edition** (Ch. 5 = CSPs,
  Ch. 6 = Games; the US edition numbers differ). Secondary: Luger 6th ed. (Prolog),
  Eiben & Smith 2nd ed. (evolutionary computing).

## Layers

| Layer | Path | Owner | Rule |
|---|---|---|---|
| Raw sources | `raw/` | Human | **Immutable.** Never edit, move, rename or delete anything here. |
| Text cache | `_meta/extracted/` | Script | Plain-text copies made by `tools/extract.py`. Disposable, git-ignored. |
| Wiki | `wiki/` | Agent | All pages are written by the agent. |
| Schema | `AGENTS.md` | Both | Co-evolved. Update it when a convention changes. |

```
wiki/
  index.md catalog of every page (read this first when answering a query)
  log.md append-only history of ingests, queries, lints
  overview.md course map, syllabus, grading, evolving synthesis
  concepts/ one idea per page (algorithms, definitions, theory)
  people/ entity pages for researchers and the instructor
  sources/ one summary page per raw source (or per textbook)
  code/ walkthroughs of Raymond's own code in raw/
  comparisons/ side-by-side tables (GA vs PSO vs ACO, BFS vs A*,...)
  exam-review/ cheat sheets per unit + midterm hubs
tools/
  extract.py raw/ -> _meta/extracted/ text (pptx, pdf, docx, code)
  lint.py broken links, orphans, missing frontmatter, index coverage
```

## Page conventions

**File names**: lowercase kebab-case, unique across the whole vault (Obsidian resolves
`[[name]]` by file name). Examples: `a-star.md`, `slides-02-problem-solving.md`,
`hw01-ex02-80-tile.md`.

**Frontmatter** (required on every page except `index.md` and `log.md`):

```yaml
---
type: concept | person | source | code | comparison | exam-review | overview
summary: One sentence, used verbatim in index.md.
unit: 1-10 # syllabus unit(s), see table below; list allowed, e.g. [3, 4]
tags: [search, heuristics]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---
```

**Links**: Obsidian wikilinks `[[file-name]]` or `[[file-name|Display text]]`. Link the
first mention of every concept that has its own page. Never use relative markdown links
for internal pages.

**Citations**: every non-obvious claim cites where it came from, inline:
`([[slides-02-problem-solving]], slide 14)`, `([[russell-norvig-aima]] §3.5.2)`,
`([[dorigo-1996-ant-system]], Eq. 4)`. If a claim comes from general knowledge and not
from a source in `raw/`, mark it `(general knowledge)` so it can be verified later.

**Math**: Obsidian MathJax, `$f(n) = g(n) + h(n)$` inline and `$$... $$` for blocks.

**Callouts** (Obsidian syntax):

```markdown
> [!warning] Contradiction
> Slides 01 (slide 9) say Prolog was created by Dennis Ritchie at Bell Labs; the Prolog
> deck (slide 8) says Colmerauer & Roussel, Marseille, 1972. The latter is correct.

> [!tip] Exam tip
>...

> [!question]- Q1. Is greedy best-first search optimal?
> **Answer.** No. It ignores g(n)... ([[russell-norvig-aima]] §3.5.1)
```

The `-` after `[!question]` makes the callout collapsed, so the answer stays hidden until
clicked. Use it for every practice question.

### Page templates

**concept** — sections in this order (skip ones that do not apply):
1. One-paragraph definition in plain words.
2. `## How it works` (pseudocode or steps, formulas).
3. `## Properties` (complete? optimal? time/space; parameters).
4. `## In this course` — what the slides/homework say, with citations; links to
   `code/` pages where Raymond implemented it.
5. `## Common mistakes` / pitfalls.
6. `## Related` — wikilinks.
7. `## Practice questions` — 3-6 collapsed `[!question]-` callouts, mixing recall,
   reasoning, and a small worked computation when possible.

**source** — bibliographic line, what it is, `## Key points` (bulleted, with slide/page
numbers), `## Pages that use this source`, `## Issues found` (errors, contradictions,
image-only slides whose content is missing from the text extraction).

**code** — path to the file in `raw/`, what problem it solves, `## Design decisions`,
`## Walkthrough` (functions with line ranges), `## Results` (numbers), `## Known issues
/ improvements`, `## Related concepts`, and practice questions about the code.

**comparison** — a short intro, one or more tables, then `## When to use which`, and
practice questions.

**exam-review** — dense cheat sheet: definitions, formulas, complexity table, "must
know" facts, common traps, links to concept pages, 8-15 practice questions.

**person** — who, when, contribution to AI relevant to this course, links.

### Syllabus units (from [[slides-00-instructor-introduction]], slide 4)

| Unit | Topic |
|---|---|
| 1 | History and foundations of AI |
| 2 | Intelligent agents and problem formulation |
| 3 | Heuristic search |
| 4 | Adversarial search in games |
| 5 | Knowledge, reasoning and planning |
| 6 | Propositional and first-order logic: Prolog, unification, forward/backward chaining |
| 7 | Uncertainty: probability, Bayes, naive Bayes |
| 8 | Temporal reasoning: Markov models |
| 9 | Optimization and bio-inspired algorithms |
| 10 | Machine learning and neural networks: perceptron; ethics and safety |

CSPs are taught inside the problem-solving deck; tag them unit 3.

## Workflows

### Ingest (new source dropped into `raw/`)
1. Run `.venv/bin/python tools/extract.py` (only new/changed files are processed).
2. Read the extracted text. For image-heavy slides, say which slides had no text.
3. Briefly tell Raymond the key takeaways and ask what to emphasize (skip if he said
   to batch-ingest).
4. Write/update the `sources/` page.
5. Update or create every affected `concepts/`, `people/`, `code/`, `comparisons/`
   and `exam-review/` page. Add citations. Flag contradictions with older pages using
   the `Contradiction` callout instead of silently overwriting.
6. Update `index.md` (add the page under its section with its summary) and
   `overview.md` if the big picture changed.
7. Append a log entry. Run `.venv/bin/python tools/lint.py` and fix what it reports.

**Textbooks** are ingested on demand, chapter by chapter, when the course reaches a
topic — never the whole book at once. Record which sections were read on the textbook's
source page.

### Query
1. Read `index.md`, then the relevant pages; only go back to `_meta/extracted/` if the
   wiki lacks the detail.
2. Answer with wikilink citations.
3. If the answer is reusable (a comparison, a derivation, a worked example), offer to
   file it as a new page; if accepted, file it and log it.

### Lint
Run `tools/lint.py`, then review by reading: contradictions between pages, stale
claims, concepts mentioned without a page, missing cross-links, units without exam
review, questions worth investigating next. Log the pass.

### Exam prep
When Raymond says "prepare me for midterm N", build/refresh the `exam-review/` hub
for that exam, quiz him with the practice questions, and record weak spots on the hub.

## Log format

Append to `wiki/log.md`, newest at the bottom, one heading per event:

```
## [2026-10-01] ingest | Slides 02 Problem Solving
- Created: [[slides-02-problem-solving]], [[a-star]]
- Updated: [[index]], [[heuristic-functions]]
- Notes: slides 8, 10, 13 are image-only.
```

Kinds: `setup`, `ingest`, `query`, `lint`, `schema`, `exam-prep`.
`grep "^## \[" wiki/log.md | tail -5` lists the latest events.

## Honesty rules

- Raymond's own work (homework, code) is a source like any other: describe what it
  does, including its weak spots, so exam answers stay accurate.
- Do not invent results. Numbers come from the reports or from re-running the code.
- When a slide is image-only, say so instead of guessing what the image showed; fill
  the gap from the textbook or paper and cite that.
