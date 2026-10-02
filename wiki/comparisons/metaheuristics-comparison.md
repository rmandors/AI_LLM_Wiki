---
type: comparison
summary: Side-by-side comparison of hill climbing, gradient descent, simulated annealing, GA, PSO, ACO and ABC — inspiration, representation, parameters, exploration/exploitation mechanisms, memory and typical problems.
unit: 9
tags: [optimization, metaheuristics, comparison]
sources: ["[[slides-04-optimization]]", "[[russell-norvig-aima]]", "[[eiben-smith-evolutionary-computing]]", "[[holland-1992-genetic-algorithms]]", "[[kennedy-eberhart-1995-pso]]", "[[dorigo-1996-ant-system]]"]
updated: 2026-10-01
---

# Metaheuristics comparison

The seven optimisers of unit 9 fall into two groups. **Single-solution** methods
([[hill-climbing]], [[gradient-descent]], [[simulated-annealing]]) move one current state.
**Population** methods ([[genetic-algorithms]], [[particle-swarm-optimization]],
[[ant-colony-optimization]], [[artificial-bee-colony]]) keep many candidates that share
information. The tables below summarise them; each row is detailed on the concept page.

## Overview

| | Hill climbing | Gradient descent | Simulated annealing | Genetic algorithm | PSO | ACO (Ant System) | ABC |
|---|---|---|---|---|---|---|---|
| **Inspiration** | mountaineering (greedy ascent) | calculus (steepest slope) | metallurgical annealing / Metropolis | natural selection & genetics (Holland) | bird flocking, fish schooling (Kennedy & Eberhart 1995) | ant foraging & pheromone trails (Dorigo 1996) | honeybee foraging (Karaboga 2007) |
| **Representation** | any state + neighbourhood | real vector, differentiable $f$ | any state + random neighbour | chromosome (bit string, permutation, …) | real vector + velocity | path built on a graph; pheromone matrix | real vector ("food source") |
| **Space** | discrete or continuous | continuous | discrete or continuous | mostly discrete (encoded) | continuous | discrete / combinatorial | continuous |
| **Population?** | no (1 state) | no (1 point) | no (1 state) | yes ($\mu$ individuals) | yes (swarm) | yes ($m$ ants) | yes ($SN$ sources) |
| **Key parameters** | neighbourhood, sideways-move cap, restarts | step size $\eta$, iterations/tolerance | $T_0$, cooling schedule, step size | pop. size, selection, $p_c$, $p_m$, elitism | swarm size, $w$, $c_1$, $c_2$, $v_{max}$ | $m$, $\alpha$, $\beta$, $\rho$, $Q$, $\tau_0$ | $SN$, limit, MCN |
| **Exploration mechanism** | random restarts / sideways moves | none (restarts) | accepting worse moves w.p. $e^{-\Delta/T}$ | mutation; crossover of diverse parents | momentum/overshoot; random factors | probabilistic choice; evaporation | scout bees (random reinit after *limit*) |
| **Exploitation mechanism** | always take best neighbour | follow $-\nabla f$ | low $T$ ⇒ only improvements | selection pressure; elitism | pull to $p_{best}$, $g_{best}$ | pheromone reinforcement ($\alpha$); greedy visibility ($\beta$) | employed + onlooker local search; fitness-proportional recruitment |
| **Memory** | current state | current point | current + best-so-far | the population (+ elites) | each particle's $p_{best}$ + swarm $g_{best}$ | pheromone matrix (colony memory) | sources + trial counters + best |
| **Uses gradient?** | no | yes | no | no | no | no | no |
| **Guarantee** | local optimum | stationary point | global w.p. → 1 with slow enough cooling | none | none | none | none |
| **Typical problems** | n-queens, SAT, scheduling | ML training, smooth objectives | VLSI layout, scheduling, TSP | design, scheduling, combinatorial search | NN weights, continuous benchmarks | TSP, QAP, job-shop, routing | continuous benchmark functions |
| **Course code** | — | [[gradient-descent-py]] | [[simulated-annealing-py]] | [[genetic-algorithm-py]] | [[particle-swarm-py]] | [[ant-colony-py]] | — |

Sources for the rows: [[russell-norvig-aima]] §4.1–4.2; [[eiben-smith-evolutionary-computing]]
§3, §6.1, §6.7; [[holland-1992-genetic-algorithms]]; [[kennedy-eberhart-1995-pso]];
[[dorigo-1996-ant-system]]; [[slides-04-optimization]], slides 2–18. ABC formulas and "typical
problems" cells are general knowledge where the slides are silent.

## Update rules at a glance

| Algorithm | Core update |
|---|---|
| Hill climbing | $x \leftarrow \arg\max_{x' \in N(x)} f(x')$ if better, else stop |
| Gradient descent | $w \leftarrow w - \eta \nabla f(w)$ |
| Simulated annealing | accept $x'$ if $\Delta < 0$, else with prob. $e^{-\Delta/T}$; $T \leftarrow aT$ |
| GA | select → crossover → mutate (flip each bit w.p. $p_m$) → replace |
| PSO | $v \leftarrow w v + c_1 r_1 (p - x) + c_2 r_2 (g - x)$; $x \leftarrow x + v$ |
| ACO | $p_{ij} \propto \tau_{ij}^\alpha \eta_{ij}^\beta$; $\tau \leftarrow \rho\tau + \sum_k Q/L_k$ |
| ABC | $v_{ij} = x_{ij} + \phi_{ij}(x_{ij} - x_{kj})$, $\phi \in [-1,1]$; $p_i = \text{fit}_i/\sum \text{fit}$; scout if trials > limit |

## Observed behaviour in the course code (re-runs, 2026-10-01)

| Program | Problem | Outcome |
|---|---|---|
| [[gradient-descent-py]] | convex 2-D quadratic | exact to $10^{-6}$ in 65 iterations; float floor at 161 |
| [[simulated-annealing-py]] | 2-D Rastrigin | global basin in 5/5 runs, but cooling makes it hill climbing after ~50 iterations |
| [[genetic-algorithm-py]] | 2-D quadratic, 0.1 grid | exact optimum in 10/10 runs; median 5 generations, one run 78 (diversity collapse) |
| [[particle-swarm-py]] | 2-D quadratic, continuous | $f - 10 \approx 0.001$–$0.003$ by ~20 iterations, then swarm diverges |
| [[ant-colony-py]] | 25-city random TSP | 8–19% shorter than nearest-neighbour tour |

## When to use which

- **Smooth, differentiable, (nearly) convex objective** → [[gradient-descent]] (or Newton's
  method). Fast and precise; nothing else in the table competes.
- **Discrete states with a natural neighbourhood, few deep traps** → [[hill-climbing]] with random
  restarts (R&N: very effective even for millions of queens, [[russell-norvig-aima]] §4.1.1).
- **Rugged landscape, cheap evaluations, one solution at a time** → [[simulated-annealing]] with
  a slow schedule.
- **Combinatorial problem with good partial "building blocks" and a meaningful encoding** →
  [[genetic-algorithms]]; hybridise with local search for final tuning
  ([[holland-1992-genetic-algorithms]], p. 72).
- **Continuous black-box function, moderate dimension** → [[particle-swarm-optimization]] (with
  inertia/constriction) or [[artificial-bee-colony]].
- **Problem that is naturally a path or sequence on a graph (TSP, routing, scheduling)** →
  [[ant-colony-optimization]], whose constructive ants and pheromone matrix fit the structure
  ([[dorigo-1996-ant-system]] §VII).
- **No Free Lunch**: no method wins on every problem ([[eiben-smith-evolutionary-computing]]
  §4.2.2); choose by structure, then tune.

## Practice questions

> [!question]- Q1. Which of the seven methods need a gradient, and which work naturally on permutations?
> **Answer.** Only gradient descent needs $\nabla f$. ACO (tours on a graph) and GAs with permutation
> encodings work naturally on permutations; hill climbing and SA do too if you define a neighbour
> (e.g. swap two cities).

> [!question]- Q2. Name the exploration mechanism of SA, GA, PSO, ACO and ABC.
> **Answer.** SA: accepting worse moves with $e^{-\Delta/T}$. GA: mutation (and crossover of
> diverse parents). PSO: momentum/overshoot plus random factors. ACO: probabilistic edge choice
> and evaporation. ABC: scout bees.

> [!question]- Q3. Which algorithm stores its "memory" in the environment rather than in individuals?
> **Answer.** ACO: the pheromone matrix is shared memory written and read by all ants (stigmergy —
> general knowledge); individual ants keep only a tabu list ([[dorigo-1996-ant-system]] §II).

> [!question]- Q4. You must tune 30 real-valued parameters of a simulator that takes 1 s per run and has no gradient. Which method do you pick and why not gradient descent?
> **Answer.** PSO (with inertia) or ABC, or an evolution strategy: continuous, derivative-free,
> population-based. Gradient descent needs $\nabla f$; finite differences would cost 31 runs per
> step and still get stuck in local minima.

> [!question]- Q5. Which methods have a theoretical global-optimum guarantee, and how practical is it?
> **Answer.** SA: probability → 1 if $T$ is lowered slowly enough ([[russell-norvig-aima]]
> §4.1.2); random-restart hill climbing: complete with probability 1. Both guarantees need
> impractically long runs. GA/PSO/ACO/ABC have no practical guarantee.

> [!question]- Q6. Why is a GA described as "stochastic beam search plus crossover"?
> **Answer.** Both keep $k$ states and select successors with probability related to fitness; the GA
> additionally creates successors from two parents, which helps when partial solutions combine
> usefully ([[russell-norvig-aima]] §4.1.4; [[beam-search]]).
