# work-cici and repo CI / labels

## PR labels (required on `main`)

**work-cici–only** changes (`docs/skill-work/work-cici/**`, including `work-dev-mirror/` and `work-politics-mirror/`) should use GitHub label **`lane/work-cici`**. See [.github/pull_request_template.md](../../../.github/pull_request_template.md).

If the PR also touches **parent lane** trees outside this folder (e.g. `docs/skill-work/work-dev/**` beyond the mirror, `docs/skill-work/work-politics/**` beyond the mirror), **`scripts/**`**, **`users/grace-mar/**`**, **`bot/**`**, or another lane’s canonical paths, add **`lane/cross`** and a non-empty **Cross-lane justification**.

## Gate shape (Record / Voice)

This lane holds **advisor and operator WORK** drafts — not Grace-Mar’s Record. Anything that should become **Grace-Mar** identity or Voice obligations must be staged in **`users/grace-mar/recursion-gate.md`** and merged only with companion approval via **`python3 scripts/process_approved_candidates.py`** per [AGENTS.md](../../../AGENTS.md).

The companion’s **cognitive-fork** **Record** (Cici’s instance) lives in **her** instance repository; durable identity changes there use **her** gate and merge script — not silent edits from grace-mar `work-cici` files.

There is no work-cici–specific gate paste CLI in this repo; use the standard staging tools if a milestone is explicitly gated.

## Summary

| Change | Label |
|--------|--------|
| Cici / **work-cici** advisor docs, mirrors, runbooks, BrewMind WORK files | `lane/work-cici` |
| Same + edits to canonical work-dev / work-politics / scripts / companion paths | `lane/cross` + justification |

## Drift guard

Run before merging lane copy that touches the **skill-work** hub row, `work-cici` **README** / **INDEX** / **LANES** / **LEAKAGE** active prose, or any change that could reintroduce “Xavier as the *current* lane identity”:

```bash
python3 scripts/check_work_cici_drift.py
```

- **Pass:** exit `0`.  
- **Fail:** exit `1`; messages on stderr as `path:line: ` plus a trimmed one-line preview.

Failing output flags disallowed *active* phrasing. **Allowlisted** on a per-line basis (if any of these substrings appear on the line, the line is not checked for fails): `formerly Xavier`, `legacy Xavier`, `Xavier-x01`, `work-xavier`, `users/xavier`, `xavier-` (e.g. legacy filename prefix), `TERMS-XAVIER`, `COMPANION-XAVIER`, `build_xavier_handbook_bundle.py`, `generate_smm_xavier_pdf.sh`, `xavier_journal_ob1_digest.py`. Fenced code blocks (triple backtick) in those files are skipped. See [scripts/check_work_cici_drift.py](../../../scripts/check_work_cici_drift.py) for the full **fail** substring set.
