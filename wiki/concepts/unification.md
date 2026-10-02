---
type: concept
summary: Finding the most general substitution (MGU) that makes two terms identical — two-way pattern matching that powers every first-order inference rule and every Prolog call; Prolog skips the occurs check.
unit: [5, 6]
tags: [logic, unification, mgu, occurs-check, prolog]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Unification

**Unification** takes two terms and finds a **substitution** (a set of variable bindings $\{x/t\}$) that makes them identical, or fails ([[slides-xx-logic-programming-prolog]], slide 14; [[russell-norvig-aima]] §9.2.1). It is "pattern matching in both directions: neither side is the 'input'". Every lifted inference rule — Generalized Modus Ponens, [[forward-chaining]], [[backward-chaining]], [[conjunctive-normal-form-and-resolution|resolution]] — needs it, and in [[prolog]] it is how a goal is matched to a clause head and how `=/2` works.

## How it works

$\text{UNIFY}(p, q) = \theta$ such that $\text{SUBST}(\theta, p) = \text{SUBST}(\theta, q)$.

**Rules** ([[slides-xx-logic-programming-prolog]], slide 14):

1. Atoms and numbers unify only with themselves.
2. A variable unifies with anything, then stays bound.
3. Compound terms unify iff they have the same functor and arity and their arguments unify pairwise (left to right, carrying the substitution).

**Algorithm** ([[russell-norvig-aima]] Fig. 9.1):

```
UNIFY(x, y, θ):
    if θ = failure: return failure
    if x = y: return θ
    if VARIABLE(x): return UNIFY-VAR(x, y, θ)
    if VARIABLE(y): return UNIFY-VAR(y, x, θ)
    if COMPOUND(x) and COMPOUND(y):
        return UNIFY(ARGS(x), ARGS(y), UNIFY(OP(x), OP(y), θ))
    if LIST(x) and LIST(y):
        return UNIFY(REST(x), REST(y), UNIFY(FIRST(x), FIRST(y), θ))
    return failure

UNIFY-VAR(var, x, θ):
    if {var/val} ∈ θ: return UNIFY(val, x, θ)
    if {x/val} ∈ θ: return UNIFY(var, val, θ)
    if OCCUR-CHECK(var, x): return failure
    return θ ∪ {var/x}
```

**Most general unifier (MGU).** If two terms unify, there is a single most general unifier, unique up to renaming. `Knows(John, x)` and `Knows(y, z)` unify with $\{y/John, x/z\}$ or with $\{y/John, x/John, z/John\}$; the first is more general, because the second is the first plus $\{z/John\}$ ([[russell-norvig-aima]] §9.2.1).

**Standardizing apart.** `Knows(John, x)` and `Knows(x, Elizabeth)` fail only because both use the name `x`. Rename one to `x17` and they unify with $\{x/Elizabeth, x17/John\}$ ([[russell-norvig-aima]] §9.2.1). Prolog does this automatically: each clause use gets fresh variables.

**Examples in SWI-Prolog** ([[slides-xx-logic-programming-prolog]], slide 14):

```prolog
?- f(a, Y) = f(X, b).
X = a, Y = b.
?- [H|T] = [1, 2, 3].
H = 1, T = [2, 3].
?- f(a) = g(a).
false. % different functors
?- X = f(X).
X = f(X). % cyclic: no occurs check
?- unify_with_occurs_check(X, f(X)).
false.
```

## Properties

- **Occurs check**: when binding variable $x$ to term $t$, fail if $x$ occurs inside $t$ ($S(x)$ cannot unify with $S(S(x))$). It makes unification quadratic in the size of the terms, so most logic programming systems **omit** it ([[russell-norvig-aima]] §9.2.1, §9.4.2).
- Without it, Prolog can make **unsound** inferences, "almost never a problem in practice" ([[russell-norvig-aima]] §9.4.2). Luger lists it with cut and negation as failure as violations of the pure logic-programming semantics ([[luger-ai-6e]] §14.3.2).
- Linear-time algorithms exist ([[russell-norvig-aima]] §9.2.1).
- Unification is **not evaluation**: `3 + 4 = 7` fails because the term `+(3,4)` is not the atom `7` ([[slides-xx-logic-programming-prolog]], slide 16). Use `is/2` or `=:=/2`.
- Retrieval: indexing facts by predicate (and argument) avoids pointless unification attempts ([[russell-norvig-aima]] §9.2.2).

## In this course

- Slide 14: the rules and examples above, including the cyclic term `X = f(X)` ([[slides-xx-logic-programming-prolog]], slide 14).
- Slide 15: [[sld-resolution]] = depth-first backward chaining **with unification**; "on failure, backtrack: undo bindings" ([[slides-xx-logic-programming-prolog]], slide 15).
- Slide 16: `=/2` (unify) vs `is/2` (evaluate) vs `==/2` (identity) vs `\=/2` (not unifiable).
- Slide 19: lists are terms; `[H|T] = [1,2,3]` splits a list; `append/3` runs backwards because unification is two-way.
- Slide 22: the BST — "pattern matching takes it apart" (`node(K, L, R)`); see [[prolog-lecture-examples]].
- In [[lab01-family-pl]], `X \= Y` in `sibling/2` is "X and Y do not unify", which on ground atoms means "different names".

## Common mistakes

- Treating `=` as assignment or as arithmetic equality.
- Using `\=` on unbound variables: `X \= a` *fails* when `X` is free, because `X` can unify with `a`.
- Forgetting standardizing apart in hand traces (re-using `X` from two different clauses).
- Assuming `X = f(X)` fails in Prolog — it succeeds and builds a cyclic term.

## Related

[[first-order-logic]] · [[backward-chaining]] · [[forward-chaining]] · [[sld-resolution]] · [[prolog]] · [[conjunctive-normal-form-and-resolution]]

## Practice questions

> [!question]- Q1. Give the MGU of `f(X, g(Y), Y)` and `f(a, g(b), Z)`.
> **Answer.** Argument 1: $\{X/a\}$. Argument 2: `g(Y) = g(b)` → $\{Y/b\}$. Argument 3: `Y = Z` with $Y = b$ → $\{Z/b\}$. MGU $= \{X/a, Y/b, Z/b\}$ (checked in SWI-Prolog).

> [!question]- Q2. Unify `p(X, X)` with `p(f(Y), f(a))`.
> **Answer.** $X/f(Y)$; then $X = f(a)$ means $f(Y) = f(a)$ → $Y/a$. MGU $= \{X/f(a), Y/a\}$.

> [!question]- Q3. Do `p(X, f(X))` and `p(Y, Y)` unify (a) with the occurs check, (b) in plain Prolog `=`?
> **Answer.** First $X/Y$; then $f(X) = Y$ becomes $Y = f(Y)$. (a) The occurs check fails it: `unify_with_occurs_check/2` returns `false`. (b) Plain `=` succeeds and builds a cyclic term (checked in SWI-Prolog).

> [!question]- Q4. Predict: `?- knows(john, X) = knows(X, elizabeth).`
> **Answer.** `false`. `X = john` from argument 1, then `john = elizabeth` fails. In logic you would standardize the two sentences apart first; inside one Prolog query the two `X` are the same variable ([[russell-norvig-aima]] §9.2.1).

> [!question]- Q5. Predict: `?- [A, B | C] = [1, 2].` and `?- [H|T] = [a].`
> **Answer.** `A = 1, B = 2, C = []` and `H = a, T = []` — the tail of the last cell is the empty list ([[slides-xx-logic-programming-prolog]], slide 19).

> [!question]- Q6. `Knows(John, x)` and `Knows(y, z)` can be unified by $\theta_1 = \{y/John, x/z\}$ or $\theta_2 = \{y/John, x/John, z/John\}$. Which is the MGU and why?
> **Answer.** $\theta_1$. Applying $\theta_1$ gives `Knows(John, z)`, which still allows any `z`; $\theta_2$ equals $\theta_1$ followed by the extra binding $\{z/John\}$, so it is less general ([[russell-norvig-aima]] §9.2.1).
