---
type: comparison
summary: Side-by-side of minimax, alpha-beta, heuristic alpha-beta (H-MINIMAX with cutoff + EVAL) and Monte Carlo tree search — optimality, cost, what each needs, and when to use it.
unit: 4
tags: [games, minimax, alpha-beta, mcts, evaluation-function, comparison]
sources: ["[[russell-norvig-aima]]", "[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# Game search algorithms compared

Four ways to choose a move in a deterministic two-player zero-sum game ([[adversarial-search]]). The first two are exact; the last two trade exactness for speed. $b$ = branching factor, $m$ = maximum depth, $d$ = cutoff depth.

## Main table

| | [[minimax]] | [[alpha-beta-pruning]] | Heuristic alpha-beta (H-MINIMAX) | [[monte-carlo-tree-search]] |
|---|---|---|---|---|
| Idea | back up exact utilities through the whole tree | minimax + prune branches outside $(\alpha, \beta)$ | alpha-beta to a cutoff depth, then EVAL | average outcome of many playouts; grow tree selectively |
| Value returned | exact minimax value | exact minimax value (same move) | estimate | estimate (win rate) |
| Optimal? | yes (vs optimal opponent) | yes | no — only as good as EVAL | converges with enough playouts (UCT), not in finite time |
| Time | $O(b^m)$ | $O(b^{m/2})$ best, $\approx O(b^{3m/4})$ random, $O(b^m)$ worst | $O(b^d)$ … $O(b^{d/2})$ | linear per playout × number of playouts |
| Space | $O(bm)$ | $O(bm)$ | $O(bd)$ (+ transposition table) | size of the stored tree |
| Needs | UTILITY | UTILITY + good move ordering | EVAL, cutoff test (quiescence) | rules + playout policy (+ selection policy, e.g. UCB1) |
| Anytime? | no | no | with iterative deepening | yes |
| Shannon type | — | — | Type A (wide, shallow) | Type B (narrow, deep) |
| Known in practice | tic-tac-toe 3×3 | small games | Deep Blue, Stockfish, [[tic-tac-toe-4x4-py]] | AlphaGo/AlphaZero, KataGo |

(Sources: [[slides-02-problem-solving]], slides 18 and 20; [[russell-norvig-aima]] §6.2.1, §6.2.3-6.2.4, §6.3, §6.4.)

## Same budget, different depth

R&N's example: $b = 32$, 100-ply games, $10^9$ states per move → minimax searches **6 ply**, alpha-beta with perfect ordering **12 ply**, MCTS runs **10 million playouts** ([[russell-norvig-aima]] §6.4). Chess with ~$10^6$ nodes/s: minimax ≈ 5 ply per minute (beaten by an average human), alpha-beta + transposition table ≈ 14 ply (expert), Stockfish 30+ ply ([[russell-norvig-aima]] §6.3.3).

Measured in [[tic-tac-toe-4x4-py]] (first AI move, depth 5): plain minimax 396,076 nodes vs alpha-beta 6,923 (re-run 2026-10-01).

## Strengths and weaknesses

| Algorithm | Main strength | Main weakness |
|---|---|---|
| Minimax | simple, exact, basis for analysis | exponential; infeasible beyond toy games |
| Alpha-beta | exact with up to twice the depth | depends on move ordering; still exponential |
| Heuristic alpha-beta | practical, strong when EVAL is good | horizon effect, needs quiescence; one bad EVAL value can mislead it |
| MCTS | no EVAL needed; robust aggregate; anytime | may miss a single sharp move; slow to confirm "obvious" wins |

([[russell-norvig-aima]] §6.3.2, §6.4.)

## When to use which

- **Tiny game tree** (3×3 tic-tac-toe, < 9! leaves): full minimax or alpha-beta, no evaluation needed.
- **Medium/large tree, low $b$, good evaluation** (chess, checkers, 4×4 tic-tac-toe): heuristic alpha-beta + move ordering + iterative deepening + transposition table.
- **High $b$ or no good evaluation** (Go, new games, general game playing): MCTS, ideally with learned policy/value networks ([[chess-vs-go]]).
- **Chance elements** (backgammon): expectiminimax with chance nodes (R&N §6.5) — not compared here.

## Related

[[adversarial-search]] · [[minimax]] · [[alpha-beta-pruning]] · [[monte-carlo-tree-search]] · [[chess-vs-go]] · [[tic-tac-toe-4x4-py]] · [[search-algorithms-comparison]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Which of the four algorithms always return the same move? Which can be wrong?
> **Answer.** Minimax and alpha-beta return the same (exact) decision. Heuristic alpha-beta can be wrong when EVAL misjudges the cutoff positions; MCTS can be wrong when the playouts have not sampled the crucial line.

> [!question]- Q2. With a budget of $10^9$ nodes and $b = 32$, how deep do minimax and perfect-ordering alpha-beta search?
> **Answer.** $32^6 \approx 1.07 \times 10^9$ → minimax ≈ 6 ply; alpha-beta ≈ $b^{d/2}$ → $32^{6} = 32^{12/2}$ → ≈ 12 ply ([[russell-norvig-aima]] §6.4).

> [!question]- Q3. What does heuristic alpha-beta need that plain alpha-beta does not?
> **Answer.** A cutoff test (depth limit, ideally only at quiescent positions) and an evaluation function EVAL that equals UTILITY on terminal states and lies between loss and win otherwise ([[russell-norvig-aima]] §6.3).

> [!question]- Q4. Why is MCTS called "anytime" and alpha-beta not?
> **Answer.** MCTS improves its estimates every iteration and can return the most-visited move whenever it is stopped. Plain alpha-beta only has a reliable answer when the full search to its depth finishes; iterative deepening makes it anytime by keeping the move of the last completed depth.

> [!question]- Q5. Map each algorithm to Shannon's Type A / Type B.
> **Answer.** Heuristic alpha-beta (all moves to a fixed depth, then evaluate) is Type A; MCTS and forward pruning (follow promising lines deep, ignore bad-looking moves) are Type B ([[russell-norvig-aima]] §6.2.4, §6.3.3).
