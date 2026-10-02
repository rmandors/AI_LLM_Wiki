---
type: code
summary: Walkthrough of Raymond's Genetic_algorithm.py — a 16-bit sign-magnitude GA with top-10 elitism and truncation selection that minimises (x+2)²+(y−2)²+10; usually exact in under 10 generations, but can stall on a Hamming cliff.
unit: 9
tags: [genetic-algorithms, code, class-exercise, raymond-work]
sources: ["[[ga-exercise-explanation]]", "[[slides-04-optimization]]", "[[eiben-smith-evolutionary-computing]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# `Genetic_algorithm.py` — Raymond's GA class exercise

**File:** `raw/Class_exercises/Genetic Algorithm Exercise/Genetic_algorithm.py` (109 lines,
NumPy + Matplotlib). Write-up: [[ga-exercise-explanation]].

**Problem.** Minimise $f(x, y) = (x+2)^2 + (y-2)^2 + 10$ (global minimum $f = 10$ at
$(-2, 2)$) with a bit-string [[genetic-algorithms|genetic algorithm]], as asked in the GA class
activity ([[slides-04-optimization]], slides 5–6).

## Design decisions

| Choice | Value in code | Comment |
|---|---|---|
| Representation | 16 bits = (sign + 7-bit magnitude) for $x$, same for $y$; value = ±magnitude/10 | range $[-12.7, 12.7]$, step 0.1 |
| Population | 100 | |
| Generations | 100 (`num_epochs`) | |
| "Fitness" | $f$ itself, **lower is better** | name clashes with the usual "higher is better" convention ([[eiben-smith-evolutionary-computing]] §3.2.2) |
| Survivor selection | **elitism**: top `k_elites = 10` copied unchanged | |
| Parent selection | two parents drawn uniformly **from the 10 elites only** | i.e. **truncation selection** of the top 10% — very strong pressure |
| Crossover | single-point, cut in $[1, 15]$, two children | matches [[eiben-smith-evolutionary-computing]] §4.2.2 |
| Mutation | uniform bit-flip, $p_m = 1/L = 1/16$ per bit | the common $1/L$ rule |
| Replacement | 10 elites + 90 mutated children (generational for non-elites) | |

Compared with the simple GA of [[eiben-smith-evolutionary-computing]] Table 6.1 (roulette-wheel
selection, generational, *no* elitism), this is a much greedier design.

## Walkthrough

- **L4–6 `objective(x, y)`** — the paraboloid.
- **L8–12 constants** — `BITS_PER_VAR = 8`, `CHROMOSOME_LENGTH = 16`, `SCALE = 10.0`.
- **L15–16 `random_individual`** — 16 random `"0"`/`"1"` characters (chromosomes are Python
  strings).
- **L19–22 `decode_variable(bits)`** — first bit `1` → negative; `int(bits[1:], 2) / 10` is the
  magnitude. E.g. `10010100` → −(20/10) = −2.0.
- **L25–28 `decode_individual`** — first 8 bits → $x$, last 8 → $y$.
- **L31–33 `fitness`** — decode then evaluate $f$.
- **L36–41 `crossover`** — `point = randint(1, 16)` gives a cut in 1..15; children swap tails.
- **L44–52 `mutate`** — each bit flips with probability `mutation_rate` (default $1/16$).
- **L56–59 parameters**; **L61–69** random initial population, best tracked.
- **L71–98 main loop.** L73 sorts by $f$; L76–77 keep the 10 best as elites; L80–85 repeatedly
  pick indices `i, j` in 0..9 (with replacement, so `i == j` is possible), cross over, mutate both
  children, append until 100; L89–96 track best-so-far; L98 prints the epoch's best.
- **L100–110** report and plot best $f$ per epoch.

## Results

Write-up run ([[ga-exercise-explanation]]): start ≈ $(-1.5, 2.0)$, $f = 10.25$; then $(-2.3,
2.1)$, $(-1.9, 2.0)$, $(-2.0, 2.0)$; exact minimum $f = 10$ by **epoch 7**.

Re-runs (2026-10-01, NumPy seeds 0–9, unmodified code): every run ends at exactly $(-2.0, 2.0)$,
$f = 10$. First epoch reaching $f = 10$: **78, 3, 4, 2, 6, 5, 4, 5, 8, 5** — median 5, consistent
with the write-up's 7. Seed 0 is the outlier:

> [!warning] Diversity collapse + Hamming cliff (seed 0)
> By epoch 3 the best was $(-1.9, 2.0)$, $f = 10.01$, chromosome `10010011 00010100`. By epoch 5
> **all 10 elites were identical** (and only ~40–50 of 100 individuals distinct). Crossover between
> identical parents produces copies, so only mutation can move. Going from $-1.9$ to $-2.0$ means
> magnitude 19 → 20, i.e. `0010011` → `0010100`: **three bits must flip at once** — a Hamming cliff
> ([[eiben-smith-evolutionary-computing]] §4.2). Probability per child $\approx (1/16)^3
> (15/16)^{13} \approx 1.1 \times 10^{-4}$, so ≈1% per generation with 90 children; it took until
> epoch 78. Gray coding, a less greedy selection, or a slightly higher mutation rate would fix it.

Search-space note: there are only $2^{16} = 65{,}536$ genotypes (65,025 distinct points, since
`10000000` and `00000000` both decode to 0), and a run evaluates about 9,000 new children, so on
this problem the GA is competing with brute force.

## Known issues / improvements

1. **Truncation to 10 parents + elitism** gives very high selection pressure; diversity collapses
   within ~5 generations (above). Use tournament ($k = 2$–3) or rank selection over the whole
   population ([[eiben-smith-evolutionary-computing]] §5.2).
2. **Binary Hamming cliffs** — switch to Gray code or a real-valued representation
   ([[eiben-smith-evolutionary-computing]] §4.2: bit strings for real numbers are "usually a
   mistake").
3. **`i == j` self-mating** produces clones; draw `j ≠ i`.
4. **Redundant zero** (`+0.0` and `−0.0`) — harmless but wastes code space; two's complement or
   offset binary avoids it.
5. **"Fitness" is minimised** — fine, but would break if swapped for roulette selection, which
   needs a positive, maximised fitness ([[eiben-smith-evolutionary-computing]] §5.1).
6. **Repeated evaluation**: `sorted(..., key=fitness)` and `min(..., key=fitness)` each re-decode
   all 100 individuals; caching fitness halves the work (minor here).
7. **No stopping rule** — all 100 epochs run even after $f = 10$; the optimum is known, so a
   target-fitness or no-improvement criterion would do ([[eiben-smith-evolutionary-computing]]
   §3.2.8).
8. The write-up's statement "true minimum is at $(-2, 0)$" is a typo for $(-2, 2)$.

## Related concepts

[[genetic-algorithms]], [[evolutionary-computation]], [[schema-theory-and-building-blocks]],
[[exploration-vs-exploitation]], [[optimization-problems]], [[particle-swarm-py]] (same
objective), [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Why 8 bits per variable, and what is the resolution and range?
> **Answer.** 1 sign bit + 7 magnitude bits → magnitudes 0..127, divided by 10 → $[-12.7, 12.7]$
> in steps of 0.1. That range contains the optimum $(-2, 2)$ exactly on the grid, so the GA can
> hit $f = 10$ exactly.

> [!question]- Q2. What selection method does your code use? Is it fitness-proportional?
> **Answer.** No. Parents are drawn uniformly from the top 10 of 100 — truncation selection —
> plus elitism (the same 10 survive unchanged). It ignores fitness differences inside the top 10
> and gives zero chance to the other 90, so selection pressure is very high.

> [!question]- Q3. Decode `00001111 10000011`.
> **Answer.** $x$: sign 0, `0001111` = 15 → $+1.5$. $y$: sign 1, `0000011` = 3 → $-0.3$.
> $f = 3.5^2 + 2.3^2 + 10 = 12.25 + 5.29 + 10 = 27.54$.

> [!question]- Q4. One of my re-runs got stuck at $(-1.9, 2.0)$ for 75 generations. Why?
> **Answer.** All elites became identical, so crossover could not create anything new; reaching
> $-2.0$ from $-1.9$ needs the three low bits `011` → `100` to flip together (a Hamming cliff),
> which has probability ≈ $10^{-4}$ per child with $p_m = 1/16$.

> [!question]- Q5. What does elitism buy you here, and what would happen without it?
> **Answer.** The best-so-far can never be lost, so the fitness curve is monotone (flat at 10
> after convergence). Without elitism (and with the same truncation selection) the best could be
> destroyed by crossover/mutation and the curve would fluctuate, but diversity would be slightly
> higher ([[russell-norvig-aima]] §4.1.4).

> [!question]- Q6. Your write-up says mutation adds "small" random exploration. Is that always true?
> **Answer.** No: a flip of the sign bit changes the sign, and a flip of the top magnitude bit
> changes the value by 6.4. Expected flips per child is 1, so many children take large jumps; the
> step size in phenotype space depends on *which* bit flips.
