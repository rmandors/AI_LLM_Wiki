---
type: source
summary: Raymond's Lab 01 written report (docx/pdf, 2 pages) — run_tests screenshot plus a three-part analysis of why sibling/2 needs X \= Y, which rules return duplicate answers, and what the closed-world assumption silently claims.
unit: [5, 6]
tags: [lab01, prolog, report, closed-world-assumption, student-work]
sources: ["[[slides-xx-logic-programming-prolog]]"]
updated: 2026-10-01
---

# Lab 01 report — Prolog family knowledge base

**Bibliographic line.** Raymond Portilla, *LAB #01*, Artificial Intelligence NRC 1651, USFQ, dated 08/09/2026. Raw files: `raw/Class_exercises/01_Code/Portilla_Raymond_lab01.docx` and `Portilla_Raymond_lab01.pdf` (same text, 2 pages), plus `Portilla_Raymond_lab01.zip` (submission bundle; not extracted). The code it describes is [[lab01-family-pl]].

**What it is.** The written half of the Lab 01 deliverable ([[slides-xx-logic-programming-prolog]], slides 29–30): the `run_tests` output and a half-page analysis answering the three questions of exercise 4 (20 pts).

## Key points

**Tests output.** The section heading is present, but the content is an image (a screenshot) and has no text in the extraction. Re-running the code here gives `% All 20 tests passed` (SWI-Prolog, `run_tests` with `format(log)`). See [[lab01-family-pl]].

**1) Why `sibling/2` needs `X \= Y`** (page 1).
- Without it, `father(F, X), father(F, Y)` succeeds with `X = Y = ana`, so everyone with a father is their own sibling. "A person always shares a parent with themselves."
- With `X \= Y`, ana's siblings are luis and rosa, not ana. This is the reason for the required negative test `sibling(X, X)` failing.
- Matches the FOL definition $Sibling(x,y) \Leftrightarrow x \neq y \wedge \exists p\,Parent(p,x) \wedge Parent(p,y)$ ([[russell-norvig-aima]] §8.3.2) and §8.2.7's point that two existential variables may name the same object.

**2) Same answer twice** (pages 1–2).
- The slide-12 `sibling/2` (one shared parent `P`) answers `sibling(ana, luis)` twice, once through hector and once through carmen.
- Raymond's version requires the same father **and** the same mother, so each pair comes out once. `sister/2` and `brother/2` inherit that.
- `uncle/2` and `aunt/2` *could* repeat (they start from `parent(P, Child)`), but in this tree only one parent is the uncle's or aunt's sibling, so `uncle(luis, sofia)` comes out once.
- `related/2` repeats: `related(ana, hector)` comes back four times, one per path. That is why several tests use `once/1`.
- `cousin/2` could repeat but `cousin(sofia, diego)` comes out once.

**3) Closed-world assumption** (page 2).
- Never written: rosa has no children, diego has none, there is no `stranger`, hector is not a mother. Prolog still answers "no" because none of these can be proved.
- "If it is not in the knowledge base, it did not happen." Only the 16 people in `male/1` and `female/1` exist.
- Negative tests rely on this: `parent(rosa, _)` failing is read as "rosa has no kids", with no `childless/1` fact.
- "If a person was missing from the file, Prolog would not say unknown. It would just say no."

## Verification (re-run on 2026-10-01, SWI-Prolog)

| Claim in report | Re-run result |
|---|---|
| All tests pass | 20/20 passed |
| `sibling(ana, luis)` once | 1 solution |
| `related(ana, hector)` four times | 4 solutions |
| `uncle(luis, sofia)` once | 1 (all uncle pairs are distinct) |
| `cousin(sofia, diego)` once | 1 |

All numeric claims check out.

## Pages that use this source

[[lab01-family-pl]] · [[negation-as-failure]] · [[prolog]] · [[backward-chaining]] · [[first-order-logic]] · [[unit-06-logic-prolog-review]]

## Issues found

- **Tests output is image-only.** The extraction has nothing under "Tests Output". The 20/20 result is taken from re-running the `.pl` file, not from the report.
- **Missing consequence of the sibling design.** The report presents "same father AND same mother" only as a fix for duplicate answers. It does not mention that it also **excludes half-siblings**, and anyone with a missing parent fact can never have a sibling (e.g. the married-in spouses pedro, maria, juan, andres, elena). That is a semantic change, not just a deduplication ([[lab01-family-pl]]).
- **Scale of `related/2` duplication is understated.** "Four times" is true for `related(ana, hector)`. `related(hector, Y)` returns **229** answers for 16 distinct people, and `related(juan, Y)` returns 334 (re-run). Proving the negative `related(hector, stranger)` explores every simple path (2,571 inferences).
- **CWA answer stops at the CWA.** It could also name the other two database-semantics assumptions: unique names (hector ≠ carmen is never written) and domain closure ([[russell-norvig-aima]] §9.4.4; [[luger-ai-6e]] §14.3.2). See [[negation-as-failure]].
- **Date format**: "08/09/2026" is presumably 8 September 2026 (dd/mm), consistent with the file timestamps (general knowledge about local convention).
