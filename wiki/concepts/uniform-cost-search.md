---
type: concept
summary: Uniform-cost search (Dijkstra's algorithm) expands the frontier node with the lowest path cost g(n); complete and cost-optimal with positive costs, O(b^(1+floor(C*/epsilon))) time and space.
unit: 3
tags: [search, uninformed-search, ucs, dijkstra, priority-queue, late-goal-test]
sources: ["[[russell-norvig-aima]]", "[[discussion-01-astar-vs-dijkstra]]"]
updated: 2026-10-01
---

# Uniform-cost search (Dijkstra's algorithm)

**Uniform-cost search (UCS)** is best-first search with evaluation function $f(n) = g(n)$, the cost of the path from the start to $n$. It is called **Dijkstra's algorithm** in theoretical CS and UCS in AI ([[russell-norvig-aima]] §3.4.2). Where BFS spreads in waves of equal *depth*, UCS spreads in waves of equal *path cost*. It is the right uninformed algorithm when actions have different costs.

## How it works

`UNIFORM-COST-SEARCH(problem) = BEST-FIRST-SEARCH(problem, PATH-COST)` (Fig. 3.9). Priority queue ordered by $g$; reached table keeps the best $g$ per state; **late goal test** (test when popped).

**Worked example** (Fig. 3.10, Sibiu → Bucharest): expand Sibiu → RV (80), Fagaras (99). Pop RV → Pitesti (177). Pop Fagaras → Bucharest (310) — *generated but not tested*. Pop Pitesti → Bucharest again at 278 < 310, replaces it. Pop Bucharest (278) → goal. An **early** goal test would have returned the 310 path ([[russell-norvig-aima]] §3.4.2).

## Properties

| Property | Value |
|---|---|
| Complete | Yes, if every action cost $\ge \epsilon > 0$ (and $b$ finite) |
| Cost-optimal | Yes — first goal popped is cheapest (with late goal test) |
| Time / space | $O(b^{1+\lfloor C^*/\epsilon \rfloor})$; equals $O(b^{d+1})$ when all costs equal |
| Frontier | priority queue (binary heap) on $g(n)$ |
| Evaluation function | $f(n) = g(n)$ |

$C^*$ = optimal solution cost, $\epsilon$ = minimum action cost. UCS can explore big trees of cheap actions before a single expensive but useful one, which is why the bound can exceed $b^d$ ([[russell-norvig-aima]] §3.4.2).

UCS is the special case $W = 0$ of [[weighted-a-star]], and [[a-star]] with $h \equiv 0$ ([[russell-norvig-aima]] §3.5.4).

## In this course

- **Not on the slides** of [[slides-02-problem-solving]]; it appears in the class discussion as "Dijkstra" ([[discussion-01-astar-vs-dijkstra]]).
- Discussion 01 (Romania, Arad → Bucharest): Dijkstra also finds the optimal 418 route but pops **13 nodes** (including the goal), fanning out to Zerind, Timisoara, Lugoj, Mehadia and Drobeta, which lie away from Bucharest. A* with $h_{SLD}$ needs 5 expansions before the goal. Full trace and the counting caveat in [[astar-vs-dijkstra]].
- Raymond did not implement UCS in HW01: all his path problems have unit costs, where UCS degenerates to BFS.

## Common mistakes

- Using the **early** goal test → can return a suboptimal path (the 310 vs 278 example).
- Forgetting the "better path" update: a state already in `reached` must be re-added if found with lower $g$.
- Zero-cost cycles or arbitrarily small costs break completeness (need $\epsilon > 0$).
- Thinking Dijkstra must compute all shortest paths: as UCS it stops when the goal is popped.

## Related

[[breadth-first-search]] · [[a-star]] · [[weighted-a-star]] · [[uninformed-search]] · [[astar-vs-dijkstra]] · [[search-algorithms-comparison]]

## Practice questions

> [!question]- Q1. Run UCS from Arad on the Romania map and list the first six nodes popped with their $g$.
> **Answer.** Arad 0, Zerind 75, Timisoara 118, Sibiu 140, Oradea 146 (via Zerind), Rimnicu Vilcea 220. Then Lugoj 229, Fagaras 239, Mehadia 299, Pitesti 317, Craiova 366, Drobeta 374, Bucharest 418 (road costs from [[russell-norvig-aima]] Fig. 3.1).

> [!question]- Q2. Why must UCS use a late goal test? Give the book's counterexample.
> **Answer.** A goal generated early may not be cheapest. Sibiu → Bucharest: via Fagaras (310) is generated before via Pitesti (278). Testing on generation returns 310; testing on pop returns 278 ([[russell-norvig-aima]] §3.4.2).

> [!question]- Q3. With $C^* = 10$ and $\epsilon = 2$, what is the UCS bound?
> **Answer.** $O(b^{1 + \lfloor 10/2 \rfloor}) = O(b^6)$.

> [!question]- Q4. When are UCS and BFS equivalent?
> **Answer.** When all action costs are equal: they expand in the same order (UCS may generate one extra level because of the late goal test, $b^{d+1}$) ([[russell-norvig-aima]] §3.4.2).

> [!question]- Q5. How is UCS related to A*?
> **Answer.** UCS is A* with $h(n) = 0$ for all $n$ (a trivially admissible, consistent heuristic), or weighted A* with $W = 0$ ([[russell-norvig-aima]] §3.5.4).
