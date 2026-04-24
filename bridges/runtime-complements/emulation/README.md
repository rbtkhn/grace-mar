# Emulation adapter examples

These examples show how a foreign runtime can consume the emulation-oriented export bundle without becoming the system of record.

## Status

Example-only, non-authoritative, stdlib-first.

## Use this when

Use these examples when a downstream runtime needs a governed identity package with:

- the PRP for behavior loading
- the fork export for machine-readable inspection
- the policy references needed to return durable changes safely

## Do not use this when

If you only need a narrow membrane-safe context bundle or a place to import runtime-only observations, use:

- `scripts/runtime/export_runtime_context.py`
- `scripts/runtime/import_runtime_observation.py`

That membrane path is smaller and intentionally does not package the broader governed export set.

## Files

- `simple_llm_emulation.example.py` — minimal stdlib loader that builds a system prompt and safe return payloads
- `langgraph_emulation.example.py` — example node shape for graph-style runtimes without introducing a new runtime root here

## Export first

```bash
python3 scripts/export.py emulation -- --mode portable_bundle_only -o /tmp/grace-mar-emulation
```

Then point the example loader at that output directory.
