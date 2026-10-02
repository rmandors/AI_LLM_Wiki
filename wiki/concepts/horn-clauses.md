---
type: concept
summary: Clauses with at most one positive literal — definite clauses (rules), facts and goal clauses; they read as implications and make entailment linear-time (propositional), which is why Prolog is built on them.
unit: [5, 6]
tags: [logic, horn-clauses, definite-clauses, prolog]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Horn clauses

A **Horn clause** is a clause (disjunction of literals) with **at most one positive literal** ([[slides-xx-logic-programming-prolog]], slide 4; [[russell-norvig-aima]] §7.5.3). That one restriction makes every clause readable as an implication with a conjunctive body and a single conclusion, makes [[forward-chaining|forward]] and [[backward-chaining]] natural, and makes propositional entailment linear in the size of the knowledge base. A [[prolog]] program is a set of first-order Horn clauses.

## How it works

The three shapes ([[slides-xx-logic-programming-prolog]], slide 4; [[luger-ai-6e]] §14.3.2):

| Shape | Clause form | Implication form | Prolog | Role |
|---|---|---|---|---|
| **Definite clause** (rule) | $\neg A \vee \neg B \vee C$ | $A \wedge B \Rightarrow C$ | `c:- a, b.` | exactly one positive literal |
| **Fact** | $C$ | $True \Rightarrow C$ | `c.` | definite clause, empty body |
| **Goal clause** | $\neg A \vee \neg B$ | $A \wedge B \Rightarrow False$ | `?- a, b.` | no positive literal: a query |

Vocabulary: the positive literal is the **head**, the negative literals form the **body** ([[russell-norvig-aima]] §7.5.3). Luger calls the three forms "headless clause (goals to be tried)", "facts" and "rule relation" ([[luger-ai-6e]] §14.3.2).

**Turning a clause into Horn form** (Luger): move the single positive literal to the front, rewrite $a \vee \neg b_1 \vee \dots \vee \neg b_n$ as $a \Leftarrow \neg(\neg b_1 \vee \dots \vee \neg b_n)$, then De Morgan gives $a \Leftarrow b_1 \wedge \dots \wedge b_n$ ([[luger-ai-6e]] §14.3.2).

Grammar (R&N Fig. 7.12, shown on [[slides-xx-logic-programming-prolog]], slide 3):

```
HornClauseForm → DefiniteClauseForm | GoalClauseForm
DefiniteClauseForm → Fact | (Symbol1 ∧ … ∧ Symboll) ⇒ Symbol
GoalClauseForm → (Symbol1 ∧ … ∧ Symboll) ⇒ False
```

## Properties

- **Readable**: "$\neg L \vee \neg B \vee M$ is hard to parse; $L \wedge B \Rightarrow M$ is not" ([[slides-xx-logic-programming-prolog]], slide 5).
- **Closed under resolution**: resolving two Horn clauses gives a Horn clause ([[russell-norvig-aima]] §7.5.3).
- **Linear-time propositional entailment** with [[forward-chaining]] (PL-FC-ENTAILS?) or [[backward-chaining]] ([[russell-norvig-aima]] §7.5.4).
- **First-order**: definite-clause entailment stays *semidecidable* (function symbols), but the search is "far cheaper than full resolution" ([[slides-xx-logic-programming-prolog]], slide 5; [[russell-norvig-aima]] §9.3.2). With no function symbols (**Datalog**) forward chaining reaches a fixed point after at most $p\,n^k$ facts ($p$ predicates, $n$ constants, max arity $k$) ([[russell-norvig-aima]] §9.3.2).
- **Less expressive**: no disjunctive conclusions ($P \vee Q$ has no Horn form) and no way to assert a negative fact ([[slides-xx-logic-programming-prolog]], slide 4; [[russell-norvig-aima]] §9.4.4). Prolog compensates for negation with [[negation-as-failure]].
- **Refutation-complete** with left-to-right, depth-first goal reduction *if* recursion is well-founded and the occurs check is on ([[luger-ai-6e]] §14.3.2, citing van Emden & Kowalski 1976).

## In this course

- Slide 2: step 3 of the deck, "At most one positive literal. Cheap entailment."
- Slide 4: definitions and the three-way table above, plus "Prolog cannot say 'one of these, I do not know which'".
- Slide 5: three reasons definite-clause KBs matter, and the seven-clause AND–OR graph (R&N Fig. 7.16): $P \Rightarrow Q$, $L \wedge M \Rightarrow P$, $B \wedge L \Rightarrow M$, $A \wedge P \Rightarrow L$, $A \wedge B \Rightarrow L$, $A$, $B$ ([[slides-xx-logic-programming-prolog]], slide 5; [[russell-norvig-aima]] §7.5.4).
- Every clause in [[lab01-family-pl]] and [[prolog-lecture-examples]] is a definite clause; every `?-` query is a goal clause.

## Common mistakes

- Thinking "Horn" means "exactly one positive literal" — that is a *definite* clause. Goal clauses (zero positive) are Horn too.
- Counting literals in the implication form: $A \wedge B \Rightarrow C$ has *one* positive literal ($C$); $A$ and $B$ become negative.
- Believing `\+` turns Prolog into full FOL; it is negation as failure, not classical negation.

## Related

[[propositional-logic]] · [[first-order-logic]] · [[conjunctive-normal-form-and-resolution]] · [[forward-chaining]] · [[backward-chaining]] · [[sld-resolution]] · [[prolog]] · [[logic-systems-comparison]]

## Practice questions

> [!question]- Q1. Classify each clause: (a) $\neg P \vee \neg Q \vee R$, (b) $P \vee Q$, (c) $\neg P \vee \neg Q$, (d) $R$, (e) $P \vee \neg Q \vee R$.
> **Answer.** (a) definite (rule $P \wedge Q \Rightarrow R$); (b) not Horn (two positives); (c) goal clause (Horn, $P \wedge Q \Rightarrow False$); (d) fact; (e) not Horn (two positives, $P$ and $R$).

> [!question]- Q2. Write $\forall x\ Missile(x) \wedge Owns(Nono,x) \Rightarrow Sells(West,x,Nono)$ in clause form and in Prolog.
> **Answer.** Clause: $\neg Missile(x) \vee \neg Owns(Nono,x) \vee Sells(West,x,Nono)$ — one positive literal, definite. Prolog: `sells(west, X, nono):- missile(X), owns(nono, X).` ([[slides-xx-logic-programming-prolog]], slide 7; [[russell-norvig-aima]] Eq. 9.6).

> [!question]- Q3. Why does a query `?- a, b.` correspond to the clause $\neg a \vee \neg b$?
> **Answer.** Prolog proves the query by refutation: it adds the negated goal $\neg(a \wedge b) \equiv \neg a \vee \neg b$ — a goal clause — and tries to derive the empty clause ([[luger-ai-6e]] §14.3.2).

> [!question]- Q4. "Every person is male or female" — can this go in a Prolog KB as a rule?
> **Answer.** Not as stated: $Person(x) \Rightarrow Male(x) \vee Female(x)$ has two positive literals. Prolog can only go the other way (`person(P):- male(P).` `person(P):- female(P).`), which is what [[lab01-family-pl]] does (lines 97–98).
