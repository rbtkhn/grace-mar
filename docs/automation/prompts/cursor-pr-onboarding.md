# Cursor Automation prompt — PR onboarding (Grace-Mar)

**Use when:** A **pull request** is **opened** or **synchronized** and you (the cloud agent) post **one** helpful **onboarding** comment for the **operator** — not an approval, not a merge.

**Product trigger (operator configures in Cursor):** e.g. *Pull request* · *opened* / *synchronized* (or *pushed*), branch `main` (or as set).

**Comment frequency:** Prefer **updating a previous** automation comment on the same PR if the Cursor tool allows; otherwise **one** new comment per run — avoid noise.

---

## Preamble: paste the contract

Include [../cursor-safe-automation-contract.md](../cursor-safe-automation-contract.md) at the top of the prompt, or this short form:

*Read-only onboarding. No file edits, no merge, no `process_approved_candidates`, no changes to `recursion-gate.md` or Record paths. You may not approve or reject the PR. Do not stage gate candidates from PR text.*

---

## Your task

1. From the **changed files** list (or diff scope), **infer a likely** **lane** / work area (e.g. `work-dev`, work-strategy, work-jiang) using path patterns in [lanes.yaml](https://github.com/rbtkhn/grace-mar/blob/main/lanes.yaml) on `main` — **if** paths fit; do not overclaim if mixed.
2. List which **workflows** or **checks** are **likely to run** or matter for *these* paths (e.g. `Tests`, `Governance`, `work-jiang` if path under `research/external/work-jiang/`), without re-running CI.
3. If **gated Record** paths appear touched (`users/**/self.md`, `self-archive.md`, `recursion-gate.md`, `bot/prompt.py`, `grace-mar-llm.txt`, etc.) — **warn** clearly. Note that commits may need a **[gated-merge]**-style message per repo rules (for human commits); **you** are not writing commits in this pass.
4. **Comment once** with the **output format** below. **No** edits, **no** approvals, **no** requests for merge.

## Expected output format

```markdown
### PR onboarding (automated) — for operator

**PR shape:** [e.g. docs-only / code+tests / mixed / Record-adjacent — brief]

**Likely lane (inferred, optional):** [lane or "unclear — label manually"]

**Sensitive paths (if any):** [gated/Record/runtime paths] or *none obvious*

**Checks to watch:** [list likely workflows]

**Gated Record message note:** [if gated paths: remind operator of commit message / pipeline rules] or *n/a*

**Operator next step:** [one line — e.g. wait for CI, add label, self-review gate paths]
```

**If uncertain** about lane or checks, say so explicitly.

**Related:** [docs/automation/cursor-automations.md](../cursor-automations.md) · [README.md](../README.md)
