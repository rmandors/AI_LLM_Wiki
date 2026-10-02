---
type: concept
summary: Search in multi-agent competitive environments (games) where an opponent chooses half the moves, so the goal is an optimal strategy rather than a path.
unit: 4
tags: [games, adversarial-search, minimax, zero-sum]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]", "[[hw01-report]]"]
updated: 2026-10-01
---

# Adversarial search

**Adversarial search** is search in a competitive multi-agent environment: two (or more) agents have conflicting goals, so the searcher cannot just find a path to a goal state. It must find a **strategy** (a conditional plan that answers every possible opponent reply), assuming the opponent also plays well ([[slides-02-problem-solving]], slide 17; [[russell-norvig-aima]] §6.1, §6.2). The classic setting is the game: **deterministic, two-player, turn-taking, perfect-information, zero-sum** games such as chess, Go and tic-tac-toe ([[russell-norvig-aima]] §6.1.1).

## How it works

A game is defined formally by six elements ([[russell-norvig-aima]] §6.1.1):

| Element | Meaning |
|---|---|
| $S_0$ | initial state (how the game is set up) |
| `TO-MOVE(s)` | the player whose turn it is in $s$ |
| `ACTIONS(s)` | legal moves in $s$ |
| `RESULT(s, a)` | transition model |
| `IS-TERMINAL(s)` | terminal test (game over?) |
| `UTILITY(s, p)` | final payoff for player $p$ (chess: 1, 0, ½) |

- The two players are called **MAX** (wants to maximise the utility) and **MIN** (wants to minimise it); "one player's gain is the other player's loss" ([[slides-02-problem-solving]], slides 17-18).
- $S_0$, `ACTIONS` and `RESULT` define a **state-space graph**; superimposing a search tree that follows every move sequence to a terminal state gives the **game tree** ([[russell-norvig-aima]] §6.1.1). Compare [[state-space-and-graph-search]].
- A **ply** is one move by one player (one level of the tree) ([[russell-norvig-aima]] §6.2).
- The optimal decision is computed with [[minimax]]; [[alpha-beta-pruning]] computes the same decision while skipping irrelevant branches; real games cut the search off at a depth and apply an **evaluation function** (H-MINIMAX, see [[minimax#H-MINIMAX]]) or estimate values by random playouts ([[monte-carlo-tree-search]]) ([[russell-norvig-aima]] §6.1, §6.3, §6.4).

**Three stances** toward other agents ([[russell-norvig-aima]] §6.1): treat many agents in aggregate as an *economy*; treat the adversary as part of a *nondeterministic environment* (misses that it actively tries to beat you); or *explicitly model it* with game-tree search — the subject of this unit.

## Properties

- **Environment** (see [[environment-properties]]): multi-agent competitive, fully observable ("perfect information"), deterministic, sequential, discrete ([[slides-02-problem-solving]], slide 17).
- **Zero-sum**: what is good for one player is equally bad for the other; chess is technically *constant-sum* (+1 total per game) but the name is traditional ([[russell-norvig-aima]] §6.1.1, footnote 2).
- **Size**: tic-tac-toe has fewer than $9! = 362{,}880$ terminal nodes (5,478 distinct states); chess has over $10^{40}$ nodes in its state graph and a game tree of about $35^{80} \approx 10^{123}$ ([[russell-norvig-aima]] §6.1.1, §6.2.1). So the full tree is "a theoretical construct", and practical play needs pruning and cutoffs.
- **Variants** outside the deterministic two-player case: multiplayer games use vectors of utilities ([[russell-norvig-aima]] §6.2.2); dice games add chance nodes and **expectiminimax** ([[russell-norvig-aima]] §6.5); card games have imperfect information (§6.6, not covered in class yet).

## In this course

- Slide 17 of [[slides-02-problem-solving]] introduces the topic: "So far: one agent searching for a solution in a cooperative or neutral environment. In games: two or more agents with opposing objectives. The problem is no longer finding a path to the goal; it is finding the optimal strategy while considering that the opponent also plays optimally." Slides 18-22 cover [[minimax]] and [[alpha-beta-pruning]]; **slides 19, 21 and 22 are image-only** (their content is missing from the text extraction; the pages here fill it from R&N §6.2).
- The HW01 research question compared chess and Go as adversarial search problems → [[chess-vs-go]] ([[hw01-report]], Research Question).
- The class exercise [[tic-tac-toe-4x4-py]] implements depth-limited minimax with alpha-beta for 4×4 tic-tac-toe.
- Side-by-side of the algorithms: [[game-search-comparison]]. Cheat sheet: [[unit-04-games-review]].

## Common mistakes

- Using plain single-agent [[breadth-first-search]] or [[depth-first-search]] to look for "a winning path": they ignore that the opponent chooses half of the moves. (Minimax itself *is* a depth-first traversal; the issue is the missing MIN/MAX alternation, not depth-first order —.)
- Calling the output a "path". It is a **strategy**/policy; in practice only the root decision (the next move) is used.
- Confusing **state-space size** (distinct positions) with **game-tree size** (distinct move sequences, roughly $b^d$, much larger because positions repeat).
- Forgetting that utilities are from MAX's point of view in two-player zero-sum games.

## Related

[[minimax]] · [[alpha-beta-pruning]] · [[monte-carlo-tree-search]] · [[game-search-comparison]] · [[chess-vs-go]] · [[tic-tac-toe-4x4-py]] · [[intelligent-agents]] · [[environment-properties]] · [[heuristic-functions]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Name the six elements of the formal definition of a game.
> **Answer.** $S_0$ (initial state), `TO-MOVE(s)`, `ACTIONS(s)`, `RESULT(s,a)`, `IS-TERMINAL(s)`, `UTILITY(s,p)` ([[russell-norvig-aima]] §6.1.1).

> [!question]- Q2. Why does adversarial search return a strategy instead of a path?
> **Answer.** Because MAX does not control MIN's moves. A plan must specify a reply to every possible MIN move (a contingent plan), just like AND-OR search in nondeterministic environments ([[russell-norvig-aima]] §6.2). In practice the agent re-searches at every turn and only plays the root move.

> [!question]- Q3. Classify chess along the environment dimensions.
> **Answer.** Fully observable (perfect information), deterministic, multi-agent competitive, sequential, discrete, and static (semidynamic with a clock) ([[slides-02-problem-solving]], slide 17; [[environment-properties]]).

> [!question]- Q4. Chess has $b \approx 35$ and games of about 80 ply. Estimate the game-tree size.
> **Answer.** $35^{80} = 10^{80 \log_{10} 35} \approx 10^{80 \times 1.544} \approx 10^{123.5}$, i.e. about $10^{123}$ ([[russell-norvig-aima]] §6.2.1).

> [!question]- Q5. Is chess really "zero-sum" if a win is worth 1 and a draw ½ to each side?
> **Answer.** Strictly it is *constant-sum*: the payoffs always add to 1. Subtracting an "entry fee" of ½ per player makes the sum zero, so the theory is the same ([[russell-norvig-aima]] §6.1.1, footnote 2).
