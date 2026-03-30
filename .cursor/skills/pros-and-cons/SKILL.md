---
name: pros-and-cons
preferred_activation: unpack
description: >-
  When the operator does not understand a proposal—or asks for pros/cons, unpack, or tradeoffs—restate the idea in plain language, then structured pros, cons, disproportion, and a clear recommendation. Default Think lane; no repo edits unless they switch to ship.
---

# Pros and cons (unpack a proposal)

**Preferred activation (operator):** say **`unpack`** (or **`pros cons`**).

Use when:

- The operator says they **do not understand** something the assistant proposed, or
- They ask for **pros and cons**, **tradeoffs**, **unpack**, **why would we**, or **what are we giving up**.

Aligns with [.cursor/rules/operator-style.mdc](../../../.cursor/rules/operator-style.mdc) (lists, disproportion, hypothesis vs ship).

## Lane

- Default **Think**: explain and compare; **no** file edits, git, merge, or push unless the operator explicitly moves to implementation.
- If they only want clarification **without** a full pros/cons frame, give a short restatement first and offer the full structure.

## Output shape (in order)

1. **Restate the proposal** — One plain sentence: what would actually happen or change (scope boundary in one line: what is **in** / **out** if helpful).
2. **Pros** — Bulleted; concrete (what improves, for whom, when).
3. **Cons** — Bulleted; concrete (cost, risk, lock-in, maintenance, confusion).
4. **Disproportion** — One short paragraph: **which side weighs more** and **why** (the gap is often the insight).
5. **Recommendation** — One or two sentences: **do / defer / do differently**, without pretending the operator has already approved ship.
6. **Optional — What would change the call** — 1–3 triggers (e.g. “if we add a consumer for X, then…”).

## Do not

- Bury the restatement inside jargon the operator already flagged as unclear.
- Flatten into generic “it depends” without naming the main tradeoff.
- Jump to **EXECUTE** or edits while they are still orienting.

## WORK lane

If the thread is clearly **WORK** and the operator did not say **no menu**, end with **3–5 labeled next-step options** per operator-style (real forks, not “we’re done”). Otherwise skip the menu.

## Related

- [docs/start-here.md](../../../docs/start-here.md) — audience routing when proposals touch onboarding or seed formation.
- [extract-skill-from-session](../extract-skill-from-session/SKILL.md) — if this pattern needs a variant after repeated use.
