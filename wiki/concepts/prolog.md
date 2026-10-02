---
type: concept
summary: Prolog ("programmation en logique", Marseille 1972) — first-order Horn clauses plus depth-first backward chaining with unification; you state what holds, the interpreter searches for a proof.
unit: [5, 6]
tags: [prolog, logic-programming, swi-prolog, horn-clauses, declarative]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]", "[[slides-01-introduction-to-ai]]"]
updated: 2026-10-01
---

# Prolog

**Prolog** — *programmation en logique* — is the most widely used logic programming language. A program is a set of first-order [[horn-clauses|definite clauses]] (facts and rules); running it means asking a query, which the interpreter answers by [[sld-resolution]]: depth-first, left-to-right [[backward-chaining]] with [[unification]]. "You state what holds, not how to compute it. The interpreter searches for a proof; the answer is the substitution that made it work" ([[slides-xx-logic-programming-prolog]], slide 8). Kowalski's slogan **Algorithm = Logic + Control**: your clauses are the logic, Prolog supplies the control ([[slides-xx-logic-programming-prolog]], slide 2; [[russell-norvig-aima]] §9.4.2).

## How it works

### History

Born in **Marseille in 1972** ([[alain-colmerauer]] and Philippe Roussel), on theory from [[robert-kowalski]] in Edinburgh ([[slides-xx-logic-programming-prolog]], slide 8). Colmerauer built it to parse natural language; its clauses started out as context-free grammar rules. R&N place Kowalski's theoretical work at Imperial College London. Both are right, since Kowalski moved from Edinburgh to Imperial in the mid-1970s (general knowledge). Backward chaining itself came earlier, in Hewitt's PLANNER (1969), and efficient Prolog compilers use Warren's Abstract Machine (WAM, 1983) ([[russell-norvig-aima]] Ch. 9 bibliographical notes). Prolog became popular in Europe and Japan, and Japan's 1981 "Fifth Generation" project planned massively parallel computers running Prolog ([[russell-norvig-aima]] §1.3.4; see [[history-of-ai]]).

> [!warning] Contradiction
> [[slides-01-introduction-to-ai]] (slide 9) says Prolog was "created by Dennis Ritchie at Bell Labs" and is "an imperative, compiled language" — that describes **C**, not Prolog. The Prolog deck (slide 8) and R&N (Ch. 9 notes) agree: Colmerauer & Roussel, Marseille, 1972, with Kowalski's theory. Prolog is declarative. The Prolog deck is correct.

### From FOL to Prolog: four conventions ([[slides-xx-logic-programming-prolog]], slide 7)

1. Implication written backwards: $A \wedge B \Rightarrow C$ becomes `C:- A, B.`
2. Case inverted: **Uppercase = variable**, lowercase = constant (opposite of R&N's FOL).
3. Quantifiers implicit: every variable is universally quantified (per clause).
4. Punctuation: `,` = and, `;` = or, every clause ends with `.`

### Anatomy ([[slides-xx-logic-programming-prolog]], slide 12)

Everything is a **term**: atoms (`ana`, `'Ana María'`), numbers, variables (`X`, `_`, `Qs`), compound terms (`parent(hector, ana)`, `[1,2,3]`). A predicate is identified by **name/arity** — `father/2` is not `father/3`.

```prolog
% family.pl (slide 12)
parent(hector, ana). parent(hector, luis).
parent(ana, sofia). parent(luis, diego).
male(hector). male(luis). male(diego).
female(ana). female(sofia).

father(X, Y):- parent(X, Y), male(X).
grandparent(X, Z):- parent(X, Y), parent(Y, Z).
sibling(X, Y):- parent(P, X), parent(P, Y), X \= Y.
ancestor(X, Y):- parent(X, Y).
ancestor(X, Y):- parent(X, Z), ancestor(Z, Y).
```

### Queries ([[slides-xx-logic-programming-prolog]], slides 11, 13)

```prolog
?- parent(hector, Who).
Who = ana;
Who = luis.
?- grandparent(G, sofia).
G = hector;
false. % a choicepoint survived
?- findall(D, ancestor(hector, D), Ds).
Ds = [ana, luis, sofia, diego].
?- setof(P, C^parent(P, C), Parents).
Parents = [ana, hector, luis].
```

A predicate is a **relation, not a function**: one query can succeed once per solution; `;` asks for the next. `findall/3` keeps duplicates and returns `[]` on no solutions; `setof/3` sorts, deduplicates and *fails* on no solutions; `C^Goal` means "any C will do" (slide 13).

### Arithmetic ([[slides-xx-logic-programming-prolog]], slide 16)

| Operator | Meaning |
|---|---|
| `X = 3+4` | unify — `X` becomes the *term* `3+4` |
| `X is 3+4` | evaluate the right side, then unify — `X = 7`; right side must be bound |
| `=:=`, `=\=` | arithmetic equal / not equal (both sides evaluated) |
| `< > =< >=` | comparisons — note `=<`, never `<=` |
| `==` | term identity (no binding) |
| `\=` | not unifiable |

`?- X is Y + 1.` raises "Arguments are not sufficiently instantiated": arithmetic runs one way only. R&N: "`5 is X+Y` fails, because the built-in functions do not do arbitrary equation solving" ([[russell-norvig-aima]] §9.4.2).

### Lists ([[slides-xx-logic-programming-prolog]], slide 19)

A list is `[]` or `[Head|Tail]`; `[1,2,3]` is `[1|[2|[3|[]]]]`. Relations run backwards: `append(X, Y, [1,2,3])` enumerates all four splits ([[russell-norvig-aima]] §9.4.2 shows the same).

```prolog
mymember(X, [X|_]).
mymember(X, [_|T]):- mymember(X, T).
myappend([], L, L).
myappend([H|T], L, [H|R]):- myappend(T, L, R).
mylen([], 0).
mylen([_|T], N):- mylen(T, N0), N is N0 + 1.
```

### Built-ins worth memorising ([[slides-xx-logic-programming-prolog]], slide 24)

`findall/3`, `bagof/3`, `setof/3`, `aggregate_all(count, G, N)`, `forall(C, A)`, `between(L, H, X)`, `select(X, L, Rest)`, `permutation(L, P)`, `length(L, N)`, `msort/2`, `sort/2` (removes duplicates), `format/2`, `time/1`, `listing/1`, `make/0`.

### SWI-Prolog ([[slides-xx-logic-programming-prolog]], slides 9–11)

The course implementation (written against 9.2; 10.x is current). `swipl file.pl` loads a file; `?-` is the query prompt, `|:` means Prolog is reading clauses; `[user].` lets you type clauses; `consult('queens.pl')` or `[queens].` loads a file. Useful features: `trace/0` / `gtrace/0` debugger, `library(clpfd)`, tabling, SWISH in the browser. ISO covers the core (terms, control, arithmetic, `is/2`, `findall/3`); list, aggregation and I/O predicates are library and vary between implementations.

## Properties

- **Where it departs from logic** ([[russell-norvig-aima]] §9.4.2; [[luger-ai-6e]] §14.3.2):
  - database semantics: [[negation-as-failure]] under the closed-world and unique-names assumptions;
  - built-in arithmetic evaluated by code, not inference;
  - side-effecting built-ins (I/O, `assert/retract`);
  - **no occurs check** in [[unification]];
  - depth-first search with no loop check → incomplete; clause and goal order matter ([[sld-resolution]]);
  - the [[prolog-cut|cut]] prunes the search and breaks the declarative reading.
- **Expressiveness**: no disjunctive heads, no classical negation, so it is "less expressive than first-order logic" but more efficient and concise ([[russell-norvig-aima]] §9.4.4).
- **Uses**: expert systems, rule engines, legal/medical reasoning, NLP via definite clause grammars, compilers, program analysis, constraint problems ([[slides-xx-logic-programming-prolog]], slide 8; [[russell-norvig-aima]] §9.4.2).
- **CSPs**: standard Prolog solves finite-domain CSPs exactly like chronological [[csp-backtracking-search]]; constraint logic programming (`clpfd`) adds propagation ([[russell-norvig-aima]] §9.4.5). See the N-queens case study in [[prolog-lecture-examples]].

## In this course

- Taught in the Prolog deck, slides 2–31 ([[slides-xx-logic-programming-prolog]]); assessed in Lab 01 (slides 29–30), Raymond's submission: [[lab01-family-pl]] and [[lab01-prolog-family-report]].
- Lecture programs (factorial, Fibonacci, isEven, isPerm, BST, N-queens, predicates.pl): [[prolog-lecture-examples]].
- Reading list: R&N §7.5 and §9.4; Luger §14.2–14.3; Bratko; Sterling & Shapiro; learnprolognow.org; Triska's metalevel.at ([[slides-xx-logic-programming-prolog]], slide 31).

## Common mistakes

From [[slides-xx-logic-programming-prolog]], slide 28:

- A missing period: the clause merges with the next one.
- `=` instead of `is`: `X = 3+4` binds a term, not 7.
- Ignoring singleton-variable warnings (usually a typo, or should be `_`).
- Left recursion: a clause that calls itself before consuming anything loops.
- Uppercase where you meant an atom: `parent(Hector, ana)` means "some Hector".
- `\+` on unbound variables — bind first.
- Returning `true`/`false` atoms as outputs ("Java thinking"); in Prolog, succeeding *is* the answer (slide 20).

## Related

[[horn-clauses]] · [[backward-chaining]] · [[sld-resolution]] · [[unification]] · [[negation-as-failure]] · [[prolog-cut]] · [[first-order-logic]] · [[lab01-family-pl]] · [[prolog-lecture-examples]] · [[alain-colmerauer]] · [[robert-kowalski]] · [[unit-06-logic-prolog-review]]

## Practice questions

> [!question]- Q1. Translate to Prolog: $\forall x\ Missile(x) \Rightarrow Weapon(x)$ and $\forall x\ Enemy(x, America) \Rightarrow Hostile(x)$.
> **Answer.** `weapon(X):- missile(X).` and `hostile(X):- enemy(X, america).` — head first, uppercase variable, lowercase constant, implicit $\forall$ ([[slides-xx-logic-programming-prolog]], slide 7).

> [!question]- Q2. Predict the output: `?- X = 3 + 4, Y is X * 2.`
> **Answer.** `X = 3+4, Y = 14`. `=` binds `X` to the unevaluated term `3+4`; `is` then evaluates `(3+4)*2` ([[slides-xx-logic-programming-prolog]], slide 16).

> [!question]- Q3. Predict: `?- 3 + 4 = 7.`, `?- 3 + 4 =:= 7.`, `?- 1 + 2 == 2 + 1.`
> **Answer.** `false` (different structures), `true` (values compared), `false` (`==` is term identity; the terms differ) ([[slides-xx-logic-programming-prolog]], slide 16).

> [!question]- Q4. With slide 12's `family.pl`, how many answers does `?- sibling(ana, S).` give, and what would they be if hector had two `parent/2` children with carmen too?
> **Answer.** One: `S = luis` (via `parent(hector, _)`). If carmen were also recorded as parent of both, `S = luis` would come back **twice** — once through each shared parent — the duplicate-answers point of Lab 01 ([[lab01-prolog-family-report]]).

> [!question]- Q5. `findall(X, parent(sofia, X), L)` vs `setof(X, parent(sofia, X), L)` on slide 12's KB?
> **Answer.** `findall` gives `L = []`; `setof` **fails** (`false`) because it has no solutions ([[slides-xx-logic-programming-prolog]], slide 13).

> [!question]- Q6. Spot the bug: `grandparent(X, Z):- parent(X, Y), parent(y, Z).`
> **Answer.** Lowercase `y` is an atom, not the variable `Y`, so it asks whether the constant `y` is a parent of `Z`. SWI-Prolog would also warn that `Y` is a singleton ([[slides-xx-logic-programming-prolog]], slide 28).
