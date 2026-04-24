# work-cici and repo CI / labels

## PR labels (required on `main`)

**work-cici–only** changes (`docs/skill-work/work-cici/**`, including `work-dev-mirror/` and `work-politics-mirror/`) should use GitHub label **`lane/work-cici`**. See [.github/pull_request_template.md](../../../.github/pull_request_template.md).

If the PR also touches **parent lane** trees outside this folder (e.g. `docs/skill-work/work-dev/**` beyond the mirror, `docs/skill-work/work-politics/**` beyond the mirror), **`scripts/**`**, **`users/grace-mar/**`**, **`bot/**`**, or another lane’s canonical paths, add **`lane/cross`** and a non-empty **Cross-lane justification**.

## Gate shape (Record / Voice)

This lane holds **advisor and operator WORK** drafts — not Grace-Mar’s Record. Anything that should become **Grace-Mar** identity or Voice obligations must be staged in **`users/grace-mar/recursion-gate.md`** and merged only with companion approval via **`python3 scripts/process_approved_candidates.py`** per [AGENTS.md](../../../AGENTS.md).

Xavier’s **cognitive fork** lives in **her instance repo**; durable identity changes there use **her** gate and merge script — not silent edits from grace-mar `work-cici` files.

There is no work-cici–specific gate paste CLI in this repo; use the standard staging tools if a milestone is explicitly gated.

## Summary

| Change | Label |
|--------|--------|
| Xavier advisor docs, mirrors, runbooks, BrewMind WORK files | `lane/work-cici` |
| Same + edits to canonical work-dev / work-politics / scripts / companion paths | `lane/cross` + justification |
