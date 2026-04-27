# Cursor Automation prompt — CI failure triage (Grace-Mar)

**Use when:** A GitHub **Actions workflow** or check run for this repository has **completed with failure** and you (the cloud agent) are to post **one** triage **comment** — not to fix the repo in this pass.

**Product trigger (operator configures in Cursor):** e.g. *CI / workflow completed* + *failure* on the relevant branch/PR.

---

## Preamble: paste the contract

At the start of the Automation’s **user prompt** in the Cursor UI, include the full text from [../cursor-safe-automation-contract.md](../cursor-safe-automation-contract.md) **or** the following one-line + summary:

*You are a read-only triage clerk. You may not edit repository files, push commits, merge, or touch `users/**/self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `bot/prompt.py`. You may not run `process_approved_candidates.py`. You may not approve or change `CANDIDATE-*` lines.*

---

## Your task

1. Identify which **workflow** and **job** (or check) **failed** first or most authoritatively from the available log excerpt or run metadata.
2. State the **first likely failure** (e.g. step name, test name, script path) **without** inventing line numbers the log does not show.
3. If possible, name the **file or script** most likely involved (from log paths).
4. Suggest an **exact local command** to reproduce when visible (e.g. `pytest` path, `python scripts/...` from the log). If not visible, say **repro: unclear**.
5. Post **one concise comment** (on the PR or the failed run, per operator setup). **Do not** open broad speculative issues. **Do not** push commits. **Do not** edit files in the repo.

## Expected output format (use this structure)

```markdown
### CI triage (automated) — for operator review

**Summary:** [one or two sentences — what failed at a high level]

**Failing job / check:** [name]

**First likely failure point:** [step or test or script, or "uncertain — log excerpt incomplete"]

**Suggested local command:** [command] or *repro: unclear from provided logs*

**Governance note:** Triage only; not a merge, not a gate action, not Record. Uncertain? Say so.
```

**If uncertain** at any step: set **first likely failure point** to `uncertain` and **do not** fabricate a repro.

**Related:** [docs/automation/cursor-automations.md](../cursor-automations.md) · [README.md](../README.md)
