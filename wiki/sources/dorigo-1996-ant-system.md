---
type: source
summary: Dorigo, Maniezzo & Colorni (1996) Ant System paper — transition rule, pheromone update with evaporation, ant-cycle vs ant-density vs ant-quantity, parameter study on Oliver30 TSP, elitist ants.
unit: 9
tags: [ant-colony-optimization, tsp, swarm-intelligence, paper]
sources: ["[[dorigo-1996-ant-system]]"]
updated: 2026-10-01
---

# Dorigo, Maniezzo & Colorni (1996) — "Ant System"

**Bibliographic line.** M. Dorigo, V. Maniezzo and A. Colorni, "Ant System: Optimization by
a Colony of Cooperating Agents," *IEEE Transactions on Systems, Man, and Cybernetics — Part
B*, 26(1), pp. 29–41, February 1996. File: `raw/Papers/3 - dorigo1996.pdf`.

**What it is.** The journal paper that defines the Ant System (AS), the first
[[ant-colony-optimization]] algorithm, by [[marco-dorigo]] and colleagues, applied mainly to
the Travelling Salesman Problem (TSP). The course cites it as "Marco Dorigo – 1996"
([[slides-04-optimization]], slide 12).

## Key points

- **Main ideas (abstract).** Positive feedback (rapid discovery of good solutions),
  distributed computation (avoids premature convergence), and a constructive greedy heuristic
  (acceptable solutions early on).
- **Biology (§I, Fig. 1).** Almost-blind ants find shortest paths by laying and following
  pheromone. The process is **autocatalytic** (positive feedback): the more ants follow a
  trail, the more attractive it becomes. Obstacle experiment: the shorter side around an
  obstacle accumulates pheromone faster.
- **Model (§II).** $n$ towns, $m$ ants, $d_{ij}$ Euclidean distance. Each ant chooses the next
  town by a probability depending on distance and trail; a **tabu list** forbids already
  visited towns until the tour is complete; on completion it lays trail on every edge used.
  One *cycle* = $n$ iterations, after which every ant has a complete tour.
- **Eq. (1) — trail update:** $\tau_{ij}(t+n) = \rho\,\tau_{ij}(t) + \Delta\tau_{ij}$, where
  **$\rho$ is the trail persistence and $(1-\rho)$ the evaporation**; $\rho < 1$ avoids
  unlimited accumulation.
- **Eq. (2):** $\Delta\tau_{ij} = \sum_{k=1}^{m} \Delta\tau_{ij}^{k}$.
- **Eq. (3) — ant-cycle deposit:** $\Delta\tau_{ij}^{k} = Q / L_k$ if ant $k$ used edge
  $(i,j)$ in its tour, else 0; $L_k$ = tour length, $Q$ a constant. Initial trail
  $\tau_{ij}(0) = c$, a small positive constant.
- **Visibility:** $\eta_{ij} = 1/d_{ij}$, fixed during the run.
- **Eq. (4) — transition probability** for ant $k$ at town $i$:
  $$p_{ij}^{k}(t) = \frac{[\tau_{ij}(t)]^{\alpha}\,[\eta_{ij}]^{\beta}}{\sum_{l \in \text{allowed}_k} [\tau_{il}(t)]^{\alpha}\,[\eta_{il}]^{\beta}} \quad \text{if } j \in \text{allowed}_k, \text{ else } 0$$
  $\alpha$ weights trail, $\beta$ weights visibility. With $\alpha = 0$ the trail is ignored
  and AS becomes "a stochastic greedy algorithm with multiple starting points" (§III).
- **Stagnation (§III, §IV).** All ants making the same tour; the system stops exploring. Used
  as a stopping criterion alongside $NC_{MAX}$.
- **Complexity (§III).** $O(NC \cdot n^2 \cdot m)$; with $m \approx n$ it is $O(NC \cdot n^3)$.
- **Three variants (§III, Eqs. 5–6).** *Ant-density*: deposit $Q$ on each edge as it is
  traversed. *Ant-quantity*: deposit $Q/d_{ij}$ as traversed. *Ant-cycle*: deposit $Q/L_k$
  after the tour. Ant-cycle was best (Table I) because it uses **global** information (tour
  quality); the other two use only local information.
- **Parameter study (§IV).** Defaults $\alpha=1, \beta=1, \rho=0.5, Q=100$; tested
  $\alpha \in \{0, 0.5, 1, 2, 5\}$, $\beta \in \{0,1,2,5\}$, $\rho \in \{0.3, \dots, 0.999\}$,
  $Q \in \{1, 100, 10000\}$; $m = n$; Oliver30 (30-city TSP), 5,000 cycles, 10 trials.
  **Best ant-cycle set: $\alpha = 1, \beta = 5, \rho = 0.5, Q = 100$**; the influence of $Q$
  was negligible. $\rho = 0.5$ is optimal because the algorithm must "forget part of the
  experience gained in the past". High $\alpha$ → fast stagnation with bad tours; too little
  trail importance → bad tours without stagnation; good results in a central band of
  $(\alpha, \beta)$ (Fig. 8).
- **Results.** Table I averages over 10 trials: ant-density 426.740 (best 424.635),
  ant-quantity 427.315 (426.255), **ant-cycle 424.250 (best 423.741)**. A GA in the literature
  had found 424.635; ant-cycle found **423.741** (integer length 420) after 342 cycles
  (Fig. 9).
- **§V-A Synergy.** Communicating ants ($\alpha > 0$) beat non-communicating ones; the optimal
  number of ants is close to the number of cities ($m \approx n$).
- **§V-B Initialisation.** Spreading ants over different towns beats starting all in one
  town; random vs uniform spreading made little difference.
- **§V-C Elitist strategy.** Each cycle, edges of the best-so-far tour get extra trail
  $e \cdot Q / L^*$ ($e$ elitist ants). There is an optimal range of $e$; too many force search
  around suboptimal tours (Fig. 14). With $e = 8$, AS always found 423.741 on Oliver30 in under
  400 cycles and never stagnated.
- **§VI Comparisons.** On Oliver30 (integer distances, 1 h on a 386 PC): AS best 420, mean
  420.4 (sd 1.3); tabu search 420, 420.6 (1.5); simulated annealing 422, 459.8 (25.1). AS
  beat 2-opt and was comparable to Lin–Kernighan but was much slower than TSP-specific
  heuristics. See [[simulated-annealing]].
- **§VII Generality.** Also applied to asymmetric TSP, quadratic assignment and job-shop
  scheduling.
- **§VIII–IX Interpretation.** An isolated greedy ant makes good early moves but bad forced
  final moves; with many ants, good path segments collect more trail. Information gained
  during search modifies the problem representation so that bad tours become improbable.

## Pages that use this source

[[ant-colony-optimization]], [[swarm-intelligence]], [[exploration-vs-exploitation]],
[[ant-colony-py]], [[simulated-annealing]], [[metaheuristics-comparison]],
[[unit-09-optimization-review]].

## Issues found

- The bodies of **Eq. (2) and Eq. (4)** are missing from the extraction; Greek letters come
  out as Latin ("a" for α, "p" for both β and ρ). The formulas above were reconstructed from
  the surrounding definitions and the standard statement of the Ant System (general
  knowledge for the exact typography; the content matches the paper's prose).
- **Notation trap.** In this paper $\rho$ is *persistence* and $(1-\rho)$ evaporation. Many
  later texts write $\tau \leftarrow (1-\rho)\tau + \Delta\tau$, with $\rho$ as the
  *evaporation rate* (general knowledge). With $\rho = 0.5$ both readings coincide, which is
  why [[ant-colony-py]] (`EVAPORATION_RATE = 0.5`) matches the paper either way.
