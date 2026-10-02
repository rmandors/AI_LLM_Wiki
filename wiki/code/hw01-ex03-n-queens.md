---
type: code
summary: Walkthrough of HW01 Exercise 3 — N-Queens as a CSP solved by plain recursive backtracking, one queen per column, first 8-queens solution [0,4,7,5,2,6,1,3] after 113 placements.
unit: 3
tags: [csp, backtracking, n-queens, python, hw01]
sources: ["[[hw01-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# HW01 Exercise 3 — N-Queens (`Exercise03.py`)

**File**: `raw/HW_01/Practical_exercises/Exercise03.py` (108 lines; docstring title "Exercise 03: 8-Queens").

**Problem**: place N queens on an N×N board so that no two attack each other (same row, column or diagonal). The user types N; the program prints the first solution found or reports that none exists. Modelled as a [[constraint-satisfaction-problems|CSP]] following R&N §5.1.3: variables = columns, domain of each column = the N rows, constraints = no two queens in the same row or diagonal ([[hw01-report]], Ex. 3). Solved with [[csp-backtracking-search]].

## Design decisions

| Decision | Why |
|---|---|
| Backtracking, not BFS / A* | No path cost — any legal placement is a solution; depth is known (N), so depth-first uses only $O(N)$ extra memory. |
| One queen per column | Removes the column constraint by construction; the space drops from $\binom{64}{8}$ to $8^8$ before pruning. |
| `is_safe` looks only left | Invariant: when column `col` is filled, only columns `0..col-1` hold queens. |
| Stop at the first solution | The task is to solve, not to count (8-queens has 92 solutions, 12 up to symmetry). |
| No MRV / min-conflicts | Plain backtracking is what the exercise targets, and N = 8 is instant. |
| 2-D board of 0/1 | Easy to print and to read; a 1-D `queens[col] = row` would be more compact. |
| N from `input` | Shows the solver is general (N = 1 solvable, 2 and 3 not, every N ≥ 4 solvable). |

## Walkthrough

- **l.12-19 `create_board(N_QUEENS)`** — builds an N×N list of lists of zeros; a new `row` list is created inside the loop, avoiding the `[ [0] * N ] * N` aliasing bug.
- **l.22-44 `print_board`** — ASCII board with `Q` cells, explicit `while` loops.
- **l.46-51 `place_queen` / `remove_queen`** — write 1 / 0 in place; this is the "modify one state and undo" style of R&N Fig. 5.5.
- **l.54-78 `is_safe(board, row, col)`** — three checks, all to the left:
  - l.55-58 same row, columns `0..col-1`;
  - l.60-67 upper-left diagonal (`r-1, c-1` until the edge);
  - l.69-76 lower-left diagonal (`r+1, c-1`).
- **l.81-94 `backtrack(board, col)`** — base case `col == len(board)` → success (l.82-83). Otherwise for each row (l.85): if safe, place (l.87), recurse on `col + 1` (l.88), propagate `True` (l.90-91), else **remove the queen** (l.92) and try the next row. If no row works, return `False` (l.94) so the caller moves its own queen.
- **l.97-108 main** — `int(input(...))`, build the board, call `backtrack(board, 0)`, print the board or "No solution found".

The recursion depth equals the current column; a solution is found at depth N. The call stack *is* the current path of the search tree.

## Results

Re-run 2026-10-01 by wrapping `place_queen` with a counter (identical to for N = 8):

| N | Solution (row of the queen in each column, 0-indexed) | Queen placements |
|---|---|---|
| 1 | [0] | 1 |
| 2 | none | 2 |
| 3 | none | 5 |
| 4 | [1, 3, 0, 2] | 8 |
| 8 | **[0, 4, 7, 5, 2, 6, 1, 3]** | **113** |

[0, 4, 7, 5, 2, 6, 1, 3] is the lexicographically first 8-queens solution, as expected because rows are tried top to bottom.

> [!tip] Link to the Prolog version
> The Prolog deck's `queens.pl` uses a **permutation** representation (`select/3` picks the next row, `\+ threat/2` checks only diagonals) and its first answer is `Qs = [4,2,7,3,6,8,5,1]` ([[slides-xx-logic-programming-prolog]], slides 25-26; [[prolog-lecture-examples]]). That list is exactly the **reverse** of this program's solution in 1-indexed form, [1, 5, 8, 6, 3, 7, 2, 4]: Prolog tries values in the same ascending order but builds the list by prepending to `SafeQs`. Both enumerate the same search tree via chronological backtracking ([[prolog]], [[backward-chaining]]). The deck's solution-count table (N = 4: 2, 6: 4, 8: 92) is a good check for an "all solutions" variant.

## Known issues / improvements

- **`is_safe` is $O(N)$** per call (row scan + two diagonal walks). Use three boolean arrays — rows, "/" diagonals (`r + c`), "\" diagonals (`r - c + N - 1`) — for $O(1)$ checks, or a 1-D `queens[col]` with `abs(r1 - r2) == abs(c1 - c2)`.
- **No heuristics**: always the leftmost column, always top-down rows. MRV (column with fewest safe rows) or forward checking would prune more; for large N, **min-conflicts** solves a million queens in ~50 steps ([[russell-norvig-aima]] §5.4; [[csp-heuristics]]).
- **Stops at the first solution**; counting all would need `count += 1` at the base case and no early return.
- **No input validation**: a letter raises `ValueError`; N = 0 prints an empty board as a "solution"; negative N silently gives an empty board.
- **Recursion depth = N**: Python's default limit (~1000) would stop very large N, though plain backtracking becomes too slow long before that (general knowledge).
- Docstring says "8-Queens" while the program is general N-Queens (cosmetic).
- Complexity: worst case about $O(N!)$ placements × $O(N)$ per `is_safe`.

## Related concepts

[[constraint-satisfaction-problems]] · [[csp-backtracking-search]] · [[csp-heuristics]] · [[depth-first-search]] · [[prolog-lecture-examples]] · [[hw01-ex06-sudoku]] · [[hw01-report]] · [[csp-techniques-comparison]]

## Practice questions

> [!question]- Q1. Why don't you check the column or the right side of the board in `is_safe`?
> **Answer.** There is exactly one queen per column by construction, and columns to the right of `col` are still empty when `is_safe` is called.

> [!question]- Q2. Is your algorithm optimal? Is it complete?
> **Answer.** "Optimal" does not apply — no path cost. It is complete: it tries every safe row in order, so if a solution exists it finds one, and for N = 2, 3 it correctly reports none ([[hw01-report]], Ex. 3).

> [!question]- Q3. What does line 92 (`remove_queen`) do and what happens if you delete it?
> **Answer.** It undoes the placement when the recursive call fails, restoring the board for the next row. Without it, failed queens stay on the board, later `is_safe` calls see phantom queens, and the solver reports wrong failures or wrong boards.

> [!question]- Q4. How would you make `is_safe` O(1)?
> **Answer.** Keep `used_row[r]`, `used_diag1[r + c]`, `used_diag2[r - c + N - 1]`; set them on place, clear them on remove; a square is safe iff all three are False.

> [!question]- Q5. Why does it take 113 placements for N = 8 and only 8 for N = 4?
> **Answer.** Placements count every tentative queen, including those later removed. For N = 4 the search fails only twice before succeeding; for N = 8 the first-column choice 0 is right, but deeper columns need many retries before reaching [0, 4, 7, 5, 2, 6, 1, 3] (re-run 2026-10-01).

> [!question]- Q6. How is this formulation related to the "incremental" vs "complete-state" formulations?
> **Answer.** It is incremental: start from an empty board and add one queen at a time to the leftmost empty column. The complete-state formulation (all queens on the board, move one) is what hill climbing and min-conflicts use ([[hill-climbing]]).
