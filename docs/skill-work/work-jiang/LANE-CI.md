# work-jiang and repo CI / gate shape

## PR labels (required on `main`)

Work-jiang-only changes should carry GitHub label **`lane/work-jiang`**. Same mechanics as other lanes: see [.github/pull_request_template.md](../../../.github/pull_request_template.md).

If a PR touches **both** this lane and companion Record paths (e.g. `users/**`, `bot/prompt.py`) or work-dev integration paths, add **`lane/cross`** and a non-empty **Cross-lane justification** in the PR body.

## What “strict gate parsing” applies to

These tools assume **markdown blocks** in `recursion-gate.md` of the form:

- `### CANDIDATE-NNNN`
- followed by a fenced ` ```yaml` / ` ``` ` block

See [`scripts/gate_block_parser.py`](../../../scripts/gate_block_parser.py) (shared with dashboards and review).

**work-jiang research** under `research/external/work-jiang/` does **not** need that shape. It becomes relevant when you **paste into** the companion gate for merge.

## Draft files vs canonical gate blocks

`scripts/work_jiang/run_comparative_sweep.py` still writes a small **`blocks:` YAML** draft for operator notes. That format is **not** what the bot or `gate_block_parser` consumes. Prefer the **`.paste-snippet.md`** file emitted next to it: same sweep run produces a ready-to-edit `### CANDIDATE-*` block aligned with merge tooling.

## Optional JSON sidecars

`users/<id>/gate-staging/*.json` sidecars are produced when the **bot / handback** stages with the canonical shape. They are **gitignored** and are not emitted by work-jiang transcript tooling unless you stage through that path.

## Summary

| Surface | Label | Gate shape |
|--------|-------|------------|
| Transcripts, analysis JSON, claims | `lane/work-jiang` | N/A |
| Paste into companion merge queue | usually `lane/companion-record` or cross-lane | `### CANDIDATE-*` + yaml fence |
