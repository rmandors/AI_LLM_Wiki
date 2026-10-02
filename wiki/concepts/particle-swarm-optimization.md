---
type: concept
summary: Particle swarm optimization moves a swarm of particles through a continuous space, each velocity pulled at random toward the particle's personal best and the swarm's global best (Kennedy & Eberhart 1995).
unit: 9
tags: [particle-swarm-optimization, swarm-intelligence, continuous, metaheuristics]
sources: ["[[slides-04-optimization]]", "[[kennedy-eberhart-1995-pso]]", "[[eiben-smith-evolutionary-computing]]"]
updated: 2026-10-01
---

# Particle swarm optimization (PSO)

**Particle swarm optimization** is a stochastic, population-based optimiser for continuous
functions, introduced by [[kennedy-and-eberhart]] in 1995 from simulations of bird flocks and
fish schools ([[slides-04-optimization]], slide 8; [[kennedy-eberhart-1995-pso]] §1). Each
particle is a candidate point $x$ with a velocity $v$; it remembers the best point it has
visited ($p_{best}$, "autobiographical memory") and knows the best point the whole swarm has
found ($g_{best}$, "publicized knowledge"). Every step, the velocity is nudged at random toward
both, and the particle moves ([[kennedy-eberhart-1995-pso]] §3.3, §3.6). It is a core example of
[[swarm-intelligence]].

## How it works

**Original update** ([[kennedy-eberhart-1995-pso]] §3.6), per particle $i$ and per dimension
$d$, with fresh $r_1, r_2 \sim U[0,1]$:
$$v_{id} \leftarrow v_{id} + 2\,r_1\,(p_{best,id} - x_{id}) + 2\,r_2\,(g_{best,d} - x_{id}), \qquad x_{id} \leftarrow x_{id} + v_{id}$$
The factor 2 gives the random term mean 1 so particles "overfly" the target about half the time.
No inertia weight, no velocity clamp in the paper.

**Modern form with inertia** ([[eiben-smith-evolutionary-computing]] §6.7):
$$v_i' = w\, v_i + \varphi_1 U_1 (b_i - x_i) + \varphi_2 U_2 (c - x_i), \qquad x_i' = x_i + v_i'$$
$w$ = inertia; $\varphi_1$ = cognitive (personal) learning rate; $\varphi_2$ = social learning
rate; $U_1, U_2$ = diagonal matrices of independent $U[0,1]$ draws (one per coordinate); $b_i$ =
personal best; $c$ = global best ("champion"). Personal best update: $b_i' = x_i'$ if
$f(x_i') < f(b_i)$, else $b_i$. Setting $w = 1$, $\varphi_1 = \varphi_2 = 2$ recovers the 1995
rule.

> [!note] Slide notation
> The slides call $\varphi_1, \varphi_2$ "random variables uniformly distributed over $[0,1]$"
> ([[slides-04-optimization]], slide 9) — i.e. the slide's $\varphi$ is the book's $U$, and the
> constant multipliers (2 in the paper) are separate. The velocity formula on slide 9 is an
> image and did not extract.

```text
for each particle i: x_i ← random in bounds; v_i ← 0 (or small random); p_i ← x_i
g ← argmin_i f(p_i)
repeat for T iterations:
    for each particle i:
        r1, r2 ← U[0,1]^D # one per dimension
        v_i ← w·v_i + c1·r1⊙(p_i − x_i) + c2·r2⊙(g − x_i)
        (optional) clamp v_i to [−v_max, v_max]
        x_i ← x_i + v_i
        if f(x_i) < f(p_i): p_i ← x_i
        if f(x_i) < f(g): g ← x_i
return g
```

## Properties

- **Continuous** search spaces; derivative-free; few parameters; a few lines of code
  ([[kennedy-eberhart-1995-pso]] §1, §6).
- **Not guaranteed** to find the global optimum; can converge prematurely if the social pull
  dominates — high g_increment made the flock rush "prematurely toward local minima"
  ([[kennedy-eberhart-1995-pso]] §3.3).
- **Parameter roles:**
  - $w$ (inertia): large → exploration/overshoot; small → quick contraction. Typical 0.4–0.9,
    often decreased over the run (general knowledge).
  - $c_1$ vs $c_2$: personal vs social; roughly equal works best
    ([[kennedy-eberhart-1995-pso]] §3.3).
  - Swarm size: 20–50 typical; the paper's XOR test used 20 (general knowledge;
    [[kennedy-eberhart-1995-pso]] §3.4).
  - $v_{max}$ or a **constriction factor** $\chi \approx 0.7298$ with $c_1 = c_2 \approx 1.496$
    keeps the swarm from exploding (general knowledge: Clerc & Kennedy 2002).
- **Stability.** With no inertia damping ($w = 1$) and $c_1 + c_2 = 4$, the velocity recurrence
  is not damped and random factors make the oscillation amplitude grow (general knowledge). This
  is visible in Raymond's run: max $|v|$ reached $10^6$–$10^8$ by iteration 100
  ([[particle-swarm-py]]).
- **Memory:** each particle stores $x, v, p_{best}$; swarm stores $g_{best}$. Unlike GAs, PSO
  populations are ordered lists with identities ([[eiben-smith-evolutionary-computing]] §6.7).
- **Relation to EAs:** no crossover; "mutation" is vector addition; moving toward pbest and
  gbest is "conceptually similar to the crossover operation"
  ([[eiben-smith-evolutionary-computing]] §6.7; [[kennedy-eberhart-1995-pso]] §6).

## In this course

- Slides 8–9: PSO by Kennedy & Eberhart (1995), stochastic, inspired by birds, fish and swarm
  theory; particles have $x_t$, $v_t$, $p_{best}$; the swarm keeps $g_{best}$; $\varphi_1,
  \varphi_2 \sim U[0,1]$ ([[slides-04-optimization]], slides 8–9). Slide 10 labels exploration
  vs exploitation; slide 11 is image-only.
- Raymond's [[particle-swarm-py]] implements exactly the 1995 rule ($\alpha_1 = \alpha_2 = 2$,
  no inertia, no clamping) on $(x+2)^2 + (y-2)^2 + 10$ with 100 particles and 100 epochs. It
  gets within ~0.03–0.05 of the optimum in about 20 iterations, then the swarm diverges and
  $g_{best}$ stops improving. One deviation from the paper: it draws **one** $r_1, r_2$ per
  particle, not per dimension.

## Common mistakes

- Forgetting to update $p_{best}$/$g_{best}$ *after* moving, or comparing in the wrong
  direction for minimisation.
- Using the same random number for every dimension (changes the search geometry: the pull
  becomes a straight line toward pbest/gbest).
- Leaving out both inertia damping and velocity limits.
- Attributing the inertia weight $w$ to the 1995 paper (it came later).
- Removing the momentum term entirely ($v \leftarrow$ only the attraction terms): the paper
  found this "quite ineffective at finding global optima" ([[kennedy-eberhart-1995-pso]] §3.7).

## Related

[[swarm-intelligence]], [[ant-colony-optimization]], [[artificial-bee-colony]],
[[genetic-algorithms]], [[evolutionary-computation]], [[exploration-vs-exploitation]],
[[gradient-descent]], [[kennedy-and-eberhart]], [[particle-swarm-py]],
[[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. 1-D original PSO: $x = 2$, $v = 1$, $p_{best} = 3$, $g_{best} = 5$, $r_1 = 0.5$, $r_2 = 0.25$. Compute the new velocity and position.
> **Answer.** $v' = 1 + 2(0.5)(3-2) + 2(0.25)(5-2) = 1 + 1 + 1.5 = 3.5$; $x' = 2 + 3.5 = 5.5$.
> The particle overshoots $g_{best}$ — the "overfly" behaviour the factor 2 was chosen to
> produce ([[kennedy-eberhart-1995-pso]] §3.6).

> [!question]- Q2. Same numbers with inertia $w = 0.7$ and $c_1 = c_2 = 1.5$.
> **Answer.** $v' = 0.7(1) + 1.5(0.5)(1) + 1.5(0.25)(3) = 0.7 + 0.75 + 1.125 = 2.575$;
> $x' = 4.575$ — it now stops short of $g_{best}$ ([[eiben-smith-evolutionary-computing]] §6.7).

> [!question]- Q3. What do $p_{best}$ and $g_{best}$ represent socially, and what happens if one dominates?
> **Answer.** $p_{best}$ = individual memory ("simple nostalgia"); $g_{best}$ = group norm /
> publicized knowledge. Too much personal pull → isolated particles wander; too much social pull
> → the swarm rushes prematurely to a local minimum. Roughly equal weights worked best
> ([[kennedy-eberhart-1995-pso]] §3.3).

> [!question]- Q4. Why did Kennedy and Eberhart multiply rand by 2?
> **Answer.** To give the stochastic factor a mean of 1, so that agents "overfly" the target
> about half the time — overshooting gives exploration ([[kennedy-eberhart-1995-pso]] §3.6, §6).

> [!question]- Q5. In Raymond's run the swarm finds $f \approx 10.002$ by iteration ~20 and then never improves, while velocities grow to $10^7$. Explain and propose two fixes.
> **Answer.** With no inertia damping and $c_1 + c_2 = 4$, each velocity keeps all its momentum
> and receives random kicks of up to 2× the distance to the attractors; oscillations grow, so
> particles fly ever farther from $g_{best}$ and stop sampling near it. Fixes: inertia $w \approx
> 0.7$ (or decreasing 0.9→0.4), a constriction factor, or velocity clamping $v_{max}$; also
> bound positions to the search box ([[particle-swarm-py]]; general knowledge for the fixes).

> [!question]- Q6. Which of Millonas' swarm principles does PSO satisfy through the split between $p_{best}$ and $g_{best}$?
> **Answer.** The principle of **diverse response** — the allocation of responses between
> pbest and gbest keeps the population from committing to narrow channels
> ([[kennedy-eberhart-1995-pso]] §4).
