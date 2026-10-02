---
type: concept
summary: Swarm intelligence is collective problem solving that emerges from many simple agents following local rules and sharing information directly or through the environment; PSO, ACO and ABC are its main optimisers.
unit: 9
tags: [swarm-intelligence, metaheuristics, bio-inspired]
sources: ["[[slides-04-optimization]]", "[[kennedy-eberhart-1995-pso]]", "[[dorigo-1996-ant-system]]", "[[russell-norvig-aima]]", "[[eiben-smith-evolutionary-computing]]"]
updated: 2026-10-01
---

# Swarm intelligence

**Swarm intelligence** is the useful collective behaviour that emerges when many simple agents —
birds, ants, bees, or their software counterparts — follow local rules and share information,
without any central controller. No single agent knows the solution; the group finds it
([[slides-04-optimization]], slides 8, 12, 16). In optimisation, the swarm is a population of
candidate solutions whose members influence each other, either **directly** (PSO particles see
the global best) or **indirectly through the environment** (ants read pheromone left by others —
called *stigmergy*, general knowledge).

## How it works

Common ingredients:
1. **Population of simple agents**, each holding or building a candidate solution.
2. **Local rule** for moving/constructing (velocity update, probabilistic edge choice,
   neighbour search).
3. **Information sharing**: a global or neighbourhood best (PSO), a pheromone matrix (ACO),
   waggle-dance recruitment proportional to quality (ABC onlookers).
4. **Positive feedback** (good things get reinforced) balanced by **negative feedback** or
   randomness (evaporation, scouts, random factors) — see [[exploration-vs-exploitation]].

**Millonas' five principles** ([[kennedy-eberhart-1995-pso]] §4):

| Principle | Meaning | PSO example |
|---|---|---|
| Proximity | Simple space and time computations | $n$-dimensional updates per time step |
| Quality | Respond to quality factors in the environment | respond to pbest and gbest |
| Diverse response | Don't commit along excessively narrow channels | pull split between pbest and gbest |
| Stability | Don't change behaviour mode every time the environment changes | state changes only when gbest changes |
| Adaptability | Change mode when worth the computational price | it does change when gbest changes |

(Principles 4 and 5 are "opposite sides of the same coin".)

## Properties

- **Decentralised and robust**: losing one agent changes little; naturally parallel.
- **Emergent**: the colony's ability exceeds any agent's; Dorigo showed **synergy** —
  communicating ants beat the same number of independent ants ([[dorigo-1996-ant-system]] §V-A).
- **Autocatalytic risk**: positive feedback without a limiting mechanism "leads to explosion"
  (or stagnation) ([[dorigo-1996-ant-system]] §I, footnote 1).
- **Main algorithms in the course:**

| Algorithm | Inspiration | Shared information | Space |
|---|---|---|---|
| [[particle-swarm-optimization]] | bird flocks, fish schools | global best position | continuous |
| [[ant-colony-optimization]] | ant foraging trails | pheromone matrix | discrete (graphs) |
| [[artificial-bee-colony]] | honeybee foraging | fitness-proportional recruitment | continuous |

- Many later "-inspired" algorithms (firefly, glowworm, cuckoo search, grey wolf) follow the same
  template ([[russell-norvig-aima]] Ch. 4 notes, p. 160). R&N's list mixes physics (particle
  swarms) and entomology (ants, bees) as inspirations.

## In this course

- The deck is titled "Optimization and Biology-Inspired Agents"; PSO is introduced as inspired
  by "swarm theory" ([[slides-04-optimization]], slide 8), and ABC as "a swarm-intelligence
  approach" ([[slides-04-optimization]], slide 16).
- The agent view connects to unit 2: each ant/particle is a very simple reflex-like agent; see
  [[intelligent-agents]] and [[agent-architectures]].
- Raymond's swarm implementations: [[particle-swarm-py]] and [[ant-colony-py]].

## Common mistakes

- Calling GAs "swarm intelligence": GAs are evolutionary (generations, selection, inheritance);
  swarms are about simultaneous interaction of persistent agents. PSO is sometimes grouped
  with EAs because it fits the generate-and-test template
  ([[eiben-smith-evolutionary-computing]] §6.7).
- Assuming more agents is always better — Dorigo found $m \approx n$ ants optimal
  ([[dorigo-1996-ant-system]] §V-A).

## Related

[[particle-swarm-optimization]], [[ant-colony-optimization]], [[artificial-bee-colony]],
[[evolutionary-computation]], [[exploration-vs-exploitation]], [[intelligent-agents]],
[[kennedy-and-eberhart]], [[marco-dorigo]], [[dervis-karaboga]], [[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. What is swarm intelligence? Give one direct-communication and one indirect-communication example.
> **Answer.** Collective problem solving emerging from many simple agents with local rules and
> shared information, without central control. Direct: PSO particles all know $g_{best}$.
> Indirect: ACO ants communicate through pheromone on edges (stigmergy — general knowledge).

> [!question]- Q2. List Millonas' five principles.
> **Answer.** Proximity, quality, diverse response, stability, adaptability
> ([[kennedy-eberhart-1995-pso]] §4).

> [!question]- Q3. What did Dorigo's "synergy" experiment show?
> **Answer.** On a 4×4 grid TSP, ants that communicate through trail ($\alpha > 0$) solved the
> problem more efficiently than the same number of non-communicating ants ($\alpha = 0$), with
> the best efficiency near $m \approx n$ ([[dorigo-1996-ant-system]] §V-A).

> [!question]- Q4. Why does positive feedback need a counterweight in swarm algorithms? Give the counterweight in ACO and ABC.
> **Answer.** Unchecked positive feedback makes everyone follow the first good-looking option
> (stagnation/explosion). ACO: pheromone evaporation (and probabilistic choice). ABC: scout bees
> replace exhausted sources ([[dorigo-1996-ant-system]] §I; [[slides-04-optimization]], slide 17).
