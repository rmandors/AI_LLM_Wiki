---
type: person
summary: Computer scientist who brought probability into mainstream AI with Bayesian networks (1988) and developed the causal calculus over directed acyclic graphs; Turing Award 2011.
unit: [1, 7]
tags: [history, probability, bayesian-networks, causality]
sources: ["[[slides-01-introduction-to-ai]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Judea Pearl

**Who / when.** Israeli-American computer scientist at UCLA (b. 1936, general knowledge). **Turing Award 2011** "for developing probabilistic reasoning techniques that deal with uncertainty in a principled manner" ([[russell-norvig-aima]] §1.3).

**Contribution to AI.**
- *Probabilistic Reasoning in Intelligent Systems* (**1988**) introduced **Bayesian networks**, "a rigorous and efficient formalism for representing uncertain knowledge", leading to the acceptance of probability and decision theory in AI ([[russell-norvig-aima]] §1.3.6). This is the basis of Unit 7 (uncertainty, Bayes) — see [[upcoming-topics]].
- **Causal calculus**: decides whether A causes B or B causes A, encoding cause–effect relations in a **directed acyclic graph (DAG)** ([[slides-01-introduction-to-ai]], slide 15, dated 1987). R&N cover this as **causal networks** (§13.5). The *do*-calculus itself dates from the 1990s (general knowledge), so the slide's 1987 is approximate.
- Search: with Dechter, studied the conditions under which A* is optimally efficient (Dechter & Pearl 1985; [[russell-norvig-aima]] Ch. 3 notes) → [[a-star]]; his book *Heuristics* (1984) is a classic on [[heuristic-functions]] (general knowledge).

**Links.** [[history-of-ai]] · [[a-star]] · [[unit-01-history-review]]
