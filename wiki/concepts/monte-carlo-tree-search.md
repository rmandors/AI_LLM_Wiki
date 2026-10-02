---
type: concept
summary: MCTS estimates move values from many simulated playouts, growing a search tree by repeated selection (UCB1/UCT), expansion, simulation and back-propagation; it is the core of modern Go programs.
unit: 4
tags: [games, mcts, uct, ucb1, go, exploration-exploitation]
sources: ["[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Monte Carlo tree search (MCTS)

**Monte Carlo tree search** chooses a move without a hand-written evaluation function: the value of a state is estimated as the **average utility of many simulated games** (playouts / rollouts) started from it. A search tree is grown selectively toward the most promising moves, balancing **exploitation** of moves that have won often and **exploration** of moves that have been tried rarely ([[russell-norvig-aima]] §6.4). Modern Go programs abandoned alpha-beta for MCTS ([[russell-norvig-aima]] §6.4; [[chess-vs-go]]).

## How it works

Repeat until time runs out ([[russell-norvig-aima]] §6.4, Figs. 6.10-6.11):

1. **Selection** — from the root, repeatedly pick a child using the **selection policy** (e.g. UCT) until a leaf of the tree.
2. **Expansion** — add one (or more) new child node to the selected leaf.
3. **Simulation** — play out the game from the new node with a **playout policy** (random or learned); these moves are *not* stored in the tree.
4. **Back-propagation** — update wins/visits of every node on the path to the root (the winner's nodes get +1 win and +1 playout; the loser's nodes get +1 playout only).

Finally return the move with the **most playouts** (more robust than the highest average: 65/100 beats 2/3) ([[russell-norvig-aima]] §6.4).

**UCT selection** uses the UCB1 formula ([[russell-norvig-aima]] §6.4):

$$
\text{UCB1}(n) = \frac{U(n)}{N(n)} + C \sqrt{\frac{\ln N(\text{PARENT}(n))}{N(n)}}
$$

$U(n)$ = total utility of playouts through $n$, $N(n)$ = number of playouts through $n$. The first term is exploitation, the second exploration; theory suggests $C = \sqrt 2$, practitioners tune it. See [[exploration-vs-exploitation]].

**Variants.** *Pure Monte Carlo search* does N playouts from the root only (no tree). AlphaZero replaces random playouts with a **value network** and adds a **policy-network prior** to the selection formula (PUCT) ([[russell-norvig-aima]] §6.4). Playouts can be truncated early and scored with an evaluation function (**early playout termination**) ([[russell-norvig-aima]] §6.4).

## Properties

- **Anytime**: can stop after any iteration and return the current best move.
- **Cost of one playout** is linear in game length (one move per ply), not exponential ([[russell-norvig-aima]] §6.4).
- **Needs no evaluation function** — only the rules; good for new games or games like Go where evaluation is hard ([[russell-norvig-aima]] §6.4).
- **Robust to single evaluation errors** because it aggregates many playouts; alpha-beta can be misled by one wrong leaf value ([[russell-norvig-aima]] §6.4).
- **Weakness**: a single crucial move (trap/tactic) may never be sampled (it is a Type B, selective strategy); and "obvious" wins may take many playout moves to confirm ([[russell-norvig-aima]] §6.4).
- **Budget example**: $b = 32$, 100-ply games, $10^9$ states per move → minimax reaches 6 ply, alpha-beta 12 ply, MCTS can run 10 million playouts ([[russell-norvig-aima]] §6.4).

## In this course

- Not in the slides of [[slides-02-problem-solving]] (the games part covers only [[minimax]] and [[alpha-beta-pruning]]); it appears in the HW01 research question.
- [[hw01-report]] (Research Question): for Go "the big change was AlphaGo, and then AlphaGo Zero and AlphaZero. They train a deep neural network by playing against themselves, and they use Monte Carlo tree search to choose a move"; "the net says which moves look promising, so the search does not try everything".
- has the model answer for "How does MCTS work?" (four steps, UCB1/UCT, AlphaZero's PUCT). Current Go engines (KataGo, Leela Zero) use MCTS (PUCT) + policy/value network.
- No MCTS code in `raw/` yet.

## Common mistakes

- Thinking playouts are stored in the tree — only one node is added per iteration; playout moves are discarded.
- Returning the child with highest win *rate* instead of most *visits*.
- Using $\log_{10}$ instead of the natural log in UCB1 (R&N's numbers in Fig. 6.10 only work with $\ln$).
- Saying MCTS "is a neural network". Plain MCTS uses no learning; AlphaGo/AlphaZero *combine* MCTS with networks (see [[perceptron]] for the neural-network basics).
- Assuming MCTS needs randomness from the game: the game is deterministic; the randomness is in the playout policy.

## Related

[[adversarial-search]] · [[minimax]] · [[alpha-beta-pruning]] · [[exploration-vs-exploitation]] · [[chess-vs-go]] · [[game-search-comparison]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. List the four MCTS steps in order and say which one uses the playout policy.
> **Answer.** Selection → expansion → simulation → back-propagation. The **simulation** step uses the playout policy; selection uses the selection policy (e.g. UCT) ([[russell-norvig-aima]] §6.4).

> [!question]- Q2. Root has 100 playouts. Child A: 60 wins / 79 playouts, child B: 2/11, child C: 1/10. Compute UCB1 for A and B with C = 1.4 and C = 1.5.
> **Answer.** $\ln 100 = 4.605$. A: $60/79 = 0.759$; exploration $= C\sqrt{4.605/79} = C \times 0.241$ → **1.098** (C = 1.4), **1.122** (C = 1.5). B: $2/11 = 0.182$; exploration $= C\sqrt{4.605/11} = C \times 0.647$ → **1.088** (C = 1.4), **1.152** (C = 1.5). So A is selected with C = 1.4 and B with C = 1.5, matching R&N §6.4 (Fig. 6.10).

> [!question]- Q3. Black wins a playout through the path root (white, 37/100) → 60/79 (black) → 16/53 (white) → 27/35 (black). What are the new counts?
> **Answer.** Black nodes get +1 win and +1 playout: 27/35 → 28/36, 60/79 → 61/80. White nodes get +1 playout only: 16/53 → 16/54, root 37/100 → 37/101 ([[russell-norvig-aima]] §6.4).

> [!question]- Q4. Why did Go favour MCTS over alpha-beta for so long?
> **Answer.** Huge branching factor (361 at the start, ≈250 on average) limits alpha-beta to a few ply, and there is no good cheap evaluation function (material means little; groups live or die far in the future). MCTS needs no evaluation function and samples selectively ([[russell-norvig-aima]] §6.4; [[chess-vs-go]]).

> [!question]- Q5. Name one situation where MCTS is weaker than alpha-beta.
> **Answer.** When a single move changes the game (a sharp tactic): the stochastic, selective search may never sample it. Also when a position is "obviously" won but needs many moves to confirm in playouts ([[russell-norvig-aima]] §6.4).
