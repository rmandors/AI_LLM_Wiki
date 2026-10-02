---
type: code
summary: Walkthrough of HW01 Exercise 5 — missionaries and cannibals with state (m_left, c_left, boat_left), five boat loads and a both-banks safety rule, solved by BFS in 11 crossings.
unit: 3
tags: [hw01, code, python, river-crossing, bfs, problem-formulation]
sources: ["[[hw01-report]]"]
updated: 2026-10-01
---

# HW01 Ex. 5 — Missionaries and cannibals (`Exercise05.py`)

**File**: `raw/HW_01/Practical_exercises/Exercise05.py` (165 lines).

**Problem.** Three missionaries and three cannibals must cross a river in a boat holding one or two people. On neither bank may cannibals outnumber missionaries when at least one missionary is there. Find the shortest crossing sequence ([[hw01-report]] §5).

## Design decisions

| Decision | Why |
|---|---|
| State = `(m_left, c_left, boat_left)` | right bank is always `3 - left`; storing it would be redundant. $4 \times 4 \times 2 = 32$ tuples, **20 legal**, **16 reachable** (verified by re-running, 2026-10-01) |
| Start `(3, 3, True)`, goal `(0, 0, False)` | everyone on the left |
| `BOAT_LOADS = [(1,0), (2,0), (0,1), (0,2), (1,1)]` | the capacity rule (1–2 people, never empty) encoded once |
| Check **both** banks | danger can appear on the bank the boat leaves or the one it reaches |
| [[breadth-first-search]] | small space, unit costs → minimum number of crossings |



## Walkthrough

| Lines | Function | What it does |
|---|---|---|
| 13 | `BOAT_LOADS` | 5 legal loads `(dm, dc)` |
| 16–26 | `is_legal(state)` | illegal if `m_left < c_left and m_left > 0`, same for the right bank |
| 29–34 | `describe_action` | text such as "0 missionary(ies) and 2 cannibal(s) cross the river" |
| 37–75 | `get_next_states(state)` | for each load: if boat left, the load must fit in the left bank (`dm > m_left or dc > c_left` → skip) and is subtracted; else must fit in the right bank and is added; flip boat; keep only legal results (l.70). Note `i = i + 1` before each `continue` (l.52, l.62) — without it the `while` loop never ends |
| 78–104 | `bfs` | `deque`, late goal test, `visited` set, `parent` dict; legality already filtered by the successor function |
| 107–117 | `reconstruct_path` | parent pointers |
| 120–157 | `print_solution`, `print_state` | output (both banks, boat side) |
| 160–165 | `__main__` | run and print |

## Results

BFS finds **11 crossings** (re-run 2026-10-01): 2C cross · 1C back · 2C cross · 1C back · 2M cross · 1M1C back · 2M cross · 1C back · 2C cross · **1M back** · **1M1C cross**.

- The last two steps differ from the classic textbook ending (1C back, 2C cross): both are optimal. From `(0, 1, right)` the loads are tried in `BOAT_LOADS` order and `(1,0)` precedes `(0,1)`, so "1 missionary returns" is enqueued first.
- First move: three legal options (1C, 2C, 1M1C). After "1C crosses" the only possible return recreates the start, so that branch is a dead end.
- 11 is the known optimum of the classic instance. Search-tree depth 11.

## Known issues / improvements

- Hard-coded 3: generalise to $N$ people and capacity $C$ by generating all `(dm, dc)` with $1 \le dm + dc \le C$.
- No generated/expanded counters (as in Ex04).
- `while` + manual `i = i + 1` before `continue` is fragile (an easy infinite-loop bug); a `for load in BOAT_LOADS` loop is safer (style).
- Legality inside the successor function here, outside in Ex04 — inconsistent design between the two files (both correct).

## Related concepts

[[problem-formulation]] · [[breadth-first-search]] · [[state-space-and-graph-search]] · [[hw01-ex04-farmer-wolf-goat-cabbage]] · [[uninformed-search]] · [[hw01-report]]

## Practice questions

> [!question]- Q1. Why store only the left bank?
> **Answer.** The right bank is determined: `3 - m_left`, `3 - c_left`. Storing it adds no information and multiplies the representable tuples.

> [!question]- Q2. How many states are legal and how many are reachable? Why the difference?
> **Answer.** 20 legal of 32, 16 reachable. Some legal tuples are unreachable, e.g. all six people on the left with the boat on the right `(3, 3, False)` — the boat cannot cross empty.

> [!question]- Q3. Why does your solution end with "1 missionary returns, 1 missionary and 1 cannibal cross"?
> **Answer.** Both endings are optimal; BFS keeps the first one generated, and `(1,0)` comes before `(0,1)` in `BOAT_LOADS`.

> [!question]- Q4. What happens if you remove `i = i + 1` before `continue` on line 52?
> **Answer.** The index never advances for an infeasible load, so the `while` loop spins forever on that load.

> [!question]- Q5. Compare this formulation with the farmer puzzle.
> **Answer.** Same BFS skeleton; the state is counts instead of booleans and the safety rule is numeric (outnumbering) instead of forbidden pairs.
