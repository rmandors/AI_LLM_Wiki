---
type: exam-review
summary: Dense unit-3 cheat sheet on search — problem formulation, graph vs tree search, b/d/m criteria, properties of every algorithm, heuristic properties (admissible, consistent, dominance, relaxed problems, b*), early vs late goal test, HW01 numbers, traps and 14 practice questions.
unit: 3
tags: [exam-review, search, heuristics, midterm-1]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]", "[[discussion-01-astar-vs-dijkstra]]"]
updated: 2026-10-01
---

# Unit 3 review — Search

Part of [[midterm-01-review]]. CSPs (also unit 3) have their own sheet: [[unit-03-csp-review]]. Games: [[unit-04-games-review]].

## 1. Formulation → [[problem-formulation]]

- Problem-solving agent: goal-based; **formulate → search → execute**; environment observable, deterministic, discrete, static (+ known) → open-loop plan; solution = **sequence of actions** ([[slides-02-problem-solving]], slide 2).
- Five components: **initial state, actions $\text{ACTIONS}(s)$, transition model $\text{RESULT}(s,a)$, goal test, action cost $c(s,a,s')$**; first three define the **state space** (slide 3).
- Path cost is additive; optimal solution = lowest path cost; costs > 0 (≥ ε).

## 2. State space vs search tree → [[state-space-and-graph-search]]

- State space: graph, one node per state, implicit, explored progressively (slide 4). Search tree: one node per *path*; repeated states (cycles, redundant paths) (slide 5).
- Node = (STATE, PARENT, ACTION, PATH-COST $g$). Frontier = generated, not expanded. Reached = frontier ∪ expanded ("explored set" on slides).
- **Graph search** = keep reached table, never re-add a state unless cheaper. **Tree-like search** = no table (less memory, redundant work, loops). Middle way: cycle check along the current path.
- 8-puzzle: $9!/2 = 181{,}440$ reachable states; 15-puzzle $16!/2 > 10^{13}$.

## 3. Criteria → [[uninformed-search]]

Completeness · cost optimality · time · space; measured with **$b$** (branching factor), **$d$** (depth of shallowest solution), **$m$** (max depth), plus $C^*$, $\epsilon$, $\ell$ ([[russell-norvig-aima]] §3.3.4).

## 4. Properties table → [[search-algorithms-comparison]]

| Algorithm | Frontier / $f$ | Complete | Optimal | Time | Space |
|---|---|---|---|---|---|
| BFS | FIFO | Yes | equal costs | $O(b^d)$ | $O(b^d)$ |
| UCS (Dijkstra) | PQ on $g$ | Yes (ε > 0) | Yes | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | same |
| DFS (tree) | LIFO | No (graph: finite only) | No | $O(b^m)$ | $O(bm)$ |
| DLS | LIFO ≤ $\ell$ | No | No | $O(b^\ell)$ | $O(b\ell)$ |
| IDS | DLS $\ell=0,1,…$ | Yes | equal costs | $O(b^d)$ | $O(bd)$ |
| Bidirectional | 2 frontiers | Yes | equal costs/UCS | $O(b^{d/2})$ | $O(b^{d/2})$ |
| Greedy | PQ on $h$ | finite graphs | No | $O(|V|)$ | $O(|V|)$ |
| A* | PQ on $g+h$ | Yes | admissible $h$ (consistent for graph w/o re-open) | exp. worst | $O(b^d)$ |
| Weighted A* | PQ on $g+Wh$ | Yes | No, ≤ $W C^*$ | ≪ A* | ≪ A* |
| Beam ($k$) | best $k$/level | No | No | $O(kbd)$ | $O(kb)$ |
| IDA* | $f$-limit DFS | Yes | admissible | ≥ A* | $O(bd)$ |

Family: $f = g + W h$ — $W=0$ UCS, $W=1$ A*, $1<W<\infty$ weighted A*, $W=\infty$ greedy ([[russell-norvig-aima]] §3.5.4).

## 5. Heuristics → [[heuristic-functions]]

- Slides: $h(n) \ge 0$, $h(\text{goal}) = 0$, an estimate (slide 11). Slide 16 "Properties of Heuristics" is image-only — content below from the book.
- **Admissible**: $h(n) \le h^*(n)$ (never overestimates) → A* optimal (tree search).
- **Consistent**: $h(n) \le c(n,a,n') + h(n')$ (triangle inequality) → admissible; $f$ non-decreasing along paths; graph-search A* optimal without re-opening; **optimally efficient**.
- **Dominance**: $h_2 \ge h_1$ everywhere (both admissible) → A*($h_2$) expands ≤ A*($h_1$).
- **max** of admissible heuristics is admissible and dominates each.
- **Relaxed problem**: optimal cost of a relaxation = admissible **and consistent** $h$. 8-puzzle: drop "Y blank" → Manhattan; drop "adjacent" too → misplaced.
- **Pattern databases** (exact subproblem costs; disjoint ones can be added), **landmarks** ($h_L$ inadmissible, differential $h_{DH}$ admissible).
- **Effective branching factor**: $N + 1 = 1 + b^* + (b^*)^2 + \dots + (b^*)^d$; good $h$ → $b^* \to 1$. Example $N = 52$, $d = 5$ → $b^* = 1.92$.
- A* expands **all** $f < C^*$, some $f = C^*$, **none** $f > C^*$.

## 6. Goal-test timing

| | Early (on generation) | Late (on pop) |
|---|---|---|
| Safe for | BFS (unit costs) | everything; **required** for UCS / A* optimality |
| Saves | one layer of nodes ($b^{d+1}$ → $b^d$) | — |
| Raymond | beam search | BFS (Ex01, 04, 05), A*, weighted A*, greedy |

Counterexample: UCS Sibiu → Bucharest — early test returns 310 (via Fagaras), late test returns 278 (via Pitesti) ([[russell-norvig-aima]] §3.4.2).

## 7. Numbers from HW01 and the discussion

- 8-puzzle ([[hw01-ex01-8-puzzle]]): BFS **20** (149,026 gen / 55,409 exp), DFS 66,056, greedy Manhattan 48 / Euclid 94 / misplaced 116 with **123 < 413 < 1,134** expanded; start $h_1 = 6$, Euclid 11.30, $h_2 = 14$ ([[heuristics-8-puzzle-comparison]]).
- 80-tile ([[hw01-ex02-80-tile]]): $h(\text{start}) = 306$; A* capped at 250,000 expansions (best $h$ 287); weighted A* W=10 → 1,116; beam 500 → 1,078; beam 5000 → **740**; $306 \le C^* \le 740$.
- Farmer **7**, M&C **11** ([[hw01-ex04-farmer-wolf-goat-cabbage]], [[hw01-ex05-missionaries-cannibals]]).
- Romania: optimal 418 via Sibiu–RV–Pitesti; greedy finds 450 via Fagaras; A* 5 non-goal expansions vs Dijkstra 12 ([[astar-vs-dijkstra]]).

## 8. Must-know facts

- Only the frontier changes between BFS, DFS, UCS, greedy, A* — same loop.
- BFS optimal **only** with equal costs; DFS never optimal.
- Memory, not time, kills BFS (b = 10, d = 10: 10 TB).
- IDS overhead ≈ $b/(b-1)$; preferred uninformed method for big spaces with unknown depth.
- A* with $h = 0$ is UCS; with $h = h^*$ it expands only the optimal path.
- Weighted A* bound: cost ∈ $[C^*, W C^*]$; in practice much closer to $C^*$.
- Beam: incomplete, suboptimal, memory-bounded; ordering by $h$ = ordering by $f$ when all nodes in a level share $g$.

## 9. Traps

- Slide 14 ties A* *completeness* to admissibility — the book does not (admissibility → optimality) ([[a-star]]).
- Slides' "Best-First Search" = greedy; book's best-first = general scheme with any $f$.
- Graph-search DFS memory is $O(|V|)$, not $O(bm)$.
- Counting the blank in misplaced tiles / Manhattan breaks admissibility.
- Admissible ⇏ consistent.
- Dominance theorems are for A*, not greedy.
- Compare expansion counts consistently (with or without the goal pop) — Discussion 01 mixes them.
- Generated ≠ expanded; the book's $b^*$ uses generated nodes.

## Practice questions

> [!question]- Q1. List the five components of a search problem for the farmer–wolf–goat–cabbage puzzle.
> **Answer.** Initial state `(R,R,R,R)`; actions: farmer alone / with wolf / goat / cabbage (passenger on farmer's bank); transition: flip farmer (and passenger); goal `(L,L,L,L)`; cost 1 per crossing. Illegal states (wolf+goat or goat+cabbage without farmer) are excluded ([[hw01-ex04-farmer-wolf-goat-cabbage]]).

> [!question]- Q2. BFS with early goal test, $b = 2$, solution at $d = 3$: worst-case nodes generated? With late goal test?
> **Answer.** Early: $1 + 2 + 4 + 8 = 15$. Late: the goal is popped last at depth 3, after expanding the other 7 depth-3 nodes → $+7\cdot2 = 14$ more ≈ 29 (bounded by $O(b^{d+1})$).

> [!question]- Q3. Which of BFS, DFS, IDS, UCS are optimal when action costs are 1 or 2?
> **Answer.** Only UCS (BFS and IDS need equal costs; DFS is never optimal).

> [!question]- Q4. A* frontier: A ($g=5$, $h=7$), B ($g=8$, $h=3$), C ($g=2$, $h=11$). Which node does A* expand? Greedy? UCS?
> **Answer.** $f$: A 12, B 11, C 13 → A* expands **B**. Greedy (min $h$) → **B**. UCS (min $g$) → **C**.

> [!question]- Q5. Is $h(n) = 0$ admissible? Consistent? What does A* become?
> **Answer.** Yes and yes (costs ≥ 0). A* becomes uniform-cost search.

> [!question]- Q6. $h(A) = 6$, $c(A, B) = 2$, $h(B) = 3$. Is $h$ consistent on this edge? Could it still be admissible?
> **Answer.** $6 \le 2 + 3 = 5$? No → inconsistent. It can still be admissible if $h^*(A) \ge 6$ and $h^*(B) \ge 3$ (e.g. $h^*(B) = 5$, $h^*(A) = 7$).

> [!question]- Q7. Derive Manhattan distance and misplaced tiles as relaxed problems.
> **Answer.** Original: tile moves X→Y if X adjacent to Y and Y blank. Drop "Y blank" → each tile walks independently → Manhattan. Drop both → each tile jumps in one move → misplaced tiles ([[russell-norvig-aima]] §3.6.2).

> [!question]- Q8. A* solves a problem at depth 2 generating 6 nodes. What is $b^*$?
> **Answer.** $N + 1 = 7 = 1 + b^* + b^{*2}$ → $b^{*2} + b^* - 6 = 0$ → $b^* = 2$.

> [!question]- Q9. Why does A* need a late goal test? Use Romania.
> **Answer.** Bucharest is generated from Fagaras with $f = 450$ before Pitesti ($f = 417$) is expanded; testing on generation would return 450 instead of the optimal 418 ([[a-star]]).

> [!question]- Q10. Raymond's weighted A* (W = 10) returns 1,116 moves; $h(\text{start}) = 306$. Give the theoretical and the empirical bound on suboptimality.
> **Answer.** Theory: ≤ $10\,C^*$. Empirical: $C^* \ge 306$ → path ≤ $1116/306 \approx 3.65\,C^*$ ([[weighted-a-star]]).

> [!question]- Q11. Why did greedy best-first with Manhattan return 48 moves on the 8-puzzle when the optimum is 20?
> **Answer.** Greedy ($f = h$) ignores accumulated cost $g$; it is not optimal. A* with Manhattan would return 20 ([[greedy-best-first-search]]).

> [!question]- Q12. When is tree-like DFS preferable to BFS? Give the memory for $b = 10$, $m = 15$.
> **Answer.** When memory is the constraint and any solution is acceptable on a finite (acyclic) space: $bm = 150$ nodes vs BFS's $b^d$ ([[depth-first-search]]).

> [!question]- Q13. Is beam search with $k = 5000$ complete? Why did it beat $k = 500$ on the 80-tile?
> **Answer.** Not complete (it discards nodes). A wider beam throws away fewer promising nodes, finding 740 vs 1,078, at ~7× the generated nodes ([[beam-search]]).

> [!question]- Q14. Show that Manhattan distance is consistent for the 8-puzzle.
> **Answer.** A move slides one tile one square; that tile's Manhattan distance changes by exactly ±1, others unchanged. So $h(n) - h(n') \le 1 = c(n, a, n')$.

## Weak spots

*(To be filled during exam prep: record the questions Raymond misses here.)*
