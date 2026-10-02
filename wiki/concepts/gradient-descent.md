---
type: concept
summary: Gradient descent minimises a differentiable function by repeatedly stepping against the gradient, w ← w − η∇f(w); the step size η controls speed and stability.
unit: 9
tags: [optimization, continuous, calculus, machine-learning]
sources: ["[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Gradient descent

**Gradient descent** is local search for continuous, differentiable objectives: at every step
it moves a small distance in the direction of steepest decrease, $-\nabla f$. It is the
continuous analogue of [[hill-climbing]] (gradient *ascent* climbs $+\nabla f$) and the
workhorse of machine learning (training the [[perceptron]] and neural networks in unit 10)
([[russell-norvig-aima]] §4.1, §4.2).

## How it works

$$w_{t+1} = w_t - \eta\, \nabla f(w_t)$$

where $\eta$ (R&N: $\alpha$, the **step size** or learning rate) is a small positive constant
([[russell-norvig-aima]] §4.2 writes the ascent form $x \leftarrow x + \alpha \nabla f(x)$).

```text
w ← initial point
repeat N times (or until ‖∇f(w)‖ < ε):
    g ← ∇f(w)
    w ← w − η · g
return w
```

If no analytic gradient exists, use an **empirical gradient** (finite differences); that is
steepest-ascent hill climbing on a discretised space ([[russell-norvig-aima]] §4.2).
**Newton–Raphson** uses second derivatives: $x \leftarrow x - H_f^{-1}(x)\nabla f(x)$, which
jumps straight to the minimum of a quadratic ([[russell-norvig-aima]] §4.2).

**Exact behaviour on a quadratic bowl.** For $f(w) = \|w - w^*\|^2$, $\nabla f = 2(w - w^*)$,
so
$$w_{t+1} - w^* = (1 - 2\eta)(w_t - w^*) \;\Rightarrow\; w_t - w^* = (1-2\eta)^t (w_0 - w^*).$$
The error shrinks geometrically when $|1 - 2\eta| < 1$, i.e. $0 < \eta < 1$; $\eta = 0.5$
lands on $w^*$ in one step; $\eta > 1$ diverges (general knowledge, derived here).

## Properties

- **Converges to a stationary point** ($\nabla f = 0$): a minimum on convex functions, but
  possibly a local minimum or saddle point otherwise. Not global on multimodal functions like
  Rastrigin.
- **Step size**: too small → many steps; too large → overshoot or divergence. **Line search**
  doubles $\alpha$ until $f$ starts getting worse ([[russell-norvig-aima]] §4.2).
- **Cost per step**: one gradient evaluation, $O(n)$ for $n$ variables (vs $O(n^2)$ Hessian
  entries plus inversion for Newton's method).
- Deterministic: same start ⇒ same result. Random restarts or [[simulated-annealing]] help on
  multimodal landscapes ([[russell-norvig-aima]] §4.2).

## In this course

- The optimization slides do not cover gradient descent directly ([[slides-04-optimization]]);
  it comes from R&N §4.2 and the class exercise code [[gradient-descent-py]], which minimises
  $f(x,y) = (x-2)^2 + (y+2)^2$ from $(0,0)$ with $\eta = 0.1$ for 1,000 iterations.
- Worked numbers from that code: error factor $1 - 2(0.1) = 0.8$ per step;
  $f_t = 8 \cdot 0.64^t$; after 1 step $w = (0.4, -0.4)$, $f = 5.12$; after 65 steps the
  coordinates are within $10^{-6}$ of $(2,-2)$; from iteration 161 on, $f$ is stuck at
  $\approx 3.9\times 10^{-31}$ (floating-point floor). See [[gradient-descent-py]].
- PSO was compared against backpropagation (a gradient method) for neural-network training in
  [[kennedy-eberhart-1995-pso]] §5.

## Common mistakes

- Sign errors: descent subtracts the gradient; ascent adds it.
- Assuming a bigger learning rate is always faster — past $\eta = 1/L$-type thresholds (here
  $\eta > 1$) it diverges.
- Running a fixed huge number of iterations instead of a tolerance test (1,000 iterations in
  [[gradient-descent-py]] where ~65 suffice for $10^{-6}$ accuracy).
- Expecting gradient descent to escape local minima: it cannot without added randomness.

## Related

[[hill-climbing]], [[optimization-problems]], [[simulated-annealing]], [[perceptron]],
[[particle-swarm-optimization]], [[metaheuristics-comparison]], [[gradient-descent-py]].

## Practice questions

> [!question]- Q1. Write the gradient-descent update and explain each symbol.
> **Answer.** $w_{t+1} = w_t - \eta \nabla f(w_t)$: $w_t$ current point, $\nabla f$ vector of
> partial derivatives (direction of steepest increase), $\eta > 0$ step size; the minus sign
> moves downhill ([[russell-norvig-aima]] §4.2).

> [!question]- Q2. For $f(x,y) = (x-2)^2 + (y+2)^2$, $\eta = 0.1$, start $(0,0)$: compute the first two iterates and $f$ after each.
> **Answer.** $\nabla f = (2(x-2), 2(y+2))$. At $(0,0)$: $\nabla f = (-4, 4)$, so $w_1 = (0,0) -
> 0.1(-4,4) = (0.4, -0.4)$, $f = 1.6^2 + 1.6^2 = 5.12$. At $w_1$: $\nabla f = (-3.2, 3.2)$, so
> $w_2 = (0.72, -0.72)$, $f = 1.28^2 \cdot 2 = 3.2768$. Each step multiplies the error by 0.8 and
> $f$ by 0.64 — matches the program's output ([[gradient-descent-py]]).

> [!question]- Q3. On the same function, for which $\eta$ does gradient descent converge, and which $\eta$ is best?
> **Answer.** Error factor $1 - 2\eta$; converges iff $|1-2\eta| < 1 \iff 0 < \eta < 1$.
> $\eta = 0.5$ gives factor 0 — the exact minimum in one step. $\eta = 1$ oscillates between two
> points forever; $\eta > 1$ diverges.

> [!question]- Q4. How many iterations does the class code need to get within $10^{-6}$ of the optimum in each coordinate?
> **Answer.** Need $2 \cdot 0.8^t < 10^{-6} \Rightarrow t > \ln(5\times10^{-7})/\ln 0.8 \approx 65$.
> The program's output confirms coordinates $1.999999$ at iteration 65 ([[gradient-descent-py]]).

> [!question]- Q5. Why does R&N say empirical-gradient search is "the same as steepest-ascent hill climbing in a discretized version of the state space"?
> **Answer.** Without an analytic gradient you probe nearby points ($\pm\delta$ in each
> variable), which is exactly evaluating a discretised neighbourhood and moving to the best
> neighbour ([[russell-norvig-aima]] §4.2).
