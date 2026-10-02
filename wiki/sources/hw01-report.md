---
type: source
summary: Raymond's Homework 1 report — a chess-vs-Go research essay plus six practical problems (8-puzzle, 80-tile, N-Queens, farmer, missionaries and cannibals, Sudoku) solved with BFS/DFS/greedy/A*/weighted A*/beam search and CSP backtracking.
unit: [3, 4]
tags: [hw01, homework, search, csp, games, report]
sources: ["[[hw01-report]]"]
updated: 2026-10-01
---

# HW01 report (Raymond Portilla)

**Bibliographic line.** Portilla, R. *Homework #1*. Artificial Intelligence, NRC 1651, USFQ; dated 16/09/2026. Files: `raw/HW_01/HW01_RP.pdf` / `raw/HW_01/HW01_RP.docx`; code in `raw/HW_01/Practical_exercises/`.

**What it is.** The submitted homework: one research question and six practical problems. Every table number reproduces when the code is re-run (Ex01, Ex04, Ex05 re-checked for this wiki on 2026-10-01).

## Key points

**Research question — chess vs Go** → [[chess-vs-go]]
- State of the art: Deep Blue (1997) = alpha-beta + handcrafted evaluation (Campbell et al., 2002); Stockfish = alpha-beta + neural evaluation; AlphaGo → AlphaZero = self-play network + MCTS (Silver et al., 2018).
- Similar: two-player, zero-sum, deterministic, perfect information; both superhuman. Different: branching factor ~35 vs ~250; game tree ~$10^{123}$ vs ~$10^{360}$; state space ~$10^{46}$ vs ~$10^{172}$ (van den Herik et al., 2002); easy material evaluation in chess, none in Go.
- Complexity: generalized $n\times n$ chess needs exponential time (Fraenkel & Lichtenstein, 1981); Go is "computationally very hard" (Lichtenstein & Sipser, 1980 — PSPACE-hard).
- BFS/DFS: not usable alone; [[minimax]] is the right model; [[alpha-beta-pruning]] works for chess; Go needs [[monte-carlo-tree-search]] with a network.

**1. 8-tile** → [[hw01-ex01-8-puzzle]]
- Formulation from §3.2; start = book Fig. 3.3 start, goal blank-last; parity check; graph search.
- BFS 20 (optimal), DFS 66,056, greedy Manhattan 48 / Euclidean 94 / misplaced 116. Manhattan expanded the fewest nodes (123) → [[heuristics-8-puzzle-comparison]], [[greedy-best-first-search]], [[breadth-first-search]], [[depth-first-search]].

**2. 80-tile** → [[hw01-ex02-80-tile]]
- 9×9 board, Manhattan start = 306 (lower bound). [[a-star]] stopped at 250,000 expansions (best $h$ 287); [[weighted-a-star]] W = 10 → 1,116; [[beam-search]] k = 500 → 1,078, k = 5000 → **740** (best, not proven optimal). Depth-2 Graphviz tree.

**3. N-Queens** → [[hw01-ex03-n-queens]]
- CSP: variables = columns, domain = rows; incremental backtracking, one queen per column, `is_safe` checks left side only; works for any N; none for N = 2, 3 → [[csp-backtracking-search]], [[constraint-satisfaction-problems]].

**4. Farmer, wolf, goat, cabbage** → [[hw01-ex04-farmer-wolf-goat-cabbage]]
- 4-boolean state; BFS → 7 crossings; twin solution exists.

**5. Missionaries and cannibals** → [[hw01-ex05-missionaries-cannibals]]
- `(m_left, c_left, boat_left)`; 5 boat loads; BFS → 11 crossings.

**6. Sudoku** → [[hw01-ex06-sudoku]]
- CSP with all-different constraints; naive backtracking vs MRV vs LCV vs forward checking, each alone; MRV best (board 1: 51 assignments, 0 backtracks; board 2: 4,036 vs 335,637 naive); both boards have a unique solution → [[csp-heuristics]], [[constraint-propagation]], [[csp-techniques-comparison]].

**Closing**: BFS for small unit-cost path problems; backtracking for CSPs; beam k = 5000 as best 80-tile path; A* "would be optimal with more time and a stronger heuristic".

## Pages that use this source

[[hw01-ex01-8-puzzle]] · [[hw01-ex02-80-tile]] · [[hw01-ex03-n-queens]] · [[hw01-ex04-farmer-wolf-goat-cabbage]] · [[hw01-ex05-missionaries-cannibals]] · [[hw01-ex06-sudoku]] · [[chess-vs-go]] · [[heuristics-8-puzzle-comparison]] · [[search-algorithms-comparison]] · [[problem-formulation]] · [[breadth-first-search]] · [[depth-first-search]] · [[greedy-best-first-search]] · [[a-star]] · [[weighted-a-star]] · [[beam-search]] · [[heuristic-functions]] · [[unit-03-search-review]] · [[midterm-01-review]]

## Issues found

Wording in the report that does not match the code (the table numbers do match):
- **9H vs 9I** — the assignment text names 9H as missing but also says only quadrant I has the hole; the report and code remove 9I.
- **"Each 3×3 is also rotated"** — it is a clockwise **spiral** (`1 2 3 / 8 9 4 / 7 6 5`), not a rotation.
- **"h goes back to 306"** in the 80-tile tree — that node is the start state (tree drawn without visited set).
- **"Other weights were less stable in small tests"** — no trace in the code; W = 10 was hand-tuned.
- **"The true length is much larger than 306"** — unproven; only $306 \le C^* \le 740$.
- **"MRV already sees a dead cell very soon, so extra forward checking does not change the story much"** (Sudoku) — MRV + FC was never run together; this is an expectation, not a result.
- **"Start board from the book figure"** — only the start; the goal differs from Fig. 3.3 (optimum 20 vs 26).
- **BFS "as in the book"** — the code uses the late goal test, the book's Fig. 3.9 the early one.
- **Go "computationally very hard"** — say PSPACE-hard (EXPTIME-complete with Japanese ko).
- **"Plain BFS or DFS cannot finish"** — alpha-beta itself is depth-first, inside iterative deepening.
- Date: report dated 16/09/2026, while the syllabus lists HW01 for September 11 ([[slides-00-instructor-introduction]], slide 5) — likely a moved deadline (unverified).
- AI use: Graphviz syntax and the reading list came from an AI chat ([[hw01-ai-transcript]]).
