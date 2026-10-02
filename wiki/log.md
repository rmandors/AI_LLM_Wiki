# Log

Append-only record of what happened to the wiki. Format and kinds are defined in
`AGENTS.md`. Latest entries: `grep "^## \[" wiki/log.md | tail -5`. Catalog: [[index]].

## [2026-10-01] setup | Wiki created from Karpathy's LLM Wiki gist
- Downloaded the gist to `_meta/llm-wiki.md`; wrote the schema `AGENTS.md`.
- Decisions with Raymond: Obsidian wikilinks + frontmatter; English; ingest course
  materials now and textbooks only for chapters the slides cover; study features =
  practice questions, exam-review sheets, code walkthroughs, comparison tables.
- Tooling: `.venv` (python-pptx, pypdf, python-docx), `tools/extract.py` (raw → text cache
  in `_meta/extracted/`), `tools/lint.py` (links, orphans, frontmatter, index coverage).

## [2026-10-01] ingest | Initial batch: all course materials in raw/
- Slides: [[slides-00-instructor-introduction]], [[slides-01-introduction-to-ai]],
  [[slides-02-problem-solving]], [[slides-03-intelligent-agents]], [[slides-04-optimization]],
  [[slides-xx-logic-programming-prolog]].
- Papers: [[holland-1992-genetic-algorithms]], [[kennedy-eberhart-1995-pso]],
  [[dorigo-1996-ant-system]].
- Textbooks (chapters relevant to taught units only): [[russell-norvig-aima]] Ch. 1–9 and
  §4.1–4.2; [[luger-ai-6e]] §14.2–14.3; [[eiben-smith-evolutionary-computing]] selected sections of
  Ch. 2–6 and 16 (listed on its page).
- Raymond's work: [[hw01-report]], [[hw01-ai-transcript]],
  [[discussion-01-astar-vs-dijkstra]], [[lab01-prolog-family-report]],
  [[ga-exercise-explanation]], and 14 code pages (Python and Prolog; code was re-run
  where it was safe, without writing into `raw/`).
- Created: 53 concept pages, 11 people, 17 sources, 14 code, 9 comparisons, 8 exam-review
  sheets, [[overview]], [[index]], [[midterm-01-review]].
- Contradictions flagged (details on each page): Prolog attributed to Dennis Ritchie
  (slides 01, slide 9); A* "complete if admissible" (slides 02, slide 14); MRV filed under
  constraint propagation (slides 02, slide 24); logic text on "What is an agent?"
  (slides 03, slide 2); GA dated 1975 and 1992 (slides 04); world/transition model naming
  (slides 03, slide 15); Discussion 01 expansion counts (5 vs 13 counted differently);
  9H vs 9I in the 80-tile statement.
- Bugs found in code: `binaryTree.pl` delete2 drops the left subtree; `isMerged` returns
  duplicates; SA cooling 0.8/iteration makes it hill climbing after ~50 iterations; PSO
  without inertia diverges after converging; GA can stall on a Hamming cliff; tic-tac-toe
  AI may delay an available win.
- Gaps: image-only slides (listed per source page); `family.pl` and the HW02 statement are
  not in `raw/`; Midterm 1 scope unconfirmed.

## [2026-10-01] schema | Removed a private HW01 study-notes file
- Deleted the markdown study notes from `raw/HW_01/` and the source page that summarized them.
- Removed every citation and mention. Facts that remain now cite [[hw01-report]], the code pages, or [[russell-norvig-aima]].
- Updated: [[index]], [[overview]], [[log]].
