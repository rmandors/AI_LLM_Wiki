---
type: concept
summary: Uninformed search that expands the shallowest node first with a FIFO queue; complete, optimal only for equal action costs, O(b^d) time and space.
unit: 3
tags: [search, uninformed-search, bfs, fifo, early-goal-test]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Breadth-first search (BFS)

**Breadth-first search** expands the root, then all its children, then all grandchildren — **level by level, shallowest node first** — using a **FIFO queue** as the frontier ([[slides-02-problem-solving]], slide 7). Because it finishes depth $d-1$ before touching depth $d$, the first goal it finds has the **fewest actions**. It is the default choice for small spaces with unit action costs.

## How it works

Book version with the **early goal test** ([[russell-norvig-aima]] §3.4.1, Fig. 3.9):

```text
node ← NODE(initial); if IS-GOAL(node.state): return node
frontier ← FIFO queue [node]; reached ← {initial}
while frontier not empty:
    node ← POP(frontier) # oldest = shallowest
    for child in EXPAND(node):
        if IS-GOAL(child.state): return child # early test: on generation
        if child.state not in reached:
            add child.state to reached; push child
return failure
```

Two tricks over generic best-first search: a FIFO queue is faster than a priority queue, and `reached` can be a plain **set** because the first path to a state is already the shallowest. That is also why the **early goal test** is safe for BFS (it is *not* safe for UCS/A*).

## Properties

| Property | Value | Note |
|---|---|---|
| Complete | Yes | if $b$ finite; systematic, so complete even on infinite spaces ([[russell-norvig-aima]] §3.4.1) |
| Cost-optimal | Yes **iff all action costs are equal** | finds fewest-steps path ([[slides-02-problem-solving]], slide 7) |
| Time | $O(b^d)$ | $1 + b + b^2 + \dots + b^d$ |
| Space | $O(b^d)$ | every node stays in memory; frontier grows exponentially |
| Frontier | FIFO queue | |

**Memory is the real problem**: $b = 10$, $10^6$ nodes/s, 1 KB/node, $d = 10$ → under 3 hours but **10 TB**; $d = 14$ → 3.5 years ([[russell-norvig-aima]] §3.4.1).

With a **late goal test** (test on pop), BFS generates one extra layer — up to $O(b^{d+1})$ — but remains optimal for unit costs.

## In this course

- Slide 7: "expands the shallowest nodes first, level by level; FIFO queue; complete; optimal (fewest steps when costs are uniform); $O(b^d)$ time and space; memory grows exponentially with depth" ([[slides-02-problem-solving]]). Slide 8 is image-only.
- **HW01** — BFS is Raymond's tool for every small unit-cost path problem:
  - [[hw01-ex01-8-puzzle]]: optimal path **20** moves, 149,026 generated, 55,409 expanded. Generated/expanded ≈ 2.7, matching the 8-puzzle's average branching factor $(4\cdot2 + 4\cdot3 + 1\cdot4)/9 = 2.67$.
  - [[hw01-ex04-farmer-wolf-goat-cabbage]]: **7** crossings.
  - [[hw01-ex05-missionaries-cannibals]]: **11** crossings.
- Implementation: `collections.deque` + `popleft` (O(1); `list.pop(0)` would be O(n)); `visited` set marked **when generated**; `parent` dict for path reconstruction.
- **Late goal test**: all three BFS implementations test `current_state == goal_state` right after `popleft` (e.g. `Exercise01.py` l.152). Still optimal for unit cost; it only inflates the generated count slightly. This differs from the book's Fig. 3.9.

## Common mistakes

- Claiming BFS is optimal with **varying costs** — use [[uniform-cost-search]] instead.
- Implementing the queue with `list.pop(0)` ($O(n)$ per pop).
- Thinking the early goal test is always fine: in UCS it can return a costlier path ([[russell-norvig-aima]] §3.4.2).
- Underestimating memory: BFS dies of memory before time.

## Related

[[uninformed-search]] · [[depth-first-search]] · [[uniform-cost-search]] · [[iterative-deepening-search]] · [[state-space-and-graph-search]] · [[search-algorithms-comparison]]

## Practice questions

> [!question]- Q1. Why is BFS cost-optimal when every action costs 1, but not in general?
> **Answer.** With unit costs, path cost = depth, and BFS reaches every depth-$(d-1)$ node before any depth-$d$ node, so the first goal found is the shallowest = cheapest. With different costs a deeper path can be cheaper ([[russell-norvig-aima]] §3.4.1).

> [!question]- Q2. How many nodes does BFS generate for $b = 3$, $d = 4$ (early goal test, worst case)?
> **Answer.** $1 + 3 + 9 + 27 + 81 = 121$ nodes. With a late goal test it could also generate the children of depth-4 nodes: up to $3^5 = 243$ more.

> [!question]- Q3. Raymond's BFS tests the goal when popping. Is the result still optimal? What does it cost?
> **Answer.** Yes — unit costs, FIFO order still pops shallow nodes first. The cost is one extra layer of generated nodes before the goal is popped.

> [!question]- Q4. Why is `reached` a set (not a dict of best costs) in BFS?
> **Answer.** The first time BFS reaches a state it is via a shallowest path; no later path can be better, so only membership matters ([[russell-norvig-aima]] §3.4.1).

> [!question]- Q5. In the 8-puzzle run, BFS generated 149,026 nodes and expanded 55,409. Estimate the average branching factor and compare with theory.
> **Answer.** $149{,}026 / 55{,}409 \approx 2.69$. Theory: the blank has 2 moves in 4 corners, 3 on 4 edges, 4 in the centre: $(8+12+4)/9 \approx 2.67$.
