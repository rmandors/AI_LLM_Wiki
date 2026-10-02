---
type: source
summary: Unit 1 deck: a timeline of AI from Talos and the Antikythera mechanism through the Turing test, Dartmouth, LISP, the perceptron, backpropagation, SVMs, deep learning and causal models.
unit: 1
tags: [history, foundations, timeline, neural-networks]
sources: ["[[slides-01-introduction-to-ai]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Slides 01 — Introduction to Artificial Intelligence

**Bibliographic line.** Riofrío, D. *Introduction to Artificial Intelligence* (lecture slides, 19 slides; "thanks to Luciana Valdivieso"). AI course NRC 1651, USFQ, Fall 2026. File: `raw/Slides/01_Introduction to Artificial Intelligence.pptx`.

**What it is.** A visual timeline of milestones on the way to modern AI. Most slides are one milestone + a year. The deck is mostly *chronological from 1700 to 2026* (slides 2–15), then jumps back to antiquity (slides 17–19). Synthesised in [[history-of-ai]]; cheat sheet in [[unit-01-history-review]].

## Key points

- **Slide 2 — What is intelligence?** Dictionary-style definitions: ability to understand/comprehend; to solve problems; knowledge and comprehension; meaning assigned to a proposition; ability, skill, experience. Timeline axis 1700 → 2026 ending in "Generative AI, LLMs, Agents".
- **Slide 3 — Automata.** 1770 *Mechanical Turk* by Wolfgang von Kempelen, a machine that *appeared* to play strong chess. 1768–1774 Pierre Jaquet-Droz's automata: the musician, the draughtsman, the writer.
- **Slide 4 — Early computers.** 1936 *Z1* by Konrad Zuse: binary calculator reading operations from punched cards, +, −, ×, ÷, floating point, memory. 1945 *ENIAC*, labelled "First Universal Computer": general purpose, programmable, vacuum tubes, 170 m², 27 t.
- **Slide 5 — 1950 Turing test.** Two humans + one computer; the interrogator is isolated and chats by text terminal; if they fail to identify the computer, the machine "is assumed to be intelligent"; an attempt at an operational definition of intelligence. → [[turing-test]], [[alan-turing]]
- **Slide 6 — Early languages.** FORTRAN 1957 (IBM): numerical/scientific computing, imperative (state, conditionals, loops). LISP 1955–1958 by [[john-mccarthy]]: lambda calculus and recursion, dynamic types, list processing, prefix calls `(f a1 a2 a3)`.
- **Slide 7 — 1956 Birth of AI.** Quote from the Dartmouth proposal ("every aspect of learning... can in principle be so precisely described that a machine can be made to simulate it"); organisers Shannon, Minsky, Rochester, McCarthy; proposal topics: automatic computers, programming a computer to use language, neuron nets, theory of the size of a calculation, self-improvement, abstractions, randomness and creativity.
- **Slide 8 — 1958 Perceptron** ([[frank-rosenblatt]]): neuron-inspired model; a neural network is a distributed parallel processor of simple units that stores experiential knowledge in synaptic weights acquired by a learning process. → [[perceptron]]
- **Slide 9 — 1970 Prolog.** "Algorithm = Logic + Control"; expert systems in legal/medical/financial domains; programs are sets of positive clauses in a notation like first-order logic. → [[prolog]], [[horn-clauses]] (see Issues).
- **Slide 10 — What is a model?** A mathematical description of a system or phenomenon; a hypothesis; built from a-priori rules or observations. *Formal methods*: first-order calculus, lambda calculus, temporal logic, rewriting systems, causal calculus. *Statistical methods*: regression, classification, Bayesian networks, Markov networks.
- **Slide 11 — Backpropagation** (dated 1975): computes the gradient of the loss w.r.t. every weight; allowed training neurons in series with nonlinearity, so a network could solve **XOR**.
- **Slide 12 — 1995 SVM.** Vapnik and colleagues at AT&T Bell Labs: a linear classifier, similar to the perceptron, that **maximises the margin** between two subspaces (the objective formula is an image).
- **Slide 13 — Deep learning** (timeline year 2000): tools existed since the 1960s, the *term* introduced in 1986; Bengio, Hinton and LeCun laid the foundations for training deep networks with a modified backprop.
- **Slide 14 — "Limitations of Statistical Models"** — title only.
- **Slide 15 — Causal models.** Decide whether A causes B or B causes A (not both); [[judea-pearl]]'s causal calculus (dated 1987) encodes cause–effect relations in a **directed acyclic graph** (DAG).
- **Slides 17–18 — Antikythera mechanism.** Wreck found 1900; gear noticed 1902 and dismissed; study resumed 1951 and 1971 (82 fragments, X-ray/gamma-ray); dated ~200 BC; earliest known **analog computer**, predicted astronomical positions and eclipses up to 19 years ahead and the dates of six ancient Greek games.
- **Slide 19 — Talos** (dated "800 BC?"): bronze giant automaton protecting Europa on Crete.

## Pages that use this source

[[history-of-ai]], [[turing-test]], [[perceptron]], [[alan-turing]], [[john-mccarthy]], [[frank-rosenblatt]], [[judea-pearl]], [[unit-01-history-review]], [[prolog]], [[overview]], [[midterm-01-review]].

## Issues found

> [!warning] Contradiction — who created Prolog
> Slide 9 says Prolog (1970) was "created by Dennis Ritchie at Bell Labs" and is "an imperative, compiled language that provides control statements for state management, decision-making, repetitive tasks". That text describes **C** (Ritchie, Bell Labs, ~1972), not Prolog. The Prolog deck ([[slides-xx-logic-programming-prolog]], slide 8) says Prolog was born in Marseille in **1972** (Alain Colmerauer and Philippe Roussel) on theory from Robert Kowalski; R&N agree ([[russell-norvig-aima]] Ch. 9 Bibliographical notes). Prolog is **declarative**, not imperative. The Prolog deck is right. See [[alain-colmerauer]], [[robert-kowalski]].

> [!warning] Contradiction — dating backpropagation and "deep learning"
> Slide 11 dates backpropagation to **1975**. R&N say it was discovered several times (Kelley 1960, Bryson 1962,..., **Werbos 1974** PhD thesis, applied to neural nets) and became widely known with **Rumelhart, Hinton & Williams (1986)** ([[russell-norvig-aima]] §1.3.3, §1.3.5 and Ch. 22 notes). Slide 13 says the *term* "deep learning" was introduced in 1986; this matches Rina Dechter's 1986 use in machine learning (general knowledge), but R&N date the deep-learning era to 2011 onwards (§1.3.8). Not wrong, but easy to confuse on an exam.

> [!warning] Contradiction — first computers
> Slide 4 dates the **Z1 to 1936**; Zuse built it 1936–1938, finished 1938 (general knowledge). Slide 4 calls **ENIAC (1945)** the "First Universal Computer". R&N credit the first operational programmable computer to Zuse's **Z-3 (1941)**, the first electronic computer to Atanasoff & Berry's ABC (1940–42), and Colossus (1943); ENIAC was "the most influential forerunner of modern computers" ([[russell-norvig-aima]] §1.2.6). "One of the first general-purpose electronic computers" is the safe phrasing.

- **Image-only / empty slides:** slide **14** ("Limitations of Statistical Models" — title only, content is an image) and slide **16** (completely empty). Their content is not recoverable; the closest textbook material is R&N §1.3.6 (probabilistic reasoning) and Pearl's causal networks ([[russell-norvig-aima]] §13.5). Slide 12's SVM objective is an image; the standard form is "maximise the margin $2/\lVert w\rVert$", i.e. minimise $\tfrac12\lVert w\rVert^2$ s.t. $y_i(w\cdot x_i+b)\ge 1$ (general knowledge).
- **Talos date.** Slide 19 says "The Iliad describes Talos... 800 BC?". R&N place the Talos legend in "7th century BCE Greek mythology" and say Greek legends "as far back as Homer (circa 700 BCE)" envisioned Talos ([[russell-norvig-aima]] Ch. 26 and Ch. 28 notes). In the classical sources Talos guards Crete and is best known from Apollonius' *Argonautica*; the Iliad attribution is doubtful (general knowledge).
- **Causal calculus date.** Slide 15 says Pearl proposed causal calculus in 1987. Pearl's *Probabilistic Reasoning in Intelligent Systems* (Bayesian networks) is **1988** ([[russell-norvig-aima]] §1.3.6); the *do*-calculus is from the 1990s (Pearl 1995; *Causality* 2000) (general knowledge). Treat "1987" as approximate.
- **Mechanical Turk** was a hoax (a hidden human chess player operated it) — the slide's "appeared to play" hints at this but does not say it (general knowledge).
- **Dartmouth organisers.** Slide 7 lists Shannon, Minsky, Rochester, McCarthy — correct; R&N add that there were 10 attendees incl. Newell & Simon, who presented the Logic Theorist ([[russell-norvig-aima]] §1.3.1).
- The deck's chronology is non-monotonic (antiquity appears last), so the [[history-of-ai]] page re-sorts it.
