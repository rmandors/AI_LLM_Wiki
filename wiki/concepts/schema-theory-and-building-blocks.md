---
type: concept
summary: Holland's schema theory explains GAs through schemata (bit patterns with * wildcards), implicit parallelism and the schema theorem, leading to the building block hypothesis; useful intuition with known limits.
unit: 9
tags: [genetic-algorithms, theory, schema-theorem]
sources: ["[[holland-1992-genetic-algorithms]]", "[[eiben-smith-evolutionary-computing]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Schema theory and building blocks

A **schema** (plural *schemata*) is a template over the chromosome alphabet with a "don't care"
symbol: `11****` stands for every 6-bit string starting with `11`. Each schema is a region
(hyperplane) of the search space, and every string belongs to many schemata at once. Holland's
insight is that a GA, while evaluating only $\mu$ strings, implicitly estimates the average
fitness of a huge number of schemata and allocates more offspring to above-average ones —
**implicit parallelism** ([[holland-1992-genetic-algorithms]], p. 68;
[[eiben-smith-evolutionary-computing]] §16.1). Short, low-order, above-average schemata are
**building blocks** that crossover recombines into better solutions.

## How it works

**Vocabulary** ([[eiben-smith-evolutionary-computing]] §16.1):
- **Order** $o(H)$: number of fixed (non-`*`) positions.
- **Defining length** $d(H)$: distance between the outermost fixed positions (= number of cut
  points that can split the schema). Example: $H =$ `1**0*1*0` has $o(H) = 4$, $d(H) = 8 - 1 =
  7$.
- A string of length $l$ is an instance of $2^l$ schemata. Holland estimated that a
  population of size $\mu$ usefully processes $O(\mu^3)$ schemata.
- Holland's example: `11011001` belongs to `11******`, `1*******`, `**0**00*`, …
  ([[holland-1992-genetic-algorithms]], p. 68).

**Schema theorem** for the simple GA (fitness-proportional selection, one-point crossover with
probability $p_c$, bitwise mutation $p_m$, generational replacement)
([[eiben-smith-evolutionary-computing]] Eq. 16.1):
$$m(H, t+1) \;\ge\; m(H,t)\cdot\frac{f(H)}{\langle f\rangle}\cdot\left[1 - p_c\,\frac{d(H)}{l-1}\right]\cdot\left[1 - p_m\, o(H)\right]$$
- $m(H,t)$: proportion of the population in $H$; $f(H)$: mean fitness of its instances;
  $\langle f\rangle$: mean population fitness.
- Selection multiplies by $f(H)/\langle f\rangle$.
- One-point crossover destroys $H$ with probability at most $d(H)/(l-1)$.
- Mutation destroys it with probability $1 - (1-p_m)^{o(H)} \approx p_m\, o(H)$.

**Building block hypothesis** ([[eiben-smith-evolutionary-computing]] §16.1): GAs first select
among short, low-order schemata, then combine them into higher-order ones, until the optimum is
assembled.

**Compactness** ([[holland-1992-genetic-algorithms]], p. 68): in a 6-gene string, the region
`10****` is left only if the cut falls between positions 1 and 2 — one chance in five; in a
1,000-gene string, one in 999. `1****1` is broken by every cut. **Inversion** can make blocks
more compact by moving distant genes together (p. 69).

## Properties

- **Short + low-order + above-average ⇒ grows** (all else equal) — the qualitative message.
- **R&N's version:** if the average fitness of a schema's instances is above the mean, the
  number of instances grows over time; GAs "work best when schemas correspond to meaningful
  components of a solution", so representation must be engineered ([[russell-norvig-aima]]
  §4.1.4).
- **Nonlinearity:** fitness of two blocks together can differ from the sum; then single-bit
  blocks are not enough but compact multi-bit blocks can still be detected
  ([[holland-1992-genetic-algorithms]], p. 69).
- **Deception:** problems can be built where low-order schemata point *away* from the optimum
  (e.g. a 4-bit problem with optimum `0000` but $f(1\#\#\#) > f(0\#\#\#)$, etc.)
  ([[eiben-smith-evolutionary-computing]] §16.1).

> [!warning] Criticisms (know these for a "discuss" question)
> [[eiben-smith-evolutionary-computing]] §16.2: (1) growth is not really exponential, because
> $f(H)/\langle f\rangle$ falls as $H$ spreads and the mean rises; (2) the theorem uses fitness
> *estimated from the current population* and predicts only the next generation; (3) Holland's
> claim that FPS allocates trials optimally was shown incorrect; (4) it ignores the constructive
> effects of operators (it is a special case of Price's theorem); (5) Holland, Mitchell & Forrest's
> **Royal Road** functions, built to show GA superiority, found local search doing better and
> revealed **hitchhiking** (bad alleles spreading because they sit next to a good schema).

## In this course

- The slides mention crossover as exchanging "bit sections at the same position" but not
  schemata ([[slides-04-optimization]], slide 6); the theory comes from the assigned Holland
  article ([[holland-1992-genetic-algorithms]], pp. 68–69).
- In Raymond's [[genetic-algorithm-py]] each 8-bit half encodes one variable, so the sign bit
  plus high-order magnitude bits of $x$ form a natural compact block (e.g. `1001****` ≈ "x is
  between −1.6 and −3.1"). A cut at position 8 swaps whole variables without breaking either.

## Common mistakes

- Confusing order with defining length: `1******1` has order 2 but defining length 7.
- Treating the schema theorem as proof that GAs find the optimum — it is an inequality about
  expected proportions one generation ahead.
- Forgetting that the theorem is for the SGA; Raymond's truncation + elitism GA does not fit
  its assumptions.

## Related

[[genetic-algorithms]], [[evolutionary-computation]], [[exploration-vs-exploitation]],
[[john-holland]], [[holland-1992-genetic-algorithms]], [[beam-search]].

## Practice questions

> [!question]- Q1. For $H =$ `*1*0**1*` ($l = 8$), give $o(H)$ and $d(H)$.
> **Answer.** Fixed positions 2, 4, 7 ⇒ $o(H) = 3$; $d(H) = 7 - 2 = 5$
> ([[eiben-smith-evolutionary-computing]] §16.1).

> [!question]- Q2. With $l = 6$, $p_c = 1$, $p_m = 0.01$, a schema `10****` has $f(H)/\langle f\rangle = 1.5$ and currently makes up 10% of the population. Lower-bound its share next generation.
> **Answer.** $o = 2$, $d = 1$. Crossover survival $1 - 1/5 = 0.8$ (Holland's "one chance in
> five"); mutation survival $\approx 1 - 0.02 = 0.98$. $m \ge 0.10 \times 1.5 \times 0.8 \times
> 0.98 \approx 0.118$ — about 11.8%, so it grows.

> [!question]- Q3. Same setting but $H =$ `1****1`. Does it grow?
> **Answer.** $d = 5$ ⇒ crossover survival $1 - 5/5 = 0$, so the bound is 0: one-point
> crossover always cuts it (Holland: it "runs the risk of leaving its parents' region no matter
> where crossover occurs"). It may still survive by luck (the other parent has matching bits),
> which the inequality ignores ([[holland-1992-genetic-algorithms]], p. 68).

> [!question]- Q4. What is implicit parallelism?
> **Answer.** Because each string belongs to $2^l$ schemata, evaluating $\mu$ strings gives
> statistical information about far more regions than $\mu$; Holland estimated $O(\mu^3)$ are
> usefully processed. The GA thus samples many regions in parallel while manipulating few strings
> ([[holland-1992-genetic-algorithms]], p. 68; [[eiben-smith-evolutionary-computing]] §16.1).

> [!question]- Q5. Give two criticisms of the schema theorem.
> **Answer.** Any two of: growth isn't exponential (selective advantage shrinks as the schema
> spreads); it predicts only the next generation from current estimates; it ignores
> constructive effects of crossover/mutation; Royal Road experiments contradicted its
> predictions; FPS doesn't allocate trials optimally ([[eiben-smith-evolutionary-computing]]
> §16.2).
