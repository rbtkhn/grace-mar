# workbench-receipts (work-dev)

**Purpose:** Default **storage location** for [Workbench Harness](../../../docs/skill-work/work-dev/workbench/README.md) JSON receipts — **workbench** `receiptKind` only. **Not** the Record, **not** EVIDENCE, **not** a merge or gate artifact by itself.

**Usage:** Add `*.json` files here (or in dated subfolders) as your team prefers. If some runs are **local-only** (large binaries, client secrets in paths), add patterns to **`.gitignore`** at repo root or here — do not commit sensitive paths.

**Spec:** [WORKBENCH-RECEIPT-SPEC.md](../../../docs/skill-work/work-dev/workbench/WORKBENCH-RECEIPT-SPEC.md)

**Examples (fixtures, non-authoritative):** [workbench/examples/](../../../docs/skill-work/work-dev/workbench/examples/)
