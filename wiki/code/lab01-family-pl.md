---
type: code
summary: Walkthrough of Raymond's Lab 01 Prolog file — 16-person, 4-generation family KB with spouse/2, 17 rules (incl. uncle/aunt by marriage, cousin, father_in_law, descendant, terminating related/2) and 20 plunit tests (7 negative), all passing.
unit: [5, 6]
tags: [prolog, lab01, kinship, plunit, student-work, closed-world-assumption]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[lab01-prolog-family-report]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Lab 01 — `Portilla_Raymond_lab01.pl`

**File:** `raw/Class_exercises/01_Code/Portilla_Raymond_lab01.pl` (190 lines). Written report: [[lab01-prolog-family-report]].

**Problem.** Prolog Lab 01 ([[slides-xx-logic-programming-prolog]], slides 29–30). The task is to extend the lecture's `family.pl` to at least 16 people over 4 generations with a new `spouse/2`, and to record both parents of every child, with one couple having three or more children and someone having none (20 pts). Then add at least eight relationship rules, including `mother/2`, `sister/2`, `grandmother/2`, `uncle/2`, `cousin/2`, `father_in_law/2` and one new recursive rule that is not `ancestor/2` (35 pts). It also needs at least 20 plunit tests with six or more negative ones, including "nobody is their own sibling" (25 pts), a written analysis (20 pts), and optionally a terminating `related/2` (bonus +10).

**Status (re-run 2026-10-01, SWI-Prolog):** loads with no errors or warnings under `swipl -g true -t halt`; `run_tests` reports **All 20 tests passed**.

## The family

| Gen | People (spouse) | Children |
|---|---|---|
| 1 | hector + carmen | ana, luis, rosa (the 3-child couple) |
| 2 | ana + pedro | sofia, carlos |
| 2 | luis + maria | diego |
| 2 | rosa + juan | — (childless couple) |
| 3 | sofia + andres | lucia, mateo |
| 3 | carlos + elena | valentina |
| 3 | diego | — |
| 4 | lucia, mateo, valentina | — |

8 males, 8 females, 6 couples. The married-in spouses (pedro, maria, juan, andres, elena) have **no parents recorded**. Every *child* has both parents, as the brief requires.

## Design decisions

- **Spouse stored symmetrically as facts** (both `spouse(a,b)` and `spouse(b,a)`), rather than a symmetric rule. Rules that call `spouse/2` never need to try both orders, and there is no risk of a `spouse(X,Y):- spouse(Y,X)` loop.
- **`sibling/2` requires the same father and the same mother.** This removes the duplicate answers the slide-12 version produces (one per shared parent), at the cost of excluding half-siblings (see Known issues).
- **Uncles and aunts by marriage** are second clauses: the spouse of a parent's sister or brother, with a `male/1` or `female/1` check.
- **`descendant/2`** is the "own recursive rule".
- **`related/2` (bonus)** is a graph search over `family_link/2` (parent, child or spouse edges). A **visited list** with `\+ memberchk/2` stops it from walking up and down the same link forever, the failure mode named on slide 29.
- **Tests** use `once/1` on positive goals that have several proofs, so plunit does not warn about choicepoints. Negative tests use the `[fail]` option.
- AI assistance is declared for the two plunit setup lines (6–8).

## Walkthrough

| Lines | Code | What it does |
|---|---|---|
| 1–4 | header comment | Still the lecture's `family.pl` header (see Known issues) |
| 6–8 | `:- use_module(library(plunit)).` `:- set_test_options([format(log)]).` | Loads plunit; prints one line per test. Marked "AI helped" |
| 11–16 | `male/1`, `female/1` | 16 people |
| 18–24 | `spouse/2` | 6 couples × 2 directions |
| 26–39 | `parent/2` | Gen 1→2 (6 facts), 2→3 (6), 3→4 (6) |
| 44 | `mother(X,Y):- parent(X,Y), female(X).` | |
| 46 | `father(X,Y):- parent(X,Y), male(X).` | |
| 48–51 | `sibling/2` | Same father, same mother, `X \= Y` |
| 53, 55 | `sister/2`, `brother/2` | `sibling` + gender |
| 57–59 | `grandparent/2` | parent of a parent |
| 61 | `grandmother/2` | `grandparent` + female |
| 63–70 | `uncle/2` | (a) brother of a parent; (b) male spouse of a parent's sister |
| 72–79 | `aunt/2` | (a) sister of a parent; (b) female spouse of a parent's brother |
| 81–84 | `cousin/2` | parents are siblings (first cousins, blood only) |
| 86–88 | `father_in_law(X,Y):- spouse(Y,S), father(X,S).` | father of one's spouse |
| 90–91 | `ancestor/2` | lecture version (right-recursive, terminates) |
| 93–95 | `descendant(D,A)` | parent, or parent of an ancestor-chain |
| 97–98 | `person/1` | male or female |
| 100–102 | `related(X,Y):- person(X), reachable(X,Y,[X]).` | bonus entry point |
| 104–108 | `reachable/3` | reflexive base case; step along a link to an unvisited node |
| 110–112 | `family_link/2` | parent→child, child→parent, spouse |
| 117–178 | plunit block | 20 tests |
| 182–190 | comments | suggested queries |

```prolog
sibling(X, Y):-
    father(F, X), father(F, Y),
    mother(M, X), mother(M, Y),
    X \= Y.

uncle(X, Y):- parent(P, Y), brother(X, P).
uncle(X, Y):- parent(P, Y), sister(S, P), spouse(X, S), male(X).

related(X, Y):- person(X), reachable(X, Y, [X]).
reachable(X, X, _).
reachable(X, Y, Visited):-
    family_link(X, Z),
    \+ memberchk(Z, Visited),
    reachable(Z, Y, [Z|Visited]).
```

`X \= Y` sits **last** in `sibling/2`, after both are bound. Placed first, `X \= Y` on two free variables would fail, because they unify ([[unification]]). The `\+ memberchk(Z, Visited)` call is safe [[negation-as-failure]] because `Z` is bound by `family_link/2`.

### Tests (lines 119–176)

| # | Test | Kind | Checks |
|---|---|---|---|
| 1 | `mother_carmen_ana` | + | `mother/2` |
| 2 | `sister_ana_of_luis` | + | `sister/2` |
| 3 | `grandmother_carmen_sofia` | + | `grandmother/2` |
| 4 | `uncle_luis_of_sofia` | + | blood uncle |
| 5 | `cousin_sofia_diego` | + | `cousin/2` |
| 6 | `father_in_law_hector_pedro` | + | `father_in_law/2` |
| 7 | `descendant_recursive_four_generations` | + | `descendant(lucia, hector)` |
| 8 | `aunt_rosa_of_sofia` | + | blood aunt |
| 9 | `father_hector_ana` | + | `father/2` |
| 10 | `sibling_ana_luis` | + | `sibling/2` |
| 11 | `ancestor_hector_lucia` | + | `ancestor/2`, 3 levels |
| 12 | `nobody_is_own_sibling` | − | `sibling(X, X)` fails (required) |
| 13 | `rosa_has_no_children` | − | CWA |
| 14 | `diego_has_no_children` | − | CWA |
| 15 | `hector_is_not_mother` | − | gender check |
| 16 | `luis_is_not_sister_of_ana` | − | gender check |
| 17 | `siblings_are_not_cousins` | − | `cousin(sofia, carlos)` fails |
| 18 | `related_parent_child_terminates` | + | bonus terminates |
| 19 | `related_by_marriage_across_tree` | + | `related(juan, valentina)` |
| 20 | `not_related_to_stranger` | − | unknown constant |

13 positive and 7 negative (6 required).

## Results

Re-run 2026-10-01 with SWI-Prolog:

| Query | Result |
|---|---|
| `run_tests.` | All 20 tests passed |
| `findall(U-Y, uncle(U,Y), L)` | 9 distinct pairs: luis→sofia, carlos; carlos→lucia, mateo; juan→sofia, carlos, diego; pedro→diego; andres→valentina |
| `findall(A-Y, aunt(A,Y), L)` | 9 pairs: rosa→sofia, carlos, diego; ana→diego; sofia→valentina; maria→sofia, carlos; elena→lucia, mateo |
| `findall(X-Y, sibling(X,Y), L)` | 10 ordered pairs (5 unordered), no duplicates |
| `findall(X-Y, cousin(X,Y), L)` | 8 ordered pairs, e.g. sofia–diego, lucia–valentina |
| `findall(X-Y, father_in_law(X,Y), L)` | hector→pedro, maria, juan; pedro→andres, elena |
| `descendant(D, hector)` | 9 descendants |
| `related(ana, hector)` | 4 solutions (same answer) |
| `related(hector, Y)` | 229 solutions, 16 distinct |
| `related(hector, stranger)` | fails after 2,571 inferences |

## Known issues / improvements

1. **Half-siblings are excluded.** `sibling/2` needs the same father *and* mother, so children who share only one parent are not siblings. People with a missing parent fact can never have siblings either. This explains why `sibling(pedro, X)` is empty (pedro has no recorded parents). The report presents the rule only as a de-duplication fix. A version that keeps the duplicate-free behaviour and allows half-siblings: `sibling(X,Y):- setof(P, (parent(P,X), parent(P,Y)), _), X \= Y.` On this KB it gives the same 10 ordered pairs, each once (checked).
2. **Uncle/aunt chains inherit that restriction.** The blood clauses go through `brother/2` or `sister/2`, so a parent with unrecorded parents (pedro, maria, andres, elena) contributes no blood uncles or aunts. Great-uncles are not modelled. In this KB the clauses happen to give no duplicates, but a child whose two parents were *both* siblings of X would get X twice.
3. **`related/2` repeats answers heavily** (229 answers for 16 people from hector). Each simple path is a separate proof, and the negative case enumerates every simple path, which is exponential in general. Fixes: wrap in `setof/3` or `distinct/1`, or use a tabled reachability relation (`:- table conn/2. conn(X,Y):- family_link(X,Y). conn(X,Y):- conn(X,Z), family_link(Z,Y).`), which terminates and returns each person once. Checked: `conn(hector, Y)` gives 16 answers, all distinct, and `conn(hector, stranger)` fails immediately ([[sld-resolution]]).
4. **`related/2` is reflexive.** `related(hector, hector)` succeeds via `reachable(X, X, _)`, and `related(X, Y)` with `Y` free returns `Y = X` first. That is defensible, but it should be stated. `related(stranger, _)` fails at `person/1`, while `Y` is not checked with `person/1`. It only reaches people anyway.
5. **`descendant/2` is `ancestor/2` with the arguments swapped.** Both relations have exactly 36 pairs (re-run). It meets the letter of "a recursive rule that is not `ancestor/2`" but adds no new knowledge. A more convincing rule would compute something new, e.g. `generation_gap(A, D, N)` or `blood_relative/2`.
6. **`cousin/2` is first cousins by blood only.** It has no `X \= Y`, which is safe here because nobody's parents are siblings of each other.
7. **The header is stale.** Lines 1–4 still say "family.pl -- the knowledge base used in the Prolog lecture". The slide 30 rule asks for an AI-use statement in a header comment that says what was changed; the file has only an inline note on lines 6–8.
8. **Sections are by kind (facts, rules, tests), not "one section per exercise"** as slide 30 asks.
9. `uncle/2` clause (b) and `aunt/2` clause (b) keep the `male/1` or `female/1` check. That makes them correct even for same-sex couples, so it is a good choice rather than a redundancy.

## Related concepts

[[prolog]] · [[first-order-logic]] (R&N kinship axioms §8.3.2) · [[backward-chaining]] · [[unification]] · [[negation-as-failure]] · [[sld-resolution]] · [[prolog-cut]] (`once/1`) · [[depth-first-search]] (`reachable/3` is DFS with a path-based visited list) · [[state-space-and-graph-search]]

## Practice questions

> [!question]- Q1. Why does `sibling/2` need `X \= Y`, and why is it the last goal?
> **Answer.** Without it, everyone with parents is their own sibling: both `father(F, ana)` calls succeed with the same F. It is last because `\=` means "do not unify". With unbound `X` and `Y` it would fail immediately, so both have to be bound by the `father`/`mother` goals first ([[lab01-prolog-family-report]]; [[unification]]).

> [!question]- Q2. Your `sibling/2` gives each pair once. What did you give up to get that?
> **Answer.** Half-siblings. Requiring the same father and the same mother means children who share only one parent are not siblings, and anyone missing a parent fact has no siblings at all (e.g. `sibling(pedro, X)` is empty). Using `setof/3` over shared parents would keep both properties.

> [!question]- Q3. Walk me through how `uncle(juan, sofia)` is proved.
> **Answer.** Clause 1: `parent(P, sofia)` gives P = ana, then `brother(juan, ana)` fails because juan has no recorded parents. P = pedro also fails. Clause 2: `parent(P, sofia)` gives P = ana. `sister(S, ana)` gives S = rosa (same father hector and mother carmen, rosa ≠ ana). `spouse(juan, rosa)` ✓ and `male(juan)` ✓. Proved ([[backward-chaining]]).

> [!question]- Q4. Why would a naive `related/2` loop, and how does yours terminate?
> **Answer.** With `related(X,Y):- link(X,Z), related(Z,Y).` and symmetric links, Prolog's depth-first search goes ana → hector → ana → … forever. Mine carries a `Visited` list and refuses to step to a node already on the path (`\+ memberchk(Z, Visited)`). Every path is simple and the graph has 16 nodes, so the search is finite ([[sld-resolution]]).

> [!question]- Q5. `related(ana, hector)` succeeds four times. Is that a bug? How would you return each relative once?
> **Answer.** It is not a logical bug. Each distinct simple path from ana to hector is a different proof (directly, through carmen, …). For each relative once: `setof(Y, related(X, Y), Ys)`, `distinct(Y, related(X, Y))`, or a tabled connectivity predicate. Tabling also stops the negative query from exploring every path (2,571 inferences for `stranger`).

> [!question]- Q6. Which of your negative tests depend on the closed-world assumption?
> **Answer.** `rosa_has_no_children`, `diego_has_no_children` and `not_related_to_stranger` hold only because no fact proves the opposite. `hector_is_not_mother` and `luis_is_not_sister_of_ana` hold because `female(hector)` and `female(luis)` are not in the KB, which is also CWA. `nobody_is_own_sibling` and `siblings_are_not_cousins` follow from the rules' structure ([[negation-as-failure]]).

> [!question]- Q7. Is `descendant/2` really a new recursive rule?
> **Answer.** Logically it is the inverse of `ancestor/2`: `descendant(D, A)` holds iff `ancestor(A, D)`, and both have 36 pairs. It satisfies the wording of the brief. A stronger answer would add a rule that computes something new, such as the number of generations between two people.

> [!question]- Q8. Why do your positive tests use `once/1`?
> **Answer.** Goals such as `related(ana, hector)` or `ancestor(hector, lucia)` can succeed more than once or leave a choicepoint, and plunit warns when a deterministic test leaves choicepoints. `once/1` commits to the first proof. It acts like a cut after the goal ([[prolog-cut]]).
