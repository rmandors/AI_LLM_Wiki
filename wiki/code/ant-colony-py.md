---
type: code
summary: Walkthrough of Raymond's Ant_colony.py — an ant-cycle Ant System for a random 25-city Euclidean TSP (100 ants, α=β=1, evaporation 0.5, Q=100, nearest-neighbour τ0) that beats the nearest-neighbour tour by 8–19%.
unit: 9
tags: [ant-colony-optimization, tsp, code, class-exercise, raymond-work]
sources: ["[[dorigo-1996-ant-system]]", "[[slides-04-optimization]]"]
updated: 2026-10-01
---

# `Ant_colony.py` — Raymond's ACO class exercise

**File:** `raw/Class_exercises/Genetic Algorithm Exercise/Ant_colony.py` (227 lines, NumPy +
Matplotlib).

**Problem.** Find a short closed tour through 25 cities placed uniformly at random in a 100×100
plane (fully connected, Euclidean distances) using [[ant-colony-optimization]] — the Ant System of
[[dorigo-1996-ant-system]].

## Design decisions

| Choice | Value | Dorigo 1996 | Comment |
|---|---|---|---|
| Cities $n$ | 25 random | Oliver30 (30 fixed) | new instance every run |
| Ants $m$ | 100 | best $m \approx n$ (§V-A) | 4× more ants than cities |
| Cycles | 100 epochs | 2,500–5,000 cycles | |
| $\alpha$ (pheromone weight) | 1 | 1 | |
| $\beta$ (visibility weight) | **1** | **5** best (§IV) | defaults in Dorigo's study were also $\beta = 1$ |
| Evaporation | `EVAPORATION_RATE = 0.5` → multiply by $1 - 0.5$ | persistence $\rho = 0.5$ | same number under both conventions |
| $Q$ | 100 | 100 | |
| Deposit | $Q/L_k$ by **every** ant on every edge of its tour | ant-cycle, Eq. 3 | no elitist ants |
| Initial trail $\tau_0$ | $1/(n \cdot L_{nn})$, $L_{nn}$ = nearest-neighbour tour length | small constant $c$ | the $1/(nL_{nn})$ rule is the one used in Ant Colony System (general knowledge) |
| Visibility $\eta$ | $1/d_{ij}$ | $1/d_{ij}$ | |
| Next-city choice | roulette wheel over unvisited cities with weights $\tau^\alpha\eta^\beta$ | Eq. 4 | |
| Start city | random per ant | uniform spread slightly better than all-in-one (§V-B) | |
| Best tour | best of (NN tour, every epoch's best ant) | | |

## Walkthrough

- **L4–12 constants.**
- **L15–16 `create_cities`** — uniform points in $[0, 100]^2$.
- **L19–30 `distance_matrix`** — symmetric Euclidean matrix, zero diagonal.
- **L33–55 `nearest_neighbor_tour`** — greedy tour from a random start city: always go to the
  closest unvisited city. Used for $\tau_0$ and as the initial best.
- **L58–65 `tour_length`** — closed tour length (wraps back to the start).
- **L68–107 `construct_tour`** — one ant: start at a random city; for each step build `allowed`
  (unvisited) and `weights = τ^α · η^β`; roulette-wheel choice (L95–103); fallback to uniform choice
  if all weights are 0 (L92–94). Implements Eq. 4 with a tabu-list equivalent (`visited`).
- **L111–127 `update_pheromone`** — evaporate every entry by `1 − EVAPORATION_RATE`, then each ant
  adds `Q / L_k` to both directions of every edge it used. Eqs. 1–3, ant-cycle.
- **L130–137 `heuristic_matrix`** — $\eta_{ij} = 1/d_{ij}$ off the diagonal.
- **L140–150 `initialize_pheromone`** — computes the NN tour and sets every off-diagonal
  $\tau_{ij} = 1/(n L_{nn})$.
- **L153–167 `run_ants`** — all 100 ants build tours, pheromone updated once, epoch-best returned.
- **L170–199 `plot_results`** — convergence curve + best tour drawing.
- **L202–227 main** — instance, matrices, initial best = NN tour, 100 epochs, print, plot.

## Results

Re-runs (2026-10-01, seeds 0–2, unmodified code; each seed is a different city set):

| Seed | $\tau_0$ | NN tour | ACO best | Improvement | Last improvement |
|---|---|---|---|---|---|
| 0 | $6.8\times10^{-5}$ | 587.38 | 477.70 | 18.7% | epoch 72 |
| 1 | $9.4\times10^{-5}$ | 426.17 | 392.05 | 8.0% | epoch 18 |
| 2 | $8.9\times10^{-5}$ | 449.32 | 382.73 | 14.8% | epoch 64 |

Same seeds with `BETA = 5` (Dorigo's best): 475.37, 393.43, 382.15 — no consistent difference on
these 25-city instances (two slightly better, one slightly worse, all within 0.6%). Optimality cannot be
checked without an exact solver; these numbers only show improvement over the greedy baseline.

## Known issues / improvements

1. **$\tau_0$ is effectively irrelevant.** One ant deposits $Q/L \approx 100/450 \approx 0.2$ per
   edge, and 100 ants deposit on the first cycle, while $\tau_0 \approx 10^{-4}$. After the first
   update the initial value is swamped by 3–4 orders of magnitude. The $1/(nL_{nn})$ initialisation
   makes sense in Ant Colony System, where deposits are small and local updates pull edges back
   toward $\tau_0$ (general knowledge); in plain AS any small constant would do — Dorigo used a
   "small positive constant" ([[dorigo-1996-ant-system]] §II).
2. **$\beta = 1$ vs Dorigo's 5.** Defensible as Dorigo's default, but his best ant-cycle setting
   was $\beta = 5$; worth knowing.
3. **$m = 100 \gg n = 25$.** Dorigo found $m \approx n$ most efficient; 100 ants cost 4× the work
   per cycle.
4. **No elitist ants / no local search.** Adding $e \cdot Q/L^*$ on the best tour (e ≈ 8 worked in
   [[dorigo-1996-ant-system]] §V-C) or 2-opt would likely improve tours.
5. **No stagnation measure.** Pheromone ranged from about $10^{-11}$ to 36 at the end of seed 2,
   so some edges are effectively deleted; tracking node branching or tour-length variance would
   show how close the colony is to stagnation.
6. Pure-Python loops ($O(m n^2)$ per cycle) make it slow; vectorising the probability computation
   would speed it up.

## Related concepts

[[ant-colony-optimization]], [[swarm-intelligence]], [[exploration-vs-exploitation]],
[[optimization-problems]], [[greedy-best-first-search]] (the NN tour is a greedy construction),
[[marco-dorigo]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Which Ant System variant is this, and why?
> **Answer.** Ant-cycle: each ant deposits $Q/L_k$ on all edges of its tour after completing it,
> so the deposit reflects global tour quality ([[dorigo-1996-ant-system]] Eq. 3, §IV).

> [!question]- Q2. With your code's evaporation, what happens to an edge with $\tau = 4$ that no ant uses for 3 epochs?
> **Answer.** Multiplied by $0.5$ each epoch: $4 \to 2 \to 1 \to 0.5$. After 10 unused epochs it is
> $4/1024 \approx 0.004$ — evaporation quickly erases unused edges.

> [!question]- Q3. Why initialise pheromone with $1/(n L_{nn})$? Does it matter here?
> **Answer.** It sets $\tau_0$ on the scale of one good tour's contribution, a rule from Ant Colony
> System (general knowledge). Here it barely matters: the first deposit (~0.2 per ant per edge, 100
> ants) dwarfs $\tau_0 \approx 10^{-4}$.

> [!question]- Q4. You use $\beta = 1$; Dorigo recommends $\beta = 5$. What would change?
> **Answer.** A higher $\beta$ makes ants much greedier toward short edges, giving better tours
> early and, per Dorigo, better final tours on Oliver30. In my re-runs on 25 cities the final
> lengths with $\beta = 5$ were within ±0.6% of $\beta = 1$.

> [!question]- Q5. How would you make it an elitist Ant System?
> **Answer.** After the normal update, add $e \cdot Q/L^*$ to every edge of the best-so-far tour
> $L^*$, with $e$ elitist ants (Dorigo found an optimal range; $e = 8$ worked on Oliver30)
> ([[dorigo-1996-ant-system]] §V-C).
