---
type: code
summary: Walkthrough of the class exercise code sa_functions.py — simulated annealing on 2-D Rastrigin whose 0.8-per-iteration cooling makes it a hill climber after ~50 of 100,000 iterations, yet still lands in the global basin.
unit: 9
tags: [simulated-annealing, code, class-exercise]
sources: ["[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# `sa_functions.py` — simulated annealing class exercise code

**File:** `raw/Class_exercises/sa_functions.py` (65 lines, NumPy + Matplotlib, Spanish comments).
Probably instructor-provided class exercise code rather than Raymond's own (no name, Spanish
comments, same style as [[gradient-descent-py]]).

**Problem.** Minimise the 2-D **Rastrigin** function
$f(x) = 10n + \sum_i (x_i^2 - 10\cos 2\pi x_i)$ on $[-5.12, 5.12]^2$ (global minimum 0 at the
origin, many local minima near integer points — general knowledge) with
[[simulated-annealing]].

## Design decisions

| Choice | Value |
|---|---|
| Start | uniform random in bounds |
| Neighbour | current + $U(-1, 1)$ per coordinate, clipped to bounds |
| Acceptance | always if $\Delta < 0$, else with probability $e^{-\Delta/T}$, $\Delta = f(\text{new}) - f(\text{cur})$ |
| Schedule | $T_0 = 100$, geometric $T \leftarrow 0.8\,T$ after **every** iteration |
| Iterations | 100,000 |
| Best-so-far | tracked separately, updated only on accepted moves |
| Recorded history | `values` = current value per iteration (not the best) |

## Walkthrough

- **L4–37 `simulated_annealing(func, bounds, max_iter, initial_temp, cooling_rate)`**
  - L6–11 random start, best = start, $T = T_0$.
  - L13–18 propose `new = current + U(-1,1)`, clip, evaluate.
  - L21 `delta = new_value - current_value` (minimisation).
  - L24 `if delta < 0 or rand < exp(-delta / temperature)` — the Metropolis rule. Note that
    $\Delta = 0$ is accepted too ($e^0 = 1$).
  - L29–31 update best (inside the acceptance branch, which is enough because an improving move is
    always accepted).
  - L34 `temperature *= cooling_rate`.
- **L40–42 `objective_function`** — Rastrigin.
- **L44–47 `objective_f2`** — Ackley function, **defined but never used**.
- **L50–56** parameters and the run on Rastrigin; **L58–66** print and plot.

**Sign convention.** The code's rule is the minimisation form. R&N's Global-Edition Fig. 4.5
writes $\Delta E = \text{VALUE(current)} - \text{VALUE(next)}$, accepts if $\Delta E > 0$, else with
$e^{\Delta E/T}$ — with VALUE read as a cost that is exactly $-\Delta$, so the two rules are
identical. In the maximisation form ($\Delta E = v(\text{next}) - v(\text{current})$) it is also
the same rule. In every case worse moves are accepted with $e^{-|\text{worsening}|/T}$
([[russell-norvig-aima]] §4.1.2; see the table on [[simulated-annealing]]).

## Results

**Temperature schedule (computed):** $T_k = 100 \cdot 0.8^k$.
- $T \approx 10.7$ after 10 iterations, $1.15$ after 20, $0.12$ after 30, **below $10^{-3}$ after
  52**, $2 \times 10^{-8}$ after 100.
- Floating point: $T$ does **not** reach 0. It sinks into subnormal numbers and from iteration
  3,354 on stays at $\approx 10^{-323}$, because $0.8 \times 10^{-323}$ rounds back to the same
  subnormal value. From then on `-delta / temperature` overflows to $-\infty$ for any worsening
  move, `exp` returns 0, and Python prints **"RuntimeWarning: overflow encountered in scalar
  divide"** (about 96,800 occurrences per run if all warnings are shown; by default it is printed
  once). There is no division by zero.

**Runs (2026-10-01, seeds 0–4, unmodified code):** best $f$ = 0.0028, 0.0008, 0.0021, 0.0039,
0.0001, all at points within 0.004 of the origin — **the global basin every time**.

**Why it still works.** After ~50 iterations the algorithm is a first-choice hill climber with
random steps up to ±1 per coordinate. Rastrigin's local minima are 1 apart, so a single proposal
can jump straight into a lower neighbouring basin, and 100,000 proposals in 2-D are plenty. The
"annealing" contributes almost nothing; the large step size and the huge budget do the work. On a
higher-dimensional Rastrigin this would not be enough.

## Known issues / improvements

1. **Cooling far too fast**: the exploratory phase is ~0.05% of the run. Use a factor like
   0.9999 per iteration (≈46,000 iterations from 100 to 1), or cool every $L$ iterations
   (general knowledge).
2. **No stopping rule on $T$** — R&N stop when $T = 0$ ([[russell-norvig-aima]] Fig. 4.5); here
   $T$ never reaches 0 numerically. Stop at a minimum temperature like $10^{-8}$.
3. **Overflow warnings** — guard with `if temperature > 1e-12` before the exponential.
4. **Fixed step size** — shrinking the step as $T$ falls would give finer final solutions (the
   best found is ~$10^{-3}$, not ~$10^{-10}$).
5. **`objective_f2` (Ackley) unused** — probably meant as a second experiment.
6. Plotted history is the *current* value, which is noisy in theory but flat here because $T$
   collapses immediately.

## Related concepts

[[simulated-annealing]], [[hill-climbing]], [[optimization-problems]],
[[exploration-vs-exploitation]], [[gradient-descent-py]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. At iteration 10 ($T \approx 10.74$) a proposal worsens $f$ by 2. Acceptance probability? And at iteration 30 ($T \approx 0.124$)?
> **Answer.** $e^{-2/10.74} = e^{-0.186} \approx 0.83$. $e^{-2/0.124} = e^{-16.1} \approx 10^{-7}$
> — effectively never.

> [!question]- Q2. Is this really simulated annealing?
> **Answer.** Only for the first ~50 of 100,000 iterations; after that $T < 10^{-3}$ and almost no
> worsening move is accepted, so it behaves like first-choice hill climbing with random steps.

> [!question]- Q3. Show the code's acceptance rule equals R&N's.
> **Answer.** Code: $\Delta = f_{new} - f_{cur}$, accept if $\Delta < 0$ else with $e^{-\Delta/T}$.
> R&N: $\Delta E = -\Delta$ (VALUE as cost), accept if $\Delta E > 0$ else with $e^{\Delta E/T} =
> e^{-\Delta/T}$. Same ([[russell-norvig-aima]] Fig. 4.5).

> [!question]- Q4. Why does the program print an overflow warning, and does $T$ ever become 0?
> **Answer.** $T$ shrinks to the subnormal $\approx 10^{-323}$ and stays there (rounding), so
> $-\Delta/T$ overflows to $-\infty$; `exp(-inf) = 0`, so the move is rejected. $T$ never becomes
> exactly 0.

> [!question]- Q5. Why does it still find the global minimum on 2-D Rastrigin?
> **Answer.** Steps of up to ±1 per coordinate can jump between adjacent basins (spaced 1 apart),
> and 100,000 random proposals in 2-D give many chances to land in a lower basin — random-step hill
> climbing with a big budget, not annealing.
