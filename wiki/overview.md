---
type: overview
summary: The big picture - course logistics, how the units fit together (almost everything so far is search in a different space), graded work, open questions.
unit: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tags: [overview, syllabus, synthesis]
sources: ["[[slides-00-instructor-introduction]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Overview — Artificial Intelligence, USFQ, Fall 2026

Instructor [[daniel-riofrio]] · NRC 1651 · Textbook [[russell-norvig-aima]] (Global Edition).
Start at [[index]] for the full catalog, or [[midterm-01-review]] if an exam is near.

## Grading and dates ([[slides-00-instructor-introduction]], slide 5)

| Item | Weight | Date | Status | Wiki |
|---|---|---|---|---|
| Homework 01 | 12 % | Sep 11 | submitted (report dated Sep 16) | [[hw01-report]] |
| Homework 02 | 16 % | Oct 2 | not in `raw/` yet | — |
| Midterm 1 | 20 % | Oct 8 | upcoming | [[midterm-01-review]] |
| Homework 03 | 12 % | Nov 6 | — | — |
| Midterm 2 | 20 % | Dec 3 | — | — |
| Final project | 20 % | Dec 7–17 | — | — |

Ungraded or in-class work so far: Prolog Lab 01 ([[lab01-prolog-family-report]]),
Discussion 01 on A* vs Dijkstra ([[discussion-01-astar-vs-dijkstra]]), the GA/PSO/ACO class
activity ([[ga-exercise-explanation]]), and class code for SA, gradient descent and 4×4
tic-tac-toe.

## Course map

| Unit | Topic | Status | Entry page |
|---|---|---|---|
| 1 | History and foundations | taught | [[history-of-ai]] |
| 2 | Agents and problem formulation | taught | [[intelligent-agents]], [[problem-formulation]] |
| 3 | Heuristic search (+ CSPs) | taught | [[informed-search]], [[constraint-satisfaction-problems]] |
| 4 | Adversarial search | taught | [[adversarial-search]] |
| 5 | Knowledge, reasoning, planning | not yet | [[upcoming-topics]] |
| 6 | Logic and Prolog | taught (Prolog deck) | [[prolog]], [[horn-clauses]] |
| 7 | Uncertainty, Bayes | not yet | [[upcoming-topics]] |
| 8 | Markov models | not yet | [[upcoming-topics]] |
| 9 | Optimization, bio-inspired | taught | [[optimization-problems]], [[metaheuristics-comparison]] |
| 10 | ML, neural networks, ethics | not yet (perceptron in Unit 1) | [[perceptron]], [[upcoming-topics]] |

The course is not taught in syllabus order: the Prolog deck (Unit 6) and Optimization
(Unit 9) came before Homework 1 was due.

## Synthesis: it is all search

So far every unit is the same idea (choose the next candidate from a set of candidates)
applied to a different space. Seeing it this way makes the units easier to compare.

| What is being searched | Candidate | How the next one is chosen | Pages |
|---|---|---|---|
| Paths in a state space | a node (partial path) | frontier order: FIFO, LIFO, $g$, $h$, $g+h$ | [[search-algorithms-comparison]] |
| Assignments in a CSP | a partial assignment | depth-first backtracking + MRV/LCV + propagation | [[csp-techniques-comparison]] |
| Moves in a game | a game-tree node | minimax values, alpha-beta bounds, MCTS statistics | [[game-search-comparison]] |
| Proofs in a Horn knowledge base | a goal list | SLD resolution = depth-first backward chaining | [[sld-resolution]], [[logic-systems-comparison]] |
| Points in an objective landscape | a full solution (or a population) | neighbour, gradient, temperature, selection + crossover, swarm velocity, pheromone | [[metaheuristics-comparison]] |

Three ideas come back in every row:

1. **Systematic vs. local.** Path search, CSP backtracking, game trees and Prolog are
   systematic: they keep enough structure to be complete. Hill climbing, SA, GA, PSO and ACO
   keep only current solutions, so they use little memory but give no guarantee
   ([[optimization-problems]]).
2. **Knowledge as a guide.** A heuristic $h$ in A*, the evaluation function in H-MINIMAX,
   MRV in CSPs, visibility $\eta = 1/d$ in ACO and fitness in a GA all inject problem
   knowledge to decide what to try next ([[heuristic-functions]]).
3. **Exploration vs. exploitation.** BFS vs. greedy, beam width $k$, UCT's exploration
   term in MCTS, temperature in SA, mutation rate in GA, and $\alpha/\beta$ in ACO all set
   the same trade-off ([[exploration-vs-exploitation]]).

Concrete links between units found in the sources:

- N-Queens appears three times: CSP backtracking in HW01 ([[hw01-ex03-n-queens]]), the
  Prolog case study ([[prolog-lecture-examples]], whose first answer is the reverse of the
  Python one), and the GA example in R&N §4.1.4 ([[genetic-algorithms]]).
- Beam search (HW01 80-tile) → local beam search → GA = stochastic beam search + crossover
  ([[beam-search]], [[genetic-algorithms]]).
- Prolog's execution is depth-first search with backtracking, the same control strategy
  as [[csp-backtracking-search]] ([[sld-resolution]]).

## Recurring caveats

- Many slides are image-only, so their text could not be extracted; each source page lists
  which ones, and the content was filled from the textbook or papers.
- Several slide errors are recorded as `Contradiction` callouts; the list is on
  [[midterm-01-review]].

## Open questions to ask

- What exactly does Midterm 1 cover?
- Where is `family.pl` (cited by the Prolog deck, missing from `raw/`)?
- Is the 80-tile hole tile 9H or 9I? The assignment text says both ([[hw01-ex02-80-tile]]).
