---
type: concept
summary: The seven dimensions that classify task environments — observable, agents, deterministic, episodic, static, discrete, known — and how each dictates agent design.
unit: 2
tags: [agents, environments, observability, determinism]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Environment properties

A task environment (the "problem" an agent is the "solution" to) can be classified along a small set of **dimensions**, and these largely determine which agent design and which algorithms apply ([[russell-norvig-aima]] §2.3.2). The hardest case is *partially observable, multi-agent, nondeterministic, sequential, dynamic, continuous and unknown* — e.g. driving a rented car in a foreign country.

## How it works — the dimensions

| Dimension | Easy end | Hard end | Key question ([[slides-03-intelligent-agents]]) | Design consequence |
|---|---|---|---|---|
| Observability | **Fully** observable | **Partially** observable (or unobservable) | Can the sensors detect all aspects relevant to choosing an action? (s8) | Partial → needs memory / internal state ([[agent-architectures]]) |
| Agents | **Single** agent | **Multi**-agent (competitive / cooperative) | Are other entities maximising a measure that depends on my behaviour? (s12) | Multi → [[adversarial-search]], communication, randomisation |
| Determinism | **Deterministic** | **Nondeterministic** / stochastic | Is the next state fully determined by current state + action? (s9) | Must handle uncertainty; contingency plans, probabilities |
| Episodes | **Episodic** | **Sequential** | Can current decisions affect future ones? (s10) | Sequential → must think ahead (search, planning) |
| Change | **Static** | **Dynamic** (semidynamic) | Does the world change while the agent deliberates? (s11) | Dynamic → must act fast; "not deciding = doing nothing" |
| Values | **Discrete** | **Continuous** | Finite well-defined states, percepts, actions? (s12) | Continuous → optimisation, calculus ([[gradient-descent]]) |
| Knowledge | **Known** | **Unknown** | Are the "laws of physics" (outcomes of actions) given? (R&N only) | Unknown → must learn / explore |

Clarifications (R&N §2.3.2):
- **Effectively fully observable**: the sensors capture everything *relevant* to the decision.
- **Multi-agent test**: B is an agent (for A) if B's behaviour is best described as maximising a performance measure that depends on A's behaviour. Chess = competitive; taxi = partially cooperative (avoid collisions) and partially competitive (parking spaces).
- **Stochastic vs nondeterministic**: *stochastic* models quantify outcome probabilities ("25 % chance of rain"); *nondeterministic* just lists possibilities. A partially observable deterministic environment can *appear* nondeterministic.
- **Semidynamic**: the environment does not change but the performance score does — chess with a clock (slide 11).
- **Known ≠ observable**: solitaire is known but partially observable; a new video game can be fully observable but unknown.

**Classification table** (R&N Fig. 2.6):

| Task environment | Observable | Agents | Deterministic | Episodic | Static | Discrete |
|---|---|---|---|---|---|---|
| Crossword puzzle | Fully | Single | Deterministic | Sequential | Static | Discrete |
| Chess with a clock | Fully | Multi | Deterministic | Sequential | Semi | Discrete |
| Poker | Partially | Multi | Stochastic | Sequential | Static | Discrete |
| Backgammon | Fully | Multi | Stochastic | Sequential | Static | Discrete |
| Taxi driving | Partially | Multi | Stochastic | Sequential | Dynamic | Continuous |
| Medical diagnosis | Partially | Single | Stochastic | Sequential | Dynamic | Continuous |
| Image analysis | Fully | Single | Deterministic | Episodic | Semi | Continuous |
| Part-picking robot | Partially | Single | Stochastic | Episodic | Dynamic | Continuous |
| Refinery controller | Partially | Single | Stochastic | Sequential | Dynamic | Continuous |
| English tutor | Partially | Multi | Stochastic | Sequential | Dynamic | Discrete |

Course examples (classified here, general knowledge applying R&N's definitions): 8-puzzle ([[hw01-ex01-8-puzzle]]) and N-queens ([[hw01-ex03-n-queens]]) are fully observable, single-agent, deterministic, sequential, static, discrete, known; 4×4 tic-tac-toe ([[tic-tac-toe-4x4-py]]) is the same but **multi-agent** (competitive).

## Properties

- Classifications are not always clear-cut: medical diagnosis is episodic if it is "pick a diagnosis from symptoms", sequential if it includes ordering tests (R&N §2.3.2).
- Classic search ([[uninformed-search]], [[a-star]]) assumes the easy end of every dimension (fully observable, deterministic, static, discrete, known). [[minimax]] relaxes "single agent". Unit 7–8 methods relax determinism and observability.
- Evaluating agents is done over an **environment class** (many simulated conditions), reporting average performance (§2.3.2).

## In this course

- [[slides-03-intelligent-agents]] slides 8–12 cover observability (8), determinism incl. "same input, same output — no randomness" vs stochastic (9), episodic vs sequential (10), static/dynamic/semidynamic (11), discrete/continuous and single/multi-agent (12). The **known/unknown** dimension is not on the slides.

> [!warning] Contradiction
> Slide 9 treats "non-deterministic" and "stochastic" as the same idea ("Stochastic systems: same input can give different outputs due to randomness"). R&N distinguish them: stochastic = with explicit probabilities, nondeterministic = possibilities without probabilities ([[russell-norvig-aima]] §2.3.2). Use R&N's distinction when a question hinges on it.

## Common mistakes

- Calling poker "deterministic because the rules are fixed": dealing is random → stochastic.
- Calling chess "partially observable" because you cannot see the opponent's plan — the *state* (board) is fully visible.
- Confusing **episodic** with "short" — it means decisions do not affect later episodes.
- Confusing **static** with deterministic — static is about change *during deliberation*.
- Mixing up *sequential* (opposite of episodic) with *sequential vs parallel* computing (R&N §2.3.2 fn. 4).

## Related

[[intelligent-agents]] · [[rationality-and-peas]] · [[agent-architectures]] · [[state-representation]] · [[problem-formulation]] · [[adversarial-search]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. Classify a crossword puzzle and taxi driving on all six table dimensions.
> **Answer.** Crossword: fully, single, deterministic, sequential, static, discrete. Taxi: partially, multi, stochastic, sequential, dynamic, continuous ([[russell-norvig-aima]] Fig. 2.6).

> [!question]- Q2. Why is chess with a clock "semidynamic"?
> **Answer.** The board does not change while you think, but your performance (remaining time) does ([[slides-03-intelligent-agents]], slide 11; [[russell-norvig-aima]] §2.3.2).

> [!question]- Q3. Give an environment that is known but partially observable, and one that is unknown but fully observable.
> **Answer.** Solitaire (rules known, face-down cards hidden); a new video game whose screen shows everything but whose buttons' effects you do not know ([[russell-norvig-aima]] §2.3.2).

> [!question]- Q4. What is the difference between stochastic and nondeterministic in R&N?
> **Answer.** Stochastic models attach probabilities to outcomes; nondeterministic ones list possible outcomes without probabilities ([[russell-norvig-aima]] §2.3.2).

> [!question]- Q5. Classify the Sudoku solver from HW01 and justify which agent type suffices.
> **Answer.** Fully observable, single-agent, deterministic, sequential (each assignment constrains later ones), static, discrete, known. A goal-based agent using [[csp-backtracking-search]] suffices; no utility or learning needed ([[hw01-ex06-sudoku]]; classification by R&N §2.3.2 definitions).

> [!question]- Q6. Why does partial observability force a model-based (or better) agent?
> **Answer.** The current percept does not contain all relevant information, so the agent must keep internal state built from the percept history and models of the world; a simple reflex agent can loop forever ([[russell-norvig-aima]] §2.4.2–2.4.3; [[slides-03-intelligent-agents]], slide 14).
