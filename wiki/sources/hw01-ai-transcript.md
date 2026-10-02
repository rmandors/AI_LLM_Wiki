---
type: source
summary: Transcript of Raymond's two AI-assistant exchanges for HW01 — Graphviz DOT syntax for drawing the 80-tile search tree, and a reading list of peer-reviewed sources for the chess-vs-Go research question.
unit: [3, 4]
tags: [hw01, ai-use, graphviz, references, transparency]
sources: ["[[hw01-ai-transcript]]"]
updated: 2026-10-01
---

# HW01 AI-assistant transcript

**Bibliographic line.** Portilla, R. *Chat Transcription* (AI assistant conversation, Markdown). File: `raw/HW_01/AI_transcript.md`.

**What it is.** The disclosure of AI use for HW01. Two questions: (1) how to render a portion of the search tree in Python; (2) trustworthy academic sources for the chess-vs-Go question. It also contains the **full statement of the 80-tile exercise** and of the **research question**, which are otherwise not in `raw/`.

## Key points

- **80-tile statement** (quoted by Raymond): 9×9 matrix, tiles 1–9 with surname A–I by quadrant; "Only quadrant I has an empty space, so tile 9H does not exist"; goal Fig. 02, quadrant order Fig. 03; achieve the shortest path exploring as few states as possible; show part of the tree, states generated, states analysed and path length → [[hw01-ex02-80-tile]].
- **Graphviz answer**: write a DOT `digraph` while walking the tree (nodes = boards, edges labelled Up/Down/Left/Right), stop at depth 2–3, optionally put `h=` in labels; render at edotor.net. The `write_dot` sketch with a recursive `walk` and `counter = [0]` is the template of `write_dot_walk` in `Exercise02.py` l.449–461.
- **Research statement** (chess vs Go): state of the art, most advanced algorithms, similarities, differences, complexity of each game, and whether BFS/DFS/minimax/alpha-beta can be used → [[chess-vs-go]].
- **Reading list**: Russell & Norvig; Knuth & Moore 1975 (alpha-beta analysis); Shannon 1950; Fraenkel & Lichtenstein 1981; Lichtenstein & Sipser 1980; Robson 1983; Allis 1994; Campbell et al. 2002 (Deep Blue); Silver et al. 2016/2017/2018 (AlphaGo, AlphaGo Zero, AlphaZero); Coulom 2006 and Kocsis & Szepesvári 2006 (MCTS/UCT); Wu 2019 (KataGo); Stockfish and Leela websites. Advice: cite DOI/peer-reviewed papers, date any "state of the art" claim → [[alpha-beta-pruning]], [[monte-carlo-tree-search]].

## Pages that use this source

[[hw01-ex02-80-tile]] · [[hw01-report]] · [[chess-vs-go]]

## Issues found

> [!warning] Contradiction
> The assistant lists "Russell & Norvig — Ch. 3 (BFS/DFS) and **Ch. 5 (minimax, alpha-beta, MCTS)**". In the **Global Edition** used in this course, Ch. 5 is CSPs and **Ch. 6 is games** ([[russell-norvig-aima]]). The report itself cites the right chapters.

- **9H vs 9I**: the quoted statement says 9H is missing while also saying only quadrant I has the hole; Raymond removed 9I ([[hw01-ex02-80-tile]]).
- Of the suggested references, the report cites only five (Russell & Norvig, Fraenkel & Lichtenstein, Lichtenstein & Sipser, Campbell et al., Silver et al. 2018) and adds one the assistant did not suggest (van den Herik et al., 2002, source of the $10^{46}$ / $10^{172}$ / $10^{123}$ / $10^{360}$ figures). Knuth & Moore, Robson, Allis, Coulom, Kocsis & Szepesvári are absent — Raymond should know which ones he actually opened.
- The transcript shows AI was used for DOT syntax and for finding sources; the modelling, code integration and analysis are Raymond's.
