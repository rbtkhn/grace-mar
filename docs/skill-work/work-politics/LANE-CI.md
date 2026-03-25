# work-politics and repo CI / gate shape

## PR labels (required on `main`)

**work-politics–only** doc or script changes should use GitHub label **`lane/work-politics`**. Same mechanics as other lanes: [.github/pull_request_template.md](../../../.github/pull_request_template.md).

If the PR touches **companion Record** paths (`users/**`, `bot/prompt.py`, …), **work-dev** integration paths, or another lane, add **`lane/cross`** and a non-empty **Cross-lane justification** in the PR body.

## Gate shape (canonical)

Merge queue tooling and `gate_block_parser` expect **`recursion-gate.md`** blocks in this shape:

- `### CANDIDATE-NNNN` (optional title line in parentheses)
- fenced ` ```yaml` / ` ``` ` body

**Territory:** every work-politics candidate needs **`territory: work-politics`** so `--territory work-politics` batch merge and operator reports stay correct.

**`channel_key`:** use the `operator:wap:…` convention (see [README § Gate convention](README.md)). Not informal “WAP” in prose — the **token** in YAML is still `operator:wap:`.

Full field reference: [wap-candidate-template.md](wap-candidate-template.md).

## Paste helpers

- **CLI:** `python scripts/emit_work_politics_gate_paste_snippet.py --help` — writes `users/<id>/recursion-gate-staging/work-politics-<date>.paste-snippet.md` with the next `CANDIDATE-*` id and required territory fields.
- **Manual:** follow [wap-candidate-template.md](wap-candidate-template.md) if you prefer hand-authored YAML.

## Optional JSON sidecars

Bot / handback staging emits **gitignored** `users/<id>/gate-staging/*.json` sidecars when candidates go through the **canonical staging path**. That is separate from editing `docs/skill-work/work-politics/**` only.

## Summary

| What you change | Label | Gate |
|-----------------|-------|------|
| This docs tree, `generate_work_politics_*`, WAP operator scripts | `lane/work-politics` | Only if you paste into `recursion-gate.md` for merge |
| Companion + politics in one PR | `lane/cross` + justification | `### CANDIDATE-*` + `territory: work-politics` |
