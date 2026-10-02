---
type: concept
summary: Simulated annealing is stochastic local search that always accepts improvements and accepts worse moves with probability e^(−Δ/T), lowering the temperature T over time to move from exploration to exploitation.
unit: 9
tags: [local-search, optimization, stochastic, metaheuristics]
sources: ["[[russell-norvig-aima]]", "[[dorigo-1996-ant-system]]"]
updated: 2026-10-01
---

# Simulated annealing

**Simulated annealing (SA)** is [[hill-climbing]] with controlled randomness. It proposes a
random neighbour; if the neighbour is better it moves there, and if it is worse it still moves
with a probability that shrinks with how much worse it is and with a "temperature" $T$ that
decreases over time. The metaphor is metallurgical annealing — heat a metal and cool it slowly
so it settles into a low-energy crystal — or shaking a bumpy surface hard at first, then gently,
so a ball escapes shallow dips but stays in the deepest one ([[russell-norvig-aima]] §4.1.2).
First described by Kirkpatrick et al. (1983), borrowing the Metropolis algorithm (1953)
([[russell-norvig-aima]] Ch. 4 notes, p. 160).

## How it works

R&N's version ([[russell-norvig-aima]] Fig. 4.5, Global Ed., as extracted):

```text
function SIMULATED-ANNEALING(problem, schedule) returns a solution state
    current ← problem.INITIAL
    for t = 1 to ∞ do
        T ← schedule(t)
        if T = 0 then return current
        next ← a randomly selected successor of current
        ΔE ← VALUE(current) − VALUE(next)
        if ΔE > 0 then current ← next
        else current ← next only with probability e^(ΔE/T)
```

**Sign conventions — learn them once.** Whatever the convention, the probability of accepting
a *worse* move is $e^{-|\text{worsening}|/T} < 1$.

| Convention | Define | Accept if | Else accept with prob. |
|---|---|---|---|
| Minimise cost $c$ (code, [[simulated-annealing-py]]) | $\Delta = c(\text{next}) - c(\text{current})$ | $\Delta < 0$ | $e^{-\Delta/T}$ |
| R&N Global Ed. Fig. 4.5 (VALUE read as a cost — the text has just "switched our point of view… to gradient descent") | $\Delta E = \text{VALUE(current)} - \text{VALUE(next)}$ | $\Delta E > 0$ | $e^{\Delta E/T}$ |
| Maximise value $v$ (classic textbook form, general knowledge) | $\Delta E = v(\text{next}) - v(\text{current})$ | $\Delta E > 0$ | $e^{\Delta E/T}$ |

All three are the same rule: in each, "accept" means the move improves, and the exponent is
negative exactly when the move is worse.

**Cooling schedules.** Geometric $T_{k+1} = a\,T_k$ ($a$ close to 1, e.g. 0.99 in Dorigo's SA
baseline, [[dorigo-1996-ant-system]] §VI-B); linear; logarithmic $T_k = c/\ln(k+1)$ (slow, has
the theoretical guarantee — general knowledge).

## Properties

- **Convergence guarantee.** If $T$ is lowered slowly enough, the Boltzmann distribution
  $e^{\Delta E/T}$ concentrates on the global optima, so SA finds a global optimum with
  probability approaching 1 ([[russell-norvig-aima]] §4.1.2). "Slowly enough" is impractically
  slow; real schedules trade this guarantee for speed.
- **Limits:** $T \to \infty$ ⇒ random walk (accepts everything); $T \to 0$ ⇒ first-choice /
  stochastic hill climbing (accepts only improvements).
- **Parameters:** initial temperature $T_0$, cooling rule/rate, neighbourhood (step size),
  number of iterations (optionally several per temperature), stopping rule.
- **Memory:** one current state, plus usually a separately tracked best-so-far.
- Applications: VLSI layout since the 1980s, factory scheduling ([[russell-norvig-aima]]
  §4.1.2). In Dorigo's Oliver30 comparison SA was worst of three: best 422, mean 459.8 (sd
  25.1) vs 420.4 for the Ant System ([[dorigo-1996-ant-system]] §VI-B).

## In this course

- Not on the optimization slides ([[slides-04-optimization]]); comes from R&N §4.1.2 and the
  class exercise code [[simulated-annealing-py]] (Rastrigin 2-D on $[-5.12, 5.12]^2$, step
  $U(-1,1)$ per coordinate, $T_0 = 100$, $T \leftarrow 0.8\,T$ every iteration, 100,000
  iterations).
- That schedule is far too fast: $T < 10^{-3}$ after 52 iterations, so for 99.9% of the run
  the code is a first-choice hill climber. It still lands in the global basin in every re-run
  (best $f \approx 10^{-4}$–$4\times10^{-3}$), because a step of up to ±1 can hop between
  neighbouring Rastrigin basins. Details and the floating-point surprise ($T$ never reaches 0;
  it freezes at $10^{-323}$) are on [[simulated-annealing-py]].

## Common mistakes

- Getting the sign of the exponent wrong and accepting *bad* moves with probability > 1 or
  good ones with probability < 1.
- Cooling geometrically every single proposal with a small factor like 0.8 — the "annealing"
  is over before it begins. Typical rates are 0.95–0.999, often with many proposals per
  temperature (general knowledge).
- Reporting the final *current* state instead of the best state seen.
- Dividing by $T$ when $T = 0$ (R&N's pseudocode returns before that happens).

## Related

[[hill-climbing]], [[gradient-descent]], [[optimization-problems]],
[[exploration-vs-exploitation]], [[genetic-algorithms]], [[metaheuristics-comparison]],
[[simulated-annealing-py]].

## Practice questions

> [!question]- Q1. Minimising cost, the current state costs 12 and a random neighbour costs 15. What is the acceptance probability at $T = 10$, $T = 3$ and $T = 0.5$?
> **Answer.** $\Delta = 15 - 12 = 3 > 0$ (worse). $P = e^{-3/T}$: $T=10$: $e^{-0.3} \approx 0.741$;
> $T=3$: $e^{-1} \approx 0.368$; $T=0.5$: $e^{-6} \approx 0.0025$. If the neighbour cost 9
> instead, it is accepted with probability 1.

> [!question]- Q2. Show that the acceptance rule in [[simulated-annealing-py]] is the same as R&N's Fig. 4.5.
> **Answer.** The code uses $\Delta = c(\text{new}) - c(\text{cur})$ and accepts if $\Delta < 0$,
> else with $e^{-\Delta/T}$. R&N (Global Ed.) uses $\Delta E = \text{VALUE(cur)} -
> \text{VALUE(next)} = -\Delta$ when VALUE is a cost, accepts if $\Delta E > 0 \iff \Delta < 0$,
> else with $e^{\Delta E/T} = e^{-\Delta/T}$. Identical ([[russell-norvig-aima]] Fig. 4.5).

> [!question]- Q3. What does SA become as $T \to \infty$ and as $T \to 0$?
> **Answer.** $T \to \infty$: $e^{-\Delta/T} \to 1$, every move accepted — a random walk.
> $T \to 0$: worse moves essentially never accepted — stochastic (first-choice) hill climbing
> ([[russell-norvig-aima]] §4.1.2).

> [!question]- Q4. With $T_0 = 100$ and $T_{k+1} = 0.8\,T_k$, after how many updates is $T < 1$? Is this a reasonable schedule for 100,000 iterations?
> **Answer.** Need $100 \cdot 0.8^k < 1 \Rightarrow k > \ln(0.01)/\ln(0.8) \approx 20.6$, so 21
> updates. No: the exploratory phase is ~20–50 iterations out of 100,000; the rest is hill
> climbing. A factor like $0.9999$ (≈ 46,000 iterations to drop from 100 to 1) would spread the
> cooling over the run ([[simulated-annealing-py]]).

> [!question]- Q5. Why does SA keep track of a separate "best so far"?
> **Answer.** Because it deliberately accepts worse states, the current state at the end can be
> worse than one visited earlier; storing the best seen costs one extra state and guarantees the
> reported answer is the best evaluated.
