---
type: exam-review
summary: Unit 9 cheat sheet — optimization landscape, hill climbing, gradient descent, simulated annealing, GA, schema theorem, PSO, ACO and ABC with all update formulas, parameter effects, traps and 14 practice questions.
unit: 9
tags: [exam-review, optimization, metaheuristics]
sources: ["[[slides-04-optimization]]", "[[russell-norvig-aima]]", "[[eiben-smith-evolutionary-computing]]", "[[holland-1992-genetic-algorithms]]", "[[kennedy-eberhart-1995-pso]]", "[[dorigo-1996-ant-system]]"]
updated: 2026-10-01
---

# Unit 9 review — Optimization and bio-inspired algorithms

Main source: [[slides-04-optimization]] (slides 7, 11, 14, 15, 19 are image-only; formulas on 9
and 18 missing — filled from the papers). Concept pages: [[optimization-problems]],
[[exploration-vs-exploitation]], [[hill-climbing]], [[gradient-descent]],
[[simulated-annealing]], [[evolutionary-computation]], [[genetic-algorithms]],
[[schema-theory-and-building-blocks]], [[swarm-intelligence]],
[[particle-swarm-optimization]], [[ant-colony-optimization]], [[artificial-bee-colony]].
Big table: [[metaheuristics-comparison]].

## Must-know definitions

- **Optimization problem**: find the state maximising/minimising an objective; path irrelevant.
  **Local search** keeps one/few states, little memory, not systematic ([[russell-norvig-aima]]
  §4.1).
- **Landscape**: global/local maximum, plateau (flat), shoulder (flat with exit), ridge
  ([[russell-norvig-aima]] Fig. 4.1, 4.4).
- **Exploration** = sample new regions; **exploitation** = refine near good ones;
  **premature convergence** = diversity lost too early ([[eiben-smith-evolutionary-computing]]
  §3.5).
- **Evolutionary computation** history per slides: Fogel 1960 (finite-state machines),
  Rechenberg & Schwefel 1970 (evolution strategies), Holland 1975 (GAs)
  ([[slides-04-optimization]], slide 2). Textbooks: all three dialects arose in the 1960s.
- **Adaptation / heredity / natural selection** ([[slides-04-optimization]], slide 3).
- **Swarm intelligence**: collective behaviour of simple agents sharing information; Millonas'
  principles: proximity, quality, diverse response, stability, adaptability
  ([[kennedy-eberhart-1995-pso]] §4).

## Formula sheet

**Hill climbing**: move to best neighbour while it improves; random restart expects $1/p$ runs
and $\text{cost}_{succ} + \frac{1-p}{p}\text{cost}_{fail}$ steps ([[russell-norvig-aima]]
§4.1.1).

**Gradient descent**: $w \leftarrow w - \eta \nabla f(w)$. On $\|w - w^*\|^2$: error × $(1-2\eta)$
per step; converges iff $0 < \eta < 1$ (derived on [[gradient-descent]]).

**Simulated annealing** (minimise): $\Delta = f(\text{next}) - f(\text{cur})$; accept if
$\Delta < 0$, else w.p. $e^{-\Delta/T}$. R&N Global Ed.: $\Delta E = \text{VALUE(cur)} -
\text{VALUE(next)}$, accept if $\Delta E > 0$, else $e^{\Delta E/T}$ (same rule). Geometric
cooling $T_{k+1} = aT_k$ ([[russell-norvig-aima]] Fig. 4.5).

**GA**:
- Roulette (FPS): $P(i) = f_i/\sum_j f_j$; tournament: best of $k$ random.
- One-point crossover at $r \in [1, l-1]$: child 1 = P1[1..r] + P2[r+1..l].
- Bit-flip mutation: each bit w.p. $p_m$; expected flips $L p_m$; $P(\text{no flip}) = (1-p_m)^L$.
- Takeover time FPS: $\tau^* = \lambda\ln\lambda$ ([[eiben-smith-evolutionary-computing]] §5.4).

**Schema theorem**: $m(H,t+1) \ge m(H,t)\frac{f(H)}{\langle f\rangle}\left[1 - p_c\frac{d(H)}{l-1}\right][1 - p_m o(H)]$
([[eiben-smith-evolutionary-computing]] Eq. 16.1).

**PSO**:
- Original (1995): $v \leftarrow v + 2r_1(p_{best} - x) + 2r_2(g_{best} - x)$, $x \leftarrow x + v$,
  $r_i \sim U[0,1]$ ([[kennedy-eberhart-1995-pso]] §3.6).
- With inertia: $v' = wv + \varphi_1 U_1(b - x) + \varphi_2 U_2(c - x)$
  ([[eiben-smith-evolutionary-computing]] §6.7).

**ACO (Ant System)** ([[dorigo-1996-ant-system]] Eqs. 1–4):
- $p_{ij}^k = \dfrac{\tau_{ij}^\alpha \eta_{ij}^\beta}{\sum_{l \in \text{allowed}_k}\tau_{il}^\alpha\eta_{il}^\beta}$, $\eta_{ij} = 1/d_{ij}$.
- $\tau_{ij} \leftarrow \rho\,\tau_{ij} + \sum_k \Delta\tau_{ij}^k$, $\Delta\tau_{ij}^k = Q/L_k$ (ant-cycle);
  $1 - \rho$ = evaporation.
- Elitist: $+\,e\,Q/L^*$ on best tour's edges.

**ABC** (general knowledge; slide formula is an image):
- $v_{ij} = x_{ij} + \phi_{ij}(x_{ij} - x_{kj})$, $\phi_{ij} \sim U[-1,1]$, $k \ne i$ random, $j$
  random ([[slides-04-optimization]], slide 18 gives $k \in \{1..BN\}$, $j \in \{1..D\}$).
- $\text{fit}_i = 1/(1+f_i)$ if $f_i \ge 0$ else $1 + |f_i|$; $p_i = \text{fit}_i / \sum_n
  \text{fit}_n$.
- Abandon a source when trials > limit (scout). Parameters: $SN$ (=BN), limit, MCN.

## Parameter effects (one line each)

| Parameter | ↑ increases | Risk if too high | Risk if too low |
|---|---|---|---|
| SA $T_0$ / slow cooling | exploration | wasted time (random walk) | stuck like hill climbing |
| GA $p_m$ | exploration | random search | no new genes once converged |
| GA selection pressure ($k$, truncation, elitism) | exploitation | premature convergence | slow progress |
| PSO $w$ | exploration/momentum | divergence (swarm explosion) | premature collapse |
| PSO $c_1$ vs $c_2$ | personal vs social | $c_1$: wandering; $c_2$: rush to local min | — |
| ACO $\alpha$ | trail exploitation | stagnation | greedy multistart |
| ACO $\beta$ | greediness toward short edges | near-deterministic greedy | ignores distances |
| ACO $\rho$ (persistence) | memory | stagnation | forgets good tours |
| ABC limit | exploitation of each source | wasted trials on exhausted sources | too many restarts |

Dorigo's best: $\alpha = 1, \beta = 5, \rho = 0.5, Q = 100$, $m \approx n$; Oliver30 best 423.741
([[dorigo-1996-ant-system]] §IV).

## Must-know facts

- GA ≈ **stochastic beam search + crossover**; mixing number $\rho = 1$ is stochastic beam search
  ([[russell-norvig-aima]] §4.1.4; [[beam-search]]).
- Simple GA (Table 6.1): bit strings, 1-point crossover, bit-flip, roulette FPS, generational,
  **no elitism** ([[eiben-smith-evolutionary-computing]] §6.1).
- Holland: mutation ≈ 1 in 10,000 bits, "insurance" against uniformity; offspring replace
  low-fitness strings; implicit parallelism; compact building blocks survive crossover
  ([[holland-1992-genetic-algorithms]], p. 68).
- PSO 1995: factor 2 gives mean 1 so particles overfly the target half the time; removing the
  momentum term made it ineffective ([[kennedy-eberhart-1995-pso]] §3.6–3.7).
- ACO: ant-cycle > ant-density > ant-quantity because it uses global (tour-length) information;
  $\alpha = 0$ ⇒ stochastic greedy ([[dorigo-1996-ant-system]] §III–IV).
- ABC: employed + onlooker = exploitation; scouts = exploration ([[slides-04-optimization]],
  slide 17).
- 8-queens hill climbing: 14% success; 94% with ≤100 sideways moves ([[russell-norvig-aima]]
  §4.1.1).

## Common traps

- SA sign: worse moves get $e^{-|\text{worsening}|/T}$, never > 1.
- ACO $\rho$: persistence (Dorigo) vs evaporation (many later texts).
- PSO $\varphi$: random numbers on the slide; constant learning rates in Eiben & Smith.
- "Holland 1992" on slide 5 = the Scientific American article, not the invention date (1975 book;
  technique from the mid-1960s).
- Elitism ≠ part of the simple GA; FPS needs positive, maximised fitness.
- Crossover point range is $[1, l-1]$.
- Gradient descent converges to *a* stationary point, not the global minimum.

## Raymond's code — points to remember

- [[genetic-algorithm-py]]: truncation (top 10) + elitism ⇒ diversity collapses in ~5
  generations; Hamming cliff $-1.9 \to -2.0$ needs 3 bit flips (one re-run stalled 75
  generations).
- [[particle-swarm-py]]: exact 1995 rule, no inertia/clamp ⇒ $g_{best}$ freezes ~iteration 20 and
  velocities reach $10^6$–$10^8$; one random factor per particle instead of per dimension.
- [[ant-colony-py]]: ant-cycle AS, $\beta = 1$ (Dorigo: 5), $m = 4n$, $\tau_0 = 1/(nL_{nn})$
  swamped by the first deposit; 8–19% better than nearest neighbour.
- Class exercise code [[simulated-annealing-py]]: cooling 0.8 per iteration ⇒ hill climbing after
  ~50 of 100,000 iterations; $T$ freezes at $10^{-323}$ (overflow warnings), still finds Rastrigin's
  global basin in 2-D.
- Class exercise code [[gradient-descent-py]]: error × 0.8 per step; $10^{-6}$ accuracy at
  iteration 65; float floor at 161.

## Practice questions

> [!question]- Q1. Name and define the four landscape features that defeat hill climbing.
> **Answer.** Local maximum (better than neighbours, not global), plateau/flat local maximum (no
> uphill exit), shoulder (flat with an uphill exit), ridge (sequence of unconnected local maxima)
> ([[russell-norvig-aima]] §4.1.1).

> [!question]- Q2. SA, minimising: current cost 5, neighbour cost 5.5, $T = 1$. Accept with what probability? And if the neighbour costs 4?
> **Answer.** $\Delta = 0.5$, $P = e^{-0.5} \approx 0.607$. Cost 4 ⇒ $\Delta < 0$ ⇒ accepted with
> probability 1.

> [!question]- Q3. One-point crossover after bit 3 of P1 = `11010110`, P2 = `00111001`. Then two-point crossover with cuts after bits 2 and 5.
> **Answer.** One-point: C1 = `110` + `11001` = `11011001`; C2 = `001` + `10110` = `00110110`.
> Two-point: swap the middle segment (bits 3–5): C1 = `11` `111` `110` = `11111110`; C2 = `00`
> `010` `001` = `00010001`.

> [!question]- Q4. Decode `01010101 11111111` with Raymond's sign + 7-bit/10 encoding and give $f = (x+2)^2+(y-2)^2+10$.
> **Answer.** $x$: sign 0, `1010101` = 85 → $8.5$. $y$: sign 1, `1111111` = 127 → $-12.7$. $f =
> 10.5^2 + 14.7^2 + 10 = 110.25 + 216.09 + 10 = 336.34$ — the worst corner region of the range.

> [!question]- Q5. A population has costs (to minimise) 2, 4, 4, 10. Convert to fitness $1/(1+c)$ and give roulette probabilities.
> **Answer.** Fitness $= 1/3, 1/5, 1/5, 1/11 \approx 0.333, 0.2, 0.2, 0.091$; sum $\approx 0.824$.
> Probabilities $\approx 0.40, 0.24, 0.24, 0.11$.

> [!question]- Q6. Schema $H$ = `1***0*` in 6-bit strings, $p_c = 0.8$, $p_m = 0.05$, $f(H)/\langle f\rangle = 1.2$, $m(H,t) = 0.2$. Lower-bound $m(H, t+1)$.
> **Answer.** $o = 2$, $d = 5 - 1 = 4$, $l - 1 = 5$. Crossover factor $1 - 0.8 \cdot 4/5 = 0.36$;
> mutation factor $1 - 0.05 \cdot 2 = 0.9$. $m \ge 0.2 \cdot 1.2 \cdot 0.36 \cdot 0.9 \approx 0.078$ —
> a long schema shrinks despite above-average fitness.

> [!question]- Q7. 2-D PSO with inertia: $x = (1,1)$, $v = (0.5, -0.5)$, $p_{best} = (2,1)$, $g_{best} = (0,3)$, $w = 0.5$, $c_1 = c_2 = 2$, $r_1 = (0.5, 0.5)$, $r_2 = (0.25, 0.5)$. New $v$ and $x$?
> **Answer.** $wv = (0.25, -0.25)$; cognitive $2(0.5,0.5)\odot(1, 0) = (1, 0)$; social
> $2(0.25, 0.5)\odot(-1, 2) = (-0.5, 2)$. $v' = (0.75, 1.75)$; $x' = (1.75, 2.75)$.

> [!question]- Q8. ACO with $\alpha = 2, \beta = 1$: $\tau = (1, 2, 1)$, $d = (2, 4, 1)$ to cities A, B, C. Probabilities?
> **Answer.** $\eta = (0.5, 0.25, 1)$; $\tau^2\eta = (0.5, 1, 1)$, sum 2.5 ⇒ $p = (0.2, 0.4, 0.4)$.
> Raising $\alpha$ moved probability toward the high-pheromone edge B (compare 0.25 with
> $\alpha = 1$, [[ant-colony-optimization]] Q1).

> [!question]- Q9. Edge with $\tau = 6$, persistence $\rho = 0.5$, $Q = 100$; three ants used it with tour lengths 50, 50, 100. New $\tau$?
> **Answer.** $0.5 \cdot 6 + 2 + 2 + 1 = 8$.

> [!question]- Q10. ABC: $x_i = (4, -1)$, $x_k = (2, 3)$, $j = 1$, $\phi = 0.5$. Candidate? If its cost is better, what happens to trial$_i$?
> **Answer.** $v_{i1} = 4 + 0.5(4 - 2) = 5$, so $v_i = (5, -1)$. If better, it replaces $x_i$ and
> trial$_i$ resets to 0; otherwise trial$_i$ increases by 1 (general knowledge).

> [!question]- Q11. Which bees explore and which exploit? What are ABC's three control parameters?
> **Answer.** Employed and onlooker bees exploit; scouts explore. Parameters: number of food
> sources (= employed = onlookers), limit, MCN ([[slides-04-optimization]], slides 17–18).

> [!question]- Q12. Why did Dorigo find ant-cycle better than ant-density and ant-quantity, and which parameter values were best?
> **Answer.** Ant-cycle deposits $Q/L_k$ after the tour, using global information about solution
> quality; the others deposit during the walk using only local information. Best:
> $\alpha = 1, \beta = 5, \rho = 0.5, Q = 100$ ([[dorigo-1996-ant-system]] §IV).

> [!question]- Q13. Gradient descent on $f = (x-2)^2 + (y+2)^2$ from $(0,0)$ with $\eta = 0.25$: first two iterates? What is the error factor?
> **Answer.** Factor $1 - 2(0.25) = 0.5$. $w_1 = (0,0) - 0.25(-4, 4) = (1, -1)$; $w_2 = (1,-1) -
> 0.25(-2, 2) = (1.5, -1.5)$. Error halves each step.

> [!question]- Q14. Explain why Raymond's PSO stops improving after ~20 iterations while his GA reaches the exact optimum.
> **Answer.** PSO uses the 1995 rule without inertia damping or velocity limits, so the swarm's
> oscillations grow and particles fly away from $g_{best}$ ([[particle-swarm-py]]). The GA works on
> a 0.1 grid that contains $(-2, 2)$ exactly and, with elitism, keeps it once found
> ([[genetic-algorithm-py]]); PSO's continuous answer can only approach 10.

## Weak spots

(To be filled during exam prep.)
