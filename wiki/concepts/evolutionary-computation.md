---
type: concept
summary: Evolutionary computation is the family of population-based, stochastic generate-and-test algorithms (GA, ES, EP, GP and relatives) that optimise by repeated variation and selection.
unit: 9
tags: [evolutionary-computation, metaheuristics, history]
sources: ["[[slides-04-optimization]]", "[[eiben-smith-evolutionary-computing]]", "[[russell-norvig-aima]]", "[[holland-1992-genetic-algorithms]]"]
updated: 2026-10-01
---

# Evolutionary computation

**Evolutionary computation (EC)** applies the principles of biological evolution — variation,
heredity and natural selection — to problem solving. A population of candidate solutions
competes for a limited number of places; better candidates are more likely to reproduce, their
offspring inherit and vary their features, and over generations the population's quality rises
([[eiben-smith-evolutionary-computing]] §3.1; [[slides-04-optimization]], slides 2–3). The
algorithms are called **evolutionary algorithms (EAs)**; the main "dialects" are
[[genetic-algorithms]], evolution strategies, evolutionary programming and genetic programming.
R&N describe EAs as "variants of stochastic beam search" motivated by natural selection
([[russell-norvig-aima]] §4.1.4; see [[beam-search]]).

## How it works

General scheme ([[eiben-smith-evolutionary-computing]] Fig. 3.1):

```text
INITIALISE population with random candidate solutions
EVALUATE each candidate
repeat until TERMINATION CONDITION
    1 SELECT parents
    2 RECOMBINE pairs of parents
    3 MUTATE the resulting offspring
    4 EVALUATE new candidates
    5 SELECT individuals for the next generation
```

The components that must be specified ([[eiben-smith-evolutionary-computing]] §3.2):

| Component | Role | Examples |
|---|---|---|
| Representation | Map phenotypes (solutions) ↔ genotypes (chromosomes) | bit strings, real vectors, permutations, trees |
| Fitness function | Defines what "better" means | objective or a transform of it |
| Population | Multiset of genotypes; the unit of evolution | fixed size $\mu$ |
| Parent selection | Bias reproduction toward better individuals (usually stochastic) | roulette wheel, tournament, ranking |
| Variation | Create new candidates | mutation (unary), recombination/crossover ($n$-ary) |
| Survivor selection | Decide who enters the next generation (often deterministic) | generational, steady-state, elitism, $(\mu+\lambda)$, $(\mu,\lambda)$ |
| Initialisation / termination | Start and stop | random; max evaluations, stagnation, target fitness |

R&N's list of design choices is similar: population size, representation, **mixing number**
$\rho$ (number of parents; $\rho = 1$ is stochastic beam search), selection, recombination,
mutation rate, and makeup of the next generation (elitism, culling)
([[russell-norvig-aima]] §4.1.4).

**Dialects** ([[eiben-smith-evolutionary-computing]] §3.1, §2.2; [[russell-norvig-aima]] §4.1.4):

| Dialect | Origin | Typical representation | Main variation |
|---|---|---|---|
| Evolutionary programming (EP) | Fogel, Owens & Walsh, USA, 1960s | finite-state machines | mutation only |
| Evolution strategies (ES) | Rechenberg & Schwefel, Berlin, 1960s | real vectors (+ step sizes) | Gaussian mutation, self-adaptation |
| Genetic algorithms (GA) | Holland, Michigan, 1960s–70s | bit strings | crossover (main), mutation (background) |
| Genetic programming (GP) | Koza, early 1990s | trees (programs) | subtree crossover |

[[particle-swarm-optimization]] and differential evolution are often presented as EA relatives
because they fit the same generate-and-test framework ([[eiben-smith-evolutionary-computing]]
§6.6–6.7).

## Properties

- **Population-based, stochastic, mostly recombination-based** generate-and-test
  ([[eiben-smith-evolutionary-computing]] §3.1).
- **Anytime behaviour**: rapid improvement early, flattening later; can be stopped at any time
  with a usable answer ([[eiben-smith-evolutionary-computing]] §3.5).
- **No optimality guarantee** in finite time; convergence theorems rely on mutation making the
  space connected and have limited practical value ([[eiben-smith-evolutionary-computing]]
  §3.2.5).
- **Two forces**: variation adds diversity, selection increases mean quality
  ([[eiben-smith-evolutionary-computing]] §3.1). Balancing them is the
  [[exploration-vs-exploitation]] problem.
- R&N's caution: comparisons often find GAs slower than stochastic hill climbing; their appeal
  may partly be "the appealing metaphor of evolution" ([[russell-norvig-aima]] §4.1.4 and Ch. 4
  notes).

## In this course

- Slide 2 gives the course's history line: EC arose to solve combinatorial optimization with
  evolutionary mechanisms; "its creator was Lawrence J. Fogel (1960)" (evolving finite-state
  machines); Rechenberg & Schwefel (1970) evolution strategies; [[john-holland]] (1975) genetic
  algorithms ([[slides-04-optimization]], slide 2).
- Slide 3 defines adaptation, heredity and natural selection and proposes treating each point
  of a function's domain as an individual ([[slides-04-optimization]], slide 3).
- Raymond's [[genetic-algorithm-py]] is the course's EA implementation.

> [!warning] Contradiction — dates and "creator"
> The slides date evolution strategies to 1970 and name Fogel as *the* creator of EC.
> [[eiben-smith-evolutionary-computing]] §2.2 and §6.2 place ES in the early 1960s and list
> Turing (1948) and Bremermann (1962) as earlier pioneers; [[russell-norvig-aima]] (Ch. 4 notes,
> p. 161) cites Rechenberg (1965) and also mentions 1950s statisticians (Box, Friedman). For the
> exam, give the slide's answer but know that the three dialects arose independently in the
> 1960s.

## Common mistakes

- Using "genetic algorithm" for every EA — ES, EP and GP differ in representation and operators.
- Forgetting that selection is representation-independent while variation operators must match
  the representation ([[eiben-smith-evolutionary-computing]] §3.1).
- Confusing parent selection (who reproduces) with survivor selection (who stays).

## Related

[[genetic-algorithms]], [[schema-theory-and-building-blocks]], [[particle-swarm-optimization]],
[[swarm-intelligence]], [[beam-search]], [[optimization-problems]],
[[exploration-vs-exploitation]], [[john-holland]], [[history-of-ai]],
[[metaheuristics-comparison]].

## Practice questions

> [!question]- Q1. List the components that must be specified to define an evolutionary algorithm.
> **Answer.** Representation, fitness (evaluation) function, population, parent selection,
> variation operators (mutation, recombination), survivor selection, plus initialisation and a
> termination condition ([[eiben-smith-evolutionary-computing]] §3.2).

> [!question]- Q2. Match each dialect to its classic representation: GA, ES, EP, GP.
> **Answer.** GA — strings over a finite alphabet (often bits); ES — real-valued vectors; EP —
> finite-state machines; GP — trees/programs ([[eiben-smith-evolutionary-computing]] §3.1).

> [!question]- Q3. Why do R&N call evolutionary algorithms variants of stochastic beam search? What is the difference?
> **Answer.** Both keep a population of $k$ states and choose successors probabilistically in
> proportion to value. EAs add recombination: successors come from *two or more* parents
> (mixing number $\rho \ge 2$); with $\rho = 1$ an EA *is* stochastic beam search
> ([[russell-norvig-aima]] §4.1.3–4.1.4).

> [!question]- Q4. According to the course slides, who created evolutionary computation and what did he evolve?
> **Answer.** Lawrence J. Fogel (1960), who evolved finite-state machines
> ([[slides-04-optimization]], slide 2). (Caveat: Eiben & Smith list earlier pioneers.)

> [!question]- Q5. What is "anytime behaviour" and why is it useful?
> **Answer.** The best-so-far fitness improves quickly early and then flattens; the algorithm
> can be stopped at any time and still return its best solution. Useful when compute time is
> limited, and it shows that long runs often buy little ([[eiben-smith-evolutionary-computing]]
> §3.5).
