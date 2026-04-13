# Runtime storage boundaries (safety)

Grace-Mar **does not** adopt ambient instruction-file or scatter-write patterns reported against some external memory tools.

## Hard rules

1. **Single ledger root** — Runtime observations append only to `runtime/observations/index.jsonl` (or a path overridden by `GRACE_MAR_RUNTIME_LEDGER_ROOT` for tests).
2. **No instruction files as side effects** — Logging and retrieval do not create `CLAUDE.md`, `.cursorrules`, or similar outside documented surfaces.
3. **No silent promotion** — Runtime JSON never merges into the Record without the gate pipeline.
4. **Optional services** — Any future HTTP or worker must document access control; do not expose captured observations on wide interfaces by default.

## Tests

`tests/runtime/test_log_observation.py` asserts the logger does not write outside `runtime/observations/` under an isolated ledger root.
