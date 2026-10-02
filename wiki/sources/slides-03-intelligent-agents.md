---
type: source
summary: Unit 2 deck on intelligent agents — agent function vs program, vacuum world, rationality and performance measures, PEAS, environment properties, the four agent architectures and atomic/factored/structured states.
unit: 2
tags: [agents, rationality, peas, environments, architectures]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Slides 03 — Intelligent Agents

**Bibliographic line.** Riofrío, D. *Intelligent Agents* (lecture slides, 18 slides). AI course NRC 1651, USFQ, Fall 2026. File: `raw/Slides/03_Intelligent Agents.pptx`. Follows [[russell-norvig-aima]] Ch. 2 closely.

**What it is.** The unit-2 theory deck. Pages built from it: [[intelligent-agents]], [[rationality-and-peas]], [[environment-properties]], [[agent-architectures]], [[state-representation]], [[agent-types-comparison]], and the cheat sheet [[unit-02-agents-review]].

## Key points

- **Slide 2 — What is an agent?** Examples: human (eyes/ears → brain → hands/mouth), robot (cameras/sensors → processor → motors), software agent (keyboard/file inputs → program → screen/network outputs). (The rest of the slide text is misplaced; see Issues.)
- **Slide 3 — Agent function vs agent program ("agent model").** *Agent function*: abstract behavioural specification, defines what to do in every situation, maps the **percept history** to an action, could in theory be a lookup table ("what we want to achieve"). *Agent program*: concrete implementation on a physical architecture that approximates the function compactly ("how we approximate it efficiently"). "All AI design is the search for good programs that approximate the ideal function."
- **Slide 4 — Vacuum world.** Two rooms A and B, dirty/clean; sensors = position + room status; actuators = left, right, vacuum. The space of percept histories grows exponentially with variables and time → a table is intractable for a real agent.
- **Slide 5 — Rationality.** Rational agent: at every moment selects the action that **maximises the expected value of a performance measure, given its percept history and built-in knowledge**; explores to gather information; learns from percepts. Performance measure: an *external* criterion defined by the designer, not the agent. "You get what you ask for" — a poor measure produces unintended behaviour.
- **Slide 6 — PEAS**: Performance, Environment, Actuators, Sensors. → [[rationality-and-peas]]
- **Slides 8–12 — Environment dimensions.** Fully vs partially observable (does the agent need memory/state estimation?); deterministic vs non-deterministic ("same input, same output"; stochastic = randomness); episodic vs sequential; static vs dynamic (+ semidynamic: chess with a clock); discrete vs continuous; single vs multi-agent (competitive or cooperative). → [[environment-properties]]
- **Slide 14 — Simple reflex agent**: current percept only, condition–action rules; simple and efficient; fails in partially observable environments.
- **Slide 15 — Model-based reflex agent**: internal state from a "world model" and a "transition model"; updates state each step, then applies rules; copes with partial observability.
- **Slide 16 — Goal-based agent**: goals = desired world states; needs planning and search; adapts when the goal changes; goals are binary, cannot rank paths.
- **Slide 17 — Utility-based agent**: maximises expected utility weighting outcome probabilities; handles conflicting objectives (taxi: speed vs safety) and uncertainty. → [[agent-architectures]]
- **Slide 18 — State representation**: atomic (black box), factored (variables/attributes), structured (objects + relations); more expressiveness → more reasoning but more computation. → [[state-representation]]

## Pages that use this source

[[intelligent-agents]], [[rationality-and-peas]], [[environment-properties]], [[agent-architectures]], [[state-representation]], [[agent-types-comparison]], [[unit-02-agents-review]], [[problem-formulation]], [[midterm-01-review]], [[overview]].

## Issues found

> [!warning] Contradiction — slide 2 contains logic text
> Slide 2, titled "What Is an Agent?", opens with "A proposition is a statement that can be true or false / Propositional symbols represent facts about the world / Complex sentences are built using logical connectives". This is the definition of [[propositional-logic]], apparently pasted from a logic deck. The actual agent definition is R&N's: *an agent is anything that perceives its environment through **sensors** and acts on it through **actuators*** ([[russell-norvig-aima]] §2.1). The examples on the slide (eyes → brain → hands) are consistent with R&N.

> [!warning] Contradiction — "world model" vs "transition model"
> Slide 15 says a model-based agent keeps two models: a *world model* (how the environment evolves independently of the agent) and a *transition model* (how the agent's actions affect the environment). R&N split it differently: the **transition model** covers *both* the effects of the agent's actions *and* how the world evolves on its own; the second model is the **sensor model** (how world state is reflected in percepts) ([[russell-norvig-aima]] §2.4.3). Use R&N's terms on exams, but know the slide's version.

- **Image-only slides:** slide **7** (empty — by position, likely the PEAS example table, e.g. the automated taxi; filled from R&N Fig. 2.4/2.5 in [[rationality-and-peas]]) and slide **13** (empty — by position, likely the agent/environment diagram or the list of agent types; filled from R&N §2.4 in [[agent-architectures]]). Their contents are a guess from position only.
- **Missing topics vs R&N Ch. 2:** no *known vs unknown* environment dimension (R&N §2.3.2), no **learning agent** (R&N §2.4.6: performance element, learning element, critic, problem generator), no table-driven agent analysis ($\sum_{t=1}^{T}|P|^t$ entries, §2.4.1). These pages include them, marked as R&N material.
- **Deterministic vs stochastic** (slide 9): the slide treats "non-deterministic" and "stochastic" loosely as synonyms. R&N distinguish them: *stochastic* = outcomes with explicit probabilities, *nondeterministic* = possible outcomes listed without probabilities (§2.3.2).
- **Slide 16 "it also needs to know where it wants to go"**: "goals are binary" is R&N's "crude binary distinction between happy and unhappy states" (§2.4.5) — consistent.
