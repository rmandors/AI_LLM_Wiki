---
type: code
summary: Walkthrough of Raymond's Particle_swarm.py — the original 1995 PSO (α1=α2=2, no inertia, no velocity clamp) on (x+2)²+(y−2)²+10; converges to f≈10.002 in ~20 iterations, then the swarm diverges.
unit: 9
tags: [particle-swarm-optimization, code, class-exercise, raymond-work]
sources: ["[[kennedy-eberhart-1995-pso]]", "[[eiben-smith-evolutionary-computing]]", "[[slides-04-optimization]]"]
updated: 2026-10-01
---

# `Particle_swarm.py` — Raymond's PSO class exercise

**File:** `raw/Class_exercises/Genetic Algorithm Exercise/Particle_swarm.py` (89 lines, NumPy
only; no plot).

**Problem.** Minimise the same $f(x,y) = (x+2)^2 + (y-2)^2 + 10$ as [[genetic-algorithm-py]],
in continuous space, with [[particle-swarm-optimization]].

## Design decisions

| Choice | Value | Comment |
|---|---|---|
| Swarm size / iterations | 100 particles, 100 epochs | |
| Dimensions | 2 | `objective` generalises to $D$ dims (target −2 in dim 0, +2 in dim 1, 0 elsewhere) |
| Cognitive / social weights | `ALPHA1 = ALPHA2 = 2.0` | exactly the 1995 constants ([[kennedy-eberhart-1995-pso]] §3.6) |
| Random factors | `phi1, phi2 = np.random.random` | **one scalar per particle per step**, shared by both dimensions |
| Inertia | none ($w = 1$ implicitly) | original version, before inertia weights |
| Velocity clamp | none | |
| Initial positions | $U(-10, 10)^2$ | bounds used only at initialisation |
| Initial velocities | zero | |
| Topology | global best (gbest) | |

## Walkthrough

- **L3–11 constants.**
- **L14–20 `objective(position)`** — squared distance to $(-2, 2)$ plus 10.
- **L23–44 `initialize_particles`** — random positions, zero velocities, pbest = start; tracks
  the initial global best (position copied, so no aliasing).
- **L47–55 `update_particles(particles, g)`** — for each particle draws `phi1`, `phi2`, then
  `v = v + 2·phi1·(pbest − x) + 2·phi2·(g − x)` and `x = x + v`. This is the §3.6 rule of
  [[kennedy-eberhart-1995-pso]], with the slide's notation ($\varphi \sim U[0,1]$,
  [[slides-04-optimization]], slide 9).
- **L58–70 `evaluate_particles`** — updates each pbest if improved, and the global best if
  improved; returns the new global best.
- **L73–90 main** — initialise; each epoch: update all particles with last epoch's $g_{best}$
  (synchronous), then evaluate; print epochs 1–10 and every 10th.

**Is the global-best bookkeeping correct?** Yes. `evaluate_particles` receives the current best,
updates local variables, and returns them; the main loop reassigns both (L82–84), and positions
are copied (`.copy`), so later in-place changes cannot corrupt $g_{best}$. The only subtlety is
that particles move using the $g_{best}$ from the *previous* epoch (synchronous update), which is
standard.

## Results

Re-runs (2026-10-01, seeds 0–4, unmodified code):

| Seed | $f$ initial best | $f$ at epoch 10 | final $f$ | last $g_{best}$ improvement | max $\lvert v\rvert$ at epoch 10 → 100 |
|---|---|---|---|---|---|
| 0 | 10.244 | 10.0104 | 10.00218 | epoch 21 | 160 → $3.4\times10^{7}$ |
| 1 | 10.802 | 10.0087 | 10.00237 | 21 | 88 → $9.4\times10^{6}$ |
| 2 | 10.777 | 10.0077 | 10.00117 | 14 | 165 → $1.4\times10^{8}$ |
| 3 | 11.743 | 10.0226 | 10.00272 | 24 | 213 → $1.4\times10^{6}$ |
| 4 | 10.233 | 10.0044 | 10.00132 | 23 | 385 → $4.5\times10^{6}$ |

So the swarm finds a point within ~0.03–0.05 of $(-2, 2)$ in about 15–25 iterations and **never
improves again**; by epoch 100 the mean particle distance from the optimum is $10^5$–$10^6$. The
best answer comes from early luck, not from convergence.

## Known issues / improvements

1. **Divergence (swarm explosion).** With no inertia damping and $c_1 + c_2 = 4$, velocities
   keep all momentum and receive random kicks proportional to the distance to the attractors; the
   oscillation grows without bound (general knowledge; observed above). Fix: inertia $w \approx
   0.7$ or linearly decreasing 0.9 → 0.4, the constriction factor $\chi \approx 0.73$ with $c_1 =
   c_2 \approx 1.5$, and/or velocity clamping $v_{max}$ (general knowledge).
   [[eiben-smith-evolutionary-computing]] §6.7 presents the inertia form.
2. **Scalar random factors.** The paper's `rand` is applied per element of the agent×dimension
   matrix, and Eiben & Smith's $U_1, U_2$ are diagonal matrices with one draw per coordinate. Here
   one `phi` is shared by both coordinates, so each attraction acts along a straight line and
   the swarm explores less of the plane.
3. **No position bounds** after initialisation — particles leave $[-10, 10]^2$ freely (harmless
   for this unbounded paraboloid, wrong for a constrained problem).
4. **No convergence check / history plot** — the console output hides the divergence; plotting
   swarm spread or $\max|v|$ would reveal it.
5. Fair comparison with [[genetic-algorithm-py]]: the GA reaches exactly $f = 10$ only because its
   0.1-grid contains the optimum; PSO works in continuous space where an exact 10 is never hit.

## Related concepts

[[particle-swarm-optimization]], [[swarm-intelligence]], [[exploration-vs-exploitation]],
[[genetic-algorithm-py]], [[kennedy-and-eberhart]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Which PSO version did you implement, and how do you know?
> **Answer.** The original 1995 simplified version: $v \leftarrow v + 2r_1(p - x) + 2r_2(g - x)$,
> with constants 2 and no inertia weight ([[kennedy-eberhart-1995-pso]] §3.6). Modern PSO adds an
> inertia $w$ ([[eiben-smith-evolutionary-computing]] §6.7).

> [!question]- Q2. Trace one update: particle at $(0, 0)$, $v = (0, 0)$, $p_{best} = (0,0)$, $g_{best} = (-2, 2)$, `phi2 = 0.75`.
> **Answer.** Cognitive term is 0 (particle is at its pbest). Social: $2 \cdot 0.75 \cdot ((-2,2) -
> (0,0)) = (-3, 3)$. New $v = (-3, 3)$, new $x = (-3, 3)$ — it overshoots $g_{best}$ by 1 in each
> coordinate.

> [!question]- Q3. Your best $f$ stops improving after ~20 iterations. Why?
> **Answer.** Without inertia damping or velocity limits the velocities grow (max $|v|$ reaches
> $10^6$–$10^8$), so particles are flung far from $g_{best}$ and stop sampling near it. Adding
> $w < 1$ or a constriction factor would let the swarm contract.

> [!question]- Q4. Is the global-best update correct?
> **Answer.** Yes: it is updated whenever a particle's new fitness beats it, the function returns
> the new value, and main reassigns it; positions are copied. Particles use last epoch's
> $g_{best}$, a synchronous update.

> [!question]- Q5. What would change if `phi1` and `phi2` were drawn per dimension?
> **Answer.** Each coordinate would get its own random weight, so the attraction would no longer be
> a straight line toward pbest/gbest; the swarm samples a box rather than a segment, which is the
> standard formulation and adds diversity ([[eiben-smith-evolutionary-computing]] §6.7).
