# Cursor Automation prompt — gate queue nudge (Grace-Mar)

**Priority:** **Medium** — not recommended as the **first** live automation. Use after CI triage (and optionally PR onboarding / integrity) are **trusted**.

**Use when:** A **weekly** nudge to surface **queue visibility** for the **recursion-gate** — **read-only**; no processing, no script runs that merge.

**Product trigger (operator configures in Cursor):** e.g. *Scheduled* (weekly).

---

## Preamble: paste the contract

Include [../cursor-safe-automation-contract.md](../cursor-safe-automation-contract.md) at the top. Emphasize: **read-only** `recursion-gate.md`; **no** `process_approved_candidates.py`; **no** candidate edits.

---

## Your task

1. **Read** `users/grace-mar/recursion-gate.md` in the working tree **only** (or the path the operator points to for this instance; default **grace-mar** user id).
2. **Count** visible **`CANDIDATE-*`** entries that appear to be in the **pending** / not-processed part of the file (follow the file’s `##` structure; if ambiguous, state **uncertain**).
3. **List** up to **10** candidate **ids** with **one-line summaries** only when those summaries **already appear in the file** next to the candidate. **Do not** invent or paraphrase into merge recommendations.
4. **Do not** approve, reject, renumber, or modify any line. **Do not** run `process_approved_candidates.py` (any flags). **Do not** add new candidates from the internet or from PRs.

5. Output for **operator** and **companion** attention only — a **reminder**, not a Steward decision.

## Expected output format

```markdown
### Gate queue nudge (automated) — for operator

**Queue count (approx.):** [n] *or* uncertain — [reason]

**Candidate ids (up to 10, from file only):** [CANDIDATE-... — pasted one-line from file, or "see file" if too long]

**Suggested human next step:** [e.g. open gate in editor, run weekly review, companion reviews top item — **no** script execution in this message]

**Hard boundary reminder:** This automation does **not** process, merge, or stage gate content. **Companion approval** required for any merge. Run `process_approved_candidates` only when **you** intend to, with approved ids.
```

**If** `recursion-gate.md` is missing or unreadable: one-line **abstain** and ask the operator to check path/permissions.

**Related:** [AGENTS.md](../../../AGENTS.md) · [docs/automation/cursor-automations.md](../cursor-automations.md) · [README.md](../README.md)
