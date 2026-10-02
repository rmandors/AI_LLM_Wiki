---
type: comparison
summary: A* (f = g + h_SLD) vs Dijkstra / uniform-cost search (f = g) on the Romania map from Arad to Bucharest — both return the optimal 418, A* expands 5 non-goal nodes vs Dijkstra's 12, with full traces.
unit: 3
tags: [a-star, dijkstra, uniform-cost-search, comparison, romania]
sources: ["[[discussion-01-astar-vs-dijkstra]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# A* vs Dijkstra (Romania, Arad → Bucharest)

The class discussion asked which is better on the book's Romania example ([[discussion-01-astar-vs-dijkstra]]). Dijkstra's algorithm is [[uniform-cost-search]] ($f = g$); [[a-star]] adds the straight-line-distance heuristic $h_{SLD}$ ($f = g + h$). Road costs from [[russell-norvig-aima]] Fig. 3.1, $h_{SLD}$ from Fig. 3.16.

## Properties

| | Dijkstra / UCS | A* |
|---|---|---|
| Evaluation function | $g(n)$ | $g(n) + h(n)$ |
| Frontier | priority queue on $g$ | priority queue on $f$ |
| Complete | Yes (costs ≥ ε) | Yes |
| Optimal | Yes | Yes if $h$ admissible/consistent ($h_{SLD}$ is consistent) |
| Contours | circles of equal $g$ around the start | ellipses of equal $f$ stretched toward the goal |
| Needs domain knowledge | No | Yes ($h$) |
| Time / space | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | depends on $h$; ≤ UCS for consistent $h$ |

## Traces (nodes popped, late goal test)

| # | Dijkstra pop ($g$) | A* pop ($f = g + h$) |
|---|---|---|
| 1 | Arad 0 | Arad 0 + 366 = 366 |
| 2 | Zerind 75 | Sibiu 140 + 253 = 393 |
| 3 | Timisoara 118 | Rimnicu Vilcea 220 + 193 = 413 |
| 4 | Sibiu 140 | Fagaras 239 + 176 = 415 |
| 5 | Oradea 146 | Pitesti 317 + 100 = 417 |
| 6 | Rimnicu Vilcea 220 | **Bucharest 418 + 0 = 418** ✓ |
| 7 | Lugoj 229 | |
| 8 | Fagaras 239 | |
| 9 | Mehadia 299 | |
| 10 | Pitesti 317 | |
| 11 | Craiova 366 | |
| 12 | Drobeta 374 | |
| 13 | **Bucharest 418** ✓ | |

Dijkstra trace recomputed for this wiki from Fig. 3.1 (it agrees with the discussion's "13 nodes" and dead ends Zerind, Timisoara, Lugoj, Mehadia, Drobeta). A* trace from Fig. 3.18. Both return **Arad–Sibiu–Rimnicu Vilcea–Pitesti–Bucharest, cost 140 + 80 + 97 + 101 = 418**.

| Count | Dijkstra | A* |
|---|---|---|
| Non-goal expansions | 12 | 5 |
| Total pops incl. goal | 13 | 6 |

> [!warning] Contradiction
> [[discussion-01-astar-vs-dijkstra]] compares "5 expansions" for A* (goal excluded) with "13 nodes" for Dijkstra (goal included), and lists Fagaras (415) before Rimnicu Vilcea (413). Correct like-for-like numbers are **5 vs 12** (or 6 vs 13), and A* pops RV before Fagaras. The conclusion — A* wins — is unchanged.

## When to use which

- **A\***: single start–goal query with a good admissible (ideally consistent) heuristic — same optimality, far fewer expansions; Timisoara (447) and Zerind (449) are never expanded ([[russell-norvig-aima]] §3.5.3).
- **Dijkstra**: no useful heuristic, or you need shortest paths from the start to **all** nodes (run to exhaustion) ([[discussion-01-astar-vs-dijkstra]]). Also the safe choice when a heuristic's admissibility is doubtful.
- With $h \equiv 0$ A* *is* Dijkstra; better heuristics shrink the expanded set monotonically (dominance, [[heuristic-functions]]).

## Practice questions

> [!question]- Q1. Why does Dijkstra expand Zerind and Timisoara but A* never does?
> **Answer.** Their $g$ (75, 118) is small, so UCS pops them early. Their $f$ (449, 447) exceeds $C^* = 418$, and A* never expands nodes with $f > C^*$ ([[russell-norvig-aima]] §3.5.3).

> [!question]- Q2. When Dijkstra pops Fagaras ($g = 239$) it generates Bucharest with $g = 450$. Why doesn't it return then?
> **Answer.** Late goal test: Bucharest is only tested when popped. Before it reaches $g = 450$, Pitesti (317) generates Bucharest at 418, which replaces 450 and is popped at step 13 ([[uniform-cost-search]]).

> [!question]- Q3. Verify that $h_{SLD}$ is consistent on the edge Pitesti → Bucharest.
> **Answer.** $h(\text{Pitesti}) = 100 \le c(\text{Pitesti}, \text{Bucharest}) + h(\text{Bucharest}) = 101 + 0$. ✓

> [!question]- Q4. If $h$ were doubled ($2h_{SLD}$), would A* still return 418 on this map?
> **Answer.** Not guaranteed — $2h$ is inadmissible, this is weighted A* with $W = 2$ (bound $2C^*$). Check: after Sibiu, RV gets $220 + 386 = 606$, Fagaras $239 + 352 = 591$, so Fagaras is expanded first and Bucharest via Fagaras gets $f = 450$; Pitesti would have $317 + 200 = 517 > 450$ → returns the **450** path.

> [!question]- Q5. Name two situations where Dijkstra is preferable to A*.
> **Answer.** No informative heuristic is available; you need shortest paths to all nodes (single-source all-destinations) ([[discussion-01-astar-vs-dijkstra]]).
