# Automation Classification Template

**Use when:** Proposing a new automation, GitHub workflow change, scheduled job, or Cursor prompt. Complete one **copy** per **surface** (or use these field headings in a PR **description**). Cross-check the assigned **R0–R5** class against [automation-readiness-policy.md](automation-readiness-policy.md). **If** the proposal **ships**, add or update a row in [automation-readiness-ledger.md](automation-readiness-ledger.md).

---

## Fields

- **Surface name** — Short label (e.g. “Slack gate digest nudge”).
- **Surface type** — e.g. Cursor Automation, GitHub Action, local script, skill extension, scheduled cron.
- **Surface context** — **One of:** local/operator, GitHub CI, Cursor (or other agent host). “Unattended” differs by context; see [policy — Surfaces](automation-readiness-policy.md#surfaces-who-runs-what-unattended).
- **Owner / lane** — e.g. grace-mar instance, work-dev, default WORK.
- **Source files** — Repo paths to prompts, workflows, scripts, or skills.
- **Proposed trigger** — e.g. PR open, weekly schedule, manual, push to `main`.
- **Proposed tool authority (max R0–R5)** — Candidate class; see [readiness classes](automation-readiness-policy.md#readiness-classes-r0r5).
- **Reads** — What repo, API, or CI state is read.
- **Writes** — What files, issues, PR bodies, or branches are written (“none” is valid).
- **External side effects** — e.g. Slack post, email, Pages deploy, third-party API call.
- **Memory use** — Will the tool persist PR/issue/log text in product memory? (Default: no per [contract](cursor-safe-automation-contract.md) §10.)
- **Protected paths touched?** — Yes/no for `users/**/self.md`, `self-archive.md`, `recursion-gate.md` (as mutable content), `session-log.md`, `bot/prompt.py`, Record/EVIDENCE. If **yes**, default **R5** or **blocked** unless a documented policy carves a narrow exception.
- **Candidate class (R0–R5)** — Final class after review.
- **Why this class** — 2–4 sentences mapping behavior to the policy table.
- **Allowed unattended behavior** — What may run without a human in the loop per invocation (for that surface **context**).
- **Prohibited unattended behavior** — What must never run without explicit human or companion approval.
- **Required human decision** — What only the operator or companion decides.
- **Failure mode** — What goes wrong if the automation misfires (bad comment, wrong regen, false green).
- **Rollback / disable plan** — How to turn it off (Cursor UI, workflow disable, revert commit).

---

## Checklist (before filing)

- [ ] Does it touch Record / gate / prompt / session canonical paths?
- [ ] Does it approve, reject, merge, or stage candidates?
- [ ] Does it use untrusted PR/issue text as input for **writes**?
- [ ] Does it mutate generated or derived artifacts (regen, bundle, index)?
- [ ] Does it pretend to complete `coffee`, `dream`, `bridge`, or Steward / gate **review**?
- [ ] Can deterministic CI do this instead of an LLM layer?
- [ ] **Which surface?** (CI / Cursor / local) — see **Surface context** above.
- [ ] Is the smallest safe class R1 (read-only) or R2 (comment only)? If not, say why.

If any protected-path or merge question is **yes**, default **up** to **R5** (or **split** the design) until a human path is explicit.

---

## See also

- [automation-readiness-policy.md](automation-readiness-policy.md)
- [automation-readiness-ledger.md](automation-readiness-ledger.md)
- [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md)
