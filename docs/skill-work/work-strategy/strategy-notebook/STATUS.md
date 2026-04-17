# Strategy notebook — status

> Operator-maintained. Run from repo root; not auto-generated.

| Field | Value |
|-------|--------|
| **Project status** | `active` |
| **Active chapter** | `2026-04` |
| **Last substantive entry** | `2026-04-16` — **`## 2026-04-16`** in [`chapters/2026-04/days.md`](chapters/2026-04/days.md): weave **Marandi** (Breaking Points 2026-04-16) — Signal / Judgment / Links / Open; inbox [`daily-strategy-inbox.md`](daily-strategy-inbox.md) `## 2026-04-16`, expert thread [`strategy-expert-seyed-marandi-thread.md`](strategy-expert-seyed-marandi-thread.md), Hormuz scaffold [`knots/strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md`](knots/strategy-notebook-knot-2026-04-13-marandi-ritter-mercouris-hormuz-scaffold.md). **Also:** `2026-04-18` — Leo XIV Bamenda × Hegseth Pentagon / **ROME-PASS** seam (same `days.md`; [`ROME-PASS.md`](../work-strategy-rome/ROME-PASS.md) § rolling seam note — 2026-04-16). |
| **Prepared stub** | _Optional_ — only if you use calendar stubs; otherwise capture in [daily-strategy-inbox.md](daily-strategy-inbox.md) and **weave** when you run **`strategy`** / explicit **`weave`** / **`fold`** (legacy) |
| **Daily inbox** | [daily-strategy-inbox.md](daily-strategy-inbox.md) — **SSOT** (cadence + paste-ready lines); weave/prune → [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox* |
| **Next stitch** | Optional: roll month-end summary into [STRATEGY.md](../STRATEGY.md) §IV |
| **Operator prefs** | [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) |

## Seam / weave observability (optional)

| Artifact | Role |
|----------|------|
| [gamification-metrics.md](gamification-metrics.md) | Guardrails + meaning of `weave_count` / `seam_integrity` / checklist flags in `knot-index.yaml` v4+ |
| [`python3 ../../../../scripts/knot_seam_metrics.py`](../../../../scripts/knot_seam_metrics.py) | Read-only: outgoing links to other knot files vs optional `weave_count` |
| [forecast-watch-log.md](forecast-watch-log.md) | Monthly / episodic falsifiable metrics (preferred to raw counts) |

## Expert-thread month segments (skill-strategy pointer)

Calendar **`## YYYY-MM`** blocks in **`strategy-expert-*-thread.md`** Segment 1 follow a **parse contract** (terminators, prose minimum, scripts). Spec: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Expert-thread month segments (parse contract + scripts)](STRATEGY-NOTEBOOK-ARCHITECTURE.md#expert-thread-month-segments). Validate: `python3 scripts/validate_strategy_expert_threads.py`.

## Next actions

1. When adding new work, append a **`## YYYY-MM-DD`** block (or an episodic `##` section) at the bottom of [`chapters/2026-04/days.md`](chapters/2026-04/days.md) when ready — target **~1000 words** of consolidated analysis per **weave** where applicable (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Entry model*); bump **Last substantive entry** here.
2. Refresh this file when the active month changes or after notable closes.
