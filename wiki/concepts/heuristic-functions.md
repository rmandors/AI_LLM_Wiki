---
type: concept
summary: Heuristic functions h(n) estimate cost-to-goal; this page covers admissibility, consistency, dominance, effective branching factor, and how to invent heuristics (relaxed problems, max of heuristics, pattern databases, landmarks), with 8-puzzle examples.
unit: 3
tags: [search, heuristics, admissible, consistent, dominance, relaxed-problem, pattern-database, manhattan]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Heuristic functions

A **heuristic function** $h(n)$ estimates the cost of the cheapest path from the state at node $n$ to a goal. It encodes problem knowledge that the problem definition itself (ACTIONS, RESULT) does not contain — e.g. straight-line distances on a map ([[russell-norvig-aima]] §3.5, §3.5.1). Requirements on the slides: $h(n) \ge 0$ and $h(\text{goal}) = 0$; it is an estimate, not a guarantee ([[slides-02-problem-solving]], slide 11).

> [!note] Slide gap
> Slide 16 of [[slides-02-problem-solving]] is titled **"Properties of Heuristics"** but its body is image-only — no text was extracted. Slide 15 is entirely image-only. Everything below on properties is filled from [[russell-norvig-aima]] §3.5.2 and §3.6.

## How it works

### Properties (definitions)

- **Admissible**: never overestimates — $h(n) \le h^*(n)$ for all $n$, where $h^*$ is the true optimal cost to the goal. Admissible heuristics are *optimistic*. A* with an admissible $h$ is cost-optimal ([[russell-norvig-aima]] §3.5.2).
- **Consistent (monotone)**: for every node $n$ and successor $n'$ via action $a$,
  $$h(n) \le c(n, a, n') + h(n')$$
  — a triangle inequality (Fig. 3.19). Every consistent heuristic is admissible, not vice versa. With consistency, $f$ never decreases along a path, the first time A* reaches a state it is optimal, and states never need re-opening ("monotonic heuristic" is a synonym; equivalence proved by Pearl, 1984) ([[russell-norvig-aima]] §3.5.2–3.5.3; [[judea-pearl]]).
- **Dominance**: $h_2$ dominates $h_1$ if $h_2(n) \ge h_1(n)$ for every $n$ (both admissible). Then A* with $h_2$ never expands more nodes than with $h_1$ (except tie-breaking luck), because every node surely expanded with $h_2$ ($h(n) < C^* - g(n)$) is surely expanded with $h_1$ too ([[russell-norvig-aima]] §3.6.1). **Prefer the larger admissible heuristic**, as long as it is cheap to compute.
- **Effective branching factor $b^*$**: if A* generates $N$ nodes for a solution at depth $d$, $b^*$ solves
  $$N + 1 = 1 + b^* + (b^*)^2 + \dots + (b^*)^d.$$
  A good heuristic has $b^*$ close to 1. Example: $d = 5$, $N = 52$ → $b^* = 1.92$ ([[russell-norvig-aima]] §3.6.1). Alternative view (Korf & Reid 1998): a heuristic reduces the *effective depth* by a constant $k_h$, cost $O(b^{d-k_h})$.

### The 8-puzzle heuristics

| Heuristic | Definition | Admissible because… | Relaxed problem |
|---|---|---|---|
| $h_1$ misplaced tiles | # tiles not on goal square (blank excluded) | each misplaced tile needs ≥ 1 move | a tile can jump **anywhere** in one move |
| $h_2$ Manhattan | $\sum_\text{tiles} |\Delta r| + |\Delta c|$ | each move moves one tile one step | a tile can move to **any adjacent** square, even occupied |
| Euclidean | $\sum_\text{tiles} \sqrt{\Delta r^2 + \Delta c^2}$ | straight line ≤ Manhattan ≤ real moves | (no clean relaxation; weaker than $h_2$) |

([[russell-norvig-aima]] §3.6, §3.6.2; Euclidean from [[hw01-report]].) Per tile, misplaced ⇒ distance ≥ 1, so **Manhattan ≥ Euclidean ≥ misplaced** for every state. Book example (Fig. 3.25, optimum 26): $h_1 = 8$, $h_2 = 3+1+2+2+2+3+3+2 = 18$.

### Inventing heuristics

1. **Relaxed problems** — remove constraints from the action rules; the optimal cost of the relaxed problem is an **admissible and consistent** heuristic for the original (relaxed graph is a supergraph; exact costs obey the triangle inequality). From "a tile can move X→Y if X adjacent to Y **and** Y blank": drop "Y blank" → Manhattan; drop both → misplaced tiles. The relaxed problem must be solvable *without search*, ideally decomposing into independent subproblems ([[russell-norvig-aima]] §3.6.2). ABSOLVER generated heuristics automatically this way.
2. **Max of heuristics** — $h(n) = \max\{h_1(n), \dots, h_k(n)\}$ is admissible (consistent if all are) and dominates each component; cost: more computation ([[russell-norvig-aima]] §3.6.2).
3. **Pattern databases** — store the exact cost of solving a *subproblem* (e.g. tiles 1–4 + blank: $9\cdot8\cdot7\cdot6\cdot5 = 15{,}120$ patterns), computed backward from the goal. Combining DBs by max cuts 15-puzzle nodes ~1,000×. **Disjoint** PDBs count only moves of the pattern's own tiles, so they can be **added**: ~10,000× fewer nodes on the 15-puzzle, ~10⁶× on the 24-puzzle ([[russell-norvig-aima]] §3.6.3).
4. **Landmarks** — precompute $C^*(v, L)$ to a few landmark vertices. $h_L(n) = \min_L C^*(n,L) + C^*(L,\text{goal})$ is efficient but **inadmissible**; the **differential heuristic** $h_{DH}(n) = \max_L |C^*(n,L) - C^*(\text{goal},L)|$ is admissible ([[russell-norvig-aima]] §3.6.4).
5. **Learning** heuristics from experience (features + regression) — §3.6.6, not used in this course yet.

## Properties

- Admissible ⇐ consistent ⇐ derived from an exact relaxed problem.
- Trade-off: accuracy (fewer nodes) vs computation time per node.
- Inadmissible heuristics (weighted, landmarks) can be fine for satisficing search: A* with an inadmissible $h$ is still optimal if $h$ is admissible along one optimal path, or overestimates by less than $C_2 - C^*$ ([[russell-norvig-aima]] §3.5.2).

## In this course

- Slide 11 defines $h$ and its two basic properties; slide 16 "Properties of Heuristics" has no extracted body ([[slides-02-problem-solving]]).
- **HW01 Exercise 1** ([[hw01-ex01-8-puzzle]]): implements misplaced tiles (Raymond's "free" heuristic), Manhattan and Euclidean; start values $h_1 = 6$, Euclidean $= 11.30$, $h_2 = 14$, all below the true 20 as admissibility requires. Greedy expansions: 123 (Manhattan) < 413 (Euclidean) < 1,134 (misplaced) — the same order as dominance predicts ([[heuristics-8-puzzle-comparison]]).
- **HW01 Exercise 2** ([[hw01-ex02-80-tile]]): only Manhattan, because max(Manhattan, misplaced) = Manhattan. Start $h = 306$ — a **lower bound** on any solution. Computed **incrementally**: one move changes one tile, so `next_h = h - cost[tile][new_blank] + cost[tile][blank]` is $O(1)$. Suggested stronger heuristics: **linear conflict**, (disjoint) **pattern databases**, problem decomposition.
- Manhattan is consistent: one move changes it by exactly ±1 = the action cost.
- $h_{SLD}$ on Romania is consistent ([[russell-norvig-aima]] §3.5.2); used in [[astar-vs-dijkstra]].

## Common mistakes

- Counting the **blank** in misplaced tiles or Manhattan — that can overestimate (one move would "fix" two things) and breaks admissibility.
- Thinking a *bigger* heuristic is always better: only if it stays admissible (for optimality) and is cheap.
- Assuming admissible ⇒ consistent. Counterexample: $h(A) = 4$, $h(B) = 1$, $c(A,B) = 1$, $h^*(A) = 5$: admissible at A, but $4 > 1 + 1$.
- Adding two non-disjoint pattern databases — not admissible.
- Effective branching factor uses nodes **generated**, not expanded, in the book's tables.

## Related

[[informed-search]] · [[a-star]] · [[greedy-best-first-search]] · [[weighted-a-star]] · [[heuristics-8-puzzle-comparison]] · [[hw01-ex01-8-puzzle]] · [[hw01-ex02-80-tile]] · [[unit-03-search-review]]

## Practice questions

> [!question]- Q1. Compute $h_1$ (misplaced) and $h_2$ (Manhattan) for the start `7 2 4 / 5 _ 6 / 8 3 1` with goal `1 2 3 / 4 5 6 / 7 8 _`.
> **Answer.** Misplaced: 7, 4, 5, 8, 3, 1 → $h_1 = 6$ (2 and 6 are in place). Manhattan: 7→2, 2→0, 4→3, 5→1, 6→0, 8→1, 3→3, 1→4 → $h_2 = 14$. Both ≤ 20 (BFS optimum) ([[hw01-ex01-8-puzzle]]).

> [!question]- Q2. Show that consistency implies admissibility.
> **Answer.** Induct on the number of steps to the goal along an optimal path $n = n_0, n_1, \dots, n_k = G$: $h(n_k) = 0 = h^*(n_k)$; if $h(n_{i+1}) \le h^*(n_{i+1})$ then $h(n_i) \le c(n_i, n_{i+1}) + h(n_{i+1}) \le c(n_i, n_{i+1}) + h^*(n_{i+1}) = h^*(n_i)$.

> [!question]- Q3. A* finds a depth-4 solution generating 40 nodes. Is $b^* = 2$ a good estimate?
> **Answer.** $1 + 2 + 4 + 8 + 16 = 31 \ne 41$. Try $b^* = 2.2$: $1 + 2.2 + 4.84 + 10.65 + 23.43 \approx 42.1$. So $b^* \approx 2.18$ — slightly above 2.

> [!question]- Q4. From which relaxation of the 8-puzzle rule do misplaced tiles and Manhattan come?
> **Answer.** Rule: "a tile can move from X to Y if X is adjacent to Y and Y is blank". Remove both conditions → misplaced tiles; remove "Y is blank" → Manhattan ([[russell-norvig-aima]] §3.6.2).

> [!question]- Q5. Why didn't Raymond combine misplaced tiles and Manhattan with max on the 80-tile puzzle?
> **Answer.** Manhattan ≥ misplaced on every state, so $\max(h_\text{Man}, h_\text{mis}) = h_\text{Man}$; the combination adds computation with no gain.

> [!question]- Q6. Is $h(n) = 2 \times$ Manhattan admissible for the 8-puzzle? What happens if A* uses it?
> **Answer.** No — e.g. one move from the goal it gives 2 > 1. A* with it is weighted A* with $W = 2$: faster, cost ≤ $2C^*$, but no optimality guarantee ([[weighted-a-star]]).
