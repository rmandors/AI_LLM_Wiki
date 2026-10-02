---
type: source
summary: Raymond's class discussion comparing A* (straight-line-distance heuristic) with Dijkstra's algorithm on the Romania map, Arad to Bucharest — both find cost 418, A* with 5 expansions vs Dijkstra's 13.
unit: 3
tags: [discussion, a-star, dijkstra, uniform-cost-search, romania]
sources: ["[[discussion-01-astar-vs-dijkstra]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Discussion 01 — A* vs Dijkstra

**Bibliographic line.** Portilla, R. *A\* vs Dijkstra – Shortest Path* (class discussion). Artificial Intelligence, USFQ; dated 24/08/2026. File: `raw/Class_exercises/Discussion_01_RP.docx`.

**What it is.** A short answer to the prompt "Take the example in the book and compute Dijkstra's Algorithm vs A\*. Which one is the best, why?", using the Romania map ([[russell-norvig-aima]] Fig. 3.1) and the A* trace of Fig. 3.18 with $h_{SLD}$ (Fig. 3.16).

## Key points

- Notation $f(n) = g(n) + h(n)$; $g$ = real cost from Arad, $h$ = straight-line distance to Bucharest. Dijkstra uses only $g$, "it has no idea where Bucharest is", so it expands uniformly in every direction → [[uniform-cost-search]], [[a-star]].
- A* sequence given: Sibiu ($f=393$) → Fagaras (415) → Rimnicu Vilcea (413) → Pitesti (417) → Bucharest ($f = g = 418$); "only 5 expansions before reaching the goal"; cost 418, optimal.
- Dijkstra also finds 418 "but only after expanding 13 nodes", including dead ends Zerind, Timisoara, Lugoj, Mehadia and "Dobreta" (Drobeta).
- Both are optimal because $h_{SLD}$ is admissible; A* "dominates Dijkstra whenever we have a good admissible heuristic". Dijkstra is preferable when no heuristic is available or when shortest paths to **all** nodes are needed.
- Full comparison table and trace → [[astar-vs-dijkstra]].

## Pages that use this source

[[astar-vs-dijkstra]] · [[a-star]] · [[uniform-cost-search]] · [[uninformed-search]] · [[informed-search]] · [[unit-03-search-review]]

## Issues found

- **Expansion order**: the document lists Fagaras (415) *before* Rimnicu Vilcea (413). A* pops the lowest $f$ first, so the true order is Arad → Sibiu → **RV (413) → Fagaras (415)** → Pitesti → Bucharest ([[russell-norvig-aima]] Fig. 3.18). The listed sequence is an expansion order, not the solution path; the path is Arad–Sibiu–RV–Pitesti–Bucharest.
- **Inconsistent counting**: "5 expansions before reaching the goal" for A* excludes the goal pop (Arad, Sibiu, RV, Fagaras, Pitesti), while "13 nodes" for Dijkstra includes it (12 non-goal pops + Bucharest; recomputed for this wiki from Fig. 3.1). Like-for-like: **5 vs 12** (excluding goal) or **6 vs 13** (including goal). The conclusion is unchanged.
- Spelling: "Dobreta" → **Drobeta** (book).
- NRC on the document is **1653**, whereas the course is NRC 1651 ([[slides-00-instructor-introduction]]) — likely a typo.
- The prompt's "diagram" (the book figure) is not reproduced in the extraction; the empty table at the end is a leftover.
