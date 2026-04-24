# Letta runtime complement adapter

## Status

Optional, file-based, **runtime-only**, **non-canonical**. This is not a live Letta integration. No network calls, no required vendor SDK, and no Mem0 in this path.

## Purpose

**Prepare** [runtime export bundles](../../../runtime/runtime-complements/exports/) for a Letta-style (or similar) stateful agent runtime.

**Import** session summaries into Grace-Mar [runtime-complement inbox](../../../runtime/runtime-complements/inbox/) via [import_runtime_observation.py](../../../scripts/runtime/import_runtime_observation.py) (e.g. through [letta_import_summary.py](../../../scripts/runtime/letta_import_summary.py)).

## Boundary rule

> Letta may remember inside Letta.  
> Grace-Mar remembers only through the **gate** ([`recursion-gate.md`](../../../users/grace-mar/recursion-gate.md) and companion-approved merge; see [AGENTS.md](../../../AGENTS.md)).

## Suggested memory block labels (Letta-local)

- `grace_mar_boundary`
- `grace_mar_context`
- `operator_instructions`
- `runtime_session_notes`

These are **not** Record surfaces. Do not treat them as SELF, EVIDENCE, SKILLS, or SELF-LIBRARY.

**Promotion (short):** Letta summary → **inbox** + **receipt** → **human review** → optional **recursion-gate** → normal approved merge.

Full contract: [LETTA-ADAPTER-CONTRACT](LETTA-ADAPTER-CONTRACT.md).

## What this does

- Read a bundle from [export_runtime_context.py](../../../scripts/runtime/export_runtime_context.py).
- Build a `letta_seed_context` file with [letta_prepare_seed.py](../../../scripts/runtime/letta_prepare_seed.py).
- Import an example (or your file) with [letta_import_summary.py](../../../scripts/runtime/letta_import_summary.py).

## What this does not do

- No Letta API calls, no required Letta SDK, no agent lifecycle in-repo.
- No Mem0, no Docker, no canonical Record writes (only inbox + receipt per import script).

## Usage

From the repo root:

```bash
python3 scripts/runtime/export_runtime_context.py \
  --name letta-demo \
  --include-doc docs/runtime/runtime-complements.md \
  --include-doc docs/runtime-vs-record.md

python3 scripts/runtime/letta_prepare_seed.py \
  --bundle <printed-bundle-path> \
  --out runtime/runtime-complements/exports/letta-seed-demo.json
```

`export_runtime_context.py` prints the bundle path. Use that value in place of `<printed-bundle-path>`.

```bash
python3 scripts/runtime/letta_import_summary.py \
  --input bridges/runtime-complements/letta/letta-session-summary.example.json
```

A bare `python3 scripts/runtime/letta_import_summary.py` uses the same example by default.

## See also

- [runtime complements (membrane)](../../../docs/runtime/runtime-complements.md)
- [LETTA-ADAPTER-CONTRACT](LETTA-ADAPTER-CONTRACT.md)
- [letta-seed.example.json](letta-seed.example.json) · [letta-session-summary.example.json](letta-session-summary.example.json)
