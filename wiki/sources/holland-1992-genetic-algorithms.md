---
type: source
summary: Holland's 1992 Scientific American article on genetic algorithms — crossover, schemata, implicit parallelism, building blocks, exploration vs exploitation and classifier systems.
unit: 9
tags: [genetic-algorithms, schema-theory, classifier-systems, paper]
sources: ["[[holland-1992-genetic-algorithms]]"]
updated: 2026-10-01
---

# Holland (1992) — "Genetic Algorithms"

**Bibliographic line.** J. H. Holland, "Genetic Algorithms," *Scientific American* 267(1),
pp. 66–73, July 1992. File: `raw/Papers/Holland-GeneticAlgorithms-1992.pdf` (JSTOR scan).

**What it is.** A popular-science article by the inventor of [[genetic-algorithms]]
([[john-holland]]). It explains why recombination matters, introduces schemata and
*implicit parallelism*, and describes classifier systems (evolving rule sets). It is the
paper the course slides cite as "John Holland – 1992" ([[slides-04-optimization]], slide 5).
Page numbers below are the magazine's (pdf page = magazine page − 64).

## Key points

- **History (p. 66).** Early 1950s–60s attempts relied on mutation rather than mating and
  "fared poorly". Bremermann (early 1960s) added a summing form of mating. Holland developed
  the GA by the **mid-1960s**, "well suited to evolution by both mating and mutation".
- **Classifier systems (pp. 66–67, 69).** Rules whose conditions/actions are bit strings
  (e.g. 1 = "hairy", "barks"…). Any FORTRAN/LISP program can be rewritten as a classifier
  system. Strings are rated by fitness; high-quality strings mate, low-quality ones perish.
- **Landscape view (p. 67).** The space of strings is a landscape: valleys = poor strings,
  highest point = best string. Hill climbing struggles because complex problems have many
  peaks. See [[hill-climbing]], [[optimization-problems]].
- **The GA loop (p. 68).** (1) evaluate every string; (2) higher-ranking strings mate by
  **single-point crossover** — a random point is chosen and the segments are exchanged,
  producing two offspring; offspring replace **low-fitness strings**, not their parents, so
  the population size stays constant; (3) **mutation** flips "roughly one in every 10,000
  symbols". Mutation "does not generally advance the search" but is "insurance against the
  development of a uniform population incapable of further evolution".
- **Schemata and implicit parallelism (p. 68).** Regions of the space are written with `*`
  for "don't care". The string `11011001` belongs to `11******`, `1*******`, `**0**00*`, etc.
  A population of a few thousand strings therefore samples a vastly larger number of regions;
  this **implicit parallelism** is the GA's "central advantage". The number of strings in a
  region grows at a rate proportional to the statistical estimate of that region's fitness.
  See [[schema-theory-and-building-blocks]].
- **Crossover disruption (p. 68).** For a six-gene string sampling `10****`, the offspring can
  leave the region only if the cut falls at the second position — one chance in five; in a
  1,000-gene string, one in 999. A region like `1****1` is broken wherever the cut falls.
  Closely adjacent defining bits are **compact building blocks**; they survive crossover and
  spread at a rate proportional to their average fitness.
- **Inversion (p. 69).** Rearranges genes so distant ones become adjacent, making building
  blocks more compact.
- **Nonlinearity (p. 69).** In nonlinear problems the fitness of two blocks together can be
  much more or less than the sum; single-bit blocks are then insufficient, but implicit
  parallelism still lets useful compact blocks be detected statistically.
- **Exploration vs exploitation (p. 69).** Exploiting a good strategy makes discovering novel
  ones unlikely; exploring costs performance. The GA's answer "turns on crossover": it tests
  building blocks in new combinations and, when it breaks a block, creates new ones that probe
  unsampled regions. See [[exploration-vs-exploitation]].
- **Prisoner's Dilemma (pp. 69–71).** Payoffs 3/3 (both cooperate), 5/0, 0/5, and a minimal
  payoff for mutual defection. Axelrod & Forrest encoded strategies as bit strings indexed by
  the last three plays; the GA quickly discovered **tit for tat** and later a variant that
  exploits players that can be "bluffed".
- **Rule competition and credit (p. 71).** Rules bid to act; winners are strengthened on
  success. Systems evolve **default hierarchies** (general rules on top, exceptions below)
  and learn to anticipate delayed payoff.
- **Applications and limits (p. 72).** Gas-pipeline control (Goldberg), communication networks
  (Davis), a jet-engine turbine design (100+ variables, more than $10^{387}$ points) where a GA
  seeded by an expert system tripled the improvement of a manual design in two days. Limit:
  GAs are best at locating promising regions; small refinements of a few variables are better
  done by "more standard methods" — the motivation for hybridising with local search.

## Pages that use this source

[[genetic-algorithms]], [[schema-theory-and-building-blocks]], [[evolutionary-computation]],
[[exploration-vs-exploitation]], [[hill-climbing]], [[genetic-algorithm-py]],
[[metaheuristics-comparison]], [[unit-09-optimization-review]].

## Issues found

> [!warning] Extraction lost superscripts and some digits
> Exponents were flattened: "1060 strategies for playing chess" is $10^{60}$; "more than
> 10387 points" is $10^{387}$; "more than 31,000 possibilities" for 1,000-digit strings is an
> exponent whose base was lost (the space has $2^{1000}$ strings — general knowledge). In the
> Prisoner's Dilemma passage the text reads "54 possibilities… a 54-bit string" and "264
> (approximately 15 quadrillion)"; three plays with four outcomes each give $4^3 = 64$, so
> "54" is almost certainly an OCR error for 64, and "264" is $2^{64}$. Note that
> $2^{64} \approx 1.8 \times 10^{19}$ (general knowledge), which does not match "15
> quadrillion"; check the printed article before quoting that number.

> [!note] Mutation rate
> Holland's "one in 10,000" is far lower than the $1/L$ rule of thumb in
> [[eiben-smith-evolutionary-computing]] §6.1 and the $1/16$ used in
> [[genetic-algorithm-py]]. Not a contradiction — different string lengths and purposes —
> but a good oral-exam question.
