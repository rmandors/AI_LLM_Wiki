---
type: concept
summary: Prolog's execution strategy — resolve the leftmost goal against clauses in file order, depth first with backtracking; SLD resolution is complete for definite clauses but Prolog's fixed search rule is not, so clause and goal order matter (left recursion loops; tabling fixes it).
unit: [5, 6]
tags: [prolog, sld-resolution, backtracking, left-recursion, tabling, search]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# SLD resolution

**SLD resolution** (Selective Linear Definite-clause resolution) is resolution restricted to [[horn-clauses|definite clauses]]: a goal list is repeatedly reduced by resolving one selected goal against a program clause. [[prolog]] fixes the two free choices — always select the **leftmost** goal, and try clauses in **file order**, depth first with backtracking. The slides define it as "depth-first [[backward-chaining]] with [[unification]]" ([[slides-xx-logic-programming-prolog]], slide 15). The name expansion is general knowledge; the course uses only the acronym.

## How it works

Prolog's loop ([[slides-xx-logic-programming-prolog]], slide 15):

1. Take the leftmost goal.
2. Scan the clauses in file order for a head that unifies with it.
3. Replace the goal by that clause's body (with the unifier applied to the whole goal list).
4. On failure, **backtrack**: undo bindings back to the latest choicepoint and try the next clause.
5. Succeed when no goals remain. The composed substitution is the answer.

Luger writes the same thing as goal-list rewriting. Given goal $\leftarrow a_1 \wedge a_2 \wedge \dots \wedge a_n$ and the first clause $a_1 \leftarrow b_1 \wedge \dots \wedge b_n$ that unifies with $a_1$ (unifier $\xi$), the new goal is $\leftarrow (b_1 \wedge \dots \wedge b_n \wedge a_2 \wedge \dots \wedge a_n)\xi$. "The goal list is treated as a stack enforcing depth-first search" ([[luger-ai-6e]] §14.3.2). Pure logic programming allows *any* goal and *any* clause to be chosen nondeterministically. Sequential Prolog is an ordered approximation of that ([[luger-ai-6e]] §14.3.2).

### Same logic, different fate ([[slides-xx-logic-programming-prolog]], slide 15; [[russell-norvig-aima]] §9.4.3)

```prolog
link(a, b). link(b, c).

% base case first: an answer comes back
path(X, Z):- link(X, Z).
path(X, Z):- path(X, Y), link(Y, Z).
% ?- path(a, c). true. (but; still loops)

% left recursion first: no answer at all
path(X, Z):- path(X, Y), link(Y, Z).
path(X, Z):- link(X, Z).
% ?- path(a, c). ERROR: Stack limit (1.0Gb) exceeded
```

With left recursion first, `path(a,c)` calls `path(a,Y)`, which calls `path(a,Y')`, and so on, never reaching a fact (R&N Fig. 9.9b). In the first version the answer is found, but asking for more (`;`) re-enters the recursive clause and loops.

### Fixes

- **Tabling**: `:- table path/2.` memoises subgoals and answers, so `path/2` terminates in either order. It combines the goal-directedness of backward chaining with the dynamic-programming efficiency of [[forward-chaining]] and is complete for Datalog ([[slides-xx-logic-programming-prolog]], slides 9, 15; [[russell-norvig-aima]] §9.4.3).
- **Right recursion** (`path(X,Z):- link(X,Y), path(Y,Z).`) consumes a link before recursing. That terminates on acyclic graphs but still loops on cycles (general knowledge).
- **Visited list**: carry the nodes already seen, as `reachable/3` does in [[lab01-family-pl]].

## Properties

| Aspect | SLD resolution (the inference rule) | Prolog's search rule |
|---|---|---|
| Soundness | Sound (with occurs check) | Sound in practice; no occurs check |
| Completeness | Refutation-complete for definite clauses | **Incomplete**: depth-first can follow an infinite branch |
| Memory | — | Linear in the depth of the proof |
| Order sensitivity | None (logically) | Clause order and goal order change termination, answer order and cost |

"SLD resolution is complete; Prolog's search rule is not" ([[slides-xx-logic-programming-prolog]], slide 15). R&N: Prolog is "incomplete as a theorem prover for definite clauses — even for Datalog programs" ([[russell-norvig-aima]] §9.4.3). Luger: with well-founded recursion and occurs checking, left-to-right depth-first goal reduction does find refutations when they exist ([[luger-ai-6e]] §14.3.2, citing van Emden & Kowalski 1976). The [[prolog-cut|cut]] can prune away solutions.

**Redundant work**: on R&N Fig. 9.8(b), depth-first backward chaining takes 877 inferences against 62 for forward chaining, because it keeps re-proving dead subgoals ([[russell-norvig-aima]] §9.4.3). The naive Fibonacci in [[prolog-lecture-examples]] shows the same thing: `fibo(25, _)` takes about 1.09 million inferences ([[slides-xx-logic-programming-prolog]], slide 18).

**Search view**: the SLD tree is an OR-tree of clause choices. Prolog does [[depth-first-search]] on it, with chronological backtracking. N-queens in Prolog is literally [[csp-backtracking-search]] ([[russell-norvig-aima]] §9.4.5).

## In this course

- Slide 15: the algorithm, the `path/2` example, and the tabling fix ([[slides-xx-logic-programming-prolog]], slide 15).
- Slide 17: `A > 0` and `C is A - 1` must come before the recursive call in `factorial/2`, because goal order matters for `is/2` ([[slides-xx-logic-programming-prolog]], slide 17).
- Slide 27: generate-and-test vs test-as-you-go N-queens. Same logic with a different goal order, and up to 77× fewer inferences at N = 10 ([[slides-xx-logic-programming-prolog]], slide 27).
- Slide 28: the `trace/0` four-port debugger shows the SLD steps (Call, Exit, Redo, Fail).
- Slide 29 (bonus): a naive `related/2` "walks up a parent link and straight back down it, forever"; [[lab01-family-pl]] fixes it with a visited list.

## Common mistakes

- Believing logically equivalent programs behave the same. In Prolog they need not.
- Putting the recursive call first ("left recursion") in transitive-closure rules.
- Putting an `is/2` goal before its inputs are bound.
- Thinking a final `false` after an answer means the query failed. It only means a leftover choicepoint found nothing more.

## Related

[[backward-chaining]] · [[prolog]] · [[unification]] · [[horn-clauses]] · [[depth-first-search]] · [[csp-backtracking-search]] · [[prolog-cut]] · [[negation-as-failure]] · [[conjunctive-normal-form-and-resolution]]

## Practice questions

> [!question]- Q1. List the five steps Prolog uses to answer a query.
> **Answer.** Take the leftmost goal; scan clauses in file order for a unifying head; replace the goal by that clause's body; on failure, backtrack (undo bindings, try the next clause); succeed when no goals remain ([[slides-xx-logic-programming-prolog]], slide 15).

> [!question]- Q2. Predict: with `path(X,Z):- path(X,Y), link(Y,Z).` as the *first* clause, what does `?- path(a, c).` do? How do you fix it without reordering?
> **Answer.** It recurses on `path(a, _)` forever and ends with a stack-limit error. Add `:- table path/2.` to memoise subgoals. It then terminates and returns `true` ([[slides-xx-logic-programming-prolog]], slide 15).

> [!question]- Q3. Explain "SLD resolution is complete; Prolog's search rule is not".
> **Answer.** If a refutation exists, some sequence of SLD steps finds it. Prolog commits to depth-first, file-order exploration, though, and can descend an infinite branch before reaching the finite proof on another branch ([[russell-norvig-aima]] §9.4.3).

> [!question]- Q4. Give the goal list after one step: goal `?- grandparent(hector, Z).`, clause `grandparent(X, Z1):- parent(X, Y), parent(Y, Z1).`
> **Answer.** Unifier $\{X/hector, Z1/Z\}$. New goal list: `parent(hector, Y), parent(Y, Z)`. The next step resolves `parent(hector, Y)` against the first matching fact ([[luger-ai-6e]] §14.3.2).

> [!question]- Q5. Why does tabling help naive `fibo/2` as well as `path/2`?
> **Answer.** Both re-prove identical subgoals. Tabling stores each answered subgoal (`fibo(23, _)` and so on), so each is solved once. That turns exponential work into linear for Fibonacci and stops the infinite regress for `path/2` ([[slides-xx-logic-programming-prolog]], slide 18).
