---
type: concept
summary: Weighted A* uses f(n) = g(n) + W·h(n) with W > 1 to trade optimality for speed; it is a bounded-suboptimal search returning a cost between C* and W·C*.
unit: 3
tags: [search, informed-search, weighted-a-star, satisficing, bounded-suboptimal]
sources: ["[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Weighted A* search

**Weighted A\*** is A* with the heuristic multiplied by a weight $W > 1$:
$$f(n) = g(n) + W \times h(n).$$
Inflating $h$ makes the search more goal-directed ("somewhat-greedy search"): it explores far fewer states but may miss the optimal path. It is the standard example of **satisficing** search — accepting a "good enough" solution ([[russell-norvig-aima]] §3.5.4).

## How it works

Identical to [[a-star]], only the priority changes. A weighted heuristic $W h$ is generally **inadmissible** even when $h$ is admissible. The intuition is the road engineers' **detour index** (1.2–1.6): multiply straight-line distance by ~1.3 to estimate road distance.

**One formula for the whole family** ([[russell-norvig-aima]] §3.5.4):

| $W$ | Algorithm |
|---|---|
| 0 | [[uniform-cost-search]] ($g$) |
| 1 | [[a-star]] ($g + h$) |
| $1 < W < \infty$ | weighted A* |
| $\infty$ | [[greedy-best-first-search]] ($h$) |

## Properties

| Property | Value |
|---|---|
| Complete | Yes (same conditions as A*) |
| Cost-optimal | No — **bounded suboptimal**: cost $\in [C^*, W \cdot C^*]$ (for admissible $h$) |
| Time / space | usually far fewer nodes than A*; still exponential worst case |
| Frontier | priority queue on $g + W h$ |

In practice solutions are "much closer to $C^*$ than $W \cdot C^*$". Fig. 3.21: with $W = 2$ on a grid, weighted A* explored **7× fewer states** for a path **5 % costlier** ([[russell-norvig-aima]] §3.5.4). Related notions: *bounded-cost* search (cost < some constant $C$) and *unbounded-cost* search such as speedy search.

## In this course

- **Not on the slides** — Raymond took it from [[russell-norvig-aima]] §3.5.4 for the 80-tile puzzle.
- [[hw01-ex02-80-tile]]: `weighted_a_star(start, cost, neigh, weight=10, max_expansions=1_000_000, time_limit=60)`; plain A* is the same function with `weight = 1` (`Exercise02.py` l.347–348). Result: path **1,116** moves, 1,159,075 generated, 314,397 expanded, ~3.7–3.8 s ([[hw01-report]]).
- Guarantee with $W = 10$: $\le 10\,C^*$; measured: $1116 / 306 \approx 3.65$ times the Manhattan lower bound at most.
- **W = 10 was chosen by trial**, not from the book; "other weights were less stable in small tests" has no trace in the code — the honest answer is "tuned by hand".
- Known code issue: stale heap entries are not skipped after a cheaper $g$ is found, so the expansion count is slightly inflated; fix `if g_value > visited[current]: continue`.

## Common mistakes

- Claiming weighted A* is optimal "because it is A*" — it is not, unless $W = 1$.
- Misreading the bound: the guarantee is relative to $C^*$, not to the heuristic value of the start; with $h(s_0) = 306$ we can only bound the *ratio to the lower bound*.
- Thinking larger $W$ is always faster: very large $W$ behaves like greedy and can wander on plateaus (general knowledge).

## Related

[[a-star]] · [[greedy-best-first-search]] · [[uniform-cost-search]] · [[beam-search]] · [[heuristic-functions]] · [[informed-search]] · [[hw01-ex02-80-tile]]

## Practice questions

> [!question]- Q1. A node has $g = 20$, $h = 30$. Compute its priority for $W = 1, 2, 10$.
> **Answer.** $W = 1$: 50. $W = 2$: 80. $W = 10$: 320. Larger $W$ makes $h$ dominate the ordering.

> [!question]- Q2. Raymond's weighted A* ($W = 10$) found 1,116 moves. What can he claim about optimality?
> **Answer.** Theoretical bound: $\le 10\,C^*$. Empirically, since $C^* \ge 306$ (Manhattan of the start), the path is at most $1116/306 \approx 3.65$× optimal. He cannot claim more.

> [!question]- Q3. Why might the professor ask "why 10 and not 2"? What is the honest answer?
> **Answer.** Because the book's example uses $W = 2$. Honest answer: 10 was an empirical choice that finished in ~4 s; smaller $W$ is closer to A* and needs more expansions; the guarantee with 10 is weak but practical results are much closer to $C^*$.

> [!question]- Q4. Which values of $W$ give UCS, A* and greedy?
> **Answer.** $W = 0$ → UCS, $W = 1$ → A*, $W \to \infty$ → greedy ([[russell-norvig-aima]] §3.5.4).
