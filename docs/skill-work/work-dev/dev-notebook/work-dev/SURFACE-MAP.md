# work-dev — surface map (grace-mar)

**Not** a Git `main` tree (contrast: [work-cici UPSTREAM-MAP](../work-cici/UPSTREAM-MAP.md)). This table lists **authoritative** work-dev **paths in this repo** and a few **explicit** external template pointers. Re-read [work-dev README](../../README.md) when extending rows.

| Path (grace-mar) | Role | Note |
|------------------|------|------|
| [workspace.md](../../workspace.md) | **Entrypoint** — current blockers, next actions (operator). | Stale-OK; operator-maintained. |
| [work-dev-history.md](../../work-dev-history.md) | **Milestone** append-only log (shipped artifacts, GAPs). | Distinct from [dev journal](journal/README.md) narrative. |
| [work-dev README](../../README.md) | **Territory** identity, OpenClaw integration, **Contents** table. | Template mirror: [companion-self work-dev](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-dev/README.md) |
| [known-gaps.md](../../known-gaps.md) | GAP / control-plane index. | — |
| [implementation-ledger.md](../../implementation-ledger.md) | Narrative spine for `artifacts/work-dev`. | — |
| [workbench/](../../workbench/README.md) | Workbench harness (receipts, no merge authority). | — |
| [control-plane/](../../control-plane/) (as indexed in README) | Contracts, checklists, tier policy. | See README Contents. |
| [scripts/](../../../../../scripts/) (selected) | Cross-cutting scripts (`detect_capability_shift.py`, `emit_compute_ledger.py`, `journal_habit_snapshot.py`, …) | Many paths are cited in work-dev-history. |
| [dev-notebook/journal/](./journal/) | Inward day journal (this tree). | Symlink: `users/grace-mar/SELF-LIBRARY/dev-journal` → here. |
| [identity-fork-protocol-ifp-2026-04-24.md](./identity-fork-protocol-ifp-2026-04-24.md) | **IFP** spec snapshot (WORK): identity fork + merge sovereignty + membrane (links to gate, workbench). | Not SELF/EVIDENCE. |
| [journal-metrics-habit.md](../../journal-metrics-habit.md) | Light habit / telemetry (optional). | — |

**Regen:** None — this map is hand-maintained when you add a new “canonical” work-dev surface. Prefer linking the territory [README](../../README.md#contents) to avoid drift.
