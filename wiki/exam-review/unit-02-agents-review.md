---
type: exam-review
summary: Unit 2 cheat sheet — agent, agent function vs program, rationality, PEAS, the seven environment dimensions, the five agent designs, state representations, traps and 13 practice questions.
unit: 2
tags: [exam-review, agents, peas, environments, midterm-1]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Unit 2 review — Intelligent agents

Part of [[midterm-01-review]]. Full notes: [[intelligent-agents]], [[rationality-and-peas]], [[environment-properties]], [[agent-architectures]], [[agent-types-comparison]], [[state-representation]]. Problem formulation (also unit 2) is in [[problem-formulation]] / [[unit-03-search-review]].

## Definitions

- **Agent**: perceives the environment through **sensors**, acts through **actuators** ([[russell-norvig-aima]] §2.1).
- **Percept** (current input) vs **percept sequence** (full history).
- **Agent function** $f:\mathcal P^*\to\mathcal A$ — abstract, on histories, could be a table. **Agent program** — concrete, takes the current percept, runs on the architecture. **agent = architecture + program** ([[slides-03-intelligent-agents]], slide 3; §2.4).
- **Rational agent**: for each percept sequence, selects the action **expected** to maximise the **performance measure**, given the percepts and built-in knowledge (slide 5; §2.2.2).
- Rationality depends on: performance measure, prior knowledge, available actions, percept sequence.
- **Performance measure**: external, set by the designer, scores *environment state sequences*. "You get what you ask for."
- **Omniscience** ≠ rationality (expected vs actual). **Autonomy**: learn to compensate for wrong/partial prior knowledge. **Information gathering**: act to improve future percepts.
- **PEAS**: Performance, Environment, Actuators, Sensors (slide 6).

## Formulas

- Table-driven agent size: $\sum_{t=1}^{T}|P|^t$ entries (§2.4.1). Vacuum, $|P|=4$: reflex agent needs 4 rules instead of $4^T$-ish.
- Expected utility: $\text{EU}(a)=\sum_{s'}P(s'\mid s,a)\,U(s')$; utility-based agent picks $\arg\max_a \text{EU}(a)$ (§2.4.5).

## Environment dimensions (slides 8–12; §2.3.2)

| Dimension | Values | Ask |
|---|---|---|
| Observable | fully / partially / un- | Do sensors give all relevant state? |
| Agents | single / multi (competitive, cooperative) | Does another entity maximise a measure depending on me? |
| Deterministic | deterministic / nondeterministic (stochastic = with probabilities) | Next state fixed by state + action? |
| Episodic | episodic / sequential | Do decisions affect the future? |
| Static | static / dynamic / semidynamic | Does the world change while I think? |
| Discrete | discrete / continuous | Finite states, percepts, actions, time? |
| Known | known / unknown (not on slides) | Are action outcomes given? |

Quick table (R&N Fig. 2.6): crossword F-S-D-Seq-Static-Disc · chess+clock F-M-D-Seq-**Semi**-Disc · poker **P**-M-**Stoch**-Seq-Static-Disc · backgammon F-M-Stoch-Seq-Static-Disc · taxi P-M-Stoch-Seq-Dyn-**Cont** · image analysis F-S-D-**Episodic**-Semi-Cont · part-picking P-S-Stoch-Episodic-Dyn-Cont.

## Agent designs (slides 14–17; §2.4)

| Type | Adds | Handles | Limit |
|---|---|---|---|
| Simple reflex | condition–action rules | fully observable | loops if partially observable (randomise to escape) |
| Model-based reflex | internal state; **transition model** + **sensor model** | partial observability | rules still fixed |
| Goal-based | goals + search/planning | sequential tasks; goal changes | binary goals |
| Utility-based | utility, max **expected** utility | trade-offs, uncertainty | utility hard to specify, costly |
| Learning | performance element, learning element, critic (fixed standard), problem generator | unknown environments | needs feedback |

## State representations (slide 18; §2.4.7)

Atomic (black box: search, games, HMMs, MDPs) → Factored (variables: CSPs, propositional logic, planning, Bayes nets) → Structured (objects + relations: FOL, Prolog, databases). Expressiveness ↑, conciseness ↑, reasoning cost ↑.

## Must-know facts

- The reflex vacuum agent is rational **only** under specific assumptions (+1 per clean square per step, known geography, deterministic moves, correct sensing); with a cost per move it is not (§2.2.2).
- Design performance measures by what you want **in the environment**, not how the agent should behave (§2.2.1).
- A partially observable deterministic environment can *appear* nondeterministic (§2.3.2).
- Not every rational agent has an explicit utility function (§2.4.5).

## Common traps

> [!warning] Contradiction
> - Slide 2 "What is an agent?" contains propositional-logic text ("a proposition is a statement that can be true or false…") — ignore it; use the sensors/actuators definition (§2.1).
> - Slide 15 names the two models "world model" and "transition model"; R&N's are **transition model** (action effects + autonomous evolution) and **sensor model** (§2.4.3).
> - Slide 9 blurs nondeterministic and stochastic; R&N separate them.
- Slides 7 and 13 are image-only — content filled from R&N (PEAS examples; agent diagrams).
- Agent *program* ≠ agent *function*; "architecture" in R&N means hardware.
- Episodic ≠ static; semidynamic = score changes, world doesn't.
- The critic's performance standard must be **fixed**, outside the agent.

## Practice questions

> [!question]- Q1. Define a rational agent precisely.
> **Answer.** For each possible percept sequence, it selects an action expected to maximise its performance measure, given the evidence from the percept sequence and its built-in knowledge ([[russell-norvig-aima]] §2.2.2).

> [!question]- Q2. Give the PEAS of an automated taxi.
> **Answer.** P: safe, fast, legal, comfortable, profitable, minimal impact on others. E: roads, traffic, police, pedestrians, customers, weather. A: steering, accelerator, brake, signal, horn, display, speech. S: cameras, radar/lidar, speedometer, GPS, engine sensors, accelerometer, microphones, touchscreen ([[russell-norvig-aima]] Fig. 2.4).

> [!question]- Q3. Classify poker on all dimensions.
> **Answer.** Partially observable, multi-agent, stochastic, sequential, static, discrete; known rules ([[russell-norvig-aima]] Fig. 2.6).

> [!question]- Q4. Classify a part-picking robot and say why it is episodic although it is dynamic.
> **Answer.** Partially observable, single-agent, stochastic, **episodic**, dynamic, continuous ([[russell-norvig-aima]] Fig. 2.6). Episodic: each decision concerns the current part only and does not affect the next part. Dynamic: the conveyor keeps moving while it deliberates — the two dimensions are independent.

> [!question]- Q5. How many table entries does a table-driven vacuum agent need for T = 2? How many rules for the reflex agent?
> **Answer.** $4 + 4^2 = 20$; the reflex agent needs 4 rules (effectively 3, as Suck does not depend on location) ([[russell-norvig-aima]] §2.4.1–2.4.2).

> [!question]- Q6. Why is a simple reflex agent with only a dirt sensor doomed in the two-square world, and how does randomisation help?
> **Answer.** On [Clean] it always takes the same move; starting in the "wrong" square, it bumps the wall forever. Choosing Left/Right at random reaches the other square in 2 steps on average ([[russell-norvig-aima]] §2.4.2).

> [!question]- Q7. Name and explain the two models of a model-based agent (R&N version).
> **Answer.** Transition model: how the world changes (effects of actions and independent evolution). Sensor model: how world states are reflected in percepts ([[russell-norvig-aima]] §2.4.3).

> [!question]- Q8. Why are goals insufficient for a taxi, and what replaces them?
> **Answer.** Many routes reach the destination; goals cannot say which is faster, safer or cheaper, nor trade off conflicting goals under uncertainty. A utility function ranks states and the agent maximises expected utility ([[russell-norvig-aima]] §2.4.5; [[slides-03-intelligent-agents]], slides 16–17).

> [!question]- Q9. Compute: action A gives utility 8 with p=0.5 and 2 with p=0.5; action B gives 5 for sure. Which does an expected-utility maximiser choose?
> **Answer.** EU(A) = 0.5·8 + 0.5·2 = 5 = EU(B). It is indifferent; any tie-break is rational. A risk-averse *utility* (concave) would prefer B.

> [!question]- Q10. List the four components of a learning agent.
> **Answer.** Performance element, learning element, critic, problem generator ([[russell-norvig-aima]] §2.4.6).

> [!question]- Q11. Classify the representations: 8-puzzle state for BFS; Sudoku as 81 variables; family tree in Prolog.
> **Answer.** Atomic (BFS only tests equality/goal); factored; structured ([[russell-norvig-aima]] §2.4.7).

> [!question]- Q12. Known vs fully observable: give an example of each without the other.
> **Answer.** Known but partially observable: solitaire. Unknown but fully observable: a new video game with all state on screen ([[russell-norvig-aima]] §2.3.2).

> [!question]- Q13. A vacuum's measure gives +1 per clean square per step and −1 per move. Is the reflex vacuum rational? What would be?
> **Answer.** No — after cleaning it oscillates, losing points. A rational agent would stop (NoOp) once it knows both squares are clean, which requires memory (model-based) ([[russell-norvig-aima]] §2.2.2).

## Weak spots

*(to be filled during exam prep)*
