---
type: concept
summary: Beam search keeps only the k best nodes (by f or h) at each level and discards the rest — memory-bounded and fast, but incomplete and not optimal.
unit: 3
tags: [search, informed-search, beam-search, memory-bounded, satisficing]
sources: ["[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Beam search

**Beam search** limits the size of the frontier: it keeps only the **$k$ nodes with the best $f$-scores** (the *beam width*) and discards every other expanded node. Picture A* spreading in concentric contours; beam search explores only a narrow, focused slice of those contours ([[russell-norvig-aima]] §3.5.5).

## How it works

Level-by-level version (the one Raymond implemented):

```text
level ← [start]
while level not empty:
    children ← all successors of all nodes in level (skip already visited)
    if any child is a goal: return it # early goal test
    sort children by h (or f)
    level ← first k children
return failure
```

Variant: instead of a hard $k$, keep every node whose $f$ is within $\delta$ of the best — few nodes when there are strong candidates, more when there are none ([[russell-norvig-aima]] §3.5.5). Beam search with $k = 1$ is essentially greedy hill climbing; local beam search (Ch. 4) shares the idea ([[hill-climbing]]).

## Properties

| Property | Value |
|---|---|
| Complete | **No** — the good branch may be pruned |
| Cost-optimal | **No** |
| Time | $O(k\,b)$ nodes generated per level, $O(k\,b\,d)$ to depth $d$ |
| Space | $O(k\,b)$ per level (plus the visited set, if any) |
| Frontier | the current level, truncated to $k$ |

$k$ controls the trade-off: wider beam → fewer good branches discarded, more work; $k = \infty$ → BFS (or best-first). ([[russell-norvig-aima]] §3.5.5)

## In this course

- **Not on the slides** — taken from [[russell-norvig-aima]] §3.5.5 for HW01.
- [[hw01-ex02-80-tile]] `beam_search` (`Exercise02.py` l.351–416), max depth 4,000 (safety cap), 90 s limit ([[hw01-report]]):

| Width $k$ | Path | Generated | Expanded | Time |
|---|---|---|---|---|
| 500 | 1,078 | 1,996,339 | 535,239 | ~4.5 s |
| 5,000 | **740** | 13,759,668 | 3,650,285 | ~39 s |

  The 740-move path is Raymond's best answer for the 80-tile (≤ 2.42× the 306 lower bound). The wider beam costs ~7× more nodes and ~9× more time.
- Design details (–5.3):
  - **Ordering by $h$ only is equivalent to ordering by $f = g + h$**, because every node in a level has the same $g$ (= depth) under unit costs.
  - **Early goal test** (`if next_h == 0` while generating, l.396), unlike his A*.
  - `visited` is **global over all levels**, so the beam can even run out of children; the code returns failure then (l.403–405).
  - `counter` in the tuples breaks ties by insertion order, so Python never compares two 81-tuples.

## Common mistakes

- Calling beam search complete because it "eventually explores": it permanently discards nodes.
- Confusing beam width with depth limit.
- Forgetting that a global visited set can make the beam starve (no new children) even when solutions exist.
- Ordering by $h$ when costs are *not* unit — then $g$ differs within a level and $f$ should be used.

## Related

[[a-star]] · [[weighted-a-star]] · [[greedy-best-first-search]] · [[breadth-first-search]] · [[hill-climbing]] · [[informed-search]] · [[hw01-ex02-80-tile]]

## Practice questions

> [!question]- Q1. With $b = 4$ and $k = 500$, at most how many children are generated per level? How many after 1,078 levels?
> **Answer.** $k \cdot b = 2{,}000$ per level; $\approx 2{,}000 \times 1{,}078 \approx 2.16$ million. Raymond measured 1,996,339 (the blank often has fewer than 4 moves and visited states are skipped).

> [!question]- Q2. Is beam search complete? Optimal?
> **Answer.** Neither: discarding all but $k$ nodes can throw away the only path to the goal or the optimal one ([[russell-norvig-aima]] §3.5.5).

> [!question]- Q3. Why is sorting by $h$ the same as sorting by $g + h$ in Raymond's beam search?
> **Answer.** The beam advances one level at a time with unit costs, so all nodes in a level have $g$ = depth; adding a constant does not change the order.

> [!question]- Q4. Why did $k = 5000$ find a shorter path (740) than $k = 500$ (1,078)?
> **Answer.** A wider beam discards fewer promising nodes, so it is less likely to lose the good branch; the price is ~7× more generated nodes and ~9× more time.

> [!question]- Q5. What happens to beam search when $k = 1$? When $k = \infty$?
> **Answer.** $k = 1$: greedy descent along the single best child (like hill climbing). $k = \infty$: nothing is pruned — a level-by-level BFS (general knowledge; [[hill-climbing]]).
