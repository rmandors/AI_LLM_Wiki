---
type: code
summary: Walkthrough of HW01 Exercise 6 — Sudoku as a CSP solved by backtracking with switchable MRV, LCV and forward checking, compared on a 30-given and a 22-given board (MRV best; MRV+LCV even better in a re-run).
unit: 3
tags: [csp, sudoku, backtracking, mrv, lcv, forward-checking, python, hw01]
sources: ["[[hw01-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# HW01 Exercise 6 — Sudoku (`Exercise06.py`)

**Files**: `raw/HW_01/Practical_exercises/Exercise06.py` (370 lines), boards `sudoku_board1.txt` (30 givens, 51 empty; the classic Wikipedia example per ) and `sudoku_board2.txt` (22 givens, 59 empty; origin not documented).

**Problem**: solve a 9×9 Sudoku read from a text file and compare four solver versions. Modelled as a [[constraint-satisfaction-problems|CSP]]: variables = empty cells, domain {1..9}, Alldiff on every row, column and 3×3 box ([[hw01-report]], Ex. 6; [[russell-norvig-aima]] §5.2.6). Solver: [[csp-backtracking-search]] with optional [[csp-heuristics]] (MRV, LCV) and [[constraint-propagation]] (forward checking). Finally it counts all solutions with MRV to show each board has exactly one.

## Design decisions

| Decision | Why |
|---|---|
| Backtracking | Sudoku is a CSP; R&N Fig. 5.5 is the base algorithm. Same skeleton as [[hw01-ex03-n-queens]]. |
| Board from `.txt` (`0` or `.` = empty) | Solver not tied to one puzzle. |
| Naive = first empty cell in row-major order, digits 1..9 | R&N's static-ordering baseline (§5.3.1). |
| MRV, LCV, FC as boolean switches, each **alone** | Measure each idea against the same baseline. |
| Domains recomputed on the fly (`legal_values`) | Simple; no domain bookkeeping to undo. Costly per node (see Known issues). |
| Count solutions with MRV, not LCV | When enumerating all solutions, value ordering is irrelevant (R&N §5.3.1). |
| Work on a copy (`run_solver`) | Every version starts from the same board. |

## Walkthrough

- **l.15-26 `copy_board`** — manual deep copy of the list of lists (`board[:]` would share the rows).
- **l.29-51 `read_board`** — `line.replace(".", "0").split`, converts to `int`, checks 9 numbers per row and 9 rows; returns `None` on bad shape.
- **l.54-72 `print_board`** — prints with box separators, `.` for empty.
- **l.75-99 `is_consistent(board, row, col, value)`** — the constraint check: value not in the row (l.76-80), column (l.82-86) or box with origin `(row // 3) * 3, (col // 3) * 3` (l.88-97).
- **l.102-109 `legal_values`** — current domain of a cell = digits 1..9 that pass `is_consistent` (up to 9 × 27 cell reads).
- **l.112-121 `find_empty_naive`** — first `0` in row-major order, or `(-1, -1)`.
- **l.124-143 `find_empty_mrv`** — scans every empty cell, keeps the one with the smallest `len(legal_values)`; strict `<` (l.136) means **ties keep the first cell in row-major order**; no degree tie-break.
- **l.146-180 `lcv_score`** — counts empty neighbours in the row (l.150-155), column (l.157-162) and box excluding cells already counted in the row/column (l.164-178) that still accept `value`, i.e. that would **lose** it.
- **l.183-207 `order_values_lcv`** — bubble sort of the values by score, swapping values in parallel (stable: equal scores keep ascending digit order).
- **l.210-239 `forward_check_ok`** — after the digit is written, recomputes `legal_values` for every empty neighbour (row, column, box) and returns `False` if any is empty. Detects empty domains instead of maintaining reduced domains.
- **l.242-250 `make_stats`** — a dict of counters shared by all recursive calls (mutable).
- **l.253-293 `backtrack(board, stats, depth, use_mrv, use_lcv, use_fc, stop_at_first)`**:
  - l.254-255 record max depth;
  - l.257-260 choose the cell (MRV or naive);
  - l.262-268 no empty cell → count a solution, store the first; return `True` only if `stop_at_first`, otherwise `False` so the search keeps counting;
  - l.270-272 domain, optionally LCV-ordered;
  - l.274-291 for each value: write it (l.277), count an assignment (l.278), optional FC (l.280-282), recurse (l.284-287), else erase it and count a backtrack (l.289-290).
- **l.296-303 `run_solver`** — copy, stats, `time.time` around the search.
- **l.306-319 `print_stats_row`**, **l.322-357 `solve_board`** — runs the four versions, prints the naive solution and the comparison table, then counts solutions with MRV (l.352-356).
- **l.360-370 main** — boards are found next to the script via `os.path.dirname(__file__)`.

Search depth is fixed: one level per empty cell, **51** (board 1) and **59** (board 2); heuristics change the width of the tree, not its depth ([[hw01-report]], Ex. 6).

## Results

From the report (times on Raymond's laptop) ([[hw01-report]], Ex. 6; reproduced in ):

**Board 1** (30 givens, 51 empty)

| Version | Assignments | Backtracks | Max depth | Time |
|---|---|---|---|---|
| Naive backtracking | 4,208 | 4,157 | 51 | 0.024 s |
| MRV | **51** | **0** | 51 | 0.008 s |
| LCV | 2,084 | 2,033 | 51 | 0.029 s |
| Forward checking | 516 | 465 | 51 | 0.025 s |

**Board 2** (22 givens, 59 empty)

| Version | Assignments | Backtracks | Max depth | Time |
|---|---|---|---|---|
| Naive backtracking | 335,637 | 335,578 | 59 | 2.09 s |
| MRV | **4,036** | 3,977 | 59 | 1.01 s |
| LCV | 341,523 | 341,464 | 59 | 5.07 s |
| Forward checking | 153,330 | 153,271 | 59 | 7.73 s |

- Both boards have exactly **one** solution (counting mode with MRV).
- Sanity check: assignments − backtracks = number of empty cells in every row of both tables.
- Brute force for comparison: $9^{51} \approx 4.6 \times 10^{48}$ and $9^{59} \approx 2.0 \times 10^{56}$ grids ([[hw01-report]], Ex. 6).
- MRV on board 1 never guesses: at every step some cell has exactly one legal digit (a "naked single").

**Combinations not in the report** — re-run on 2026-10-01 by calling `run_solver` with other switch settings (the code itself is unchanged; assignment counts are deterministic, times are from a different machine and only comparable within this table):

| Version | Board 1 assign. / backtr. | Board 2 assign. / backtr. | Board 2 time |
|---|---|---|---|
| Naive (control) | 4,208 / 4,157 | 335,637 / 335,578 | 1.22 s |
| MRV (control) | 51 / 0 | 4,036 / 3,977 | 0.53 s |
| **MRV + FC** | 51 / 0 | 4,036 / 3,977 | 0.61 s |
| **MRV + LCV** | 51 / 0 | **181 / 122** | **0.02 s** |
| MRV + LCV + FC | 51 / 0 | 181 / 122 | 0.03 s |

MRV + FC is identical to MRV because both recompute domains from the board: if FC would reject an assignment (a neighbour with an empty domain), MRV's next scan selects that empty-domain cell and fails before any assignment. MRV + LCV is the clear winner (≈22× fewer assignments than MRV alone on board 2).

## Known issues / improvements

From a comparison of the report with the code, plus this review:

- **Forward checking recomputes domains** (`legal_values` for up to 20 neighbours, each 9 digits × 27 reads) instead of maintaining them incrementally as R&N §5.3.2 describes; this is why FC is slower than naive on board 2 despite half the assignments.
- **MRV + FC were never combined** in the report, although R&N recommends it; the report's claim that "extra forward checking does not change the story much" was an expectation, not a measurement. The re-run above confirms it for this implementation — but only because FC adds no information that MRV's full rescan does not already have.
- **MRV + LCV not tried** either; it is the best combination by far on board 2.
- **No degree tie-break** in MRV: ties go to the first cell in row-major order. On board 1, four cells tie at 1 legal value at the very start.
- **MRV cost per node**: every call rescans all empty cells × 9 digits × 27 reads; 83× fewer assignments but only ≈2× faster on board 2. Stored domains (or bitmasks per row/column/box) would make MRV and FC cheap.
- **`is_consistent` is O(27)** per digit; row/column/box bitsets would make it O(1) (general knowledge).
- **No AC-3 / MAC**, naked/hidden singles or exact-cover (Dancing Links) — the "real solver" improvements ([[constraint-propagation]]).
- **Input validation**: `read_board` checks the shape but not that digits are 0-9 or that the givens are mutually consistent; with duplicate givens the solver would still fill the empty cells and print an invalid grid (from reading the code).
- **Timing** uses one `time.time` measurement per run; times vary by machine and run (the re-run's naive time on board 2 was 1.22 s vs 2.09 s in the report). `time.perf_counter` and several repeats would be more reliable.
- Cosmetic: `def copy_board (board)` spacing; files opened without `with`.

## Related concepts

[[constraint-satisfaction-problems]] · [[csp-backtracking-search]] · [[csp-heuristics]] · [[constraint-propagation]] · [[csp-techniques-comparison]] · [[hw01-ex03-n-queens]] · [[hw01-report]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Why does MRV have 0 backtracks on board 1?
> **Answer.** On that board some empty cell always has exactly one legal digit; MRV always picks such a cell, so it never guesses wrong (verified in all 51 steps).

> [!question]- Q2. MRV uses 83× fewer assignments than naive on board 2 but is only about 2× faster. Why?
> **Answer.** Each MRV step scans every empty cell and recomputes its legal digits (up to 59 cells × 9 digits × 27 checks), so the cost per node is much higher.

> [!question]- Q3. Forward checking halves the assignments on board 2 but is the slowest version. Why, and how would you fix it?
> **Answer.** `forward_check_ok` recomputes the domain of every empty neighbour from scratch after every assignment. Maintain domains incrementally (remove the digit from neighbours, restore on undo) as in R&N §5.3.2.

> [!question]- Q4. What would happen with MRV + forward checking? Did you measure it?
> **Answer.** Not in the report. Re-running `run_solver(..., use_mrv=True, use_fc=True)` gives exactly the MRV counts (51 and 4,036): with recomputed domains, MRV already detects an empty domain on its next scan, so FC only adds overhead. With *maintained* domains, FC would make MRV cheaper rather than smarter ([[russell-norvig-aima]] §5.3.2).

> [!question]- Q5. How do you know each board has a unique solution?
> **Answer.** `solve_board` runs the solver with `stop_at_first = False` and MRV; the base case counts a solution and returns `False` so the search continues through the whole tree. It found exactly 1 for each board (l.262-268, l.352-356).

> [!question]- Q6. Why is the maximum depth the same for every version?
> **Answer.** Depth = number of assigned variables, and every solution must fill all empty cells (51 or 59). Heuristics only change how many wrong branches are explored ([[hw01-report]], Ex. 6).

> [!question]- Q7. What exactly is counted as a "backtrack"?
> **Answer.** Every time a digit is erased at l.289-290 — after a failed recursive call **or** after forward checking rejects it.
