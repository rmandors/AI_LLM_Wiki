---
type: concept
summary: A* is best-first search on f(n) = g(n) + h(n); complete, cost-optimal with an admissible (tree) or consistent (graph) heuristic, optimally efficient, but its memory grows exponentially.
unit: 3
tags: [search, informed-search, a-star, admissible, consistent, optimal]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[discussion-01-astar-vs-dijkstra]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# A* search

**A\*** ("A-star") always expands the frontier node with the lowest
$$f(n) = g(n) + h(n),$$
where $g(n)$ is the actual cost from the start to $n$ and $h(n)$ the heuristic estimate from $n$ to the goal. So $f(n)$ estimates the cost of the **best complete path through $n$**. Intuition: it looks not only at what *seems* close (greedy's $h$) but at the best estimated *total* cost ([[slides-02-problem-solving]], slide 14; [[russell-norvig-aima]] §3.5.2).

## How it works

Best-first graph search ([[state-space-and-graph-search]]) with a priority queue on $f$, **late goal test** (goal detected when popped, not when generated), and re-insertion of a state reached by a cheaper $g$.

**Romania trace** (Fig. 3.18; $h_{SLD}$ from Fig. 3.16), nodes popped in order:

| Step | Pop | $f = g + h$ | New frontier entries |
|---|---|---|---|
| 1 | Arad | 0 + 366 = 366 | Sibiu 393, Timisoara 447, Zerind 449 |
| 2 | Sibiu | 140 + 253 = 393 | RV 413, Fagaras 415, Arad 646, Oradea 671 |
| 3 | Rimnicu Vilcea | 220 + 193 = 413 | Pitesti 417, Craiova 526, Sibiu 553 |
| 4 | Fagaras | 239 + 176 = 415 | **Bucharest 450**, Sibiu 591 |
| 5 | Pitesti | 317 + 100 = 417 | **Bucharest 418**, Craiova 615, RV 607 |
| 6 | Bucharest | 418 + 0 = 418 | goal → return |

Bucharest appears at step 4 with $f = 450$ but is not selected, because Pitesti (417) might lead to something cheaper. Timisoara (447) and Zerind (449) are **never expanded** — that is A*'s pruning ([[russell-norvig-aima]] §3.5.2–3.5.3).

**Optimality proof sketch (admissible $h$)**: suppose A* returns cost $C > C^*$. Some node $n$ on an optimal path is unexpanded, so $f(n) > C^*$. But $f(n) = g^*(n) + h(n) \le g^*(n) + h^*(n) = C^*$. Contradiction ([[russell-norvig-aima]] §3.5.2).

**Contours**: with a consistent $h$, $f$ never decreases along a path, so A* expands in concentric bands of increasing $f$ — stretched toward the goal, unlike UCS's circular $g$-bands (Fig. 3.20). A* expands **all** nodes with $f < C^*$ ("surely expanded"), possibly some with $f = C^*$, and **none** with $f > C^*$ (§3.5.3).

## Properties

| Property | Value |
|---|---|
| Complete | Yes (positive costs ≥ ε, finite $b$, and finite space or a solution exists) — does *not* need admissibility ([[russell-norvig-aima]] §3.5.2, fn. 11) |
| Cost-optimal | Yes if $h$ **admissible** (tree search, or graph search that re-opens states); **consistent** $h$ guarantees it for graph search without re-opening |
| Optimally efficient | With consistent $h$: no algorithm extending paths from the start with the same $h$ expands fewer nodes (up to ties at $f = C^*$) |
| Time | depends on $h$; worst case exponential in solution length |
| Space | $O(b^d)$ — keeps every reached node in memory (the real bottleneck) |
| Frontier | priority queue (min-heap) on $f(n)$ |

Special cases: $h \equiv 0$ → [[uniform-cost-search]]; $h = h^*$ → straight down the optimal path. Memory-bounded variants: **IDA\*** (iterative deepening on $f$), **RBFS** (linear space, backed-up values), **SMA\*** (drop worst leaf when memory is full) ([[russell-norvig-aima]] §3.5.5).

## In this course

- **Slide 14**: $f = g + h$; priority queue on $f$; "complete: always finds a solution if one exists and $h$ is admissible; optimal if $h$ is admissible/consistent; space $O(b^d)$, stores every node; time depends on the quality of $h$" ([[slides-02-problem-solving]]). Slides 13 and 15 are image-only (probably the Romania trace).
- **Discussion 01** ([[discussion-01-astar-vs-dijkstra]]): A* reaches Bucharest (418) after 5 expansions vs Dijkstra's 13 node pops — see [[astar-vs-dijkstra]] for the corrected expansion order and counts.
- **HW01, 80-tile** ([[hw01-ex02-80-tile]]): `a_star = weighted_a_star(weight = 1)` with Manhattan distance. It **did not finish** within 250,000 expansions (887,441 generated, ~2.4 s); start $h = 306$, best $h$ reached 287. Reason: A* must expand every node with $f < C^*$, and the gap between 306 and $C^*$ (somewhere in [306, 740]) is hundreds of moves. Raymond switched to [[weighted-a-star]] and [[beam-search]].
- **HW01, 8-puzzle**: A* was not run; A*(Manhattan) would give the optimal 20 with far fewer nodes than BFS (book Fig. 3.26: ~1,318 vs ~91,493 generated at $d = 20$) ([[heuristics-8-puzzle-comparison]]).

> [!warning] Contradiction
> Slide 14 says A* is complete "if $h$ is admissible". The textbook says A* is complete regardless of admissibility (given positive costs and a finite space or an existing solution); admissibility/consistency matter for **optimality**, not completeness ([[russell-norvig-aima]] §3.5.2). Use the book's statement in exams, but know the slide's wording.

## Common mistakes

- Stopping when the goal is **generated** (early test) — can return 450 instead of 418 on Romania.
- Using an admissible-but-inconsistent $h$ in a graph search that **never re-opens** closed states → may lose optimality.
- Not skipping **stale heap entries** (a state pushed twice with different $g$): correct but wastes expansions — Raymond's 80-tile code has exactly this issue ([[hw01-ex02-80-tile]]).
- Believing "A* is always fast": with a weak heuristic on a big space it is exponential in time *and* memory.
- Tie-breaking: among equal $f$, preferring larger $g$ (deeper) usually reaches the goal sooner (general knowledge).

## Related

[[heuristic-functions]] · [[greedy-best-first-search]] · [[uniform-cost-search]] · [[weighted-a-star]] · [[beam-search]] · [[iterative-deepening-search]] · [[astar-vs-dijkstra]] · [[search-algorithms-comparison]] · [[judea-pearl]]

## Practice questions

> [!question]- Q1. After expanding Arad and Sibiu, the frontier holds RV (g = 220, h = 193), Fagaras (239, 176), Timisoara (118, 329), Zerind (75, 374), Oradea (291, 380). Which node does A* expand next?
> **Answer.** Compute $f$: RV 413, Fagaras 415, Timisoara 447, Zerind 449, Oradea 671. A* expands **Rimnicu Vilcea** (413).

> [!question]- Q2. Bucharest is on the frontier with $f = 450$ while Pitesti has $f = 417$. Why doesn't A* stop?
> **Answer.** Goal test is done on pop. Pitesti's $f = 417 < 450$ means a path through Pitesti could cost as little as 417, so A* expands Pitesti first, finds Bucharest at 418 and returns that ([[russell-norvig-aima]] §3.5.2).

> [!question]- Q3. Prove (sketch) that A* with an admissible heuristic is cost-optimal.
> **Answer.** If it returned $C > C^*$, an unexpanded node $n$ on the optimal path would have $f(n) > C^*$ (else it would have been expanded first); but admissibility gives $f(n) = g^*(n) + h(n) \le g^*(n) + h^*(n) = C^*$. Contradiction ([[russell-norvig-aima]] §3.5.2).

> [!question]- Q4. Why did A* with Manhattan distance not finish on Raymond's 80-tile puzzle?
> **Answer.** A* must expand every node with $f < C^*$. Start $h = 306$ and $C^*$ is somewhere in [306, 740]; the set of nodes with $f$ below $C^*$ is astronomically large, and memory (every 81-tuple + parent pointer) grows fast. It stopped at the 250,000-expansion cap with best $h = 287$ ([[hw01-ex02-80-tile]]).

> [!question]- Q5. What is the difference between A*'s completeness condition and its optimality condition?
> **Answer.** Completeness needs positive action costs ≥ ε and a finite branching factor (finite space or a solution). Optimality additionally needs an admissible $h$ (consistent for graph search without re-opening) ([[russell-norvig-aima]] §3.5.2).

> [!question]- Q6. Which nodes does A* surely expand, and which does it never expand?
> **Answer.** Surely expands all nodes reachable on paths with $f(n) < C^*$; may expand some with $f = C^*$; never expands nodes with $f > C^*$ ([[russell-norvig-aima]] §3.5.3).
