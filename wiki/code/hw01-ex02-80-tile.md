---
type: code
summary: Walkthrough of HW01 Exercise 2 — the 9×9 "80-tile" puzzle with Manhattan distance; A* hits its 250,000-expansion cap, weighted A* (W=10) finds 1,116 moves, beam search finds 1,078 (k=500) and 740 (k=5000); optimum lies in [306, 740].
unit: 3
tags: [hw01, code, python, sliding-puzzle, a-star, weighted-a-star, beam-search, graphviz]
sources: ["[[hw01-report]]", "[[hw01-ai-transcript]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# HW01 Ex. 2 — 80-tile puzzle (`Exercise02.py`)

**File**: `raw/HW_01/Practical_exercises/Exercise02.py` (625 lines). Writes `Exercise02_tree.dot` next to itself.

**Problem.** The 8-puzzle scaled to a 9×9 board: 80 tiles named *number + quadrant letter* (`3F`) and one hole. Start: quadrants `A B C / D E F / G H I`, each block `1..9` in reading order, hole bottom-right (tile **9I** removed). Goal: quadrants `A B C / H I D / G F E`, each block `1 2 3 / 8 9 4 / 7 6 5` — a **clockwise spiral** at both levels, so the hole ends at the centre (index 40). Achieve the shortest path exploring as few states as possible, show a portion of the tree, report generated/expanded nodes and path length ([[hw01-report]] §2; statement quoted in [[hw01-ai-transcript]]).

## Design decisions

| Decision | Why |
|---|---|
| `tile = quadrant * 9 + number` (1..81), state = 81-tuple | one int per tile keeps the 8-puzzle representation; `tile_name` decodes |
| Remove **9I** (`BLANK_TILE = 8*9 + 9`) | "only quadrant I has an empty space" + hole starts bottom-right (see 9H vs 9I below) |
| General parity test | permutation parity (incl. blank) must equal parity of the blank's taxicab distance; each move flips both. Start: parity 0, taxicab 8 → solvable |
| **Manhattan** only | admissible + consistent; $h(\text{start}) = 306$ is a lower bound on $C^*$; max(Manhattan, misplaced) = Manhattan |
| [[a-star]] first, cap 250,000 expansions / 30 s | the only optimal option; memory grows fast with 81-tuples |
| [[weighted-a-star]] $W = 10$, cap 10⁶ / 60 s | satisficing (§3.5.4); $W$ chosen **by trial** |
| [[beam-search]] $k = 500$ and $5000$, max depth 4,000, 90 s | memory-bounded (§3.5.5); two widths show the trade-off |
| Beam ordered by $h$ only | same $g$ within a level ⇒ same order as $f = g + h$ |
| Precomputed tables | `cost[tile][index]` (82 × 81) and legal blank moves per cell avoid millions of `index` calls and bounds checks |
| **Incremental heuristic** | one move moves one tile: `next_h = h - cost[tile][new_blank] + cost[tile][blank]`, $O(1)$ instead of $O(81)$ |
| Tree portion depth 2 | 1 + 2 + 6 = **9 nodes, 8 edges**; enough to show successors and $h$ |



## Walkthrough

| Lines | Function | What it does |
|---|---|---|
| 16–35 | constants | `SIZE = 9`, `N_CELLS = 81`, `START/GOAL_QUADRANTS`, `START/GOAL_INSIDE = [1,2,3,8,9,4,7,6,5]`, `BLANK_TILE`, `MOVES` with ±`SIZE` for Up/Down |
| 38–47 | `make_tile`, `tile_name` | encode; decode with `(tile-1)//9` → letter, `(tile-1)%9+1` → number |
| 50–80 | `build_board(quadrants, inside)` | for block `qi` (block row `qi//3`, col `qi%3`) and local cell `li`, write tile at `row*9+col`; then replace 9I with 0 |
| 83–110 | `board_lines`, `print_board` | text board with block separators |
| 113–145 | `find_blank`, `get_next_states` | generic successor function (used only by the Graphviz walk) |
| 148–186 | `inversion_parity` | map tiles to goal indices (`perm`), decompose into **cycles**; a cycle of length $L$ = $L-1$ swaps; total mod 2 |
| 189–200 | `blank_taxicab`, `is_solvable` | parity(perm) == taxicab % 2 |
| 203–213 | `reconstruct_path` | parent pointers, as in Ex01 |
| 216–242 | `build_goal_tables` | `cost[tile][p]` = Manhattan distance of `tile` at cell `p` |
| 245–253 | `manhattan_distance` | table lookups, used once for the start |
| 256–280 | `neighbors_of_blank` | for each cell, list of `(move, new_blank)` |
| 283–287 | `apply_move` | swap blank and neighbour, return tuple |
| 290–344 | `weighted_a_star(start, cost, neigh, weight, max_expansions, time_limit)` | heap entries `(f, g, h, counter, state, blank)` (l.295, l.341); `visited` = dict **state → best g** (l.297); goal test **on pop**: `if h_value == 0` (l.316; Manhattan is 0 only at the goal); limits checked (l.321); re-push if cheaper $g$ (l.335, the book's Fig. 3.7 test); incremental $h$ (l.338); `best_h` tracks progress |
| 347–348 | `a_star` | `weighted_a_star(..., 1,...)` — A* as the $W = 1$ case |
| 351–416 | `beam_search(start, cost, neigh, width, max_depth, time_limit)` | expand the whole level, build `children`; **early goal test** `if next_h == 0` (l.396); global `visited` (l.389–391); `children.sort` on `(h, counter, …)`; keep first `width`; failure if no children (l.403–405) |
| 419–446 | `board_dot_label` | HTML-like Graphviz table: yellow hole, alternating grey quadrants, `h=` in the title |
| 449–461 | `write_dot_walk` | **recursive tree walk without visited set**; `counter = [0]` is a one-element list so recursive calls share a mutable counter |
| 464–480 | `write_dot_file`, `print_tree_portion` | write the `.dot`, suggest edotor.net |
| 483–530 | `print_compact_path`, `print_stats` | output |
| 533–625 | `__main__` | build boards and tables, parity check, tree depth 2 (l.558), run the four solvers with limits (l.561–598), pick the shortest finished path (l.601–618), comparison table |

The Graphviz/DOT pattern came from an AI chat ([[hw01-ai-transcript]]); Raymond adapted it to his successor function and added the board labels.

## Results

From [[hw01-report]] (re-run 2026-09-23 per, times vary by hundredths):

| Strategy | Path | Generated | Expanded | Time |
|---|---|---|---|---|
| A* ($g + h$) | none (cap) | 887,441 | 250,000 | 2.37 s |
| Weighted A* ($W = 10$) | 1,116 | 1,159,075 | 314,397 | 3.83 s |
| Beam $k = 500$ | 1,078 | 1,996,339 | 535,239 | 4.45 s |
| Beam $k = 5000$ | **740** | 13,759,668 | 3,650,285 | 39.05 s |

- $h(\text{start}) = 306$; A* best $h$ when stopped: 287. Hence $306 \le C^* \le 740$.
- Suboptimality bounds vs. the lower bound: $740/306 = 2.42$, $1078/306 = 3.52$, $1116/306 = 3.65$.
- Depth-1 children (Up, Left) both have $h = 307$; at depth 2 non-reversing moves give 308, the reverse move gives the start again (306).
- (Not re-run for this wiki: the script writes a `.dot` file into `raw/`, which is immutable.)

## Known issues / improvements

Report wording that does not match the code:

- **9H vs 9I**: the statement says "tile 9H does not exist" but also "only quadrant I has an empty space"; code and report remove **9I**. What to say: "I followed the figure and 'only quadrant I has an empty space'; the bottom-right cell is 9I."
- **"Rotated" should be "spiral"**: the report says each 3×3 block is "rotated", but `GOAL_INSIDE = [1,2,3,8,9,4,7,6,5]` is a clockwise **spiral**, and so is the quadrant layout `A B C / H I D / G F E`.
- **"Back to 306"**: that depth-2 node is the start state itself (tree drawn without visited set). Every first move *increases* $h$.
- **W = 10 tuning**: no trace of "other weights" tests in the code; say "tuned by hand, not from the book".
- **"True length much larger than 306"**: unproven; only $306 \le C^* \le 740$ is known.
- **Stale heap entries in weighted A\***: when a cheaper $g$ re-pushes a state, the old entry is still popped and expanded → inflated expansion count. Fix after pop: `if g_value > visited[current]: continue`.
- **Tie-breaking** prefers smaller $g$ among equal $f$ (natural tuple order); preferring larger $g$ usually reaches the goal sooner.
- **Inconsistent goal tests**: A*/weighted A* test on pop (correct for optimality); beam tests on generation.
- **Stronger heuristics** would help A*: linear conflict, disjoint pattern databases ([[russell-norvig-aima]] §3.6.3), or decomposition (solve block by block; fast, not optimal). IDA* would not help — it saves memory, not expansions.

## Related concepts

[[a-star]] · [[weighted-a-star]] · [[beam-search]] · [[heuristic-functions]] · [[state-space-and-graph-search]] · [[iterative-deepening-search]] · [[hw01-ex01-8-puzzle]] · [[search-algorithms-comparison]] · [[hw01-report]]

## Practice questions

> [!question]- Q1. Why did A* not finish if Manhattan is admissible and consistent?
> **Answer.** A* expands every node with $f < C^*$; with $h(\text{start}) = 306$ and $C^*$ hundreds of moves away, that set is astronomically large. Admissibility is what makes A* optimal — and slow. The cap of 250,000 expansions was hit after ~2.4 s.

> [!question]- Q2. Is your A* really optimal if it finishes?
> **Answer.** Yes: late goal test (h == 0 on pop), admissible and consistent heuristic, and it re-pushes states reached with a cheaper $g$.

> [!question]- Q3. Explain the incremental heuristic update in one line.
> **Answer.** A move slides one tile from `new_blank` to `blank`; only that tile's distance changes: `next_h = h - cost[tile][new_blank] + cost[tile][blank]`, $O(1)$.

> [!question]- Q4. Explain your solvability test.
> **Answer.** Each move is one transposition (flips permutation parity) and moves the blank one cell (flips its taxicab-distance parity). So the two parities stay equal along any path; a start is solvable iff parity(permutation) = parity(taxicab of blank to its goal cell). Start: 0 and 8 → both even.

> [!question]- Q5. The statement says 9H is missing. Why did you remove 9I?
> **Answer.** The statement contradicts itself: it also says only quadrant I has an empty space, and the hole starts at the bottom-right, which is 9I's position. I followed the figure.

> [!question]- Q6. Your weighted A* can push the same state twice. Does it expand it twice?
> **Answer.** Yes — stale entries are not skipped, so expansions are slightly inflated. One-line fix: after popping, `if g_value > visited[current]: continue`.

> [!question]- Q7. What is `counter` for in the heap tuples?
> **Answer.** A unique increasing number before the state: ties are broken by insertion order and Python never compares two 81-tuples (faster, deterministic).

> [!question]- Q8. How would you actually improve the result?
> **Answer.** A stronger admissible heuristic: linear conflict (+2 per reversed pair in a goal row/column), disjoint pattern databases, or problem decomposition. Also skip stale entries and tie-break toward larger $g$.
