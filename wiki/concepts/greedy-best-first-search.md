---
type: concept
summary: Best-first search with f(n) = h(n) — always expands the node that looks closest to the goal; fast with a good heuristic but not optimal and complete only on finite spaces with repeated-state control.
unit: 3
tags: [search, informed-search, greedy, best-first-search, heuristic]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Greedy best-first search

**Greedy best-first search** expands the frontier node with the lowest $h(n)$ — the node that *appears* closest to the goal — so $f(n) = h(n)$. It makes the locally best decision at every step and **ignores the cost already paid** $g(n)$ ([[slides-02-problem-solving]], slide 12; [[russell-norvig-aima]] §3.5.1). The slides call it simply "Best-First Search".

## How it works

Best-first graph search with a priority queue keyed by $h$.

**Romania example** ([[russell-norvig-aima]] §3.5.1, Fig. 3.17) with $h_{SLD}$ (straight-line distance to Bucharest): Arad (366) → expand → Sibiu 253, Timisoara 329, Zerind 374 → expand Sibiu → Fagaras 176, RV 193, Oradea 380, Arad 366 → expand Fagaras → Bucharest 0. Path Arad–Sibiu–Fagaras–Bucharest = $140 + 99 + 211 = 450$, **32 miles longer** than the optimal 418 via RV and Pitesti. It never expanded a node off its solution path — fast, but not optimal.

## Properties

| Property | Value |
|---|---|
| Complete | Graph search: yes on **finite** spaces; no on infinite ones. Tree-like: can loop |
| Cost-optimal | No |
| Time / space | worst case $O(|V|)$ (graph); good $h$ can reduce to $O(bm)$ |
| Frontier | priority queue ordered by $h(n)$ |
| Evaluation function | $f(n) = h(n)$ |

([[russell-norvig-aima]] §3.5.1.) It may be trapped by a misleading heuristic into a suboptimal path or a dead end ([[slides-02-problem-solving]], slide 12). It is the $W \to \infty$ limit of [[weighted-a-star]]. For unit-cost problems it coincides with **speedy search** ([[russell-norvig-aima]] §3.5.4).

## In this course

- Slide 12 ("Best-First Search"): expands the node closest to the goal by $h(n)$; priority queue by $h$; greedy; complete only when repeated states are controlled; not optimal; may be trapped by misleading $h$ ([[slides-02-problem-solving]]). Slide 13 is image-only (probably the Romania greedy trace).
- **HW01 8-puzzle** ([[hw01-ex01-8-puzzle]]): `best_first_search(start, goal, heuristic)` with `heapq` entries `(h, state)`; the heuristic is a *function parameter*, so one function runs all three heuristics. Results ([[hw01-report]]):

| Heuristic | Path | Generated | Expanded |
|---|---|---|---|
| Manhattan | 48 | 339 | 123 |
| Euclidean | 94 | 1,132 | 413 |
| Misplaced tiles | 116 | 3,069 | 1,134 |
| *(BFS, optimal)* | *20* | *149,026* | *55,409* |

  Greedy is ~450× cheaper than BFS with Manhattan but the path is 2.4× too long. See [[heuristics-8-puzzle-comparison]].
- Raymond chose greedy (not A*) on purpose: the exercise asked for best-first with heuristics and greedy "shows the pure effect of each heuristic".
- 80-tile: the report notes that after the first move $h$ *rises* (306 → 307) — a greedy search can be fooled by such plateaus/rises, A* keeps both branches because it counts $g$ ([[hw01-report]]; [[hw01-ex02-80-tile]]).

## Common mistakes

- Expecting the better heuristic to give the *shorter path* with greedy — it typically gives fewer expansions, but path length is not guaranteed (it happened to hold in HW01: 48 < 94 < 116).
- Calling greedy "A* without g" and assuming it inherits A*'s optimality.
- Using tree-like greedy on a reversible problem — it can oscillate between two states (e.g. Iasi ↔ Neamt when going to Fagaras, classic example; general knowledge).

## Related

[[informed-search]] · [[a-star]] · [[weighted-a-star]] · [[heuristic-functions]] · [[hill-climbing]] · [[heuristics-8-puzzle-comparison]] · [[search-algorithms-comparison]]

## Practice questions

> [!question]- Q1. Trace greedy best-first from Arad to Bucharest with $h_{SLD}$ and give the path cost.
> **Answer.** Arad → Sibiu (253) → Fagaras (176) → Bucharest (0). Cost $140 + 99 + 211 = 450$, vs optimal 418 ([[russell-norvig-aima]] §3.5.1).

> [!question]- Q2. Why did greedy Manhattan return a 48-move solution when BFS proves 20 is optimal?
> **Answer.** Greedy ignores $g(n)$: it follows whatever looks closest now, even if the accumulated path grows. To get 20 with a heuristic you need A* ($g + h$).

> [!question]- Q3. Is greedy best-first complete? Distinguish graph and tree-like versions.
> **Answer.** Graph version: complete on finite spaces (never re-expands a state). Tree-like: can loop forever. Neither is complete on infinite spaces ([[russell-norvig-aima]] §3.5.1; [[slides-02-problem-solving]], slide 12).

> [!question]- Q4. In Ex01, how does Python's `heapq` break ties between two nodes with equal $h$?
> **Answer.** Entries are `(h, state)`; with equal $h$ Python compares the state tuples lexicographically — deterministic and always valid because states are tuples of ints.

> [!question]- Q5. Greedy expanded 123 nodes with Manhattan vs 55,409 for BFS. What fraction is that?
> **Answer.** $123 / 55{,}409 \approx 0.22\,\%$ — about 450× fewer expansions, at the price of a non-optimal path.
