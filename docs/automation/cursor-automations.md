# Cursor Automations in Grace-Mar — design note

**Status:** Policy and prompts only. **Not** a claim that any Automation is enabled in this repo or in Cursor. **WORK** documentation; not Record.

## Purpose

Define how [Cursor Automations](https://cursor.com/docs/cloud-agent/automations) may be used with this repository **without** breaching the authority model: companion-owned Record, human gate, merge only via the approved path described in [AGENTS.md](../../AGENTS.md) and [instance-doctrine.md](../../users/grace-mar/instance-doctrine.md).

**Headline:** Cursor Automations are allowed to **reduce operator attention cost**. They are **not** allowed to **acquire** operator authority.

**Operating distinction:**

| Layer | Question it answers |
|-------|----------------------|
| **GitHub Actions** (and the scripts they run) | **Did** the deterministic check pass? |
| **Cursor Automations** (optional, LLM-shaped) | **What** does the failed output **probably** mean, and **where** should the operator look **first**? |

## What Cursor Automations may do

- **Read** public repo state (in the Automation’s checked-out context): workflows, logs, file paths, `recursion-gate.md` for visibility (not mutation).
- **Summarize, triage, comment** (e.g. one PR comment) in plain language; **suggest** local commands to reproduce or fix, when deducible from logs.
- **Label** their output as report, triage, or comment — not as `coffee` completion, not as dream, not as gate decision.

## What Cursor Automations may not do

- **Direct edits** to Record, **EVIDENCE**, `recursion-gate.md` (as gate content), `session-log.md`, or `bot/prompt.py` — same prohibition as in [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md).
- **Unattended** `process_approved_candidates.py --apply`, or any merge into profile/Record.
- **Approve, reject,** or **re-stage** `CANDIDATE-*` lines from **untrusted** text (e.g. PR body only).
- **Substitute** for **coffee**, **dream**, **bridge**, **Steward**, or **companion** gate approval.
- **Redefine** CI: deterministic pass/fail remains **Actions**; Automations are not a second test runner.

## Recommended first live automation

**CI failure triage comment** — on **GitHub: workflow / CI completed** with **failure** (or equivalent trigger).

- **Why first:** Tight event, one comment, no file writes, clear value (first failing job + repro hint), low governance surface if the prompt includes the [safe contract](cursor-safe-automation-contract.md).
- **How:** [README — First live automation: CI failure triage](README.md#first-live-automation-ci-failure-triage) · operator guide [cursor-ci-failure-triage.md](cursor-ci-failure-triage.md) · paste prompt [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md).

## Trigger map

| Event (product / operator choice) | Intended prompt | Output channel |
|-----------------------------------|-----------------|----------------|
| **CI / workflow completed + failure** | [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md) | PR or workflow comment (as configured) |
| **PR opened** or **synchronized** | [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md) | Single PR comment (update in place if the tool allows) |
| **Weekly schedule** (or manual) | [prompts/cursor-integrity-summary.md](prompts/cursor-integrity-summary.md) | Report / Slack / issue **text only** — no commit of regen |
| **Weekly schedule** | [prompts/cursor-gate-queue-nudge.md](prompts/cursor-gate-queue-nudge.md) | Nudge only — **medium priority**; read-only `recursion-gate.md` |

**Human rituals:** **coffee** (cadence), **dream** (maintenance consolidation), **bridge** (session handoff), and **Steward / gate** (approval, `process_approved_candidates` when the **operator** runs it) are **not** replaced by this schedule table.

## Non-goals

- Enabling or configuring Automations in the Cursor product from this repo (this doc does not touch Cursor settings).
- New GitHub Actions workflows, new scheduled jobs in-repo, or scripts that **mutate** the repo for Automations in this **prompt-pack** change set.
- Using Automations to **open** or **edit** `users/**/self.md`, EVIDENCE, or gate as part of the automation run.
- **Memory** tools on untrusted PR/issue content (see contract § 10) unless a **later**, explicit policy allows it.

## Related

- [README.md](README.md) — index and principle.
- [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) — paste into every prompt.
- [docs/skill-work/work-dev/cursor-automations-candidates.md](../skill-work/work-dev/cursor-automations-candidates.md) — prior friction/CI survey.
