---
type: concept
summary: The simplest logic — proposition symbols joined by five connectives, truth defined by truth tables; decidable (entailment is co-NP-complete) but unable to talk about objects or say "every".
unit: [5, 6]
tags: [logic, knowledge-representation, entailment, truth-tables]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Propositional logic

**Propositional logic** (the *propositional calculus*) is a language whose atomic sentences are **proposition symbols** — $P$, $Q$, $B_{1,1}$ — each of which is simply true or false. Complex sentences are built with connectives, and the meaning of a sentence in a **model** (an assignment of true/false to every symbol) is computed mechanically from truth tables ([[russell-norvig-aima]] §7.4). It is the first rung of the ladder the Prolog deck climbs: "connectives and truth tables, but no objects … Decidable, but it cannot say 'every'" ([[slides-xx-logic-programming-prolog]], slide 2).

## How it works

**Syntax** ([[russell-norvig-aima]] §7.4.1). Five connectives, in precedence order from highest to lowest:

| Connective | Name | Example |
|---|---|---|
| $\neg$ | negation | $\neg W_{1,3}$ |
| $\wedge$ | conjunction | $W_{1,3} \wedge P_{3,1}$ |
| $\vee$ | disjunction | $(W_{1,3} \wedge P_{3,1}) \vee W_{2,2}$ |
| $\Rightarrow$ | implication | $(W_{1,3} \wedge P_{3,1}) \Rightarrow \neg W_{2,2}$ |
| $\Leftrightarrow$ | biconditional | $W_{1,3} \Leftrightarrow \neg W_{2,2}$ |

**Semantics** ([[russell-norvig-aima]] §7.4.2, Fig. 7.8). $P \Rightarrow Q$ is false *only* when $P$ is true and $Q$ is false; $P \Leftrightarrow Q$ is true when both sides have the same value.

**Core vocabulary** ([[russell-norvig-aima]] §7.3, §7.5):

- **Entailment** $\alpha \models \beta$: $\beta$ is true in every model where $\alpha$ is true, i.e. $M(\alpha) \subseteq M(\beta)$.
- **Logical equivalence** $\alpha \equiv \beta$: same models (Fig. 7.11 lists the standard ones: De Morgan, contraposition, implication elimination, distributivity …).
- **Valid** (tautology): true in all models, e.g. $P \vee \neg P$. **Satisfiable**: true in some model.
- **Deduction theorem**: $\alpha \models \beta$ iff $(\alpha \Rightarrow \beta)$ is valid.
- **Refutation**: $\alpha \models \beta$ iff $(\alpha \wedge \neg \beta)$ is unsatisfiable — the basis of [[conjunctive-normal-form-and-resolution|resolution]].
- **Sound** inference derives only entailed sentences; **complete** inference derives every entailed sentence (§7.3).

**Inference by model checking** — TT-ENTAILS? enumerates all $2^n$ models depth-first (Fig. 7.10): sound and complete, $O(2^n)$ time, $O(n)$ space (§7.4.4).

**Inference by theorem proving** — apply rules such as Modus Ponens ($\alpha \Rightarrow \beta,\ \alpha \vdash \beta$) and And-Elimination (§7.5.1), or the single rule of resolution on clauses (§7.5.2).

## Properties

- **Decidable**: there are finitely many models, so entailment can always be settled ([[slides-xx-logic-programming-prolog]], slide 2).
- **Hard in the worst case**: propositional entailment is co-NP-complete; SAT was the first problem proved NP-complete ([[russell-norvig-aima]] §7.4.4, §7.5).
- **Cheap fragment**: for [[horn-clauses|Horn / definite clauses]], entailment is linear in the KB size via [[forward-chaining]] or [[backward-chaining]] ([[russell-norvig-aima]] §7.5.3).
- **Ontological commitment**: only *facts* that are true or false — no objects, no relations ([[russell-norvig-aima]] §8.1, Fig. 8.1). "All kings are persons" needs one symbol per king.

## In this course

- The Prolog deck opens with propositional logic as step 1 of four (propositional → [[first-order-logic|first-order]] → [[horn-clauses]] → [[prolog]]) ([[slides-xx-logic-programming-prolog]], slide 2).
- CNF and the clause grammar (R&N Fig. 7.12) are introduced on slide 3; Horn clauses as the tractable subset on slides 4–5 ([[slides-xx-logic-programming-prolog]]).
- The seven-clause AND–OR graph on slide 5 (R&N Fig. 7.16) is a propositional definite-clause KB; Prolog "explores exactly this graph — depth first, left to right".
- Connection to CSPs: every finite [[constraint-satisfaction-problems|CSP]] is a satisfiability question ([[russell-norvig-aima]] §7.5).

## Common mistakes

- Reading $P \Rightarrow Q$ as causation. It is just $\neg P \vee Q$; a false premise makes it true.
- Confusing $\equiv$ / $\models$ (claims *about* sentences) with $\Leftrightarrow$ / $\Rightarrow$ (symbols *inside* sentences) ([[russell-norvig-aima]] §7.5).
- Thinking "decidable" means "fast": the truth table is $2^n$ rows.
- Trying to express "every person has a parent" — impossible without objects and quantifiers; that is what [[first-order-logic]] adds.

## Related

[[first-order-logic]] · [[conjunctive-normal-form-and-resolution]] · [[horn-clauses]] · [[forward-chaining]] · [[backward-chaining]] · [[logic-systems-comparison]] · [[unit-06-logic-prolog-review]]

## Practice questions

> [!question]- Q1. Is $(P \Rightarrow Q) \Leftrightarrow (\neg Q \Rightarrow \neg P)$ valid, satisfiable, or unsatisfiable?
> **Answer.** Valid: it is the contraposition equivalence of R&N Fig. 7.11, so both sides have the same truth value in all four models ([[russell-norvig-aima]] §7.5).

> [!question]- Q2. A KB has 20 proposition symbols. How many rows does TT-ENTAILS? check, and why is it still "decidable"?
> **Answer.** $2^{20} = 1{,}048{,}576$ models. It is decidable because the number is finite; the algorithm always terminates, just slowly — $O(2^n)$ time, $O(n)$ space ([[russell-norvig-aima]] §7.4.4).

> [!question]- Q3. Show by refutation that $\{P \Rightarrow Q,\ P\} \models Q$.
> **Answer.** Check that $KB \wedge \neg Q$ is unsatisfiable. Clauses: $\neg P \vee Q$, $P$, $\neg Q$. Resolve $\neg P \vee Q$ with $P$ → $Q$; resolve $Q$ with $\neg Q$ → empty clause. Contradiction, so the entailment holds ([[russell-norvig-aima]] §7.5.2).

> [!question]- Q4. Why can't propositional logic write "every American who sells weapons to a hostile nation is a criminal" as one sentence?
> **Answer.** It has no variables or quantifiers. You would need a separate symbol (and rule) for every person/weapon/nation combination. [[first-order-logic]] writes it once with $\forall x,y,z$ ([[slides-xx-logic-programming-prolog]], slide 7; [[russell-norvig-aima]] §8.1).

> [!question]- Q5. Which connective is the "main" one in $\neg A \vee B \Rightarrow C$, given R&N's precedence?
> **Answer.** $\Rightarrow$. Precedence is $\neg$, then $\wedge$, $\vee$, $\Rightarrow$, $\Leftrightarrow$, so it parses as $((\neg A) \vee B) \Rightarrow C$ ([[russell-norvig-aima]] §7.4.1).
