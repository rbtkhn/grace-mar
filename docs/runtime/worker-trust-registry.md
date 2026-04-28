# Worker trust registry

Grace-Mar keeps an inspectable map of runtime-related workers in [`config/runtime_workers/registry.yaml`](../runtime_workers/registry.yaml) and routing docs ([worker-routing.md](worker-routing.md)). The **worker trust registry** is an additive JSON document that records—per worker—allowed authority bounds, forbidden actions, evidence expectations, receipt expectations, and gate-review requirements.

## Non-goals (read this first)

- **No canonical authority.** This registry is **documentation plus CI validation**. It does **not** grant merge approval, does **not** give workers authority over [`RECURSION-GATE`](../../users/grace-mar/recursion-gate.md), and does **not** change companion-controlled merges ([`process_approved_candidates.py`](../../scripts/process_approved_candidates.py)).
- **No Record edits.** Workers documented here **must not** be interpreted as permission to edit `users/*/self.md`, `self-archive.md`, or [`bot/prompt.py`](../../bot/prompt.py); those paths remain governed solely by the gated pipeline in [`AGENTS.md`](../../AGENTS.md).

If tooling reads this file in the future, treat it as **constraints documentation**, not as an ACL that replaces human gate review.

## Files

| File | Role |
|------|------|
| [`config/runtime_workers/worker-trust-registry.v1.json`](../../config/runtime_workers/worker-trust-registry.v1.json) | Trust bounds per worker `id`. |
| [`schemas/worker-trust-registry.v1.schema.json`](../../schemas/worker-trust-registry.v1.schema.json) | JSON Schema (draft 2020-12) for the document shape. |
| [`scripts/runtime/verify_worker_trust_registry.py`](../../scripts/runtime/verify_worker_trust_registry.py) | Validates schema + policy rules + parity with `registry.yaml`. |

## Verify locally

```bash
python3 scripts/runtime/verify_worker_trust_registry.py
```

Exit code **0** means schema validation passed and policy checks passed:

- No worker lists `approve_candidate`, `merge_candidate`, `edit_record_surface`, or `overwrite_record_surface` in **`allowed_actions`**.
- Any worker with **`stage_candidate`** in `allowed_actions` must set **`gate_review_required`** to **true**.
- Every worker id declared under `shared_workers` / `routed_workers` in [`registry.yaml`](../../config/runtime_workers/registry.yaml) appears **exactly once** in the trust registry. Orchestrator-only ids (e.g. `grace_mar_runtime_worker`) may appear in addition to those keys.

## Field glossary

| Field | Meaning |
|-------|---------|
| `allowed_actions` | Verb-like capability tokens this worker may claim when documented honestly (not an executable ACL). |
| `forbidden_actions` | Explicit denial list; always includes merge/approve/Record edit tokens as documentation. |
| `evidence_requirements` | What operators or auditors expect when asserting lineage or scope. |
| `receipt_expectations` | What runtime receipts or artifacts might exist (see [execution receipts](execution-receipts.md)); non-canonical. |
| `gate_review_required` | Whether staged output must pass human gate review before merge—**required** when staging candidates is allowed. |

## Maintenance

When adding a worker to [`registry.yaml`](../../config/runtime_workers/registry.yaml), add a matching row to [`worker-trust-registry.v1.json`](../../config/runtime_workers/worker-trust-registry.v1.json) and run the verifier.

Optional CI hardening: add an explicit workflow step `python3 scripts/runtime/verify_worker_trust_registry.py` next to other work-dev validators (full `pytest tests/` already exercises [`tests/test_worker_trust_registry.py`](../../tests/test_worker_trust_registry.py)).

## See also

- [Worker routing](worker-routing.md)
- [Execution receipts](execution-receipts.md)
