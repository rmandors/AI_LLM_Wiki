---
type: concept
summary: Heuristic search that uses a problem-specific estimate h(n) of the cost to the goal to decide which frontier node to expand next; covers greedy best-first, A*, weighted A*, beam search and memory-bounded variants.
unit: 3
tags: [search, informed-search, heuristic-search, best-first-search, evaluation-function]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Informed (heuristic) search

**Informed search** uses extra knowledge about the problem — encoded in a **heuristic function** $h(n)$, the estimated cost of the cheapest path from $n$ to a goal — to guide exploration toward the goal ([[slides-02-problem-solving]], slide 11; [[russell-norvig-aima]] §3.5). A heuristic is only an *estimate*; it does not guarantee the correct path, but a good one dramatically reduces the number of nodes explored.

## How it works

Every informed algorithm here is **best-first search** ([[state-space-and-graph-search]]) with a different evaluation function $f(n)$, plus some memory-saving variations:

| Algorithm | $f(n)$ | Page |
|---|---|---|
| Uniform-cost (uninformed baseline) | $g(n)$ | [[uniform-cost-search]] |
| Greedy best-first | $h(n)$ | [[greedy-best-first-search]] |
| A* | $g(n) + h(n)$ | [[a-star]] |
| Weighted A* | $g(n) + W\,h(n)$, $W > 1$ | [[weighted-a-star]] |
| Beam search | keep only the $k$ best by $f$ | [[beam-search]] |
| IDA*, RBFS, SMA* | A* with bounded memory | [[a-star]], [[iterative-deepening-search]] |

Heuristic requirements from the slides: $h(n) \ge 0$ always and $h(\text{goal}) = 0$ ([[slides-02-problem-solving]], slide 11). Where heuristics come from (relaxed problems, pattern databases, landmarks) and how they are judged (admissibility, consistency, dominance, effective branching factor) is in [[heuristic-functions]].

**Weighted A\* unifies the family** ([[russell-norvig-aima]] §3.5.4): $W = 0$ → UCS, $W = 1$ → A*, $1 < W < \infty$ → weighted A*, $W = \infty$ → greedy.

## Properties

- Informed search keeps the same skeleton as uninformed search; only the priority changes.
- Quality depends on $h$: with $h \equiv 0$ A* is UCS; with $h = h^*$ (perfect) A* walks straight down the optimal path.
- Two families of goals: **optimal** (A* with admissible $h$) vs **satisficing** (greedy, weighted A*, beam: "good enough", faster) ([[russell-norvig-aima]] §3.5.4).
- Memory is the main limitation of A*-style searches → beam search, IDA*, RBFS, SMA* ([[russell-norvig-aima]] §3.5.5).

## In this course

- Slides 11 (informed search, $h$), 12 (best-first = greedy), 14 (A*) and 16 ("Properties of Heuristics", title only) of [[slides-02-problem-solving]]. Slides 13 and 15 are image-only. Weighted A* and beam search are **not on the slides**; Raymond took them from [[russell-norvig-aima]] §3.5.4–3.5.5 for HW01.
- HW01 uses: greedy best-first with 3 heuristics on the 8-puzzle ([[hw01-ex01-8-puzzle]], [[heuristics-8-puzzle-comparison]]); A*, weighted A* and beam search on the 80-tile ([[hw01-ex02-80-tile]]).
- Discussion 01: A* vs Dijkstra on Romania ([[astar-vs-dijkstra]]).
- In games, the heuristic idea reappears as the **evaluation function** at the cutoff of [[alpha-beta-pruning]] ([[chess-vs-go]]).

## Common mistakes

- Calling "best-first search" a single algorithm: in the book it is the *general scheme*; the slides use "best-first" for the *greedy* variant ([[slides-02-problem-solving]], slide 12 vs [[russell-norvig-aima]] §3.3.1).
- Assuming any heuristic makes search optimal — only admissible (tree) / consistent (graph) heuristics with A*.
- Ignoring the cost of computing $h$: a stronger but slow heuristic may lose in wall-clock time.

## Related

[[heuristic-functions]] · [[greedy-best-first-search]] · [[a-star]] · [[weighted-a-star]] · [[beam-search]] · [[uninformed-search]] · [[search-algorithms-comparison]] · [[hill-climbing]]

## Practice questions

> [!question]- Q1. What two properties must every heuristic satisfy according to the slides?
> **Answer.** $h(n) \ge 0$ for all $n$, and $h(n) = 0$ when $n$ is a goal ([[slides-02-problem-solving]], slide 11).

> [!question]- Q2. Give the evaluation function for UCS, greedy, A* and weighted A*, and the value of $W$ that turns weighted A* into each.
> **Answer.** UCS $g$ ($W=0$); A* $g+h$ ($W=1$); weighted A* $g+Wh$ ($1<W<\infty$); greedy $h$ ($W=\infty$) ([[russell-norvig-aima]] §3.5.4).

> [!question]- Q3. A node has $g = 140$ and $h = 253$. What is its priority under greedy, A* and weighted A* with $W = 2$?
> **Answer.** Greedy 253; A* $140 + 253 = 393$; weighted A* $140 + 2\cdot253 = 646$.

> [!question]- Q4. "Satisficing" — what does it mean and which algorithms are satisficing?
> **Answer.** Accepting a solution that is good enough rather than optimal, to save time/memory. Greedy best-first, weighted A*, beam search ([[russell-norvig-aima]] §3.5.4–3.5.5).
