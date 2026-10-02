---
type: concept
summary: Logic with objects, relations, functions and the quantifiers ∀/∃ — expressive enough for "every" and "some", but entailment is only semidecidable.
unit: [5, 6]
tags: [logic, fol, quantifiers, knowledge-representation, kinship]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# First-order logic

**First-order logic** (FOL, the *predicate calculus*) assumes the world contains **objects** with **relations** among them and **functions** on them, and adds **variables** and the **quantifiers** $\forall$ ("for all") and $\exists$ ("there exists") so a single sentence can state a general law ([[russell-norvig-aima]] §8.1–8.2). It is step 2 of the Prolog deck: "Objects and quantifiers. Undecidable." ([[slides-xx-logic-programming-prolog]], slide 2). [[prolog]] is a restricted, executable fragment of it.

## How it works

**Vocabulary** ([[russell-norvig-aima]] §8.2.2–8.2.5):

| Element | Examples | Notes |
|---|---|---|
| Constant symbols | `John`, `Nono`, `M1` | name objects |
| Predicate symbols | `King(x)`, `Sells(x,y,z)` | relations; true/false |
| Function symbols | `LeftLeg(John)`, `Father(x)` | map objects to objects |
| Terms | `John`, `x`, `Father(Father(x))` | denote objects; **ground term** = no variables |
| Atomic sentence | `Brother(Richard, John)` | predicate applied to terms |
| Complex sentence | connectives as in [[propositional-logic]] | |
| Quantified sentence | $\forall x\ King(x) \Rightarrow Person(x)$ | |
| Equality | $Father(John) = Henry$ | two terms, same object |

**Quantifier rules of thumb** ([[russell-norvig-aima]] §8.2.6):

- $\forall$ goes with $\Rightarrow$: $\forall x\ King(x) \Rightarrow Person(x)$. Writing $\forall x\ King(x) \wedge Person(x)$ claims *everything* is a king.
- $\exists$ goes with $\wedge$: $\exists x\ Crown(x) \wedge OnHead(x, John)$. Writing $\exists x\ Crown(x) \Rightarrow OnHead(x,John)$ is true as soon as anything is not a crown.
- Order matters: $\forall x \exists y\ Loves(x,y)$ ("everybody loves somebody") $\neq$ $\exists y \forall x\ Loves(x,y)$ ("someone is loved by all").
- De Morgan for quantifiers: $\neg \exists x\ P \equiv \forall x\ \neg P$, $\neg \forall x\ P \equiv \exists x\ \neg P$.

**Kinship axioms** ([[russell-norvig-aima]] §8.3.2), the textbook version of Raymond's lab:

$$\forall g,c\ \ Grandparent(g,c) \Leftrightarrow \exists p\ Parent(g,p) \wedge Parent(p,c)$$
$$\forall x,y\ \ Sibling(x,y) \Leftrightarrow x \neq y \wedge \exists p\ Parent(p,x) \wedge Parent(p,y)$$

The $x \neq y$ is exactly the `X \= Y` in `sibling/2` ([[lab01-family-pl]]). R&N §8.2.7 makes the same point: $\exists x,y\ Brother(x,Richard) \wedge Brother(y,Richard)$ does *not* say Richard has two brothers unless you add $\neg(x = y)$.

**Inference** ([[russell-norvig-aima]] Ch. 9): Universal Instantiation (substitute any ground term), Existential Instantiation (introduce a fresh **Skolem constant**), **propositionalization** (§9.1), and the *lifted* rules built on [[unification]]: Generalized Modus Ponens, [[forward-chaining]], [[backward-chaining]], and [[conjunctive-normal-form-and-resolution|resolution]].

## Properties

- **Semidecidable**: an algorithm can say *yes* to every entailed sentence, but no algorithm can say *no* to every non-entailed one (Turing 1936, Church 1936) ([[russell-norvig-aima]] §9.1.1). Function symbols make the Herbrand universe infinite (`Father(Father(…))`).
- **Standard semantics vs database semantics**: standard FOL does not assume different names mean different objects, nor that unstated facts are false. **Database semantics** adds the unique-names assumption, the **closed-world assumption** and domain closure ([[russell-norvig-aima]] §8.2.8) — this is what Prolog uses ([[negation-as-failure]]).
- **Ontological commitment**: facts, objects, relations; epistemological: true/false/unknown ([[russell-norvig-aima]] Fig. 8.1).

## In this course

- Slide 7 shows the West crime rule twice — in FOL ($\forall x,y,z\ American(x) \wedge Weapon(y) \wedge Sells(x,y,z) \wedge Hostile(z) \Rightarrow Criminal(x)$) and in Prolog — and lists four translation conventions: implication written backwards, inverted case, implicit $\forall$, `,` = and / `;` = or / `.` ends a clause ([[slides-xx-logic-programming-prolog]], slide 7).
- R&N itself notes FOL convention uses lowercase variables and Prolog uses uppercase — "the opposite of our convention" ([[russell-norvig-aima]] §8.2.6, §9.4.2).
- Luger's clause-form procedure (9 steps including skolemization) is the FOL→clauses bridge ([[luger-ai-6e]] §14.2.2); see [[conjunctive-normal-form-and-resolution]].
- Lab 01 is a FOL kinship KB written in Prolog: [[lab01-family-pl]].

## Common mistakes

- $\forall$ with $\wedge$, or $\exists$ with $\Rightarrow$ (see above) — R&N calls the first one "a common mistake, made frequently even by diligent readers".
- Swapping quantifier order.
- Forgetting $x \neq y$ when the English implies "two different …".
- Assuming FOL has a closed world. In FOL, `Course(CS,101), Course(CS,102)` says "between one and infinitely many courses" ([[russell-norvig-aima]] §9.4.4).

## Related

[[propositional-logic]] · [[horn-clauses]] · [[unification]] · [[prolog]] · [[negation-as-failure]] · [[logic-systems-comparison]] · [[unit-06-logic-prolog-review]]

## Practice questions

> [!question]- Q1. Translate "Every student who studies passes some exam" into FOL.
> **Answer.** $\forall s\ [Student(s) \wedge Studies(s)] \Rightarrow \exists e\ [Exam(e) \wedge Passes(s,e)]$. Universal with $\Rightarrow$, existential with $\wedge$ ([[russell-norvig-aima]] §8.2.6).

> [!question]- Q2. What is wrong with $\forall x\ Student(x) \wedge Smart(x)$ as "all students are smart"?
> **Answer.** It says every object in the domain is a student *and* smart. The intended sentence is $\forall x\ Student(x) \Rightarrow Smart(x)$ ([[russell-norvig-aima]] §8.2.6).

> [!question]- Q3. Write the FOL sentence for "Richard has at least two brothers" and explain the role of the last conjunct.
> **Answer.** $\exists x,y\ Brother(x,Richard) \wedge Brother(y,Richard) \wedge \neg(x = y)$. Without $\neg(x=y)$ the sentence holds when $x$ and $y$ both name the same single brother ([[russell-norvig-aima]] §8.2.7). Same reason `sibling/2` needs `X \= Y` ([[lab01-prolog-family-report]]).

> [!question]- Q4. Why is FOL entailment only semidecidable when propositional entailment is decidable?
> **Answer.** With function symbols there are infinitely many ground terms. By Herbrand's theorem a proof, if it exists, uses a finite subset, so a search that grows term depth eventually finds it. If no proof exists the search may never stop, and Turing and Church showed no procedure can always detect that ([[russell-norvig-aima]] §9.1.1).

> [!question]- Q5. Push the negation inward: $\neg \forall x\ \exists y\ Loves(x,y)$.
> **Answer.** $\exists x\ \neg \exists y\ Loves(x,y) \equiv \exists x\ \forall y\ \neg Loves(x,y)$ — "someone loves nobody" ([[russell-norvig-aima]] §8.2.6, De Morgan for quantifiers).
