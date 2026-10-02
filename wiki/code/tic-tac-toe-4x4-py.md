---
type: code
summary: Walkthrough of the class exercise tic-tac-toe.py — 4x4 tic-tac-toe where the AI (X, MAX) plays heuristic alpha-beta (H-MINIMAX) with a 7-ply cutoff, centre>corner>side move ordering and a 1/3/9 line-weight evaluation.
unit: 4
tags: [games, minimax, alpha-beta, evaluation-function, python, class-exercise]
sources: ["[[russell-norvig-aima]]", "[[slides-02-problem-solving]]"]
updated: 2026-10-01
---

# Class exercise — 4×4 tic-tac-toe with H-MINIMAX + alpha-beta (`tic-tac-toe.py`)

**File**: `raw/Class_exercises/tic-tac-toe.py` (214 lines, Spanish identifiers and comments).

**Problem**: a human (O) plays 4×4 tic-tac-toe against the computer (X). Four in a row, column or main diagonal wins; a full board with no winner is a draw. The AI is **MAX** (+1 = X wins) and chooses its move with **heuristic minimax with alpha-beta pruning** and a depth cutoff — R&N's H-MINIMAX / heuristic alpha-beta tree search ([[russell-norvig-aima]] §6.2.3, §6.3; [[minimax]], [[alpha-beta-pruning]]). The human moves first.

Glossary: *tablero* = board, *casilla* = cell, *ganador* = winner, *lleno* = full, *jugada/movimiento* = move, *turno* = turn, *profundidad* = depth, *mejor valor* = best value, *empate* = draw.

## Design decisions

| Decision | Effect |
|---|---|
| Board = flat list of 16 chars `' '`, `'X'`, `'O'` | Index `i` = row `i // 4`, column `i % 4`; the human types 1-16. |
| 10 winning lines hard-coded (`combinaciones`) | 4 rows, 4 columns, 2 diagonals; used by both the terminal test and the evaluation. |
| Utility ±1, draw 0 | Terminal values from X's (MAX's) point of view, as in R&N §6.1.1. |
| Alpha-beta inside minimax | Same move as minimax, far fewer nodes ([[alpha-beta-pruning]]). |
| Fixed depth cutoff `max_profundidad = 7` | Bounded thinking time; positions at depth 7 are scored by EVAL. |
| Move ordering centre (5, 6, 9, 10) > corners (0, 3, 12, 15) > sides | Tries likely-good moves first to increase pruning (R&N §6.2.4). |
| EVAL = weighted count of open lines (1/3/9 for 1/2/3 own marks), divided by 90, clamped to [−1, 1] | A weighted linear evaluation function in the sense of R&N §6.3.1. |
| Board modified in place and undone (`tablero[move] = ' '`) | No copying; same "do/undo" style as CSP backtracking. |

## Walkthrough

- **l.1-5 `combinaciones`** — the 10 lines (rows, columns, diagonals `(0,5,10,15)` and `(3,6,9,12)`).
- **l.7-20 `mostrar_tablero`** — prints the 4×4 grid.
- **l.23-31 `hay_ganador`** — returns `'X'`/`'O'` if all four cells of some line match and are not empty, else `None`.
- **l.34-38 `tablero_lleno`** — `' ' not in tablero`.
- **l.41-52 `evaluar`** — utility of terminal positions: +1 X wins, −1 O wins, 0 otherwise.
- **l.55-65 `movimientos_disponibles`** — legal moves (empty cells) in the fixed preferred order (l.60-64).
- **l.68-134 `h_minimax(tablero, es_turno_de_X, alpha, beta, profundidad, max_profundidad)`** — returns `(value, move)`:
  - l.79-85 terminal test first: X win → (1, None), O win → (−1, None), full board → (0, None);
  - l.87-88 cutoff test → `(eval_heuristica(tablero), None)`;
  - l.93-113 **MAX (X)**: for each move, place X (l.99), recurse with `False` and depth + 1 (l.100), undo (l.101). Inside `if valor > mejor_valor` (l.104-111): store best value and move, `alpha = max(alpha, mejor_valor)` (l.109), and `break` if `mejor_valor >= beta` (l.110-111);
  - l.115-134 **MIN (O)**: symmetric with `valor < mejor_valor`, `beta = min(beta, mejor_valor)` (l.130), `break` if `mejor_valor <= alpha` (l.131-132).
- **l.137-141 `is_cutoff`** — `profundidad >= max_profundidad`.
- **l.144-163 `eval_heuristica`** — for each line: if only X marks, add `weights[x_count]`; if only O marks, subtract `weights[o_count]`; mixed lines are dead and count 0 (l.152-160). Weights `{1: 1, 2: 3, 3: 9}` (l.150). Return `max(-1, min(1, score / 90))` (l.163); 90 = 10 lines × 9, the largest possible raw score.
- **l.166-210 `jugar`** — game loop: show board, check for end (l.180-189); human turn reads 1-16 with `try/except` and rejects occupied cells (l.191-204); AI turn calls `h_minimax(tablero, True, max_profundidad=7)` (l.208) and plays the returned move.
- **l.213-214** — `if __name__ == "__main__": jugar`.

**Is the alpha/beta update inside the `if valor > mejor_valor` block correct?** Yes. Within a MAX node β never changes; if `valor` does not improve `mejor_valor`, then `max(alpha, mejor_valor)` is unchanged and `mejor_valor >= beta` was already false at the previous check. So updating/testing only on improvement is equivalent to R&N Fig. 6.7. The first child always enters the block (finite value > −∞). Same argument for MIN.

## Results

Re-run on 2026-10-01 by executing the source in memory and counting calls to `h_minimax` from the AI's first decision (human O has played one move; 15 empty cells). Plain minimax = the same code without pruning, written for comparison.

| Human's first move | Depth | Alpha-beta nodes | Plain minimax nodes | AI reply (index) | Root value |
|---|---|---|---|---|---|
| corner (cell 1) | 3 | 350 | 2,956 | 5 | 0.011 |
| corner (cell 1) | 5 | 6,923 | 396,076 | 5 | 0.011 |
| corner (cell 1) | 7 | 127,701 (≈0.24 s) | not run (≈ 15·14·…·9 ≈ $3.2\times10^7$ leaves) | 6 | 0.011 |
| centre (cell 6) | 7 | 139,793 (≈0.27 s) | — | 10 | 0.011 |
| side (cell 2) | 7 | 119,249 (≈0.24 s) | — | 6 | 0.022 |

- Alpha-beta at depth 5 visits ≈57× fewer nodes than plain minimax, with the same root value.
- The root values are tiny positive numbers (1/90, 2/90): at depth 7 from the opening the search sees no forced result, so the move is chosen by EVAL alone.
- **Quick-win test**: over 181 random legal positions where X had an immediate winning move, the AI chose a *different* move in **25** (≈14%) — e.g. board `..XO / OOX. /.XX. / O..O` (row-major, `.` = empty): column 2-6-10-14 wins at once at index 14, but the AI played index 8, which also leads to a forced win (value +1) only later.

## Known issues / improvements

- **No preference for quicker wins (or slower losses).** Every forced win is +1 regardless of depth, and ties keep the first move in the ordering, so the AI may delay a win (14% of the test positions). It still wins if the forced win is real, but it looks odd and gives the human more chances against an imperfect horizon. Fix: return `+(1000 - profundidad)` / `-(1000 - profundidad)` for wins/losses (general knowledge).
- **EVAL can equal a real win.** The heuristic is clamped to **[−1, 1]**, the same as the terminal utilities, so a cutoff position scored +1 is indistinguishable from a proven win. R&N only require loss ≤ EVAL ≤ win, but keeping EVAL **strictly** inside (e.g. divide by 100, or scale utilities to ±1000) is safer. In practice the scores are small (even a probe board with five X on cells 0, 1, 2, 4, 8 and no O scores only 0.256), but nothing in the code guarantees it.
- **Docstring mismatch**: `h_minimax` says the value is (+1, 0, −1) (l.72), but with the cutoff it returns fractions.
- **What depth 7 means on a 16-cell board.** On its first decision the AI looks 7 plies ahead out of the 15 remaining, so early moves are heuristic, not optimal. Depth 7 is also the *minimum* depth at which X's own four-in-a-row can appear from that first move (X moves at plies 1, 3, 5, 7), and O's at ply 6. Before X's $k$-th move there are $17 - 2k$ empty cells, so from the AI's **5th** move on (≤ 7 empty cells) the search reaches the end of the game and play is exact minimax.
- **EVAL ignores whose turn it is and double threats.** Three X in an open line is worth 9 whether X or O is to move; forks (two open threes) are not rewarded specially.
- **Centre-first ordering is a convention, not "more lines".** On 4×4 both centre cells and corners lie on 3 lines (row, column, one diagonal), sides on 2. The ordering still helps pruning but its comment's rationale is weaker than on 3×3.
- **No transposition table or iterative deepening.** Many move orders reach the same position; caching values (R&N §6.2.4) would cut the ≈130k nodes substantially, and iterative deepening would allow a time limit instead of a fixed depth (R&N §6.3.2).
- **No quiescence check**: a position with an open three for the side to move is evaluated statically at the cutoff (horizon effect, R&N §6.3.2).
- Human always moves first as O; the AI (MAX) moves second — unlike R&N's convention that MAX moves first, harmless but worth noticing.
- The board display does not show cell numbers, so the human must count 1-16.

## Related concepts

[[minimax]] · [[alpha-beta-pruning]] · [[adversarial-search]] · [[game-search-comparison]] · [[heuristic-functions]] · [[iterative-deepening-search]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Why does the code check for a winner before the cutoff test?
> **Answer.** The cutoff test must return true for terminal states but the evaluation should not replace a real result: a won/lost/drawn position gets its exact utility (±1/0) even at depth 7 (R&N §6.3.2: EVAL = UTILITY on terminal states). Otherwise a win at the horizon would only be "estimated".

> [!question]- Q2. α and β are updated only when the best value improves. Is that a bug?
> **Answer.** No. If the best value did not change, `max(alpha, mejor_valor)` and the cutoff test would give the same result as at the previous iteration (β is fixed inside a MAX node, α inside a MIN node). The code is equivalent to R&N Fig. 6.7.

> [!question]- Q3. The AI sometimes does not take an immediate win. Why, and how do you fix it?
> **Answer.** All forced wins are worth +1, whatever their depth, and among equal values the first move in the ordering is kept (strict `>`). Make wins worth more the sooner they happen, e.g. `1000 - profundidad`.

> [!question]- Q4. Explain the evaluation function and its normalisation.
> **Answer.** For each of the 10 lines, if only X has marks there add 1, 3 or 9 for 1, 2, 3 marks; if only O, subtract; mixed lines are dead (0). The maximum raw score is 10 × 9 = 90, so dividing by 90 maps it into [−1, 1].

> [!question]- Q5. Why order moves centre → corners → sides?
> **Answer.** Alpha-beta prunes more when good moves come first (best case $O(b^{m/2})$). Central cells take part in many lines, so they are usually strong; on 4×4 the corners are on as many lines as the centre, so it is a heuristic choice.

> [!question]- Q6. How many nodes does the first AI move examine at depth 7, and how many would plain minimax examine?
> **Answer.** About 120k-140k nodes (≈0.25 s) with alpha-beta. Plain minimax at depth 5 already needs 396,076 nodes (vs 6,923); at depth 7 it would be on the order of $15 \cdot 14 \cdots 9 \approx 3.2 \times 10^7$ leaves (re-run 2026-10-01).

> [!question]- Q7. When does the AI start playing perfectly?
> **Answer.** When at most 7 cells are empty at its turn, i.e. from its 5th move: the 7-ply search then reaches the end of the game and the cutoff never fires.
