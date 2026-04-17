# SELF-HISTORY — grace-mar

> **Derived dual log** — **not** part of the **Record**; **not** a merge surface for new identity facts. **Canonical truth** remains **`self.md`**, **`self-archive.md`** (EVIDENCE + § VIII), and **`bot/prompt.py`** after **RECURSION-GATE** approval. This file **aggregates and narrates**; it does **not** override **SELF**, **EVIDENCE**, **`self-memory`**, or **`session-log`**.

---

## Purpose

**`self-history`** holds a **systematic, dense** timeline that combines:

1. **WORK stream** — consolidation of per-lane operator milestones from **`docs/skill-work/work-*/*-history.md`** (see [work-modules-history-principle.md](../../docs/skill-work/work-modules-history-principle.md)).
2. **COMPANION stream** — **gate-approved** companion-relevant events and facts already merged into **SELF / EVIDENCE** (summaries or pointers with **ACT ids / dates / merge receipts** — never **pending** gate text as fact).

**Use:** human orientation, future retrieval, and (optionally) ML — with **provenance** preserved so the two streams do not collapse.

---

## Contract

| Tag (in-body) | Meaning | Source of truth |
|----------------|---------|-----------------|
| **`WORK:`** | Lane activity, artifacts, SHAs | Respective **`work-*-history.md`**; git |
| **`COMPANION:`** | Life / identity milestones as **approved** | Merged **`self-archive.md`**, **`self.md`**, § VIII — not staging |

**Density:** Prefer **dated blocks**, **tight bullets**, paths, and ids over diary prose.

**Backdoor rule:** New companion facts enter only via **RECURSION-GATE** + merge script — **not** by “writing them here first.”

---

## Maintenance

Choose one rhythm and stick to it (document changes here if you switch):

- **Append-only gazette** — new **`## YYYY-MM-DD`** sections only; older blocks stay frozen.
- **Periodic rebuild** — regenerate from sources on a schedule; note rebuild date in a header comment line if useful.

**Semi-automation:** [`scripts/draft_self_history.py`](../../scripts/draft_self_history.py) — draft **WORK** / **COMPANION** markdown from `work-*-history.md` and `self-archive.md` § V (default: print to stdout; **`--write`** refreshes log sections from `## Log — WORK (aggregate)` through EOF).

### Initial population (2026-03-30)

- **COMPANION strategy:** **3a — monthly rollup** from merged **`users/grace-mar/self-archive.md` § V. ACTIVITY LOG** (YAML `activities`); not § VIII transcript; not pending gate.
- **WORK strategy:** Copy from **`docs/skill-work/work-*/*-history.md`** logs as of same date; note empty lanes explicitly.

---

## Log — WORK (aggregate)

- **WORK:work-dev — 2026-03-30** — Huang / Lex #494 digest + OpenClaw/Grace-Mar diff: `research/external/work-dev/transcripts/lex-fridman-494-jensen-huang-DIGEST.md`; README index row; commits through `51de012` (source: [work-dev-history.md](../../docs/skill-work/work-dev/work-dev-history.md)).
- **WORK:meta — 2026-03-30** — No dated `## Log` entries yet in other `docs/skill-work/work-*/*-history.md` territories (work-politics, work-jiang, work-strategy, work-business, work-career, work-companion-self, work-curate-library, work-health-fitness, work-human-teacher, work-xavier, work-civ-mem, work-alpha-school).

---

## Log — COMPANION (gate-approved)

- **COMPANION: 2026-02** — 44 activities in `self-archive.md` § V (`ACT-0001`–`ACT-0044`). Canonical: [self-archive.md](self-archive.md) **§ V. ACTIVITY LOG**.
- **COMPANION: 2026-03** — 11 activities in `self-archive.md` § V (`ACT-0045`–`ACT-0055`). Canonical: [self-archive.md](self-archive.md) **§ V. ACTIVITY LOG**.
