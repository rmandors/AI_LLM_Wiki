---
type: exam-review
summary: Hub for Midterm 1 (October 8, 20 % of the grade) - scope, a one-week study plan, links to every unit cheat sheet, the 25 facts most likely to be asked, mixed practice questions and a weak-spots log.
unit: [1, 2, 3, 4, 6, 9]
tags: [exam-review, midterm-1, hub]
sources: ["[[slides-00-instructor-introduction]]", "[[slides-01-introduction-to-ai]]", "[[slides-02-problem-solving]]", "[[slides-03-intelligent-agents]]", "[[slides-xx-logic-programming-prolog]]", "[[slides-04-optimization]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Midterm 1 — review hub

**Date:** October 8, 2026 · **Weight:** 20 % ([[slides-00-instructor-introduction]], slide 5;
"dates may change"). Homework 02 (16 %) is due October 2; its statement is not in `raw/` yet.

> [!warning] Scope not confirmed
> No source says which units Midterm 1 covers. This hub assumes **everything taught before
> October 8**: Units 1–4 (history, agents, search, CSPs, games), the Prolog deck (Unit 6)
> and Optimization (Unit 9), since all of these have slides and graded work already.
> Ask the instructor and update this box.

## Unit cheat sheets

| Unit | Sheet | Main concept pages | Your graded work |
|---|---|---|---|
| 1 History | [[unit-01-history-review]] | [[history-of-ai]], [[turing-test]], [[perceptron]] | — |
| 2 Agents | [[unit-02-agents-review]] | [[intelligent-agents]], [[rationality-and-peas]], [[environment-properties]], [[agent-architectures]] | — |
| 3 Search | [[unit-03-search-review]] | [[a-star]], [[heuristic-functions]], [[breadth-first-search]], [[depth-first-search]] | [[hw01-report]], [[discussion-01-astar-vs-dijkstra]] |
| 3 CSPs | [[unit-03-csp-review]] | [[constraint-satisfaction-problems]], [[csp-heuristics]], [[constraint-propagation]] | [[hw01-ex03-n-queens]], [[hw01-ex06-sudoku]] |
| 4 Games | [[unit-04-games-review]] | [[minimax]], [[alpha-beta-pruning]], [[monte-carlo-tree-search]] | [[chess-vs-go]], [[tic-tac-toe-4x4-py]] |
| 6 Logic / Prolog | [[unit-06-logic-prolog-review]] | [[horn-clauses]], [[unification]], [[backward-chaining]], [[prolog]] | [[lab01-family-pl]] |
| 9 Optimization | [[unit-09-optimization-review]] | [[genetic-algorithms]], [[particle-swarm-optimization]], [[ant-colony-optimization]], [[simulated-annealing]] | [[genetic-algorithm-py]], [[ga-exercise-explanation]] |

Comparison tables worth printing: [[search-algorithms-comparison]],
[[game-search-comparison]], [[csp-techniques-comparison]], [[logic-systems-comparison]],
[[metaheuristics-comparison]], [[agent-types-comparison]].

## One-week plan (Oct 1 – Oct 7)

| Day | Focus | Do |
|---|---|---|
| Thu 1 | HW02 (due Oct 2) | Finish HW02, then drop its statement and your solution into `raw/HW_02/` for ingest. |
| Fri 2 | Units 1–2 | Read both sheets; answer all their questions without peeking. |
| Sat 3 | Unit 3 search | Sheet + hand-run A* and UCS on the Romania map ([[astar-vs-dijkstra]]). |
| Sun 4 | Unit 3 CSPs + Unit 4 | Hand-run alpha-beta on a 3-ply tree; MRV/forward checking on a small map-colouring. |
| Mon 5 | Unit 6 Prolog | Unification drills, trace backward chaining, predict query outputs. |
| Tue 6 | Unit 9 | One PSO velocity update, one ACO probability, one SA acceptance, decode a GA chromosome by hand. |
| Wed 7 | Mixed | The mixed questions below, then re-do whatever is in "Weak spots". |

## The 25 facts most likely to be asked

1. Problem formulation has five parts: initial state, actions, transition model, goal test, action cost ([[problem-formulation]]).
2. BFS: complete; optimal only with equal step costs; $O(b^d)$ time **and** space ([[breadth-first-search]]).
3. DFS: $O(bm)$ space; not optimal; complete only in finite spaces with repeated-state control ([[depth-first-search]]).
4. UCS = Dijkstra: expands lowest $g$; optimal for positive costs ([[uniform-cost-search]]).
5. Greedy best-first: $f = h$; not optimal ([[greedy-best-first-search]]).
6. A*: $f = g + h$; optimal if $h$ admissible (tree search) or consistent (graph search) ([[a-star]]).
7. Admissible: $h(n) \le h^*(n)$. Consistent: $h(n) \le c(n,a,n') + h(n')$. Consistent ⇒ admissible ([[heuristic-functions]]).
8. Manhattan dominates misplaced tiles, so A* with Manhattan expands no more nodes ([[heuristics-8-puzzle-comparison]]).
9. Weighted A* ($f = g + Wh$) trades optimality for speed; cost ≤ $W \cdot C^*$ ([[weighted-a-star]]).
10. Minimax: $O(b^m)$ time, $O(bm)$ space; assumes optimal opponent ([[minimax]]).
11. Alpha-beta returns the minimax value; best case $O(b^{m/2})$; move ordering matters ([[alpha-beta-pruning]]).
12. Real games use a cutoff test + evaluation function (H-MINIMAX); Go needed MCTS + neural networks ([[chess-vs-go]]).
13. A CSP has variables, domains, constraints; a solution is a complete, consistent assignment ([[constraint-satisfaction-problems]]).
14. MRV picks the variable (fail-first); LCV orders the values (fail-last); forward checking prunes neighbour domains ([[csp-heuristics]]).
15. Rational agent: maximises *expected* performance given percepts and built-in knowledge, not omniscient ([[rationality-and-peas]]).
16. PEAS = Performance, Environment, Actuators, Sensors ([[rationality-and-peas]]).
17. Environment dimensions: observable, deterministic, episodic, static, discrete, single-agent (and opposites) ([[environment-properties]]).
18. Agent types: simple reflex → model-based → goal-based → utility-based (→ learning) ([[agent-architectures]]).
19. Turing test (1950) and Dartmouth (1956, McCarthy coins "AI") ([[history-of-ai]]).
20. Horn clause: at most one positive literal; definite clause = rule, fact = empty body, goal clause = query ([[horn-clauses]]).
21. Prolog = Horn clauses + backward chaining (depth first, left to right) + unification ([[sld-resolution]]).
22. `is/2` evaluates arithmetic; `=/2` only unifies; `\+` is negation as failure under the closed-world assumption ([[negation-as-failure]]).
23. GA: selection, crossover, mutation; elitism keeps the best; bits encode solutions ([[genetic-algorithms]]).
24. PSO: $v \leftarrow v + c_1 r_1 (p_{best} - x) + c_2 r_2 (g_{best} - x)$, then $x \leftarrow x + v$ ([[particle-swarm-optimization]]).
25. ACO: $p_{ij} \propto \tau_{ij}^\alpha \eta_{ij}^\beta$ with $\eta = 1/d$; evaporation stops the trail from exploding ([[ant-colony-optimization]]).

## Known errors in the slides (do not repeat them on the exam)

- Slides 01, slide 9 attribute Prolog to Dennis Ritchie at Bell Labs; it was Colmerauer and
  Roussel, Marseille, 1972 ([[slides-01-introduction-to-ai]], [[prolog]]).
- Slides 02, slide 14 say A* is complete "if h is admissible"; A* is complete regardless,
  admissibility is what gives optimality ([[a-star]]).
- Slides 02, slide 24 list MRV as constraint propagation; it is a variable-ordering heuristic
  ([[csp-heuristics]]).
- Slides 03, slide 2 contain logic text under "What is an agent?" ([[slides-03-intelligent-agents]]).
- Slides 04 date GAs both 1975 and 1992 (1992 is Holland's Scientific American article)
  ([[slides-04-optimization]]).

If the instructor's answer key follows the slide, mention both in your answer.

## Mixed practice questions

> [!question]- Q1. An agent plays poker with other people. Classify the environment on the six dimensions.
> **Answer.** Partially observable (hidden cards), stochastic (shuffle), sequential, static
> (ignoring the clock), discrete, multi-agent and competitive ([[environment-properties]]).

> [!question]- Q2. BFS and A* with Manhattan distance both find the 20-move 8-puzzle solution. Why does A* still win?
> **Answer.** Both are optimal here (unit costs; admissible h), but A* expands far fewer
> nodes because h focuses the search: in R&N Fig. 3.26 at depth 20, BFS-style search
> generates about 91,000 nodes vs about 1,300 for A*(h2) ([[hw01-ex01-8-puzzle]], [[a-star]]).

> [!question]- Q3. Give a heuristic that is admissible but not consistent, on a 3-node graph.
> **Answer.** S→A cost 1, A→G cost 1. Set h(S)=2, h(A)=0, h(G)=0. Admissible: h*(S)=2,
> h*(A)=1. Not consistent: h(S)=2 > c(S,A)+h(A)=1+0 ([[heuristic-functions]]).

> [!question]- Q4. Minimax tree: MAX root with two MIN children; leaves (3, 12, 8) and (2, 4, 6). Value? What does alpha-beta prune?
> **Answer.** First MIN = 3, so α = 3 at the root. In the second MIN node the first leaf is 2 ≤ α,
> so leaves 4 and 6 are pruned. Root value = 3 ([[alpha-beta-pruning]]).

> [!question]- Q5. Australia map colouring: after WA = red, which domains does forward checking change?
> **Answer.** Removes red from the neighbours of WA: NT and SA become {green, blue}; the
> others are unchanged ([[constraint-propagation]], [[russell-norvig-aima]] §5.3.2).

> [!question]- Q6. Unify `knows(john, X)` with `knows(Y, mother(Y))`.
> **Answer.** {Y/john, X/mother(john)} ([[unification]]).

> [!question]- Q7. Why does `path(X,Z):- path(X,Y), link(Y,Z).` placed first overflow the stack in Prolog, though it is logically fine?
> **Answer.** SLD resolution picks the leftmost goal and clauses in file order, so `path`
> calls itself before consuming any `link`: infinite left recursion. Put the base case first
> and the recursive call last, or use `:- table path/2.` ([[sld-resolution]]).

> [!question]- Q8. Decode the 8-bit GA half `10010110` with Raymond's encoding (sign bit + 7-bit magnitude / 10).
> **Answer.** Sign 1 → negative; 0010110₂ = 22 → 2.2; value = −2.2 ([[genetic-algorithm-py]]).

> [!question]- Q9. PSO, 1-D: x = 4, v = 1, pbest = 2, gbest = 0, c1 = c2 = 2, r1 = 0.5, r2 = 0.25. New v and x?
> **Answer.** v = 1 + 2·0.5·(2−4) + 2·0.25·(0−4) = 1 − 2 − 2 = −3; x = 4 − 3 = 1
> ([[particle-swarm-optimization]]).

> [!question]- Q10. SA minimising cost: current 10, neighbour 12, T = 4. Acceptance probability?
> **Answer.** Δ = 2 > 0, so p = e^(−2/4) = e^(−0.5) ≈ 0.61 ([[simulated-annealing]]).

> [!question]- Q11. Which HW01 problems did you solve with BFS and why not A*?
> **Answer.** 8-puzzle (for the optimal path), farmer and missionaries: small state spaces
> with unit costs, where BFS is cost-optimal and needs no heuristic ([[hw01-report]]).

> [!question]- Q12. A thermostat that turns on heat when temperature < 20 °C: which agent type?
> **Answer.** Simple reflex agent: a condition–action rule on the current percept
> ([[agent-architectures]]).

## Weak spots

Filled in during exam-prep sessions (date, topic, what went wrong).

- *(none recorded yet)*
