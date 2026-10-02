---
type: concept
summary: Uninformed search that always expands the deepest node using a LIFO stack; not optimal, complete only on finite spaces with repeated-state control, but only O(bm) memory as a tree-like search.
unit: 3
tags: [search, uninformed-search, dfs, lifo, backtracking]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Depth-first search (DFS)

**Depth-first search** always expands the **deepest** node on the frontier, following one branch to the end before backing up to the next deepest unexpanded node. The frontier is a **LIFO stack** ([[slides-02-problem-solving]], slide 9). Its selling point is memory: as a tree-like search it stores only the current path plus the unexpanded siblings, $O(bm)$.

## How it works

Same loop as [[breadth-first-search]], but `pop` from the end of the frontier. It is usually implemented as a **tree-like** search, optionally with a cycle check on the current path ([[russell-norvig-aima]] §3.4.3).

**Backtracking search** is a DFS variant that generates **one successor at a time** and modifies the state in place, undoing the change on return: memory falls to one state + $O(m)$ actions ([[russell-norvig-aima]] §3.4.3). It is the basis of [[csp-backtracking-search]] and of Prolog's [[sld-resolution]].

## Properties

| Property | Tree-like DFS | Graph-search DFS |
|---|---|---|
| Complete | No (infinite paths, cycles) | Yes on **finite** spaces |
| Cost-optimal | No — returns the first solution found | No |
| Time | $O(b^m)$ | bounded by $|V|+|E|$ |
| Space | $O(bm)$ | $O(|V|)$ (the reached table) |
| Frontier | LIFO stack | LIFO stack |

([[russell-norvig-aima]] §3.4.3, §3.4.6.) $m$ is the maximum depth — possibly much larger than $d$, or infinite.

Why use it? DFS is the workhorse of CSPs, SAT and logic programming because some problems that would need exabytes with BFS fit in kilobytes with DFS ([[russell-norvig-aima]] §3.4.3).

## In this course

- Slide 9: "expands the deepest nodes first; LIFO stack; complete only when repeated states are controlled and the space is finite; not optimal; $O(b^m)$ time; $O(b\cdot m)$ space; low memory compared with BFS" ([[slides-02-problem-solving]]). Slide 10 is image-only.
- **HW01 8-puzzle** ([[hw01-ex01-8-puzzle]]): DFS found a path of **66,056 moves** (optimal is 20), generating 269,224 and expanding 99,900 nodes. Code is identical to BFS except `stack.pop` — the point being that only the frontier changes.
- Raymond's DFS is a **graph-search** DFS (marks states visited when pushed): complete on the 181,440-state space, but memory is $O(\text{states})$, not $O(bm)$.
- The report argues DFS could solve the farmer and M&C puzzles but may return longer walks ([[hw01-report]]).
- [[hw01-ex03-n-queens]] and [[hw01-ex06-sudoku]] use recursive **backtracking** = DFS over partial assignments; the call stack *is* the path.
- In games, [[minimax]] and [[alpha-beta-pruning]] traverse the tree depth-first ([[chess-vs-go]]).

## Common mistakes

- Saying DFS is complete "because it explores everything": only with repeated-state control **and** a finite space.
- Using $O(bm)$ space for a graph-search DFS — the visited set is $O(|V|)$.
- Confusing "DFS found a solution quickly" with "DFS found a short solution" (66,056 vs 20).
- Forgetting that a recursive DFS in Python can hit the recursion limit (~1000 frames) on deep spaces (general knowledge).

## Related

[[uninformed-search]] · [[breadth-first-search]] · [[iterative-deepening-search]] · [[csp-backtracking-search]] · [[backward-chaining]] · [[search-algorithms-comparison]]

## Practice questions

> [!question]- Q1. Why did Raymond's DFS return a 66,056-move solution for an 8-puzzle whose optimum is 20?
> **Answer.** DFS always continues from the newest (deepest) state, wandering through a large part of the state space; the path returned is just the branch it happened to follow. It terminated only because graph search + finite space.

> [!question]- Q2. Compare the memory of tree-like DFS and BFS for $b = 10$, $d = m = 12$ (count nodes stored).
> **Answer.** DFS: $\approx b\cdot m = 120$ nodes. BFS: $\approx b^d = 10^{12}$ nodes. Ten orders of magnitude.

> [!question]- Q3. On which kind of space is tree-like DFS complete? Where can it fail?
> **Answer.** Complete on finite tree-shaped (acyclic) spaces. It fails by looping on cycles, or by descending an infinite path in infinite spaces ([[russell-norvig-aima]] §3.4.3).

> [!question]- Q4. How does backtracking search reduce DFS's memory further?
> **Answer.** It generates one successor at a time and modifies a single state in place (undoing on backtrack), so it stores one state and $O(m)$ actions instead of $O(bm)$ nodes ([[russell-norvig-aima]] §3.4.3).

> [!question]- Q5. Is DFS optimal if all costs are equal?
> **Answer.** No. It returns the first solution on the current branch, which can be arbitrarily deep ([[slides-02-problem-solving]], slide 9).
