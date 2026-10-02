---
type: source
summary: Russell & Norvig, Artificial Intelligence - A Modern Approach, 4th ed. Global Edition (2021) - the course's base textbook, ingested chapter by chapter.
unit: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tags: [textbook, aima]
sources: []
updated: 2026-10-01
---

# Russell & Norvig — *AIMA* 4th ed., Global Edition

Stuart J. Russell, Peter Norvig. *Artificial Intelligence: A Modern Approach*, 4th ed.,
Global Edition. Pearson, 2021. File: `raw/Books/Stuart J. Russell, Peter Norvig - Artificial Intelligence_ A Modern Approach, Global Edition-Pearson (2021).pdf`
(1,167 PDF pages; **PDF page = book page + 1**).

The course's base textbook. The slides cite it directly (e.g. the Prolog deck reproduces
Figs. 7.12, 7.16 and 9.7, see [[slides-xx-logic-programming-prolog]]), and the homework
cites it by section ([[hw01-report]]).

> [!warning] Edition numbering
> This is the **Global Edition**: Ch. 5 = Constraint Satisfaction Problems, Ch. 6 =
> Adversarial Search and Games. The US 4th edition swaps them (CSPs = Ch. 6, Games = Ch. 5).
> If the professor quotes a US chapter number, translate it.

## Chapter map to the syllabus

| Chapter (book page) | Topic | Unit | Status | Main wiki pages |
|---|---|---|---|---|
| 1 Introduction (p. 19) | definitions of AI, foundations, history | 1 | read (§1.1–1.4) | [[history-of-ai]], [[turing-test]] |
| 2 Intelligent Agents (p. 54) | agents, rationality, PEAS, environments, agent programs | 2 | read (all) | [[intelligent-agents]], [[rationality-and-peas]], [[environment-properties]], [[agent-architectures]], [[state-representation]] |
| 3 Solving Problems by Searching (p. 81) | formulation, BFS/DFS/UCS/IDS, greedy, A*, weighted A*, beam, heuristics | 2, 3 | read (all) | [[problem-formulation]], [[uninformed-search]], [[informed-search]], [[a-star]], [[heuristic-functions]] |
| 4 Search in Complex Environments (p. 128) | hill climbing, SA, local beam, evolutionary algorithms, continuous spaces | 9 | read (§4.1–4.2) | [[hill-climbing]], [[simulated-annealing]], [[genetic-algorithms]], [[gradient-descent]] |
| 5 Constraint Satisfaction Problems (p. 164) | CSPs, AC-3, backtracking, MRV/LCV, FC, min-conflicts, structure | 3 | read (§5.1–5.5) | [[constraint-satisfaction-problems]], [[csp-backtracking-search]], [[csp-heuristics]], [[constraint-propagation]] |
| 6 Adversarial Search and Games (p. 192) | minimax, alpha-beta, cutoffs and evaluation, MCTS | 4 | read (§6.1–6.5) | [[minimax]], [[alpha-beta-pruning]], [[monte-carlo-tree-search]] |
| 7 Logical Agents (p. 226) | propositional logic, resolution, Horn clauses, chaining | 5, 6 | read (§7.3–7.5) | [[propositional-logic]], [[conjunctive-normal-form-and-resolution]], [[horn-clauses]], [[forward-chaining]] |
| 8 First-Order Logic (p. 269) | syntax and semantics of FOL | 6 | read (§8.1–8.3) | [[first-order-logic]] |
| 9 Inference in First-Order Logic (p. 298) | unification, forward/backward chaining, logic programming | 6 | read (§9.1–9.5.1) | [[unification]], [[backward-chaining]], [[prolog]], [[sld-resolution]] |
| 10–11 Knowledge representation, planning | ontologies, classical planning | 5 | not yet | [[upcoming-topics]] |
| 12 Quantifying Uncertainty (p. 403) | probability, Bayes' rule, naive Bayes | 7 | not yet | [[upcoming-topics]] |
| 13 Probabilistic Reasoning (p. 430) | Bayesian networks | 7 | not yet | [[upcoming-topics]] |
| 14 Probabilistic Reasoning over Time (p. 479) | Markov models, HMMs, filtering | 8 | not yet (only §14.3.2 cited once) | [[upcoming-topics]] |
| 19, 21 Learning, neural networks | supervised learning, perceptron, deep learning | 10 | only §19.6.4 cited for the perceptron | [[perceptron]], [[upcoming-topics]] |
| 27–28 Ethics, future | AI safety, ethics | 10 | only §28.1.4 cited | [[upcoming-topics]] |

## Sections read so far (initial build, 2026-10-01)

§1.1–1.4 · §2.1–2.4.7 · §3.1–3.6.4 (Figs. 3.1, 3.9, 3.15–3.18, 3.26) · §4.1–4.2
(Figs. 4.1–4.8) · §5.1–5.5 (Figs. 5.5, 5.7–5.9) · §6.1–6.5 (Figs. 6.2, 6.5, 6.6) ·
§7.3–7.5.4 (Figs. 7.8, 7.15) · §8.1–8.3.2 · §9.1–9.5.1 (Figs. 9.1, 9.3, 9.6, 9.7) ·
bibliographic notes of Ch. 4.

## Key facts the wiki relies on

- Search criteria: completeness, cost optimality, time and space complexity, in terms of
  b, d, m (§3.3.4). Property table of uninformed strategies in Fig. 3.15.
- A* is cost-optimal with an admissible heuristic; with a consistent heuristic every
  node is expanded once on its optimal path (§3.5.2). Weighted A* bounds cost by W·C*
  (§3.5.4). Manhattan distance dominates misplaced tiles (§3.6.1); relaxed problems
  generate admissible heuristics (§3.6.2).
- Local search: hill climbing gets stuck in local maxima, ridges and plateaus (§4.1.1);
  simulated annealing accepts worse moves with probability $e^{\Delta E/T}$ (Fig. 4.5);
  genetic algorithms = stochastic beam search + crossover (§4.1.4).
- CSPs: AC-3 (Fig. 5.3), backtracking (Fig. 5.5), MRV and degree heuristics, LCV
  (§5.3.1), forward checking and MAC (§5.3.2), min-conflicts (§5.4).
- Games: minimax O(b^m); alpha-beta with perfect move ordering O(b^{m/2}) (§6.2.4);
  H-MINIMAX with cutoff and evaluation (§6.3); MCTS with UCT (§6.4).
- Logic: Horn/definite clauses give linear-time propositional entailment by chaining
  (§7.5.4); unification and the MGU (§9.2); Prolog = depth-first backward chaining
  (§9.4).

## Pages that use this source

Almost every concept page. The densest users are [[unit-03-search-review]],
[[unit-04-games-review]], [[unit-03-csp-review]], [[unit-06-logic-prolog-review]] and
[[unit-09-optimization-review]].

## Issues found

- Fig. 4.5 (simulated annealing) in this extraction reads `ΔE ← VALUE(current) − VALUE(next)`;
  the sign convention is discussed on [[simulated-annealing]].
- §3.6 prints "9!/2 = 181,400" reachable 8-puzzle states; the correct value is 181,440
  (see [[hw01-ex01-8-puzzle]]).
- Go's branching factor is given as 361 (empty board), while the homework uses the
  average ≈250; both are right for different measures (see [[chess-vs-go]]).
