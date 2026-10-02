---
type: source
summary: Eiben & Smith, Introduction to Evolutionary Computing (2nd ed., 2015) — secondary textbook for EA components, operators, selection, the simple GA, PSO with inertia and schema theory.
unit: 9
tags: [evolutionary-computation, genetic-algorithms, textbook]
sources: ["[[eiben-smith-evolutionary-computing]]"]
updated: 2026-10-01
---

# Eiben & Smith — *Introduction to Evolutionary Computing*

**Bibliographic line.** A. E. Eiben and J. E. Smith, *Introduction to Evolutionary
Computing*, 2nd ed., Natural Computing Series, Springer, 2015. File:
`raw/Books/A.E. Eiben_ J.E. Smith - Introduction to Evolutionary Computing-Springer (2015).pdf`.

**What it is.** The course's secondary textbook for evolutionary computing (see
[[overview]]). It gives the general EA scheme, then catalogues representations, variation
operators and selection schemes, and finally surveys the classic EA "dialects" (GA, ES, EP,
GP, DE, PSO, EDA). Book page = pdf page − 14.

## Sections read (ingested on demand, 2026-10-01)

| Section | Book pages | Used for |
|---|---|---|
| §2.2 Brief history | ~13–14 | [[evolutionary-computation]] |
| §3.1–3.2 What is an EA; components | 25–34 | [[evolutionary-computation]] |
| §3.3 Evolutionary cycle by hand ($x^2$ example) | 34–36 | [[genetic-algorithms]] |
| §3.4.1 Eight-queens EA | 36–39 | [[genetic-algorithms]] |
| §3.5 (part) exploration/exploitation, premature convergence, anytime behaviour | 41–42 | [[exploration-vs-exploitation]] |
| §4.2 Binary representation, bit-flip mutation, 1-point / n-point / uniform crossover | 51–54 | [[genetic-algorithms]], [[genetic-algorithm-py]] |
| §5.1 Population management models | 79–80 | [[evolutionary-computation]] |
| §5.2.1–5.2.4 Fitness-proportional, ranking, roulette wheel/SUS, tournament | 80–86 | [[genetic-algorithms]] |
| §5.3.2 Fitness-based replacement, elitism, $(\mu+\lambda)$, $(\mu,\lambda)$ | 88–90 | [[genetic-algorithms]] |
| §5.4 Selection pressure, takeover time | 90 | [[genetic-algorithms]] |
| §6.1 Genetic algorithms, Table 6.1 (simple GA) | 99–100 | [[genetic-algorithms]] |
| §6.2, §6.3 (first lines only) ES and EP origins | 101, 103 | [[evolutionary-computation]] |
| §6.7 Particle swarm optimisation | 112–113 | [[particle-swarm-optimization]] |
| §6.8 (one line) truncation selection | 115 | [[genetic-algorithm-py]] |
| §16.1–16.2 Schema theorem and criticisms | 232–237 | [[schema-theory-and-building-blocks]] |

Not yet read: Ch. 1, Ch. 7 onward (parameter control, multimodality details, constraint
handling, memetic algorithms, etc.).

## Key points

- **General EA scheme (§3.1, Fig. 3.1).** Initialise → evaluate → repeat {select parents;
  recombine; mutate; evaluate; select survivors} until termination. EAs are
  population-based, mostly use recombination, and are stochastic. Two forces: *variation*
  creates diversity/novelty; *selection* pushes quality up.
- **Dialects (§3.1, §2.2).** GAs use strings over a finite alphabet; ES real-valued vectors;
  EP finite-state machines; GP trees. In the 1960s Fogel, Owens & Walsh (EP, USA), Holland
  (GA) and Rechenberg & Schwefel (ES, Germany) developed the idea separately; they were
  unified as "evolutionary computing" in the early 1990s. Turing (1948) and Bremermann
  (1962) came earlier.
- **Components (§3.2).** Representation (phenotype ↔ genotype; encoding/decoding), fitness
  function, population (multiset; diversity), parent selection (typically probabilistic),
  mutation (unary, random, unbiased) and recombination (binary), survivor selection (often
  deterministic), initialisation, termination. Minimisation problems are trivially recast as
  maximisation of fitness (§3.2.2).
- **$x^2$ worked example (§3.3, Tables 3.1–3.3).** 5-bit strings, fitness-proportional
  selection $p_i = f(i)/\sum_j f(j)$, one-point crossover, bitwise mutation, generational
  replacement; average fitness rises from 293 to 588.5 and best from 576 to 729 in one cycle.
- **Eight-queens (§3.4.1, Table 3.4).** Permutation representation (removes row/column
  clashes), swap mutation, "cut-and-crossfill" crossover, parents = best 2 of random 5,
  replace worst, population 100, stop at a solution or 10,000 evaluations. Compare
  [[hw01-ex03-n-queens]].
- **Exploration/exploitation (§3.5).** Exploration = new individuals in untested regions;
  exploitation = concentrating near known good solutions; **premature convergence** = losing
  diversity too quickly and getting trapped in a local optimum.
- **Binary operators (§4.2).** Using bit strings for non-binary data "is usually a mistake";
  standard binary has **Hamming cliffs** (7 = 0111 → 8 = 1000 needs four flips), fixed by
  **Gray coding**. Bitwise mutation flips each bit with $p_m$ (expected $L \cdot p_m$ flips);
  typical rates give between one flip per generation and one per offspring. One-point
  crossover picks $r \in [1, l-1]$; n-point generalises it; uniform crossover chooses each
  gene's parent independently. n-point has **positional bias**; uniform has **distributional
  bias**.
- **Selection (§5.2).** FPS $P(i) = f_i / \sum_j f_j$ suffers premature convergence early,
  vanishing pressure late, and sensitivity to shifting $f$ (Table 5.1); remedies: windowing,
  sigma scaling $f' = \max(f - (\bar f - c\sigma), 0)$, ranking. Roulette wheel (Fig. 5.1) vs
  stochastic universal sampling (Fig. 5.2). **Tournament selection** (Fig. 5.3) needs only
  comparisons; larger $k$ = more selection pressure.
- **Survivor selection (§5.3.2).** Replace-worst (GENITOR) improves fast but risks premature
  convergence; **elitism** keeps the current best; $(\mu+\lambda)$ merges parents and
  offspring; $(\mu,\lambda)$ discards parents (can leave local optima).
- **Selection pressure (§5.4).** Takeover time $\tau^*$; for FPS, $\tau^* = \lambda \ln \lambda
  \approx 460$ for $\lambda = 100$.
- **Simple GA (§6.1, Table 6.1).** Bit strings, 1-point crossover, bit-flip mutation,
  fitness-proportional selection by roulette wheel, generational replacement — and
  **no elitism**. Classic advice: $p_m$ between $1/l$ and $1/\mu$, $p_c \approx 0.6$–$0.8$,
  population in the fifties to low hundreds. Modern practice adds elitism, SUS, rank/
  tournament selection, uniform crossover, self-adaptive mutation.
- **PSO (§6.7).** Launched 1995 by Kennedy & Eberhart; no crossover; "mutation" is vector
  addition. Each individual is a triple $\langle x_i, v_i, b_i \rangle$:
  $$v_i' = w \cdot v_i + \varphi_1 U_1 \cdot (b_i - x_i) + \varphi_2 U_2 \cdot (c - x_i), \qquad x_i' = x_i + v_i'$$
  with inertia $w$, learning rates $\varphi_1$ (personal) and $\varphi_2$ (social), and
  random diagonal matrices $U_1, U_2$ that scale *every coordinate separately*; $c$ is the
  global best. Personal best is replaced only if $f(x_i') < f(b_i)$.
- **Schema theorem (§16.1, Eq. 16.1).** Order $o(H)$, defining length $d(H)$;
  $$m(H,t+1) \ge m(H,t)\,\frac{f(H)}{\langle f \rangle}\left[1 - p_c\frac{d(H)}{l-1}\right]\left[1 - p_m\, o(H)\right]$$
  A string of length $l$ belongs to $2^l$ schemata; a population "usefully processes"
  $O(\mu^3)$ of them (implicit parallelism). Leads to the **building block hypothesis**.
- **Criticisms (§16.2).** Growth is not really exponential; the theorem predicts only the next
  generation; Holland's optimal-allocation argument was shown incorrect; it ignores
  constructive effects (it is a special case of Price's theorem); Royal Road experiments by
  Holland, Mitchell & Forrest found the GA *losing* to local search, revealing hitchhiking.

## Pages that use this source

[[evolutionary-computation]], [[genetic-algorithms]], [[schema-theory-and-building-blocks]],
[[particle-swarm-optimization]], [[exploration-vs-exploitation]], [[optimization-problems]],
[[genetic-algorithm-py]], [[particle-swarm-py]], [[metaheuristics-comparison]],
[[unit-09-optimization-review]].

## Issues found

- The extraction drops spaces in many headings and some sentences ("FitnessProportionalSelection",
  "h o l l a n d ’ s") and loses figures (e.g. Fig. 3.2 flowchart, Fig. 4.2 crossover diagram).
  Formulas mostly survive but subscripts are flattened.
- §6.7 notation clashes with [[slides-04-optimization]] slide 9: in the book $\varphi_i$ are
  constants and $U_i$ are random; on the slide $\varphi_i$ are the random numbers.
