---
type: concept
summary: Alpha-beta pruning returns the same move as minimax while skipping branches that cannot affect the decision, using bounds α (MAX's best so far) and β (MIN's best so far); with perfect move ordering it costs O(b^(m/2)).
unit: 4
tags: [games, alpha-beta, minimax, pruning, move-ordering]
sources: ["[[slides-02-problem-solving]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Alpha-beta pruning

**Alpha-beta pruning** is [[minimax]] with two extra parameters that let it stop exploring a node as soon as it is clear that the node cannot change the decision higher up. It "finds the same solution as Minimax while exploring far fewer nodes" ([[slides-02-problem-solving]], slide 20; [[russell-norvig-aima]] §6.2.3).

- $\alpha$ = value of the best (highest) choice found so far for **MAX** anywhere along the current path — think "at least".
- $\beta$ = value of the best (lowest) choice found so far for **MIN** along the path — think "at most".

([[slides-02-problem-solving]], slide 20; [[russell-norvig-aima]] §6.2.3.)

## How it works

General principle: if Player has a better choice $m$ (at the same level or anywhere higher up), Player will never move to $n$, so once we know enough about $n$ we prune it ([[russell-norvig-aima]] §6.2.3, Fig. 6.6).

Algorithm (R&N Fig. 6.7, paraphrased):

```text
ALPHA-BETA-SEARCH(state): v, move = MAX-VALUE(state, -inf, +inf); return move
MAX-VALUE(s, α, β):
    if terminal: return UTILITY(s), null
    v = -inf
    for a in ACTIONS(s):
        v2 = MIN-VALUE(RESULT(s,a), α, β)
        if v2 > v: v, move = v2, a; α = max(α, v)
        if v >= β: return v, move # β-cutoff: MIN above will never allow this
    return v, move
MIN-VALUE(s, α, β): symmetric: keep smallest v, β = min(β, v), cut if v <= α
```

Slide 20 of [[slides-02-problem-solving]] states the rule in words: "If the value at a MIN node falls below α → prune (MAX would never choose this path). If the value at a MAX node rises above β → prune (MIN would never choose this path)." The book and code prune on equality as well ($\le\alpha$, $\ge\beta$), which is also safe.

**Worked example (R&N Fig. 6.5).** Leaves B = (3, 12, 8), C = (2, *x*, *y*), D = (14, 5, 2), left to right:
1. B: 3, 12, 8 → B = 3. At the root, α = 3.
2. C: first leaf 2 → C ≤ 2 ≤ α → **prune** C's other two leaves.
3. D: 14 (D ≤ 14, keep going), 5, 2 → D = 2.
4. Root = max(3, ≤2, 2) = **3**. Two leaves are never evaluated: $\text{MINIMAX}(root) = \max(3, \min(2,x,y), 2) = 3$ for any $x, y$ ([[russell-norvig-aima]] §6.2.3).

### Move ordering

Pruning depends heavily on the order in which children are examined ([[russell-norvig-aima]] §6.2.4):

| Ordering | Nodes examined | Effective branching factor |
|---|---|---|
| None (plain minimax) | $O(b^m)$ | $b$ |
| Random | $\approx O(b^{3m/4})$ | $b^{3/4}$ |
| Perfect (best move first) | $O(b^{m/2})$ | $\sqrt{b}$ (chess: about 6 instead of 35) |

With perfect ordering alpha-beta can search **about twice as deep** as minimax in the same time ([[russell-norvig-aima]] §6.2.4; the $O(b^{m/2})$ result is Knuth & Moore 1975 per ). Practical ordering tricks: captures first, then threats, then forward moves (chess), **killer moves**, ordering from the previous [[iterative-deepening-search]] iteration, and **transposition tables** that cache values of positions reached by different move orders ([[russell-norvig-aima]] §6.2.4).

### Heuristic alpha-beta

For real games, replace the terminal test by a cutoff test and the utility by EVAL: `if IS-CUTOFF(state, depth): return EVAL(state), null` (see [[minimax#H-MINIMAX]]; [[russell-norvig-aima]] §6.3.2). **Forward pruning** (beam over moves, PROBCUT, late-move reduction) also discards moves that only *look* bad — faster but may lose the best move (a Shannon "Type B" strategy; [[russell-norvig-aima]] §6.3.3; compare [[beam-search]]).

## Properties

- **Correct**: returns exactly the minimax value and move at the root (pruned branches provably cannot change it) ([[russell-norvig-aima]] §6.2.3).
- **Time**: best case $O(b^{m/2})$ ("optimal complexity", [[slides-02-problem-solving]], slide 20), random ordering $\approx O(b^{3m/4})$, worst case $O(b^m)$ (no pruning).
- **Space**: same as minimax, $O(bm)$ — depth-first.
- Values returned for *internal* nodes may only be bounds (when a cutoff happened), but the root value is exact (general knowledge).

## In this course

- Slide 20 of [[slides-02-problem-solving]]: motivation ("Minimax explores the entire tree but is inefficient for real games"), $O(b^{m/2})$, the pruning rule and the meaning of α/β. **Slides 21 and 22 are image-only** — probably the step-by-step pruning figure, but the extraction has no text, so the worked example here is R&N Fig. 6.5.
- HW01 research: "Alpha-beta pruning is a smarter minimax … For chess this worked very well. Deep Blue was basically this idea, only at a huge scale" and modern Stockfish still uses alpha-beta, now with an NNUE evaluation ([[hw01-report]], Research Question; [[chess-vs-go]]).
- [[tic-tac-toe-4x4-py]] implements heuristic alpha-beta with move ordering centre > corners > sides. Measured from the AI's first reply to a corner opening: depth 3 visits 350 nodes vs 2,956 for plain minimax, depth 5 visits 6,923 vs 396,076 (≈57× fewer), depth 7 about 128k nodes in ≈0.25 s (re-run 2026-10-01; [[tic-tac-toe-4x4-py]], Results).

## Common mistakes

- Thinking alpha-beta can return a *different* move than minimax. It cannot (same root value; with ties it may pick a different but equally valued move only if the tie-break differs).
- Resetting α/β when going down: children inherit the parent's current $(\alpha, \beta)$ window.
- Updating α in a MIN node or β in a MAX node. MAX nodes raise α; MIN nodes lower β.
- Quoting $O(b^{m/2})$ as the general complexity — it is the **best case** with perfect ordering.
- In code: updating α and checking the cutoff only when the best value improves is **not** a bug — if $v$ did not change, neither would $\max(\alpha, v)$ nor the test $v \ge \beta$ (this is how [[tic-tac-toe-4x4-py]] does it).

## Related

[[minimax]] · [[adversarial-search]] · [[monte-carlo-tree-search]] · [[iterative-deepening-search]] · [[depth-first-search]] · [[beam-search]] · [[game-search-comparison]] · [[chess-vs-go]] · [[tic-tac-toe-4x4-py]] · [[unit-04-games-review]]

## Practice questions

> [!question]- Q1. Run alpha-beta left to right on a MAX root with MIN children (5, 8, 7), (3, 9, 1), (6, 2, 10). Which leaves are pruned?
> **Answer.** First child: 5 → α = 5. Second child: 3 ≤ α → prune **9 and 1**. Third: 6 > 5 so continue, 2 ≤ α → prune **10**. Root = **5**. Three of nine leaves pruned.

> [!question]- Q2. Same tree as R&N Fig. 6.2 but with the children reordered: (2, 4, 6), (14, 5, 2), (3, 12, 8). What is pruned now?
> **Answer.** Nothing. α becomes 2 after the first child; the second child's leaves 14 and 5 are > 2 and only the last leaf (2) reaches α; the third child's leaves 3, 12, 8 never drop to ≤ 2 before the end. Root = 3 as before — same value, **zero** pruning. This is why move ordering matters ([[russell-norvig-aima]] §6.2.4).

> [!question]- Q3. Three-ply tree: MAX root → MIN₁, MIN₂ → each has two MAX nodes → two leaves each. Leaves MIN₁: (3, 5), (6, 9); MIN₂: (1, 2), (0, −1). Trace alpha-beta.
> **Answer.** MIN₁: first MAX child = max(3, 5) = 5, so β = 5 at MIN₁. Second MAX child sees 6 ≥ β = 5 → **prune 9**; it returns 6, MIN₁ = 5. Root α = 5. MIN₂: first MAX child = max(1, 2) = 2 (no cut since 2 < β = ∞), MIN₂ ≤ 2 ≤ α = 5 → **prune the whole second MAX child (leaves 0 and −1)**. Root = **5**.

> [!question]- Q4. What does "alpha-beta with perfect ordering searches twice as deep" mean numerically for chess?
> **Answer.** Nodes ≈ $b^{m/2} = (\sqrt b)^m$, so the effective branching factor drops from 35 to $\sqrt{35} \approx 5.9$. With the same budget $N = 35^{d}$ of minimax, alpha-beta reaches depth $2d$ ([[russell-norvig-aima]] §6.2.4).

> [!question]- Q5. What is a transposition table and why does it help alpha-beta?
> **Answer.** A cache (hash table) of positions already evaluated. In games different move orders often lead to the same position (transpositions), so storing the backed-up value avoids re-searching it; in chess it can double the reachable depth ([[russell-norvig-aima]] §6.2.4).

> [!question]- Q6. Why does alpha-beta alone not work well for Go?
> **Answer.** Branching factor starts at 361 (≈250 on average), so even with pruning the search reaches only 4-5 ply, and there is no good cheap evaluation function for the cutoff ([[russell-norvig-aima]] §6.4; [[chess-vs-go]]).
