---
type: exam-review
summary: Unit 5–6 cheat sheet — propositional and first-order logic, CNF and resolution, Horn clauses, forward/backward chaining, unification, Prolog syntax and execution (SLD), arithmetic, NAF, cut, Lab 01 — with 14 practice questions.
unit: [5, 6]
tags: [exam-review, logic, prolog, unification, chaining, cheat-sheet]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]", "[[lab01-prolog-family-report]]"]
updated: 2026-10-01
---

# Unit 6 review — Logic and Prolog

Covers [[slides-xx-logic-programming-prolog]] (all 31 slides), R&N §7.3–7.5, Ch. 8, §9.1–9.4 ([[russell-norvig-aima]]), Luger §14.2–14.3 ([[luger-ai-6e]]), and Lab 01 ([[lab01-family-pl]], [[lab01-prolog-family-report]]).

## The ladder (slide 2)

| Step | Adds | Price |
|---|---|---|
| [[propositional-logic]] | connectives, truth tables | no objects, no "every" |
| [[first-order-logic]] | objects, predicates, functions, ∀, ∃ | semidecidable |
| [[horn-clauses]] | ≤ 1 positive literal | no disjunction, no negative facts |
| [[prolog]] | depth-first backward chaining + unification + built-ins | incomplete search, closed world, no occurs check |

**Algorithm = Logic + Control** ([[robert-kowalski]], 1979). Prolog: Marseille 1972, [[alain-colmerauer]] & Roussel. *Not* Ritchie/Bell Labs, which is C; Slides 01 slide 9 is wrong ([[slides-01-introduction-to-ai]]).

## Definitions to know cold

- **Entailment** $\alpha \models \beta$ iff $M(\alpha) \subseteq M(\beta)$. **Valid** = true in all models. **Satisfiable** = true in some model.
- $\alpha \models \beta$ iff $\alpha \Rightarrow \beta$ is valid (deduction theorem) iff $\alpha \wedge \neg\beta$ is unsatisfiable (refutation).
- **Sound** = derives only entailed sentences. **Complete** = derives all of them.
- **Literal / clause / CNF**: symbol or negated symbol / disjunction of literals / conjunction of clauses.
- **Horn** ≤ 1 positive literal. **Definite** = exactly 1 (rule; a **fact** has an empty body). **Goal clause** = 0 (a query).
- **Unifier** θ: SUBST(θ,p) = SUBST(θ,q). **MGU** = most general such θ (unique up to renaming). **Occurs check**: never bind X to a term containing X.
- **Generalized Modus Ponens**: from $p_1', \dots, p_n'$ and $(p_1 \wedge \dots \wedge p_n \Rightarrow q)$ with SUBST(θ, $p_i'$) = SUBST(θ, $p_i$), infer SUBST(θ, q).
- **Database semantics**: unique names + closed world + domain closure.
- **SLD resolution**: leftmost goal, clauses in file order, depth first, backtrack on failure.

## Conversions

**CNF (propositional):** (1) $\Leftrightarrow$ → two $\Rightarrow$; (2) $\alpha \Rightarrow \beta$ → $\neg\alpha \vee \beta$; (3) push ¬ in (De Morgan, double negation); (4) distribute ∨ over ∧.
**FOL extra steps:** standardize variables apart, **Skolemize** (∃ inside ∀x becomes $F(x)$), drop ∀. Luger has 9 steps.
**FOL → Prolog:** head first (`C:- A, B.`), Uppercase = variable, ∀ implicit, `,` and, `;` or, `.` end.

## Prolog operators (slide 16)

| | meaning | example |
|---|---|---|
| `=` | unify | `X = 3+4` → `X = 3+4` |
| `is` | evaluate RHS (must be bound), unify | `X is 3+4` → `7` |
| `=:=` `=\=` | arithmetic equal / not | `3+4 =:= 7` → true |
| `==` | identical terms | `1+2 == 2+1` → false |
| `\=` | not unifiable | `a \= b` → true |
| `< > =< >=` | compare numbers | `=<`, never `<=` |
| `\+ G` | NAF: G not provable | bind variables first |
| `!` | commit; no retry left, no later clause | `max/3` bug |

`findall/3` keeps duplicates and returns `[]` when nothing matches. `setof/3` sorts, dedups and **fails** when nothing matches; `V^G` means "any V".

## Complexity / properties table

| Method | Sound | Complete | Cost |
|---|---|---|---|
| Truth table (TT-ENTAILS?) | ✓ | ✓ | $O(2^n)$ time, $O(n)$ space |
| Propositional resolution | ✓ | refutation-complete | exponential worst case |
| Forward chaining (definite) | ✓ | ✓ | linear (propositional); FOL Datalog ≤ $p n^k$ facts |
| Backward chaining (depth-first) | ✓ | ✗ (loops) | linear space |
| Prolog | ~✓ (no occurs check) | ✗ | clause/goal order matters |
| Tabled Prolog | ✓ | ✓ for Datalog | memo table |
| FOL entailment in general | — | semidecidable | — |

## Must-know facts

- Propositional entailment is co-NP-complete; SAT was the first NP-complete problem ([[russell-norvig-aima]] §7.4.4–7.5).
- Horn clauses are closed under resolution; propositional Horn entailment is linear ([[russell-norvig-aima]] §7.5.3).
- $P \vee Q$ has no Horn form ([[slides-xx-logic-programming-prolog]], slide 4).
- Prolog runs **depth first, left to right**. Logically identical programs can differ in termination. Left recursion → stack overflow; `:- table p/2.` fixes it ([[sld-resolution]]).
- `X = f(X)` succeeds in SWI-Prolog (cyclic term); `unify_with_occurs_check(X, f(X))` fails.
- `is/2` runs one way: `X is Y + 1` with Y unbound gives an instantiation error. `factorial(X, 120)` errors for the same reason.
- `\+` is safe only on bound goals. `\+ parent(X, ana)` is `false`, not "find a non-parent".
- Cut: green (efficiency only) vs red (changes meaning). The slide's `max(X,Y,X):- X >= Y, !.` gives `max(5,3,3)` = true.
- Naive `fibo(25)` takes ~1.09 M inferences; an accumulator or tabling makes it linear ([[prolog-lecture-examples]]).
- N-queens in Prolog = chronological [[csp-backtracking-search]]. Test-as-you-go beats generate-and-test by 17× at N = 8 and 77× at N = 10. There are 92 solutions for N = 8 (slides 26–27).
- Lab 01: `sibling/2` needs `X \= Y` (placed last); duplicates come from multiple proofs; the CWA makes "no fact" mean "false" ([[lab01-prolog-family-report]]).

## Common traps

1. ∀ with ∧ / ∃ with ⇒.
2. Confusing "Horn" (≤ 1 positive) with "definite" (exactly 1).
3. Resolving two complementary pairs at once.
4. Skolem *constant* where a Skolem *function* is needed.
5. `=` vs `is` vs `=:=` vs `==`.
6. Uppercase atoms (`Hector` is a variable), missing periods, singleton warnings.
7. `\+` or `\=` before the variables are bound.
8. Reading the final `false` after `X = 120;` as failure. It only means no more answers.
9. Assuming backward chaining always terminates.

## Practice questions

> [!question]- Q1. Convert $P \Leftrightarrow (Q \wedge R)$ to CNF and say which clauses are Horn.
> **Answer.** $(P \Rightarrow Q \wedge R) \wedge (Q \wedge R \Rightarrow P)$ → $(\neg P \vee (Q \wedge R)) \wedge (\neg Q \vee \neg R \vee P)$ → $(\neg P \vee Q) \wedge (\neg P \vee R) \wedge (\neg Q \vee \neg R \vee P)$. All three have exactly one positive literal, so all are definite: `q:- p.` `r:- p.` `p:- q, r.`

> [!question]- Q2. Classify: $\neg A \vee B$, $A \vee B$, $\neg A \vee \neg B$, $C$.
> **Answer.** Definite (rule $A \Rightarrow B$); not Horn; goal clause; fact ([[horn-clauses]]).

> [!question]- Q3. Give the MGU of `p(X, f(Y), b)` and `p(a, f(Z), Z)`.
> **Answer.** $X/a$; `f(Y) = f(Z)` gives $Y/Z$; `b = Z` gives $Z/b$, so $Y/b$. MGU $= \{X/a, Y/b, Z/b\}$ ([[unification]]).

> [!question]- Q4. Do `q(X, X)` and `q(Y, f(Y))` unify?
> **Answer.** $X/Y$, then $Y = f(Y)$, which fails the occurs check. In plain Prolog `=` it "succeeds" with a cyclic term ([[unification]]).

> [!question]- Q5. Forward chaining on: $A$, $B$, $A \wedge B \Rightarrow C$, $C \Rightarrow D$, $D \wedge E \Rightarrow F$. Which symbols are inferred? Is $F$ entailed?
> **Answer.** $C$, then $D$. $F$ needs $E$, which is never derived, so the fixed point is $\{A, B, C, D\}$ and $F$ is not entailed ([[forward-chaining]]).

> [!question]- Q6. Trace Prolog on the West KB: in what order are the subgoals of `criminal(west)` solved, and with what bindings?
> **Answer.** `american(west)` (fact) → `weapon(Y)` → `missile(Y)` with `Y = m1` → `sells(west, m1, Z)` via `sells(west, X, nono):- missile(X), owns(nono, X)` with `Z = nono` → `hostile(nono)` → `enemy(nono, america)`. Result: `true` ([[backward-chaining]]; R&N Fig. 9.7).

> [!question]- Q7. Predict each: `?- X = 2 + 3.` `?- X is 2 + 3.` `?- 2 + 3 =:= 5.` `?- 2 + 3 == 5.` `?- X is Y * 2.`
> **Answer.** `X = 2+3`; `X = 5`; `true`; `false`; instantiation error ([[prolog]]).

> [!question]- Q8. Predict: `?- findall(X, member(X, [b,a,b]), L).` and `?- setof(X, member(X, [b,a,b]), L).` and `?- setof(X, member(X, []), L).`
> **Answer.** `L = [b,a,b]`; `L = [a,b]`; `false` ([[slides-xx-logic-programming-prolog]], slide 13).

> [!question]- Q9. Why does `path(X,Z):- path(X,Y), link(Y,Z).` placed first make `?- path(a,c).` crash, and give two fixes.
> **Answer.** The leftmost goal `path(a, Y)` calls the same clause again before consuming any `link`, so the recursion never ends. Fixes: put the base case first and recurse on the right (`link(X,Y), path(Y,Z)`), or add `:- table path/2.` ([[sld-resolution]]).

> [!question]- Q10. Spot the bug: `max(X, Y, X):- X >= Y, !.` / `max(_, Y, Y).`
> **Answer.** `max(5, 3, 3)` is true. The first head doesn't unify (the third argument should be 5), so the cut is never reached and the second clause answers. Fix: `max(X, Y, M):- X >= Y, !, M = X.` or use `( X >= Y -> M = X; M = Y )` ([[prolog-cut]]).

> [!question]- Q11. With slide 12's family KB, predict `?- \+ parent(X, ana).` and `?- X = sofia, \+ parent(X, _).`
> **Answer.** `false` (hector is a parent of ana); `X = sofia` (no children recorded). Bind first, then negate ([[negation-as-failure]]).

> [!question]- Q12. In Lab 01, why does `sibling/2` need `X \= Y`, and why does the one-parent version return `sibling(ana, luis)` twice?
> **Answer.** Without it, everyone is their own sibling (they share a parent with themselves). With `parent(P,X), parent(P,Y)`, P can be hector or carmen, which gives two proofs of the same pair. Raymond's same-father-and-mother version returns each pair once but excludes half-siblings ([[lab01-family-pl]]).

> [!question]- Q13. What does `isMerged([1,a,2,b], A, B)` from `predicates.pl` return first, and what does the predicate mean?
> **Answer.** First answer `A = [], B = [1,a,2,b]` (clause 2: L2 empty, so L1 = L3). The predicate holds when L1 is the alternating interleave of L2 and L3, starting with L2, with the leftover appended. It returns 7 answers in total, including `[1,2]/[a,b]` three times ([[prolog-lecture-examples]]).

> [!question]- Q14. Prolog's N-queens (`select` + `\+ threat`) vs HW01's Python backtracker: same algorithm?
> **Answer.** Yes. Both are chronological backtracking, assigning one row/column at a time with the smallest value first and checking only against queens already placed. Prolog's backtracking is built in; Python's is an explicit recursive loop with undo. Prolog's first 8-queens answer `[4,2,7,3,6,8,5,1]` is the reverse of Python's `[0,4,7,5,2,6,1,3]` (1-based `[1,5,8,6,3,7,2,4]`), because Prolog prepends each placed queen ([[prolog-lecture-examples]]; [[hw01-ex03-n-queens]]).

## Weak spots

*(to be filled during exam-prep sessions)*

## Related

[[logic-systems-comparison]] · [[prolog]] · [[sld-resolution]] · [[unification]] · [[horn-clauses]] · [[conjunctive-normal-form-and-resolution]] · [[forward-chaining]] · [[backward-chaining]] · [[negation-as-failure]] · [[prolog-cut]] · [[lab01-family-pl]] · [[prolog-lecture-examples]] · [[history-of-ai]]
