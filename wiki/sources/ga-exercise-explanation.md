---
type: source
summary: Raymond's one-page write-up (17/09/2026) explaining his class-exercise genetic algorithm — encoding, elitism, crossover, mutation and the run that reached f = 10 by epoch 7.
unit: 9
tags: [genetic-algorithms, class-exercise, raymond-work]
sources: ["[[ga-exercise-explanation]]"]
updated: 2026-10-01
---

# GA class activity — explanation (Raymond Portilla)

**Bibliographic line.** R. Portilla, "Class Activity — Writing a Genetic Algorithm,"
Artificial Intelligence NRC 1651, USFQ, dated 17/09/2026. Files:
`raw/Class_exercises/Genetic Algorithm Exercise/Explanation_RP.docx` and `Explanation_RP.pdf`.

**What it is.** Raymond's short explanation of his program [[genetic-algorithm-py]], answering
the prompt "Provide a short explanation of the algorithm and the choices it made through its
execution." It is a source for *design intent* and for one run's results; the code page checks
the claims against the code.

## Key points

- **Problem.** Minimise $f(x,y) = (x+2)^2 + (y-2)^2 + 10$ by evolving bit-string solutions;
  "lower is better" (fitness = $f$ of the decoded point).
- **Encoding.** 16-bit chromosome, 8 bits per variable; the first bit of each half is the sign
  and the other 7 bits a magnitude scaled by 10, so each variable lies in about
  $[-12.7, 12.7]$.
- **Generation step.** Rank the 100 individuals; **elitism** copies the top 10 unchanged "so
  the current best can't be lost"; the other 90 come from picking two elites at random,
  **single-point crossover**, then **uniform bit-flip mutation** with probability $1/16$ per
  bit. Rationale given: "crossover recombines good fragments, mutation adds small random
  exploration, and elitism keeps the search from sliding backward".
- **Reported run.** Start near the bowl at about $(-1.5, 2.0)$ with $f = 10.25$; elite path
  $(-2.3, 2.1) \to (-1.9, 2.0) \to (-2.0, 2.0)$; **exact minimum $f = 10$ by epoch 7**; flat
  afterwards because elitism keeps the solution and mutations only perturb copies.

## Pages that use this source

[[genetic-algorithm-py]], [[genetic-algorithms]], [[unit-09-optimization-review]].

## Issues found

> [!warning] Typo in the write-up
> The PDF says "The true minimum is at $(-2, 0)$ with $f = 10$". From the formula, the minimum
> is at $(-2, \mathbf{2})$; $f(-2, 0) = 14$. The code and the rest of the write-up use
> $(-2, 2)$ correctly. Fix before submitting anything derived from it.

- **Extraction.** The `.docx` extraction lost every inline equation (blanks where $f$, $(x,y)$
  and intervals were). The `.pdf` extraction keeps them, except squares render as "!"
  ($(x+2)^!$). The wiki uses the PDF text.
- Small wording slip: "8 bits $x$ for and 8 for $y$" (should read "8 bits for $x$").
- **Claims worth qualifying.** "Mutation adds *small* random exploration" is only
  partly true: flipping the top magnitude bit moves a variable by 6.4. And the run is one
  random seed; re-runs show convergence is usually fast but one seed stalled for 75
  generations at $x = -1.9$ (see [[genetic-algorithm-py]], *Results*).
