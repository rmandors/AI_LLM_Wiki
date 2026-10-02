---
type: concept
summary: Backtracking search is depth-first search over partial CSP assignments that assigns one variable per level, checks constraints, and undoes the last choice on failure; it is the base algorithm that MRV, LCV and inference improve.
unit: 3
tags: [csp, backtracking, depth-first-search, n-queens, sudoku]
sources: ["[[russell-norvig-aima]]", "[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# Backtracking search for CSPs

**Backtracking search** solves a [[constraint-satisfaction-problems|CSP]] by building an assignment one variable at a time, depth-first. At each level it picks an unassigned variable, tries its values in turn, and recurses with each value that is consistent with the current assignment; if no value works, it returns failure so that the caller can try its next value ("backtracks") ([[russell-norvig-aima]] §5.3, Fig. 5.5). It is the recursive [[depth-first-search]] of Chapter 3, specialised to CSPs.

## How it works

```text
BACKTRACKING-SEARCH(csp): return BACKTRACK(csp, {})
BACKTRACK(csp, assignment):
    if assignment is complete: return assignment
    var = SELECT-UNASSIGNED-VARIABLE(csp, assignment) # MRV, degree
    for value in ORDER-DOMAIN-VALUES(csp, var, assignment): # LCV
        if value is consistent with assignment:
            add {var = value}
            inferences = INFERENCE(csp, var, assignment) # forward checking, MAC
            if inferences != failure:
                add inferences
                result = BACKTRACK(csp, assignment)
                if result != failure: return result
                remove inferences
            remove {var = value}
    return failure
```

([[russell-norvig-aima]] §5.3, Fig. 5.5.) The three hooks are where [[csp-heuristics]] and [[constraint-propagation]] plug in.

**Why one variable per level (commutativity).** A naive depth-limited search that may assign *any* variable at each level has branching factor $nd$, then $(n-1)d$, …, giving $n!\,d^n$ leaves although only $d^n$ complete assignments exist. Because assignment order does not matter in a CSP (commutativity), fixing one variable per node removes the $n!$ factor ([[russell-norvig-aima]] §5.3).

**Single state, undo on failure.** The algorithm keeps one assignment and modifies it in place instead of copying states ([[russell-norvig-aima]] §5.3) — exactly what `remove_queen` in [[hw01-ex03-n-queens]] and `board[row][col] = 0` in [[hw01-ex06-sudoku]] do.

**Worked example (4-queens, columns left to right, rows top to bottom; as in [[hw01-ex03-n-queens]]).** Q₀ = 0; Q₁ = 2; Q₂ has no safe row → undo Q₁; Q₁ = 3; Q₂ = 1; Q₃ has no safe row → undo Q₂; Q₂ has no other safe row → undo Q₁ → Q₁ exhausted → undo Q₀; Q₀ = 1; Q₁ = 3; Q₂ = 0; Q₃ = 2 ✓. Solution [1, 3, 0, 2] after **8 placements** (re-run of `Exercise03.py`, 2026-10-01).

### Smarter backtracking (looking backward)

- **Chronological backtracking** (Fig. 5.5) revisits the most recent decision, even if it is irrelevant (e.g. re-colouring Tasmania when SA fails) ([[russell-norvig-aima]] §5.3.3).
- **Backjumping** jumps to the most recent variable in the **conflict set** of the failed variable. Every branch pruned by backjumping is also pruned by forward checking, so it is redundant with FC/MAC ([[russell-norvig-aima]] §5.3.3).
- **Conflict-directed backjumping** propagates conflict sets upward: $\text{conf}(X_i) \leftarrow \text{conf}(X_i) \cup \text{conf}(X_j) - \{X_i\}$ ([[russell-norvig-aima]] §5.3.3).
- **Constraint learning** records a minimal conflicting assignment as a **no-good** so the same failure is not rediscovered ([[russell-norvig-aima]] §5.3.4).

## Properties

| Property | Value |
|---|---|
| Complete? | Yes for finite domains: it eventually tries every consistent partial assignment |
| Optimal? | Not applicable (no path cost) |
| Time | $O(d^n)$ worst case |
| Space | $O(n)$ extra beyond the domains: recursion depth = number of variables |
| Solution depth | always $n$ (all variables assigned); heuristics change the **width** explored, not the depth ([[hw01-report]], Ex. 6) |

## In this course

- Slides 23-24 of [[slides-02-problem-solving]] define CSPs but do not show the backtracking algorithm in text (slide 25 is image-only); the algorithm here is R&N Fig. 5.5.
- **N-Queens** ([[hw01-ex03-n-queens]]): plain backtracking, one queen per column, `is_safe` checks only the left side; first 8-queens solution [0, 4, 7, 5, 2, 6, 1, 3] after 113 placements.
- **Sudoku** ([[hw01-ex06-sudoku]]): the same skeleton with switches for MRV, LCV and forward checking; naive backtracking needs 4,208 assignments on board 1 and 335,637 on board 2.
- "Every assignment is either undone or part of the final solution", so in the Sudoku tables **assignments − backtracks = number of empty cells** (51 or 59).
- Prolog gets backtracking for free: in `queens.pl`, `select/3` is the choice point and a failing `\+ threat(...)` makes Prolog retry the next value ([[slides-xx-logic-programming-prolog]], slide 25; [[prolog-lecture-examples]]; [[backward-chaining]]).

## Common mistakes

- Copying the whole board at every node instead of undoing the change — correct but slow and memory-hungry.
- Forgetting to undo the assignment when the recursive call fails (the board keeps a wrong value).
- In Python, building the board with `[ [0] * N ] * N`: every row is the same list.
- Confusing backtracking with *backjumping*: plain backtracking always goes back exactly one level.
- Saying backtracking is "BFS-like": it is depth-first, which is why its memory is linear in $n$.

## Related

[[constraint-satisfaction-problems]] · [[csp-heuristics]] · [[constraint-propagation]] · [[depth-first-search]] · [[csp-techniques-comparison]] · [[hw01-ex03-n-queens]] · [[hw01-ex06-sudoku]] · [[prolog]] · [[backward-chaining]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Why does backtracking assign only one variable per tree level? Quantify the saving.
> **Answer.** Commutativity: the order of assignments does not change the result. Allowing any variable at any level gives $n!\,d^n$ leaves; one variable per level gives $d^n$ ([[russell-norvig-aima]] §5.3).

> [!question]- Q2. Trace backtracking on 4-queens (columns left to right, rows 0-3 top to bottom). Which solution is found first and after how many placements?
> **Answer.** [1, 3, 0, 2] (row per column), after 8 placements: (0,0), (2,1), (3,1), (1,2), then restart at (1,0), (3,1), (0,2), (2,3). See the worked example above.

> [!question]- Q3. In the Sudoku experiments, why is assignments − backtracks always equal to the number of empty cells?
> **Answer.** Each assignment is either erased later (counted as a backtrack) or survives in the final solution; the surviving ones are exactly one per empty cell (51 or 59).

> [!question]- Q4. What is a conflict set and how does backjumping use it?
> **Answer.** The set of earlier assignments that rule out values of a variable. When the variable has no legal value, backjumping returns to the most recent variable in its conflict set instead of the chronologically previous one ([[russell-norvig-aima]] §5.3.3).

> [!question]- Q5. Is backjumping useful if you already do forward checking?
> **Answer.** Simple backjumping is redundant: every branch it prunes is already pruned by forward checking. Conflict-directed backjumping and no-good learning can still help ([[russell-norvig-aima]] §5.3.3-5.3.4).
