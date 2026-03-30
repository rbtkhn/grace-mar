---
name: fact-check
preferred_activation: fact check
description: >-
  Triage-first fact check: fast web pass on operator-pasted claims with lean verdicts (supported / contradicted / unclear / out of scope),
  one solid cite per claim when possible, high abstention. Escalation flags when deeper audit is needed. Not Record merge unless gated.
---

# Fact check (operator)

**Preferred activation (operator):** say **`fact check`** (or **`verify this`**, **`check this claim`**).

**Default mode — triage (v1):** **fast pre-flight**, not a research memo. Prefer **one good source** + honest **Unclear** when the web is thin or noisy. **Upgrade later:** the skill can gain **standard** / **primary** depth passes if operator practice needs them — say **`fact check deep`** (or similar) when you add that tier.

Use when the operator wants a **quick external sanity check** on something **they paste or name** — a sentence, stat, quote attribution, URL summary, or draft line — before shipping, teaching, or archiving.

**Not a substitute for** [politics-massie](../politics-massie/SKILL.md) (breaking-news hooks + `@usa_first_ky` drafts). Use **fact check** for **neutral verification**; use **massie x** when the goal is **campaign-shaped** copy from today’s news.

## Lane

- Default **Think**: answer in the thread with **citations**; **no** repo edits, merge, stage, or gate writes unless the operator switches to **Ship** and names files.
- If the operator asks to **draft a gate candidate** or **edit a doc**, treat that as explicit **Ship** scope for that turn only.

## Procedure (triage)

1. **Isolate claims** — List **discrete** checkable statements (who / what / when / how many). Merge near-duplicates. If the prompt is vague, ask **one** narrowing question **or** state your assumption in one line — do not block on back-and-forth.
2. **Classify each claim**
   - **Factual** (empirically checkable).
   - **Interpretive** — label **interpretation**; do not score as Supported/Contradicted without marking it as inference.
   - **Out of scope** — prediction, pure opinion, privileged access — **Out of scope**; no fake certainty.
3. **Search and cite (light)** — One **credible** source per factual claim is enough for **triage** (reputable outlet, official page, or primary doc if it surfaces quickly). Add a **second** source **only** if the claim is **obviously contested**, **high-stakes** (election / legal / medical / financial / attribution of a quote), or the first source is weak/unclear.
4. **Verdict table (lean)** — For each **factual** claim:

   | Claim (short) | Verdict | Source (title + URL) |
   |---------------|---------|----------------------|
   | … | **Supported** / **Contradicted** / **Unclear** / **Out of scope** | … |

   One-line **caveat** under the table if dates, geography, or “developing story” matter.

5. **Interpretations** (if any) — **Three bullets max** — what is **speculation** vs what the cited material **actually says**.
6. **Confidence** — **One line** after the table: **low / medium / high** for triage purposes only, plus **one** phrase on what would raise it (e.g. “pull roll-call vote,” “original press release”).
7. **Escalation (required when applicable)** — If triage is **insufficient**, append a short **Escalate** block: **why** (stakes, conflict, no primary found) + **what a deeper pass would do** (e.g. two independent lines, pull primary PDF). Do **not** pretend triage was enough when it was not.

## Guardrails (Grace-Mar)

- **Knowledge boundary:** Assistant + web output is **not** [Record](../../../users/grace-mar/self.md) truth. Nothing here **enters** SELF, EVIDENCE, or `bot/prompt.py` without companion approval through **RECURSION-GATE** and `process_approved_candidates.py`. See [AGENTS.md](../../../AGENTS.md) and [knowledge-boundary-framework.md](../../../docs/knowledge-boundary-framework.md).
- **No leakage:** Do not present training-data “facts” as checks. Cite **what you found** and **where**.
- **Lexile / Voice:** If output is **for the Voice** or **child-facing**, stay within instance **Lexile** (grace-mar: **600L** unless raised with evidence) and **no** undocumented biographical claims.
- **Election / legal / medical / financial:** Default **Unclear** or **Escalate** unless a **strong** primary or two clear independents surfaced quickly — say when a **human professional** is the right next step.

## WORK lane

If the thread is clearly **WORK** and the operator did not say **no menu**, end with **3–5 labeled next-step options** (e.g. run a deeper pass later, tighten one sentence for posting, pivot to **massie x**, add a doc footnote under **Ship**). Otherwise skip the menu.

## Related

- [politics-massie](../politics-massie/SKILL.md) — news hooks + X drafts for the Massie analysis lane.
- **Massie news hooks:** If your Cursor install includes **massie-x-news-search-draft** (optional user skill), use it for **today’s** KY-4 / Massie-relevant cited briefs; **fact check** stays **claim-neutral**.
- [pros-and-cons](../pros-and-cons/SKILL.md) — tradeoffs when the question is **should we**, not **is it true**.
