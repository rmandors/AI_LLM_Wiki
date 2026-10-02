---
type: source
summary: Riofrío's 31-slide deck "Logic Programming with Prolog" — propositional → FOL → Horn clauses → Prolog, unification, SLD resolution, arithmetic, recursion, lists, NAF and cut, N-queens case study, debugging, and the Lab 01 assignment.
unit: [5, 6]
tags: [slides, prolog, logic, horn-clauses, lab01]
sources: ["[[slides-xx-logic-programming-prolog]]"]
updated: 2026-10-01
---

# Slides XX — Logic Programming with Prolog

**Bibliographic line.** Daniel Riofrío ([[daniel-riofrio]]), *Logic Programming with Prolog*, lecture slides, Artificial Intelligence (NRC 1651), USFQ, Fall 2026. Raw file: `raw/Slides/XX_Logic Programming with Prolog.pptx` (31 slides; "XX" because the deck is not yet numbered in the course sequence).

**What it is.** The course's single Prolog lecture, covering syllabus units 5–6. It moves from checkable logic to runnable logic ("Until now our logic could only be checked. Today we can run it", slide 2), teaches SWI-Prolog hands-on, and ends with the Lab 01 assignment. Program files shown in class are in `raw/Class_exercises/01_Code/` ([[prolog-lecture-examples]]). Several figures are taken from R&N 4e Global Edition (Figs. 7.12, 7.16, 9.7) ([[russell-norvig-aima]]).

## Key points

| Slide | Topic | Key content | Wiki page |
|---|---|---|---|
| 1 | Title | — | — |
| 2 | Where we are | Four steps: propositional (decidable, no "every") → FOL (undecidable) → Horn (cheap entailment) → Prolog (Horn + backward chaining + unification). Kowalski 1979: *Algorithm = Logic + Control* | [[propositional-logic]], [[first-order-logic]] |
| 3 | Sentences → clauses | Literal, clause, CNF; rewriting is an equivalence; resolution is refutation-complete and needs clause form; R&N Fig. 7.12 grammar | [[conjunctive-normal-form-and-resolution]] |
| 4 | Horn clauses | At most one positive literal; definite clause / fact / goal clause; $P \vee Q$ has no Horn form | [[horn-clauses]] |
| 5 | Why Horn matters | Read as implications; chaining; linear propositional entailment, FOL semidecidable but cheaper; AND–OR graph (R&N Fig. 7.16) | [[forward-chaining]], [[backward-chaining]] |
| 6 | Backward chaining | Criminal(West) proof tree (R&N Fig. 9.7); depth first, left to right; space linear in proof size | [[backward-chaining]] |
| 7 | FOL → Prolog | Four conventions (backwards `:-`, inverted case, implicit ∀, punctuation); West KB in Prolog; `?- criminal(west). true.` | [[prolog]] |
| 8 | What is Prolog | Marseille 1972, Colmerauer & Roussel, Kowalski's theory; uses (expert systems, DCG parsing, compilers, constraints); declarative reading of `ancestor/2` | [[prolog]], [[alain-colmerauer]], [[robert-kowalski]] |
| 9 | SWI-Prolog | Univ. of Amsterdam since 1987; course on 9.2, current 10.x; trace/gtrace, clpfd, tabling, SWISH; ISO vs library | [[prolog]] |
| 10 | Installing | brew / winget / apt / dnf; `swipl --version` → 9.2.9; SWISH | — |
| 11 | First session | `X is 2+3*4` → 14; `[user].`; `consult/1`, `listing/1`, `halt/0`; prompts `?-` (query) vs `\|:` (reading clauses); `;` vs Enter | [[prolog]] |
| 12 | Program anatomy | Terms (atom, number, variable, compound); fact/rule/query; name/arity; `family.pl` | [[prolog]] |
| 13 | Querying | Multiple answers; leftover choicepoint `false`; `findall/3` vs `setof/3`, `C^Goal`; `\+ parent(sofia,_)` | [[prolog]], [[negation-as-failure]] |
| 14 | Unification | Rules; examples; `X = f(X)` cyclic; `unify_with_occurs_check/2` | [[unification]] |
| 15 | Execution | SLD resolution steps; `path/2` base-first vs left-recursive → stack overflow; "SLD resolution is complete; Prolog's search rule is not"; `:- table path/2.` | [[sld-resolution]] |
| 16 | Arithmetic | `is/2` vs `=/2`; `=:=`, `=\=`, `<`, `>`, `=<`, `>=`, `==`, `\=`; instantiation error; `**`, `mod` | [[prolog]] |
| 17 | Factorial | Two clauses; `A > 0`; `is` before recursive call; unbounded integers (20!); exercises: `factorial(X,120)`, accumulator | [[prolog-lecture-examples]] |
| 18 | Fibonacci | Naive exponential `fibo/2` (25 → 1,092,530 inferences); accumulator `fib/2` (seeded 1,1); tabling | [[prolog-lecture-examples]] |
| 19 | Lists | `[H\|T]`; `append/3` run backwards; `mymember`, `myappend`, `mylen`; library list predicates | [[prolog]] |
| 20 | isEven / isOdd | Mutual recursion on list length; singleton warnings; idiomatic `even_length/1` | [[prolog-lecture-examples]] |
| 21 | isPerm bug | Mutual inclusion = set equality, not permutation; `[1,1,2]` vs `[1,2,2]`; fix with `msort/2` or `permutation/2` | [[prolog-lecture-examples]] |
| 22 | BST | `member2/2`, `insert/3` on `node(K,L,R)`; terms are immutable, structure sharing; original file's extra `empty` clauses are subsumed | [[prolog-lecture-examples]] |
| 23 | NAF and cut | `\+` + closed world; bind first; cut semantics; `max/3` bug; prefer `->` | [[negation-as-failure]], [[prolog-cut]] |
| 24 | Built-ins | findall, bagof/setof, aggregate_all, forall, between, select, permutation, length, msort/sort, format, time, listing, make | [[prolog]] |
| 25 | N-queens | Permutation representation; `select/3` as choicepoint; `\+ threat/2` diagonal test; `range/3` | [[prolog-lecture-examples]] |
| 26 | Running N-queens | First 8-queens answer `[4,2,7,3,6,8,5,1]`; 92 solutions; N=6 → 4; solution-count table N=4..10 (2,10,4,40,92,352,724); `print_board/1` | [[prolog-lecture-examples]] |
| 27 | Generate & test vs test-as-you-go | `queens_perm` vs `queens_bt`; inference ratios 2.1× (N=4) to 77.1× (N=10) | [[prolog-lecture-examples]], [[csp-backtracking-search]] |
| 28 | Debugging | `trace/0` four ports; common mistakes list | [[prolog]] |
| 29 | Lab 01 | KB ≥16 people/4 generations + `spouse/2` (20); ≥8 rules incl. mother, sister, grandmother, uncle, cousin, father_in_law + one new recursive rule (35); ≥20 plunit tests, ≥6 negative incl. no self-sibling (25); analysis (20); bonus `related/2` that terminates (+10) | [[lab01-family-pl]], [[lab01-prolog-family-report]] |
| 30 | Deliverables | `lastname_firstname_lab01.pl` + `.pdf` (≤2 pages); must load cleanly with `swipl -g true -t halt`; singleton warnings cost points; declare AI use in a header comment | [[lab01-family-pl]] |
| 31 | Reading | R&N §7.5, §9.4; Luger §14.2–14.3; Bratko; Sterling & Shapiro; swi-prolog.org, SWISH, learnprolognow.org, metalevel.at | [[russell-norvig-aima]], [[luger-ai-6e]] |

### N-queens inference table (slide 27)

| N | generate & test | interleaved | ratio |
|---|---|---|---|
| 4 | 425 | 200 | 2.1× |
| 5 | 2,370 | 808 | 2.9× |
| 6 | 15,358 | 3,090 | 5.0× |
| 7 | 119,997 | 13,587 | 8.8× |
| 8 | 1,058,230 | 61,770 | 17.1× |
| 9 | 10,426,943 | 296,373 | 35.2× |
| 10 | 113,230,594 | 1,468,869 | 77.1× |

SWI-Prolog 9.2.9; "Your numbers will be close, not identical" (slide 27).

## Pages that use this source

Concepts: [[propositional-logic]], [[first-order-logic]], [[conjunctive-normal-form-and-resolution]], [[horn-clauses]], [[forward-chaining]], [[backward-chaining]], [[unification]], [[prolog]], [[sld-resolution]], [[negation-as-failure]], [[prolog-cut]]. Code: [[lab01-family-pl]], [[prolog-lecture-examples]]. Other: [[lab01-prolog-family-report]], [[logic-systems-comparison]], [[unit-06-logic-prolog-review]], [[history-of-ai]], [[alain-colmerauer]], [[robert-kowalski]].

## Issues found

> [!warning] Contradiction
> [[slides-01-introduction-to-ai]] (slide 9, under "1970") says Prolog is a "general-purpose programming language. Created by Dennis Ritchie at Bell Labs. It is an imperative, compiled language that provides control statements for: State Management, Decision-Making, Repetitive Tasks". That describes **C** (Ritchie, Bell Labs, early 1970s; general knowledge). This deck (slide 8) is correct: Prolog was born in Marseille in 1972 ([[alain-colmerauer]] and Philippe Roussel), on theory from [[robert-kowalski]], and it is **declarative**. R&N agrees (Ch. 9 bibliographical notes). The rest of slide 9 in Slides 01 ("Algorithm = Logic + Control", expert systems, clauses similar to FOL) is correct and is paraphrased from R&N §9.4.2. See also [[history-of-ai]].

- **Kowalski's location**: slide 8 says "Robert Kowalski in Edinburgh". R&N's notes say Imperial College London. Both fit a career move in the mid-1970s (general knowledge), so this is not a real contradiction.
- **Image-only content**: slide 3 (R&N Fig. 7.12 grammar), slide 5 (AND–OR graph, R&N Fig. 7.16) and slide 6 (Criminal(West) proof tree, R&N Fig. 9.7) show figures with no text in the extraction. The wiki rebuilds them from [[russell-norvig-aima]] §7.5.2, §7.5.4 and §9.4.1.
- **Slide 29 says "Start from 01_Code/family.pl"** and slide 31 says 01_Code "holds every program shown today, plus family.pl". Neither `family.pl` nor the slide versions of `fib/2`, `path/2`, `max/3`, `queens_perm/2`, `queens_bt/2` or `print_board/1` are in `raw/Class_exercises/01_Code/`. That folder has `factorial`, `fibonacci`, `isEven`, `isPerm`, `binaryTree`, `queens`, `predicates`, plus Raymond's lab. The only copy of `family.pl` is the slide 12 text and Raymond's extended file.
- **Slide 18 inference count**: `time(fibo(25,_))` reports 1,092,530 inferences. Re-running `fibonacci.pl` here with `statistics(inferences)` gave 1,092,533. The difference is measurement overhead.
- **Slide 22 understates the BST file.** It says the original adds redundant `empty` clauses. The file also has `delete2/3` and `inOrderSuccesor/2`, which the slide omits, and `delete2/3` has a real bug: its last clause builds `node(K, R, M)` instead of `node(K, L, M)` ([[prolog-lecture-examples]]).
- **Slide 20 and slide 21 code differs slightly from the files.** The files also carry singleton variables in `isInc([], Y)` and `isMember(X, [X|XS])` (isPerm.pl), which the slide does not flag.
- **Luger sections (slide 31)**: "Sections 14.2 and 14.3 cover Horn clause logic and Prolog". In the 6th edition, §14.2 is *Resolution Theorem Proving* and only §14.3 is *Prolog and Automated Reasoning* ([[luger-ai-6e]]).
- The syllabus places logic in units 5–6, but the deck's number ("XX") is unassigned. Its position relative to the other decks (00–04) is unknown.
