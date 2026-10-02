---
type: concept
summary: The cut (!) commits Prolog to the choices made so far in a clause — no retrying goals to its left, no later clauses for that predicate; it buys speed but breaks the declarative reading (the max/3 bug); prefer if-then-else.
unit: [5, 6]
tags: [prolog, cut, control, backtracking, pitfalls]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# The cut (`!`)

The **cut**, written `!`, is a goal that always succeeds and, as a side effect, **commits** to the choices made so far in the current clause. Prolog will not retry the goals to its left, and will not try any later clause of the same predicate ([[slides-xx-logic-programming-prolog]], slide 23). It is pure control, Kowalski's "Control" half of Algorithm = Logic + Control. It has no logical meaning. "It buys speed but destroys the declarative reading. Prefer `( Cond -> Then; Else )`." ([[slides-xx-logic-programming-prolog]], slide 23).

## How it works

When a clause `h:- a, b, !, c, d.` is used for a goal:

- Before the cut, `a` and `b` can backtrack normally.
- Executing `!` throws away the choicepoints of `a`, `b`, and the alternative clauses for `h`.
- If `c` or `d` later fails, the **whole call to `h` fails**; nothing to the left is retried.

Luger: "The interpreter, when encountering the cut, is committed to the current execution path … Should failure be encountered within the clause after the cut, the entire clause fails … cut can mean that only some of the possible interpretations of the model are ever computed" ([[luger-ai-6e]] §14.3.2).

### The `max/3` bug ([[slides-xx-logic-programming-prolog]], slide 23)

```prolog
% WRONG: the output sits in the head
max(X, Y, X):- X >= Y, !.
max(_, Y, Y).

?- max(5, 3, 3).
true. % WRONG
```

The call `max(5, 3, 3)` does not unify with the first head (`X = 5` but the third argument would have to be 5 too). So the cut is never reached, and the second clause says "the max is Y = 3". The second clause is only correct *if* the first one was tried and cut, and a partially bound call skips that. Checked in SWI-Prolog: `true`.

```prolog
% right: unify the output only after the cut
max(X, Y, M):- X >= Y, !, M = X.
max(_, Y, Y).

% better: no cut at all
max2(X, Y, M):- ( X >= Y -> M = X; M = Y ).
```

### Green vs red cuts (general knowledge)

- **Green cut**: removes only choicepoints that could never lead to more solutions. Deleting it doesn't change the answers, only efficiency (e.g. a `!` after `A > 0` in a clause whose alternative requires `A =:= 0`).
- **Red cut**: the program's meaning *depends* on it, as in the `max/3` second clause, which is wrong in isolation. Red cuts are what "destroy the declarative reading".

### Cut and negation

`\+ G` can be defined with a cut: `\+ G:- call(G), !, fail.` `\+ _.` ([[negation-as-failure]]; general knowledge).

## Properties

- **Efficiency**: frees backtrack pointers and prunes the search ([[luger-ai-6e]] §14.3.2).
- **Completeness**: a cut can prune branches that contain solutions. Luger's completeness claim for the resolution-based interpreter holds "provided that part of the set of interpretations is not pruned away by using cut" ([[luger-ai-6e]] §14.3.2).
- **Order-dependent**: a program with cuts no longer has the same meaning if clauses are reordered.
- Luger lists the cut, negation as failure and the missing occurs check as Prolog's departures from logic-programming semantics ([[luger-ai-6e]] §14.3.2).

## In this course

- Slide 23 introduces cut together with [[negation-as-failure]] and the `max/3` example ([[slides-xx-logic-programming-prolog]], slide 23).
- Slide 17: `factorial(5, X)` answers `X = 120; false.` A choicepoint survives because the two clauses are tried in turn. A green cut or `->` would remove it ([[slides-xx-logic-programming-prolog]], slide 17; [[prolog-lecture-examples]]).
- Slide 29: the plunit example uses `mother(rosa, ana), !.` inside a test to drop extra solutions. Raymond's [[lab01-family-pl]] uses `once/1` for the same purpose; `once(G)` behaves like `(G, !)` (general knowledge).

## Common mistakes

- Putting output arguments in the head of a cut clause (the `max/3` bug).
- Using cut to "fix" duplicate answers whose real cause is the logic, such as two parents or many paths. `once/1`, `setof/3` or a better rule is cleaner.
- Cutting before all tests are done: `p(X):- !, X > 0.` commits even when `X > 0` will fail.

## Related

[[prolog]] · [[negation-as-failure]] · [[sld-resolution]] · [[backward-chaining]] · [[prolog-lecture-examples]]

## Practice questions

> [!question]- Q1. With the buggy `max/3`, predict `?- max(3, 5, M).` and `?- max(5, 3, M).` and `?- max(5, 3, 3).`
> **Answer.** `M = 5` (the first clause fails at `3 >= 5`, the second gives `Y`). `M = 5` (the first clause succeeds and cuts). `true`, which is wrong: the first head does not unify, so the cut is never reached and the second clause answers ([[slides-xx-logic-programming-prolog]], slide 23; checked in SWI-Prolog).

> [!question]- Q2. Given `p(1). p(2). p(3).` and `q(X):- p(X), !.`, what does `?- q(X).` return, including after `;`?
> **Answer.** `X = 1.` and nothing more. The cut discards `p/1`'s remaining choicepoints.

> [!question]- Q3. Given `r(X):- p(X), !, X > 1.` with the same `p/1`, what is `?- r(X).`?
> **Answer.** `false`. `p(X)` binds `X = 1`, the cut commits, `1 > 1` fails, and because of the cut Prolog does not go back to try `X = 2`.

> [!question]- Q4. Rewrite `max/3` without a cut and explain why it is safer.
> **Answer.** `max(X, Y, M):- ( X >= Y -> M = X; M = Y ).` The condition and both branches are in one clause, so no clause depends on another having been cut, and partially bound calls like `max(5,3,3)` correctly fail ([[slides-xx-logic-programming-prolog]], slide 23).

> [!question]- Q5. Green or red: `sign(X, pos):- X > 0, !. sign(X, zero):- X =:= 0, !. sign(X, neg):- X < 0.`
> **Answer.** Green. Each clause tests its own condition, so removing the cuts changes no answers. The cuts only avoid useless retries (general knowledge).
