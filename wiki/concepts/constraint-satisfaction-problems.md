---
type: concept
summary: A CSP is a problem with a factored state (variables X, domains D, constraints C), solved by finding a complete and consistent assignment; examples are map colouring, N-queens and Sudoku.
unit: 3
tags: [csp, constraints, factored-representation, sudoku, n-queens]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Constraint satisfaction problems (CSPs)

A **constraint satisfaction problem** is a problem whose states are not black boxes but have internal structure: a set of **variables**, each of which must get a **value** from its **domain**, subject to **constraints** on which combinations are allowed. It is solved when every variable has a value and no constraint is violated ([[slides-02-problem-solving]], slide 23; [[russell-norvig-aima]] Ch. 5 intro). This is a **factored** representation, in contrast with the atomic states of ordinary search ([[state-representation]]).

## How it works

A CSP has three components ([[slides-02-problem-solving]], slide 24; [[russell-norvig-aima]] §5.1):

- $\mathcal{X} = \{X_1, \dots, X_n\}$ — variables ("what must be assigned");
- $\mathcal{D} = \{D_1, \dots, D_n\}$ — a domain of allowed values for each variable;
- $\mathcal{C}$ — constraints; each is a pair ⟨*scope*, *rel*⟩, e.g. $\langle (X_1, X_2), X_1 > X_2 \rangle$ or the explicit set $\{(3,1),(3,2),(2,1)\}$.

Vocabulary ([[russell-norvig-aima]] §5.1; [[slides-02-problem-solving]], slide 24):

| Term | Meaning |
|---|---|
| Consistent (legal) assignment | violates no constraint |
| Complete assignment | every variable has a value |
| Solution | complete **and** consistent assignment |
| Partial solution | consistent partial assignment |
| Constraint graph | nodes = variables, edges = binary constraints |

**Constraint types** ([[russell-norvig-aima]] §5.1.3): *unary* (one variable, e.g. SA ≠ green), *binary* (two variables, e.g. SA ≠ NSW), *higher-order/global* (any number, e.g. **Alldiff**). Every finite-domain constraint can be reduced to binary ones with auxiliary variables (or the dual-graph transformation), but global constraints are easier to write and admit specialised inference. *Preference* constraints turn the problem into a **constrained optimization problem (COP)** ([[russell-norvig-aima]] §5.1.3; [[optimization-problems]]).

**Domains**: discrete finite (map colouring, Sudoku, 8-queens), discrete infinite (start times without a deadline; needs implicit constraints), continuous (linear programming, solvable in polynomial time) ([[russell-norvig-aima]] §5.1.3).

### Standard examples

| Problem | Variables | Domains | Constraints |
|---|---|---|---|
| Australia map colouring | WA, NT, Q, NSW, V, SA, T | {red, green, blue} | 9 binary "≠" between neighbours ([[russell-norvig-aima]] §5.1.1) |
| 8-queens | $Q_1..Q_8$ = queen in column $i$ | rows {1..8} | no two in the same row or diagonal ([[russell-norvig-aima]] §5.1.3) |
| Sudoku | 81 squares (or only the empty ones) | {1..9}; givens have singleton domains | 27 Alldiff (9 rows, 9 columns, 9 boxes) ([[russell-norvig-aima]] §5.2.6) |
| Job-shop scheduling | task start times | {0..30} minutes | precedence $T_1 + d_1 \le T_2$, disjunctive (no overlap) ([[russell-norvig-aima]] §5.1.2) |
| School timetable | classes | time slots | e.g. "sports cannot be scheduled after lunch" ([[slides-02-problem-solving]], slide 23) |

## Properties

- **Why formulate as a CSP?** Natural representation; mature fast solvers; and pruning: once a partial assignment violates a constraint, all its refinements are discarded at once. In Australia, after SA = blue the five neighbours have $2^5 = 32$ instead of $3^5 = 243$ combinations, an 87% reduction ([[russell-norvig-aima]] §5.1.1).
- The actions and transition model follow from the problem description — no domain-specific successor function is needed ([[russell-norvig-aima]] Ch. 5 intro).
- **Complexity**: solving a general finite-domain CSP is **NP-complete**; tree-structured CSPs are solvable in $O(nd^2)$ ([[russell-norvig-aima]] §5.1, §5.5).
- No path cost: "optimal" does not apply to plain CSP solutions.

**Solution methods** (each has its own page):
1. [[constraint-propagation]] — inference that shrinks domains (node, arc, path consistency; AC-3).
2. [[csp-backtracking-search]] — depth-first search over partial assignments.
3. [[csp-heuristics]] — MRV, degree, LCV, and forward checking to guide/prune backtracking.
4. Local search — **min-conflicts** over complete assignments ([[russell-norvig-aima]] §5.4; see [[csp-heuristics]] and [[hill-climbing]]).
5. Problem structure — independent subproblems, tree-CSP solver, cutset conditioning, tree decomposition ([[russell-norvig-aima]] §5.5).

## In this course

- Slides 23-24 of [[slides-02-problem-solving]] (inside the problem-solving deck, so tagged unit 3): states with internal structure, Sudoku and school-schedule examples, the X/D/C components, consistent vs complete assignment, and a list of techniques ("Forward Checking, Arc Consistency, Minimum Remaining Values"). **Slide 25 is image-only** (no text extracted).
- HW01 Exercise 3, N-Queens as a CSP (variables = columns, domain = rows) → [[hw01-ex03-n-queens]] ([[hw01-report]], Ex. 3).
- HW01 Exercise 6, Sudoku as a CSP (variables = empty cells, domain {1..9}, all-different on rows, columns, boxes) → [[hw01-ex06-sudoku]] ([[hw01-report]], Ex. 6).
- The Prolog deck solves N-queens declaratively with a permutation representation → [[prolog-lecture-examples]] ([[slides-xx-logic-programming-prolog]], slides 25-26).
- Comparison of techniques with HW numbers: [[csp-techniques-comparison]]; cheat sheet: [[unit-03-csp-review]].

> [!warning] Contradiction
> Slide 24 of [[slides-02-problem-solving]] lists Minimum Remaining Values under "Constraint propagation: domains can be reduced before assignment". In R&N, MRV is a **variable-ordering heuristic** for backtracking (§5.3.1), not propagation, and forward checking is inference done **during** search after each assignment (§5.3.2). Only arc consistency (AC-3) is typically run before search (§5.2). See [[csp-heuristics]] and [[constraint-propagation]].

## Common mistakes

- Calling Sudoku or N-queens a shortest-path problem: there is no path cost; any solution is as good as any other.
- Forgetting that a *complete* assignment is not necessarily a *solution* (it must also be consistent).
- Treating the givens of a Sudoku as variables with full domains — they have singleton domains (or are left out of the variable set, as in [[hw01-ex06-sudoku]]).
- Using the US-edition chapter numbers: in the Global Edition CSPs are **Chapter 5** (intro).

## Related

[[csp-backtracking-search]] · [[csp-heuristics]] · [[constraint-propagation]] · [[csp-techniques-comparison]] · [[hw01-ex03-n-queens]] · [[hw01-ex06-sudoku]] · [[state-representation]] · [[problem-formulation]] · [[prolog]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Formulate 4-colouring of a map with regions A, B, C where A borders B and B borders C, as a CSP.
> **Answer.** $\mathcal X = \{A, B, C\}$; $D_i = \{1,2,3,4\}$; $\mathcal C = \{A \ne B, B \ne C\}$. Constraint graph: the path A–B–C (a tree, so it is solvable without backtracking after directional arc consistency).

> [!question]- Q2. What is the difference between a complete assignment, a consistent assignment and a solution?
> **Answer.** Complete = all variables assigned; consistent = no constraint violated; solution = both ([[russell-norvig-aima]] §5.1).

> [!question]- Q3. How many Alldiff constraints does Sudoku have, and how many variables are in each?
> **Answer.** 27 (9 rows + 9 columns + 9 boxes), each over 9 squares ([[russell-norvig-aima]] §5.2.6).

> [!question]- Q4. In Australia, how much does assigning SA = blue shrink the joint space of its five neighbours?
> **Answer.** From $3^5 = 243$ to $2^5 = 32$ combinations, an 87% reduction ([[russell-norvig-aima]] §5.1.1).

> [!question]- Q5. Why does the CSP formulation of 8-queens use one variable per column?
> **Answer.** It builds the "one queen per column" constraint into the representation, so only rows and diagonals need explicit constraints; the space drops from $\binom{64}{8}$ placements to $8^8$ ([[russell-norvig-aima]] §5.1.3).

> [!question]- Q6. Is solving CSPs easy in general? What structure makes it easy?
> **Answer.** No — finite-domain CSPs are NP-complete in general. Tree-structured constraint graphs are solvable in $O(nd^2)$ (topological order + directional arc consistency), and independent components can be solved separately ([[russell-norvig-aima]] §5.1, §5.5).
