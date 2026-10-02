---
type: concept
summary: Hill climbing is greedy local search that repeatedly moves to a better neighbour; fast and memory-light but stuck at local optima, plateaus and ridges unless helped by sideways moves, randomness or restarts.
unit: 9
tags: [local-search, optimization, greedy]
sources: ["[[russell-norvig-aima]]", "[[holland-1992-genetic-algorithms]]"]
updated: 2026-10-01
---

# Hill climbing

**Hill climbing** (greedy local search) keeps a single current state and repeatedly replaces
it by a better neighbour, stopping when no neighbour is better. It looks only one step ahead —
"like trying to find the top of Mount Everest in a thick fog while suffering from amnesia"
([[russell-norvig-aima]] §4.1.1). When the objective is a cost to minimise, the same idea is
called descent; with gradients in continuous space it becomes [[gradient-descent]].

## How it works

Steepest-ascent version ([[russell-norvig-aima]] Fig. 4.2):

```text
function HILL-CLIMBING(problem) returns a local maximum
    current ← problem.INITIAL
    loop
        neighbor ← highest-valued successor of current
        if VALUE(neighbor) ≤ VALUE(current) then return current
        current ← neighbor
```

Variants ([[russell-norvig-aima]] §4.1.1):
- **Sideways moves**: allow equal-value moves to cross shoulders; cap them (e.g. 100) to avoid
  wandering forever on a flat maximum.
- **Stochastic hill climbing**: choose randomly among uphill moves (probability can depend on
  steepness).
- **First-choice hill climbing**: generate random successors until one is better — good when
  there are thousands of successors (or infinitely many, as in continuous spaces).
- **Random-restart hill climbing**: repeat from random initial states until a goal is found;
  complete with probability 1. Expected restarts $= 1/p$ for per-run success probability $p$.

## Properties

- **Complete?** No (basic version). Random restarts make it complete with probability 1.
- **Optimal?** No — it returns a local optimum.
- **Memory** $O(1)$ states; **time** per step = cost of generating and evaluating the
  neighbourhood.
- **8-queens numbers** (complete-state formulation, 56 successors per state, $8^8 \approx 17$
  million states): steepest ascent solves **14%** of random instances (4 steps when it succeeds,
  3 when stuck); allowing up to 100 sideways moves raises this to **94%** (21 steps on success,
  64 on failure). Random restart needs about $1/0.14 \approx 7$ runs ≈ 22 steps, or ≈ 25 steps
  with sideways moves ([[russell-norvig-aima]] §4.1.1).
- Failure modes: local maxima, ridges, plateaus ([[optimization-problems]]).

## In this course

- The course slides do not have a hill-climbing slide; it is the baseline every unit-9
  algorithm improves on. Holland contrasts it with GAs: on landscapes with many peaks, tunnels
  and bridges, "finding the right hill or even determining which way is up becomes
  increasingly difficult" ([[holland-1992-genetic-algorithms]], p. 67).
- [[simulated-annealing]] is "a version of stochastic hill climbing where some downhill moves
  are allowed" ([[russell-norvig-aima]] Fig. 4.5). Raymond's class exercise code
  [[simulated-annealing-py]] cools so fast that after about 50 iterations it *is* a
  first-choice hill climber with random steps in $[-1, 1]^2$.
- [[beam-search]] (local beam search) runs $k$ hill climbers that share information;
  [[genetic-algorithms]] add crossover to stochastic beam search.
- HW01's [[hw01-ex03-n-queens]] solves n-queens with an *incremental* formulation (place one
  queen per column); hill climbing instead uses R&N's *complete-state* formulation (all 8 queens
  on the board, move one within its column).
- R&N's bibliographic notes: most comparisons find GAs *slower* to converge than stochastic
  hill climbing ([[russell-norvig-aima]] Ch. 4 notes, p. 161).

## Common mistakes

- Saying hill climbing "backtracks" — it does not; it keeps no history.
- Treating random-restart hill climbing as parallel beam search: restarts are independent,
  beam search shares information ([[russell-norvig-aima]] §4.1.3).
- Allowing unlimited sideways moves: on a true flat maximum the search never terminates.

## Related

[[optimization-problems]], [[gradient-descent]], [[simulated-annealing]], [[beam-search]],
[[genetic-algorithms]], [[greedy-best-first-search]], [[heuristic-functions]],
[[exploration-vs-exploitation]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Is hill climbing complete? Optimal? What changes with random restarts?
> **Answer.** Basic hill climbing is neither complete nor optimal — it stops at the first local
> optimum. Random-restart hill climbing is complete with probability 1, because eventually a
> random initial state is itself a goal ([[russell-norvig-aima]] §4.1.1).

> [!question]- Q2. A single hill-climbing run succeeds with probability $p = 0.2$. A successful run takes 5 steps and a failed one 4 steps. What is the expected number of runs and of steps for random-restart hill climbing?
> **Answer.** Expected runs $= 1/p = 5$ (4 failures + 1 success). Expected steps $= 5 + \frac{1-p}{p}\cdot 4 = 5 + 4\cdot 4 = 21$, using R&N's formula "cost of one success plus $(1-p)/p$ times the cost of failure" ([[russell-norvig-aima]] §4.1.1).

> [!question]- Q3. Why do ridges defeat hill climbing even when the ridge rises steadily?
> **Answer.** The ridge's rising direction is not aligned with any single available move; from
> each point on it, every one-variable move goes downhill, so each point looks like a local
> maximum ([[russell-norvig-aima]] Fig. 4.4).

> [!question]- Q4. When is first-choice hill climbing preferable to steepest ascent?
> **Answer.** When a state has very many successors (thousands, or infinitely many in a
> continuous space): evaluating all of them each step is expensive, while sampling until one
> improves is cheap ([[russell-norvig-aima]] §4.1.1).

> [!question]- Q5. On 8-queens, sideways moves raise the success rate from 14% to 94% but raise steps per success from 4 to 21. Which random-restart variant needs fewer total steps?
> **Answer.** With sideways moves: $1\cdot 21 + (0.06/0.94)\cdot 64 \approx 25$ steps. Without:
> $4 + (0.86/0.14)\cdot 3 \approx 22$ steps. Both are cheap; R&N quote ≈22 vs ≈25
> ([[russell-norvig-aima]] §4.1.1).
