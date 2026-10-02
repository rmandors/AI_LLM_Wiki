---
type: comparison
summary: Side-by-side comparison of simple reflex, model-based, goal-based, utility-based and learning agents — knowledge used, environments handled, strengths, limits and course examples.
unit: 2
tags: [agents, comparison, architectures]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Agent types comparison

The agent designs of [[agent-architectures]] form a ladder: each one adds a component that lets it handle a harder [[environment-properties|environment]]. This page puts them side by side ([[slides-03-intelligent-agents]], slides 14–17; [[russell-norvig-aima]] §2.4).

## What each agent knows and asks

| Type | Extra component | Question it answers | Decision rule |
|---|---|---|---|
| Simple reflex | Condition–action rules | "What is the world like *now* (from this percept)?" | First matching rule |
| Model-based reflex | Internal state + transition model + sensor model | "What is the world like now, including what I can't see?" | First rule matching the *estimated* state |
| Goal-based | Goals | "What will it be like if I do A? Does that reach my goal?" | Search/plan for an action sequence reaching a goal state |
| Utility-based | Utility function $U$ | "How happy will I be in that state?" | $\arg\max_a \sum_{s'} P(s'\mid s,a)U(s')$ |
| Learning (wrapper) | Learning element, critic, problem generator | "How can I do better next time?" | Whatever its performance element uses |

## Strengths, limits and fit

| Type | Advantage | Limitation | Minimum environment it needs | Course example |
|---|---|---|---|---|
| Simple reflex | Simple, fast, tiny (can be a Boolean circuit) | No memory; loops in partially observable worlds | Fully observable | Reflex vacuum (R&N Fig. 2.8) |
| Model-based reflex | Acts coherently without seeing everything | Rules still fixed; state is a guess | Partially observable OK | Taxi tracking cars in blind spots |
| Goal-based | Flexible: change the goal, not the rules | Goals are binary — can't rank paths | Sequential, needs a goal test | 8-puzzle / 80-tile solvers ([[hw01-ex01-8-puzzle]], [[hw01-ex02-80-tile]]), N-queens ([[hw01-ex03-n-queens]]) |
| Utility-based | Trades off conflicting goals; handles uncertainty | Utility hard to specify; maximising EU is costly | Stochastic, multi-objective | Game players with evaluation functions ([[tic-tac-toe-4x4-py]], [[minimax]]); optimisers with fitness ([[genetic-algorithms]]) |
| Learning | Works in unknown environments; improves past initial knowledge | Needs feedback and a fixed performance standard | Unknown environments | Samuel's checkers ([[history-of-ai]]); Unit 10 [[perceptron]] |

(Advantages/limitations from [[slides-03-intelligent-agents]] slides 14–17 and [[russell-norvig-aima]] §2.4; course-example mapping is the wiki's own classification.)

## When to use which

- **Fully observable, rules known, speed critical** (e.g. a thermostat, reflexive braking): simple reflex.
- **Partially observable but no need to plan ahead**: model-based reflex.
- **A clear goal test and a sequence of actions needed** (puzzles, route finding, CSPs): goal-based + [[uninformed-search]] / [[a-star]] / [[csp-backtracking-search]].
- **Several competing objectives or uncertain outcomes** (taxi speed vs safety, games with evaluation functions): utility-based.
- **Environment or performance measure unknown, or too complex to hand-code**: learning agent around any of the above.
- Rule of thumb: pick the *simplest* design that is rational in the environment — the reflex vacuum is rational under R&N's assumptions (§2.2.2).

## Practice questions

> [!question]- Q1. Which agent type is the minimum needed for each: (a) a thermostat; (b) the 8-puzzle solver; (c) a self-driving taxi choosing between fast and safe routes?
> **Answer.** (a) Simple reflex (current temperature suffices). (b) Goal-based (needs search to reach the goal configuration). (c) Utility-based (conflicting objectives under uncertainty), ideally with learning ([[russell-norvig-aima]] §2.4).

> [!question]- Q2. What single limitation of goal-based agents does the utility-based agent remove?
> **Answer.** Goals give only a binary happy/unhappy distinction; utility ranks states by how desirable they are, so the agent can prefer quicker, safer or cheaper solutions ([[slides-03-intelligent-agents]], slide 16–17; [[russell-norvig-aima]] §2.4.5).

> [!question]- Q3. Is a learning agent a separate rung on the ladder? Explain.
> **Answer.** No. Learning is a wrapper: any type (reflex, model-based, goal-based, utility-based) can be built as a learning agent whose learning element improves its performance element ([[russell-norvig-aima]] §2.4.6).

> [!question]- Q4. A simple reflex agent and a model-based reflex agent face a fully observable environment. Is there any benefit to the model?
> **Answer.** Little for tracking state, since the percept already contains everything relevant; the model adds cost without benefit. The model matters when the environment is partially observable ([[russell-norvig-aima]] §2.4.2–2.4.3).

> [!question]- Q5. Where does an A* agent sit on this table, and does its path cost make it utility-based?
> **Answer.** It is goal-based: it searches for a sequence reaching a goal test. Minimising path cost is a fixed performance criterion inside the problem definition, not a utility over outcome states under uncertainty — though it is a step toward utility (ranking solutions) ([[a-star]]; [[russell-norvig-aima]] §2.4.4).
