# Cursor Automations — prompt pack (Grace-Mar)

This folder holds **operator-facing** prompt templates and policy for [Cursor Automations](https://cursor.com/docs/cloud-agent/automations). **These files are not live automations.** Enabling a cloud agent in the Cursor product is a separate step; this repo only documents **how** to do it safely.

## Core principle

**Automate visibility, not authority.**

Cursor Automations are allowed to **reduce operator attention cost**. They are **not** allowed to acquire operator authority (merge, approve, stage gate content, or edit the Record outside the human-gated path).

A useful distinction:

- **GitHub Actions and local scripts** answer: *did the deterministic check pass?*
- **Cursor Automations** (when you enable them) answer: *what does the failed check probably mean, and what should the operator inspect first?*

That keeps Automations from becoming a second CI system. Deterministic checks stay owned by [`.github/workflows/`](../../.github/workflows/) and the scripts they invoke.

## Doctrine and boundaries

- [AGENTS.md](../../AGENTS.md) — agents may **stage**; they may **not** merge without companion approval; routing vs accountability.
- [docs/runtime-vs-record.md](../runtime-vs-record.md) — what is operator/runtime scaffolding vs Record-adjacent.
- [users/grace-mar/instance-doctrine.md](../../users/grace-mar/instance-doctrine.md) — modes, file update protocol, merge via `process_approved_candidates.py` only when the operator runs it.

## What’s in this folder

| File | Role |
|------|------|
| [cursor-automations.md](cursor-automations.md) | Design note: fit, trigger map, non-goals. |
| [cursor-ci-failure-triage.md](cursor-ci-failure-triage.md) | **Operator guide** for the first live automation: triggers, allow/deny, failure taxonomy, **canonical comment template**. |
| [cursor-pr-onboarding.md](cursor-pr-onboarding.md) | **Operator guide** for PR onboarding: triggers, lane/sensitive heuristics, **canonical PR comment template**. |
| [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) | **Paste** at the top of any Automation prompt. |
| [prompts/](prompts/) | **Paste-ready** prompts per use case. |

## Intended automation classes (prompts, not running jobs)

| Class | Prompt | Typical trigger (when you enable it) |
|-------|--------|--------------------------------------|
| 1. CI failure triage | [cursor-ci-failure-triage.md](cursor-ci-failure-triage.md) (guide) + [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md) (paste) | Workflow completed with failure |
| 2. PR onboarding | [cursor-pr-onboarding.md](cursor-pr-onboarding.md) (guide) + [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md) (paste) | PR opened, synchronized, or reopened |
| 3. Integrity summary | [prompts/cursor-integrity-summary.md](prompts/cursor-integrity-summary.md) | Weekly schedule (or manual) |
| 4. Gate queue nudge | [prompts/cursor-gate-queue-nudge.md](prompts/cursor-gate-queue-nudge.md) | Weekly schedule — **medium priority**; not recommended as first live automation |

**Rituals unchanged:** `coffee`, `dream`, `bridge`, **Steward / gate review**, and **companion approval** for merges remain **human/operator** responsibilities. Automations may **remind** or **summarize**; they do **not** complete those rituals.

## Prior work

A broader opportunity probe (friction list, CI inventory) lives in [docs/skill-work/work-dev/cursor-automations-candidates.md](../skill-work/work-dev/cursor-automations-candidates.md). **Prompts SSOT** for paste-ready text is this `docs/automation/` tree.

<a id="first-live-automation-ci-failure-triage"></a>

## First live automation: CI failure triage

**Recommended first** because it is **event-bounded** (runs only after a failure), **read-only** (comments / report text, not commits), and **complements** existing GitHub Actions without duplicating pass/fail logic.

1. **Operator guide** (setup, taxonomy, **canonical** PR comment template): [cursor-ci-failure-triage.md](cursor-ci-failure-triage.md)
2. **Paste prompt** (bounded identity + procedure; references the guide’s template): [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md)
3. **Design context:** [cursor-automations.md § Recommended first live automation](cursor-automations.md#recommended-first-live-automation)

**This does not** enable an automation in GitHub or in the repo; it documents how to configure one in the Cursor product.

<a id="pr-onboarding-comment"></a>

## PR onboarding comment

**Recommended second** live automation (after [CI failure triage](#first-live-automation-ci-failure-triage)). It **reduces PR cognitive load** by summarizing **shape**, **likely lane**, **sensitive** paths, and **checks to watch** before the operator **reads the full diff** or waits on **all** **green** checks — a **narration** layer only; it does **not** replace [lane-pr-hint](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/lane-pr-hint.yml) or [lane-scope](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/lane-scope.yml) **enforcement**.

1. **Operator guide** (triggers, allow/deny, **canonical** PR comment **template**): [cursor-pr-onboarding.md](cursor-pr-onboarding.md)
2. **Paste prompt** (identity + procedure; **exact** [template](cursor-pr-onboarding.md#output-comment-format) by reference): [prompts/cursor-pr-onboarding.md](prompts/cursor-pr-onboarding.md)
3. **Design context:** [trigger map](cursor-automations.md#trigger-map) in [cursor-automations.md](cursor-automations.md)

**This does not** enable an automation; it documents Cursor **product** configuration. **No** **labels**, **merges**, or **auto**-**fixes** from the bot.
