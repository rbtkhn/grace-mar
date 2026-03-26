# META-class infrastructure proposals

**Purpose:** Stage **infrastructure** changes (scripts, configs, bot code) through the same [`recursion-gate.md`](../users/grace-mar/recursion-gate.md) queue with an explicit **`META_INFRA`** proposal class — **without** treating them like SELF/IX merges.

**Sovereignty:** The companion/operator still approves candidates. **No script auto-commits** to `main`. Patch application stays **human + git**.

**Related:** [`AGENTS.md`](../AGENTS.md) (gated merge, no direct Record edits), [`docs/perf-budgets.md`](perf-budgets.md), [`scripts/process_meta_candidates.py`](../scripts/process_meta_candidates.py).

---

## What META is not

- Not a substitute for normal **knowledge / curiosity / personality** candidates (`mind_category` + IX targets).
- Not auto-applied: [`process_approved_candidates.py`](../scripts/process_approved_candidates.py) records approval and moves the block to **Processed** but does **not** merge META into `self.md` / `self-evidence.md` / `prompt.py`.
- Not permission to bypass **pipeline merge** for Record files — META proposals must not target `users/*/self.md`, `self-evidence.md`, or PRP outputs as “diff targets.”

---

## YAML schema (inside the usual `### CANDIDATE-XXXX` + ` ```yaml ` block)

| Field | Required | Description |
|-------|----------|-------------|
| `proposal_class` | yes | Must be `META_INFRA` (exact). |
| `status` | yes | `pending` until review; then `approved` / `rejected`. |
| `summary` | yes | Short description for receipts and logs. |
| `meta_risk` | recommended | `LOW`, `MEDIUM`, or `HIGH`. |
| `meta_targets` | yes | Multiline block (` \| `) listing **repo-relative** paths (one per line) that the diff touches. |
| `meta_rationale` | recommended | Why this change is needed. |
| `meta_test_plan` | recommended | What to run (e.g. perf tiers, manual checks). |
| **Diff** | one of | `meta_diff:` (block scalar containing a **unified diff** text) **or** `meta_artifact_path:` pointing to a file under `users/<id>/artifacts/meta-diffs/` (e.g. `users/grace-mar/artifacts/meta-diffs/CANDIDATE-0090.patch`). |

Omit or set `profile_target` / IX-oriented fields to `none` where possible so META is not confused with SELF merges.

**Example (abbreviated):**

```yaml
proposal_class: META_INFRA
status: pending
summary: "Tighten retriever cache invalidation"
channel_key: operator:cursor
meta_risk: MEDIUM
meta_targets: |
  bot/retriever.py
meta_rationale: |
  Align disk cache invalidation with fingerprint changes.
meta_test_plan: |
  python3 scripts/run_perf_suite.py --tier 1 2 -u grace-mar --check-baseline
meta_artifact_path: users/grace-mar/artifacts/meta-diffs/CANDIDATE-0090.patch
```

---

## Path allowlist (validation)

`process_meta_candidates.py` only accepts targets (and paths inside the diff) under these **prefixes** (repo-relative):

- `scripts/`
- `config/`
- `bot/`
- `integrations/`
- `apps/` (optional app servers)

**Denied:** `users/` (except optional `users/<id>/artifacts/meta-diffs/*` as **artifact** paths), `docs/` (use operator PRs for doc-only if needed), root PRP `*.txt`, `.env`, etc.

---

## Operator workflow

1. **Author** a candidate with `proposal_class: META_INFRA`, targets, and diff (inline or artifact file).
2. **Validate (no writes):**  
   `python3 scripts/process_meta_candidates.py -u grace-mar`
3. **Write reports:**  
   `python3 scripts/process_meta_candidates.py -u grace-mar --write-report`
4. **Sandbox (optional):** copy tree, `git apply --check`, apply, run tier 1–2 perf + integrity:  
   `python3 scripts/process_meta_candidates.py -u grace-mar --sandbox`  
   (Slow; requires a clean diff and local resources.)
5. **Review** in gate-review-app / Telegram; approve when satisfied.
6. **Merge approval** via `process_approved_candidates.py --apply` — moves META block to Processed, logs pipeline/session; **does not** apply the patch.
7. **Apply patch manually:** `git apply users/<id>/artifacts/meta-patches/CANDIDATE-XXXX.patch` (or from artifact), then commit with a normal message (e.g. mention `[meta-infra]` for searchability).

---

## Merge pipeline behavior

On **`META_INFRA` + `approved`**, the merge script **skips** SELF/EVIDENCE/prompt updates for that candidate and still **moves** the block to **Processed**, emits a pipeline event, and updates session / **self-evidence § VIII** with a **META-INFRA** marker. See [`scripts/process_approved_candidates.py`](../scripts/process_approved_candidates.py).

---

## Rollback

Revert the git commit that applied the patch, or restore from git history. META reports under `users/<id>/artifacts/meta-reports/` are diagnostic only.
