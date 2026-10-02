# Page registry (initial build, 2026-10-01)

Every page of the first build, by owner. Any agent may LINK to any page here (they will
all exist); each agent CREATES only the pages in its own section. Paths are relative to
`wiki/`. Link with `[[file-name]]` (no folder, no `.md`).

## Hub (lead agent)
- index, log, overview
- concepts/upcoming-topics
- sources/russell-norvig-aima
- exam-review/midterm-01-review

## A — History, agents, people
- concepts/history-of-ai, concepts/turing-test, concepts/perceptron
- concepts/intelligent-agents, concepts/rationality-and-peas,
  concepts/environment-properties, concepts/agent-architectures,
  concepts/state-representation
- people/daniel-riofrio, people/alan-turing, people/john-mccarthy,
  people/frank-rosenblatt, people/judea-pearl, people/john-holland,
  people/kennedy-and-eberhart, people/marco-dorigo, people/dervis-karaboga,
  people/robert-kowalski, people/alain-colmerauer
- sources/slides-00-instructor-introduction, sources/slides-01-introduction-to-ai,
  sources/slides-03-intelligent-agents
- comparisons/agent-types-comparison
- exam-review/unit-01-history-review, exam-review/unit-02-agents-review

## B — Search
- concepts/problem-formulation, concepts/state-space-and-graph-search,
  concepts/uninformed-search, concepts/breadth-first-search,
  concepts/depth-first-search, concepts/uniform-cost-search,
  concepts/iterative-deepening-search, concepts/informed-search,
  concepts/greedy-best-first-search, concepts/a-star, concepts/weighted-a-star,
  concepts/beam-search, concepts/heuristic-functions
- sources/slides-02-problem-solving, sources/hw01-report,
  sources/hw01-ai-transcript,
  sources/discussion-01-astar-vs-dijkstra
- code/hw01-ex01-8-puzzle, code/hw01-ex02-80-tile,
  code/hw01-ex04-farmer-wolf-goat-cabbage, code/hw01-ex05-missionaries-cannibals
- comparisons/search-algorithms-comparison, comparisons/heuristics-8-puzzle-comparison,
  comparisons/astar-vs-dijkstra
- exam-review/unit-03-search-review

## C — Games and CSPs
- concepts/adversarial-search, concepts/minimax, concepts/alpha-beta-pruning,
  concepts/monte-carlo-tree-search
- concepts/constraint-satisfaction-problems, concepts/csp-backtracking-search,
  concepts/csp-heuristics, concepts/constraint-propagation
- code/hw01-ex03-n-queens, code/hw01-ex06-sudoku, code/tic-tac-toe-4x4-py
- comparisons/game-search-comparison, comparisons/chess-vs-go,
  comparisons/csp-techniques-comparison
- exam-review/unit-03-csp-review, exam-review/unit-04-games-review

## D — Logic and Prolog
- concepts/propositional-logic, concepts/first-order-logic,
  concepts/conjunctive-normal-form-and-resolution, concepts/horn-clauses,
  concepts/forward-chaining, concepts/backward-chaining, concepts/unification,
  concepts/prolog, concepts/sld-resolution, concepts/negation-as-failure,
  concepts/prolog-cut
- sources/slides-xx-logic-programming-prolog, sources/lab01-prolog-family-report,
  sources/luger-ai-6e
- code/lab01-family-pl, code/prolog-lecture-examples
- comparisons/logic-systems-comparison
- exam-review/unit-06-logic-prolog-review

## E — Optimization and bio-inspired algorithms
- concepts/optimization-problems, concepts/exploration-vs-exploitation,
  concepts/hill-climbing, concepts/gradient-descent, concepts/simulated-annealing,
  concepts/evolutionary-computation, concepts/genetic-algorithms,
  concepts/schema-theory-and-building-blocks, concepts/particle-swarm-optimization,
  concepts/ant-colony-optimization, concepts/artificial-bee-colony,
  concepts/swarm-intelligence
- sources/slides-04-optimization, sources/holland-1992-genetic-algorithms,
  sources/kennedy-eberhart-1995-pso, sources/dorigo-1996-ant-system,
  sources/eiben-smith-evolutionary-computing, sources/ga-exercise-explanation
- code/genetic-algorithm-py, code/particle-swarm-py, code/ant-colony-py,
  code/simulated-annealing-py, code/gradient-descent-py
- comparisons/metaheuristics-comparison
- exam-review/unit-09-optimization-review

## Raw file -> source page map
| raw/ path | source page |
|---|---|
| Slides/00_Instructor Introduction.pptx | slides-00-instructor-introduction |
| Slides/01_Introduction to Artificial Intelligence.pptx | slides-01-introduction-to-ai |
| Slides/02_Problem Solving.pptx | slides-02-problem-solving |
| Slides/03_Intelligent Agents.pptx | slides-03-intelligent-agents |
| Slides/04_Optimization.pptx | slides-04-optimization |
| Slides/XX_Logic Programming with Prolog.pptx | slides-xx-logic-programming-prolog |
| Papers/Holland-GeneticAlgorithms-1992.pdf | holland-1992-genetic-algorithms |
| Papers/2 - Particle_swarm_optimization.pdf | kennedy-eberhart-1995-pso |
| Papers/3 - dorigo1996.pdf | dorigo-1996-ant-system |
| Books/Stuart J. Russell, Peter Norvig -... (2021).pdf | russell-norvig-aima |
| Books/Artificial Intelligence - 6th Edition.pdf (Luger) | luger-ai-6e |
| Books/A.E. Eiben_ J.E. Smith -... (2015).pdf | eiben-smith-evolutionary-computing |
| HW_01/HW01_RP.pdf/.docx | hw01-report |
| HW_01/AI_transcript.md | hw01-ai-transcript |
| HW_01/Practical_exercises/*.py | code/hw01-ex0N-* |
| Class_exercises/Discussion_01_RP.docx | discussion-01-astar-vs-dijkstra |
| Class_exercises/01_Code/* (lab + lecture.pl) | lab01-prolog-family-report, lab01-family-pl, prolog-lecture-examples |
| Class_exercises/Genetic Algorithm Exercise/* | ga-exercise-explanation, genetic-algorithm-py, particle-swarm-py, ant-colony-py |
| Class_exercises/sa_functions.py | simulated-annealing-py |
| Class_exercises/gd_functions.py | gradient-descent-py |
| Class_exercises/tic-tac-toe.py | tic-tac-toe-4x4-py |
