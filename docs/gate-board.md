# Gate Board

The Gate Board is a **generated Kanban-style operator view** over Grace-Mar’s existing review system. It lives at [`artifacts/gate-board.md`](../artifacts/gate-board.md).

## Purpose

- Make the Approval Inbox easier to **steer** (what is new, blocked, or decision-ready).
- Surface **blocked** vs **review-ready** candidates using simple, legible columns.
- Provide a **compact status overview** without replacing canonical review artifacts.

## Non-goals

- This is **not** a source of truth.
- **Editing** `artifacts/gate-board.md` does **not** change candidate status.
- This does **not** replace [`users/grace-mar/recursion-gate.md`](../users/grace-mar/recursion-gate.md), [`users/grace-mar/review-queue/`](../users/grace-mar/review-queue/), or canonical change-review JSON.

## Authority

Canonical review state remains in the **normal gate and review workflow**:

- `recursion-gate.md`
- `review-queue/` and canonical change-review objects (see [identity-fork-protocol.md](identity-fork-protocol.md) §4)

`artifacts/gate-board.md` is a **derived operator dashboard** only.

## Column mapping (pending precedence)

For candidates in the **active** region (above `## Processed`), `status: pending` rows are classified in this order:

1. **Needs contradiction check** — conflict/contradiction signals (YAML text or pipeline advisory hints when enriched data is available).
2. **Needs evidence** — weak provenance / evidence linkage (heuristic; see `scripts/build_gate_board.py`).
3. **New** — thin staging (e.g. very short summary) once the above do not apply.
4. **Ready for review** — everything else still pending.

**Approved** (active): `status: approved` — companion approved; merge not yet applied (see gate invariant).

**Rejected**: `status: rejected` in either active or processed.

**Merged** (processed): `status: approved` under `## Processed` — historical approved / integrated archive in the file layout Grace-Mar uses.

## Regenerate

From repo root:

```bash
python3 scripts/build_gate_board.py
```

Optional: `--output path/to/gate-board.md`, `-u <user-id>` (default `grace-mar`), `--repo-root <path>`.

## See also

- [Runtime vs Record](runtime-vs-record.md)
- [Operator dashboards](operator-dashboards.md)
- [Review dashboard artifact](../artifacts/review-dashboard.md) (tabular companion view)
