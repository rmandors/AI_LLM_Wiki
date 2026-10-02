---
type: concept
summary: Minimax computes the optimal move in a two-player zero-sum game by backing up utilities (MAX takes the maximum, MIN the minimum); H-MINIMAX cuts it off at a depth and uses an evaluation function.
unit: 4
tags: [games, minimax, adversarial-search, evaluation-function]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Minimax

**Minimax** is the algorithm that finds the optimal move in a deterministic two-player zero-sum game, assuming both players play optimally. MAX tries to maximise the value of the final state, MIN tries to minimise the same value; the **minimax value** of a node is the utility (for MAX) of reaching that node if both sides play perfectly from there on ([[slides-02-problem-solving]], slide 18; [[russell-norvig-aima]] §6.2).

## How it works

Recursive definition ([[russell-norvig-aima]] §6.2; [[slides-02-problem-solving]], slide 18):

$$
\text{MINIMAX}(s)=
\begin{cases}
\text{UTILITY}(s,\text{MAX}) & \text{if IS-TERMINAL}(s)\\
\max_{a\in\text{Actions}(s)} \text{MINIMAX}(\text{RESULT}(s,a)) & \text{if TO-MOVE}(s)=\text{MAX}\\
\min_{a\in\text{Actions}(s)} \text{MINIMAX}(\text{RESULT}(s,a)) & \text{if TO-MOVE}(s)=\text{MIN}
\end{cases}
$$

Algorithm (R&N Fig. 6.3, paraphrased):

```text
MINIMAX-SEARCH(game, state): v, move = MAX-VALUE(state); return move
MAX-VALUE(s): if terminal: return UTILITY(s), null
              v = -inf
              for a in ACTIONS(s):
                  v2 = MIN-VALUE(RESULT(s,a))
                  if v2 > v: v, move = v2, a
              return v, move
MIN-VALUE(s): symmetric, v = +inf, keep the smallest
```

It is a **complete depth-first exploration** of the game tree; values are "backed up" as the recursion unwinds ([[russell-norvig-aima]] §6.2.1).

**Worked example (R&N Fig. 6.2).** MAX root with three MIN children B, C, D; leaves B = (3, 12, 8), C = (2, 4, 6), D = (14, 5, 2). MIN values: B = 3, C = 2, D = 2. Root = max(3, 2, 2) = **3**; the minimax decision is the move to B ($a_1$) ([[russell-norvig-aima]] §6.2).

### H-MINIMAX

Real games are too deep to search to the end. **Heuristic minimax** replaces the terminal test with a **cutoff test** and the utility with an **evaluation function** EVAL ([[russell-norvig-aima]] §6.3):

$$
\text{H-MINIMAX}(s,d)=
\begin{cases}
\text{EVAL}(s,\text{MAX}) & \text{if IS-CUTOFF}(s,d)\\
\max_a \text{H-MINIMAX}(\text{RESULT}(s,a),d+1) & \text{if MAX to move}\\
\min_a \text{H-MINIMAX}(\text{RESULT}(s,a),d+1) & \text{if MIN to move}
\end{cases}
$$

- EVAL must equal UTILITY on terminal states and satisfy $\text{UTILITY(loss)} \le \text{EVAL}(s) \le \text{UTILITY(win)}$ otherwise; it must be fast and strongly correlated with the chance of winning ([[russell-norvig-aima]] §6.3.1).
- Typical form: a **weighted linear function** $\text{EVAL}(s) = \sum_i w_i f_i(s)$ (e.g. chess material: pawn 1, knight/bishop 3, rook 5, queen 9) ([[russell-norvig-aima]] §6.3.1).
- Cutoff policies: fixed depth limit, or better **iterative deepening** (return the move of the deepest completed search when time runs out) ([[russell-norvig-aima]] §6.3.2; [[iterative-deepening-search]]).
- Pitfalls: evaluate only **quiescent** positions (quiescence search), and beware the **horizon effect** — delaying an unavoidable loss beyond the depth limit; singular extensions help ([[russell-norvig-aima]] §6.3.2).

## Properties

| Property | Value |
|---|---|
| Complete? | Yes, if the tree is finite ([[russell-norvig-aima]] §6.2.1) |
| Optimal? | Yes, against an optimal opponent; against a suboptimal one it does at least as well ([[russell-norvig-aima]] §6.2) |
| Time | $O(b^m)$ |
| Space | $O(bm)$ generating all actions at once, $O(m)$ generating one at a time |

($b$ = legal moves per position, $m$ = maximum depth; [[slides-02-problem-solving]], slide 18; [[russell-norvig-aima]] §6.2.1.) For chess, $35^{80} \approx 10^{123}$ is infeasible, so minimax is mainly a basis for analysis and for practical approximations.

**Multiplayer extension**: each node holds a vector of utilities; the player to move picks the child best for *itself* ([[russell-norvig-aima]] §6.2.2).

## In this course

- Slide 18 of [[slides-02-problem-solving]] gives the definition, $O(b^m)$ time, $O(b\cdot m)$ space and "explores the complete tree down to terminal nodes". **Slide 19 is image-only** (no text extracted; presumably the example tree — not verified), so the worked example above comes from R&N Fig. 6.2.
- HW01 research question: "Minimax is the right idea for this type of game … But the full minimax tree is the huge game tree … so we cannot build it until the end of the game" ([[hw01-report]], Research Question). See [[chess-vs-go]].
- [[tic-tac-toe-4x4-py]] implements H-MINIMAX (named `h_minimax`) with a depth cutoff of 7 plies and a line-counting EVAL. Re-running it shows plain minimax at depth 5 visits 396,076 nodes from the first AI move, versus 6,923 with alpha-beta ([[tic-tac-toe-4x4-py]], Results).

## Common mistakes

- Treating minimax values as "who is ahead now" — they are values **under perfect play** to the end (or to the cutoff).
- Forgetting that the root of MINIMAX-SEARCH returns a **move**, not a value.
- Mixing up perspectives: utilities are always from MAX's point of view; MIN minimises the same number.
- Thinking an EVAL that is "between loss and win" is enough: it should be *strictly* inside if you want to tell a proven win from an estimate (see [[tic-tac-toe-4x4-py]], Known issues).
- Ignoring depth: plain minimax treats a win in 1 and a win in 7 as equal; prefer quicker wins with a depth-adjusted utility (general knowledge).

## Related

[[adversarial-search]] · [[alpha-beta-pruning]] · [[monte-carlo-tree-search]] · [[depth-first-search]] · [[iterative-deepening-search]] · [[heuristic-functions]] · [[game-search-comparison]] · [[tic-tac-toe-4x4-py]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Compute the minimax value of a MAX root whose three MIN children have leaves (5, 8, 7), (3, 9, 1), (6, 2, 10).
> **Answer.** MIN values: 5, 1, 2. Root = max(5, 1, 2) = **5**, so MAX moves to the first child.

> [!question]- Q2. Three-ply tree: MAX root → two MIN nodes → each has two MAX nodes → each has two leaves. Leaves: MIN₁: (3, 5), (6, 9); MIN₂: (1, 2), (0, −1). Minimax value?
> **Answer.** MAX level: 5, 9, 2, 0. MIN level: min(5, 9) = 5, min(2, 0) = 0. Root: max(5, 0) = **5**.

> [!question]- Q3. What are the time and space complexity of minimax and why is space so small?
> **Answer.** Time $O(b^m)$, space $O(bm)$ (or $O(m)$ if actions are generated one at a time) because it is depth-first: it only stores the current path and the siblings along it ([[russell-norvig-aima]] §6.2.1).

> [!question]- Q4. What two requirements must an evaluation function satisfy, and what makes it "good"?
> **Answer.** EVAL = UTILITY on terminal states, and loss ≤ EVAL ≤ win on the others. It is good if it is fast to compute and strongly correlated with the actual chance of winning ([[russell-norvig-aima]] §6.3.1).

> [!question]- Q5. What is the horizon effect? Give a remedy.
> **Answer.** A depth-limited search delays an unavoidable loss (e.g. by pawn sacrifices) until it falls beyond the depth limit and so wrongly thinks it was avoided. Remedies: singular extensions (extend clearly-best moves past the cutoff) and quiescence search ([[russell-norvig-aima]] §6.3.2).

> [!question]- Q6. If MIN plays suboptimally, is the minimax move still best for MAX?
> **Answer.** MAX will do *at least as well* as against an optimal MIN, but the minimax move is not always the best one: a risky move may win against a weak opponent with high probability ([[russell-norvig-aima]] §6.2).
