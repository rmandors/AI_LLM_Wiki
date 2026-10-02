---
type: concept
summary: Depth-limited DFS run repeatedly with limits 0, 1, 2,... — BFS's completeness and unit-cost optimality with DFS's O(bd) memory; IDA* applies the same idea to f-cost contours.
unit: 3
tags: [search, uninformed-search, ids, depth-limited-search, ida-star]
sources: ["[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Iterative deepening search (IDS)

**Depth-limited search (DLS)** is DFS that treats nodes at depth $\ell$ as if they had no children. **Iterative deepening search** runs DLS with $\ell = 0, 1, 2, \dots$ until a solution is found or DLS reports *failure* (not *cutoff*) ([[russell-norvig-aima]] §3.4.4). It combines the modest memory of DFS with the completeness and unit-cost optimality of BFS, and is "the preferred uninformed search method when the state space is larger than can fit in memory and the depth of the solution is not known".

## How it works

```text
ITERATIVE-DEEPENING(problem):
    for depth = 0 to ∞:
        result ← DEPTH-LIMITED(problem, depth)
        if result ≠ cutoff: return result # solution or failure

DEPTH-LIMITED(problem, ℓ): # tree-like, LIFO
    frontier ← stack [NODE(initial)]; result ← failure
    while frontier not empty:
        node ← POP(frontier)
        if IS-GOAL(node.state): return node
        if DEPTH(node) > ℓ: result ← cutoff
        else if not IS-CYCLE(node): push all children
    return result
```

Three return values: a solution, **failure** (no solution at any depth — space exhausted), **cutoff** (maybe a solution deeper than $\ell$) (Fig. 3.12).

**Repeated work is small**: level $d$ is generated once, level $d-1$ twice, …, level 1 $d$ times:
$$N(\text{IDS}) = d\,b + (d-1)\,b^2 + \dots + 1\cdot b^d = O(b^d).$$
For $b = 10$, $d = 5$: 123,450 vs BFS 111,110 ([[russell-norvig-aima]] §3.4.4).

**IDA\*** uses the $f = g + h$ cost as cutoff instead of depth; each iteration's new cutoff is the smallest $f$ that exceeded the old one. At most $C^*$ iterations when $f$ is integer (≤ 31 for the hardest 8-puzzles) ([[russell-norvig-aima]] §3.5.5). See [[a-star]].

## Properties

| | DLS | IDS |
|---|---|---|
| Complete | No (if $\ell < d$) | Yes (finite $b$; finite acyclic space or full cycle check) |
| Cost-optimal | No | Yes for equal action costs |
| Time | $O(b^\ell)$ | $O(b^d)$ (or $O(b^m)$ with no solution) |
| Space | $O(b\ell)$ | $O(bd)$ |
| Frontier | LIFO stack | LIFO stack |

A good $\ell$ can come from domain knowledge: Romania has 20 cities so $\ell = 19$ is safe, but its **diameter** is 9, a tighter limit ([[russell-norvig-aima]] §3.4.4).

## In this course

- **Not covered on the slides** ([[slides-02-problem-solving]]); textbook-only so far.
- **IDA\*** would not have rescued the 80-tile puzzle: it expands at least as many nodes as A* (repeating them each iteration), and A* already did not finish in 250,000 expansions ([[hw01-ex02-80-tile]]).
- Chess engines run alpha-beta inside **iterative deepening**, which is the nuance behind "BFS/DFS are not usable for chess" ([[chess-vs-go]], [[alpha-beta-pruning]]).

## Common mistakes

- Thinking IDS is "wasteful" by a large factor — the bottom level dominates, so overhead is ~$b/(b-1)$ (general knowledge; e.g. 11 % for $b = 10$).
- Forgetting the cycle check: tree-like IDS can loop inside one iteration on cyclic spaces.
- Confusing *cutoff* with *failure*: only failure proves no solution exists.

## Related

[[depth-first-search]] · [[breadth-first-search]] · [[uninformed-search]] · [[a-star]] · [[search-algorithms-comparison]]

## Practice questions

> [!question]- Q1. For $b = 2$, $d = 3$, how many nodes does IDS generate (excluding the root) and how many does BFS generate?
> **Answer.** IDS: $3\cdot2 + 2\cdot4 + 1\cdot8 = 22$. BFS: $2 + 4 + 8 = 14$. The overhead is larger for small $b$.

> [!question]- Q2. What is the space complexity of IDS and why?
> **Answer.** $O(bd)$: each iteration is a DFS to depth ≤ $d$, storing one path plus siblings ([[russell-norvig-aima]] §3.4.4).

> [!question]- Q3. Difference between the *cutoff* and *failure* results of depth-limited search?
> **Answer.** Cutoff: some node was cut at the limit, so a deeper solution might exist. Failure: the whole space was exhausted, no solution at any depth (Fig. 3.12).

> [!question]- Q4. Why would IDA* not have solved Raymond's 80-tile instance where A* failed?
> **Answer.** IDA* saves memory, not node expansions — it re-expands the f-contours every iteration, so it expands at least as many nodes as A*. The bottleneck was the 306-vs-$C^*$ heuristic gap, not memory alone.
