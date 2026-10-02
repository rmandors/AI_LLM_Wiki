---
type: code
summary: Walkthrough of the class exercise code gd_functions.py — gradient descent with η=0.1 on f=(x−2)²+(y+2)², which converges geometrically (error ×0.8 per step) to (2,−2) and hits a floating-point floor at iteration 161.
unit: 9
tags: [gradient-descent, code, class-exercise]
sources: ["[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# `gd_functions.py` — gradient descent class exercise code

**File:** `raw/Class_exercises/gd_functions.py` (41 lines, NumPy, Spanish comments/docstrings).
Probably instructor-provided class exercise code (same style as [[simulated-annealing-py]]).

**Problem.** Minimise $f(x, y) = (x-2)^2 + (y+2)^2$ (minimum 0 at $(2, -2)$) with
[[gradient-descent]] from $(0, 0)$.

## Design decisions

| Choice | Value |
|---|---|
| Gradient | analytic: $\nabla f = (2(x-2),\; 2(y+2))$ |
| Learning rate | $\eta = 0.1$ (fixed) |
| Iterations | 1,000 (fixed; no tolerance test) |
| Start | $w_0 = (0, 0)$, $f(w_0) = 8$ |
| Output | prints every iteration |

## Walkthrough

- **L4–9 `objective(w)`** — $f(x,y)$.
- **L12–20 `grad_f(w)`** — returns `[2(x-2), 2(y+2)]`.
- **L23–25** parameters: `eta = 0.1`, `num_iterations = 1000`, `w = [0, 0]`.
- **L30–39** loop: `g = grad_f(w)`; `w = w - eta * g`; print.
- **L41–42** final point and value.

## Results

**Worked analysis.** Let $e_t = w_t - w^*$ with $w^* = (2, -2)$. Since $\nabla f(w) = 2e$,
$$e_{t+1} = e_t - 0.1 \cdot 2 e_t = 0.8\,e_t \;\Rightarrow\; e_t = 0.8^t \cdot (-2,\, 2), \qquad f(w_t) = \|e_t\|^2 = 8 \cdot 0.64^t.$$

| $t$ | $w_t$ | $f(w_t)$ (formula) | program output |
|---|---|---|---|
| 0 | $(0, 0)$ | 8 | 8.0 |
| 1 | $(0.4, -0.4)$ | 5.12 | 5.120000000000001 |
| 2 | $(0.72, -0.72)$ | 3.2768 | 3.276799999999999 |
| 3 | $(0.976, -0.976)$ | 2.097152 | 2.097152 |
| 65 | $(1.999999, -1.999999)$ | $\approx 2.0 \times 10^{-12}$ | 2.017e-12 |

- Within $10^{-6}$ of the optimum per coordinate after **65 iterations** ($2 \cdot 0.8^t < 10^{-6}
  \iff t > 65$).
- From **iteration 161** on, $f$ is stuck at $3.94 \times 10^{-31}$: each coordinate is one unit in
  the last place (≈ $4.4\times10^{-16}$) away from $\pm 2$, and the update $0.1 \cdot 2e$ is too
  small to change a float near 2. The remaining ~840 iterations do nothing.
- The run is deterministic (no randomness), so these numbers are reproducible (re-run
  2026-10-01).

## Known issues / improvements

1. **Fixed iteration count** — stop when $\|\nabla f\| < \varepsilon$ or the change in $f$ is below a
   tolerance.
2. **Printing 1,000 lines** — print every $k$ iterations instead.
3. **Learning-rate choice** — on this function $\eta = 0.5$ reaches the minimum in one step and any
   $\eta \ge 1$ fails (factor $1 - 2\eta$); in general $\eta$ must be tuned or found by line search
   ([[russell-norvig-aima]] §4.2).
4. The function is convex and separable, so gradient descent is guaranteed to work here; it is a
   demonstration, not a hard test. Compare [[simulated-annealing-py]] on Rastrigin, where gradient
   descent would get stuck in the nearest basin.

## Related concepts

[[gradient-descent]], [[hill-climbing]], [[optimization-problems]], [[perceptron]],
[[simulated-annealing-py]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. Derive the gradient used in the code.
> **Answer.** $\partial f/\partial x = 2(x-2)$, $\partial f/\partial y = 2(y+2)$ — chain rule on each
> squared term.

> [!question]- Q2. Compute iteration 3 by hand.
> **Answer.** $w_2 = (0.72, -0.72)$, $\nabla f = (2(0.72-2), 2(-0.72+2)) = (-2.56, 2.56)$, so $w_3 =
> (0.72 + 0.256, -0.72 - 0.256) = (0.976, -0.976)$, $f = 2 \cdot 1.024^2 = 2.097152$.

> [!question]- Q3. By what factor does the error shrink each step, and what learning rate would be optimal?
> **Answer.** $1 - 2\eta = 0.8$. $\eta = 0.5$ makes the factor 0 — exact minimum in one step.

> [!question]- Q4. Why does $f$ stop decreasing at about $4 \times 10^{-31}$ instead of reaching 0?
> **Answer.** Floating-point resolution: near 2 the spacing of doubles is ≈ $4.4 \times 10^{-16}$;
> once the error is one such unit, the step $0.2e$ is smaller than half a unit and rounds away, so
> $w$ stops changing. $f = 2 \cdot (4.4\times10^{-16})^2 \approx 3.9 \times 10^{-31}$.

> [!question]- Q5. What would happen with $\eta = 1.1$?
> **Answer.** Factor $1 - 2.2 = -1.2$: the error flips sign and grows by 20% each step — divergence.
