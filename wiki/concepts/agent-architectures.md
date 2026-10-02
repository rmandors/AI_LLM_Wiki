---
type: concept
summary: The five agent program designs — simple reflex, model-based reflex, goal-based, utility-based and learning agents — each adding one capability to handle harder environments.
unit: 2
tags: [agents, reflex-agent, model-based, goal-based, utility, learning-agent]
sources: ["[[slides-03-intelligent-agents]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Agent architectures

R&N describe four basic kinds of **agent programs** that "embody the principles underlying almost all intelligent systems" — **simple reflex**, **model-based reflex**, **goal-based** and **utility-based** — plus a way to turn any of them into a **learning agent** ([[russell-norvig-aima]] §2.4). Each step up the ladder adds one piece of knowledge (memory, goals, preferences, self-improvement) so the agent can cope with a harder [[environment-properties|environment]]. Side-by-side table: [[agent-types-comparison]].

> [!note] Terminology
> R&N use "agent architecture" for the *hardware* the program runs on (agent = architecture + program, §2.4). The wiki page name follows common usage: the *designs* of agent programs.

## How it works

### 1. Simple reflex agent
Acts on the **current percept only** with **condition–action rules** (*if car-in-front-is-braking then initiate-braking*) ([[slides-03-intelligent-agents]], slide 14; R&N §2.4.2).

```text
function SIMPLE-REFLEX-AGENT(percept) returns action
    persistent: rules
    state ← INTERPRET-INPUT(percept)
    rule ← RULE-MATCH(state, rules)
    return rule.ACTION
```

Works only if the environment is **fully observable**. A vacuum with only a dirt sensor loops forever on [Clean]; **randomising** (flip a coin Left/Right) escapes the loop, reaching the other square in 2 steps on average (§2.4.2).

### 2. Model-based reflex agent
Keeps an **internal state** that tracks unseen parts of the world, updated with two kinds of knowledge (R&N §2.4.3):
- **transition model** — how the world changes: effects of the agent's actions *and* how the world evolves on its own;
- **sensor model** — how world states show up in percepts.

```text
function MODEL-BASED-REFLEX-AGENT(percept) returns action
    persistent: state, transition_model, sensor_model, rules, action
    state ← UPDATE-STATE(state, action, percept, transition_model, sensor_model)
    rule ← RULE-MATCH(state, rules)
    action ← rule.ACTION
    return action
```

The state is a "best guess"; uncertainty may remain.

### 3. Goal-based agent
Adds **goals** (desirable states) and asks "what will happen if I do A?" — requiring **search** and **planning** ([[slides-03-intelligent-agents]], slide 16; R&N §2.4.4). More flexible: change the destination and behaviour changes without rewriting rules. Limitation: goals are **binary** (happy/unhappy) — cannot prefer a faster or safer route.

### 4. Utility-based agent
Adds a **utility function** $U(s)$ — an internal version of the performance measure — and chooses the action with **maximum expected utility** (slide 17; R&N §2.4.5):

$$\text{EU}(a) = \sum_{s'} P(s' \mid s, a)\, U(s'), \qquad a^* = \arg\max_a \text{EU}(a)$$

Handles **conflicting goals** (speed vs safety in a taxi) and **uncertain goals** (weigh likelihood of success against importance). Not all utility-based agents are model-based — *model-free* agents learn action values directly (§2.4.5).

### 5. Learning agent
Any of the above can be made to learn (R&N §2.4.6). Four components:
- **performance element** — the old "whole agent": percepts → actions;
- **learning element** — improves the performance element;
- **critic** — feedback on how well the agent does w.r.t. a **fixed performance standard** (outside the agent);
- **problem generator** — suggests exploratory actions for informative experiences (cf. [[exploration-vs-exploitation]]).

## Properties

| Type | Memory | Looks ahead | Ranks outcomes | Fails when |
|---|---|---|---|---|
| Simple reflex | No | No | No | Partially observable |
| Model-based reflex | Yes | No | No | Rules can't express goals |
| Goal-based | Yes | Yes (search) | No (binary) | Trade-offs / uncertainty |
| Utility-based | Yes | Yes | Yes (expected utility) | Utility hard to specify; costly |
| Learning | Any | Any | Any | Poor critic / standard |

- Rationality does not *require* an explicit utility function: the reflex vacuum is rational in its environment without one (R&N §2.4.5).
- Perfect expected-utility maximisation is usually computationally infeasible (bounded rationality, §1.1.4).

## In this course

- [[slides-03-intelligent-agents]] slides 14–17 present the four basic types. Slide 13 is **image-only** (empty in the extraction) — presumably the agent-type diagram; R&N Figs. 2.9–2.14 fill the gap. The **learning agent** is not on the slides; it comes from R&N §2.4.6.

> [!warning] Contradiction
> Slide 15 says the model-based agent keeps a *world model* (how the environment evolves independently) and a *transition model* (how the agent's actions affect it). R&N's two models are the **transition model** (covers both) and the **sensor model** ([[russell-norvig-aima]] §2.4.3).

- Search agents of unit 3 ([[uninformed-search]], [[a-star]]) are goal-based; [[minimax]] game players are utility-based (terminal utilities); heuristic evaluation functions approximate utility; the [[genetic-algorithms]] "fitness" plays the role of a utility in optimisation.

## Common mistakes

- Saying a simple reflex agent has "no rules" — it has rules but no memory.
- Saying model-based agents know the true state — they hold a best guess.
- Confusing goal-based (binary goal test) with utility-based (real-valued preference).
- Thinking the critic's performance standard is learned — it must be **fixed** and external (§2.4.6).
- Treating "learning agent" as a fifth type parallel to the others — it is a wrapper any type can use.

## Related

[[agent-types-comparison]] · [[intelligent-agents]] · [[environment-properties]] · [[rationality-and-peas]] · [[state-representation]] · [[problem-formulation]] · [[unit-02-agents-review]]

## Practice questions

> [!question]- Q1. A vacuum agent has only a dirt sensor (no location sensor). Why does a deterministic simple reflex agent fail, and what are two fixes?
> **Answer.** On [Clean] it must always do the same thing, e.g. Left, which loops forever if it starts in A. Fixes: randomise Left/Right (expected 2 steps to reach the other square), or keep internal state (model-based) remembering where it has been ([[russell-norvig-aima]] §2.4.2).

> [!question]- Q2. What two models does a model-based agent need according to R&N, and what does each answer?
> **Answer.** Transition model: "how does the world change — by my actions and by itself?" Sensor model: "how does the world state appear in my percepts?" ([[russell-norvig-aima]] §2.4.3).

> [!question]- Q3. Compute: an agent can take route A (arrive on time with p = 0.9, utility 10; late with p = 0.1, utility −20) or route B (on time with p = 0.6, utility 12; late with p = 0.4, utility 0). Which does a utility-based agent pick?
> **Answer.** EU(A) = 0.9·10 + 0.1·(−20) = 7. EU(B) = 0.6·12 + 0.4·0 = 7.2. It picks **B**. A goal-based agent with goal "arrive" could not distinguish them.

> [!question]- Q4. Name the four components of a learning agent and the job of each.
> **Answer.** Performance element (chooses actions), learning element (improves it), critic (judges behaviour against a fixed performance standard), problem generator (proposes exploratory actions) ([[russell-norvig-aima]] §2.4.6).

> [!question]- Q5. Why is a goal-based agent more flexible than a reflex agent for a taxi?
> **Answer.** Its knowledge (model + goal) is explicit, so changing the destination only changes the goal; a reflex agent's turn rules work for one destination and must all be rewritten ([[russell-norvig-aima]] §2.4.4).
