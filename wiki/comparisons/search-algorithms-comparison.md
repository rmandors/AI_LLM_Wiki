---
type: comparison
summary: Side-by-side table of every search algorithm in unit 3 — BFS, UCS, DFS, DLS, IDS, bidirectional, greedy, A*, weighted A*, beam, IDA* — by completeness, optimality, time, space, frontier and evaluation function, with HW01 usage.
unit: 3
tags: [search, comparison, complexity, uninformed-search, informed-search]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Search algorithms compared

All of these are the same best-first/graph-search loop ([[state-space-and-graph-search]]) with a different frontier or evaluation function. Notation: $b$ branching factor, $d$ depth of shallowest solution, $m$ max depth, $\ell$ depth limit, $C^*$ optimal cost, $\epsilon$ min action cost, $k$ beam width ([[russell-norvig-aima]] §3.3.4).

## Uninformed

| Algorithm | Frontier | $f(n)$ / order | Complete? | Optimal? | Time | Space |
|---|---|---|---|---|---|---|
| [[breadth-first-search]] | FIFO queue | shallowest first | Yes¹ | Yes if equal costs | $O(b^d)$ | $O(b^d)$ |
| [[uniform-cost-search]] | priority queue | $g(n)$ | Yes¹˒² | Yes | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | same |
| [[depth-first-search]] (tree-like) | LIFO stack | deepest first | No (yes on finite graphs with graph search) | No | $O(b^m)$ | $O(bm)$ |
| Depth-limited | LIFO, cut at $\ell$ | deepest ≤ $\ell$ | No | No | $O(b^\ell)$ | $O(b\ell)$ |
| [[iterative-deepening-search]] | LIFO, $\ell = 0,1,\dots$ | deepest ≤ $\ell$ | Yes¹ | Yes if equal costs | $O(b^d)$ | $O(bd)$ |
| Bidirectional (BFS/UCS) | two queues | both ends | Yes¹˒⁴ | Yes³˒⁴ | $O(b^{d/2})$ | $O(b^{d/2})$ |

¹ $b$ finite and a solution exists or the space is finite; ² costs ≥ ε > 0; ³ equal costs; ⁴ both directions BFS/UCS. Tree-like versions; with graph search, bounds are capped at $|V|+|E|$ ([[russell-norvig-aima]] §3.4.6, Fig. 3.15).

## Informed

| Algorithm | Frontier | $f(n)$ | Complete? | Optimal? | Time | Space |
|---|---|---|---|---|---|---|
| [[greedy-best-first-search]] | priority queue | $h$ | Finite spaces (graph search) | No | $O(|V|)$ worst; ~$O(bm)$ with good $h$ | $O(|V|)$ |
| [[a-star]] | priority queue | $g + h$ | Yes | Yes if $h$ admissible (consistent for graph search w/o re-open) | exponential worst; depends on $h$ | $O(b^d)$ — all nodes |
| [[weighted-a-star]] | priority queue | $g + W h$, $W>1$ | Yes | No; cost ≤ $W\cdot C^*$ | usually ≪ A* | ≪ A* |
| [[beam-search]] | best $k$ per level | $h$ or $f$ | No | No | $O(kbd)$ | $O(kb)$ |
| IDA* | LIFO, $f$-limit | $g + h$ | Yes | Yes (admissible) | ≥ A* (re-expansions) | $O(bd)$ |
| RBFS / SMA* | recursion / bounded memory | $g + h$ | Yes (SMA*: if $d$ fits in memory) | Yes (admissible; SMA*: if reachable) | hard to characterize | linear / all available |

([[russell-norvig-aima]] §3.5.1–3.5.5; [[slides-02-problem-solving]], slides 7, 9, 12, 14.)

## HW01 usage

| Problem | Algorithm(s) | Result | Page |
|---|---|---|---|
| 8-puzzle | BFS / DFS / greedy ×3 | 20 / 66,056 / 48–116 moves | [[hw01-ex01-8-puzzle]] |
| 80-tile | A* / weighted A* / beam ×2 | cap / 1,116 / 1,078, 740 | [[hw01-ex02-80-tile]] |
| Farmer | BFS | 7 | [[hw01-ex04-farmer-wolf-goat-cabbage]] |
| Missionaries & cannibals | BFS | 11 | [[hw01-ex05-missionaries-cannibals]] |
| N-Queens, Sudoku | backtracking (DFS on assignments) | — | [[hw01-ex03-n-queens]], [[hw01-ex06-sudoku]] |

## When to use which

- **Small space, unit costs, need the optimum** → BFS (what Raymond did for three problems). Huge space, unknown depth, unit costs → **IDS**.
- **Varying action costs, no heuristic** → UCS / Dijkstra (also for shortest paths to all nodes) ([[astar-vs-dijkstra]]).
- **Good admissible heuristic, need the optimum, memory OK** → A*. Memory tight → IDA* / RBFS / SMA*.
- **Need *a* solution fast, quality bounded** → weighted A* (bound $W\cdot C^*$).
- **Very large spaces, memory-bounded, any decent answer** → beam search (or greedy).
- **Need low memory, any solution, deep finite space** → DFS / backtracking (CSPs: [[csp-backtracking-search]]).
- **Two opponents** → none of these: [[minimax]] / [[alpha-beta-pruning]] / [[monte-carlo-tree-search]] ([[game-search-comparison]]).

## Practice questions

> [!question]- Q1. Which algorithms in the tables are optimal for arbitrary positive costs?
> **Answer.** UCS, A* (admissible/consistent $h$), IDA*, RBFS, SMA* (if reachable), bidirectional UCS. BFS and IDS only for equal costs.

> [!question]- Q2. Rank BFS, DFS and IDS by memory for $b = 10$, $d = 8$, $m = 20$ (node counts).
> **Answer.** DFS ≈ $bm = 200$; IDS ≈ $bd = 80$; BFS ≈ $b^d = 10^8$. IDS < DFS ≪ BFS here (DFS uses $m$, IDS uses $d$).

> [!question]- Q3. What frontier data structure does each of BFS, DFS, UCS, A* use?
> **Answer.** FIFO queue, LIFO stack, priority queue on $g$, priority queue on $g + h$ ([[russell-norvig-aima]] §3.3.2).

> [!question]- Q4. Give one algorithm that is complete but not optimal, and one that is neither.
> **Answer.** Complete, not optimal: weighted A* (or graph-search greedy on finite spaces, graph DFS on finite spaces). Neither: beam search (or tree-like DFS).

> [!question]- Q5. Why does UCS's bound $b^{1+\lfloor C^*/\epsilon\rfloor}$ become $b^{d+1}$ with unit costs?
> **Answer.** With $\epsilon = 1$ and $C^* = d$, the exponent is $1 + d$ ([[russell-norvig-aima]] §3.4.2).

> [!question]- Q6. The 80-tile A* did not finish but beam search did. Which property of beam search made the difference, and what did it cost?
> **Answer.** Bounded frontier ($k$ nodes per level) — memory and work stay linear in depth. Cost: completeness and optimality are lost (740 is not proven optimal) ([[hw01-ex02-80-tile]]).
