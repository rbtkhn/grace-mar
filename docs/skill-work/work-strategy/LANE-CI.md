# work-strategy and repo CI / gate shape

## PR labels (required on `main`)

**work-strategy–only** changes (`docs/skill-work/work-strategy/**`, strategy prototype path below) should use GitHub label **`lane/work-strategy`**. See [.github/pull_request_template.md](../../../.github/pull_request_template.md).

If the PR also touches **work-politics** scripts (e.g. `generate_work_politics_daily_brief.py`), **companion** paths, **work-dev**, or another lane, add **`lane/cross`** and a non-empty **Cross-lane justification**.

## Gate shape (when you paste into `recursion-gate.md`)

Machine parsing uses the same **`### CANDIDATE-*` + fenced YAML** contract as elsewhere ([`scripts/gate_block_parser.py`](../../../scripts/gate_block_parser.py)).

**Historically in this repo**, work-strategy milestones that still use the **work-politics territory bucket** (for `--territory work-politics` / WAP reporting) were staged with:

- **`territory: work-politics`**
- **`channel_key: operator:work-strategy`**

That matches existing gate rows that bundle strategy modules under the politics territory for batch tooling. If you intentionally want a **companion-only** row (no WAP bucket), use **`territory: companion`** and an appropriate `channel_key` (e.g. `operator:cursor:…`) per your operator convention — see [`stage_gate_candidate.py`](../../../scripts/stage_gate_candidate.py).

Full WAP field patterns: [work-politics wap-candidate-template.md](../work-politics/wap-candidate-template.md).

## Paste helper CLI

```bash
python scripts/emit_work_strategy_gate_paste_snippet.py --help
```

Writes `users/<user>/recursion-gate-staging/work-strategy-<date>.paste-snippet.md` with the next `CANDIDATE-*` id, default **`territory: work-politics`** + **`channel_key: operator:work-strategy`**. Override with `--territory` / `--channel-key` if your merge plan differs.

## Prototype

[research/prototypes/mind-synthesis.py](../../../research/prototypes/mind-synthesis.py) — linked from [synthesis-engine.md](synthesis-engine.md); owned under **work-strategy** lane for scope checks.

## Summary

| Change | Label | Typical gate row |
|--------|-------|------------------|
| Strategy docs / modules / brief config | `lane/work-strategy` | optional; if pasted: `territory: work-politics` + `operator:work-strategy` |
| Strategy + politics script edits | `lane/cross` + justification | align with companion |
