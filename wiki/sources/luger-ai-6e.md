---
type: source
summary: Luger, Artificial Intelligence — Structures and Strategies for Complex Problem Solving, 6th ed. — secondary textbook; §14.2 (resolution, clause form) and §14.3 (Horn clauses, logic programs, Prolog semantics, closed world) read so far.
unit: [5, 6]
tags: [textbook, prolog, resolution, horn-clauses, automated-reasoning]
sources: ["[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Luger — *Artificial Intelligence*, 6th edition

**Bibliographic line.** George F. Luger, *Artificial Intelligence: Structures and Strategies for Complex Problem Solving*, 6th ed., Addison-Wesley/Pearson, 2009 (publisher and year are general knowledge). Raw file: `raw/Books/Artificial Intelligence - 6th Edition.pdf`.

**What it is.** The course's secondary textbook for logic and Prolog (per the wiki schema in `AGENTS.md` and [[slides-xx-logic-programming-prolog]], slide 31). Chapter 14, *Automated Reasoning*, treats resolution theorem proving and Prolog as automated reasoning. Luger uses uppercase for variables and lowercase for constants, which is already Prolog convention (§14.2.2).

## Sections read

| Section | Book pages | Read on | Used for |
|---|---|---|---|
| §14.2.1 Introduction (resolution) | 582–584 | 2026-10-01 | refutation steps, "fido will die" example |
| §14.2.2 Producing the clause form | 584–589 | 2026-10-01 | 9-step CNF / skolemization |
| §14.2.3 Binary resolution (first paragraph only) | 589 | 2026-10-01 | — |
| §14.3.1 Introduction | 603–604 | 2026-10-01 | procedural information lost in clause form |
| §14.3.2 Logic Programming and Prolog | 604–609 | 2026-10-01 | Horn forms, logic program definition, goal reduction, cut, CWA axioms |

Not yet read: §14.0–14.1 (GPS), §14.2.3–14.2.5 in full (resolution strategies, answer extraction), §14.4, and the earlier Prolog chapters.

## Key points

**§14.2 Resolution theorem proving**
- Resolution (Robinson 1965) is sound and **refutation complete**, but not complete for generating every consequence (§14.2.1).
- Refutation in 5 steps: clause form → add negated goal → resolve → empty clause → the substitutions give the answer (§14.2.1).
- "Fido will die": $\neg dog(X) \vee animal(X)$, $\neg animal(Y) \vee die(Y)$, $dog(fido)$, $\neg die(fido)$ → empty clause (Fig. 14.3).
- **Nine-step clause form** (§14.2.2): eliminate →; reduce scope of ¬; standardize variables; move quantifiers left (prenex); skolemize (`(∀X)(∃Y) mother(X,Y)` → `(∀X) mother(X, m(X))`); drop ∀; distribute ∨ over ∧; split clauses; standardize apart again. Skolemization preserves unsatisfiability, not equivalence (Chang & Lee 1973).

**§14.3 Prolog and automated reasoning**
- Clause form throws away *procedural* hints. Writing `a ← b ∧ ¬c ∧ d` says "test b first", which encodes heuristic knowledge ("test the easiest way to falsify the problem first") (§14.3.1, citing Kowalski 1979b).
- **Horn clause**: at most one positive literal. Written $a \leftarrow b_1 \wedge \dots \wedge b_n$. Three forms: headless clause (goals), facts, rule relations. $p \vee q$ has no Horn form (§14.3.2).
- **Logic program** = set of universally quantified Horn clauses + nondeterministic goal reduction. Refutation-complete with linear-input, unit-preference, left-to-right depth-first reduction, *given* well-founded recursion and occurs checking (van Emden & Kowalski 1976) (§14.3.2).
- **Sequential Prolog** fixes goal order (left to right) and clause order (program order). The goal list is a stack (depth first), and backtracking restores bindings to the latest choicepoint (§14.3.2). See [[sld-resolution]].
- **Cut** commits to the current clause and its bindings; failure after the cut fails the clause; some interpretations are never computed (§14.3.2). See [[prolog-cut]].
- Resolution with unit preference + linear input + left-to-right depth-first *is* a Prolog interpreter; the composed unifiers are the answer (§14.3.2).
- **Closed world**: three implicit axioms, unique name, closed world ($p(X) \rightarrow p(a_1) \vee \dots \vee p(a_n)$) and domain closure. "Prolog assumes as false all goals that it cannot prove to be true." Other departures: no occurs check, cut (§14.3.2). See [[negation-as-failure]].

## Pages that use this source

[[propositional-logic]] · [[first-order-logic]] · [[conjunctive-normal-form-and-resolution]] · [[horn-clauses]] · [[backward-chaining]] · [[unification]] · [[prolog]] · [[sld-resolution]] · [[negation-as-failure]] · [[prolog-cut]] · [[logic-systems-comparison]] · [[unit-06-logic-prolog-review]]

## Issues found

- **Running headers say "CHAPTER 13 / AUTOMATED REASONING"** on pages whose sections are numbered 14.x (e.g. pp. 583, 605, 607). This looks like a typesetting artifact. The table of contents lists Chapter 14 as Automated Reasoning; cite section numbers.
- **Dangling cross-reference**: §14.3.2 twice refers to "Section 14.1.5" for the cut and depth-first backtracking, but §14.1 in this edition is the General Problem Solver. The intended reference is probably the Prolog chapter earlier in the book (not read).
- **Slide 31 vs book contents**: the deck says §14.2 and §14.3 "cover Horn clause logic and Prolog". In fact §14.2 is general resolution theorem proving; Horn clauses and Prolog are in §14.3.
- **PDF page offset**: book page 604 sits at PDF page 629 (offset +25 in this part of the book), unlike R&N's +1.
