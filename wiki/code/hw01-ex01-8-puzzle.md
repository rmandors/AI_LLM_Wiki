---
type: code
summary: Walkthrough of HW01 Exercise 1 — 8-puzzle solved with BFS (optimal 20 moves), DFS (66,056) and greedy best-first with Manhattan, Euclidean and misplaced-tiles heuristics, all as graph search.
unit: 3
tags: [hw01, code, python, 8-puzzle, bfs, dfs, greedy, heuristics]
sources: ["[[hw01-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# HW01 Ex. 1 — 8-puzzle (`Exercise01.py`)

**File**: `raw/HW_01/Practical_exercises/Exercise01.py` (298 lines).

**Problem.** Solve the 8-puzzle from the start board of the book's Figure 3.3, `7 2 4 / 5 _ 6 / 8 3 1`, to the goal `1 2 3 / 4 5 6 / 7 8 _` (blank last), comparing [[breadth-first-search]], [[depth-first-search]] and [[greedy-best-first-search]] with three [[heuristic-functions]] (Euclidean, Manhattan, and a free choice: misplaced tiles). Report path length, generated and expanded nodes ([[hw01-report]] §1).

## Design decisions

| Decision | Why |
|---|---|
| State = flat tuple of 9 ints, 0 = blank | Hashable → fits in `set`/`dict`; cheap copy; row = `i // 3`, col = `i % 3` |
| Actions move the **blank** | 4 action names instead of tile × direction ([[russell-norvig-aima]] §3.2.1) |
| Inversion-parity check first | Only half the boards reach a given goal; on a 3×3 (odd width) board, solvable iff same inversion parity. Avoids a useless exhaustive search of 181,440 states |
| BFS for the optimum | Unit costs ⇒ BFS is cost-optimal ([[russell-norvig-aima]] §3.4.1) |
| Greedy best-first ($f = h$), not A* | Shows the pure effect of each heuristic; A* would add $g$ |
| Misplaced tiles as free heuristic | Book's $h_1$ alongside Manhattan $h_2$; lets him show dominance experimentally |
| Graph search everywhere (`visited` set) | Every move is reversible; without it states repeat forever ([[state-space-and-graph-search]]) |
| No depth limit on DFS | To show DFS's real behaviour; graph DFS terminates on a finite space |



## Walkthrough

| Lines | Function | What it does |
|---|---|---|
| 16–18 | `START_STATE`, `GOAL_STATE` | tuples `(7,2,4,5,0,6,8,3,1)` and `(1,2,3,4,5,6,7,8,0)` |
| 21–26 | `MOVES` | `(name, index_change, row_change, col_change)`; Up = −3 (one row = 3 cells) |
| 29–40 | `print_board` | ASCII board |
| 43–47 | `find_blank` | linear scan for 0 |
| 50–68 | `get_next_states` | blank row/col; skip moves that leave the board (l.59); `list(state)`, swap blank with neighbour (l.63–65), return `(tuple(new_state), name)` — the **transition model** |
| 71–83 | `inversion_count` | drop the blank, double loop counting pairs $i<j$ with `tiles[i] > tiles[j]`; $O(n^2)$ |
| 86–87 | `is_solvable` | compare parities (`% 2`) of start and goal |
| 90–98 | `reconstruct_path` | follow `parent[state] = (prev, action)` from goal to start (start has `(None, None)`), then `reverse` — the book's `node.PARENT` / `node.ACTION` |
| 102–107 | `misplaced_tiles` | counts `state[i] != 0 and state[i] != goal[i]` — **skips the blank** (including it would break admissibility) |
| 110–123 | `manhattan_distance` | `goal_state.index(tile)` then `abs(dr) + abs(dc)` |
| 126–139 | `euclidean_distance` | same with `math.sqrt(dr**2 + dc**2)` |
| 142–163 | `bfs` | `deque` + `popleft` (FIFO); **late goal test** right after pop (l.152); state marked visited **when generated** (l.158–160) so it enters the queue once |
| 166–187 | `dfs` | identical code with a list as stack and `stack.pop` — only the frontier changes |
| 190–215 | `best_first_search(start, goal, heuristic)` | `heapq` of `(h, state)`; heuristic passed as a function parameter so one routine runs all three; ties on $h$ broken by comparing state tuples |
| 218–238 | `print_path` | prints every board only if ≤ 30 moves (why DFS's 66,056 moves aren't printed) |
| 241–254 | `print_stats` | aligned table with `ljust` |
| 257–298 | `__main__` | parity check, run 5 searches, print comparison |

**Counters**: `generated` = every successor produced by `get_next_states` (duplicates included); `expanded` = every pop (including the goal).

## Results

Re-run on 2026-10-01 — identical to the report ([[hw01-report]]):

| Strategy | Path | Generated | Expanded |
|---|---|---|---|
| BFS | **20** (optimal) | 149,026 | 55,409 |
| DFS | 66,056 | 269,224 | 99,900 |
| Greedy Euclidean | 94 | 1,132 | 413 |
| Greedy Manhattan | 48 | 339 | 123 |
| Greedy misplaced | 116 | 3,069 | 1,134 |

- Start values: misplaced $h_1 = 6$, Euclidean $= 11.30$, Manhattan $h_2 = 14$; inversions = 16 (even; goal 0).
- BFS generated/expanded ≈ 2.69 ≈ average 8-puzzle branching factor 2.67. Effective branching factor of BFS here: $b^* \approx 1.74$ for $N = 149{,}026$, $d = 20$ (computed for this wiki; book A*($h_2$) at $d = 20$: 1.34).
- Interpretation in [[heuristics-8-puzzle-comparison]].

## Known issues / improvements

- **Late goal test in BFS**: the book's BFS tests on generation (Fig. 3.9). Still optimal for unit cost; one extra layer generated.
- **"Start board from the book figure"**: only the *start* is the book's. The book's goal has the blank top-left (`_ 1 2 / 3 4 5 / 6 7 8`, optimum 26, $h_1 = 8$, $h_2 = 18$); Raymond's goal has it bottom-right → optimum 20, $h_1 = 6$, $h_2 = 14$. Say "same start, different goal".
- **No A\***: the natural next step for an optimal heuristic search; book Fig. 3.26 suggests ~1,300 vs ~91,000 nodes at $d = 20$.
- **Graph-search DFS** uses $O(\text{states})$ memory, not the $O(bm)$ of tree-like DFS (§4.5 Q8).
- No drawn BFS/DFS graph (149,026 nodes); if required, reuse the depth-2 Graphviz approach from [[hw01-ex02-80-tile]] (§4.6).
- Minor: `goal_state.index(tile)` inside the heuristic loop is $O(9)$ per tile; a precomputed goal-position table (as in Ex02) is faster.

## Related concepts

[[problem-formulation]] · [[state-space-and-graph-search]] · [[breadth-first-search]] · [[depth-first-search]] · [[greedy-best-first-search]] · [[heuristic-functions]] · [[a-star]] · [[heuristics-8-puzzle-comparison]] · [[hw01-report]]

## Practice questions

> [!question]- Q1. Why is BFS optimal here, and why does your BFS test the goal when popping instead of when generating?
> **Answer.** All moves cost 1, so the first goal at the shallowest depth is cheapest. The late test keeps all searches uniform; it is still optimal for unit cost, it only generates one extra layer (–Q2).

> [!question]- Q2. Why does `misplaced_tiles` skip the blank?
> **Answer.** Counting the blank can overestimate (e.g. one move from the goal: blank and one tile both out of place → 2 > 1), so the heuristic would no longer be admissible.

> [!question]- Q3. Why check inversion parity? What would happen without it on an unsolvable start?
> **Answer.** On a 3×3 board, a board reaches the goal iff inversion parities match. Without the check, BFS would exhaust all 181,440 reachable states and then fail; the check answers immediately.

> [!question]- Q4. Your greedy Manhattan found 48 moves with 123 expansions. Why not 20?
> **Answer.** Greedy uses $f = h$ and ignores $g$; it follows what looks closest, lengthening the path. A* ($g + h$) with Manhattan would return 20 ([[greedy-best-first-search]]).

> [!question]- Q5. Show that Manhattan ≥ Euclidean ≥ misplaced for every state.
> **Answer.** Per tile: $|dr| + |dc| \ge \sqrt{dr^2 + dc^2}$ (triangle inequality), and a misplaced tile has distance ≥ 1 (contributes ≥ 1 to Euclidean, exactly 1 to misplaced); placed tiles contribute 0 to all. Sum over tiles. Start: 14 ≥ 11.30 ≥ 6.

> [!question]- Q6. Why are states tuples and not lists?
> **Answer.** Tuples are immutable and hashable, so they can be stored in `visited` (a set) and used as keys in `parent` (a dict). A move copies into a list, swaps, and converts back.

> [!question]- Q7. What is the difference between "generated" and "expanded" in your table?
> **Answer.** Generated = every successor produced, including duplicates later discarded; expanded = every node popped from the frontier, including the goal. BFS ratio ≈ 2.7 ≈ the puzzle's average branching factor.
