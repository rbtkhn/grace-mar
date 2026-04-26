# Work-dev derived markdown — authority metadata

**Scope:** The three **regenerable** compound-layer markdown files under `artifacts/`:

- `work-dev-compound-refresh.md` — from `python3 scripts/work_dev_compound_refresh.py`
- `work-dev-compound-gate-candidates.md` — from `python3 scripts/export_work_dev_compound_gate_candidates.py`
- `work-dev-compound-dashboard.md` — from `python3 scripts/build_work_dev_compound_dashboard.py`

Each file begins with a **small YAML block** (before the main `#` title) using the same **vocabulary** as JSON work-dev surfaces (e.g. `recordAuthority: none`, `gateEffect: none` in the [Interface Artifact Protocol](interface-artifacts/INTERFACE-ARTIFACT-PROTOCOL.md) and [Workbench receipt spec](workbench/WORKBENCH-RECEIPT-SPEC.md)):

- **`derived: true`** — the file is derived, not canonical Record.
- **`recordAuthority: none`** — does not assert SELF, EVIDENCE, or Record updates.
- **`gateEffect: none`** — no automatic gate staging, approval, or merge.
- **`artifact_kind`** — which generator produced the file (`work_dev_compound_refresh`, `work_dev_compound_gate_export`, or `work_dev_compound_dashboard`).

This is **not** a JSON schema and does not replace sidecars or receipts used elsewhere. It makes **grepping** and policy checks cheap without changing the prose boundary text that follows the front matter.

**Related:** [compound-dashboard.md](compound-dashboard.md) (operator view), [compound-gate-export.md](compound-gate-export.md), [compound-loop.md](compound-loop.md).
