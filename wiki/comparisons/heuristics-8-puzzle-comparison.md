---
type: comparison
summary: Misplaced tiles vs Euclidean vs Manhattan on the 8-puzzle — definitions, admissibility, dominance chain Manhattan ≥ Euclidean ≥ misplaced, and HW01 greedy results (123 < 413 < 1,134 expanded) alongside the textbook's A* data.
unit: 3
tags: [heuristics, 8-puzzle, comparison, manhattan, misplaced-tiles, dominance]
sources: ["[[hw01-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# 8-puzzle heuristics compared

HW01 Exercise 1 ran greedy best-first search with three admissible heuristics on the same instance (start `7 2 4 / 5 _ 6 / 8 3 1`, goal `1 2 3 / 4 5 6 / 7 8 _`, optimum 20) ([[hw01-ex01-8-puzzle]]). This page puts the theory ([[heuristic-functions]]) next to the measurements.

## Definitions and properties

| | Misplaced tiles $h_1$ | Euclidean | Manhattan $h_2$ |
|---|---|---|---|
| Per tile | 1 if not on goal square | $\sqrt{\Delta r^2 + \Delta c^2}$ | $|\Delta r| + |\Delta c|$ |
| Blank counted? | No | No | No |
| Admissible? | Yes | Yes | Yes |
| Consistent? | Yes | Yes (general knowledge: per-tile change ≤ 1 per move) | Yes (changes by exactly ±1 per move) |
| Relaxed problem | tile may jump anywhere | — | tile may move to any adjacent square |
| Start value | **6** | **11.30** | **14** |
| Dominance | weakest | between | strongest |

Chain for every state: **Manhattan ≥ Euclidean ≥ misplaced** — per tile, $|dr|+|dc| \ge \sqrt{dr^2+dc^2} \ge 1$ if misplaced, 0 otherwise ([[russell-norvig-aima]] §3.6.1–3.6.2).

## HW01 results (greedy best-first, $f = h$)

| Heuristic | Path | Generated | Expanded |
|---|---|---|---|
| Manhattan | 48 | 339 | **123** |
| Euclidean | 94 | 1,132 | 413 |
| Misplaced | 116 | 3,069 | 1,134 |
| *BFS (no heuristic)* | *20* | *149,026* | *55,409* |

Expansions follow the dominance order: **123 < 413 < 1,134** ([[hw01-report]]; re-run 2026-10-01). Paths also follow it here (48 < 94 < 116), but for greedy this is *not* guaranteed — greedy is not optimal, and dominance theorems are about A*.

## Textbook comparison (A*, averaged over 100 random instances per depth)

| $d$ | BFS generated | A*($h_1$) | A*($h_2$) | $b^*$ BFS | $b^*$ $h_1$ | $b^*$ $h_2$ |
|---|---|---|---|---|---|---|
| 6 | 128 | 24 | 19 | 2.01 | 1.42 | 1.34 |
| 12 | 2,672 | 279 | 84 | 1.80 | 1.45 | 1.28 |
| 20 | 91,493 | 9,905 | 1,318 | 1.69 | 1.50 | 1.34 |
| 28 | 463,234 | 202,565 | 22,055 | 1.53 | 1.49 | 1.36 |

([[russell-norvig-aima]] §3.6.1, Fig. 3.26, selected rows.) Raymond's single BFS run at $d = 20$ generated 149,026 nodes ($b^* \approx 1.74$, computed for this wiki), same order of magnitude as the book's average of 91,493.

## When to use which

- **Manhattan**: default for sliding puzzles — strongest of the three, cheap, consistent. With A* it is optimal and expands far fewer nodes than $h_1$.
- **Misplaced tiles**: only as a teaching baseline or where distance makes no sense; dominated by Manhattan, so $\max(h_1, h_2) = h_2$ adds nothing.
- **Euclidean**: wrong geometry for 4-connected moves (no diagonals) — admissible but systematically weaker than Manhattan.
- **Stronger than Manhattan**: linear conflict, (disjoint) pattern databases — needed for 15/24-puzzles and for Raymond's 80-tile ([[hw01-ex02-80-tile]], [[russell-norvig-aima]] §3.6.3).

## Practice questions

> [!question]- Q1. Compute the Euclidean heuristic of the HW01 start state.
> **Answer.** Displacements: 7 (2,0) → 2; 4 (1,2) → $\sqrt5$; 5 (0,1) → 1; 8 (0,1) → 1; 3 (2,1) → $\sqrt5$; 1 (2,2) → $\sqrt8$; 2 and 6 → 0. Sum $= 4 + 2\sqrt5 + \sqrt8 \approx 4 + 4.472 + 2.828 = 11.30$.

> [!question]- Q2. Why is Euclidean weaker than Manhattan on this puzzle?
> **Answer.** Tiles cannot move diagonally, so the true per-tile distance is at least the Manhattan distance; the straight line underestimates more whenever a tile is displaced in both row and column.

> [!question]- Q3. Dominance guarantees A* with $h_2$ never expands more nodes than with $h_1$. Does it guarantee greedy with $h_2$ finds a shorter path than greedy with $h_1$?
> **Answer.** No. Greedy is not optimal; dominance results rely on A*'s "surely expanded" set ($f < C^*$). HW01 happened to show 48 < 116 but that is empirical.

> [!question]- Q4. From Fig. 3.26 at $d = 20$, how many times fewer nodes does A*($h_2$) generate than BFS? Than A*($h_1$)?
> **Answer.** $91{,}493 / 1{,}318 \approx 69$×; $9{,}905 / 1{,}318 \approx 7.5$× ([[russell-norvig-aima]] Fig. 3.26).

> [!question]- Q5. A one-move-from-goal state: what are $h_1$, $h_2$, Euclidean? Is any of them exact?
> **Answer.** One tile is one square away: $h_1 = 1$, $h_2 = 1$, Euclidean $= 1$. All three are exact ($h^* = 1$).
