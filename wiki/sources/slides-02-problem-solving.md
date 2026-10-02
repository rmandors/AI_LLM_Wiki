---
type: source
summary: The 25-slide Problem Solving deck — problem formulation, state space, uninformed search (BFS, DFS), informed search (greedy best-first, A*, heuristics), then adversarial search (minimax, alpha-beta) and CSPs; nine slides are image-only.
unit: [2, 3, 4]
tags: [slides, search, heuristics, games, csp]
sources: ["[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# Slides 02 — Problem Solving

**Bibliographic line.** Riofrío, D. *Problem Solving* (lecture slides, 25 slides). Artificial Intelligence, NRC 1651, USFQ, Fall 2026. File: `raw/Slides/02_Problem Solving.pptx`. Instructor: [[daniel-riofrio]].

**What it is.** The deck that covers syllabus unit 3 (heuristic search) and, compactly, unit 4 (adversarial search) and CSPs. It closely follows [[russell-norvig-aima]] Ch. 3 (search), Ch. 6 (games) and Ch. 5 (CSPs) of the Global Edition, but much more briefly: **uniform-cost search, iterative deepening, weighted A\*, beam search and heuristic properties are not on the slides** (or are image-only) and are filled from the textbook in this wiki.

## Key points

**Problem-solving agents and formulation (slides 2–5)**
- Slide 2: a goal-based agent that **formulates → searches → executes**; assumes an observable, deterministic, discrete, static environment; the solution is always a *sequence* of actions → [[problem-formulation]], [[intelligent-agents]].
- Slide 3: five components — initial state, actions, transition model `Result(s, a) → s'`, goal test, cost function; the first three define the state space → [[problem-formulation]].
- Slide 4: state space = graph (nodes = states, edges = actions with costs), never built explicitly, explored progressively → [[state-space-and-graph-search]].
- Slide 5: state graph vs search tree; repeated states cause infinite cycles; keep a **frontier** and an **explored set**; "without repeated-state control the algorithm may not terminate even when a solution exists" → [[state-space-and-graph-search]].

**Uninformed search (slides 6–10)**
- Slide 6: blind search knows only initial state, actions and goal test; algorithms differ in expansion order; four criteria: completeness, optimality, time, space → [[uninformed-search]].
- Slide 7: **BFS** — shallowest first, FIFO; complete; optimal (fewest steps, uniform costs); $O(b^d)$ time and space; frontier grows exponentially → [[breadth-first-search]].
- Slide 8: image-only.
- Slide 9: **DFS** — deepest first, LIFO; complete only with repeated-state control and a finite space; not optimal; $O(b^m)$ time, $O(b\cdot m)$ space → [[depth-first-search]].
- Slide 10: image-only.

**Informed search (slides 11–16)**
- Slide 11: informed search uses problem knowledge encoded in $h(n)$; $h(n) \ge 0$, $h(\text{goal}) = 0$; a good heuristic dramatically reduces nodes explored → [[informed-search]], [[heuristic-functions]].
- Slide 12: "**Best-First Search**" = greedy: priority queue on $h(n)$; complete only with repeated-state control; not optimal; can be trapped by a misleading heuristic → [[greedy-best-first-search]].
- Slide 13: image-only.
- Slide 14: **A\*** — $f(n) = g(n) + h(n)$; priority queue on $f$; complete "if $h$ is admissible"; optimal if $h$ admissible/consistent; space $O(b^d)$; time depends on $h$ → [[a-star]].
- Slide 15: image-only.
- Slide 16: title "**Properties of Heuristics**" only; body image-only → filled from [[russell-norvig-aima]] §3.5–3.6 on [[heuristic-functions]].

**Adversarial search (slides 17–22)** — owned by the games pages
- Slide 17: two agents with opposing objectives (MAX, MIN), zero-sum, perfect information, deterministic → [[adversarial-search]].
- Slide 18: **Minimax** — recursive definition (Utility at terminals, max/min over successors); $O(b^m)$ time, $O(bm)$ space → [[minimax]].
- Slide 19: image-only.
- Slide 20: **Alpha–beta** — same result as minimax with far fewer nodes; best case $O(b^{m/2})$; α = best for MAX (lower bound), β = best for MIN (upper bound); prune rules → [[alpha-beta-pruning]].
- Slides 21–22: image-only.
- Comparison: [[game-search-comparison]]; research question in HW01: [[chess-vs-go]]; review: [[unit-04-games-review]].

**Constraint satisfaction (slides 23–25)** — owned by the CSP pages
- Slide 23: in CSPs states have internal structure (variables + values + constraints); solved by a complete and consistent assignment; examples Sudoku and a school schedule → [[constraint-satisfaction-problems]].
- Slide 24: variables $X$, domains $D$, constraints $C$; consistent vs complete assignment; constraint propagation: **forward checking**, **arc consistency**, **MRV** → [[constraint-propagation]], [[csp-heuristics]], [[csp-backtracking-search]].
- Slide 25: image-only (empty in the extraction).
- Comparison: [[csp-techniques-comparison]]; review: [[unit-03-csp-review]].

## Pages that use this source

[[problem-formulation]] · [[state-space-and-graph-search]] · [[uninformed-search]] · [[breadth-first-search]] · [[depth-first-search]] · [[informed-search]] · [[greedy-best-first-search]] · [[a-star]] · [[heuristic-functions]] · [[search-algorithms-comparison]] · [[unit-03-search-review]] · [[adversarial-search]] · [[minimax]] · [[alpha-beta-pruning]] · [[constraint-satisfaction-problems]] · [[constraint-propagation]] · [[csp-heuristics]] · [[unit-04-games-review]] · [[unit-03-csp-review]] · [[midterm-01-review]] · [[overview]]

## Issues found

- **Image-only slides (no text extracted): 8, 10, 13, 15, 16 (title only), 19, 21, 22, 25.** Their content (probably search-tree diagrams, the Romania A* trace, heuristic properties, game trees and pruning examples) is unknown; this wiki does not guess and fills the topics from [[russell-norvig-aima]].
- **A\* completeness** (slide 14) is tied to admissibility; the book says A* is complete regardless of admissibility (with positive costs and finite $b$) — admissibility matters for *optimality* ([[russell-norvig-aima]] §3.5.2). Flagged on [[a-star]].
- **"Best-First Search"** (slide 12) names the *greedy* algorithm; in the book best-first search is the general scheme (Fig. 3.7) and greedy is one instance (§3.5.1). Watch the terminology on exams.
- **Greedy completeness** (slide 12): "only when repeated states are controlled" — the book adds "and the state space is finite" (§3.5.1).
- **Explored set** (slide 5): the book uses *reached* (frontier ∪ expanded) and calls "closed list" a less appropriate term (§3.3, fn. 5). Same idea.
- Slide 2 lists four environment assumptions; the book also assumes **known**, **single-agent** and **episodic** (Ch. 3 intro).
- Missing from the slides but used in HW01: uniform-cost search, iterative deepening, weighted A*, beam search ([[hw01-report]]).
