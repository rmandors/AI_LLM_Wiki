---
type: concept
summary: Data-driven inference for definite clauses — fire every rule whose premises are known, add its conclusion, repeat to a fixed point; sound, complete, linear-time in the propositional case.
unit: [5, 6]
tags: [logic, inference, forward-chaining, data-driven, horn-clauses]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Forward chaining

**Forward chaining** starts from the known facts and repeatedly applies Modus Ponens: whenever every premise of a definite clause is known, its conclusion is added to the set of known facts. It stops when the query is derived or nothing new can be added (a **fixed point**). It is **data-driven** reasoning, the opposite of goal-directed [[backward-chaining]] ([[russell-norvig-aima]] §7.5.4; [[slides-xx-logic-programming-prolog]], slide 5: "Forward, from facts to query").

## How it works

**Propositional: PL-FC-ENTAILS?(KB, q)** ([[russell-norvig-aima]] Fig. 7.15):

```
count[c] ← number of premises of clause c
inferred[s] ← false for every symbol
queue ← symbols known true in KB
while queue not empty:
    p ← POP(queue)
    if p = q: return true
    if not inferred[p]:
        inferred[p] ← true
        for each clause c with p in its premise:
            count[c] ← count[c] − 1
            if count[c] = 0: push c.CONCLUSION onto queue
return false
```

The `inferred` table stops loops caused by clauses such as $P \Rightarrow Q$ and $Q \Rightarrow P$.

**First-order: FOL-FC-ASK** ([[russell-norvig-aima]] Fig. 9.3): in each round, for each rule, find every substitution $\theta$ (via [[unification]]) that makes the premises match known facts, add $\text{SUBST}(\theta, q)$ if it is not a renaming of a known fact, and stop when the query unifies with a new fact or no fact is new. Each step is **Generalized Modus Ponens**:

$$\frac{p_1', \dots, p_n', \quad (p_1 \wedge \dots \wedge p_n \Rightarrow q)}{\text{SUBST}(\theta, q)} \quad \text{where } \text{SUBST}(\theta,p_i') = \text{SUBST}(\theta,p_i)$$

**Crime example** (R&N §9.3.2), the same KB as the Prolog version on [[slides-xx-logic-programming-prolog]], slide 7:

- Round 1: $Missile(x) \wedge Owns(Nono,x) \Rightarrow Sells(West,x,Nono)$ fires with $\{x/M1\}$; $Missile(x) \Rightarrow Weapon(x)$ gives $Weapon(M1)$; $Enemy(x,America) \Rightarrow Hostile(x)$ gives $Hostile(Nono)$.
- Round 2: the criminal rule fires with $\{x/West, y/M1, z/Nono\}$ → $Criminal(West)$. Then a fixed point is reached.

## Properties

| Property | Value |
|---|---|
| Sound | Yes — every step is (Generalized) Modus Ponens |
| Complete | Yes, for definite clauses: every entailed atomic sentence is derived ([[russell-norvig-aima]] §7.5.4, §9.3.2) |
| Time (propositional) | Linear in KB size ([[russell-norvig-aima]] §7.5.4) |
| Datalog | Terminates: at most $p\,n^k$ ground facts ($p$ predicates, $n$ constants, max arity $k$) |
| With function symbols | Semidecidable — may run forever on a non-entailed query (Peano $NatNum(S(S(\dots)))$) ([[russell-norvig-aima]] §9.3.2) |
| Matching cost | Matching rule premises to facts is a CSP, NP-hard in general; cheap in practice since rules are small ([[russell-norvig-aima]] §9.3.3) |
| Weakness | Derives *everything*, including irrelevant facts |

Forward chaining does **not** suffer from Prolog's infinite left-recursion loop: on `link(a,b), link(b,c)` it derives `path(a,b)`, `path(b,c)`, `path(a,c)` and halts ([[russell-norvig-aima]] §9.4.3). That is why it is a form of dynamic programming, and why tabling in Prolog borrows its idea.

## In this course

- Slide 5 contrasts the two chaining directions and shows the AND–OR graph of R&N Fig. 7.16; forward chaining propagates up that graph from the known leaves $A$, $B$ ([[slides-xx-logic-programming-prolog]], slide 5).
- The course's executable logic, [[prolog]], uses the *other* direction ([[backward-chaining]]); `:- table` gives Prolog part of forward chaining's caching ([[slides-xx-logic-programming-prolog]], slides 9, 15).
- Real-world analogue: production systems and Rete networks (general knowledge; R&N §9.3.3 discusses Rete).

## Common mistakes

- Thinking forward chaining is incomplete because it "might miss" goals — for definite clauses it is complete; it is just unfocused.
- Forgetting to wait for **all** premises (the AND arcs in the graph) before firing.
- Re-adding facts already inferred (causes loops); the `inferred` table prevents it.

## Related

[[backward-chaining]] · [[horn-clauses]] · [[unification]] · [[propositional-logic]] · [[logic-systems-comparison]] · [[sld-resolution]]

## Practice questions

> [!question]- Q1. Run PL-FC-ENTAILS? on R&N Fig. 7.16 — $P \Rightarrow Q$, $L \wedge M \Rightarrow P$, $B \wedge L \Rightarrow M$, $A \wedge P \Rightarrow L$, $A \wedge B \Rightarrow L$, facts $A$, $B$ — with query $Q$. In what order are new symbols inferred?
> **Answer.** Queue $[A, B]$. Pop $A$: counts of $A \wedge P \Rightarrow L$ and $A \wedge B \Rightarrow L$ drop to 1. Pop $B$: $B \wedge L \Rightarrow M$ drops to 1, $A \wedge B \Rightarrow L$ drops to 0 → push $L$. Pop $L$: $L \wedge M \Rightarrow P$ drops to 1, $B \wedge L \Rightarrow M$ drops to 0 → push $M$. Pop $M$: $L \wedge M \Rightarrow P$ → 0 → push $P$. Pop $P$: $P \Rightarrow Q$ → push $Q$; $A \wedge P \Rightarrow L$ → push $L$ (already inferred). Pop $Q$ = query → **true**. Order: $L, M, P, Q$.

> [!question]- Q2. Why is forward chaining guaranteed to terminate on a Datalog KB but not in general?
> **Answer.** With no function symbols there are at most $p\,n^k$ distinct ground facts, so after that many rounds nothing new can appear. Function symbols allow infinitely many terms ($S(0), S(S(0)), \dots$), so the fixed point may never arrive ([[russell-norvig-aima]] §9.3.2).

> [!question]- Q3. An agent receives a stream of sensor percepts and must update conclusions as they arrive. Forward or backward chaining?
> **Answer.** Forward: it is data-driven and incremental — new facts go onto the agenda and trigger new inferences without a specific query ([[russell-norvig-aima]] §7.5.4).

> [!question]- Q4. Which facts does forward chaining derive from `link(a,b). link(b,c).` with `path(X,Z):- link(X,Z).` and `path(X,Z):- path(X,Y), link(Y,Z).`, regardless of clause order?
> **Answer.** Round 1: `path(a,b)`, `path(b,c)`. Round 2: `path(a,c)`. Round 3: nothing new → fixed point. Clause order is irrelevant, unlike in Prolog ([[russell-norvig-aima]] §9.4.3).
