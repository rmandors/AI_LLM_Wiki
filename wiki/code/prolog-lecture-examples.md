---
type: code
summary: Walkthrough of the seven lecture Prolog files in 01_Code — factorial, naive Fibonacci, isEven/isOdd, isPerm (set-equality bug), binary search tree (delete2 bug), N-queens, and predicates.pl (incl. isMerged = list interleaving) — with re-run results and bugs.
unit: [5, 6]
tags: [prolog, recursion, lists, bst, n-queens, lecture-code, bugs]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Prolog lecture examples (`01_Code/*.pl`)

**Files:** `raw/Class_exercises/01_Code/` contains `factorial.pl`, `fibonacci.pl`, `isEven.pl`, `isPerm.pl`, `binaryTree.pl`, `queens.pl` and `predicates.pl`. These are the instructor's programs shown in [[slides-xx-logic-programming-prolog]], slides 17–27. Most file dates are 2011, `fibonacci.pl` and `queens.pl` are 2023. Raymond's own lab is in [[lab01-family-pl]].

**Problems they solve:** recursion with arithmetic, recursion on lists, data structures as terms, and a search problem (N-queens) where Prolog's backtracking *is* the [[csp-backtracking-search]] algorithm.

**Load check** (SWI-Prolog, `swipl -g true -t halt`): `factorial`, `fibonacci` and `queens` load cleanly. `isEven` (2 warnings), `isPerm` (3), `binaryTree` (7) and `predicates` (5) produce **singleton-variable warnings**. Under the Lab 01 rules those would cost points ([[slides-xx-logic-programming-prolog]], slide 30).

## Design decisions

- **Clauses instead of if-then-else.** Base case as a fact, recursive case guarded by a test (`A > 0`, `N > 1`) (slide 17).
- **Order goals for `is/2`.** Inputs are computed before the recursive call (`C is A - 1` first), and outputs after it (`B is A * D` "on the way back up") (slide 17).
- **Data structures are terms.** `node(K, L, R)` / `empty` for trees and `[H|T]` for lists. Nothing is mutated; `insert/3` *relates* an old tree to a new one (slide 22).
- **Representation does the work** in N-queens. A permutation of 1..N gives one queen per row and per column by construction, so only diagonals are checked (slide 25).

## Walkthrough

### `factorial.pl` (lines 1–7)

```prolog
factorial(0,1).
factorial(A,B):-
           A > 0,
           C is A-1,
           factorial(C,D),
           B is A*D.
```

- l.1: base case $0! = 1$. l.3–7: guarded recursive case.
- `?- factorial(5, X).` gives `X = 120; false.` The trailing `false` is a surviving choicepoint, because both clauses are tried for `factorial(0, D)` (slide 17).
- Integers are unbounded: `factorial(20, X)` gives `2432902008176640000` (slide 17).
- **Slide exercise: `?- factorial(X, 120).`** Clause 1 fails (`1 ≠ 120`), then clause 2 calls `X > 0` with `X` unbound and raises **"Arguments are not sufficiently instantiated"** (re-run). Arithmetic runs one way only.
- Accumulator rewrite (the slide's second exercise; tail recursive, general knowledge):

```prolog
fact(N, F):- fact_(N, 1, F).
fact_(0, A, A).
fact_(N, A, F):- N > 0, A1 is A * N, N1 is N - 1, fact_(N1, A1, F).
```

### `fibonacci.pl` (lines 1–9)

```prolog
fibo(N, Y):- N > -1, N < 2, Y is 1.
fibo(N, Y):- N > 1, C is N-1, D is N-2,
             fibo(C, A), fibo(D, B), Y is A+B.
```

- Indexing starts at `fibo(0) = fibo(1) = 1`, so `fibo(10, X)` gives `89` (slide 18).
- **Exponential**: each call spawns two more. `time(fibo(25,_))` takes ~1.09 M inferences (slide 18 says 1,092,530; re-run gave 1,092,533).
- Fixes on slide 18: an accumulator `fib/2` (seeded `1, 1`; `fib(30, X)` gives `1346269`, linear time), or `:- table fibo/2.` to memoise ([[sld-resolution]]).
- **Edge case (re-run):** the guards accept non-integers. `fibo(0.5, Y)` gives `1` and `fibo(2.5, Y)` gives `2`. `integer(N)` would close that. `fibo(N, 1)` with `N` unbound raises an instantiation error.

### `isEven.pl` (lines 1–5)

```prolog
isEven([], 'true').
isEven([X|XS], Y):- isOdd(XS, Y).
isOdd([],'false').
isOdd([Y|YS], Z):- isEven(YS, Z).
```

- Mutual recursion on list **length**. The elements are never inspected (slide 20). `isEven([a,b,c,d], X)` gives `true`; `[a,b,c]` gives `false`.
- Singleton warnings for `X` (l.2) and `Y` (l.5). Rename them `_` (slide 20).
- Slide 20's critique: returning atoms `true`/`false` is "Java thinking". The idiomatic form succeeds or fails: `even_length([]). even_length([_|T]):- odd_length(T). odd_length([_|T]):- even_length(T).`
- Run backwards, `isEven(L, X)` with `L` a fresh list of length 0..3 gives `true, false, true, false` (re-run). The relation works in both directions.

### `isPerm.pl` (lines 1–7) — the bug on slide 21

```prolog
isPerm(X, Y):- isInc(X, Y), isInc(Y, X).
isInc([], Y).
isInc([X|XS],Y):- isMember(X, Y), isInc(XS, Y).
isMember(X, [X|XS]).
isMember(X, [Y|XS]):- isMember(X, XS).
```

- l.1: X ⊆ Y and Y ⊆ X. l.3–4 `isInc` = every element of the first list is in the second. l.6–7 `isMember` = `member/2`.
- **Bug: this is set equality, not permutation.** `isPerm([1,1,2], [1,2,2])` gives `true` (wrong; the built-in `permutation/2` says `false`). `isPerm([1,2], [2,1,1,1])` also gives `true`, because lengths are never compared (re-run) (slide 21).
- Fixes: `is_perm(X, Y):- msort(X, S), msort(Y, S).` or generate-and-test with `permutation/2` (slide 21).
- Singletons: `Y` (l.3), `XS` (l.6), `Y` (l.7).

### `binaryTree.pl` (lines 1–23)

```prolog
member2(K, node(K, S, T)).
member2(K, node(N, S, T)):- K < N, member2(K, S).
member2(K, node(N, S, T)):- K > N, member2(K, T).
```

- l.1–3 `member2/2`: BST lookup. The file has seven singleton warnings, on lines 1, 2, 3, 18, 21, 22 and 23. The one on **line 18 (`[L]`)** is the compiler pointing at the `delete2` bug below.
- l.5–11 `insert/3`: six clauses. The four special cases for `empty` children (l.6–9) are subsumed by the general two (l.10–11), as slide 22 says. Inserting an existing key **fails**, since no clause covers `N =:= K` (re-run: `insert(5, T, _)` with 5 already present gives `false`).
- l.13–18 `delete2/3`, not shown on the slides:

```prolog
delete2(N, node(N, empty, empty), empty).
delete2(N, node(N, L, empty), L).
delete2(N, node(N, empty, R), R).
delete2(N, node(N, L, R), M):- inOrderSuccesor(R, X), delete2(X, R, R2), M = node(X, L, R2).
delete2(N, node(K, L, R), T):- N < K, delete2(N, L, M), T = node(K, M, R).
delete2(N, node(K, L, R), T):- N > K, delete2(N, R, M), T = node(K, R, M). % BUG
```

> [!warning] Bug in `delete2/3` (line 18)
> The right-branch clause builds `node(K, R, M)`. It puts the old **right** subtree where the left one should be and loses the left subtree `L`. It should be `node(K, L, M)`. SWI-Prolog flags it on load: "Singleton variables: [L]" at line 18. Re-run with tree `node(5, node(3,e,e), node(8, node(7,e,e), e))`: `delete2(7, T, T2)` gives `node(5, node(8,node(7,e,e),e), node(8,e,e))`. The 3 is gone, 7 is still there, and 8 appears twice.

- Overlapping clauses cause **duplicate answers**. A leaf matches clauses 1, 2 and 3 (deleting 3 gives the same tree 3 times). Deleting the root 5 gives the same tree **12 times** (re-run). `inOrderSuccesor/2` (l.20–23) has the same overlap (a leaf matches its clauses 1 and 2).
- `inOrderSuccesor(R, X)` returns the **minimum** of subtree `R`, which is the in-order successor of the deleted node. The name is spelled "Succesor".

### `queens.pl` (lines 1–23)

```prolog
queens(N, Qs):- range(1, N, Ns), queens(Ns, [], Qs).
queens([], Qs, Qs).
queens(UnplacedQs, SafeQs, Qs):-
    select(Q, UnplacedQs, NewUnplaced),
    \+ threat(Q, SafeQs),
    queens(NewUnplaced, [Q|SafeQs], Qs).
threat(X, Xs):- threat(X, 1, Xs).
threat(X, N, [Y|_Ys]):- X is Y + N; X is Y - N.
threat(X, N, [_Y|Ys]):- N1 is N + 1, threat(X, N1, Ys).
range(M, N, [M|Ns]):- M < N, M1 is M + 1, range(M1, N, Ns).
range(N, N, [N]).
```

- l.1–3 build `[1..N]` and start with no safe queens. l.5–9: `select/3` is the **choice point** (a value for the next row). `\+ threat` prunes immediately, and the new queen is pushed onto `SafeQs`.
- l.11–17 `threat/3`: `N` is the row distance to each earlier queen. The new queen `X` attacks `Y` iff `X = Y ± N` (same diagonal). With `X` bound, `is/2` *checks* rather than computes.
- l.19–23 `range/3`.
- Results (re-run): `queens(8, Qs)` first gives `[4,2,7,3,6,8,5,1]`, and there are 92 solutions in total. N = 6 gives 4. N = 1 gives `[1]`. N = 2 and 3 give none. `queens(0, _)` **fails**, because `range(1, 0, _)` has no clause, although the empty board is technically one solution. All of these match slide 26.
- **Test as you go = backtracking search.** Because `\+ threat` runs right after each `select`, this is chronological [[csp-backtracking-search]] with forward checking only against placed queens ([[russell-norvig-aima]] §9.4.5: "Standard Prolog solves such problems in exactly the same way as the backtracking algorithm"). Slide 27's generate-and-test version (`permutation/2`, then `safe/1`) does 17× more inferences at N = 8 and 77× more at N = 10.
- **Answer order:** `SafeQs` is built by prepending, so `Qs` lists the queens in *reverse* placement order. The first answer `[4,2,7,3,6,8,5,1]` is the reverse of `[1,5,8,6,3,7,2,4]`, which is the 1-based form of the first solution `[0,4,7,5,2,6,1,3]` from Raymond's Python backtracker in [[hw01-ex03-n-queens]]. Both programs run the same search with the same value order. The reversed list is still a valid solution (the mirror image).

### `predicates.pl` (lines 1–21)

Lines 1–5 copy `isEven/isOdd` and lines 7–13 copy `isPerm/isInc/isMember`, with the same singleton warnings. New code:

```prolog
isMerged([], [], []).
isMerged(L1, [], L3):- isTail(L1, L3).
isMerged(L1, L2, []):- isTail(L1, L2).
isMerged([X1|[X2|L1]],[X|L2], [Y|L3]):- X=X1, Y=X2, isMerged(L1, L2, L3).

isTail([],[]).
isTail([X|XS], [Y|YS]):- X=Y, isTail(XS, YS).
```

**What `isMerged(L1, L2, L3)` means:** L1 is the **alternating interleave** ("riffle") of L2 and L3, starting with L2. It takes the head of L2, then the head of L3, and so on. When one list runs out, the rest of L1 is the rest of the other. Clause 4 consumes two elements of L1 at a time (`X1` must equal L2's head, `X2` must equal L3's head), and clauses 2–3 handle the leftover. It is **not** a sorted merge: `isMerged(L, [3,1], [2])` gives `[3,2,1]`.

- `isTail/2` is just element-wise list equality, the same as `L1 = L2` for proper lists. The name is misleading.
- Re-run results:
  - `isMerged(L, [1,2,3], [a])` gives `L = [1,a,2,3]` and `isMerged(L, [1], [a,b,c])` gives `[1,a,b,c]`.
  - `isMerged(L, [1,2], [a,b])` gives `[1,a,2,b]` **three times**. When both inputs run out together, the remaining call `isMerged([], [], [])` matches all three base clauses.
  - Split mode, `isMerged([1,a,2,b], A, B)`: 7 answers, `[]/[1,a,2,b]`, `[1,a,2,b]/[]`, `[1]/[a,2,b]`, `[1,2,b]/[a]`, and `[1,2]/[a,b]` ×3.
- Fix for the duplicates: drop clause 1, and make clause 3 require a non-empty L2. Unifying in the head is also more idiomatic than `X=X1` in the body:

```prolog
merged(L1, [], L3):- L1 = L3.
merged(L1, [H|T], []):- L1 = [H|T].
merged([X,Y|L1], [X|L2], [Y|L3]):- merged(L1, L2, L3).
```

  Checked: `merged(L, [1,2], [a,b])` gives `[1,a,2,b]` once, the split query gives 5 distinct answers, and `merged([], [], [])` succeeds once.

## Results

| Program | Query | Result (re-run 2026-10-01) |
|---|---|---|
| factorial | `factorial(5,X)` / `factorial(X,120)` | `120; false` / instantiation error |
| fibonacci | `fibo(10,X)`; inferences for `fibo(25,_)` | `89`; 1,092,533 |
| isPerm | `isPerm([1,1,2],[1,2,2])` | `true` (bug) |
| binaryTree | `delete2(7, T4, T)` | wrong tree (bug), 3 copies |
| queens | count for N = 8 / N = 6 | 92 / 4 |
| predicates | `isMerged(L,[1,2],[a,b])` | `[1,a,2,b]` ×3 |

## Known issues / improvements

1. `delete2/3` right-branch bug (line 18) and duplicate answers from overlapping clauses.
2. `isPerm/2` implements set equality, not permutation.
3. Singleton warnings in four of seven files. The Lab 01 rubric penalises them.
4. `fibo/2` is exponential, accepts floats, and runs one way only.
5. `factorial/2` cannot run backwards, and it leaves a choicepoint.
6. `isMerged/3` gives duplicate answers, and `isTail/2` is a misnamed `=/2`.
7. `queens(0, _)` fails; the output is in reverse placement order.
8. `insert/3` has four redundant clauses and fails on duplicate keys.

## Related concepts

[[prolog]] · [[sld-resolution]] · [[unification]] · [[negation-as-failure]] · [[prolog-cut]] · [[csp-backtracking-search]] · [[constraint-satisfaction-problems]] · [[hw01-ex03-n-queens]] · [[depth-first-search]]

## Practice questions

> [!question]- Q1. What does `?- factorial(X, 120).` do, and why?
> **Answer.** Clause 1 fails because 1 ≠ 120. Clause 2 calls `X > 0` with `X` unbound, which raises "Arguments are not sufficiently instantiated". `is/2` and comparisons need bound operands, so the program runs one way only (slide 16–17).

> [!question]- Q2. Spot the bug: why is `isPerm([1,1,2],[1,2,2])` true?
> **Answer.** `isPerm` only checks that each list's elements occur in the other, which is set equality. Multiplicities and lengths are ignored. Fix with `msort(X,S), msort(Y,S)` or `permutation/2` (slide 21).

> [!question]- Q3. What does `isMerged/3` compute? Predict `?- isMerged(L, [1,2,3], [a]).`
> **Answer.** It interleaves L2 and L3 alternately, starting with L2, then appends the leftover. `L = [1,a,2,3]` (re-run).

> [!question]- Q4. Why does `?- isMerged(L, [1,2], [a,b]).` return the same answer three times?
> **Answer.** After two steps of clause 4 the remaining call is `isMerged([], [], [])`. It matches clause 1, clause 2 (`isTail([],[])`) and clause 3 (`isTail([],[])`), which are three separate proofs of the same thing.

> [!question]- Q5. Find the bug in `delete2(N, node(K, L, R), T):- N > K, delete2(N, R, M), T = node(K, R, M).`
> **Answer.** The new node should keep the left subtree `L`: `T = node(K, L, M)`. As written, it moves the old right subtree to the left and drops `L` entirely.

> [!question]- Q6. In `queens.pl`, where is the backtracking, and why does it beat generate-and-test?
> **Answer.** `select/3` is the choice point. On failure Prolog backtracks into it and tries the next value. `\+ threat(Q, SafeQs)` rejects a queen as soon as it is placed, so whole subtrees are pruned. Generating a full permutation and testing it at the end is 17× slower at N = 8 and 77× slower at N = 10 (slide 27).

> [!question]- Q7. Why is the naive `fibo/2` slow, and name two fixes?
> **Answer.** Each call makes two recursive calls, so the proof tree is exponential and subgoals are re-proved (~1.09 M inferences for N = 25). Fixes: an accumulator carrying the two previous values (linear), or `:- table fibo/2.` (memoisation) (slide 18).
