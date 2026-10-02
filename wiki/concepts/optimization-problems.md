---
type: concept
summary: An optimization problem asks for the state that maximises or minimises an objective function; key ideas are the landscape, global vs local optima, continuous vs combinatorial spaces and constraints.
unit: 9
tags: [optimization, local-search, landscape]
sources: ["[[slides-04-optimization]]", "[[russell-norvig-aima]]", "[[eiben-smith-evolutionary-computing]]"]
updated: 2026-10-01
---

# Optimization problems

An **optimization problem** asks for the best state according to an **objective function**,
not for a path to a goal. You care only about the final configuration (where to put eight
queens, which tour to drive, which weights to use), so the algorithm can move freely among
complete candidate solutions and keep almost nothing in memory. This is the setting for
local search and for every bio-inspired method in unit 9 ([[russell-norvig-aima]] §4.1;
[[slides-04-optimization]], slide 3).

## How it works

Formally: given a search space $S$ and an objective $f: S \to \mathbb{R}$, find
$$x^* = \arg\max_{x \in S} f(x) \quad \text{or} \quad x^* = \arg\min_{x \in S} f(x).$$
Switching between the two is trivial: $\min f = -\max(-f)$; EAs usually maximise a
**fitness** that is the objective or a simple transform of it (e.g. $1/(1+f)$ or $M - f$)
([[eiben-smith-evolutionary-computing]] §3.2.2, §3.4.1).

**State-space landscape** ([[russell-norvig-aima]] §4.1, Fig. 4.1): imagine each state as a
location and $f$ as its elevation.

| Feature | Meaning | Why it hurts greedy search |
|---|---|---|
| Global maximum/minimum | Best point overall | The target |
| Local maximum/minimum | Better than all neighbours, not best overall | Greedy search stops there |
| Plateau / flat local max | Flat region with no uphill exit | No gradient signal |
| Shoulder | Flat region with an uphill exit | Progress possible only with sideways moves |
| Ridge | Sequence of local maxima not directly connected | All single moves look downhill |

**Kinds of spaces.**
- *Combinatorial / discrete*: permutations, bit strings, assignments — TSP, n-queens, knapsack,
  job-shop scheduling. Neighbourhoods are defined by moves (swap two cities, flip a bit).
- *Continuous*: $x \in \mathbb{R}^n$ — infinite branching factor; use gradients
  ([[gradient-descent]]), discretisation, or randomly sampled steps
  ([[russell-norvig-aima]] §4.2).
- *Constrained*: solutions must satisfy hard constraints; linear programming is the best-known
  tractable class ([[russell-norvig-aima]] §4.2).

**Benchmark functions used in this course.**
- Shifted paraboloids: $(x+2)^2 + (y-2)^2 + 10$ ([[genetic-algorithm-py]],
  [[particle-swarm-py]]) and $(x-2)^2 + (y+2)^2$ ([[gradient-descent-py]]) — unimodal, one
  minimum.
- Rastrigin: $f(x) = 10n + \sum_i \left(x_i^2 - 10\cos 2\pi x_i\right)$ on $[-5.12, 5.12]^n$
  — global minimum 0 at the origin, with a grid of local minima near integer points (general
  knowledge); used in [[simulated-annealing-py]].
- Ackley — also minimum 0 at the origin, nearly flat outer region with a central funnel
  (general knowledge); defined but unused in [[simulated-annealing-py]].
- Schaffer f6 — highly multimodal GA benchmark used in [[kennedy-eberhart-1995-pso]] §5.
- Euclidean TSP — combinatorial; Oliver30 in [[dorigo-1996-ant-system]]; random 25-city
  instances in [[ant-colony-py]].

## Properties

- **Local search** keeps one (or a few) current states, uses little memory, and works in huge
  or infinite spaces, but is **not systematic** — it may never look where the optimum is
  ([[russell-norvig-aima]] §4.1).
- **Unimodal vs multimodal.** On unimodal problems a greedy method suffices; multimodal
  problems need a mechanism to escape local optima — randomness, a population, or both (see
  [[exploration-vs-exploitation]]).
- NP-hard problems typically have exponentially many local optima
  ([[russell-norvig-aima]] §4.1.1).
- **No Free Lunch.** No operator or algorithm is best on all problems
  ([[eiben-smith-evolutionary-computing]] §4.2.2, citing the NFL theorem).

## In this course

- The slides frame optimisation as finding global optima "and avoid[ing] confusing them with
  local points", and motivate evolution as a way to do it: treat each point as an individual
  and let only those converging on global optima survive ([[slides-04-optimization]],
  slide 3).
- Raymond's three class programs all minimise a 2-D paraboloid or a TSP tour:
  [[genetic-algorithm-py]], [[particle-swarm-py]], [[ant-colony-py]]. The class exercise code
  [[simulated-annealing-py]] and [[gradient-descent-py]] cover the single-solution methods.

## Common mistakes

- Calling every local search "optimal": none of the unit-9 metaheuristics guarantees the
  global optimum in finite time.
- Mixing max and min conventions mid-derivation (fitness "higher is better" vs objective
  "lower is better"). [[genetic-algorithm-py]] calls its objective "fitness" while minimising
  it.
- Forgetting that a discretised encoding (bit strings with step 0.1) can only reach grid
  points — the optimum is found exactly only if it lies on the grid.

## Related

[[hill-climbing]], [[gradient-descent]], [[simulated-annealing]], [[beam-search]],
[[evolutionary-computation]], [[swarm-intelligence]], [[metaheuristics-comparison]],
[[problem-formulation]], [[state-space-and-graph-search]], [[constraint-satisfaction-problems]].

## Practice questions

> [!question]- Q1. What distinguishes an optimization problem from the search problems of unit 3?
> **Answer.** In unit-3 search the solution is a *path* (sequence of actions) to a goal; in an
> optimization problem only the *final state* matters and its quality is measured by an
> objective function. That is why local search can forget the path and keep just a current
> state ([[russell-norvig-aima]] §4.1).

> [!question]- Q2. Define local maximum, plateau, shoulder and ridge.
> **Answer.** Local maximum: higher than all neighbours but below the global maximum. Plateau:
> a flat area; if there is no uphill exit it is a flat local maximum, if there is one it is a
> shoulder. Ridge: a sequence of local maxima not directly connected, so every available move
> goes downhill ([[russell-norvig-aima]] §4.1.1, Figs. 4.1, 4.4).

> [!question]- Q3. Convert "minimise $f(x)=(x-3)^2+1$" into a non-negative fitness to maximise, and give the fitness of $x=1$ and $x=3$.
> **Answer.** One option: $\text{fit}(x) = 1/(1+f(x))$ (always in $(0,1]$ because $f \ge 1 > 0$).
> $f(1) = 5 \Rightarrow \text{fit} = 1/6 \approx 0.167$; $f(3) = 1 \Rightarrow \text{fit} = 0.5$.
> Ranking is preserved: lower $f$ ⇒ higher fitness ([[eiben-smith-evolutionary-computing]] §3.2.2).

> [!question]- Q4. Evaluate the 2-D Rastrigin function at $(0,0)$ and $(1,0)$. Why is it a hard test?
> **Answer.** $f(0,0) = 20 + (0 - 10) + (0 - 10) = 0$. $f(1,0) = 20 + (1 - 10\cos 2\pi) + (0 - 10)
> = 20 + (1-10) - 10 = 1$. Near every integer point there is a local minimum, so a greedy
> method with small steps gets stuck in whichever basin it starts in (general knowledge).

> [!question]- Q5. The GA in [[genetic-algorithm-py]] encodes each variable with step 0.1. Could it find the minimum of $(x-0.25)^2$ exactly?
> **Answer.** No. Decoded values are multiples of 0.1, so the best it can reach is $x = 0.2$ or
> $0.3$ with $f = 0.0025$. The representation limits the attainable precision.
