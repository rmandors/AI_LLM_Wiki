---
type: concept
summary: General-purpose CSP heuristics — MRV ("fail-first") and degree for choosing the next variable, LCV ("fail-last") for ordering its values, and min-conflicts for local search over complete assignments.
unit: 3
tags: [csp, mrv, degree-heuristic, lcv, min-conflicts, variable-ordering]
sources: ["[[russell-norvig-aima]]", "[[slides-02-problem-solving]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# CSP heuristics: MRV, degree, LCV, min-conflicts

Unlike the domain-specific [[heuristic-functions]] of path search, CSP heuristics are **domain-independent**: they only look at variables, domains and constraints, so the same code works for map colouring, N-queens or Sudoku ([[russell-norvig-aima]] §5.3). They fill the two choice hooks of [[csp-backtracking-search]] — *which variable next* and *which value first* — and a third family, **min-conflicts**, replaces backtracking with local search.

## How it works

### Variable ordering (SELECT-UNASSIGNED-VARIABLE)

- **Static ordering**: variables in a fixed order $X_1, X_2, \dots$ (or random). The baseline ([[russell-norvig-aima]] §5.3.1).
- **MRV — minimum remaining values** (a.k.a. *most constrained variable*, *fail-first*): pick the variable with the **fewest legal values left**. If some variable has 0 values, MRV picks it and failure is detected at once. Usually beats static/random ordering, "sometimes by orders of magnitude" ([[russell-norvig-aima]] §5.3.1).
- **Degree heuristic**: pick the variable involved in the **most constraints on other unassigned variables**. Useful at the start (when all domains are equal) and as an **MRV tie-breaker** ([[russell-norvig-aima]] §5.3.1).

### Value ordering (ORDER-DOMAIN-VALUES)

- **LCV — least constraining value** (*fail-last*): try first the value that **rules out the fewest choices** for neighbouring variables, leaving maximum flexibility ([[russell-norvig-aima]] §5.3.1).
- Why fail-first for variables but fail-last for values? Every variable must be assigned eventually, so failing early prunes; but we need only **one** solution, so we try the most promising value first. When enumerating **all** solutions, value ordering is irrelevant ([[russell-norvig-aima]] §5.3.1).

### Local search: min-conflicts

Start from a **complete** (usually inconsistent) assignment; repeatedly pick a random **conflicted** variable and give it the value that **minimises the number of violated constraints** ([[russell-norvig-aima]] §5.4, Fig. 5.9):

```text
MIN-CONFLICTS(csp, max_steps):
    current = an initial complete assignment
    for i in 1..max_steps:
        if current is a solution: return current
        var = random conflicted variable
        value = argmin_v CONFLICTS(var, v, current)
        set var = value
    return failure
```

On n-queens its run time is roughly independent of $n$: about **50 steps for a million queens** (after the initial placement), because solutions are dense ([[russell-norvig-aima]] §5.4). It is a form of [[hill-climbing]]; plateaus are handled with sideways moves, **tabu search**, [[simulated-annealing]] or **constraint weighting** ([[russell-norvig-aima]] §5.4). Local search also suits **online repair** (e.g. rescheduling flights after bad weather).

(Forward checking and MAC are *inference*, not ordering heuristics → [[constraint-propagation]]. MRV and forward checking work best together: "forward checking is an efficient way to incrementally compute the information that the MRV heuristic needs" — [[russell-norvig-aima]] §5.3.2.)

### Worked examples (Australia, R&N Fig. 5.1)

- **Degree at the start**: all regions have 3 colours, so MRV ties; degree picks **SA** (degree 5; others 2-3, T has 0) ([[russell-norvig-aima]] §5.3.1).
- **MRV**: after WA = red, NT = green, SA has only {blue} → MRV assigns SA next; then Q, NSW, V are forced ([[russell-norvig-aima]] §5.3.1).
- **LCV**: with WA = red, NT = green, choosing a colour for Q: blue would remove SA's last value, red removes nothing critical → LCV tries **red** first ([[russell-norvig-aima]] §5.3.1).

## Properties

| Heuristic | Decides | Principle | Cost per node | Keeps completeness? |
|---|---|---|---|---|
| MRV | next variable | fail-first | scan all unassigned domains | yes |
| Degree | next variable (tie-break) | reduce future branching | count constraints | yes |
| LCV | value order | fail-last | score each value against neighbours | yes |
| Min-conflicts | complete-state repair | greedy local search | count conflicts per value | **no** (may cycle / hit max_steps) |

## In this course

- Slide 24 of [[slides-02-problem-solving]] lists "Minimum Remaining Values" together with forward checking and arc consistency under constraint propagation — see the contradiction note on [[constraint-satisfaction-problems]]. **Slide 25 is image-only.**
- **HW01 Sudoku** ([[hw01-ex06-sudoku]]) implements MRV (`find_empty_mrv`, ties broken by row-major order, no degree tie-break) and LCV (`lcv_score` + `order_values_lcv`), each alone against naive backtracking:

| Board | Naive | MRV | LCV |
|---|---|---|---|
| 1 (30 givens) | 4,208 | **51** (0 backtracks) | 2,084 |
| 2 (22 givens) | 335,637 | **4,036** | 341,523 |

(assignments; [[hw01-report]], Ex. 6) MRV is ~83× fewer assignments on board 2 but only ~2× faster, because each MRV step scans every empty cell. LCV alone is even worse than naive on board 2: value ordering cannot rescue a bad variable ordering ([[hw01-report]], Ex. 6).
- **Re-run 2026-10-01, not in the report**: MRV + LCV together needs only **181** assignments (122 backtracks) on board 2, ≈22× fewer than MRV alone — the pairing R&N recommends. On board 1 it is 51, same as MRV.
- Concrete MRV/LCV values on board 1 (re-run): at the start MRV picks cell (row 4, col 4) (0-indexed), which has 1 legal digit — and 3 other cells tie at 1, so a degree tie-break would matter. For the naive first empty cell (0, 2), legal digits {1, 2, 4} have LCV scores 7, 11, 8, so LCV tries 1, 4, 2.
- **N-Queens** ([[hw01-ex03-n-queens]]) uses no heuristics; MRV and min-conflicts are discussed as alternatives ([[hw01-report]], Ex. 3).

## Common mistakes

- Swapping the slogans: MRV is **fail-first** (variables), LCV is **fail-last** (values).
- Using LCV when counting all solutions — it only adds overhead ([[russell-norvig-aima]] §5.3.1; that is why [[hw01-ex06-sudoku]] counts with MRV only).
- Expecting fewer nodes to mean proportionally less time: MRV and LCV cost more per node.
- Calling min-conflicts complete. It is a local search: fast, but may get stuck on plateaus.
- Forgetting the degree heuristic's role: it is mainly a tie-breaker, not a replacement for MRV.

## Related

[[csp-backtracking-search]] · [[constraint-propagation]] · [[constraint-satisfaction-problems]] · [[csp-techniques-comparison]] · [[hw01-ex06-sudoku]] · [[hw01-ex03-n-queens]] · [[hill-climbing]] · [[simulated-annealing]] · [[heuristic-functions]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Current domains: A = {1, 2}, B = {1, 2, 3}, C = {2}, D = {1, 2, 3}. B is in 3 constraints with unassigned variables, D in 1. Which variable does MRV pick? And if C did not exist?
> **Answer.** MRV picks **C** (1 value). Without C, A (2 values) is the unique minimum, so A. If A and C were both absent, B and D tie at 3 values and the degree heuristic breaks the tie in favour of **B** (degree 3).

> [!question]- Q2. Why is MRV called "fail-first" and why is that good?
> **Answer.** It chooses the variable most likely to fail soon. Since every variable must be assigned anyway, discovering a dead end early prunes the subtree before more work is wasted ([[russell-norvig-aima]] §5.3.1).

> [!question]- Q3. A cell has legal digits {1, 2, 4}; placing 1 removes an option from 7 empty neighbours, 2 from 11, 4 from 8. In which order does LCV try them?
> **Answer.** Smallest score first: **1, 4, 2** (scores 7, 8, 11). This is board 1's first empty cell in [[hw01-ex06-sudoku]] (re-run 2026-10-01).

> [!question]- Q4. On Sudoku board 2, LCV alone used 341,523 assignments vs 335,637 for naive. Why can LCV be worse?
> **Answer.** LCV only reorders digits; with row-major variable order the search still enters huge wrong subtrees, and scoring every digit costs extra work. LCV helps when combined with a good variable ordering (MRV + LCV: 181 assignments on board 2) ([[hw01-report]], Ex. 6; re-run 2026-10-01).

> [!question]- Q5. Describe one step of min-conflicts on 8-queens.
> **Answer.** With 8 queens on the board (one per column), pick a random queen that is attacked, compute for every row of its column how many queens would attack it there, and move it to the row with the fewest conflicts (ties random) ([[russell-norvig-aima]] §5.4, Fig. 5.8).

> [!question]- Q6. Why does min-conflicts solve n-queens so fast even for $n = 10^6$?
> **Answer.** Solutions are densely distributed in the space of complete assignments, so a greedy repair almost always finds one nearby — about 50 steps on average after the initial assignment ([[russell-norvig-aima]] §5.4).
