---
type: concept
summary: A genetic algorithm evolves a population of (usually bit-string) chromosomes by fitness-based selection, crossover and mutation; Holland's classic EA and the course's main bio-inspired optimiser.
unit: 9
tags: [genetic-algorithms, evolutionary-computation, metaheuristics]
sources: ["[[slides-04-optimization]]", "[[holland-1992-genetic-algorithms]]", "[[eiben-smith-evolutionary-computing]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Genetic algorithms

A **genetic algorithm (GA)** is the best-known [[evolutionary-computation]] method: candidate
solutions are encoded as **chromosomes** (classically bit strings), each is scored by a
**fitness function**, the fitter ones are more likely to become parents, and children are
produced by **crossover** (mixing two parents) and **mutation** (random bit flips). Repeating
this over generations concentrates the population in high-fitness regions
([[slides-04-optimization]], slides 5–6; [[holland-1992-genetic-algorithms]], p. 68). Invented
by [[john-holland]] in the 1960s–70s. R&N: "Genetic algorithms are similar to stochastic beam
search, but with the addition of the crossover operation" ([[russell-norvig-aima]] §4.1.4; see
[[beam-search]]).

## How it works

R&N's GA ([[russell-norvig-aima]] Fig. 4.8), one child per pair:

```text
function GENETIC-ALGORITHM(population, fitness) returns an individual
    repeat
        weights ← WEIGHTED-BY(population, fitness)
        population2 ← empty list
        for i = 1 to SIZE(population) do
            parent1, parent2 ← WEIGHTED-RANDOM-CHOICES(population, weights, 2)
            child ← REPRODUCE(parent1, parent2)
            if (small random probability) then child ← MUTATE(child)
            add child to population2
        population ← population2
    until some individual is fit enough, or enough time has elapsed
    return the best individual in population

function REPRODUCE(parent1, parent2)
    n ← LENGTH(parent1); c ← random number from 1 to n
    return APPEND(SUBSTRING(parent1, 1, c), SUBSTRING(parent2, c+1, n))
```

**Representation.** A chromosome is "a sequence of 1s and 0s representing a decimal number
encoded in binary" ([[slides-04-optimization]], slide 6). Decoding maps genotype → phenotype
(e.g. sign bit + magnitude, see [[genetic-algorithm-py]]). Standard binary has **Hamming
cliffs** (7 = `0111` → 8 = `1000` needs 4 flips); **Gray code** removes them
([[eiben-smith-evolutionary-computing]] §4.2). Other problems need other encodings: digit
strings for 8-queens ([[russell-norvig-aima]] Fig. 4.6), permutations for TSP/n-queens
([[eiben-smith-evolutionary-computing]] §3.4.1).

**Parent selection** ([[eiben-smith-evolutionary-computing]] §5.2):
- *Fitness-proportional (roulette wheel)*: $P(i) = f_i / \sum_j f_j$. Problems: a super-fit
  individual takes over early (premature convergence); little pressure when fitnesses are
  similar; result changes if $f$ is shifted by a constant.
- *Ranking*: probability depends on rank, not raw fitness.
- *Tournament*: pick $k$ at random, keep the best; larger $k$ = stronger pressure; needs only
  comparisons.
- *Truncation*: only the top fraction may reproduce (very strong pressure; used in EDAs,
  [[eiben-smith-evolutionary-computing]] §6.8, and in Raymond's code).

**Crossover (recombination)** ([[slides-04-optimization]], slide 6;
[[eiben-smith-evolutionary-computing]] §4.2.2): parents "exchange bit sections at the same
position".
- *Single (one)-point*: pick $r \in [1, l-1]$, swap tails → two children.
- *Two-/k-point*: alternate segments between $k$ cut points.
- *Uniform*: each gene independently from parent 1 or 2 (usually $p = 0.5$).
- One/k-point have **positional bias** (keep neighbouring genes together); uniform has
  **distributional bias** (tends to take ~50% from each parent).

**Mutation** — bit flip: each bit flips independently with probability $p_m$
([[slides-04-optimization]], slide 6); expected flips $= L \cdot p_m$. Common choice $p_m =
1/L$; classic range $1/L$ to $1/\mu$ ([[eiben-smith-evolutionary-computing]] §4.2.1, §6.1).
Holland: "roughly one in every 10,000 symbols", as insurance against a uniform population
([[holland-1992-genetic-algorithms]], p. 68).

**Survivor selection.** *Generational* (children replace everyone), *steady-state* (replace a
few), **elitism** (copy the best unchanged so overall best fitness never decreases), *culling*
(discard everything below a threshold) ([[russell-norvig-aima]] §4.1.4;
[[eiben-smith-evolutionary-computing]] §5.3.2).

**The simple GA (SGA)** — Table 6.1 of [[eiben-smith-evolutionary-computing]]: bit strings,
1-point crossover, bit-flip mutation, fitness-proportional selection by roulette wheel,
generational replacement, **no elitism**; $p_c \approx 0.6$–$0.8$, population 50–a few hundred.

## Properties

- **Not complete, not optimal**; anytime; stochastic (different runs, different answers).
- **Cost** per generation = population size × cost of one fitness evaluation (dominant in
  practice) + $O(\mu L)$ for operators.
- **Why crossover helps**: it combines useful **building blocks** found in different
  individuals — but only if blocks are meaningful and contiguous in the encoding; if gene
  positions are randomly permuted, crossover "conveys no advantage" ([[russell-norvig-aima]]
  §4.1.4; [[schema-theory-and-building-blocks]]).
- **Diversity dynamics**: early, a diverse population makes crossover take big steps; later,
  steps shrink as the population converges ([[russell-norvig-aima]] §4.1.4).
- **Selection pressure / takeover time**: FPS takeover time $\tau^* = \lambda \ln \lambda$
  (≈ 460 generations for $\lambda = 100$) ([[eiben-smith-evolutionary-computing]] §5.4);
  truncation and tournament are far faster.
- **Limit**: best at finding promising regions; fine-tuning a few variables is better left to
  standard local methods (hybrid/memetic approach) ([[holland-1992-genetic-algorithms]], p. 72).

## In this course

- Slide 5: GAs apply variation, selection and heredity; individuals are bit strings; fitness
  "seeks a point with a higher or lower value"; reproduction by crossover; mutation by flipping
  a bit with some probability ([[slides-04-optimization]], slide 5).
- Slide 6: chromosome, single/two/k-point crossover, per-bit mutation probability
  ([[slides-04-optimization]], slide 6). Slide 7 is image-only.
- Raymond's [[genetic-algorithm-py]] (write-up: [[ga-exercise-explanation]]): 16-bit sign +
  magnitude encoding, population 100, top-10 elitism, parents drawn only from the 10 elites,
  single-point crossover, bit-flip $p_m = 1/16$; minimises $(x+2)^2 + (y-2)^2 + 10$.
- R&N's 8-queens GA (digit strings, fitness = number of non-attacking pairs, max 28) is the
  bridge to HW01's [[hw01-ex03-n-queens]] ([[russell-norvig-aima]] Figs. 4.6–4.7).

## Common mistakes

- Using fitness-proportional selection on a *minimisation* objective or with negative values —
  transform first ([[eiben-smith-evolutionary-computing]] §5.1).
- Assuming mutation is always a "small" change: in binary, flipping a high-order bit is a huge
  jump.
- Forgetting that elitism is not part of the SGA.
- Choosing a crossover point of 0 or $l$ (no exchange) — the range is $[1, l-1]$.
- Using bit strings for real variables by default — "usually a mistake"; real-valued
  representations often work better ([[eiben-smith-evolutionary-computing]] §4.2).

## Related

[[evolutionary-computation]], [[schema-theory-and-building-blocks]], [[beam-search]],
[[hill-climbing]], [[simulated-annealing]], [[particle-swarm-optimization]],
[[exploration-vs-exploitation]], [[john-holland]], [[hw01-ex03-n-queens]],
[[genetic-algorithm-py]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Decode the chromosome `1001010000010100` using Raymond's encoding (per 8-bit half: sign bit, 1 = negative, then 7-bit magnitude ÷ 10). What is $f(x,y) = (x+2)^2 + (y-2)^2 + 10$?
> **Answer.** $x$-half `10010100`: sign 1 → negative; `0010100` = 20 → $x = -2.0$. $y$-half
> `00010100`: sign 0 → positive; `0010100` = 20 → $y = 2.0$. $f(-2, 2) = 0 + 0 + 10 = 10$ — the
> global minimum ([[genetic-algorithm-py]]).

> [!question]- Q2. Apply single-point crossover after bit 8 to P1 = `10010100 00010100` and P2 = `00001111 10000011`. Decode both children and compute $f$.
> **Answer.** C1 = `10010100 10000011` → $x = -2.0$, $y = -0.3$ (`0000011` = 3) →
> $f = 0 + (-2.3)^2 + 10 = 15.29$. C2 = `00001111 00010100` → $x = +1.5$ (`0001111` = 15),
> $y = 2.0$ → $f = 3.5^2 + 0 + 10 = 22.25$. Cutting at the gene boundary swaps whole variables;
> cutting inside a half recombines bits of one variable.

> [!question]- Q3. Four individuals have fitness 24, 23, 20, 11. What are their roulette-wheel selection probabilities?
> **Answer.** Sum = 78. $24/78 \approx 31\%$, $23/78 \approx 29\%$, $20/78 \approx 26\%$,
> $11/78 \approx 14\%$ — R&N's 8-queens example ([[russell-norvig-aima]] Fig. 4.6).

> [!question]- Q4. With 16-bit chromosomes and $p_m = 1/16$, what is the expected number of flipped bits per child, and the probability a child is not mutated at all?
> **Answer.** Expected flips $= 16 \cdot 1/16 = 1$. $P(\text{no flip}) = (15/16)^{16} \approx 0.356$.
> So about a third of the children are pure crossover products
> ([[eiben-smith-evolutionary-computing]] §4.2.1).

> [!question]- Q5. What does elitism guarantee, and what does it not guarantee?
> **Answer.** It guarantees the best fitness in the population never decreases (the best
> individual is copied unchanged) ([[russell-norvig-aima]] §4.1.4). It does not guarantee
> finding the global optimum, and with strong selection it speeds up loss of diversity.

> [!question]- Q6. R&N's parents `32752411` and `24748552` cross over after digit 3. What is the first child, and why can crossover be useful for 8-queens?
> **Answer.** `327` + `48552` = `32748552` ([[russell-norvig-aima]] Fig. 4.6). Useful because
> a block of non-attacking queens in one parent (e.g. first three columns) can be combined with a
> good block from another parent — the building-block idea
> ([[schema-theory-and-building-blocks]]).
