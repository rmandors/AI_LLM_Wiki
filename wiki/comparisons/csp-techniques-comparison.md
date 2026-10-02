---
type: comparison
summary: CSP solving techniques side by side — naive backtracking, MRV, degree, LCV, forward checking, AC-3/MAC and min-conflicts — with what each decides, its cost, and the HW01 Sudoku numbers.
unit: 3
tags: [csp, backtracking, mrv, lcv, forward-checking, ac-3, min-conflicts, sudoku, comparison]
sources: ["[[russell-norvig-aima]]", "[[hw01-report]]", "[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# CSP techniques compared

The techniques for [[constraint-satisfaction-problems]] fall into four groups: the **search skeleton** ([[csp-backtracking-search]]), **ordering heuristics** ([[csp-heuristics]]), **inference** ([[constraint-propagation]]), and **local search** (min-conflicts). They are complementary: a strong solver combines one from each of the first three groups.

## What each technique does

| Technique | Group | Hook in Fig. 5.5 | Principle | Complete? | Cost per node | R&N |
|---|---|---|---|---|---|---|
| Naive backtracking | search | — (static order) | DFS over partial assignments, undo on failure | yes | low | §5.3 |
| MRV | ordering | SELECT-UNASSIGNED-VARIABLE | fewest legal values ("fail-first") | yes | scan domains | §5.3.1 |
| Degree | ordering | SELECT-UNASSIGNED-VARIABLE (tie-break) | most constraints on unassigned vars | yes | count edges | §5.3.1 |
| LCV | ordering | ORDER-DOMAIN-VALUES | value that removes fewest neighbour options ("fail-last") | yes | score each value | §5.3.1 |
| Forward checking | inference | INFERENCE | delete inconsistent values from neighbours of the new assignment | yes | $O(\text{neighbours} \cdot d)$ | §5.3.2 |
| AC-3 (preprocessing) | inference | before search | make every arc consistent | yes (it is not a solver by itself) | $O(cd^3)$ | §5.2.2 |
| MAC | inference | INFERENCE | AC-3 from arcs into the new assignment, propagating | yes | ≤ AC-3 | §5.3.2 |
| Backjumping / CBJ | search | on failure | jump to the culprit in the conflict set | yes | bookkeeping | §5.3.3 |
| Min-conflicts | local search | replaces backtracking | repair a complete assignment, minimise violations | **no** | count conflicts | §5.4 |

Power ordering for inference: FC ⊂ MAC (MAC strictly stronger) ([[russell-norvig-aima]] §5.3.2); arc ⊂ path ⊂ k-consistency ([[russell-norvig-aima]] §5.2).

## HW01 Sudoku numbers

From [[hw01-ex06-sudoku]] ([[hw01-report]], Ex. 6). Each improvement is applied **alone** to naive backtracking. Times are from the report.

| Version | Board 1 assignments | Board 1 time | Board 2 assignments | Board 2 time |
|---|---|---|---|---|
| Naive backtracking | 4,208 | 0.024 s | 335,637 | 2.09 s |
| MRV | **51** (0 backtracks) | 0.008 s | **4,036** | 1.01 s |
| LCV | 2,084 | 0.029 s | 341,523 | 5.07 s |
| Forward checking | 516 | 0.025 s | 153,330 | 7.73 s |

Combinations re-run on 2026-10-01 with the unchanged code (not in the report; counts are deterministic):

| Version | Board 1 | Board 2 |
|---|---|---|
| MRV + FC | 51 | 4,036 (identical to MRV) |
| MRV + LCV | 51 | **181** |
| MRV + LCV + FC | 51 | 181 |

Not implemented in HW01: degree heuristic, AC-3/MAC, backjumping, min-conflicts.

**Reading the numbers**
- **MRV dominates**: ≈ 83× fewer assignments than naive on board 2 but only ≈ 2× faster, because each step rescans all empty cells.
- **LCV alone** barely helps (board 1) or hurts (board 2): value ordering cannot fix a bad variable order. Paired with MRV it is the best (181) — R&N's recommended combination.
- **FC alone** halves the nodes on board 2 but is the slowest, because it recomputes neighbour domains instead of maintaining them.
- **MRV + FC = MRV** here: with domains recomputed from the board, MRV's next scan already finds any empty domain that FC would have found.

## N-Queens

- [[hw01-ex03-n-queens]]: naive backtracking, columns left to right — 113 placements for N = 8, first solution [0, 4, 7, 5, 2, 6, 1, 3].
- Min-conflicts: ~50 steps even for a million queens, because solutions are dense ([[russell-norvig-aima]] §5.4).
- Prolog `queens.pl`: permutation representation (rows and columns distinct by construction) + diagonal check, chronological backtracking via `select/3` ([[slides-xx-logic-programming-prolog]], slide 25; [[prolog-lecture-examples]]).

## When to use which

- **Always**: MRV (with degree as tie-break) — cheap insurance, "sometimes orders of magnitude" better ([[russell-norvig-aima]] §5.3.1).
- **Finding one solution**: add LCV; **counting all solutions**: skip LCV (value order is irrelevant).
- **Inference**: FC is the minimum; MAC when constraints are tight (Sudoku); AC-3 as preprocessing — it alone solves easy Sudokus ([[russell-norvig-aima]] §5.2.6). Implement with **maintained** domains, or the per-node cost eats the gain.
- **Huge, loosely constrained problems or online repair** (n-queens with large n, scheduling): min-conflicts / local search.
- **Tree-structured or nearly-tree constraint graphs**: tree-CSP solver $O(nd^2)$, cutset conditioning ([[russell-norvig-aima]] §5.5).

## Related

[[constraint-satisfaction-problems]] · [[csp-backtracking-search]] · [[csp-heuristics]] · [[constraint-propagation]] · [[hw01-ex06-sudoku]] · [[hw01-ex03-n-queens]] · [[search-algorithms-comparison]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Which techniques change *which* variable is chosen, which change *the order of values*, and which *remove values*?
> **Answer.** Variable: MRV, degree. Value order: LCV. Remove values: forward checking, AC-3, MAC (and other consistency methods).

> [!question]- Q2. Rank naive, MRV, LCV and FC on Sudoku board 2 by assignments and by time.
> **Answer.** Assignments: MRV (4,036) < FC (153,330) < naive (335,637) < LCV (341,523). Time: MRV (1.01 s) < naive (2.09 s) < LCV (5.07 s) < FC (7.73 s) ([[hw01-report]], Ex. 6).

> [!question]- Q3. Why might MRV + LCV beat MRV alone by a factor of 22 on board 2?
> **Answer.** MRV picks the tightest cell; on board 2 that cell often still has 2+ candidates. LCV tries first the digit that leaves the most options to the neighbours, so the first guess is more often right and fewer wrong subtrees are entered (181 vs 4,036 assignments; re-run 2026-10-01).

> [!question]- Q4. Is MAC always better than forward checking?
> **Answer.** It always prunes at least as much (strictly more powerful), but costs more per node. On tightly constrained problems it usually pays off; on loose ones FC may be faster ([[russell-norvig-aima]] §5.3.2).

> [!question]- Q5. When would you choose min-conflicts over backtracking?
> **Answer.** When solutions are dense or the problem is huge (million-queens in ~50 steps), or when repairing an existing schedule after a small change. Not when you must prove that no solution exists — min-conflicts is incomplete ([[russell-norvig-aima]] §5.4).
