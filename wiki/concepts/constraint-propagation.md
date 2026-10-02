---
type: concept
summary: Constraint propagation uses constraints to delete impossible values from domains (node, arc, path, k-consistency; AC-3), either before search or interleaved with it as forward checking or MAC.
unit: 3
tags: [csp, constraint-propagation, arc-consistency, ac-3, forward-checking, mac]
sources: ["[[russell-norvig-aima]]", "[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# Constraint propagation (arc consistency, AC-3, forward checking, MAC)

**Constraint propagation** is inference in a [[constraint-satisfaction-problems|CSP]]: use the constraints to remove values that cannot be part of any solution from the domains, which in turn may remove values from other domains, and so on. It can be a preprocessing step (sometimes solving the whole problem) or be interleaved with [[csp-backtracking-search]] after every assignment ([[russell-norvig-aima]] §5.2). The key idea is **local consistency** ([[russell-norvig-aima]] §5.2).

## How it works

### Levels of local consistency

| Level | Definition | Example |
|---|---|---|
| **Node** (1-consistency) | every value satisfies the variable's unary constraints | SA dislikes green → $D_{SA}$ = {red, blue} ([[russell-norvig-aima]] §5.2.1) |
| **Arc** (2-consistency) | $X_i$ is arc-consistent w.r.t. $X_j$ if every value in $D_i$ has **some** support in $D_j$ satisfying the binary constraint | $Y = X^2$ on digits → $D_X = \{0,1,2,3\}$, $D_Y = \{0,1,4,9\}$ ([[russell-norvig-aima]] §5.2.2) |
| **Path** (3-consistency for binary CSPs) | every consistent pair $\{X_i, X_j\}$ extends to any third $X_m$ | detects that Australia cannot be 2-coloured (WA, NT, SA form a triangle), which arc consistency cannot ([[russell-norvig-aima]] §5.2.3) |
| **k-consistency** | any consistent assignment to $k-1$ variables extends to a $k$-th | strongly $n$-consistent → solve with no backtracking in $O(n^2 d)$, but establishing it is exponential ([[russell-norvig-aima]] §5.2.4) |

Arc consistency does nothing for map colouring with 3 colours: for "≠" every value always has a support ([[russell-norvig-aima]] §5.2.2).

### AC-3 (R&N Fig. 5.3, Mackworth 1977)

```text
AC-3(csp):
    queue = all arcs (Xi, Xj) of the csp # each binary constraint gives two arcs
    while queue not empty:
        (Xi, Xj) = POP(queue)
        if REVISE(csp, Xi, Xj):
            if Di is empty: return false # inconsistency found
            for Xk in neighbours(Xi) - {Xj}: add (Xk, Xi) to queue
    return true
REVISE(csp, Xi, Xj):
    revised = false
    for x in Di:
        if no y in Dj satisfies the constraint (x, y): delete x from Di; revised = true
    return revised
```

**Complexity**: $n$ variables, domain size ≤ $d$, $c$ binary constraints. Each arc $(X_k, X_i)$ re-enters the queue at most $d$ times (once per deleted value of $X_i$), and REVISE costs $O(d^2)$ → $O(cd^3)$ worst case ([[russell-norvig-aima]] §5.2.2).

**Worked example.** Variables X, Y, Z with domains {1, 2, 3} and constraints X < Y, Y < Z.
- REVISE(X, Y): X = 3 has no larger Y → $D_X = \{1, 2\}$.
- REVISE(Y, X): Y = 1 has no smaller X → $D_Y = \{2, 3\}$; REVISE(Y, Z): Y = 3 has no larger Z → $D_Y = \{2\}$.
- REVISE(Z, Y): Z must exceed 2 → $D_Z = \{3\}$; re-queued REVISE(X, Y): X must be below 2 → $D_X = \{1\}$.
- Result: X = 1, Y = 2, Z = 3 — AC-3 alone solved the CSP.

### Global constraints

- **Alldiff**: if $m$ variables share only $n < m$ possible values, the constraint fails. Simple algorithm: repeatedly remove singleton variables and delete their value from the others ([[russell-norvig-aima]] §5.2.5). This catches {WA = red, NSW = red}: SA, NT, Q all reduce to {green, blue} — 3 variables, 2 values.
- **Atmost / resource constraints** and **bounds propagation** for large integer domains, e.g. $F_1 + F_2 = 420$ with $D_1 = [0,165]$, $D_2 = [0,385]$ → $D_1 = [35,165]$, $D_2 = [255,385]$ ([[russell-norvig-aima]] §5.2.5).
- **Sudoku**: with Alldiff expanded to binary "≠", AC-3 alone fixes E6 = 4, then I6 = 7, then A6 = 1, and solves the easy puzzle of Fig. 5.4 completely; harder puzzles need PC-2 (255,960 path constraints) or strategies like **naked triples** ([[russell-norvig-aima]] §5.2.6).

### Interleaving inference with search

- **Forward checking (FC)**: after assigning $X$, for every unassigned neighbour $Y$, delete from $D_Y$ the values inconsistent with $X$'s value; if a domain becomes empty, backtrack now ([[russell-norvig-aima]] §5.3.2). It makes only the arcs *into* the new assignment consistent.
- **MAC (Maintaining Arc Consistency)**: after assigning $X_i$, run AC-3 starting with the arcs $(X_j, X_i)$ for unassigned neighbours $X_j$, and keep propagating recursively. MAC is **strictly more powerful** than FC ([[russell-norvig-aima]] §5.3.2).
- **Worked example (R&N Fig. 5.7).** FC on Australia: WA = red removes red from NT, SA. Q = green removes green from NT, SA, NSW → NT = {blue}, SA = {blue}. V = blue removes blue from NSW, SA → **SA empty → backtrack**. FC missed that already after Q = green, NT and SA (neighbours) both had only blue; MAC would have caught it one step earlier ([[russell-norvig-aima]] §5.3.2).

## Properties

| Method | When | Power | Cost |
|---|---|---|---|
| Node consistency | preprocessing | unary only | $O(nd)$ |
| AC-3 | preprocessing or inside MAC | arc consistency | $O(cd^3)$ |
| PC-2 / path consistency | preprocessing | > arc | much higher |
| Forward checking | after each assignment | arcs into the new variable only | cheap, $O(d)$ per neighbour with stored domains |
| MAC | after each assignment | full arc consistency | more than FC, usually worth it |

The propagated CSP is **equivalent** to the original (same solutions) but has smaller domains ([[russell-norvig-aima]] §5.2.2).

## In this course

- Slide 24 of [[slides-02-problem-solving]]: "Constraint propagation: domains can be reduced before assignment — Forward Checking, Arc Consistency, Minimum Remaining Values." See the contradiction note on [[constraint-satisfaction-problems]]: MRV is an ordering heuristic ([[csp-heuristics]]), and FC acts *during* search. **Slide 25 is image-only.**
- **HW01 Sudoku** ([[hw01-ex06-sudoku]]) implements forward checking as `forward_check_ok`: after writing a digit, it **recomputes** `legal_values` of every empty neighbour and fails if one is empty. Same pruning as the book, but it does not maintain reduced domains, so every check costs up to 20 neighbours × 9 digits × 27 cell reads ( Q3).
- Results: FC cuts assignments from 4,208 to 516 (board 1) and from 335,637 to 153,330 (board 2), but is **slower** on board 2 (7.73 s vs 2.09 s) ([[hw01-report]], Ex. 6).
- Re-run 2026-10-01 (not in the report): MRV + FC gives **exactly** the MRV numbers (51 / 4,036 assignments). With recomputed domains, MRV already notices an empty domain on its next scan and fails before any assignment, so FC adds only overhead. The report's sentence "extra forward checking does not change the story much" turns out to be right, although it was not measured at the time (row 6).
- AC-3 / MAC are not implemented in HW01; they are the suggested "real solver" improvement.

## Common mistakes

- Thinking arc consistency guarantees a solution exists. It only removes unsupported values; the 2-colour Australia map is arc-consistent but unsolvable.
- Forgetting to re-queue the arcs $(X_k, X_i)$ after $D_i$ shrinks, or re-queueing $(X_j, X_i)$ needlessly.
- Saying "AC-3 is $O(cd^2)$": REVISE is $O(d^2)$, but each arc can be revisited $d$ times → $O(cd^3)$.
- Confusing FC with MAC: FC does **not** propagate further when a neighbour's domain shrinks.
- Claiming FC must be faster in clock time. Fewer nodes, but more work per node (as in [[hw01-ex06-sudoku]]).

## Related

[[constraint-satisfaction-problems]] · [[csp-backtracking-search]] · [[csp-heuristics]] · [[csp-techniques-comparison]] · [[hw01-ex06-sudoku]] · [[unit-03-csp-review]]

## Practice questions

> [!question]- Q1. Domains $D_X = D_Y = \{1,2,3,4\}$, constraint $X = Y + 2$. Make the arc (X, Y) and then (Y, X) consistent.
> **Answer.** (X, Y): X needs some Y with Y = X − 2 ∈ {1..4} → $D_X = \{3, 4\}$. (Y, X): Y needs X = Y + 2 ∈ {3, 4} → $D_Y = \{1, 2\}$.

> [!question]- Q2. Why is the complexity of AC-3 $O(cd^3)$?
> **Answer.** There are $2c$ arcs; an arc $(X_k, X_i)$ is re-added only when $D_i$ loses a value, at most $d$ times; each REVISE compares up to $d \times d$ value pairs. $O(c \cdot d \cdot d^2)$ ([[russell-norvig-aima]] §5.2.2).

> [!question]- Q3. Can arc consistency prove that Australia has no 2-colouring? What can?
> **Answer.** No: for "≠" with {red, blue} every value always has a support. Path consistency can: making {WA, SA} path-consistent w.r.t. NT eliminates both consistent pairs, so no solution ([[russell-norvig-aima]] §5.2.3).

> [!question]- Q4. Run forward checking on Australia: WA = red, Q = green, V = blue. What happens?
> **Answer.** After WA = red: NT, SA ∈ {green, blue}. After Q = green: NT = {blue}, SA = {blue}, NSW ∈ {red, blue}. After V = blue: NSW = {red}, SA = {} → empty domain → backtrack immediately ([[russell-norvig-aima]] §5.3.2, Fig. 5.7).

> [!question]- Q5. What does MAC detect that forward checking misses in the previous question?
> **Answer.** After Q = green, NT and SA both have only {blue} but are neighbours, so the arc (NT, SA) is inconsistent. MAC propagates from the changed domains and fails right there; FC only checks arcs into the newly assigned variable ([[russell-norvig-aima]] §5.3.2).

> [!question]- Q6. In HW01, forward checking halved the assignments on board 2 but took 3.7× longer than naive. Explain.
> **Answer.** `forward_check_ok` recomputes the domain of every empty neighbour from scratch after each assignment (up to 20 cells × 9 digits × 27 checks), instead of maintaining domains incrementally as in the book. Fewer nodes, much higher cost per node.
