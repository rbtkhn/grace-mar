# Cursor CI failure triage (operator guide)

**Status:** **WORK** documentation. This page does **not** enable a [Cursor Automation](https://cursor.com/docs/cloud-agent/automations) in GitHub or in the repo. It describes how to configure one in Cursor and what it may do.

**Doctrine:** [AGENTS.md](../../AGENTS.md) · [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md). **No** Record edits, **no** gate processing, **no** merge authority.

---

## Purpose

A **CI failure triage** automation **comments** on failed runs with a short, human-readable interpretation: *what* failed, *where* to look first, and *suggested* local commands—when the logs support them. It **interprets**; it does **not** replace GitHub Actions and does **not** mutate the repository.

**Core line:** **GitHub Actions decide pass/fail; Cursor Automation explains the first useful place for the operator to look.**

**Related paste prompt (canonical procedure + identity):** [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md) — use that file as the **body** of the automation prompt in the Cursor product; this guide holds the **operator** setup, **taxonomy**, and the **output comment** template (single source of truth for the template).

**Maintenance:** Reconcile the failure **taxonomy** with [`.github/workflows/test.yml`](../../.github/workflows/test.yml) and sibling workflows (e.g. [governance.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/governance.yml), [lane-scope.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/lane-scope.yml)) when CI steps change. *Last reviewed against workflow layout: 2026-04.*

---

## Recommended trigger (Cursor product)

In [Cursor Automations](https://cursor.com/docs/cloud-agent/automations), the operator should prefer:

| Setting | Suggestion |
|---------|------------|
| **Event** | GitHub · workflow / check **completed** (or equivalent) |
| **Conclusion** | **Failure** only |
| **Context** | Prefer **PR-associated** runs (comment on the PR) over **push-to-`main`** with no PR |
| **Comment** | **One** triage comment per failed run, or **update** a prior automation comment if Cursor supports it—avoid spam on every push |

If there is **no** PR (e.g. failed push to `main`), do **not** require opening a new issue in v1 unless you **explicitly** add that later. Output to the **configured** destination (e.g. run summary) only.

---

## Allowed behavior

- Read the workflow **conclusion**, **failing job** names, and **log excerpts** available to the automation.
- Identify the **first likely** failure point (first **causal** step, not only the last error line).
- Name likely **script / file** paths that appear in the log.
- Suggest **at most two** exact **local** reproduction commands when visible (mirror `python` vs `python3` from the log).
- **Label uncertainty** when the log is incomplete.
- Cite the [output template](#output-comment-format) below for the **PR comment** body.

## Prohibited behavior

- No `git` **commits** or **pushes**; no file **edits** in the repo.
- No edits to `users/**/self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `bot/prompt.py`.
- No `process_approved_candidates.py` (any apply path).
- No approving, rejecting, renumbering, or staging **`CANDIDATE-*`** lines.
- No **mutating** shell commands in the environment (suggest only; operator runs locally).
- No **product memory** use for PR logs, private repo text, or untrusted issue bodies (see [contract](cursor-safe-automation-contract.md) § 10).
- No **ritual** language: do **not** call the output `coffee`, `dream`, `bridge`, **Steward**, or **gate** completion.

---

## Failure taxonomy (Grace‑Mar)

Use this table to **classify** failures after reading **which workflow** failed (`Tests`, `Governance`, `Lane scope`, `work-jiang`, `Harness`, `Naming check`, `Library index`, etc.). The **`Tests`** job in [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) chains many **named steps**; the **step name** in the log is the best key.

| Class | Signals | First place to inspect | Suggested local command (when class is known) |
| --- | --- | --- | --- |
| **Python / pytest** | `Run pytest` or `pytest` in log; test file path | Failing test file in traceback | `pytest path/to/test_file.py -v --tb=short` (from log) |
| **Integrity** | `Validate integrity`, `validate-integrity` | `manifest` / `grace-mar-llm` / runtime bundle drift in output | `python scripts/validate-integrity.py --user grace-mar --require-proposal-class` (matches CI; use `python3` if that is your local norm) |
| **Governance** | `governance_checker.py` (also in `Tests` and [Governance](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/governance.yml) workflow) | Rule name / path in script output | `python scripts/governance_checker.py` |
| **Gated Record PR** | [governance.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/governance.yml) job `gated-record-pr` | Commits in PR range touching Record paths; `[gated-merge]` / pipeline tokens | **Human:** inspect commit messages and paths—**do not** auto-fix via automation |
| **Lane scope** | [lane-scope.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/lane-scope.yml) | `PR_LANE` vs changed files per [lanes.yaml](https://github.com/rbtkhn/grace-mar/blob/main/lanes.yaml) | `python scripts/check_lane_scope.py --help` (then run the same invocation CI uses, from log) |
| **Strategy notebook** | `validate_strategy_pages`, `verify_ritter_refined_pages`, `validate_strategy_expert_threads`, `validate_expert_predictions`, `validate_knot_index`, `knot_seam_metrics` | Path in validator output / strategy-notebook file | Re-run the **exact** `python3 scripts/...` line from the failed **step** |
| **History notebook** | `validate_bookshelf_catalog`, `build_hn_* --check`, `hn_shelf_anchors` | Generated / check-mode artifacts under `history-notebook` paths from log | Re-run the **exact** `python3 scripts/...` line from the failed **step** |
| **Work-dev / workbench** | `validate_control_plane`, `preflight_workbench` | [docs/skill-work/work-dev/](../skill-work/work-dev/) and log paths | `python scripts/work_dev/validate_control_plane.py` or `python3 scripts/work_dev/preflight_workbench.py --skip-freshness` as appropriate |

**Other workflows:** [work-jiang.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/work-jiang.yml) (rebuild/validate), [harness.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/harness.yml) (Counterfactual Pack), [naming-check.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/naming-check.yml), [library-index.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/library-index.yml) — classify from **workflow name** and re-run the **failing** command from the log.

---

<a id="output-comment-format"></a>

## Output comment format (canonical template)

The automation’s **PR comment** (or other output) should follow this **markdown** shape. The paste prompt in [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md) references **this** section as the single template source.

```markdown
### CI triage

**Status:** failed
**Likely class:**
**Failing job / check:**
**First useful place to inspect:**
**Suggested local reproduction:** one or two shell lines from the failed CI step, or: *repro: unclear*
**Notes:** (optional) uncertain steps, or *see log step: …*
**Governance boundary:** This is a **triage** comment only. It did **not** approve, merge, edit Record files, or process the gate.
```

*Fill **Suggested local reproduction** with the exact `python` / `python3` / `pytest` line from the log when possible.*

---

## Operator setup

1. Read [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) and keep it at the top of the prompt (or link + short summary per that file).
2. Copy the full text of [prompts/cursor-ci-failure-triage.md](prompts/cursor-ci-failure-triage.md) into the [Cursor Automations](https://cursor.com/docs/cloud-agent/automations) prompt field (or maintain it as a single include).
3. Configure the **GitHub** trigger: workflow/check **completed** with **failure**; prefer **PR** context.
4. Enable **Comment on pull request** (or the closest equivalent) and **not** “open PR” / **not** push for this use case.
5. Do **not** turn on **Memories** for untrusted log content until a separate policy says otherwise.

**See also:** [README.md — First live automation: CI failure triage](README.md#first-live-automation-ci-failure-triage) · [cursor-automations.md](cursor-automations.md)
