---
type: concept
summary: An agent perceives its environment through sensors and acts on it through actuators; its behaviour is an agent function from percept sequences to actions, implemented by an agent program on an architecture.
unit: 2
tags: [agents, agent-function, agent-program, vacuum-world]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Intelligent agents

An **agent** is anything that can be viewed as **perceiving** its environment through **sensors** and **acting** upon that environment through **actuators** ([[russell-norvig-aima]] §2.1). A *percept* is what the sensors register at one instant; the *percept sequence* is everything the agent has ever perceived. AI, in R&N's framing, is the science of designing **rational** agents — agents that do the right thing given what they know ([[rationality-and-peas]]).

## How it works

```
        percepts actions
Environment ───► [Sensors] ─► Agent program ─► [Actuators] ───► Environment
```

| Agent | Sensors | Actuators |
|---|---|---|
| Human | eyes, ears | hands, legs, mouth |
| Robot | cameras, infrared range finders | motors |
| Software agent | keyboard, files, network packets | screen, files, network packets |

([[slides-03-intelligent-agents]], slide 2; [[russell-norvig-aima]] §2.1)

**Agent function vs agent program** ([[slides-03-intelligent-agents]], slide 3; R&N §2.1, §2.4):

| | Agent function $f: \mathcal P^* \to \mathcal A$ | Agent program |
|---|---|---|
| Nature | Abstract mathematical mapping | Concrete code on a physical machine |
| Input | Entire **percept history** | The **current percept** (must remember history itself) |
| Role | "What we want to achieve" | "How we approximate it efficiently" |
| Form | Could be a (huge) lookup table | Compact rules, models, search, learning |

$$\text{agent} = \text{architecture} + \text{program}\quad(\text{R\&N §2.4})$$

**Vacuum world** (slide 4; R&N Fig. 2.2–2.3): squares A, B, each Clean/Dirty. Percept = [location, status]; actions = Left, Right, Suck (R&N adds NoOp). Agent function: *if dirty then Suck, else move to the other square*:

```text
function REFLEX-VACUUM-AGENT([location, status]) returns action
    if status = Dirty then return Suck
    else if location = A then return Right
    else if location = B then return Left
```

**Why not a table?** TABLE-DRIVEN-AGENT appends each percept and looks up the whole sequence. With percept set $P$ and lifetime $T$ the table has $\sum_{t=1}^{T}|P|^t$ entries — >10¹⁵⁰ for chess, $10^{600{,}000{,}000{,}000}$ for an hour of taxi camera input (R&N §2.4.1). Slide 4: "The space of percept histories grows exponentially … computationally intractable". The key challenge is to produce rational behaviour from a *small program* instead of a vast table (Newton's method replaced square-root tables).

## Properties

- "Agent" is an **analysis tool**, not an absolute category — a calculator can be seen as an agent but nothing is gained (R&N §2.1).
- An agent's choice may depend on built-in knowledge and the percept sequence, **never on anything it has not perceived** (§2.1).
- Agents differ in how they compute actions — see [[agent-architectures]] (simple reflex, model-based, goal-based, utility-based, learning) and [[agent-types-comparison]].
- What an agent *should* do depends on the task environment: [[rationality-and-peas]], [[environment-properties]].
- How it represents the world: [[state-representation]].

## In this course

- Slides 2–4 of [[slides-03-intelligent-agents]] define agents with human/robot/software examples, the agent function vs program ("agent model", slide 3), and the vacuum world. Slide 3: "All AI design is the search for good programs that approximate the ideal function."
- Slide 2 also contains propositional-logic text by mistake:

> [!warning] Contradiction
> [[slides-03-intelligent-agents]] slide 2 ("What Is an Agent?") begins with "A proposition is a statement that can be true or false…" — text about [[propositional-logic]], not agents. The definition used here (sensors, actuators, percepts) is R&N's ([[russell-norvig-aima]] §2.1).

- Search problems in unit 3 ([[problem-formulation]], [[a-star]]) are solved by *goal-based problem-solving agents* with atomic states; HW01's puzzles ([[hw01-report]]) are such agents.

## Common mistakes

- Saying the agent *program* takes the percept history as input — it takes only the current percept; the *function* is defined on histories.
- Thinking a lookup table is "wrong": it implements the desired function exactly, it is just infeasibly large.
- Forgetting the environment is only the part of the universe that affects/is affected by the agent.
- Confusing **actuators** (hardware for acting) with **actions** (what is chosen).

## Related

[[rationality-and-peas]] · [[environment-properties]] · [[agent-architectures]] · [[state-representation]] · [[agent-types-comparison]] · [[problem-formulation]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. Distinguish the agent function from the agent program.
> **Answer.** The function is an abstract mapping from every possible percept *sequence* to an action (an external characterisation, possibly an infinite table). The program is a concrete implementation running on the architecture that takes the *current* percept and returns an action ([[russell-norvig-aima]] §2.1, §2.4.1; [[slides-03-intelligent-agents]], slide 3).

> [!question]- Q2. In the two-square vacuum world, how many entries does a table-driven agent need for a lifetime of T = 3 steps?
> **Answer.** Percepts: 2 locations × 2 statuses = 4. Entries $=\sum_{t=1}^{3}4^t = 4+16+64 = 84$. The reflex agent needs only 4 rules (in fact 3, since Suck does not depend on location) ([[russell-norvig-aima]] §2.4.1–2.4.2).

> [!question]- Q3. Give sensors and actuators for a software agent that filters spam.
> **Answer.** Sensors: incoming email contents and headers, user "mark as spam" clicks (file/network inputs). Actuators: moving mail to folders, flagging, displaying warnings (file/screen outputs). Pattern from [[russell-norvig-aima]] §2.1.

> [!question]- Q4. Can an agent's action depend on something it has never perceived?
> **Answer.** Only via built-in (prior) knowledge; otherwise no — choice depends on built-in knowledge and the percept sequence to date ([[russell-norvig-aima]] §2.1).
