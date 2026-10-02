---
type: concept
summary: The artificial bee colony algorithm (Karaboga 2007) optimises with employed, onlooker and scout bees — neighbourhood search around food sources, fitness-proportional recruitment, and random restarts after a limit of failures.
unit: 9
tags: [artificial-bee-colony, swarm-intelligence, continuous, metaheuristics]
sources: ["[[slides-04-optimization]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Artificial bee colony (ABC)

The **artificial bee colony** algorithm is a [[swarm-intelligence]] optimiser by
[[dervis-karaboga]] (2007) that imitates honeybee foraging ([[slides-04-optimization]],
slide 16). Each **food source** is a candidate solution and its nectar amount is the solution's
fitness. Three kinds of bees share the work: **employed bees** search near their own source,
**onlooker bees** pick sources in proportion to their quality and search near them, and **scout
bees** abandon sources that stopped improving and look for new ones at random
([[slides-04-optimization]], slide 17). R&N list it among entomology-inspired methods, citing
Karaboga & Basturk (2007) ([[russell-norvig-aima]] Ch. 4 notes, p. 160).

> [!warning] Source gap
> No ABC paper is in `raw/`, and the slide-18 formula is an image that did not extract. The
> equations below are the standard ABC (general knowledge — verify against Karaboga & Basturk,
> 2007). Only the parameter list, the role split and the index ranges for $k$ and $j$ come from
> the slides.

## How it works

Parameters ([[slides-04-optimization]], slide 18): number of food sources $SN$ (= number of
employed bees = number of onlookers; the slide also writes BN), **limit**, and **MCN** (maximum
cycle number). Dimension $D$.

**1. Initialisation** (general knowledge): for $i = 1..SN$, $j = 1..D$,
$x_{ij} = x_j^{\min} + \text{rand}(0,1)\,(x_j^{\max} - x_j^{\min})$; set trial counters to 0.

**2. Employed bee phase.** For each source $i$, choose a random partner $k \in \{1, \dots,
SN\}$, $k \ne i$, and a random dimension $j \in \{1, \dots, D\}$ (the slide's "arbitrarily
selected indices"), then
$$v_{ij} = x_{ij} + \phi_{ij}\,(x_{ij} - x_{kj}), \qquad \phi_{ij} \sim U[-1, 1]$$
(all other coordinates copied from $x_i$). **Greedy selection**: keep $v_i$ if it is better,
reset trial$_i$ to 0; otherwise trial$_i$ += 1 (general knowledge).

**3. Fitness and onlooker probabilities** (general knowledge), for minimising $f$:
$$\text{fit}_i = \begin{cases} \dfrac{1}{1 + f_i} & f_i \ge 0 \\[4pt] 1 + |f_i| & f_i < 0 \end{cases}, \qquad p_i = \frac{\text{fit}_i}{\sum_{n=1}^{SN} \text{fit}_n}$$

**4. Onlooker bee phase.** Each onlooker picks a source $i$ by roulette wheel with $p_i$ and
performs the same neighbour search + greedy selection on it — good sources receive more
search effort (recruitment).

**5. Scout bee phase.** If trial$_i$ > limit, the source is abandoned and its employed bee
becomes a scout: $x_i$ is reinitialised randomly (one scout per cycle in the basic version —
general knowledge).

**6.** Memorise the best source; repeat from step 2 until MCN cycles.

```text
init SN random sources; trial ← 0
for cycle = 1..MCN:
    for i in 1..SN: employed: v ← neighbour(x_i); greedy(x_i, v)
    compute fit_i and p_i
    for each of SN onlookers: i ← roulette(p); v ← neighbour(x_i); greedy(x_i, v)
    if max trial_i > limit: scout: x_i ← random; trial_i ← 0
    record best
```

## Properties

- **Continuous** optimisation in its basic form (discrete variants exist — general knowledge).
- **Exploitation**: employed + onlooker local search; **exploration**: scouts
  ([[slides-04-optimization]], slide 17). The random $\phi \in [-1, 1]$ and the shrinking
  difference $x_{ij} - x_{kj}$ make step sizes adapt as sources converge (general knowledge).
- **Parameters:** $SN$, limit (a common choice is $SN \cdot D$), MCN — few to tune (general
  knowledge).
- **Recruitment rate**: how quickly the colony finds and exploits a new food source — an analogy
  for how fast good solutions are found ([[slides-04-optimization]], slide 18).
- **Memory:** sources and their trial counters; global best memorised.
- Not optimal-guaranteed; changes one coordinate per neighbour move, so it can be slow on
  strongly coupled (non-separable) variables (general knowledge).

## In this course

- Slides 16–18 are the only course material; Raymond has no ABC implementation in `raw/`
  ([[slides-04-optimization]], slides 16–18). Slide 19 is image-only.
- Compare with [[particle-swarm-optimization]] (all particles move every step, guided by
  pbest/gbest) and [[genetic-algorithms]] (onlooker selection is fitness-proportional selection;
  the scout phase is a built-in random restart).

## Common mistakes

- Forgetting $k \ne i$ (with $k = i$ the difference is 0 and the move does nothing).
- Using $\phi \in [0,1]$ (that only moves *away* from the partner); ABC uses $[-1, 1]$.
- Computing onlooker probabilities from raw cost (lower = better) instead of from the
  fitness transform.
- Mixing up the roles: scouts explore, employed/onlooker bees exploit.

## Related

[[swarm-intelligence]], [[particle-swarm-optimization]], [[ant-colony-optimization]],
[[genetic-algorithms]], [[exploration-vs-exploitation]], [[hill-climbing]], [[dervis-karaboga]],
[[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Name the three bee types and say which explore and which exploit.
> **Answer.** Employed bees and onlooker bees exploit (search near known food sources); scout
> bees explore (random new sources after abandonment) ([[slides-04-optimization]], slide 17).

> [!question]- Q2. What are ABC's three control parameters?
> **Answer.** The number of food sources $SN$ (= number of employed bees = number of onlookers),
> the **limit** of unsuccessful trials before a source is abandoned, and **MCN**, the maximum
> number of cycles ([[slides-04-optimization]], slide 18).

> [!question]- Q3. $x_i = (1.0, 2.0)$, partner $x_k = (3.0, -1.0)$, chosen $j = 2$, $\phi = -0.5$. Compute the candidate $v_i$.
> **Answer.** Only coordinate 2 changes: $v_{i2} = 2.0 + (-0.5)(2.0 - (-1.0)) = 2.0 - 1.5 = 0.5$.
> $v_i = (1.0, 0.5)$. It replaces $x_i$ only if it is better (general knowledge for the formula).

> [!question]- Q4. Three sources have costs $f = (0, 1, 3)$. Compute fitness and onlooker probabilities.
> **Answer.** $\text{fit} = 1/(1+f) = (1, 0.5, 0.25)$, sum 1.75. $p = (0.571, 0.286, 0.143)$. The
> best source gets four times as many onlookers on average as the worst (general knowledge for
> the transform).

> [!question]- Q5. What happens when a source's trial counter exceeds the limit, and why is that useful?
> **Answer.** The source is abandoned and replaced by a random new one (its bee becomes a scout).
> It stops wasting effort on an exhausted region and injects diversity — a built-in random
> restart that helps escape local optima.
