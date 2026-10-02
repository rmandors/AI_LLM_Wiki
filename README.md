# AI Course Wiki

A personal study wiki for Artificial Intelligence at Universidad San Francisco de Quito
(NRC 1651, Fall 2026). It follows the [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
pattern: raw sources stay untouched, and an LLM maintains a linked set of markdown pages
on top of them. A copy of the gist is in `_meta/llm-wiki.md`. The rules the agent follows
are in `AGENTS.md`.

Open the repo folder as an Obsidian vault. Start at [`wiki/index.md`](wiki/index.md)
(every page, one line each) or [`wiki/overview.md`](wiki/overview.md) (course map).
Practice questions are collapsed; click one to show the answer. Open **Graph view** to see
how the pages connect: hubs, clusters per unit, and pages with no links.

## Layout

| Path | What it is | Who writes it |
|---|---|---|
| `raw/` | Slides, homework, code, papers, textbooks. Immutable. | You |
| `wiki/` | Concept pages, source summaries, code walkthroughs, comparisons, exam sheets | The agent |
| `wiki/index.md` | Catalog. Read this first when asking a question | The agent |
| `wiki/log.md` | Append-only history of ingests and changes | The agent |
| `AGENTS.md` | Schema: page format, citations, ingest / query / lint workflows | Both |
| `_meta/extracted/` | Disposable plain-text cache of `raw/` (git-ignored) | `tools/extract.py` |
| `tools/` | `extract.py` and `lint.py` | — |

Wikilinks look like `[[a-star]]`. Obsidian resolves them by file name, so names are unique
across the vault.

## Studying

- Browse from the index, or open a unit cheat sheet under `wiki/exam-review/`.
- [`wiki/exam-review/midterm-01-review.md`](wiki/exam-review/midterm-01-review.md) collects
  the sheets, a one-week plan, and mixed questions for the October 8 midterm.
- Ask an LLM that can read this folder, in plain language, for example: "Using the wiki,
  when is A* optimal?" It should read the index, answer with links to pages, and can file
  a useful answer back into the wiki.

## Adding a source

1. Drop the file anywhere under `raw/` (for example `raw/HW_02/`). Do not edit files
   that are already there; add a new one instead.
2. Tell the agent to ingest it. It extracts the text, writes a source page, updates the
   concept pages the source affects, refreshes the index, and appends to the log.

Textbooks are ingested chapter by chapter, when the course reaches that topic.

## Checks

```bash
.venv/bin/python tools/extract.py   # refresh the text cache (only new or changed files)
.venv/bin/python tools/lint.py      # broken links, orphans, missing frontmatter, index coverage
```

`tools/lint.py` checks structure. Contradictions between pages are reviewed by reading,
not by the script. Ask the agent to "lint the wiki" to do both.
