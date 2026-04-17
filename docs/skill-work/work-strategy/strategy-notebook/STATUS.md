# Strategy notebook — status

> Operator-maintained. Run from repo root; not auto-generated.

| Field | Value |
|-------|--------|
| **Project status** | `active` |
| **Active chapter** | `2026-04` |
| **Last substantive entry** | `2026-04-16` — **`## 2026-04-16`** in [`chapters/2026-04/days.md`](chapters/2026-04/days.md#2026-04-16): Marandi BP + Pape knots; **`strategy + verify`** (Macgregor×WSJ, Parsi×Daily Beast); ROME (Leo XIV Bamenda × Hegseth); **`thread:alexander-mercouris` × §1g** seam; **`thread:douglas-macgregor`** (JF 04-16 + optional Macgregor `X` lines still filed under inbox **Expert X … 2026-04-18** — accumulator date, not an extra `days.md` heading). Earlier mistaken **`## 2026-04-17` / `## 2026-04-18`** splits were folded here; see weave date note in that block. |
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

Calendar **`## YYYY-MM`** blocks in **`strategy-expert-*-thread.md`** (inside the **journal layer**) follow a **parse contract** (terminators, prose minimum, scripts). For **2026**, **Segment 1–4** = Jan–Apr month headings — not the machine layer. Spec: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Expert-thread month segments (parse contract + scripts)](STRATEGY-NOTEBOOK-ARCHITECTURE.md#expert-thread-month-segments). Validate: `python3 scripts/validate_strategy_expert_threads.py`.

## Next actions

1. When adding new work, append a **`## YYYY-MM-DD`** block (or an episodic `##` section) at the bottom of [`chapters/2026-04/days.md`](chapters/2026-04/days.md) when ready — target **~1000 words** of consolidated analysis per **weave** where applicable (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Entry model*); bump **Last substantive entry** here.
2. Refresh this file when the active month changes or after notable closes.
