---
type: concept
summary: A rational agent picks the action expected to maximise its performance measure given its percepts and prior knowledge; PEAS (Performance, Environment, Actuators, Sensors) specifies the task environment.
unit: 2
tags: [agents, rationality, performance-measure, peas, autonomy]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Rationality and PEAS

A **rational agent** "does the right thing": *for each possible percept sequence, it selects an action that is expected to maximise its performance measure, given the evidence provided by the percept sequence and whatever built-in knowledge it has* ([[russell-norvig-aima]] §2.2.2; [[slides-03-intelligent-agents]], slide 5). The **performance measure** is an external criterion, chosen by the designer, that scores the sequence of *environment states* the agent's behaviour produces. **PEAS** is the checklist used to specify the task environment before designing any agent.

## How it works

**What rationality depends on** (R&N §2.2.2):
1. the performance measure (criterion of success),
2. the agent's prior knowledge of the environment,
3. the actions it can perform,
4. its percept sequence to date.

$$a^* = \arg\max_{a}\; \mathbb E\big[\,\text{Performance} \mid \text{percepts}_{1..t},\ \text{knowledge},\ a\,\big]$$

**PEAS** ([[slides-03-intelligent-agents]], slide 6; R&N §2.3.1):

| | Meaning |
|---|---|
| **P**erformance | Success criterion |
| **E**nvironment | World the agent operates in |
| **A**ctuators | Mechanisms for acting |
| **S**ensors | Mechanisms for perceiving |

**Examples** (R&N Fig. 2.4–2.5; slide 7 is image-only, likely one of these):

| Agent | Performance | Environment | Actuators | Sensors |
|---|---|---|---|---|
| Automated taxi | Safe, fast, legal, comfortable, max profit, min impact on others | Roads, traffic, police, pedestrians, customers, weather | Steering, accelerator, brake, signal, horn, display, speech | Cameras, radar, speedometer, GPS, engine sensors, accelerometer, microphones, touchscreen |
| Medical diagnosis | Healthy patient, reduced costs | Patient, hospital, staff | Display of questions, tests, diagnoses, treatments | Touchscreen/voice entry of symptoms |
| Part-picking robot | % parts in correct bins | Conveyor belt, parts, bins | Jointed arm and hand | Camera, tactile and joint-angle sensors |
| Interactive English tutor | Student's test score | Students, testing agency | Display of exercises, feedback, speech | Keyboard, voice |
| Vacuum (slide 4) | Clean squares over time | Squares A, B; dirt | Left, Right, Suck | Location, dirt sensor |

## Properties

- **Rational ≠ omniscient.** Rationality maximises *expected* performance; perfection maximises *actual* performance. Crossing the street and being hit by a falling cargo door is not irrational (R&N §2.2.3).
- **Information gathering** is part of rationality: look before crossing; explore an unknown environment (§2.2.3; slide 5 "explore the environment to gather useful information").
- **Learning**: a rational agent should learn from what it perceives (slide 5; §2.2.3). Counter-examples: dung beetle and sphex wasp follow fixed plans even when they fail.
- **Autonomy**: relying on the designer's prior knowledge rather than own percepts = lacking autonomy. A rational agent should learn to compensate for partial or wrong prior knowledge (§2.2.3).
- **Designing the measure**: "what you ask for is what you get". Rewarding *dirt cleaned up* lets a vacuum dump dirt and re-clean it; reward *clean floor* instead. Rule: design measures for **what you want achieved in the environment**, not for how you think the agent should behave (§2.2.1; slide 5 "a poor measure produces unintended behavior").
- **Value alignment / King Midas problem**: the objective put into the machine may not be what we really want (§1.1.5, §2.2.1).
- **Is the reflex vacuum rational?** Yes, *if* the measure is +1 per clean square per step over 1000 steps, geography known, actions deterministic, perception correct. No, if each move costs −1 (it oscillates forever after cleaning) (§2.2.2).

## In this course

- [[slides-03-intelligent-agents]] slide 5 gives the definition, performance measure as external and designer-defined, and the warning about poorly specified measures ("What happens if we specify it incorrectly…? What if we do not specify everything?").
- Slide 6 lists PEAS; slide 7 is image-only (empty in the extraction) — the table above comes from R&N.
- Every HW01 problem can be phrased in PEAS terms before formulating it as search ([[problem-formulation]], [[hw01-report]]).

## Common mistakes

- Defining the performance measure in terms of the agent's *actions* ("suck often") rather than *environment states* ("floors clean").
- Saying the agent chooses the performance measure — the designer does.
- Equating rationality with success: an unlucky rational agent can fail.
- Mixing up "E" and "S": the environment is the world, sensors are the agent's inputs.
- Confusing the *performance measure* (external) with the *utility function* (the agent's internal version of it, [[agent-architectures]]).

## Related

[[intelligent-agents]] · [[environment-properties]] · [[agent-architectures]] · [[problem-formulation]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. Write a PEAS description for a chess-playing agent with a clock.
> **Answer.** P: win/draw/loss, rating, staying within time. E: chessboard, opponent, clock. A: moving pieces (or outputting moves), pressing the clock. S: board-state input (camera or move feed), clock reading. Format from [[russell-norvig-aima]] §2.3.1.

> [!question]- Q2. A vacuum agent's performance measure is "amount of dirt sucked in 8 hours". What can go wrong and how do you fix it?
> **Answer.** A rational agent can dump dirt and suck it up again indefinitely. Measure what you want in the environment: e.g. +1 for each clean square at each time step, possibly minus energy/noise penalties ([[russell-norvig-aima]] §2.2.1).

> [!question]- Q3. Is rationality the same as perfection? Give R&N's example.
> **Answer.** No. Rationality maximises *expected* performance given the percepts so far; perfection would need omniscience. Being hit by a falling airliner door while crossing a clear street is not irrational ([[russell-norvig-aima]] §2.2.3).

> [!question]- Q4. What four things does rationality depend on at any given time?
> **Answer.** Performance measure, prior knowledge of the environment, available actions, percept sequence to date ([[russell-norvig-aima]] §2.2.2).

> [!question]- Q5. Why is the sphex wasp a poor rational agent?
> **Answer.** It lacks learning/autonomy: when the caterpillar is moved, it restarts its fixed plan forever instead of adapting, so its behaviour depends on built-in knowledge, not on its percepts ([[russell-norvig-aima]] §2.2.3).
