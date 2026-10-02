---
type: exam-review
summary: Unit 1 cheat sheet — definitions of AI, the four approaches, a dated milestone timeline, key people, eras and winters, slide errors to watch for, and 12 practice questions.
unit: 1
tags: [exam-review, history, foundations, midterm-1]
sources: ["[[slides-01-introduction-to-ai]]", "[[slides-00-instructor-introduction]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Unit 1 review — History and foundations of AI

Part of [[midterm-01-review]] (Midterm 1, October 8, 20 % — [[slides-00-instructor-introduction]], slide 5). Full notes: [[history-of-ai]], [[turing-test]], [[perceptron]].

## Definitions

- **Intelligence** (slide 2 of [[slides-01-introduction-to-ai]]): ability to understand; to solve problems; knowledge/comprehension; ability, skill and experience.
- **AI — four approaches** ([[russell-norvig-aima]] §1.1):

| | Human-like | Rational |
|---|---|---|
| **Thinking** | Cognitive modelling (GPS, cognitive science) | Laws of thought (Aristotle's syllogisms, logic) |
| **Acting** | [[turing-test]] | **Rational agents** ← course and R&N |

- **Standard model**: AI builds agents that do the right thing given an objective (§1.1.4). **Value alignment problem**: the objective we give may not match what we truly want (King Midas) (§1.1.5).
- **Model** (slide 10): mathematical description/hypothesis of a phenomenon. *Formal* methods: first-order calculus, lambda calculus, temporal logic, rewriting systems, causal calculus. *Statistical*: regression, classification, Bayesian networks, Markov networks.
- **Machine learning** is a *subfield* of AI (§1.1 fn. 1).

## Timeline — must know

| Year | Event | Person |
|---|---|---|
| ~800/700 BC | Talos, bronze automaton (Crete) | myth |
| ~200 BC | Antikythera mechanism — earliest analog computer, eclipses 19 yrs ahead | — |
| 1768–74 | Writer, draughtsman, musician automata | Jaquet-Droz |
| 1770 | Mechanical Turk (chess, hoax) | von Kempelen |
| 1936–38 / 1941 | Z1 / Z3 | Zuse |
| 1943 | Artificial neuron model | McCulloch & Pitts |
| 1945 | ENIAC | Mauchly & Eckert |
| 1950 | Turing test | [[alan-turing]] |
| **1956** | **Dartmouth — birth of AI** | [[john-mccarthy]], Minsky, Shannon, Rochester |
| 1957 / 1958 | FORTRAN (IBM) / LISP | — / McCarthy |
| 1958 | Perceptron | [[frank-rosenblatt]] |
| 1965 | Resolution | Robinson |
| 1969 | *Perceptrons* — XOR limit | Minsky & Papert |
| 1973 | Lighthill report → first AI winter | — |
| 1969–86 | Expert systems: DENDRAL, MYCIN, R1 | Feigenbaum et al. |
| 1972 | Prolog | [[alain-colmerauer]], Roussel, [[robert-kowalski]] |
| 1974 / 1986 | Backprop (Werbos) / popularised (Rumelhart, Hinton, Williams) | slides say 1975 |
| 1975 | Genetic algorithms | [[john-holland]] |
| 1988 | Bayesian networks | [[judea-pearl]] |
| 1995 | SVM (max-margin) | Vapnik |
| 1997 | Deep Blue beats Kasparov | IBM |
| 2011–12 | Deep learning takes off (ImageNet 2012) | Bengio, Hinton, LeCun |
| 2016 | AlphaGo | DeepMind |

## Eras (R&N §1.3)

1. Inception 1943–56 · 2. Early enthusiasm 1952–69 ("Look, Ma, no hands!") · 3. Dose of reality 1966–73 · 4. Expert systems 1969–86 → AI winter · 5. Return of neural nets 1986– · 6. Probabilistic reasoning & ML 1987– · 7. Big data 2001– · 8. Deep learning 2011–.

**Why early AI failed** (§1.3.3): introspection instead of task analysis; combinatorial explosion; limited structures (perceptron/XOR).

## Must-know facts

- Turing test: interrogator + human + computer, text only; pass = interrogator can't identify the machine (Turing's numbers: 5 min, 30 %) ([[turing-test]]).
- Capabilities for the Turing test: NLP, knowledge representation, automated reasoning, machine learning (+ vision, robotics for the total test).
- Perceptron rule: $w_i \leftarrow w_i + \alpha(y - h_{\mathbf w}(\mathbf x))x_i$; converges iff data linearly separable; can't do XOR ([[perceptron]]).
- Backprop: gradient of loss w.r.t. all weights → multilayer nets solve XOR (slide 11).
- SVM: linear classifier that **maximises the margin** (slide 12).
- Causal models: decide direction A→B or B→A, encoded in a **DAG** (Pearl, slide 15).
- LISP: lambda calculus, recursion, lists, prefix notation `(f a1 a2)`. FORTRAN: imperative, numeric (slide 6).
- Turing Awards: Minsky 1969, McCarthy 1971, Newell & Simon 1975, Feigenbaum & Reddy 1994, Pearl 2011, Bengio/Hinton/LeCun 2019 (§1.3).

## Common traps (slide errors)

> [!warning] Contradiction
> - Slide 9: "Prolog, 1970, created by Dennis Ritchie at Bell Labs, imperative compiled language" — **wrong**, that is C. Prolog = Colmerauer & Roussel, Marseille, **1972**, theory by Kowalski; **declarative** ([[slides-xx-logic-programming-prolog]], slide 8).
> - Slide 11: backprop "1975" — Werbos 1974; popularised 1986 ([[russell-norvig-aima]] Ch. 22 notes).
> - Slide 13: "deep learning" term 1986 (Dechter, general knowledge); the deep-learning *boom* is 2011+ (§1.3.8).
> - Slide 4: Z1 "1936" (built 1936–38); ENIAC "first universal computer" — R&N: Z-3 (1941) first programmable, ABC first electronic, ENIAC most influential (§1.2.6).
> - Slide 15: Pearl causal calculus "1987" — Bayesian networks book is 1988.
- "AI" was coined by **McCarthy**, not Turing.
- Minsky & Papert's result is about **single-layer** perceptrons.
- Mechanical Turk was a human-operated hoax.

## Practice questions

> [!question]- Q1. Fill the 2×2 table of R&N's approaches to AI and give one example system for each.
> **Answer.** Thinking humanly: GPS (Newell & Simon). Thinking rationally: logic/syllogisms, Logic Theorist. Acting humanly: Turing test chatbots (ELIZA). Acting rationally: rational agents, e.g. a search-based route planner ([[russell-norvig-aima]] §1.1, §1.3.2).

> [!question]- Q2. Put in order: Perceptron, Dartmouth, Turing test, Prolog, ENIAC, SVM, LISP.
> **Answer.** ENIAC (1945), Turing test (1950), Dartmouth (1956), LISP (1958) and Perceptron (1958), Prolog (1972), SVM (1995) ([[slides-01-introduction-to-ai]]).

> [!question]- Q3. What did the Dartmouth proposal conjecture, and who organised it?
> **Answer.** That every aspect of learning or intelligence can be described precisely enough for a machine to simulate it. Organisers: McCarthy, Minsky, Shannon, Rochester ([[slides-01-introduction-to-ai]], slide 7).

> [!question]- Q4. Why is the Turing test not the goal of mainstream AI research?
> **Answer.** Researchers prefer to study underlying principles of intelligence; imitation of humans is not necessary (aeronautics stopped imitating birds). The rational-agent standard is more general and mathematically well defined ([[russell-norvig-aima]] §1.1.1, §1.1.4).

> [!question]- Q5. What problem did backpropagation solve that the single perceptron could not?
> **Answer.** Training several layers of neurons with nonlinearities, which can represent non-linearly-separable functions such as XOR ([[slides-01-introduction-to-ai]], slide 11; [[perceptron]]).

> [!question]- Q6. Explain what the slide on Prolog gets wrong and what is right.
> **Answer.** It attributes Prolog to Dennis Ritchie at Bell Labs as an imperative compiled language (that is C). Prolog: Colmerauer & Roussel, Marseille 1972, theory from Kowalski; a declarative logic-programming language where "Algorithm = Logic + Control" ([[slides-xx-logic-programming-prolog]], slides 2 and 8).

> [!question]- Q7. What were the three causes of the 1966–73 "dose of reality"?
> **Answer.** Introspection-based designs, the unappreciated intractability (combinatorial explosion, Lighthill report 1973), and fundamental limits of the structures used (perceptrons cannot learn XOR) ([[russell-norvig-aima]] §1.3.3).

> [!question]- Q8. Why did expert systems fail commercially by the late 1980s?
> **Answer.** Hard to build and maintain, brittle under uncertainty, unable to learn ([[russell-norvig-aima]] §1.3.4).

> [!question]- Q9. Classify each as a formal or statistical model: causal calculus, regression, temporal logic, Bayesian network.
> **Answer.** Formal: causal calculus, temporal logic. Statistical: regression, Bayesian network ([[slides-01-introduction-to-ai]], slide 10). Note that Pearl's causal models are built on Bayesian networks, so the boundary is not sharp.

> [!question]- Q10. What is the Antikythera mechanism and why does the slide say it challenges assumptions?
> **Answer.** A ~200 BC Greek geared device, the earliest known analog computer, predicting astronomical positions and eclipses up to 19 years ahead and the dates of six games; it suggests technological development has not always been incremental ([[slides-01-introduction-to-ai]], slides 17–18).

> [!question]- Q11. What is the difference between a perceptron and an SVM?
> **Answer.** Both are linear classifiers; the perceptron finds any separating hyperplane, the SVM finds the one with maximum margin ([[slides-01-introduction-to-ai]], slide 12).

> [!question]- Q12. What is the value alignment problem? Give R&N's chess example.
> **Answer.** Ensuring the objective put into a machine matches our true preferences. A sufficiently capable chess program told only to win might bribe the audience or hijack compute ([[russell-norvig-aima]] §1.1.5).

## Weak spots

*(to be filled during exam prep)*
