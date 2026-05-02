# Decision Ledger

**Status:** WORK-only operator ledger. Not Record, not gate authority, not companion identity.

This ledger records durable operator decisions about architecture, runtime, workflow, and rebuildable substrate. It exists so decisions can compound without turning self-memory into a permanent architecture notebook or treating cadence logs as the only source of continuity.

## Boundary

- Use this file for architecture/runtime/workflow decisions that should survive a session.
- Do not use it for companion identity facts, EVIDENCE, SELF-KNOWLEDGE, or Voice truth.
- If a decision would change Record truth, stage it through `users/grace-mar/recursion-gate.md`.
- If a decision creates or updates a reference source, route it through SELF-LIBRARY governance.
- If a decision is short-lived session state, keep it in `users/grace-mar/self-memory.md` instead.

## Entry Format

| Field | Meaning |
|-------|---------|
| Decision ID | Stable `DL-YYYY-MM-DD-NN` id |
| Status | `active`, `watch`, `revisit`, or `retired` |
| Decision | One-sentence commitment |
| Rationale | Why this was chosen |
| Affected surfaces | Docs, scripts, config, or workflows touched |
| Source / receipt | Session, transcript, commit, bridge, or doc anchor |
| Revisit trigger | What would cause review |

## Decisions

| Decision ID | Status | Decision | Rationale | Affected surfaces | Source / receipt | Revisit trigger |
|-------------|--------|----------|-----------|-------------------|------------------|-----------------|
| DL-2026-05-01-01 | active | Keep local-first substrate polish evolutionary rather than creating a parallel architecture. | Grace-Mar already has runtime complements, model routing, trust registries, and derived regeneration; the missing value is naming the joins. | `docs/sovereignty.md`, `docs/runtime/model-portfolio.md`, `docs/runtime/local-runtime-notes.md`, derived regeneration | Operator transcript synthesis, 2026-05-01 | Revisit if model routing YAML, local runtime execution, or bridge/conductor routing logs become the primary implementation surface. |
| DL-2026-05-01-02 | active | Treat decision-ledger summaries as derived WORK artifacts, not canonical memory. | Decisions should be easy to recover and rebuild, but authority remains in the source ledger plus existing gate boundaries. | `artifacts/work-dev/decision-ledger-summary.md`, `scripts/build_decision_ledger_summary.py`, `scripts/derived_regeneration.py` | Local-first substrate polish, 2026-05-01 | Revisit if ledger rows begin carrying Record claims or duplicate self-memory long-horizon notes. |

## Maintenance

- Add new rows when a decision changes how Grace-Mar is operated, regenerated, routed, or governed.
- Keep entries concise; link out to richer specs rather than turning this ledger into a design doc.
- Use `revisit` when the decision still matters but the original rationale is under stress.
- Derived summary target: `decision-ledger-summary`.
