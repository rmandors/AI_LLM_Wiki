# Index

Catalog of every page in the wiki, with its one-line summary. The agent reads this first when answering a question and updates it on every ingest. Start with [[overview]] for the big picture or [[midterm-01-review]] before the exam. History of changes: [[log]].

*113 pages · updated 2026-10-01*

## Hubs

- [[overview]] — The big picture - course logistics, how the units fit together (almost everything so far is search in a different space), graded work, open questions.
- [[midterm-01-review]] — Hub for Midterm 1 (October 8, 20 % of the grade) - scope, a one-week study plan, links to every unit cheat sheet, the 25 facts most likely to be asked, mixed practice questions and a weak-spots log.

## Concepts

### Unit 1 — History and foundations

- [[history-of-ai]] — Chronological synthesis of AI history — ancient automata, early computers, Turing and Dartmouth, symbolic AI and its winters, expert systems, neural-network revivals, probabilistic ML and deep learning.
- [[turing-test]] — Turing's 1950 behavioural test of machine intelligence — a computer passes if a human interrogator chatting by text cannot reliably tell it from a person.
- [[perceptron]] — Rosenblatt's 1958 single artificial neuron — a weighted sum passed through a hard threshold, trained by the perceptron learning rule; it learns any linearly separable function but cannot represent XOR.

### Unit 2 — Agents and problem formulation

- [[intelligent-agents]] — An agent perceives its environment through sensors and acts on it through actuators; its behaviour is an agent function from percept sequences to actions, implemented by an agent program on an architecture.
- [[rationality-and-peas]] — A rational agent picks the action expected to maximise its performance measure given its percepts and prior knowledge; PEAS (Performance, Environment, Actuators, Sensors) specifies the task environment.
- [[environment-properties]] — The seven dimensions that classify task environments — observable, agents, deterministic, episodic, static, discrete, known — and how each dictates agent design.
- [[agent-architectures]] — The five agent program designs — simple reflex, model-based reflex, goal-based, utility-based and learning agents — each adding one capability to handle harder environments.
- [[state-representation]] — Atomic, factored and structured representations of world states — increasing expressiveness at the cost of harder reasoning and learning — and which AI techniques use each.
- [[problem-formulation]] — How a problem-solving agent turns a task into a search problem — initial state, actions, transition model, goal test and action cost — at the right level of abstraction.

### Unit 3 — Search and CSPs

- [[state-space-and-graph-search]] — The state space as an implicit graph, the search tree built over it, frontier vs reached/explored sets, and the difference between graph search and tree-like search.
- [[uninformed-search]] — Blind search strategies that know only the problem definition (no estimate of distance to goal) and differ only in the order they expand nodes, judged by completeness, optimality, time and space.
- [[breadth-first-search]] — Uninformed search that expands the shallowest node first with a FIFO queue; complete, optimal only for equal action costs, O(b^d) time and space.
- [[depth-first-search]] — Uninformed search that always expands the deepest node using a LIFO stack; not optimal, complete only on finite spaces with repeated-state control, but only O(bm) memory as a tree-like search.
- [[uniform-cost-search]] — Uniform-cost search (Dijkstra's algorithm) expands the frontier node with the lowest path cost g(n); complete and cost-optimal with positive costs, O(b^(1+floor(C*/epsilon))) time and space.
- [[iterative-deepening-search]] — Depth-limited DFS run repeatedly with limits 0, 1, 2,... — BFS's completeness and unit-cost optimality with DFS's O(bd) memory; IDA* applies the same idea to f-cost contours.
- [[informed-search]] — Heuristic search that uses a problem-specific estimate h(n) of the cost to the goal to decide which frontier node to expand next; covers greedy best-first, A*, weighted A*, beam search and memory-bounded variants.
- [[greedy-best-first-search]] — Best-first search with f(n) = h(n) — always expands the node that looks closest to the goal; fast with a good heuristic but not optimal and complete only on finite spaces with repeated-state control.
- [[a-star]] — A* is best-first search on f(n) = g(n) + h(n); complete, cost-optimal with an admissible (tree) or consistent (graph) heuristic, optimally efficient, but its memory grows exponentially.
- [[weighted-a-star]] — Weighted A* uses f(n) = g(n) + W·h(n) with W > 1 to trade optimality for speed; it is a bounded-suboptimal search returning a cost between C* and W·C*.
- [[beam-search]] — Beam search keeps only the k best nodes (by f or h) at each level and discards the rest — memory-bounded and fast, but incomplete and not optimal.
- [[heuristic-functions]] — Heuristic functions h(n) estimate cost-to-goal; this page covers admissibility, consistency, dominance, effective branching factor, and how to invent heuristics (relaxed problems, max of heuristics, pattern databases, landmarks), with 8-puzzle examples.
- [[constraint-satisfaction-problems]] — A CSP is a problem with a factored state (variables X, domains D, constraints C), solved by finding a complete and consistent assignment; examples are map colouring, N-queens and Sudoku.
- [[csp-backtracking-search]] — Backtracking search is depth-first search over partial CSP assignments that assigns one variable per level, checks constraints, and undoes the last choice on failure; it is the base algorithm that MRV, LCV and inference improve.
- [[csp-heuristics]] — General-purpose CSP heuristics — MRV ("fail-first") and degree for choosing the next variable, LCV ("fail-last") for ordering its values, and min-conflicts for local search over complete assignments.
- [[constraint-propagation]] — Constraint propagation uses constraints to delete impossible values from domains (node, arc, path, k-consistency; AC-3), either before search or interleaved with it as forward checking or MAC.

### Unit 4 — Adversarial search

- [[adversarial-search]] — Search in multi-agent competitive environments (games) where an opponent chooses half the moves, so the goal is an optimal strategy rather than a path.
- [[minimax]] — Minimax computes the optimal move in a two-player zero-sum game by backing up utilities (MAX takes the maximum, MIN the minimum); H-MINIMAX cuts it off at a depth and uses an evaluation function.
- [[alpha-beta-pruning]] — Alpha-beta pruning returns the same move as minimax while skipping branches that cannot affect the decision, using bounds α (MAX's best so far) and β (MIN's best so far); with perfect move ordering it costs O(b^(m/2)).
- [[monte-carlo-tree-search]] — MCTS estimates move values from many simulated playouts, growing a search tree by repeated selection (UCB1/UCT), expansion, simulation and back-propagation; it is the core of modern Go programs.

### Units 5–6 — Logic and Prolog

- [[propositional-logic]] — The simplest logic — proposition symbols joined by five connectives, truth defined by truth tables; decidable (entailment is co-NP-complete) but unable to talk about objects or say "every".
- [[first-order-logic]] — Logic with objects, relations, functions and the quantifiers ∀/∃ — expressive enough for "every" and "some", but entailment is only semidecidable.
- [[conjunctive-normal-form-and-resolution]] — Every sentence can be rewritten as a conjunction of clauses (CNF); resolution, a single rule that cancels complementary literals, is refutation-complete on clauses and underlies Prolog.
- [[horn-clauses]] — Clauses with at most one positive literal — definite clauses (rules), facts and goal clauses; they read as implications and make entailment linear-time (propositional), which is why Prolog is built on them.
- [[forward-chaining]] — Data-driven inference for definite clauses — fire every rule whose premises are known, add its conclusion, repeat to a fixed point; sound, complete, linear-time in the propositional case.
- [[backward-chaining]] — Goal-directed inference for definite clauses — start from the query, find rules whose head matches, prove their bodies recursively; a depth-first AND–OR search that is Prolog's execution model.
- [[unification]] — Finding the most general substitution (MGU) that makes two terms identical — two-way pattern matching that powers every first-order inference rule and every Prolog call; Prolog skips the occurs check.
- [[prolog]] — Prolog ("programmation en logique", Marseille 1972) — first-order Horn clauses plus depth-first backward chaining with unification; you state what holds, the interpreter searches for a proof.
- [[sld-resolution]] — Prolog's execution strategy — resolve the leftmost goal against clauses in file order, depth first with backtracking; SLD resolution is complete for definite clauses but Prolog's fixed search rule is not, so clause and goal order matter (left recursion loops; tabling fixes it).
- [[negation-as-failure]] — Prolog's \+ Goal succeeds when Goal cannot be proved; it equals logical negation only under the closed-world assumption, and is only safe on goals whose variables are already bound.
- [[prolog-cut]] — The cut (!) commits Prolog to the choices made so far in a clause — no retrying goals to its left, no later clauses for that predicate; it buys speed but breaks the declarative reading (the max/3 bug); prefer if-then-else.

### Unit 9 — Optimization and bio-inspired algorithms

- [[optimization-problems]] — An optimization problem asks for the state that maximises or minimises an objective function; key ideas are the landscape, global vs local optima, continuous vs combinatorial spaces and constraints.
- [[exploration-vs-exploitation]] — The trade-off between searching new regions (exploration) and refining known good solutions (exploitation), and how each unit-9 algorithm balances it.
- [[hill-climbing]] — Hill climbing is greedy local search that repeatedly moves to a better neighbour; fast and memory-light but stuck at local optima, plateaus and ridges unless helped by sideways moves, randomness or restarts.
- [[gradient-descent]] — Gradient descent minimises a differentiable function by repeatedly stepping against the gradient, w ← w − η∇f(w); the step size η controls speed and stability.
- [[simulated-annealing]] — Simulated annealing is stochastic local search that always accepts improvements and accepts worse moves with probability e^(−Δ/T), lowering the temperature T over time to move from exploration to exploitation.
- [[evolutionary-computation]] — Evolutionary computation is the family of population-based, stochastic generate-and-test algorithms (GA, ES, EP, GP and relatives) that optimise by repeated variation and selection.
- [[genetic-algorithms]] — A genetic algorithm evolves a population of (usually bit-string) chromosomes by fitness-based selection, crossover and mutation; Holland's classic EA and the course's main bio-inspired optimiser.
- [[schema-theory-and-building-blocks]] — Holland's schema theory explains GAs through schemata (bit patterns with * wildcards), implicit parallelism and the schema theorem, leading to the building block hypothesis; useful intuition with known limits.
- [[swarm-intelligence]] — Swarm intelligence is collective problem solving that emerges from many simple agents following local rules and sharing information directly or through the environment; PSO, ACO and ABC are its main optimisers.
- [[particle-swarm-optimization]] — Particle swarm optimization moves a swarm of particles through a continuous space, each velocity pulled at random toward the particle's personal best and the swarm's global best (Kennedy & Eberhart 1995).
- [[ant-colony-optimization]] — Ant colony optimization builds solutions with artificial ants that choose edges with probability ∝ τ^α·η^β and reinforce good tours with pheromone that evaporates over time (Dorigo's Ant System, 1996).
- [[artificial-bee-colony]] — The artificial bee colony algorithm (Karaboga 2007) optimises with employed, onlooker and scout bees — neighbourhood search around food sources, fitness-proportional recruitment, and random restarts after a limit of failures.

### Not taught yet

- [[upcoming-topics]] — Syllabus units not taught yet (planning, probability, Markov models, machine learning, ethics), with the textbook chapters to ingest when they arrive.

## Exam review

- [[unit-01-history-review]] — Unit 1 cheat sheet — definitions of AI, the four approaches, a dated milestone timeline, key people, eras and winters, slide errors to watch for, and 12 practice questions.
- [[unit-02-agents-review]] — Unit 2 cheat sheet — agent, agent function vs program, rationality, PEAS, the seven environment dimensions, the five agent designs, state representations, traps and 13 practice questions.
- [[unit-03-csp-review]] — Cheat sheet for constraint satisfaction problems (taught in unit 3) — definitions, backtracking, MRV/degree/LCV, forward checking, AC-3/MAC, min-conflicts, HW01 N-Queens and Sudoku numbers, traps and 12 practice questions.
- [[unit-03-search-review]] — Dense unit-3 cheat sheet on search — problem formulation, graph vs tree search, b/d/m criteria, properties of every algorithm, heuristic properties (admissible, consistent, dominance, relaxed problems, b*), early vs late goal test, HW01 numbers, traps and 14 practice questions.
- [[unit-04-games-review]] — Cheat sheet for unit 4, adversarial search — game formalism, minimax, alpha-beta and move ordering, H-MINIMAX with evaluation functions, MCTS/UCB1, chess vs Go facts, the 4x4 tic-tac-toe exercise, traps and 13 practice questions.
- [[unit-06-logic-prolog-review]] — Unit 5–6 cheat sheet — propositional and first-order logic, CNF and resolution, Horn clauses, forward/backward chaining, unification, Prolog syntax and execution (SLD), arithmetic, NAF, cut, Lab 01 — with 14 practice questions.
- [[unit-09-optimization-review]] — Unit 9 cheat sheet — optimization landscape, hill climbing, gradient descent, simulated annealing, GA, schema theorem, PSO, ACO and ABC with all update formulas, parameter effects, traps and 14 practice questions.

## Comparisons

- [[agent-types-comparison]] — Side-by-side comparison of simple reflex, model-based, goal-based, utility-based and learning agents — knowledge used, environments handled, strengths, limits and course examples.
- [[astar-vs-dijkstra]] — A* (f = g + h_SLD) vs Dijkstra / uniform-cost search (f = g) on the Romania map from Arad to Bucharest — both return the optimal 418, A* expands 5 non-goal nodes vs Dijkstra's 12, with full traces.
- [[chess-vs-go]] — Chess vs Go as AI search problems (HW01 research question) — same game class, but b≈35 vs ≈250, game trees 10^123 vs 10^360 and easy vs hard evaluation explain why alpha-beta won chess in 1997 while Go needed MCTS with neural networks (2016).
- [[csp-techniques-comparison]] — CSP solving techniques side by side — naive backtracking, MRV, degree, LCV, forward checking, AC-3/MAC and min-conflicts — with what each decides, its cost, and the HW01 Sudoku numbers.
- [[game-search-comparison]] — Side-by-side of minimax, alpha-beta, heuristic alpha-beta (H-MINIMAX with cutoff + EVAL) and Monte Carlo tree search — optimality, cost, what each needs, and when to use it.
- [[heuristics-8-puzzle-comparison]] — Misplaced tiles vs Euclidean vs Manhattan on the 8-puzzle — definitions, admissibility, dominance chain Manhattan ≥ Euclidean ≥ misplaced, and HW01 greedy results (123 < 413 < 1,134 expanded) alongside the textbook's A* data.
- [[logic-systems-comparison]] — Side-by-side of propositional logic, first-order logic, Horn/definite clauses and Prolog (expressiveness, decidability, inference, cost), plus a forward- vs backward-chaining table.
- [[metaheuristics-comparison]] — Side-by-side comparison of hill climbing, gradient descent, simulated annealing, GA, PSO, ACO and ABC — inspiration, representation, parameters, exploration/exploitation mechanisms, memory and typical problems.
- [[search-algorithms-comparison]] — Side-by-side table of every search algorithm in unit 3 — BFS, UCS, DFS, DLS, IDS, bidirectional, greedy, A*, weighted A*, beam, IDA* — by completeness, optimality, time, space, frontier and evaluation function, with HW01 usage.

## Your code

- [[ant-colony-py]] — Walkthrough of Raymond's Ant_colony.py — an ant-cycle Ant System for a random 25-city Euclidean TSP (100 ants, α=β=1, evaporation 0.5, Q=100, nearest-neighbour τ0) that beats the nearest-neighbour tour by 8–19%.
- [[genetic-algorithm-py]] — Walkthrough of Raymond's Genetic_algorithm.py — a 16-bit sign-magnitude GA with top-10 elitism and truncation selection that minimises (x+2)²+(y−2)²+10; usually exact in under 10 generations, but can stall on a Hamming cliff.
- [[gradient-descent-py]] — Walkthrough of the class exercise code gd_functions.py — gradient descent with η=0.1 on f=(x−2)²+(y+2)², which converges geometrically (error ×0.8 per step) to (2,−2) and hits a floating-point floor at iteration 161.
- [[hw01-ex01-8-puzzle]] — Walkthrough of HW01 Exercise 1 — 8-puzzle solved with BFS (optimal 20 moves), DFS (66,056) and greedy best-first with Manhattan, Euclidean and misplaced-tiles heuristics, all as graph search.
- [[hw01-ex02-80-tile]] — Walkthrough of HW01 Exercise 2 — the 9×9 "80-tile" puzzle with Manhattan distance; A* hits its 250,000-expansion cap, weighted A* (W=10) finds 1,116 moves, beam search finds 1,078 (k=500) and 740 (k=5000); optimum lies in [306, 740].
- [[hw01-ex03-n-queens]] — Walkthrough of HW01 Exercise 3 — N-Queens as a CSP solved by plain recursive backtracking, one queen per column, first 8-queens solution [0,4,7,5,2,6,1,3] after 113 placements.
- [[hw01-ex04-farmer-wolf-goat-cabbage]] — Walkthrough of HW01 Exercise 4 — the farmer, wolf, goat and cabbage river puzzle as a 4-boolean state space solved by BFS graph search in 7 crossings.
- [[hw01-ex05-missionaries-cannibals]] — Walkthrough of HW01 Exercise 5 — missionaries and cannibals with state (m_left, c_left, boat_left), five boat loads and a both-banks safety rule, solved by BFS in 11 crossings.
- [[hw01-ex06-sudoku]] — Walkthrough of HW01 Exercise 6 — Sudoku as a CSP solved by backtracking with switchable MRV, LCV and forward checking, compared on a 30-given and a 22-given board (MRV best; MRV+LCV even better in a re-run).
- [[lab01-family-pl]] — Walkthrough of Raymond's Lab 01 Prolog file — 16-person, 4-generation family KB with spouse/2, 17 rules (incl. uncle/aunt by marriage, cousin, father_in_law, descendant, terminating related/2) and 20 plunit tests (7 negative), all passing.
- [[particle-swarm-py]] — Walkthrough of Raymond's Particle_swarm.py — the original 1995 PSO (α1=α2=2, no inertia, no velocity clamp) on (x+2)²+(y−2)²+10; converges to f≈10.002 in ~20 iterations, then the swarm diverges.
- [[prolog-lecture-examples]] — Walkthrough of the seven lecture Prolog files in 01_Code — factorial, naive Fibonacci, isEven/isOdd, isPerm (set-equality bug), binary search tree (delete2 bug), N-queens, and predicates.pl (incl. isMerged = list interleaving) — with re-run results and bugs.
- [[simulated-annealing-py]] — Walkthrough of the class exercise code sa_functions.py — simulated annealing on 2-D Rastrigin whose 0.8-per-iteration cooling makes it a hill climber after ~50 of 100,000 iterations, yet still lands in the global basin.
- [[tic-tac-toe-4x4-py]] — Walkthrough of the class exercise tic-tac-toe.py — 4x4 tic-tac-toe where the AI (X, MAX) plays heuristic alpha-beta (H-MINIMAX) with a 7-ply cutoff, centre>corner>side move ordering and a 1/3/9 line-weight evaluation.

## Sources

- [[discussion-01-astar-vs-dijkstra]] — Raymond's class discussion comparing A* (straight-line-distance heuristic) with Dijkstra's algorithm on the Romania map, Arad to Bucharest — both find cost 418, A* with 5 expansions vs Dijkstra's 13.
- [[dorigo-1996-ant-system]] — Dorigo, Maniezzo & Colorni (1996) Ant System paper — transition rule, pheromone update with evaporation, ant-cycle vs ant-density vs ant-quantity, parameter study on Oliver30 TSP, elitist ants.
- [[eiben-smith-evolutionary-computing]] — Eiben & Smith, Introduction to Evolutionary Computing (2nd ed., 2015) — secondary textbook for EA components, operators, selection, the simple GA, PSO with inertia and schema theory.
- [[ga-exercise-explanation]] — Raymond's one-page write-up (17/09/2026) explaining his class-exercise genetic algorithm — encoding, elitism, crossover, mutation and the run that reached f = 10 by epoch 7.
- [[holland-1992-genetic-algorithms]] — Holland's 1992 Scientific American article on genetic algorithms — crossover, schemata, implicit parallelism, building blocks, exploration vs exploitation and classifier systems.
- [[hw01-ai-transcript]] — Transcript of Raymond's two AI-assistant exchanges for HW01 — Graphviz DOT syntax for drawing the 80-tile search tree, and a reading list of peer-reviewed sources for the chess-vs-Go research question.
- [[hw01-report]] — Raymond's Homework 1 report — a chess-vs-Go research essay plus six practical problems (8-puzzle, 80-tile, N-Queens, farmer, missionaries and cannibals, Sudoku) solved with BFS/DFS/greedy/A*/weighted A*/beam search and CSP backtracking.
- [[kennedy-eberhart-1995-pso]] — Kennedy & Eberhart's 1995 paper introducing particle swarm optimization, from bird-flocking simulations to the simplified velocity update with constant 2 and no inertia weight.
- [[lab01-prolog-family-report]] — Raymond's Lab 01 written report (docx/pdf, 2 pages) — run_tests screenshot plus a three-part analysis of why sibling/2 needs X \= Y, which rules return duplicate answers, and what the closed-world assumption silently claims.
- [[luger-ai-6e]] — Luger, Artificial Intelligence — Structures and Strategies for Complex Problem Solving, 6th ed. — secondary textbook; §14.2 (resolution, clause form) and §14.3 (Horn clauses, logic programs, Prolog semantics, closed world) read so far.
- [[russell-norvig-aima]] — Russell & Norvig, Artificial Intelligence - A Modern Approach, 4th ed. Global Edition (2021) - the course's base textbook, ingested chapter by chapter.
- [[slides-00-instructor-introduction]] — Opening deck by Daniel Riofrío with his profile, contact channels, the 10-unit syllabus and the grading scheme with assessment dates.
- [[slides-01-introduction-to-ai]] — Unit 1 deck: a timeline of AI from Talos and the Antikythera mechanism through the Turing test, Dartmouth, LISP, the perceptron, backpropagation, SVMs, deep learning and causal models.
- [[slides-02-problem-solving]] — The 25-slide Problem Solving deck — problem formulation, state space, uninformed search (BFS, DFS), informed search (greedy best-first, A*, heuristics), then adversarial search (minimax, alpha-beta) and CSPs; nine slides are image-only.
- [[slides-03-intelligent-agents]] — Unit 2 deck on intelligent agents — agent function vs program, vacuum world, rationality and performance measures, PEAS, environment properties, the four agent architectures and atomic/factored/structured states.
- [[slides-04-optimization]] — Lecture deck 04 "Optimization and Biology-Inspired Agents" — evolutionary computation history, GA, PSO, ACO and ABC; several key slides are image-only.
- [[slides-xx-logic-programming-prolog]] — Riofrío's 31-slide deck "Logic Programming with Prolog" — propositional → FOL → Horn clauses → Prolog, unification, SLD resolution, arithmetic, recursion, lists, NAF and cut, N-queens case study, debugging, and the Lab 01 assignment.

## People

- [[alain-colmerauer]] — French computer scientist who created Prolog with Philippe Roussel in Marseille in 1972, originally for natural-language parsing.
- [[alan-turing]] — British mathematician (1912–1954) who proposed the Turing test in 1950 and outlined machine learning, genetic algorithms and reinforcement learning as routes to AI.
- [[daniel-riofrio]] — Course instructor — PhD in Computer Science (UNM), works on computer optimization and applied ML, Director of Computer Science at USFQ; contact details and office hours.
- [[dervis-karaboga]] — Turkish engineer who proposed the artificial bee colony (ABC) algorithm, modelling employed, onlooker and scout honeybees.
- [[frank-rosenblatt]] — American psychologist who proposed the perceptron (1958), the first trainable neural-network model, whose limits were later exposed by Minsky and Papert.
- [[john-holland]] — Inventor of genetic algorithms (1975) and schema theory; author of the 1992 Scientific American article used in Unit 9.
- [[john-mccarthy]] — Coined "artificial intelligence", organised the 1956 Dartmouth workshop, designed LISP (1958) and proposed logic-based knowledge representation with the Advice Taker.
- [[judea-pearl]] — Computer scientist who brought probability into mainstream AI with Bayesian networks (1988) and developed the causal calculus over directed acyclic graphs; Turing Award 2011.
- [[kennedy-and-eberhart]] — James Kennedy (social psychologist) and Russell Eberhart (electrical engineer) introduced particle swarm optimization in 1995, inspired by bird flocking and fish schooling.
- [[marco-dorigo]] — Italian researcher who created ant colony optimization; the 1996 Ant System paper with Maniezzo and Colorni applies pheromone-based search to the TSP.
- [[robert-kowalski]] — British logician who developed the theory of logic programming behind Prolog, the procedural reading of Horn clauses and the equation "Algorithm = Logic + Control" (1979).
