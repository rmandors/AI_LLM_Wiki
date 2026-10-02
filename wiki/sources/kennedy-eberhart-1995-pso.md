---
type: source
summary: Kennedy & Eberhart's 1995 paper introducing particle swarm optimization, from bird-flocking simulations to the simplified velocity update with constant 2 and no inertia weight.
unit: 9
tags: [particle-swarm-optimization, swarm-intelligence, paper]
sources: ["[[kennedy-eberhart-1995-pso]]"]
updated: 2026-10-01
---

# Kennedy & Eberhart (1995) — "Particle Swarm Optimization"

**Bibliographic line.** J. Kennedy and R. Eberhart, "Particle Swarm Optimization,"
*Proceedings of the IEEE International Conference on Neural Networks*, 1995, pp. 1942–1948.
File: `raw/Papers/2 - Particle_swarm_optimization.pdf`.

**What it is.** The founding paper of [[particle-swarm-optimization]] by
[[kennedy-and-eberhart]] (a social psychologist and an electrical engineer). It tells how a
bird-flock simulation was stripped down into an optimiser for continuous nonlinear functions,
states the update rule, and reports early tests. Cited by the course as "James Kennedy and
Russell Eberhart – 1995" ([[slides-04-optimization]], slide 8).

## Key points

- **Roots (§1, §2).** Two lineages: artificial life (bird flocking, fish schooling — Reynolds,
  Heppner & Grenander) and [[evolutionary-computation]] (GAs, evolutionary programming).
  E. O. Wilson's remark that school members "profit from the discoveries and previous
  experience of all other members" motivated the social-sharing hypothesis.
- **§3.1 Nearest-neighbour velocity matching + "craziness".** First simulation: each agent
  copied its nearest neighbour's velocity; the flock quickly settled on one direction, so
  random "craziness" was added.
- **§3.2 The cornfield vector.** Agents evaluate their position relative to a target at
  (100, 100). Each remembers its best value and position (`pbest`), and all know the group's
  best (`gbest`). Velocities were nudged by `rand*p_increment` toward pbest and
  `rand*g_increment` toward gbest using only the *sign* of the difference. High increments:
  the flock is "sucked violently into the cornfield"; low: it swirls and lands realistically.
- **§3.3 Eliminating ancillary variables.** Craziness and nearest-neighbour matching turned
  out to be unnecessary (optimization was slightly faster without matching — "the flock is
  now a swarm"). pbest ≈ "autobiographical memory"/"simple nostalgia"; gbest ≈ "publicized
  knowledge" or a group norm. Relatively high p_increment → isolated wandering; relatively
  high g_increment → rushing prematurely toward local minima; roughly equal works best.
- **§3.4 Multidimensional search.** Positions become $D \times N$ matrices. Trained a 2-3-1
  XOR network (13 weights) to error < 0.05 in an average of **30.7 iterations with 20
  agents**.
- **§3.5 Acceleration by distance.** Replace the sign test with the actual difference:
  `vx += rand*p_increment*(pbestx - presentx)`.
- **§3.6 Current simplified version — the key equation.** The increments were dropped and the
  random factor multiplied by 2 "to give it a mean of 1, so that agents would 'overfly' the
  target about half the time":
  $$v \leftarrow v + 2\,\mathrm{rand}\,(p_{best} - x) + 2\,\mathrm{rand}\,(g_{best} - x)$$
  (and $x \leftarrow x + v$). There is **no inertia weight** and no stated velocity limit. The
  authors leave open whether 2 is optimal.
- **§3.7 Variants that did not help.** A single term toward the midpoint of pbest and gbest
  converged on that point "whether it was an optimum or not"; "explorers" and "settlers";
  and removing the momentum term $v$ on the right-hand side, which "turned out to be quite
  ineffective at finding global optima".
- **§4 Swarms and particles — Millonas' five principles** of [[swarm-intelligence]]:
  proximity (simple space/time computations), quality (respond to quality factors), diverse
  response (don't commit to narrow channels), stability (don't change mode at every
  environmental change), adaptability (change mode when worth it). PSO is argued to satisfy
  all five. "Particle" was chosen because velocities apply to particles, even mass-less ones.
- **§5 Tests.** Trained NN weights as well as backpropagation (Fisher Iris: average 284
  epochs over 10 sessions); on an EEG spike data set, 92% test accuracy vs 89% for backprop.
  On **Schaffer's f6** (highly multimodal GA benchmark) it found the global optimum every run,
  with evaluation counts comparable to elementary GAs.
- **§6 Conclusions.** PSO sits "between genetic algorithms and evolutionary programming"; the
  pull toward pbest and gbest is "conceptually similar to the crossover operation"; much of
  its success comes from particles hurtling past their target — the momentum term causes
  overshooting, i.e. exploration (see [[exploration-vs-exploitation]]).

## Pages that use this source

[[particle-swarm-optimization]], [[swarm-intelligence]], [[exploration-vs-exploitation]],
[[particle-swarm-py]], [[metaheuristics-comparison]], [[unit-09-optimization-review]].

## Issues found

- The cornfield evaluation formula in §3.2 is garbled in the extraction ("Eval= Jw + 4-"); it
  is a distance-like function that is zero at (100, 100). The exact form is not recoverable
  from the text.
- Bracket-heavy pseudocode (`vx[][]`) is partly mangled but the §3.6 formula is readable.
- The paper does not use the modern inertia weight $w$ or constriction factor; those came
  later (general knowledge: Shi & Eberhart 1998; Clerc & Kennedy 2002). Do not attribute
  $w$ to this paper.
