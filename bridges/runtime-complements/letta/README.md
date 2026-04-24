# Letta runtime complement adapter

## Status

Optional, file-based, **runtime-only**, **non-canonical**. Not a live Letta
integration. No Letta API calls and no required Letta SDK.

## Purpose

This adapter **prepares** Grace-Mar
[runtime export bundles](../../../runtime/runtime-complements/exports/) for
use in a **Letta-style** (or similar) stateful agent runtime.

It **imports** Letta session summaries back into Grace-Mar's **runtime
complement** [inbox](../../../runtime/runtime-complements/inbox/) through the
[import script](../../../scripts/runtime/import_runtime_observation.py).

## Boundary rule

> Letta may remember inside Letta.  
> Grace-Mar remembers only through the **gate** ([`recursion-gate.md`](../../../users/grace-mar/recursion-gate.md) and companion-approved merge; see [AGENTS.md](../../../AGENTS.md)).

## Suggested Letta memory blocks (labels)

A Letta or similar runtime may use memory block labels such as:

- `grace_mar_boundary`
- `grace_mar_context`
- `operator_instructions`
- `runtime_session_notes`

These are **Letta-local** (runtime) context blocks. They are **not** Grace-Mar
Record surfaces and must not be treated as SELF, EVIDENCE, SKILLS, or
SELF-LIBRARY.

**Promotion path (short):**

Letta summary → runtime complement **inbox** + **receipt** → **human
review** → optional **recursion-gate** candidate → normal **gate** / approved
merge.

Full contract: [LETTA-ADAPTER-CONTRACT](LETT-ADAPTER-CONTRACT.md).

## What this adapter does

- Reads an export bundle from
  [`export_runtime_context.py`](../../../scripts/runtime/export_runtime_context.py)
- Produces a **Letta seed** JSON (`kind: letta_seed_context`) with
  `suggested_memory_blocks` and bundle provenance
  ([`letta_prepare_seed.py`](../../../scripts/runtime/letta_prepare_seed.py))
- Documents example session summaries; imports an example (or your file)
  through [`letta_import_summary.py`](../../../scripts/runtime/letta_import_summary.py)
  → `import_runtime_observation.py`

## What this adapter does not do

- Does not call Letta APIs
- Does not require a Letta SDK
- Does not create or manage Letta agents in-repo
- Does not write canonical Grace-Mar Record files
- Does not promote Letta memory into SELF, EVIDENCE, SKILLS, or SELF-LIBRARY
- Does not bypass or edit [`recursion-gate.md`](../../../users/grace-mar/recursion-gate.md) outside normal human flow
- Does not add Docker

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

`export_runtime_context.py` prints the bundle path. Substitute
`<printed-bundle-path>` with that value (a path under
`runtime/runtime-complements/exports/`, e.g. `.../runtime-complement-export_<timestamp>_letta-demo.json`).

```bash
python3 scripts/runtime/letta_import_summary.py \
  --input bridges/runtime-complements/letta/letta-session-summary.example.json
```

A bare `python3 scripts/runtime/letta_import_summary.py` uses the same
example file by default.

## See also

- [runtime complements doctrine (membrane)](../../../docs/runtime/runtime-complements.md)
- [LETTA-ADAPTER-CONTRACT](LETT-ADAPTER-CONTRACT.md) (contract)
- [letta-seed.example.json](letta-seed.example.json)
- [letta-session-summary.example.json](letta-session-summary.example.json)
