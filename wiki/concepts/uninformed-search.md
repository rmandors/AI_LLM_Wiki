---
type: concept
summary: Blind search strategies that know only the problem definition (no estimate of distance to goal) and differ only in the order they expand nodes, judged by completeness, optimality, time and space.
unit: 3
tags: [search, uninformed-search, blind-search, bfs, dfs, ucs, ids]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Uninformed search

**Uninformed (blind) search** uses no knowledge beyond the problem definition: the initial state, the available actions and the goal test. It explores the state space **systematically without favouring any path**, so it has no idea whether Zerind or Sibiu is the better first step from Arad ([[slides-02-problem-solving]], slide 6; [[russell-norvig-aima]] §3.4). All uninformed algorithms are the same loop; **they differ only in the order in which they expand nodes**, i.e. in the frontier data structure.

## How it works

| Algorithm | Frontier | Expands first | Page |
|---|---|---|---|
| Breadth-first (BFS) | FIFO queue | shallowest node | [[breadth-first-search]] |
| Uniform-cost / Dijkstra (UCS) | priority queue on $g(n)$ | cheapest path so far | [[uniform-cost-search]] |
| Depth-first (DFS) | LIFO stack | deepest node | [[depth-first-search]] |
| Depth-limited (DLS) | LIFO, cut at depth $\ell$ | deepest node ≤ $\ell$ | [[iterative-deepening-search]] |
| Iterative deepening (IDS) | DLS with $\ell = 0,1,2,\dots$ | deepest node ≤ current $\ell$ | [[iterative-deepening-search]] |
| Bidirectional | two frontiers | from start and goal at once | ([[russell-norvig-aima]] §3.4.5) |

## Properties

**Four evaluation criteria** ([[slides-02-problem-solving]], slide 6; [[russell-norvig-aima]] §3.3.4):
1. **Completeness** — guaranteed to find a solution if one exists (and report failure otherwise)?
2. **Cost optimality** — guaranteed to find the lowest-cost solution?
3. **Time complexity** — how long (nodes generated)?
4. **Space complexity** — how much memory (nodes stored)?

**Fig. 3.15 (tree-like versions)** ([[russell-norvig-aima]] §3.4.6):

| Criterion | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| Complete? | Yes¹ | Yes¹˒² | No | No | Yes¹ | Yes¹˒⁴ |
| Cost-optimal? | Yes³ | Yes | No | No | Yes³ | Yes³˒⁴ |
| Time | $O(b^d)$ | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | $O(b^m)$ | $O(b^\ell)$ | $O(b^d)$ | $O(b^{d/2})$ |
| Space | $O(b^d)$ | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | $O(bm)$ | $O(b\ell)$ | $O(bd)$ | $O(b^{d/2})$ |

¹ if $b$ finite and the space has a solution or is finite; ² if all costs $\ge \epsilon > 0$; ³ if all action costs are equal; ⁴ if both directions are BFS or UCS. For **graph-search** versions, DFS becomes complete on finite spaces and all bounds are capped by $|V|+|E|$.

**Rule of thumb** ([[russell-norvig-aima]] §3.4.1, §3.4.4): exponential problems cannot be solved by uninformed search beyond tiny instances; **memory** is the first wall (BFS with $b=10$, $d=10$: < 3 h but 10 TB). IDS is the preferred uninformed method when the space is large and the solution depth unknown.

## In this course

- Slide 6 defines uninformed search and the four criteria; slide 7 BFS; slide 9 DFS ([[slides-02-problem-solving]]). Slides 8 and 10 are image-only (probably BFS/DFS illustrations — not recoverable from the text extraction). **UCS, IDS and bidirectional search are not on the slides**; they come from the textbook.
- HW01 uses BFS for the three small unit-cost path problems and DFS as a contrast on the 8-puzzle ([[hw01-ex01-8-puzzle]], [[hw01-ex04-farmer-wolf-goat-cabbage]], [[hw01-ex05-missionaries-cannibals]]).
- In the discussion, Dijkstra (= UCS) is the uninformed baseline against A* ([[discussion-01-astar-vs-dijkstra]], [[astar-vs-dijkstra]]).

## Common mistakes

- "BFS is optimal" without the condition **equal action costs**.
- Using $d$ for DFS time: DFS is $O(b^m)$, and $m$ can be ≫ $d$ or infinite.
- Forgetting that the table is for **tree-like** search; graph-search DFS uses $O(|V|)$ memory, not $O(bm)$.

## Related

[[informed-search]] · [[state-space-and-graph-search]] · [[search-algorithms-comparison]] · [[unit-03-search-review]]

## Practice questions

> [!question]- Q1. What is the only thing that distinguishes BFS, DFS and UCS from each other?
> **Answer.** The order of expansion, i.e. the frontier: FIFO queue, LIFO stack, priority queue on $g$ ([[slides-02-problem-solving]], slide 6; [[russell-norvig-aima]] §3.3.2).

> [!question]- Q2. With $b = 10$ and $d = 5$, how many nodes does BFS generate and how many does IDS generate?
> **Answer.** BFS: $10+100+1{,}000+10{,}000+100{,}000 = 111{,}110$. IDS: $5\cdot10 + 4\cdot100 + 3\cdot1{,}000 + 2\cdot10{,}000 + 1\cdot100{,}000 = 123{,}450$ — only ~11 % more, with linear memory ([[russell-norvig-aima]] §3.4.4).

> [!question]- Q3. Why is bidirectional search attractive in theory? Compute the saving for $b = d = 10$.
> **Answer.** Two searches of depth $d/2$: $2 b^{d/2} = 2\cdot 10^5$ vs $b^d = 10^{10}$ — 50,000× fewer nodes. It requires being able to search backwards from the goal ([[russell-norvig-aima]] §3.4.5).

> [!question]- Q4. Which uninformed algorithm would you choose for a huge unit-cost space whose solution depth is unknown, and why?
> **Answer.** Iterative deepening: complete and optimal for unit costs like BFS, but $O(bd)$ memory like DFS ([[russell-norvig-aima]] §3.4.4).

> [!question]- Q5. Name the four criteria used to evaluate search algorithms.
> **Answer.** Completeness, cost optimality, time complexity, space complexity ([[slides-02-problem-solving]], slide 6).
