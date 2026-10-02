---
type: comparison
summary: Chess vs Go as AI search problems (HW01 research question) — same game class, but b≈35 vs ≈250, game trees 10^123 vs 10^360 and easy vs hard evaluation explain why alpha-beta won chess in 1997 while Go needed MCTS with neural networks (2016).
unit: 4
tags: [games, chess, go, alpha-beta, mcts, complexity, hw01]
sources: ["[[hw01-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Chess vs Go

The HW01 research question asked: what are the state-of-the-art algorithms for chess and Go, how are the games similar and different, how complex are they, and can BFS, DFS, minimax or alpha-beta be used? ([[hw01-report]], Research Question). Both are deterministic, two-player, zero-sum, perfect-information games (see [[adversarial-search]]); the differences in **branching factor** and **ease of evaluation** decide which search method works.

## Facts table

The report gives the branching factors, the game-tree sizes and the older state-space bounds, citing van den Herik et al. 2002 ([[hw01-report]], Research Question). The later state-space estimates and the complexity class names are filled in below.

| Fact | Chess | Go (19×19) |
|---|---|---|
| Average branching factor $b$ | ≈ 35 | ≈ 250 (361 on the empty board, [[russell-norvig-aima]] §6.4) |
| Typical game length | ≈ 80 plies | ≈ 150 moves |
| Game-tree size $b^d$ | $35^{80} \approx 10^{123}$ | $250^{150} \approx 10^{360}$ |
| State-space size | ≈ $10^{46}$ (Allis upper bound; later ≈ $10^{44}$) | ≈ $10^{172}$ upper bound; exactly ≈ $2.1 \times 10^{170}$ legal positions (Tromp 2016) |
| Complexity (generalised $n \times n$) | **EXPTIME-complete** (Fraenkel & Lichtenstein 1981) | **PSPACE-hard** (Lichtenstein & Sipser 1980); **EXPTIME-complete** with Japanese ko (Robson 1983) |
| Evaluation | material + simple positional features | stones all alike; value of groups depends on life-and-death far ahead |
| Milestone | Deep Blue beats Kasparov, **1997** | AlphaGo beats Lee Sedol 4-1, **2016** |
| Then | — | AlphaGo Zero 2017 (self-play only), **AlphaZero 2018** (chess, shogi, Go from the rules) |
| Current top method | alpha-beta (PVS) + **NNUE** evaluation (Stockfish); MCTS + net (Leela) | **MCTS (PUCT) + policy/value network** (KataGo, Leela Zero, AlphaZero line) |
| Solved? | No; endgames with ≤ 7 pieces are (tablebases) | No |

Mental check: $\log_{10} 35 \approx 1.54$, ×80 ≈ 123; $\log_{10} 250 \approx 2.40$, ×150 ≈ 360. R&N give the same chess numbers ($b \approx 35$, 80 ply, $35^{80} \approx 10^{123}$, [[russell-norvig-aima]] §6.2.1) and note that tablebases cover all endings with ≤ 7 pieces (400 trillion positions; [[russell-norvig-aima]] §6.3.4).

## Which search method works

| Method | Chess | Go | Why ([[hw01-report]]; [[russell-norvig-aima]] §6.2-6.4) |
|---|---|---|---|
| Plain [[breadth-first-search]] | ✗ | ✗ | ignores the opponent; $O(b^d)$ memory impossible |
| Plain [[depth-first-search]] | ✗ | ✗ | ignores the opponent; may follow a huge line |
| Full [[minimax]] | model only | model only | right concept, but $10^{123}$ / $10^{360}$ nodes |
| [[alpha-beta-pruning]] + EVAL (Type A) | ✓ (Deep Blue, Stockfish) | ✗ | $\sqrt{35} \approx 6$ effective b is manageable; in Go alpha-beta reaches only 4-5 ply and EVAL is weak |
| [[monte-carlo-tree-search]] + networks (Type B) | ✓ (AlphaZero, Leela) | ✓ (AlphaGo → KataGo) | selective, needs no hand-made EVAL, policy net prunes candidate moves |

Shannon (1950) already distinguished Type A (wide, shallow, evaluate at a fixed depth) from Type B (narrow, deep, follow promising lines); most chess programs were Type A, Go programs Type B, and Type B now also reaches world-champion level in chess (Silver et al. 2018) ([[russell-norvig-aima]] §6.2.4).

**Raymond's conclusion**: "We can use minimax and alpha-beta as the base, especially in chess, but not plain BFS or DFS. For Go we still search a tree, but the search is Monte Carlo tree search, not classic alpha-beta. The old algorithms did not disappear. They became part of a bigger system." ([[hw01-report]], Research Question).

> [!warning] Nuance
> "Plain BFS or DFS cannot finish" is true for single-agent BFS/DFS, but alpha-beta **is** a depth-first traversal and real engines wrap it in [[iterative-deepening-search]]. The depth-first idea survives inside alpha-beta.

> [!warning] Gaps in the report
> The report says Go is "computationally very hard" without naming the class — say **PSPACE-hard** (EXPTIME-complete with Japanese ko). Its state-space numbers ($10^{46}$, $10^{172}$) are old upper bounds. Knuth & Moore (alpha-beta efficiency) and Robson (Go EXPTIME) are in the reading list but not cited.
>
> Also: the report cites only Silver et al. (2018, *Science*, the AlphaZero paper) for the whole AlphaGo → AlphaGo Zero → AlphaZero story. The original AlphaGo and AlphaGo Zero results are separate *Nature* papers (Silver et al. 2016 and 2017) (general knowledge) — worth knowing if asked for the source of the 2016 milestone.

## When to use which

- **Low branching factor + good cheap evaluation** (chess, checkers, 4×4 tic-tac-toe as in [[tic-tac-toe-4x4-py]]): heuristic alpha-beta with good move ordering, iterative deepening and transposition tables.
- **High branching factor or no good evaluation** (Go, new games): MCTS; add learned policy/value networks when self-play training is possible.
- **Both** paradigms now use neural networks: Stockfish's NNUE evaluation inside alpha-beta vs AlphaZero's network inside MCTS.

## Related

[[adversarial-search]] · [[minimax]] · [[alpha-beta-pruning]] · [[monte-carlo-tree-search]] · [[game-search-comparison]] · [[hw01-report]] · [[hw01-ai-transcript]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Give the four numbers that best summarise why Go is harder than chess for search.
> **Answer.** Branching factor ≈ 35 vs ≈ 250, and game tree ≈ $10^{123}$ vs ≈ $10^{360}$ ([[hw01-report]]).

> [!question]- Q2. What is the difference between state-space complexity and game-tree complexity?
> **Answer.** State space = number of distinct legal positions (a position reached by different move orders counts once). Game tree = number of distinct move sequences, roughly $b^d$, much larger because positions repeat across branches.

> [!question]- Q3. What does "EXPTIME-complete" mean for chess, and why only for $n \times n$ boards?
> **Answer.** Perfect play needs time exponential in the board size, and chess is among the hardest problems solvable in exponential time. Standard 8×8 chess is a finite, constant-size problem; complexity classes need a growing input, so the proofs use generalised boards.

> [!question]- Q4. Why did alpha-beta work for chess in 1997 but not for Go?
> **Answer.** Branching factor (Go's ≈ 250 means far shallower search for the same node budget) and evaluation (chess has material; in Go the value of a group depends on life-and-death far in the future). Alpha-beta is only as good as the evaluation at the cutoff ([[russell-norvig-aima]] §6.4).

> [!question]- Q5. With perfect move ordering, what is chess's effective branching factor under alpha-beta?
> **Answer.** $\sqrt{35} \approx 5.9$, about 6 instead of 35 ([[russell-norvig-aima]] §6.2.4).

> [!question]- Q6. AlphaGo vs AlphaZero?
> **Answer.** AlphaGo (2016) learned first from human expert games and also used rollouts. AlphaGo Zero (2017) learned Go from self-play only. AlphaZero (2018) is the same general algorithm for chess, shogi and Go, starting from the rules only.

> [!question]- Q7. Is chess solved? Name a solved game.
> **Answer.** No; only endgames with up to 7 pieces are solved via tablebases. Checkers was weakly solved in 2007 (Schaeffer et al.).
