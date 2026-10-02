---
type: concept
summary: Goal-directed inference for definite clauses — start from the query, find rules whose head matches, prove their bodies recursively; a depth-first AND–OR search that is Prolog's execution model.
unit: [5, 6]
tags: [logic, inference, backward-chaining, goal-directed, prolog, and-or-search]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Backward chaining

**Backward chaining** works from the query back to the facts: to prove a goal, find a clause whose head matches it, then prove every literal of that clause's body the same way, until everything bottoms out in facts ([[russell-norvig-aima]] §7.5.4, §9.4). It is **goal-directed** reasoning and only touches facts relevant to the query. The slides summarise: "From the query, prove the body of any matching clause; recurse to the facts, depth first, left to right. Only facts relevant to the query are touched, and space is linear in the size of the proof" ([[slides-xx-logic-programming-prolog]], slide 6). With [[unification]] and a fixed search order it is exactly how [[prolog]] runs ([[sld-resolution]]).

## How it works

**FOL-BC-ASK** ([[russell-norvig-aima]] Fig. 9.6) is a *generator* — it can yield many substitutions, one per proof:

```
FOL-BC-OR(KB, goal, θ):
    for each rule (lhs ⇒ rhs) in FETCH-RULES-FOR-GOAL(KB, goal):
        standardize variables apart
        for each θ' in FOL-BC-AND(KB, lhs, UNIFY(rhs, goal, θ)):
            yield θ'

FOL-BC-AND(KB, goals, θ):
    if θ = failure: return
    if goals empty: yield θ
    else for each θ' in FOL-BC-OR(KB, SUBST(θ, first(goals)), θ):
             for each θ'' in FOL-BC-AND(KB, rest(goals), θ'):
                 yield θ''
```

It is an **AND–OR search**: OR over the alternative clauses for a goal, AND over the conjuncts of a body ([[russell-norvig-aima]] §9.4.1). Bindings found by one conjunct are applied to the later ones.

**Proof of Criminal(West)** (R&N Fig. 9.7; [[slides-xx-logic-programming-prolog]], slide 6). In Prolog form:

```prolog
criminal(X):- american(X), weapon(Y), sells(X, Y, Z), hostile(Z).
weapon(X):- missile(X).
hostile(X):- enemy(X, america).
sells(west, X, nono):- missile(X), owns(nono, X).
american(west). missile(m1).
owns(nono, m1). enemy(nono, america).
```

```
criminal(west)
├── american(west) fact { }
├── weapon(Y) → missile(Y) fact {Y/m1}
├── sells(west, m1, Z) → missile(m1), owns(nono, m1) {Z/nono}
└── hostile(nono) → enemy(nono, america) fact { }
```

By the time the last conjunct is reached, `Z` is already bound to `nono` ([[russell-norvig-aima]] Fig. 9.7 caption).

## Properties

| Property | Value |
|---|---|
| Sound | Yes |
| Space | Linear in the size of the proof (depth-first) ([[russell-norvig-aima]] §9.4.1) |
| Time | Propositional: linear with an efficient implementation, often *much less* since only relevant facts are touched ([[russell-norvig-aima]] §7.5.4) |
| Complete? | Depth-first version: **no** — infinite loops on repeated states / left recursion, even for Datalog ([[russell-norvig-aima]] §9.4.3) |
| Redundancy | Re-proves the same subgoals; can be exponential (877 vs 62 inferences on R&N Fig. 9.8b) |
| Fixes | Loop checking; **tabling / memoisation** (complete for Datalog) ([[russell-norvig-aima]] §9.4.3; [[slides-xx-logic-programming-prolog]], slide 15) |

It is the logical twin of [[depth-first-search]]: linear memory, but incomplete on infinite or cyclic spaces. R&N notes it is "essentially identical to the AND-OR-GRAPH-SEARCH algorithm" of Ch. 4 ([[russell-norvig-aima]] §7.5.4).

## In this course

- Slide 5: "Inference is by chaining. Forward, from facts to query; backward, from query to facts" and the AND–OR graph that "Prolog explores … depth first, left to right" ([[slides-xx-logic-programming-prolog]], slide 5).
- Slide 6: the Criminal(West) proof tree ([[slides-xx-logic-programming-prolog]], slide 6).
- Slide 15: Prolog's version, SLD resolution, and the left-recursion example (`path/2`) — see [[sld-resolution]].
- Slide 28: `trace/0` shows backward chaining step by step as Call / Exit / Redo / Fail ports ([[slides-xx-logic-programming-prolog]], slide 28).
- In [[lab01-family-pl]], every query (`uncle(U, lucia)`, `related(juan, valentina)`) is answered by backward chaining; the visited list in `reachable/3` is a hand-written loop check.

## Common mistakes

- Assuming backward chaining always terminates — it does not on left-recursive or cyclic rules.
- Forgetting that bindings propagate *left to right*: the order of body goals changes efficiency and sometimes termination ([[luger-ai-6e]] §14.3.1 calls goal order "heuristic information").
- Treating multiple identical answers as a bug in the logic; they are separate proofs ([[lab01-prolog-family-report]]).

## Related

[[forward-chaining]] · [[sld-resolution]] · [[prolog]] · [[unification]] · [[horn-clauses]] · [[depth-first-search]] · [[logic-systems-comparison]]

## Practice questions

> [!question]- Q1. Trace backward chaining for query $Q$ on R&N Fig. 7.16 ($P \Rightarrow Q$, $L \wedge M \Rightarrow P$, $B \wedge L \Rightarrow M$, $A \wedge P \Rightarrow L$, $A \wedge B \Rightarrow L$, $A$, $B$), with a loop check.
> **Answer.** $Q$ ← $P$ ← $L \wedge M$. Prove $L$: try $A \wedge P \Rightarrow L$; $A$ is a fact, but $P$ is already on the goal stack → loop check fails this branch. Try $A \wedge B \Rightarrow L$: both facts ✓. Prove $M$ ← $B \wedge L$: $B$ ✓, $L$ ✓ (as before). So $P$ ✓, $Q$ ✓.

> [!question]- Q2. Same KB written as Prolog in the textbook's order (`l:- a, p.` before `l:- a, b.`). What does `?- q.` do?
> **Answer.** It loops: `q → p → l → (a, p) → p → l → …`, because Prolog has no loop check and tries `l:- a, p` first. Checked in SWI-Prolog: the query exceeds a 100,000-inference limit. Swapping the two `l` clauses makes it answer `true` ([[russell-norvig-aima]] §9.4.3; [[slides-xx-logic-programming-prolog]], slide 15).

> [!question]- Q3. Why is backward chaining's space linear but its time potentially exponential?
> **Answer.** Depth-first keeps only the current proof path (plus choicepoints), so space is linear in proof size. Without caching, the same subgoals are re-proved on every branch, so time can be exponential in the number of facts ([[russell-norvig-aima]] §9.4.1, §9.4.3).

> [!question]- Q4. In the Prolog `criminal/1` clause, why does `sells(X, Y, Z)` already have `Y` bound when it is called?
> **Answer.** Goals run left to right and bindings are applied to later goals; `weapon(Y)` ran first and bound `Y = m1` via `missile(m1)` ([[russell-norvig-aima]] Fig. 9.7).

> [!question]- Q5. When would you prefer backward over forward chaining?
> **Answer.** When you have a specific question ("Is West a criminal?", "Where are my keys?") and a large KB: backward chaining only touches relevant facts ([[russell-norvig-aima]] §7.5.4).
