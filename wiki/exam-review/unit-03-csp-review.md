---
type: exam-review
summary: Cheat sheet for constraint satisfaction problems (taught in unit 3) — definitions, backtracking, MRV/degree/LCV, forward checking, AC-3/MAC, min-conflicts, HW01 N-Queens and Sudoku numbers, traps and 12 practice questions.
unit: 3
tags: [csp, exam-review, backtracking, mrv, lcv, forward-checking, ac-3]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Unit 3 review — Constraint satisfaction problems

Companion to [[unit-03-search-review]] (path search) and part of [[midterm-01-review]]. Slides: [[slides-02-problem-solving]] slides 23-24 (slide 25 image-only). Book: [[russell-norvig-aima]] Ch. 5 (**Global Edition** numbering; US edition = Ch. 6).

## Definitions

- **CSP** = ⟨X, D, C⟩: variables, domains, constraints ⟨scope, rel⟩ ([[constraint-satisfaction-problems]]).
- **Consistent** = no violation; **complete** = all assigned; **solution** = both.
- **Factored** state (variables with values) vs **atomic** black box in ordinary search ([[state-representation]]).
- Constraint types: unary, binary, global (Alldiff), preference (→ COP).
- **Constraint graph**: nodes = variables, edges = binary constraints.
- General CSPs are **NP-complete**; tree-structured CSPs are $O(nd^2)$.

## Algorithms in one line each

| Technique | One-liner | Page |
|---|---|---|
| Backtracking | DFS, one variable per level, try values, undo on failure | [[csp-backtracking-search]] |
| MRV | variable with fewest legal values ("fail-first") | [[csp-heuristics]] |
| Degree | variable with most constraints on unassigned vars (tie-break) | [[csp-heuristics]] |
| LCV | value that rules out fewest neighbour options ("fail-last") | [[csp-heuristics]] |
| Forward checking | after X = v, delete inconsistent values from X's unassigned neighbours; empty → backtrack | [[constraint-propagation]] |
| AC-3 | queue of arcs; REVISE; on change re-queue $(X_k, X_i)$ | [[constraint-propagation]] |
| MAC | AC-3 after each assignment, starting from arcs into it | [[constraint-propagation]] |
| Backjumping / CBJ | go back to the culprit in the conflict set | [[csp-backtracking-search]] |
| Min-conflicts | complete assignment; move a conflicted var to its min-conflict value | [[csp-heuristics]] |

## Formulas and complexity

| Quantity | Value |
|---|---|
| Leaves without commutativity | $n!\,d^n$ |
| Leaves with one variable per level | $d^n$ |
| Backtracking time / space | $O(d^n)$ / $O(n)$ |
| AC-3 | $O(cd^3)$ ($c$ arcs, REVISE $O(d^2)$, each arc ≤ $d$ times) |
| Strongly $n$-consistent → solve | $O(n^2 d)$ (but establishing it is exponential) |
| Tree-structured CSP | $O(nd^2)$ |
| Cutset of size $c$ | $O(d^c \cdot (n-c)d^2)$ |
| Independent subproblems of size $c$ | $O(d^c \, n/c)$ instead of $O(d^n)$ |
| Australia after SA = blue | $3^5 = 243 \to 2^5 = 32$ (−87%) |
| Sudoku | 81 vars, 27 Alldiff; brute force $9^{51} \approx 4.6\times10^{48}$ (board 1) |

(All from [[russell-norvig-aima]] §5.1-5.5 except the Sudoku brute-force figure, [[hw01-report]] Ex. 6.)

## Must-know facts

- Variable ordering: **fail-first** (MRV); value ordering: **fail-last** (LCV). Value ordering is irrelevant when enumerating **all** solutions.
- FC ⊂ MAC; backjumping is redundant with FC/MAC.
- Arc consistency does nothing for "≠" with ≥ 2 values per domain (3-colouring Australia); path consistency proves 2-colouring impossible.
- AC-3 alone solves easy Sudokus (E6 = 4 → I6 = 7 → A6 = 1 …) ([[russell-norvig-aima]] §5.2.6).
- Min-conflicts: ~50 steps for a million queens; incomplete.
- Optimality does not apply to CSPs (no path cost); depth of every solution = number of variables.

## HW01 numbers to memorise

**N-Queens** ([[hw01-ex03-n-queens]]): variables = columns, `is_safe` looks only left; first 8-queens solution **[0, 4, 7, 5, 2, 6, 1, 3]** after **113** placements; 92 solutions total (12 fundamental); none for N = 2, 3. Prolog version's first answer [4,2,7,3,6,8,5,1] is the same solution reversed and 1-indexed ([[prolog-lecture-examples]]).

**Sudoku** ([[hw01-ex06-sudoku]]): depth 51 / 59 (= empty cells).

| | Naive | MRV | LCV | FC | MRV+LCV (re-run) |
|---|---|---|---|---|---|
| Board 1 | 4,208 | **51** (0 bt) | 2,084 | 516 | 51 |
| Board 2 | 335,637 | **4,036** | 341,523 | 153,330 | **181** |

Assignments − backtracks = number of empty cells. MRV + FC = MRV exactly (re-run 2026-10-01). Both boards have one solution.

## Common traps

- MRV is **not** constraint propagation (slide 24 lists it there; see the contradiction note on [[constraint-satisfaction-problems]]).
- "Fewer nodes ⇒ faster" is false: HW01 FC had half the nodes of naive but 3.7× the time.
- Forward checking ≠ arc consistency of the whole graph; it checks only arcs into the new variable.
- AC-3's queue re-adds $(X_k, X_i)$ for neighbours $X_k \ne X_j$ — not $(X_i, X_k)$.
- Arc-consistent ≠ solvable.
- Chapter numbers: CSPs are Ch. 5 in the Global Edition.

## Practice questions

> [!question]- Q1. Formulate the 8-queens problem as a CSP.
> **Answer.** Variables $Q_1..Q_8$ (queen in column $i$), domains {1..8} (row), constraints: for $i \ne j$, $Q_i \ne Q_j$ and $|Q_i - Q_j| \ne |i - j|$ ([[russell-norvig-aima]] §5.1.3).

> [!question]- Q2. Why does backtracking fix one variable per tree level? What does this save?
> **Answer.** Commutativity: the order of assignments does not matter, so the $n!$ factor of the naive formulation ($n!\,d^n$ leaves) disappears, leaving $d^n$ ([[russell-norvig-aima]] §5.3).

> [!question]- Q3. Australia: WA = red, NT = green. Which variable does MRV choose next, and which colour does LCV prefer for Q if we instead pick Q?
> **Answer.** MRV: SA (only blue left). For Q: red, because blue would remove SA's last value ([[russell-norvig-aima]] §5.3.1).

> [!question]- Q4. Which variable does the degree heuristic choose first in Australia and why?
> **Answer.** SA, with degree 5 (borders WA, NT, Q, NSW, V); the others have degree 2-3 and T has 0 ([[russell-norvig-aima]] §5.3.1).

> [!question]- Q5. Run AC-3 on X < Y < Z with domains {1, 2, 3}.
> **Answer.** X loses 3, Y loses 1 and 3, Z loses 1 and 2, then X loses 2 → X = 1, Y = 2, Z = 3. AC-3 solved it with no search ([[constraint-propagation]]).

> [!question]- Q6. Give the complexity of AC-3 and justify it.
> **Answer.** $O(cd^3)$: each of the $c$ arcs is re-queued at most $d$ times (once per deleted value) and REVISE checks $d^2$ pairs ([[russell-norvig-aima]] §5.2.2).

> [!question]- Q7. Forward checking on Australia with WA = red, Q = green, V = blue: where does it fail? What would MAC have done?
> **Answer.** After V = blue, SA's domain becomes empty → backtrack. MAC fails one step earlier: after Q = green, NT and SA both have only blue and are neighbours ([[russell-norvig-aima]] §5.3.2).

> [!question]- Q8. In HW01, why did MRV have 0 backtracks on board 1 but 3,977 on board 2?
> **Answer.** Board 1 always has a cell with a single legal digit (naked single), so MRV never guesses. Board 2 (22 givens) reaches states where the tightest cell has 2+ candidates, so MRV must guess and sometimes undo.

> [!question]- Q9. Why was forward checking the slowest version on board 2 though it used fewer nodes than naive?
> **Answer.** It recomputes the legal values of up to 20 neighbours after each assignment instead of maintaining domains; per-node cost dominates.

> [!question]- Q10. Why does LCV not matter when counting all solutions?
> **Answer.** Every value of every variable must be explored anyway, so the order of values does not change the total work ([[russell-norvig-aima]] §5.3.1).

> [!question]- Q11. Describe min-conflicts and state one advantage and one drawback.
> **Answer.** Start from a complete assignment; repeatedly pick a random conflicted variable and set it to the value with fewest conflicts. Advantage: extremely fast on dense-solution problems (million queens ≈ 50 steps) and good for online repair. Drawback: incomplete, can stall on plateaus ([[russell-norvig-aima]] §5.4).

> [!question]- Q12. A constraint graph is a tree with $n = 10$ variables and $d = 3$. What is the cost of solving it, and how?
> **Answer.** $O(nd^2) = O(90)$ value-pair checks: topological sort from any root, make each (parent, child) arc consistent from the leaves up, then assign top-down without backtracking ([[russell-norvig-aima]] §5.5).

## Weak spots

*(To be filled during exam prep sessions.)*
