# Tacit candidate types (v1)

**WORK / runtime only.** JSON emitted under `runtime/tacit/candidates/` is **not** canonical and **not** an approved `CANDIDATE-*` in `recursion-gate.md`.

## Types

| `candidate_type` | When generated (deterministic) |
|------------------|--------------------------------|
| `moonshot_insight_candidate` | `intended_destination` contains `moonshot`, or raw text contains `moonshot` (fallback). |
| `skill_candidate` | Destination contains `skill`. |
| `library_candidate` | Destination contains `library`. |
| `work_doctrine_candidate` | Destination contains `work`. |

At most **one** candidate per type per normalized tacit artifact (deduped).

## Non-goals (v1)

- No `self_mutation` or direct IX/SELF candidate types.
- No LLM generation; heuristics only (`scripts/tacit/generate_tacit_candidates.py`).
- No automatic append to [recursion-gate.md](../users/grace-mar/recursion-gate.md).

## Promotion

Use [`render_tacit_candidates_md.py`](../../scripts/tacit/render_tacit_candidates_md.py) for human-readable copy, then stage a proper gate block manually if the companion approves the promotion path.
