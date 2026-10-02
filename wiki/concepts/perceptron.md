---
type: concept
summary: Rosenblatt's 1958 single artificial neuron — a weighted sum passed through a hard threshold, trained by the perceptron learning rule; it learns any linearly separable function but cannot represent XOR.
unit: [1, 10]
tags: [neural-networks, machine-learning, linear-classifier, history]
sources: ["[[slides-01-introduction-to-ai]]", "[[russell-norvig-aima]]"]
updated: 2026-10-01
---

# Perceptron

The **perceptron** is the simplest neural network: one artificial neuron that computes a weighted sum of its inputs and outputs 1 if the sum reaches a threshold, else 0. It was proposed by [[frank-rosenblatt]] (1958) as "a computational model inspired by the biological operation of neurons in the brain", where knowledge is stored in the **synaptic weights** and acquired from the environment by a learning process ([[slides-01-introduction-to-ai]], slide 8). Geometrically it is a **linear classifier**: it separates the input space with a hyperplane.

> [!note] Stub for Unit 10
> This page covers what Unit 1 needs. It will be expanded when Unit 10 (machine learning and neural networks) is taught; see [[upcoming-topics]].

## How it works

With a dummy input $x_0 = 1$ so that $w_0$ acts as the bias ([[russell-norvig-aima]] §19.6.4):

$$h_{\mathbf w}(\mathbf x) = \text{Threshold}(\mathbf w\cdot\mathbf x),\qquad \text{Threshold}(z) = \begin{cases}1 & z \ge 0\\ 0 & z<0\end{cases}$$

**Perceptron learning rule** (R&N Eq. 19.8), for one example $(\mathbf x, y)$ and learning rate $\alpha$:

$$w_i \leftarrow w_i + \alpha\,\big(y - h_{\mathbf w}(\mathbf x)\big)\,x_i$$

- Output correct → no change.
- $y=1$, output 0 → weights move *toward* $\mathbf x$ (makes $\mathbf w\cdot\mathbf x$ larger).
- $y=0$, output 1 → weights move *away* from $\mathbf x$.

Examples are presented one at a time, usually in random order (like stochastic [[gradient-descent]]).

```text
repeat until no errors (or max epochs):
    for each (x, y) in training set (shuffled):
        y_hat = 1 if w·x >= 0 else 0
        w = w + alpha * (y - y_hat) * x
```

## Properties

- **Convergence theorem** (Block et al. 1962): if the data are **linearly separable**, the rule converges to a perfect separator ([[russell-norvig-aima]] §1.3.2, §19.6.4).
- **Non-separable data**: with fixed $\alpha$ it may never settle; with a decaying rate $\alpha = O(1/t)$ and random order it converges to a minimum-error solution; finding that minimum is NP-hard (§19.6.4).
- **Gradient**: the hard threshold has zero gradient almost everywhere, so ordinary gradient descent cannot be used — hence the special rule (§19.6.4). Replacing the threshold with a sigmoid gives logistic regression (general knowledge).
- **XOR limitation**: a single perceptron cannot represent XOR (the "inputs differ" function). Minsky & Papert's *Perceptrons* (1969) proved such limits; neural-net funding "dwindled to almost nothing" though the result does not apply to multilayer nets (§1.3.3).
- **Fix**: stack neurons with nonlinear activations (multilayer perceptron) trained by **backpropagation**, which "enabled a neural network to solve the XOR problem" ([[slides-01-introduction-to-ai]], slide 11).

## In this course

- Slide 8 of [[slides-01-introduction-to-ai]] (1958) introduces the perceptron and the definition of a neural network as "a distributed parallel processor made up of simple processing units".
- Slide 11 (backpropagation) and slide 12 (SVM, "a linear classification algorithm similar to … the perceptron that attempts to maximize the margin") build on it; slide 13 extends to deep learning.
- Unit 10 of the syllabus is "Machine learning and neural networks: perceptron" ([[slides-00-instructor-introduction]], slide 4).

## Common mistakes

- Forgetting the bias $w_0$ (without it the separating line must pass through the origin).
- Updating weights when the prediction is already correct — the rule only changes weights on errors.
- Believing Minsky & Papert proved *all* neural nets are limited — only single-layer perceptrons.
- Mixing up the perceptron (hard threshold, maximises nothing in particular) and the SVM (chooses the *maximum-margin* separator).
- Attributing backprop to 1975 as the slides do; see [[history-of-ai]] (Werbos 1974; Rumelhart, Hinton & Williams 1986).

## Related

[[frank-rosenblatt]] · [[history-of-ai]] · [[gradient-descent]] · [[upcoming-topics]] · [[unit-01-history-review]]

## Practice questions

> [!question]- Q1. Prove that no single perceptron computes XOR.
> **Answer.** Need $w_0<0$ for (0,0)→0; $w_0+w_1\ge 0$ for (1,0)→1; $w_0+w_2\ge0$ for (0,1)→1; $w_0+w_1+w_2<0$ for (1,1)→0. Adding the middle two: $2w_0+w_1+w_2\ge 0$. Adding the first and last: $2w_0+w_1+w_2<0$. Contradiction — XOR is not linearly separable (general knowledge; limitation stated in [[russell-norvig-aima]] §1.3.3).

> [!question]- Q2. One update step: $\mathbf w=(0,0,0)$ (bias first), $\alpha=1$, example $\mathbf x=(1,1,0)$ (with $x_0=1$), label $y=0$. What is the new $\mathbf w$?
> **Answer.** $\mathbf w\cdot\mathbf x=0 \Rightarrow h=1$ (threshold is $\ge0$). Error $y-h=-1$. $\mathbf w \leftarrow (0,0,0) - (1,1,0) = (-1,-1,0)$. Now $\mathbf w\cdot\mathbf x=-2<0$, correctly output 0.

> [!question]- Q3. When is the perceptron learning rule guaranteed to converge?
> **Answer.** When the training data are linearly separable (perceptron convergence theorem). Otherwise it can oscillate; a learning rate decaying as $O(1/t)$ gives convergence to a minimum-error solution ([[russell-norvig-aima]] §19.6.4).

> [!question]- Q4. Why can't we train a perceptron with plain gradient descent on its 0/1 output?
> **Answer.** The threshold makes the output piecewise constant: the gradient is zero almost everywhere and undefined at $\mathbf w\cdot\mathbf x=0$ ([[russell-norvig-aima]] §19.6.4).

> [!question]- Q5. How does an SVM differ from a perceptron if both are linear classifiers?
> **Answer.** The perceptron stops at *any* separating hyperplane; the SVM chooses the one that **maximises the margin** between the classes ([[slides-01-introduction-to-ai]], slide 12), which tends to generalise better.
