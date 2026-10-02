---
type: concept
summary: Ant colony optimization builds solutions with artificial ants that choose edges with probability ∝ τ^α·η^β and reinforce good tours with pheromone that evaporates over time (Dorigo's Ant System, 1996).
unit: 9
tags: [ant-colony-optimization, swarm-intelligence, combinatorial, tsp, metaheuristics]
sources: ["[[slides-04-optimization]]", "[[dorigo-1996-ant-system]]"]
updated: 2026-10-01
---

# Ant colony optimization (ACO)

**Ant colony optimization** solves combinatorial problems — originally the Travelling Salesman
Problem — by simulating ants that build solutions step by step on a graph. Each ant picks its
next node at random, favouring edges with more **pheromone** $\tau$ and better **heuristic
desirability** $\eta$ (for TSP, $\eta = 1/d$). After building tours, ants deposit pheromone in
proportion to tour quality, and pheromone **evaporates** everywhere, so good edges are
reinforced (positive feedback) and poor ones fade ([[slides-04-optimization]], slides 12–13;
[[dorigo-1996-ant-system]] §I–II). The first ACO algorithm is the **Ant System** of
[[marco-dorigo]], Maniezzo and Colorni (1996). ACO is a form of [[swarm-intelligence]].

## How it works

**Transition rule** for ant $k$ at node $i$ ([[dorigo-1996-ant-system]] Eq. 4):
$$p_{ij}^k = \frac{\tau_{ij}^{\alpha}\,\eta_{ij}^{\beta}}{\sum_{l \in \text{allowed}_k} \tau_{il}^{\alpha}\,\eta_{il}^{\beta}} \quad \text{for } j \in \text{allowed}_k \;(\text{unvisited, via the tabu list}),\quad 0 \text{ otherwise.}$$

**Pheromone update** after all $m$ ants finish a tour (one *cycle*)
([[dorigo-1996-ant-system]] Eqs. 1–3, ant-cycle):
$$\tau_{ij} \leftarrow \rho\,\tau_{ij} + \sum_{k=1}^{m} \Delta\tau_{ij}^k, \qquad \Delta\tau_{ij}^k = \begin{cases} Q/L_k & \text{if ant } k \text{ used } (i,j) \\ 0 & \text{otherwise}\end{cases}$$
Here $\rho$ is **persistence** and $1-\rho$ the **evaporation**. (Many later texts write
$(1-\rho)\tau$ with $\rho$ = evaporation rate — general knowledge. Check which convention a
question uses.)

**Deposit variants** ([[dorigo-1996-ant-system]] §III): *ant-cycle* $Q/L_k$ after the tour
(global information, best); *ant-density* $Q$ per traversal; *ant-quantity* $Q/d_{ij}$ per
traversal. *Elitist* AS adds $e \cdot Q/L^*$ to edges of the best-so-far tour (§V-C).

```text
initialise τ_ij ← τ0 (small constant) on every edge; η_ij ← 1/d_ij
repeat for NC_MAX cycles (or until stagnation):
    place m ants on start towns; tabu_k ← [start]
    repeat n−1 times:
        each ant k at i chooses j ∉ tabu_k with probability p_ij^k # roulette wheel
        move; append j to tabu_k
    compute every L_k; record the shortest tour
    τ ← ρ·τ (evaporate)
    for each ant k, each edge (i,j) in its tour: τ_ij += Q / L_k
return shortest tour found
```

## Properties

- **Discrete/combinatorial** (graphs, permutations): TSP, asymmetric TSP, quadratic
  assignment, job-shop scheduling ([[dorigo-1996-ant-system]] §VII).
- **Constructive**: ants build solutions; the tabu list enforces feasibility.
- **Complexity** $O(NC \cdot n^2 \cdot m)$ ⇒ $O(NC \cdot n^3)$ with $m \approx n$
  ([[dorigo-1996-ant-system]] §III).
- **Parameters and effects** ([[dorigo-1996-ant-system]] §IV):
  - $\alpha$ (trail weight): $\alpha = 0$ → stochastic greedy with multiple starts; high
    $\alpha$ → rapid **stagnation** (all ants on one tour) with bad tours.
  - $\beta$ (visibility weight): greedy pull toward short edges; best found $\beta = 5$.
  - $\rho$ (persistence): best 0.5 — the colony must forget old experience.
  - $Q$: negligible influence.
  - $m$: best $m \approx n$ (§V-A).
  - Best set: $\alpha = 1, \beta = 5, \rho = 0.5, Q = 100$ (Oliver30: 423.741).
- **Not optimal-guaranteed**, but on Oliver30 ant-cycle matched tabu search and beat simulated
  annealing (mean 420.4 vs 420.6 vs 459.8, integer distances) ([[dorigo-1996-ant-system]]
  §VI-B). Much slower than TSP-specific heuristics like Lin–Kernighan (§VI-A).
- **Memory**: the pheromone matrix ($n^2$) is a shared, distributed memory of the colony's
  experience — stigmergy (indirect communication through the environment; general knowledge).

## In this course

- Slide 12: ACO by Marco Dorigo (1996), a metaheuristic originally for combinatorial problems,
  based on how ant swarms optimise paths to food or around obstacles
  ([[slides-04-optimization]], slide 12).
- Slide 13: ants wander, return with food leaving pheromone, others follow and reinforce;
  evaporation on weak paths lets good solutions gain and poor ones lose pheromone
  ([[slides-04-optimization]], slide 13). Slides 14–15 are image-only, so the formulas above
  come from [[dorigo-1996-ant-system]].
- Raymond's [[ant-colony-py]]: ant-cycle AS on 25 random cities, 100 ants, 100 epochs,
  $\alpha = \beta = 1$, evaporation 0.5, $Q = 100$, $\tau_0 = 1/(n L_{nn})$ from a
  nearest-neighbour tour, roulette-wheel choice. Improves on the nearest-neighbour tour by
  8–19% in re-runs.

## Common mistakes

- Mixing the $\rho$ conventions (persistence vs evaporation).
- Forgetting to restrict the denominator to *allowed* (unvisited) nodes.
- Depositing $Q \cdot L_k$ instead of $Q / L_k$ (would reward long tours).
- Expecting more ants to always help: Dorigo found $m \approx n$ best (§V-A).
- Confusing stagnation (all ants identical) with convergence to the optimum.

## Related

[[swarm-intelligence]], [[particle-swarm-optimization]], [[artificial-bee-colony]],
[[exploration-vs-exploitation]], [[simulated-annealing]], [[genetic-algorithms]],
[[optimization-problems]], [[marco-dorigo]], [[ant-colony-py]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. An ant at city $i$ can go to A, B or C. Pheromone $\tau = (1, 2, 1)$, distances $d = (2, 4, 1)$. Compute the transition probabilities with $\alpha = \beta = 1$.
> **Answer.** $\eta = (0.5, 0.25, 1)$. Weights $\tau\eta = (0.5, 0.5, 1)$, sum 2. $p = (0.25, 0.25,
> 0.5)$ ([[dorigo-1996-ant-system]] Eq. 4).

> [!question]- Q2. Same data with Dorigo's best $\alpha = 1, \beta = 5$.
> **Answer.** $\eta^5 = (0.03125, 0.000977, 1)$; weights $\tau\eta^5 = (0.03125, 0.00195, 1)$, sum
> $\approx 1.0332$. $p \approx (0.030, 0.002, 0.968)$. A large $\beta$ makes the choice almost
> greedy: the short edge to C dominates even though B has twice the pheromone.

> [!question]- Q3. Edge $(i,j)$ has $\tau = 2$. Persistence $\rho = 0.5$, $Q = 100$. Two ants used it this cycle with tour lengths 10 and 20. New $\tau$?
> **Answer.** $\tau' = 0.5 \cdot 2 + 100/10 + 100/20 = 1 + 10 + 5 = 16$
> ([[dorigo-1996-ant-system]] Eqs. 1–3).

> [!question]- Q4. Why did ant-cycle beat ant-density and ant-quantity?
> **Answer.** Ant-cycle deposits $Q/L_k$ after the tour, so the amount reflects the *global*
> quality of the whole solution; the other two deposit as they walk, using only local information
> unrelated to the final tour length ([[dorigo-1996-ant-system]] §IV, Table I).

> [!question]- Q5. What is stagnation, which parameter setting causes it quickly, and how does evaporation help?
> **Answer.** Stagnation: all ants follow the same tour, so no new solutions are explored. High
> $\alpha$ causes it fast. Evaporation lowers pheromone on all edges each cycle, so edges not
> reinforced fade and the colony can "forget" early choices; with $\rho$ too close to 1 trail
> accumulates and search freezes ([[dorigo-1996-ant-system]] §IV).

> [!question]- Q6. What does ACO reduce to with $\alpha = 0$?
> **Answer.** Pheromone is ignored; each ant chooses by visibility only — "a stochastic greedy
> algorithm with multiple starting points" ([[dorigo-1996-ant-system]] §III).
