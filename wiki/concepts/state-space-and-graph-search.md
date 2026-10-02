---
type: concept
summary: The state space as an implicit graph, the search tree built over it, frontier vs reached/explored sets, and the difference between graph search and tree-like search.
unit: [2, 3]
tags: [search, state-space, graph-search, tree-search, frontier, repeated-states]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# State space and graph search

The **state space** is the set of all states reachable from the initial state by any sequence of actions. It is a graph — nodes are world states, edges are actions with costs — but in practice it is **never built explicitly** because it is too large; the agent explores it progressively ([[slides-02-problem-solving]], slide 4). A **search tree** is what an algorithm superimposes on that graph while exploring it: each tree node is one *path* to a state, so the same state can appear many times ([[slides-02-problem-solving]], slide 5; [[russell-norvig-aima]] §3.3).

## How it works

**Node data structure** ([[russell-norvig-aima]] §3.3.2): `node.STATE`, `node.PARENT`, `node.ACTION`, `node.PATH-COST` (= $g(n)$). Following parent pointers from a goal node rebuilds the solution.

**Vocabulary** ([[russell-norvig-aima]] §3.3):
- **Expand** a node: apply every applicable action, **generate** a child per result.
- **Frontier** (open list): generated but not yet expanded nodes.
- **Reached**: every state for which a node has been generated (frontier ∪ expanded). The slides call the expanded part the **explored set** (closed list) ([[slides-02-problem-solving]], slide 5).
- **Separation property**: the frontier separates the expanded interior from the unreached exterior (Fig. 3.6).

**Generic best-first graph search** (Fig. 3.7, simplified):

```text
frontier ← priority queue ordered by f, containing node(initial)
reached ← {initial: node}
while frontier not empty:
    node ← POP(frontier)
    if IS-GOAL(node.state): return node # late goal test
    for child in EXPAND(node):
        s ← child.state
        if s not in reached or child.g < reached[s].g:
            reached[s] ← child; add child to frontier
return failure
```

Choosing the queue / evaluation function $f$ gives every algorithm in [[uninformed-search]] and [[informed-search]]: FIFO → [[breadth-first-search]], LIFO → [[depth-first-search]], $f=g$ → [[uniform-cost-search]], $f=h$ → [[greedy-best-first-search]], $f=g+h$ → [[a-star]].

**Three ways to treat repeated states** ([[russell-norvig-aima]] §3.3.3):
1. **Graph search** — remember all reached states, keep only the best path to each. Preferred when the table fits in memory.
2. **Tree-like search** — don't check at all; saves memory, wastes time on redundant paths, can loop forever on cycles.
3. **Cycle check only** — follow parent pointers to reject paths that revisit a state on the *current* path (used by depth-limited / [[iterative-deepening-search]]).

## Properties

- **Repeated states** come from cycles (Arad → Sibiu → Arad) and from **redundant paths** (two routes to Sibiu, one worse). Without control the tree can be infinite even when the graph is finite (20 cities) ([[russell-norvig-aima]] §3.3.3).
- With control, **each state is explored at most once** and termination is guaranteed in finite spaces ([[slides-02-problem-solving]], slide 5).
- Cost: graph search stores every reached state — memory $O(|V|)$ in the worst case.
- Complexity is measured by $|V|+|E|$ for explicit graphs, or by $b$ (branching factor), $d$ (depth of shallowest solution) and $m$ (maximum depth) for implicit ones ([[russell-norvig-aima]] §3.3.4).

## In this course

- Slide 4 defines the state space as a graph that is explored progressively; slide 5 contrasts **state graph** vs **search tree** and introduces **frontier** + **explored set** ([[slides-02-problem-solving]]).
- All of Raymond's path searches in HW01 are **graph searches**: `visited` is a `set` (BFS/DFS/greedy/beam) or a `dict state → best g` (weighted A*):
  - [[hw01-ex01-8-puzzle]] — marks a state visited *when generated* (`Exercise01.py` l.158–160), so each state enters the frontier once.
  - [[hw01-ex02-80-tile]] — weighted A* re-pushes a state if a cheaper $g$ is found (l.335), exactly the book's `child.PATH-COST < reached[s].PATH-COST` test.
  - [[hw01-ex04-farmer-wolf-goat-cabbage]], [[hw01-ex05-missionaries-cannibals]] — every crossing is reversible, so without `visited` BFS would bounce forever.
- The **Graphviz tree** of the 80-tile is drawn in **tree-like** mode (no visited set): its depth-2 level contains the start state again (Up then Down, $h=306$).
- 8-puzzle size: $9!/2 = 181{,}440$ reachable states, small enough to keep in memory ([[russell-norvig-aima]] §3.6 prints "181,400", a typo).

## Common mistakes

- Saying "the 8-puzzle search tree has 181,440 nodes": that is the **state space**; the tree is infinite without repeated-state control.
- Confusing **reached** (generated) with **expanded**. Raymond's counters: "generated" counts every successor produced (including duplicates thrown away), "expanded" counts pops.
- Marking states visited only on expansion in BFS — duplicates then pile up in the queue (still correct, more memory).
- Using a list as the visited structure — membership test becomes $O(n)$; use a hash set/dict of **hashable** (tuple) states.

## Related

[[problem-formulation]] · [[uninformed-search]] · [[informed-search]] · [[breadth-first-search]] · [[depth-first-search]] · [[a-star]] · [[search-algorithms-comparison]] · [[unit-03-search-review]]

## Practice questions

> [!question]- Q1. State graph vs search tree: which can contain the same state twice, and why?
> **Answer.** The search tree. The graph has one node per state; the tree has one node per *path*, and different paths (or cycles) can lead to the same state ([[slides-02-problem-solving]], slide 5).

> [!question]- Q2. What is the difference between graph search and tree-like search, and what does each cost?
> **Answer.** Graph search keeps a reached table and never adds a state twice (unless with a cheaper path): more memory, no redundant work, terminates on finite spaces. Tree-like search keeps no table: less memory, but redundant paths and possible infinite loops ([[russell-norvig-aima]] §3.3.3).

> [!question]- Q3. In a 10×10 grid with 8-neighbour moves, every cell is reachable in ≤ 9 moves. Roughly how many paths of length 9 exist, and what does that say about tree-like search?
> **Answer.** Almost $8^9 \approx 1.3 \times 10^8$ paths for only 100 cells — over a million redundant paths per cell on average. Eliminating redundant paths makes search roughly a million times faster ([[russell-norvig-aima]] §3.3.3).

> [!question]- Q4. Raymond's 80-tile Graphviz tree shows a depth-2 node with $h = 306$, the same as the start. Explain.
> **Answer.** It *is* the start state (Up then Down). The figure is drawn tree-like, without a visited set; the real searches would discard it as already reached ([[hw01-ex02-80-tile]]).

> [!question]- Q5. Define the three parameters $b$, $d$, $m$.
> **Answer.** $b$ = branching factor (successors per node), $d$ = depth (number of actions) of the shallowest/optimal solution, $m$ = maximum depth of any path (may be ∞) ([[russell-norvig-aima]] §3.3.4).
