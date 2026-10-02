---
type: code
summary: Walkthrough of HW01 Exercise 4 — the farmer, wolf, goat and cabbage river puzzle as a 4-boolean state space solved by BFS graph search in 7 crossings.
unit: 3
tags: [hw01, code, python, river-crossing, bfs, problem-formulation]
sources: ["[[hw01-report]]"]
updated: 2026-10-01
---

# HW01 Ex. 4 — Farmer, wolf, goat and cabbage (`Exercise04.py`)

**File**: `raw/HW_01/Practical_exercises/Exercise04.py` (161 lines).

**Problem.** A farmer must ferry a wolf, a goat and a cabbage across a river; the boat carries the farmer plus at most one passenger. Wolf and goat, or goat and cabbage, cannot be left together without the farmer. Find the shortest sequence of crossings ([[hw01-report]] §4).

## Design decisions

| Decision | Why |
|---|---|
| State = 4 booleans `(farmer, wolf, goat, cabbage)`, `True` = right bank | minimal description: only sides matter; boat is always with the farmer. $2^4 = 16$ tuples, **10 legal** (verified by re-running, 2026-10-01) |
| Start `(True)*4`, goal `(False)*4` | everyone starts on the right |
| 4 actions: farmer alone / with wolf / goat / cabbage | the passenger must be on the farmer's bank |
| [[breadth-first-search]], no heuristic | tiny space, unit costs → BFS gives the minimum number of crossings |
| Legality checked on the **new** state before enqueuing | the frontier only ever holds safe states |
| Graph search (`visited`) | every crossing is reversible, so BFS would otherwise loop |



## Walkthrough

| Lines | Function | What it does |
|---|---|---|
| 13–18 | `Actions` | list of 4 action strings — **order matters** for which optimal solution is returned |
| 20–25 | `State` | list of names; documentation only, never used |
| 28–38 | `is_legal(state)` | illegal if `wolf == goat and farmer != wolf` or `goat == cabbage and farmer != goat` |
| 41–45 | `flip_side(value)` | changes bank; equivalent to `not value` |
| 48–70 | `get_next_state(state, action)` | "alone" flips the farmer; otherwise picks passenger index, returns `None` if the passenger is on the other bank (l.65–66), else flips farmer + passenger. Returns a **list** |
| 73–97 | `bfs(start, goal)` | `deque`; late goal test after `popleft`; `tuple(next_state)` (l.90) because lists are unhashable; `visited` + `is_legal` filter (l.91–96); `parent` dict |
| 100–111 | `reconstruct_path` | parent pointers back to start |
| 114–150 | `print_solution`, `side_name`, `print_state` | output |
| 153–161 | `__main__` | run BFS and print |

## Results

BFS finds **7 crossings** (re-run 2026-10-01):

1. Farmer takes goat → 2. Farmer goes alone → 3. Farmer takes **wolf** → 4. Farmer takes goat (back) → 5. Farmer takes cabbage → 6. Farmer goes alone → 7. Farmer takes goat.

The twin optimal solution takes the cabbage at step 3 and the wolf at step 5. BFS returns the wolf-first one because `Actions` lists "takes wolf" before "takes cabbage": that child is enqueued first at depth 2, so its descendants reach the goal first. Search-tree depth 7; at most 10 nodes.

## Known issues / improvements

- `State` list (l.20–25) is unused — documentation only.
- BFS has **no generated/expanded counters**, unlike Ex01/Ex02, so the report can only give the path length.
- `flip_side` could be `not value`; `== True` comparisons are redundant (style).
- Legality is checked outside `get_next_state` (separation: transition model vs constraint); Ex05 does it inside — inconsistent across the two files but both correct.
- The start state's legality is never checked (it is legal, so harmless).

## Related concepts

[[problem-formulation]] · [[breadth-first-search]] · [[state-space-and-graph-search]] · [[hw01-ex05-missionaries-cannibals]] · [[uninformed-search]] · [[hw01-report]]

## Practice questions

> [!question]- Q1. Why is 7 the minimum and how do you know?
> **Answer.** BFS with unit costs explored every state at depth ≤ 6 without finding the goal. Intuitively: the goat must go first (any other first move leaves a forbidden pair) and must come back once.

> [!question]- Q2. How many of the 16 states are legal? Derive it.
> **Answer.** 10. For each farmer side: the 4 configurations where the goat is with the farmer are safe; with the goat alone, only 1 is safe (wolf and cabbage both with the farmer). 5 per side × 2 = 10.

> [!question]- Q3. There are two optimal solutions. Why did BFS return the wolf-first one?
> **Answer.** Action order: "takes wolf" precedes "takes cabbage" in `Actions`, so at depth 2 the wolf branch is enqueued first and its descendants reach the goal first; `parent[goal]` is set through that branch.

> [!question]- Q4. Why convert `next_state` to a tuple?
> **Answer.** `get_next_state` returns a list; lists are mutable and unhashable, so they cannot go into the `visited` set or be `parent` keys.

> [!question]- Q5. Would DFS work here?
> **Answer.** Yes — finite space and graph search guarantee termination — but it may return a longer sequence with unnecessary crossings ([[hw01-report]]).
