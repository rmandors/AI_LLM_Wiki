---
type: concept
summary: Turing's 1950 behavioural test of machine intelligence — a computer passes if a human interrogator chatting by text cannot reliably tell it from a person.
unit: 1
tags: [history, philosophy, acting-humanly, evaluation]
sources: ["[[slides-01-introduction-to-ai]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Turing test

The **Turing test** (Alan Turing, "Computing Machinery and Intelligence", 1950) replaces the vague question "Can a machine think?" with an operational one: a human **interrogator** exchanges typed messages with two hidden parties, a human and a computer; if the interrogator cannot tell which is the machine, the machine is considered intelligent. It is the defining example of the **"acting humanly"** approach to AI ([[russell-norvig-aima]] §1.1.1; [[slides-01-introduction-to-ai]], slide 5).

## How it works

1. Three participants: interrogator (human), a human respondent, and a computer. The interrogator is isolated from both ([[slides-01-introduction-to-ai]], slide 5).
2. Communication only through a **text terminal**, so voice and appearance do not matter.
3. The interrogator asks any questions and finally decides which party is the computer.
4. Turing's concrete version: a 5-minute conversation; the program passes if it fools the interrogator **30 %** of the time. He predicted a machine with ~10⁹ units of storage would pass by 2000 ([[russell-norvig-aima]] §28.1.4).

**Capabilities needed** (R&N §1.1.1): natural language processing, knowledge representation, automated reasoning, machine learning. The **total Turing test** adds physical interaction, requiring computer vision / speech recognition and robotics. These six disciplines "compose most of AI".

## Properties

- **Behavioural**, not introspective: judges only input–output behaviour, not internal mechanism.
- **Human-relative**: measures *similarity to humans*, not *rationality*; a machine that makes no arithmetic errors would be easier to spot.
- **Not a research goal**: AI researchers have spent little effort trying to pass it; R&N compare this with aeronautics, which succeeded once it stopped imitating birds (§1.1.1).
- **Gameable**: ELIZA-style chatbots fool unsuspecting users; Eugene Goostman (2014) fooled 33 % of untrained judges by posing as a Ukrainian boy with poor English; no well-trained judge has been fooled (§28.1.4). "Perhaps the Turing test is really a test of human gullibility."
- Longest-running contest: the **Loebner Prize** (Mitsuku won 2016–2019) (R&N Ch. 28 notes).
- Criticisms (general knowledge): Searle's **Chinese room** (passing ≠ understanding; R&N Ch. 28 notes mention the debate), anthropocentrism, and that LLMs now pass casual versions without agreeing on "intelligence".

## In this course

- Slide 5 of [[slides-01-introduction-to-ai]] presents the test with "2 humans and one computer" and calls it an attempt "to provide an operational and satisfactory definition of intelligence". The slide's wording "the machine is assumed to be intelligent" is the strong reading; Turing's own framing was to replace "can machines think?" with "can machines pass this game?".
- Placed at 1950 on the course timeline, six years before Dartmouth ([[history-of-ai]]).
- The course itself follows the *acting rationally* approach ([[intelligent-agents]], [[rationality-and-peas]]), not the Turing-test approach.

## Common mistakes

- Thinking the computer must be indistinguishable *always*: Turing's threshold was fooling the judge 30 % of the time in 5 minutes.
- Confusing the Turing test with the *Turing machine* (Turing's 1936 model of computation) (general knowledge).
- Claiming that passing it proves consciousness/understanding — it only tests behaviour (the "can machines really think?" question is separate, R&N §28.2).
- Saying R&N define AI by the Turing test — they define it via rational agents.

## Related

[[alan-turing]] · [[history-of-ai]] · [[intelligent-agents]] · [[unit-01-history-review]]

## Practice questions

> [!question]- Q1. Which of R&N's four approaches does the Turing test embody, and why is it not the book's chosen approach?
> **Answer.** *Acting humanly*. It measures human-likeness, not rationality; it is harder to analyse mathematically, and imitating humans is not necessary for intelligence (birds vs aeronautics analogy) ([[russell-norvig-aima]] §1.1.1, §1.1.4).

> [!question]- Q2. List the four capabilities a computer needs to pass the standard Turing test and the two extra ones for the total Turing test.
> **Answer.** NLP, knowledge representation, automated reasoning, machine learning; plus computer vision (and speech recognition) and robotics for the total test ([[russell-norvig-aima]] §1.1.1).

> [!question]- Q3. In 2014 Eugene Goostman fooled 33 % of judges. Did it pass Turing's criterion? Is it intelligent?
> **Answer.** Numerically it exceeded the 30 % threshold, but the judges were untrained amateurs and the persona (a boy with limited English) excused errors. R&N's point: the test can be gamed and measures gullibility as much as intelligence; no well-trained judge has been fooled ([[russell-norvig-aima]] §28.1.4).

> [!question]- Q4. Why does the test use a text terminal?
> **Answer.** To isolate *intelligent behaviour* from physical appearance and voice, which Turing considered irrelevant to intelligence ([[russell-norvig-aima]] §1.1.1; [[slides-01-introduction-to-ai]], slide 5).
