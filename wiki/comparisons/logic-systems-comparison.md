---
type: comparison
summary: Side-by-side of propositional logic, first-order logic, Horn/definite clauses and Prolog (expressiveness, decidability, inference, cost), plus a forward- vs backward-chaining table.
unit: [5, 6]
tags: [logic, comparison, decidability, forward-chaining, backward-chaining, prolog]
sources: ["[[slides-xx-logic-programming-prolog]]", "[[russell-norvig-aima]]", "[[luger-ai-6e]]"]
updated: 2026-10-01
---

# Logic systems compared

The Prolog deck climbs a ladder: [[propositional-logic]] → [[first-order-logic]] → [[horn-clauses]] → [[prolog]] ([[slides-xx-logic-programming-prolog]], slide 2). Each step trades expressiveness against the cost of inference. FOL adds objects and quantifiers but loses decidability. Horn clauses give up disjunction to make inference cheap. Prolog adds a fixed control strategy and database semantics, which makes the language practical but costs completeness and the pure logical reading.

## The four systems

| | Propositional | First-order (FOL) | Horn / definite clauses | Prolog |
|---|---|---|---|---|
| **Ontology** | facts (true/false) | objects, relations, functions | same as its base logic | FOL definite clauses + built-ins |
| **Can say "every"/"some"** | no | yes (∀, ∃) | ∀ implicit; ∃ only via Skolem constants | ∀ implicit per clause |
| **Disjunctive conclusions** ($P \vee Q$) | yes | yes | **no** (≤ 1 positive literal) | no |
| **Negative facts** | yes | yes | no (only goal clauses) | no; `\+` = [[negation-as-failure]] |
| **Semantics** | truth tables | Tarskian models | same | **database semantics**: unique names, closed world, domain closure |
| **Decidability of entailment** | decidable; co-NP-complete | **semidecidable** | propositional: linear time; first-order: semidecidable; Datalog: decidable | the search may not terminate |
| **Main inference** | truth tables, resolution, DPLL/WalkSAT | resolution with unification; propositionalization | [[forward-chaining]], [[backward-chaining]] (Generalized Modus Ponens) | [[sld-resolution]]: depth-first, left-to-right backward chaining |
| **Complete?** | yes (resolution, TT) | refutation-complete (resolution) | FC complete; BC complete only with loop checks | **no**: left recursion and infinite branches; cut can prune solutions |
| **Sound?** | yes | yes | yes | almost: no occurs check |
| **Cost** | $O(2^n)$ model checking | unbounded | linear (propositional); matching NP-hard per step in FOL | linear space; time can be exponential (naive `fibo`) |
| **Course source** | slide 2, 3 | slides 2, 7 | slides 4–6 | slides 7–28 |

Sources: [[russell-norvig-aima]] §7.4.4, §7.5.3–7.5.4, §8.1, §8.2.8, §9.1.1, §9.3.2–9.3.3, §9.4.2–9.4.4; [[luger-ai-6e]] §14.2.1, §14.3.2; [[slides-xx-logic-programming-prolog]], slides 2–5, 15, 23.

### Same sentence in each language

| | "Every American who sells a weapon to a hostile nation is a criminal" |
|---|---|
| Propositional | one symbol per instance: `AmericanWest ∧ WeaponM1 ∧ SellsWestM1Nono ∧ HostileNono ⇒ CriminalWest`, repeated for every combination |
| FOL | $\forall x,y,z\ American(x) \wedge Weapon(y) \wedge Sells(x,y,z) \wedge Hostile(z) \Rightarrow Criminal(x)$ |
| Clause (Horn) | $\neg American(x) \vee \neg Weapon(y) \vee \neg Sells(x,y,z) \vee \neg Hostile(z) \vee Criminal(x)$ |
| Prolog | `criminal(X):- american(X), weapon(Y), sells(X,Y,Z), hostile(Z).` |

([[slides-xx-logic-programming-prolog]], slide 7; [[russell-norvig-aima]] §9.3.1, §9.5.1)

## Forward vs backward chaining

| | [[forward-chaining]] | [[backward-chaining]] |
|---|---|---|
| Direction | facts → query (data-driven) | query → facts (goal-directed) |
| Algorithm | PL-FC-ENTAILS? (Fig. 7.15), FOL-FC-ASK (Fig. 9.3) | FOL-BC-ASK (Fig. 9.6), a generator |
| Search shape | breadth-like, rounds to a fixed point | depth-first AND–OR search |
| Work done | derives *everything* derivable, relevant or not | touches only facts relevant to the query |
| Complete (definite clauses) | yes | yes in principle; depth-first version incomplete (loops) |
| Termination | always for Datalog; may not with function symbols | can loop even on Datalog (left recursion) |
| Repeated subgoals | each fact derived once (dynamic programming) | re-proved, potentially exponential (877 vs 62 inferences, R&N Fig. 9.8b) |
| Space | stores all derived facts | linear in proof size |
| Time (propositional) | linear in KB size | linear; often much less |
| Typical use | sensor updates, production systems, Rete, deductive databases | answering specific questions; Prolog |
| Hybrid | magic sets (backward-preprocessed forward chaining) | tabling (memoised backward chaining, complete for Datalog) |

Sources: [[russell-norvig-aima]] §7.5.4, §9.3, §9.4.1, §9.4.3; [[slides-xx-logic-programming-prolog]], slides 5–6, 15.

## When to use which

- **Propositional logic**: a small, finite world with no need to talk about classes of objects (wumpus squares, circuit bits). Model-checking or SAT solvers work well.
- **FOL**: you need general rules and quantifiers, and you can live with semidecidable inference or use a theorem prover.
- **Horn / definite clauses**: your knowledge is rules of the form "if all of these then that" and you want fast, predictable inference. Most expert-system rule bases fit.
- **Prolog**: you want to *run* a definite-clause KB as a program, and the closed-world assumption fits (a database of facts you fully control, such as the Lab 01 family tree). Use tabling for transitive closure, and `clpfd` for numeric constraints.
- **Forward chaining**: many incoming facts, many possible consequences of interest, or recursive relations you want to materialise. **Backward chaining**: one question at a time over a large KB.

## Practice questions

> [!question]- Q1. Rank propositional, FOL, Horn (propositional) and Datalog by decidability and cost of entailment.
> **Answer.** Horn propositional: linear time. Datalog: decidable (polynomial in data). Full propositional: decidable but co-NP-complete. FOL: only semidecidable ([[russell-norvig-aima]] §7.4.4, §7.5.3, §9.1.1, §9.3.2).

> [!question]- Q2. Name three things FOL can express that Prolog cannot.
> **Answer.** Disjunctive conclusions ($P \vee Q$), explicit negative facts ($\neg Parent(rosa, x)$), and open-world uncertainty, e.g. "there are at least four courses, maybe more". Prolog's closed world forces "exactly these" ([[russell-norvig-aima]] §9.4.4; [[slides-xx-logic-programming-prolog]], slide 4).

> [!question]- Q3. On `link(a,b). link(b,c).` with the left-recursive `path/2`, compare forward chaining, Prolog, and tabled Prolog.
> **Answer.** Forward chaining derives `path(a,b)`, `path(b,c)`, `path(a,c)` and halts. Plain Prolog loops on `path(a,Y)` and overflows the stack. Tabled Prolog returns all three answers and terminates (checked in SWI-Prolog) ([[sld-resolution]]).

> [!question]- Q4. Why is Prolog's unsoundness "almost never a problem in practice"?
> **Answer.** The only unsound step is unification without the occurs check, which matters only when a variable is unified with a term that contains it, like `X = f(X)`. Ordinary programs rarely do that, and `unify_with_occurs_check/2` is available when it matters ([[russell-norvig-aima]] §9.4.2; [[unification]]).

> [!question]- Q5. Your KB receives 10,000 new sensor facts per second and must raise any alarm rule that fires. Forward or backward chaining? Why?
> **Answer.** Forward chaining. It is incremental and data-driven: each new fact triggers only the rules it can complete (Rete-style matching). There is no single query to chain back from ([[russell-norvig-aima]] §7.5.4, §9.3.3).
