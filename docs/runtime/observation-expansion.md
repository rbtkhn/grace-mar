# Runtime observation expansion and prepared context

## Invocation contract

**Surface type:** workflow  
**Primary purpose:** expand explicit observation IDs to bounded payloads and optionally assemble a lane-scoped prepared-context Markdown file  
**When to use:** after search/timeline have narrowed a small set of observations worth full detail or a shareable bundle  
**Inputs:** repeated `--id` (observation ids), optional `--markdown` / `--json`; for prepared context: `--lane`, `--id`, `--output` path  
**Outputs:** JSON or Markdown expansion (stdout or file); optional prepared-context artifact under `prepared-context/` (or path you choose)  
**Mutation scope:** runtime-only  
**Canonical Record access:** none  
**Typical next step:** optional `stage_candidate_from_observations.py` if proposing a durable change; otherwise re-open normative retrieval flow  
**Do not use for:** implicit search across the ledger (use `lane_search` first) or treating prepared context as approved Record truth  

**Supplements** [memory-retrieval.md](memory-retrieval.md) (normative stack and rules). This file covers **expansion and prepared-context commands** only.

Grace-Mar follows a **progressive disclosure** workflow aligned with compact index → timeline → **full expansion** → optional **prepared-context bundle**:

1. `lane_search` / `lane_timeline` — filter before heavy reads ([memory-retrieval.md](memory-retrieval.md)).
2. **`expand_observations`** — explicit IDs only; bounded fields (no implicit search). Read-only; does not mutate the ledger.
3. **`build_context_from_observations`** — turns a small expanded set into an inspectable Markdown block for agents or the next operator step. **Runtime-only**; not canonical Record truth.

## Commands

```bash
# Full bounded payload per ID (JSON array or Markdown)
python3 scripts/runtime/expand_observations.py \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --id obs_20260413T191455Z_e5f6g7h8

python3 scripts/runtime/expand_observations.py \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --markdown \
  -o runtime/observations/expanded/latest.md

# Prepared-context artifact (lane required unless --mixed-lane; max 8 IDs by default)
python3 scripts/prepared_context/build_context_from_observations.py \
  --lane work-strategy \
  --id obs_20260413T184210Z_a1b2c3d4 \
  --id obs_20260413T191455Z_e5f6g7h8 \
  -o prepared-context/runtime-observation-context.md
```

## Governance

- Expansion and prepared-context files **do not** update SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or `recursion-gate.md`.
- Grace-Mar **does not** auto-inject this material into future sessions as “truth”; operators choose when to paste or commit artifacts.
- Optional: `GRACE_MAR_RUNTIME_LEDGER_ROOT` isolates the ledger path in tests or sandboxes.

## See also

- [prepared-context/README.md](../../prepared-context/README.md)
- [progressive-disclosure.md](../prepared-context/progressive-disclosure.md)
