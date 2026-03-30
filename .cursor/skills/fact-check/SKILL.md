---
name: fact-check
preferred_activation: fact check
description: >-
  Verify operator-supplied claims, quotes, draft posts, or brief bullets using web lookup and clear sourcing.
  Verdicts per claim (supported / contradicted / unclear / out of scope); explicit limits and confidence.
  Read-only vs Record: does not merge into SELF or EVIDENCE unless the operator runs the gated pipeline.
---

# Fact check (operator)

**Preferred activation (operator):** say **`fact check`** (or **`verify this`**, **`check this claim`**).

Use when the operator wants **external grounding** for something **they paste or name** — a sentence, stat, quote attribution, URL summary, or draft social line — before shipping, teaching, or archiving.

**Not a substitute for** [politics-massie](../politics-massie/SKILL.md) (breaking-news hooks + `@usa_first_ky` drafts). Use **fact check** for **neutral verification**; use **massie x** when the goal is **campaign-shaped** copy from today’s news.

## Lane

- Default **Think**: answer in the thread with **citations**; **no** repo edits, merge, stage, or gate writes unless the operator switches to **Ship** and names files.
- If the operator asks to **draft a gate candidate** or **edit a doc**, treat that as explicit **Ship** scope for that turn only.

## Procedure

1. **Isolate claims** — List **discrete** checkable statements (who / what / when / how many). Merge near-duplicates. If the prompt is vague, ask **one** narrowing question or state what you will assume.
2. **Classify each claim**
   - **Factual** (empirically checkable: dates, votes, quotes, numbers, “did X say Y”).
   - **Interpretive** (framing, motive, “this means”) — label as **interpretation**; separate from factual checks.
   - **Out of scope** — prediction, pure opinion, or would need privileged access — say so and **do not** fake certainty.
3. **Search and cite** — Use current web sources (official primary where possible: government sites, court dockets, full transcripts, reputable newsrooms). Prefer **2+ independent** corroborations for **strong** factual verdicts when the claim is contested or high-stakes.
4. **Verdict table** — For each **factual** claim, one row:

   | Claim (short) | Verdict | Sources (title + URL) | Caveat / date sensitivity |
   |---------------|---------|------------------------|----------------------------|
   | … | **Supported** / **Contradicted** / **Unclear** / **Out of scope** | … | … |

5. **Interpretations** (if any) — Short paragraph: what the Record **does** vs **does not** justify; flag **speculation**; do not present inference as **Supported** without labeling it.
6. **Confidence** — One line: **high / medium / low** and **what would raise it** (e.g. primary document, newer poll, named dataset).
7. **Abstention** — If search is thin or conflicting, say **Unclear** and **what to look up next** (do you want me to look it up?).

## Guardrails (Grace-Mar)

- **Knowledge boundary:** Assistant + web output is **not** [Record](../../../users/grace-mar/self.md) truth. Nothing here **enters** SELF, EVIDENCE, or `bot/prompt.py` without companion approval through **RECURSION-GATE** and `process_approved_candidates.py`. See [AGENTS.md](../../../AGENTS.md) and [knowledge-boundary-framework.md](../../../docs/knowledge-boundary-framework.md).
- **No leakage:** Do not **merge** training-data “facts” as if the companion said them. Cite **what you found** and **where**.
- **Lexile / Voice:** If the operator says output is **for the Voice** or a **child-facing** channel, keep language within the instance **Lexile** ceiling (grace-mar: **600L** unless raised with evidence) and **no** undocumented biographical claims.
- **Election / legal / medical / financial:** Extra care — prefer **primary** sources; say when the claim needs a **human professional** (not an LLM pass).

## WORK lane

If the thread is clearly **WORK** and the operator did not say **no menu**, end with **3–5 labeled next-step options** (e.g. deeper primary pass, turn into brief bullet, draft gate stub for companion-approved Record update, pivot to **massie x**, file a doc footnote). Otherwise skip the menu.

## Related

- [politics-massie](../politics-massie/SKILL.md) — news hooks + X drafts for the Massie analysis lane.
- **Massie news hooks:** If your Cursor install includes **massie-x-news-search-draft** (optional user skill), use it for **today’s** KY-4 / Massie-relevant cited briefs; **fact check** stays **claim-neutral**.
- [pros-and-cons](../pros-and-cons/SKILL.md) — tradeoffs when the question is **should we**, not **is it true**.
