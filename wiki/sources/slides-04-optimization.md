---
type: source
summary: Lecture deck 04 "Optimization and Biology-Inspired Agents" — evolutionary computation history, GA, PSO, ACO and ABC; several key slides are image-only.
unit: 9
tags: [optimization, evolutionary-computation, swarm-intelligence, slides]
sources: ["[[slides-04-optimization]]"]
updated: 2026-10-01
---

# Slides 04 — Optimization and Biology-Inspired Agents

**Bibliographic line.** D. Riofrío, *Optimization and Biology-Inspired Agents*, lecture slides
(`raw/Slides/04_Optimization.pptx`), Artificial Intelligence NRC 1651, USFQ, Fall 2026. 19 slides.

**What it is.** The course deck for syllabus unit 9 (optimization and bio-inspired algorithms).
It introduces [[evolutionary-computation]], the idea of global vs local optima, and four
algorithms: [[genetic-algorithms]], [[particle-swarm-optimization]],
[[ant-colony-optimization]] and [[artificial-bee-colony]]. The deck is short on formulas:
the update equations that appear on the slides are pictures, so they did not survive text
extraction (see *Issues found*).

## Key points

- **Slide 2 — history of evolutionary computation.** Evolutionary computation came from the
  need to solve combinatorial optimization problems with the mechanisms of biological
  evolution. Lawrence J. Fogel (1960) is called its creator (evolving finite-state machines);
  Rechenberg and Hans-Paul Schwefel (1970) proposed evolution strategies for parameter
  optimization; [[john-holland]] (1975) proposed genetic algorithms as a general adaptive model.
- **Slide 3 — optima and the evolution metaphor.** Labels a landscape with *global maximum*,
  *local maximum*, *global minimum*. Defines adaptation, heredity and natural selection.
  "Optimization seeks global maximum or minimum solution points and avoids confusing them
  with local points." Treat each point of the solution space as an individual, evaluate its
  fitness, and let only individuals converging on global optima survive. See
  [[optimization-problems]].
- **Slide 4 — "Bio-Inspired Algorithms"** (title + image, credited "SALFORD & CO.").
- **Slide 5 — Genetic algorithms (labelled "John Holland – 1992").** Principles: variation,
  selection, heredity. Individuals are bit strings; evaluation by a fitness function that
  seeks a higher or lower value; reproduction by crossover; variation by flipping a bit with
  some probability.
- **Slide 6 — operators.** Chromosome = "a sequence of 1s and 0s representing a decimal
  number encoded in binary"; crossover = "parents exchange bit sections at the same
  position", generalisable to single-point, two-point or k-point; mutation = a bit flip "for
  each bit in the chromosome depending on a given probability". Diagram labels "Single
  point", "h1", "h2" (children).
- **Slide 8 — PSO, James Kennedy and Russell Eberhart, 1995.** Stochastic optimization
  algorithm inspired by social behaviour of birds and fish and by swarm theory; a swarm of
  particles moves continuously through the search space sharing information about the best
  positions found.
- **Slide 9 — PSO state.** Each particle has current position $x_t$, velocity $v_t$, and
  personal best $p_{best}$; the swarm keeps the global best $g_{best}$. "The parameters
  $\varphi_1$ and $\varphi_2$ are random variables uniformly distributed over $[0,1]$."
- **Slide 10 — "Exploration / Exploitation"** (labels on a figure). See
  [[exploration-vs-exploitation]].
- **Slide 12 — ACO, Marco Dorigo, 1996.** Metaheuristic originally proposed for
  combinatorial problems, based on how ant swarms optimise their paths to food or around
  obstacles.
- **Slide 13 — pheromones.** Ants wander randomly; on finding food they return to the colony
  leaving pheromone; other ants tend to follow and reinforce the trail. Goal: raise pheromone
  on good solutions and lower it on poor ones; evaporation on weak paths makes this possible.
- **Slide 16 — ABC, Karaboga, 2007.** Swarm-intelligence approach imitating honeybee foraging.
- **Slide 17 — bee roles.** Employed, onlooker and scout bees. Onlookers and employed bees
  exploit; scouts explore. Success depends on quickly discovering and efficiently using the
  best resources.
- **Slide 18 — ABC parameters.** Three control parameters: number of food sources, "which
  equals the number of employed bees (BN) or onlooker bees (SN)"; the *limit*; and the maximum
  number of cycles (MCN). Defines *recruitment rate* (how fast the colony finds and exploits a
  new source). "To produce a possible food position: $k \in \{1,\dots,BN\}$ and
  $j \in \{1,\dots,D\}$ are arbitrarily selected indices" — the formula itself is missing.

## Pages that use this source

[[optimization-problems]], [[exploration-vs-exploitation]], [[evolutionary-computation]],
[[genetic-algorithms]], [[particle-swarm-optimization]], [[ant-colony-optimization]],
[[artificial-bee-colony]], [[swarm-intelligence]], [[genetic-algorithm-py]],
[[particle-swarm-py]], [[ant-colony-py]], [[metaheuristics-comparison]],
[[unit-09-optimization-review]].

## Issues found

> [!warning] Image-only slides
> Slides **7, 11, 14, 15 and 19** have no extractable text at all (pictures only). In
> addition, the **formulas on slide 9** (the PSO velocity and position update) and on
> **slide 18** (the ABC candidate food position) are images; only the surrounding text
> survived. The wiki fills these gaps from the papers and textbooks, never by guessing what
> the pictures showed:
> - PSO update: [[kennedy-eberhart-1995-pso]] §3.6 (original, no inertia) and
> [[eiben-smith-evolutionary-computing]] §6.7 (with inertia $w$).
> - ACO transition rule and pheromone update: [[dorigo-1996-ant-system]] Eqs. (1)–(4).
> - ABC: no ABC paper is in `raw/`; the formulas on [[artificial-bee-colony]] are marked
> *(general knowledge)* and should be checked against Karaboga & Basturk (2007), which
> [[russell-norvig-aima]] cites in its Ch. 4 bibliographic notes.
> - Slides 14–15 sit between the ACO intro and ABC, so they probably held the ACO equations,
> and slide 7 (after the GA operators) probably held a GA flowchart or example — but that
> is inference from position only, not content.

> [!warning] Contradiction — dates
> Slide 2 dates GAs to Holland **1975**, but slide 5 labels them "John Holland – **1992**".
> 1992 is the year of the *Scientific American* article ([[holland-1992-genetic-algorithms]]),
> not of the invention; Holland himself says he developed the technique by the mid-1960s
> (p. 66), and [[russell-norvig-aima]] (Ch. 4 notes, p. 161) cites Holland (1975).
> Likewise slide 2 gives Rechenberg & Schwefel **1970**, while
> [[eiben-smith-evolutionary-computing]] §6.2 says evolution strategies were invented in the
> **early 1960s** and R&N cites Rechenberg (1965). Calling Fogel *the* creator is also
> debatable: Eiben & Smith §2.2 cite Turing's 1948 "genetical or evolutionary search" and
> Bremermann's 1962 experiments as earlier.

> [!warning] Notation — what $\varphi$ means in PSO
> Slide 9 calls $\varphi_1, \varphi_2$ *random variables* $\sim U[0,1]$. In
> [[eiben-smith-evolutionary-computing]] §6.7, $\varphi_1, \varphi_2$ are constant *learning
> rates* and the randomness is in separate factors $U_1, U_2$. In Raymond's
> [[particle-swarm-py]] the constants are `ALPHA1 = ALPHA2 = 2` and the random draws are
> `phi1`, `phi2` — the slide's convention. Know both.

> [!note] ABC parameter names
> Slide 18 reads as if BN and SN were two different counts. In Karaboga's formulation the
> number of food sources $SN$ equals the number of employed bees and also the number of
> onlookers (general knowledge). Treat BN = SN.
