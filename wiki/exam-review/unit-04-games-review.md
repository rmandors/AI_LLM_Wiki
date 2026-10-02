---
type: exam-review
summary: Cheat sheet for unit 4, adversarial search — game formalism, minimax, alpha-beta and move ordering, H-MINIMAX with evaluation functions, MCTS/UCB1, chess vs Go facts, the 4x4 tic-tac-toe exercise, traps and 13 practice questions.
unit: 4
tags: [games, exam-review, minimax, alpha-beta, mcts, chess, go]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Unit 4 review — Adversarial search in games

Part of [[midterm-01-review]]. Slides: [[slides-02-problem-solving]] slides 17-22 (**19, 21, 22 image-only**). Book: [[russell-norvig-aima]] Ch. 6 (Global Edition). HW: research question → [[chess-vs-go]]. Code: [[tic-tac-toe-4x4-py]].

## Definitions

- **Game** = $S_0$, TO-MOVE, ACTIONS, RESULT, IS-TERMINAL, UTILITY ([[adversarial-search]]).
- Deterministic, two-player, turn-taking, **perfect-information** (= fully observable), **zero-sum** (chess: constant-sum).
- **MAX** maximises, **MIN** minimises the same utility. **Ply** = one move by one player.
- **Minimax value** = utility under optimal play by both sides ([[minimax]]).
- **α** = best value for MAX so far on the path ("at least"); **β** = best for MIN ("at most") ([[alpha-beta-pruning]]).
- **EVAL** = heuristic estimate of utility at a cutoff; **cutoff test** replaces the terminal test (H-MINIMAX).
- **MCTS** = selection → expansion → simulation → back-propagation ([[monte-carlo-tree-search]]).

## Formulas

$$\text{MINIMAX}(s) = \begin{cases}\text{UTILITY}(s) & \text{terminal}\\ \max_a \text{MINIMAX}(\text{RESULT}(s,a)) & \text{MAX}\\ \min_a \text{MINIMAX}(\text{RESULT}(s,a)) & \text{MIN}\end{cases}$$

$$\text{EVAL}(s) = \sum_i w_i f_i(s), \qquad \text{UTILITY(loss)} \le \text{EVAL}(s) \le \text{UTILITY(win)}$$

$$\text{UCB1}(n) = \frac{U(n)}{N(n)} + C\sqrt{\frac{\ln N(\text{PARENT}(n))}{N(n)}}, \quad C \approx \sqrt 2 \text{ in theory}$$

Pruning rules: in a MAX node stop when $v \ge \beta$; in a MIN node stop when $v \le \alpha$.

## Complexity table

| Algorithm | Time | Space | Exact? |
|---|---|---|---|
| Minimax | $O(b^m)$ | $O(bm)$ | yes |
| Alpha-beta, perfect ordering | $O(b^{m/2})$ (eff. b = $\sqrt b$) | $O(bm)$ | yes |
| Alpha-beta, random ordering | $\approx O(b^{3m/4})$ | $O(bm)$ | yes |
| H-MINIMAX / heuristic α-β to depth $d$ | $O(b^d)$ … $O(b^{d/2})$ | $O(bd)$ | no |
| MCTS | linear per playout | tree size | no (converges) |

([[slides-02-problem-solving]], slides 18, 20; [[russell-norvig-aima]] §6.2-6.4.) Details: [[game-search-comparison]].

## Must-know facts

- Tic-tac-toe 3×3: < 9! = 362,880 terminal nodes, 5,478 distinct states; chess $35^{80} \approx 10^{123}$ ([[russell-norvig-aima]] §6.1.1, §6.2.1).
- Alpha-beta returns the **same move** as minimax; perfect ordering ≈ **twice the depth**; chess effective $b$ ≈ 6.
- Move ordering helpers: captures/threats first, killer moves, iterative deepening, **transposition tables** (can double reachable depth in chess).
- Cutoff problems: **quiescence** (only evaluate quiet positions) and **horizon effect** (singular extensions).
- **Forward pruning** (beam over moves, PROBCUT, late-move reduction) = Type B, may lose the best move.
- Endgame **tablebases** by retrograde minimax: all ≤ 7-piece endings ([[russell-norvig-aima]] §6.3.4).
- Go: b starts at 361 → alpha-beta only 4-5 ply + no good EVAL → MCTS ([[russell-norvig-aima]] §6.4).
- MCTS returns the move with **most playouts**; with C = 1.4 the 60/79 node wins, with C = 1.5 the 2/11 node ([[russell-norvig-aima]] §6.4).
- Budget $10^9$, $b = 32$: minimax 6 ply, alpha-beta 12 ply, MCTS 10 M playouts.
- **Chess vs Go** ([[chess-vs-go]]): b ≈ 35 vs ≈ 250; tree $10^{123}$ vs $10^{360}$; states ≈ $10^{46}$ (≈ $10^{44}$) vs ≈ $10^{172}$ (exact $2.1 \times 10^{170}$); EXPTIME-complete vs PSPACE-hard (EXPTIME-complete with Japanese ko); Deep Blue 1997, AlphaGo 2016, AlphaZero 2018; Stockfish = alpha-beta + NNUE, Go engines = MCTS + nets.

## Class exercise: 4×4 tic-tac-toe ([[tic-tac-toe-4x4-py]])

- AI = X = MAX, human O moves first; `h_minimax` with alpha-beta, cutoff at **7 plies**, ordering **centre > corners > sides**, EVAL = open-line weights **1/3/9** for 1/2/3 marks, **÷ 90**, clamped to [−1, 1].
- First AI move: ≈ 120-140k nodes at depth 7 (≈ 0.25 s); depth 5: 6,923 nodes vs 396,076 for plain minimax (re-run 2026-10-01).
- α/β updated only when the best value improves — **correct** (equivalent to R&N Fig. 6.7).
- Weak spots: no depth bonus → may delay a win (14% of test positions); EVAL can tie a real win (±1); from the AI's 5th move the 7-ply search reaches the end of the game.

## Common traps

- Updating α in a MIN node / β in a MAX node — wrong way round.
- Quoting $O(b^{m/2})$ as the general alpha-beta cost (it is the best case).
- "Alpha-beta may change the decision" — no, never.
- Treating EVAL values as probabilities or utilities of terminal states; EVAL must equal UTILITY only at terminal states.
- Saying BFS/DFS "solve" chess: they ignore the opponent; but minimax/alpha-beta *are* depth-first.
- UCB1 uses the **natural** log; MCTS returns most-**visited**, not highest-rate.
- Slides say "falls below α / rises above β"; book and code prune on equality too (≤ α, ≥ β) — both correct.

## Practice questions

> [!question]- Q1. Compute the minimax value and decision: MAX root, MIN children with leaves (3, 12, 8), (2, 4, 6), (14, 5, 2).
> **Answer.** MIN values 3, 2, 2 → root 3, move to the first child ($a_1$) ([[russell-norvig-aima]] §6.2, Fig. 6.2).

> [!question]- Q2. Run alpha-beta on the same tree left to right. Which leaves are pruned?
> **Answer.** After the first child α = 3. Second child: first leaf 2 ≤ α → prune **4 and 6**. Third child: 14, 5, 2 all examined (2 only arrives last). Root = 3 ([[russell-norvig-aima]] §6.2.3, Fig. 6.5).

> [!question]- Q3. Run alpha-beta on MAX root → MIN children (5, 8, 7), (3, 9, 1), (6, 2, 10).
> **Answer.** First child = 5, α = 5. Second: 3 ≤ 5 → prune 9, 1. Third: 6, then 2 ≤ 5 → prune 10. Root = 5; pruned leaves: 9, 1, 10.

> [!question]- Q4. Three-ply tree: MAX → MIN₁, MIN₂ → MAX nodes → leaves. MIN₁: (3, 5), (6, 9); MIN₂: (1, 2), (0, −1). Value and pruned leaves?
> **Answer.** Value 5. Pruned: leaf 9 (MAX node sees 6 ≥ β = 5) and the whole MAX node (0, −1) (MIN₂ ≤ 2 ≤ α = 5).

> [!question]- Q5. Reorder the children of Q1 as (2, 4, 6), (14, 5, 2), (3, 12, 8). How many leaves are pruned? What lesson?
> **Answer.** Zero. Same root value 3. Alpha-beta's savings depend on examining the best moves first ([[russell-norvig-aima]] §6.2.4).

> [!question]- Q6. State the requirements on an evaluation function and give the classic chess example.
> **Answer.** EVAL = UTILITY on terminal states, loss ≤ EVAL ≤ win otherwise, fast, strongly correlated with winning chances. Weighted linear material: pawn 1, knight/bishop 3, rook 5, queen 9 ([[russell-norvig-aima]] §6.3.1).

> [!question]- Q7. What is a quiescent position and why does it matter?
> **Answer.** One with no pending move that would swing the evaluation wildly (e.g. a capture). Evaluating non-quiescent positions gives wrong values (Fig. 6.8(b): Black seems ahead but White captures the queen), so the search continues (quiescence search) until quiet ([[russell-norvig-aima]] §6.3.2).

> [!question]- Q8. Explain the horizon effect with the 4×4 tic-tac-toe AI in mind.
> **Answer.** With a fixed 7-ply cutoff, a threat that materialises at ply 8+ is invisible; the AI may choose moves that only *postpone* a forced loss beyond the horizon and judge them fine. Remedies: deeper/iterative-deepening search, singular extensions, quiescence ([[russell-norvig-aima]] §6.3.2; [[tic-tac-toe-4x4-py]]).

> [!question]- Q9. UCB1 with C = 1.4: root has 100 playouts; child A 60/79, child B 2/11. Which is selected?
> **Answer.** A: 0.759 + 1.4·√(4.605/79) = 1.098. B: 0.182 + 1.4·√(4.605/11) = 1.088. A is selected (with C = 1.5, B: 1.152 > A: 1.122) ([[russell-norvig-aima]] §6.4).

> [!question]- Q10. Why did AlphaGo need MCTS with neural networks while Deep Blue managed with alpha-beta?
> **Answer.** Go's branching factor (≈ 250) limits alpha-beta to a few ply, and there is no simple evaluation (all stones equal, life-and-death far ahead). MCTS needs no hand-made EVAL; the policy net narrows candidate moves and the value net evaluates positions ([[chess-vs-go]]; [[hw01-report]]).

> [!question]- Q11. In `tic-tac-toe.py`, α is updated only inside `if valor > mejor_valor`. Is pruning still correct?
> **Answer.** Yes. If the best value does not change, neither does `max(alpha, mejor_valor)` nor the outcome of `mejor_valor >= beta` (β is fixed in a MAX node). Equivalent to R&N Fig. 6.7 ([[tic-tac-toe-4x4-py]]).

> [!question]- Q12. The tic-tac-toe AI sometimes ignores an immediate win. Why and how to fix?
> **Answer.** All forced wins are +1 regardless of depth and the first equal-valued move in the ordering is kept. Use a depth-adjusted utility, e.g. +(1000 − depth) for a win ([[tic-tac-toe-4x4-py]]).

> [!question]- Q13. Define state-space vs game-tree complexity and give both for chess.
> **Answer.** State space = distinct positions ≈ $10^{46}$ (later ≈ $10^{44}$); game tree = distinct move sequences ≈ $35^{80} \approx 10^{123}$ ([[chess-vs-go]]).

## Weak spots

*(To be filled during exam prep sessions.)*
