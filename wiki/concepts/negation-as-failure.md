---
type: concept
summary: Prolog's \+ Goal succeeds when Goal cannot be proved; it equals logical negation only under the closed-world assumption, and is only safe on goals whose variables are already bound.
unit: [5, 6]
tags: [prolog, negation, closed-world-assumption, database-semantics]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]", "[[lab01-prolog-family-report]]"]
updated: 2026-10-01
---

# Negation as failure

`\+ Goal` succeeds exactly when Prolog **fails to prove** `Goal`. This is **negation as failure** (NAF). It matches logical negation only under the **closed-world assumption** (CWA): whatever cannot be derived is taken to be false ([[slides-xx-logic-programming-prolog]], slide 23). Pure [[horn-clauses]] cannot express a negative fact. "There is no way to assert that a sentence is false in Prolog" ([[russell-norvig-aima]] §9.4.4). NAF is how Prolog gets a usable kind of negation anyway.

## How it works

```prolog
\+ G:- call(G), !, fail. % if G is provable, \+ G fails
\+ _. % otherwise it succeeds
```

That two-clause definition is the classic textbook one and uses the [[prolog-cut|cut]] (general knowledge). `\+` never binds variables: if `G` succeeds, its bindings are discarded along with the failure.

**Database semantics** ([[russell-norvig-aima]] §8.2.8, §9.4.4; [[luger-ai-6e]] §14.3.2). Prolog's semantics rests on three assumptions:

| Assumption | Meaning | Luger's axiom |
|---|---|---|
| Unique names | distinct constants denote distinct objects | $a_i \neq a_j$ unless identical |
| Closed world | only entailed atoms are true | $p(X) \rightarrow p(a_1) \vee \dots \vee p(a_n)$ |
| Domain closure | the named constants are all the objects | $(X = a_1) \vee \dots \vee (X = a_n)$ |

R&N's example: `Course(CS,101), Course(CS,102), Course(CS,106), Course(EE,101)`. Under database semantics that means **exactly four** courses. In FOL it means "between one and infinity", and capturing the Prolog reading needs the **completion** $Course(d,n) \Leftrightarrow (d{=}CS \wedge n{=}101) \vee \dots$ ([[russell-norvig-aima]] §9.4.4).

**Safe use: bind first** ([[slides-xx-logic-programming-prolog]], slide 23):

```prolog
?- \+ parent(sofia, _).
true. % no children recorded for sofia
?- \+ parent(X, ana).
false. % some X does satisfy it
?- X = sofia, \+ parent(X, _).
X = sofia. % bind first, then negate
```

`\+ parent(X, ana)` does **not** mean "find an X who is not ana's parent". It means "it is not the case that anyone is ana's parent", which is false.

## Properties

- **Non-monotonic**: adding a fact can make a previously true `\+` query false (general knowledge).
- **Not classical negation**: "if a goal's truth value is actually unknown to the current database, Prolog will assume it to be false" ([[luger-ai-6e]] §14.3.2).
- **Floundering**: with unbound variables the answer depends on goal order (bind first).
- NAF makes Prolog "less expressive than first-order logic, but … more efficient and more concise" ([[russell-norvig-aima]] §9.4.4).
- Variants such as answer set programming extend Prolog with disjunction and negation ([[russell-norvig-aima]] Ch. 9 notes).

## In this course

- Slide 23: the definition, the CWA, the three queries above ([[slides-xx-logic-programming-prolog]], slide 23).
- Slide 13: `?- \+ parent(sofia, _).` gives `true`, "no children recorded for sofia".
- Slide 25: N-queens uses `\+ threat(Q, SafeQs)` with `Q` and `SafeQs` already bound by `select/3`, which is safe use ([[prolog-lecture-examples]]).
- Slide 28: "\\+ on unbound variables. Bind them first." is one of the classic mistakes.
- Lab 01, question 4: "What does the closed-world assumption claim that you never wrote down?" Raymond's answer: rosa and diego having no children, nobody called `stranger`, hector not being a mother. All of these are "proved" only by failure ([[lab01-prolog-family-report]]). His `reachable/3` uses `\+ memberchk(Z, Visited)` with `Z` bound, which is safe ([[lab01-family-pl]]).
- Negative plunit tests (`[fail]`) are NAF-style tests: they pass because something cannot be proved ([[lab01-family-pl]]).

## Common mistakes

- Negating an unbound goal and expecting a generator of "non-solutions".
- Reading a `false` answer as "proved false" rather than "not provable from this KB".
- Forgetting that a missing fact (a typo, a person left out of the file) silently becomes "false". Raymond's report: "If a person was missing from the file, Prolog would not say unknown. It would just say no." ([[lab01-prolog-family-report]]).

## Related

[[prolog]] · [[prolog-cut]] · [[first-order-logic]] · [[horn-clauses]] · [[lab01-family-pl]] · [[sld-resolution]]

## Practice questions

> [!question]- Q1. With slide 12's `family.pl`, predict `?- \+ parent(X, sofia).` and `?- X = diego, \+ parent(X, _).`
> **Answer.** The first is `false`, because `parent(ana, sofia)` exists, so the inner goal is provable. The second gives `X = diego`, since diego has no recorded children ([[slides-xx-logic-programming-prolog]], slide 23).

> [!question]- Q2. Spot the bug: `childless(X):- \+ parent(X, _), person(X).` and the query `?- childless(X).`
> **Answer.** `\+ parent(X, _)` runs with `X` unbound. Some parent exists, so it fails and the query returns no answers at all. Reorder as `childless(X):- person(X), \+ parent(X, _).` so that `X` is bound first ([[slides-xx-logic-programming-prolog]], slide 23).

> [!question]- Q3. Under the CWA and unique-names assumption, how many courses do `course(cs,101). course(cs,102). course(ee,101).` describe? And in plain FOL?
> **Answer.** Exactly three under database semantics. In FOL, anything from one to infinitely many: nothing says the constants are distinct or that no other courses exist ([[russell-norvig-aima]] §9.4.4).

> [!question]- Q4. Why is NAF non-monotonic? Give a lab example.
> **Answer.** `parent(rosa, _)` fails today, so the test `rosa_has_no_children` passes. Add `parent(rosa, pablo).` and the same query succeeds, so the earlier conclusion is withdrawn. Classical logic never loses conclusions when facts are added ([[lab01-family-pl]]).
