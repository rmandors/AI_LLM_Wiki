---
type: concept
summary: Every sentence can be rewritten as a conjunction of clauses (CNF); resolution, a single rule that cancels complementary literals, is refutation-complete on clauses and underlies Prolog.
unit: [5, 6]
tags: [logic, cnf, resolution, theorem-proving, skolemization]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Conjunctive normal form and resolution

A **literal** is a symbol or its negation; a **clause** is a disjunction of literals; a sentence is in **conjunctive normal form (CNF)** when it is a conjunction of clauses ([[slides-xx-logic-programming-prolog]], slide 3). Every propositional sentence is *logically equivalent* to a CNF sentence, and every first-order sentence has an *inferentially equivalent* CNF (satisfiable iff the original is) ([[russell-norvig-aima]] §7.5.2, §9.5.1). **Resolution** is the inference rule that works on clauses: from two clauses with complementary literals, derive a clause with everything else. Used as **refutation** (add $\neg$goal, derive the empty clause), it is complete — which is why the slides say resolution "needs clause form as input" ([[slides-xx-logic-programming-prolog]], slide 3).

## How it works

### Propositional CNF conversion ([[russell-norvig-aima]] §7.5.2)

1. Eliminate $\Leftrightarrow$: $\alpha \Leftrightarrow \beta \to (\alpha \Rightarrow \beta) \wedge (\beta \Rightarrow \alpha)$.
2. Eliminate $\Rightarrow$: $\alpha \Rightarrow \beta \to \neg\alpha \vee \beta$.
3. Move $\neg$ inwards (double negation, De Morgan).
4. Distribute $\vee$ over $\wedge$.

Worked (R&N's example): $B_{1,1} \Leftrightarrow (P_{1,2} \vee P_{2,1})$
→ $(B_{1,1} \Rightarrow (P_{1,2} \vee P_{2,1})) \wedge ((P_{1,2} \vee P_{2,1}) \Rightarrow B_{1,1})$
→ $(\neg B_{1,1} \vee P_{1,2} \vee P_{2,1}) \wedge (\neg(P_{1,2} \vee P_{2,1}) \vee B_{1,1})$
→ $(\neg B_{1,1} \vee P_{1,2} \vee P_{2,1}) \wedge ((\neg P_{1,2} \wedge \neg P_{2,1}) \vee B_{1,1})$
→ $(\neg B_{1,1} \vee P_{1,2} \vee P_{2,1}) \wedge (\neg P_{1,2} \vee B_{1,1}) \wedge (\neg P_{2,1} \vee B_{1,1})$.

### First-order CNF (R&N §9.5.1; Luger's 9 steps, [[luger-ai-6e]] §14.2.2)

1. Eliminate implications. 2. Move $\neg$ inwards (also $\neg\forall x\,p \to \exists x\,\neg p$, $\neg\exists x\,p \to \forall x\,\neg p$). 3. Standardize variables apart. 4. (Luger) Move quantifiers to the front — *prenex* form. 5. **Skolemize**: replace each $\exists$ variable by a Skolem constant, or by a **Skolem function** of the enclosing $\forall$ variables — $\forall X \exists Y\ mother(X,Y)$ becomes $\forall X\ mother(X, m(X))$. 6. Drop $\forall$. 7. Distribute $\vee$ over $\wedge$. 8. Split into separate clauses. 9. Standardize apart again.

R&N's example, "Everyone who loves all animals is loved by someone", $\forall x\,[\forall y\ Animal(y) \Rightarrow Loves(x,y)] \Rightarrow [\exists y\ Loves(y,x)]$, ends as
$[Animal(F(x)) \vee Loves(G(x),x)] \wedge [\neg Loves(x,F(x)) \vee Loves(G(x),x)]$ ([[russell-norvig-aima]] §9.5.1).

### The resolution rule

$$\frac{\ell_1 \vee \dots \vee \ell_k, \quad m_1 \vee \dots \vee m_n}{\ell_1 \vee \dots \ell_{i-1} \vee \ell_{i+1} \dots \vee \ell_k \vee m_1 \vee \dots m_{j-1} \vee m_{j+1} \dots \vee m_n}\quad (\ell_i = \neg m_j)$$

Resolve one complementary pair at a time; remove duplicate literals (**factoring**) ([[russell-norvig-aima]] §7.5.2). In FOL, the two literals need only *unify*: apply the MGU from [[unification]] to the resolvent (binary resolution, [[luger-ai-6e]] §14.2.3).

**PL-RESOLUTION** (R&N Fig. 7.13): convert $KB \wedge \neg\alpha$ to clauses; repeatedly add resolvents; if the empty clause appears, $KB \models \alpha$; if nothing new can be added, $KB \not\models \alpha$.

Luger's FOL example: $\neg dog(X) \vee animal(X)$, $\neg animal(Y) \vee die(Y)$, $dog(fido)$, negated goal $\neg die(fido)$. Resolve first two with $\{Y/X\}$ → $\neg dog(Y) \vee die(Y)$; with $dog(fido)$, $\{fido/Y\}$ → $die(fido)$; with $\neg die(fido)$ → empty clause ([[luger-ai-6e]] §14.2.1, Fig. 14.3).

## Properties

- **Sound**; **refutation-complete** — if $S$ is unsatisfiable, its resolution closure contains the empty clause (ground resolution theorem, [[russell-norvig-aima]] §7.5.2). Not complete for *generating* every consequence ([[luger-ai-6e]] §14.2.1).
- Propositional resolution always terminates (finitely many clauses over $k$ symbols); FOL resolution is a semidecision procedure ([[first-order-logic]]).
- Worst case exponential — the clause set can blow up. CNF conversion can also blow up through distribution.
- **Horn clauses are closed under resolution** — resolving two Horn clauses gives a Horn clause ([[russell-norvig-aima]] §7.5.3). Restricting to Horn clauses plus a fixed search order gives [[sld-resolution]], i.e. [[prolog]].

## In this course

- Slide 3: literal / clause / CNF definitions; "the rewriting is an equivalence: nothing is lost"; resolution is "refutation-complete for propositional logic" and needs clause form; the CNF grammar (R&N Fig. 7.12) names definite and goal clauses ([[slides-xx-logic-programming-prolog]], slide 3).
- Slide 4: a clause like $P \vee Q$ has two positive literals, so it has no Horn form — "the price of tractability" ([[slides-xx-logic-programming-prolog]], slide 4).
- Luger presents the Prolog interpreter as resolution with a unit-preference, linear-input, left-to-right depth-first strategy ([[luger-ai-6e]] §14.3.2).

## Common mistakes

- Resolving two pairs at once: from $P \vee \neg Q \vee R$ and $\neg P \vee Q$ you may *not* infer $R$ ([[russell-norvig-aima]] §7.5.2).
- Skolemizing with a constant when the $\exists$ is inside a $\forall$ — it must be a function of the outer variables.
- Forgetting to negate the goal before adding it (resolution proves by contradiction).
- Calling CNF "equivalent" in FOL — after skolemization it is only *equisatisfiable* ([[luger-ai-6e]] §14.2.2).

## Related

[[propositional-logic]] · [[first-order-logic]] · [[horn-clauses]] · [[unification]] · [[sld-resolution]] · [[logic-systems-comparison]]

## Practice questions

> [!question]- Q1. Convert $(A \vee B) \Rightarrow C$ to CNF. Are the clauses Horn? Write them in Prolog.
> **Answer.** $\neg(A \vee B) \vee C \to (\neg A \wedge \neg B) \vee C \to (\neg A \vee C) \wedge (\neg B \vee C)$. Each clause has exactly one positive literal, so both are definite clauses: `c:- a.` and `c:- b.`

> [!question]- Q2. Convert $A \Rightarrow (B \vee C)$ to CNF. Can Prolog express it?
> **Answer.** $\neg A \vee B \vee C$: two positive literals, so it is not Horn. Prolog cannot state "if A then B or C, I don't know which" ([[slides-xx-logic-programming-prolog]], slide 4).

> [!question]- Q3. Use resolution to prove $R$ from $P \Rightarrow Q$, $Q \Rightarrow R$, $P$.
> **Answer.** Clauses: $\neg P \vee Q$, $\neg Q \vee R$, $P$, and negated goal $\neg R$. $\neg R$ with $\neg Q \vee R$ → $\neg Q$; with $\neg P \vee Q$ → $\neg P$; with $P$ → empty clause. Hence $KB \models R$.

> [!question]- Q4. Skolemize $\forall x\ \exists y\ \forall z\ \exists w\ P(x,y,z,w)$.
> **Answer.** $\forall x\,\forall z\ P(x, F(x), z, G(x,z))$: $y$ depends only on $x$; $w$ is inside both $\forall x$ and $\forall z$ ([[luger-ai-6e]] §14.2.2; [[russell-norvig-aima]] §9.5.1).

> [!question]- Q5. Why is it valid to drop the clause $B_{1,1} \vee \neg B_{1,1} \vee P_{1,2}$ during resolution?
> **Answer.** It contains a complementary pair, so it is equivalent to True and can never help derive the empty clause ([[russell-norvig-aima]] §7.5.2).
