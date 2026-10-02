---
type: concept
summary: Atomic, factored and structured representations of world states — increasing expressiveness at the cost of harder reasoning and learning — and which AI techniques use each.
unit: 2
tags: [agents, representation, atomic, factored, structured]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# State representation

Agent components (e.g. "what my actions do") must represent the world. R&N place representations on an axis of **increasing expressiveness**: **atomic** (state = indivisible black box), **factored** (state = vector of variable values) and **structured** (state = objects and relations) ([[russell-norvig-aima]] §2.4.7; [[slides-03-intelligent-agents]], slide 18). More expressive languages are more concise but make reasoning and learning harder.

## How it works

| Level | A state is… | Two states can… | Example (driving across a country) | Used by |
|---|---|---|---|---|
| **Atomic** | A name with no internal structure | Only be equal or different | "In Arad" | [[uninformed-search]], [[a-star]], [[adversarial-search]], hidden Markov models, MDPs |
| **Factored** | A fixed set of variables/attributes with values (Boolean, real, symbolic) | Share some attributes, differ in others | (city, fuel, GPS, oil-light, money, radio) | [[constraint-satisfaction-problems]], [[propositional-logic]], planning, Bayesian networks, many ML algorithms |
| **Structured** | Objects with attributes and relations among them | Share objects and relations | "Truck *reversing into* driveway *blocked by* loose cow" | [[first-order-logic]], [[prolog]], relational databases, first-order probability models, NLP |

([[russell-norvig-aima]] §2.4.7)

**Conciseness example** (§2.4.7): the rules of chess take 1–2 pages in first-order logic (structured), thousands of pages in propositional logic (factored), and ~10³⁸ pages as a finite-state automaton (atomic).

A second, independent axis (§2.4.7): **localist** (one concept ↔ one memory location) vs **distributed** representations (concept spread over many locations, as in neural networks) — distributed ones are robust to noise.

## Properties

- **Expressiveness ↑ ⇒ conciseness ↑, but reasoning/learning complexity ↑** (slide 18: "Greater expressiveness enables more reasoning, but also increases computational complexity").
- Factored states let algorithms exploit structure: a CSP solver sees *which variable* violates a constraint, while an atomic search only sees a goal test fail ([[csp-heuristics]]).
- Real systems may need to operate at several levels at once (§2.4.7).

## In this course

- [[slides-03-intelligent-agents]] slide 18 gives the three definitions and asks "Why is the level of representation important?"
- Unit 3 search treats states atomically ([[state-space-and-graph-search]]), even if the code stores a tuple — the *algorithm* only uses goal tests, successors and costs. [[heuristic-functions]] peek inside the state (e.g. Manhattan distance on 8-puzzle tiles), which is one reason informed search beats uninformed search.
- CSPs ([[constraint-satisfaction-problems]], HW01 N-queens and Sudoku) use factored states; Prolog ([[prolog]], [[lab01-family-pl]]) uses structured ones (`parent(tom, bob)`).
- The course progression mirrors the axis: search (atomic) → CSP and propositional logic (factored) → first-order logic and Prolog (structured).

## Common mistakes

- Judging representation by the data structure in code: an 8-puzzle stored as a tuple is still treated *atomically* by BFS, which never inspects tile positions.
- Calling propositional logic "structured" — it has variables (propositions) but no objects or relations: **factored**.
- Thinking more expressive is always better — it costs inference complexity (FOL is undecidable in general).

## Related

[[intelligent-agents]] · [[agent-architectures]] · [[problem-formulation]] · [[constraint-satisfaction-problems]] · [[propositional-logic]] · [[first-order-logic]] · [[logic-systems-comparison]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. Classify as atomic, factored or structured: (a) a city name in route finding; (b) a Sudoku grid as 81 cell variables; (c) `parent(tom, bob). parent(bob, ann).`
> **Answer.** (a) atomic, (b) factored, (c) structured ([[russell-norvig-aima]] §2.4.7).

> [!question]- Q2. Why can a CSP solver do better than a generic search algorithm on the same problem?
> **Answer.** With a factored representation it can see which variables and constraints are involved, so it can propagate constraints and choose variables cleverly (MRV, forward checking) instead of treating states as black boxes ([[russell-norvig-aima]] §2.4.7; [[csp-heuristics]]).

> [!question]- Q3. State the trade-off on the expressiveness axis with R&N's chess example.
> **Answer.** More expressive = more concise: chess rules are 1–2 pages in FOL, thousands in propositional logic, ~10³⁸ pages as an automaton; but reasoning and learning become harder as expressiveness rises ([[russell-norvig-aima]] §2.4.7).

> [!question]- Q4. What is a distributed representation and why is it robust?
> **Answer.** A concept is spread over many memory locations, each shared by several concepts (as in neural nets). A few garbled bits move it to a nearby point with similar meaning, whereas a localist code can turn "Truck" into the unrelated "Truce" ([[russell-norvig-aima]] §2.4.7).
