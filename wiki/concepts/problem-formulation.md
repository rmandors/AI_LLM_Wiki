---
type: concept
summary: How a problem-solving agent turns a task into a search problem — initial state, actions, transition model, goal test and action cost — at the right level of abstraction.
unit: [2, 3]
tags: [search, problem-solving-agent, formulation, abstraction]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Problem formulation

A **problem-solving agent** is a goal-based agent ([[agent-architectures]]) that, before acting, builds an abstract model of the task and *searches* that model for a sequence of actions reaching a goal. **Problem formulation** is the step that writes this model down: what a state is, where we start, what we can do, what each action does, when we are done and what each action costs. The output of search is always a **sequence of actions**, never a single action ([[slides-02-problem-solving]], slide 2).

## How it works

The four-phase process ([[russell-norvig-aima]] §3.1): **goal formulation → problem formulation → search → execution**. The slides compress it into "formulate, search, execute" ([[slides-02-problem-solving]], slide 2).

A search problem has five components ([[slides-02-problem-solving]], slide 3; [[russell-norvig-aima]] §3.1.1):

| Component | Notation | Romania example | 8-puzzle example |
|---|---|---|---|
| Initial state | $s_0$ | `In(Arad)` | any board, e.g. `7 2 4 / 5 _ 6 / 8 3 1` |
| Actions | $\text{ACTIONS}(s)$ | `{ToSibiu, ToTimisoara, ToZerind}` | blank moves Up/Down/Left/Right (if on board) |
| Transition model | $\text{RESULT}(s,a) = s'$ | `RESULT(Arad, ToZerind) = Zerind` | swap blank with neighbour |
| Goal test | $\text{IS-GOAL}(s)$ | `s = Bucharest` | `s = 1 2 3 / 4 5 6 / 7 8 _` |
| Action cost | $c(s,a,s')$ | road length in miles | 1 per move |

Together the initial state, actions and transition model **define the state space** implicitly ([[slides-02-problem-solving]], slide 3) — see [[state-space-and-graph-search]]. A **path** is a sequence of actions; a **solution** is a path to a goal; an **optimal solution** has the lowest path cost (costs are additive and assumed positive) ([[russell-norvig-aima]] §3.1.1).

**Abstraction.** A formulation is a model, not reality. It is *valid* if every abstract solution can be refined into a real one, and *useful* if each abstract action is easy to carry out ([[russell-norvig-aima]] §3.1.2). Example: "drive Arad → Sibiu" ignores the radio, the weather, the road condition.

## Properties

- The environment is assumed **fully observable, deterministic, discrete, static** (and known, single-agent) ([[slides-02-problem-solving]], slide 2; [[russell-norvig-aima]] Ch. 3 intro). Then the solution is an **open-loop** plan: execute it with "eyes closed" ([[russell-norvig-aima]] §3.1). See [[environment-properties]].
- Problem-solving agents use **atomic** states (no internal structure visible to the algorithm); factored states lead to CSPs and planning ([[russell-norvig-aima]] Ch. 3 intro; [[state-representation]], [[constraint-satisfaction-problems]]).
- The choice of state description decides the size of the state space. Smaller, non-redundant states → smaller search.

## In this course

- Slides 2–3 of [[slides-02-problem-solving]] give the five components; slide 4 introduces the state space.
- **HW01** formulates four path problems (see [[hw01-report]]):
  - **8-puzzle** ([[hw01-ex01-8-puzzle]]): state = flat tuple of 9 ints (0 = blank); actions move the blank (the book's own advice, [[russell-norvig-aima]] §3.2.1); cost 1. A parity check decides solvability first.
  - **80-tile puzzle** ([[hw01-ex02-80-tile]]): same model on 9×9; tile = `quadrant*9 + number`, one hole.
  - **Farmer, wolf, goat, cabbage** ([[hw01-ex04-farmer-wolf-goat-cabbage]]): state = 4 booleans; 16 tuples, 10 legal.
  - **Missionaries and cannibals** ([[hw01-ex05-missionaries-cannibals]]): state = `(m_left, c_left, boat_left)`; the right bank is implied (`3 - left`); 32 tuples, 20 legal, 16 reachable (verified by re-running the code, 2026-10-01).
- N-Queens and Sudoku in the same homework are *not* path problems — no path cost matters — so Raymond formulated them as CSPs ([[hw01-ex03-n-queens]], [[hw01-ex06-sudoku]]).

## Common mistakes

- Forgetting the **goal test** or the **cost function** — without the cost function "optimal" is undefined ([[slides-02-problem-solving]], slide 3).
- Redundant state descriptions (storing both banks in M&C) multiply the state space for nothing.
- Encoding illegal states as reachable and filtering too late — check legality on generation so the frontier holds only legal states (as Ex04/Ex05 do).
- Treating the solution as one action: in this framework it is always a plan (sequence).
- Mixing the **state space** (the problem) with the **search tree** (the process) — see [[state-space-and-graph-search]].

## Related

[[state-space-and-graph-search]] · [[uninformed-search]] · [[informed-search]] · [[intelligent-agents]] · [[rationality-and-peas]] · [[environment-properties]] · [[constraint-satisfaction-problems]] · [[unit-03-search-review]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. Name the five components of a search problem and say which three define the state space.
> **Answer.** Initial state, actions, transition model, goal test, action cost. Initial state + actions + transition model define the state space (all states reachable from the start) ([[slides-02-problem-solving]], slide 3).

> [!question]- Q2. Why does the 8-puzzle formulation move the *blank* rather than the tiles?
> **Answer.** It gives only 4 action names (Up/Down/Left/Right) instead of tile × direction, and applicability is easy to test from the blank's position ([[russell-norvig-aima]] §3.2.1). Raymond follows this in [[hw01-ex01-8-puzzle]].

> [!question]- Q3. In missionaries and cannibals, how many state tuples are there if you store only the left bank and the boat side? How many if you also stored the right bank explicitly?
> **Answer.** Left bank only: $4 \times 4 \times 2 = 32$ tuples (20 legal, 16 reachable). Storing the right bank too: $4^4 \times 2 = 512$ tuples, of which only the 32 with `right = 3 - left` are consistent — 16× more representable tuples for no information.

> [!question]- Q4. When is an abstraction "valid" and when is it "useful"?
> **Answer.** Valid: every abstract solution can be expanded into a real, detailed solution. Useful: each abstract action is easier to execute than the original problem (e.g. "drive to Sibiu" needs no further search) ([[russell-norvig-aima]] §3.1.2).

> [!question]- Q5. Under which environment assumptions is an open-loop plan safe?
> **Answer.** Fully observable, deterministic, known (and static) environments: once a solution is found, executing it without looking at percepts reaches the goal. With nondeterminism or partial observability you need a closed-loop/contingent plan ([[russell-norvig-aima]] §3.1; [[slides-02-problem-solving]], slide 2).
