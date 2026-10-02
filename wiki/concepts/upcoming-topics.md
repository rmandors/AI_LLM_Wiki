---
type: concept
summary: Syllabus units not taught yet (planning, probability, Markov models, machine learning, ethics), with the textbook chapters to ingest when they arrive.
unit: [5, 7, 8, 10]
tags: [roadmap, syllabus]
sources: ["[[slides-00-instructor-introduction]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Upcoming topics

The syllabus has ten units ([[slides-00-instructor-introduction]], slide 4). As of
2026-10-01 there are slides for units 1–4, 6 and 9 in `raw/`. This page is a placeholder
for the remaining units so links have a target. When a deck arrives, ingest it and
split this page into real concept pages.

| Unit | Topic | Textbook chapters to ingest | Expected pages |
|---|---|---|---|
| 5 | Knowledge, reasoning and planning | [[russell-norvig-aima]] Ch. 7.1–7.2 (knowledge-based agents, wumpus world), Ch. 10 (knowledge representation), Ch. 11 (classical planning) | knowledge-based-agents, wumpus-world, classical-planning |
| 7 | Uncertainty: probability, Bayes' theorem, naive Bayes | Ch. 12 (§12.1–12.6), Ch. 13 (Bayesian networks) | probability-basics, bayes-rule, naive-bayes, bayesian-networks |
| 8 | Temporal reasoning: Markov | Ch. 14 (§14.1–14.3: Markov chains, filtering, HMMs) | markov-chains, hidden-markov-models |
| 10 | Machine learning and neural networks; ethics and safety | Ch. 19 (§19.6.4 linear classifiers), Ch. 21 (deep learning), Ch. 27 (ethics) | expand [[perceptron]], neural-networks, backpropagation, ai-ethics-and-safety |

What already connects to these units:

- Unit 1 history mentions Bayesian networks and causal models ([[judea-pearl]],
  [[history-of-ai]]), the perceptron and backpropagation ([[frank-rosenblatt]],
  [[perceptron]]).
- Utility-based agents need probabilities of outcomes ([[agent-architectures]]).
- Stochastic environments ([[environment-properties]]) are where Units 7–8 apply.
- PSO was first tested by training neural-network weights ([[kennedy-eberhart-1995-pso]]),
  and gradient descent ([[gradient-descent]]) is the optimizer behind backpropagation.

## Practice questions

> [!question]- Q1. Which syllabus units have no slides in the wiki yet?
> **Answer.** Units 5 (knowledge, reasoning, planning), 7 (uncertainty), 8 (Markov
> models) and 10 (ML, neural networks, ethics), as of 2026-10-01.

> [!question]- Q2. Which agent type from Unit 2 most directly needs Unit 7's probability tools, and why?
> **Answer.** The utility-based agent: it picks the action that maximises *expected*
> utility, which requires the probabilities of each outcome ([[agent-architectures]],
> [[russell-norvig-aima]] §2.4.5).
