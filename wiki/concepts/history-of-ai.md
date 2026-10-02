---
type: concept
summary: Chronological synthesis of AI history — ancient automata, early computers, Turing and Dartmouth, symbolic AI and its winters, expert systems, neural-network revivals, probabilistic ML and deep learning.
unit: 1
tags: [history, foundations, timeline, symbolic-ai, connectionism]
sources: ["[[slides-01-introduction-to-ai]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# History of AI

**Artificial intelligence** is the study and construction of machines that behave intelligently. R&N organise definitions along two axes — *human vs rational* and *thinking vs acting* — giving four approaches: acting humanly ([[turing-test]]), thinking humanly (cognitive modelling), thinking rationally ("laws of thought", logic) and **acting rationally** (the *rational agent* approach), which dominates the field and this course ([[russell-norvig-aima]] §1.1). Its history alternates between bursts of optimism and "AI winters", and between two traditions: **symbolic** (logic, search, rules — [[prolog]], [[a-star]]) and **connectionist / statistical** (neural networks, learning — [[perceptron]]).

## How it works — the timeline

Sorted chronologically (the slides present antiquity last).

| When | Milestone | Why it matters | Source |
|---|---|---|---|
| ~800/700 BC | **Talos**, bronze giant automaton guarding Crete | Oldest idea of an artificial being | [[slides-01-introduction-to-ai]] s19; [[russell-norvig-aima]] Ch. 28 notes |
| ~200 BC | **Antikythera mechanism** | Earliest known analog computer; predicted eclipses up to 19 years ahead | s17–18 |
| 1768–74 | Jaquet-Droz automata (musician, draughtsman, writer) | Programmable mechanical behaviour | s3 |
| 1770 | von Kempelen's **Mechanical Turk** (chess) | Illusion of machine intelligence (a hidden human, general knowledge) | s3 |
| 1805 | Jacquard loom, punched cards | First programmable machine | [[russell-norvig-aima]] §1.2.6 |
| 1936–41 | Zuse's Z1 (1936–38), Z3 (1941) | Binary, floating point; Z3 = first operational programmable computer | s4; §1.2.6 |
| 1943 | **McCulloch & Pitts** artificial neuron | First work recognised as AI; neurons as logic gates | §1.3.1 |
| 1945 | **ENIAC** | General-purpose, programmable, vacuum tubes | s4; §1.2.6 |
| 1949 | Hebbian learning | First weight-update rule | §1.3.1 |
| 1950 | **Turing**, "Computing Machinery and Intelligence" | [[turing-test]]; also proposes ML, GAs, RL | s5; §1.3.1 |
| 1952–56 | Samuel's checkers (learns; on TV 1956) | Early machine learning / RL | §1.3.2 |
| **1956** | **Dartmouth workshop** (McCarthy, Minsky, Shannon, Rochester) | Birth and name of "artificial intelligence"; Logic Theorist shown | s7; §1.3.1 |
| 1957 | FORTRAN (IBM) | Imperative numerical language | s6 |
| 1958 | **LISP** ([[john-mccarthy]]); *Advice Taker* | Dominant AI language for 30 years; knowledge-based AI | s6; §1.3.2 |
| 1958 | **Perceptron** ([[frank-rosenblatt]]) | Learning linear classifier | s8; §1.3.2 |
| ~1959–61 | GPS (Newell & Simon) | "Thinking humanly"; physical symbol system hypothesis | §1.3.2 |
| 1965 | Robinson's **resolution** | Complete FOL theorem proving → [[conjunctive-normal-form-and-resolution]] | §1.3.2 |
| 1966–73 | **Dose of reality**: combinatorial explosion, Lighthill report (1973), Minsky & Papert *Perceptrons* (1969, XOR) | First AI winter; neural-net funding collapses | §1.3.3 |
| 1968 | A* (Hart, Nilsson, Raphael) | → [[a-star]] | [[russell-norvig-aima]] Ch. 3 notes |
| 1969–86 | **Expert systems**: DENDRAL, MYCIN (~450 rules, certainty factors), R1/XCON (saved DEC ~$40M/yr) | Knowledge-intensive "strong methods" | §1.3.4 |
| 1972 | **Prolog** (Colmerauer & Roussel, Marseille; theory by Kowalski) | Logic programming → [[prolog]] | [[slides-xx-logic-programming-prolog]] s8 |
| 1974 / 1986 | **Backpropagation**: Werbos thesis 1974; popularised by Rumelhart, Hinton & Williams 1986 | Trains multilayer nets, solves XOR | s11 (says 1975); §1.3.5, Ch. 22 notes |
| 1975 | Holland's **genetic algorithms** | → [[genetic-algorithms]], [[john-holland]] | [[slides-04-optimization]] s2 |
| 1981 | Japan's Fifth Generation project (Prolog machines) | | §1.3.4 |
| late 1980s | **Second AI winter** after the expert-system boom | Brittle, could not learn | §1.3.4 |
| 1988 | **Pearl**, Bayesian networks; Sutton links RL and MDPs | Probability enters mainstream AI | §1.3.6 |
| 1995 | **SVM** (Vapnik) | Maximum-margin classifier | s12 |
| 1995–96 | PSO (Kennedy & Eberhart), Ant System (Dorigo) | Swarm intelligence → [[swarm-intelligence]] | [[slides-04-optimization]] s8, s12 |
| 1997 | Deep Blue beats Kasparov | → [[alpha-beta-pruning]] | [[russell-norvig-aima]] §1.4 |
| 2001– | **Big data** | Data size beats algorithm tweaks | §1.3.7 |
| 2011– | **Deep learning** (ImageNet 2012, AlphaGo 2016) | Bengio, Hinton, LeCun (Turing Award 2019) | s13; §1.3.8 |
| 2020s | Generative AI, LLMs, agents | | s2 |

## Properties — recurring themes

- **Hype cycles.** Simon (1957) predicted a computer chess champion within 10 years; it took ~40 ([[russell-norvig-aima]] §1.3.3).
- **Why early AI failed** (§1.3.3): (1) programs based on "informed introspection" rather than task analysis; (2) ignoring **intractability** (combinatorial explosion — the motivation for [[heuristic-functions]]); (3) limits of basic structures (perceptrons cannot represent XOR).
- **Weak vs strong methods** (§1.3.4): general search ("weak", does not scale) vs domain knowledge (expert systems).
- **Neats vs scruffies** (§1.3.6 footnote): mathematical rigour vs try-it-and-see.
- **Formal vs statistical models** ([[slides-01-introduction-to-ai]] s10): formal (first-order calculus, lambda calculus, temporal logic, rewriting, causal calculus) vs statistical (regression, classification, Bayesian and Markov networks). Logic units = formal; uncertainty/ML units = statistical.
- **Turing Award milestones** (§1.3): Minsky 1969, McCarthy 1971, Newell & Simon 1975, Feigenbaum & Reddy 1994, Pearl 2011, Bengio–Hinton–LeCun 2019.

## In this course

- Slides 01 is a milestone timeline ([[slides-01-introduction-to-ai]]); it frames AI from "What do we mean by intelligence?" (slide 2) to "Generative AI, LLMs, Agents".
- Course units mirror the eras: search (units 2–4) and logic (unit 6) are the symbolic tradition; probability/Markov (7–8) the 1988+ probabilistic era; perceptron/ML (10) the connectionist line; bio-inspired optimisation (9) the evolutionary line ([[slides-00-instructor-introduction]], slide 4).
- People: [[alan-turing]], [[john-mccarthy]], [[frank-rosenblatt]], [[judea-pearl]], [[john-holland]], [[robert-kowalski]], [[alain-colmerauer]], [[kennedy-and-eberhart]], [[marco-dorigo]], [[dervis-karaboga]].

> [!warning] Contradiction
> Slides 01 slide 9 says Prolog was created in 1970 by Dennis Ritchie at Bell Labs as an imperative compiled language — that describes C. The Prolog deck (slide 8) says Colmerauer & Roussel, Marseille, 1972, theory from Kowalski; R&N agree (Ch. 9 notes). See [[slides-01-introduction-to-ai]] for the other dating issues (backprop 1975, Z1 1936, ENIAC "first universal computer").

## Common mistakes

- Saying Turing *coined* "artificial intelligence" — it was **McCarthy** in the 1955 Dartmouth proposal ([[russell-norvig-aima]] §1.3.1 fn. 12).
- Dating backprop to 1986 as its *invention*: 1986 is its *popularisation*; the algorithm existed since the 1960s (Kelley, Bryson) and Werbos applied it to neural nets in 1974.
- Thinking Minsky & Papert proved neural networks useless — their result applies to **single-layer** perceptrons only (§1.3.3).
- Confusing "ML" with "AI": ML is a subfield (R&N §1.1 fn. 1).
- Calling the Mechanical Turk an AI — it was a hoax (general knowledge).

## Related

[[turing-test]] · [[perceptron]] · [[intelligent-agents]] · [[unit-01-history-review]] · [[prolog]] · [[genetic-algorithms]] · [[evolutionary-computation]] · [[minimax]] · [[overview]]

## Practice questions

> [!question]- Q1. Name R&N's four approaches to defining AI and say which one the book (and this course) adopts.
> **Answer.** Acting humanly (Turing test), thinking humanly (cognitive modelling), thinking rationally (laws of thought/logic), acting rationally (rational agents). The rational-agent approach is adopted because it is more general than "laws of thought" (correct inference is only one way to act rationally) and mathematically well defined ([[russell-norvig-aima]] §1.1.4).

> [!question]- Q2. Give the three reasons R&N give for the "dose of reality" of 1966–1973.
> **Answer.** (1) Systems relied on informed introspection rather than careful analysis of the task; (2) the intractability / combinatorial explosion of problems was not appreciated (Lighthill report, 1973); (3) fundamental limits of the structures used, e.g. Minsky & Papert (1969) showed a two-input perceptron cannot learn XOR ([[russell-norvig-aima]] §1.3.3).

> [!question]- Q3. Who organised the 1956 Dartmouth workshop and what was its central conjecture?
> **Answer.** McCarthy, Minsky, Shannon and Rochester. "Every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it" ([[slides-01-introduction-to-ai]], slide 7; [[russell-norvig-aima]] §1.3.1).

> [!question]- Q4. Why did expert systems lead to an AI winter in the late 1980s?
> **Answer.** They were hard to build and maintain for complex domains, their reasoning broke down under uncertainty, and they could not learn from experience ([[russell-norvig-aima]] §1.3.4). The response was probabilistic reasoning (Pearl's Bayesian networks, 1988) and machine learning (§1.3.6).

> [!question]- Q5. The slides say backpropagation is from 1975 and Prolog from 1970 by Dennis Ritchie. Correct both.
> **Answer.** Backprop: discovered several times from the 1960s; Werbos (1974) applied it to neural nets; Rumelhart, Hinton & Williams (1986) made it widely known ([[russell-norvig-aima]] Ch. 22 notes). Prolog: Colmerauer & Roussel, Marseille, 1972, with theory from Kowalski ([[slides-xx-logic-programming-prolog]], slide 8). Ritchie created C.

> [!question]- Q6. Classify as formal or statistical model: temporal logic, naive Bayes, lambda calculus, Markov network, rewriting system.
> **Answer.** Formal: temporal logic, lambda calculus, rewriting system. Statistical: naive Bayes (a classification technique / Bayesian network), Markov network ([[slides-01-introduction-to-ai]], slide 10).
