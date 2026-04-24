# Journal metrics habit (operator WORK)

**Scope:** Optional **telemetry on journaling practice** for [dev-notebook/journal](work-dev/dev-notebook/journal/README.md) and [cici-notebook](work-cici/cici-notebook/README.md). **Not** Record truth, not gated merges, not a second history file (see [work-dev-history.md](work-dev/work-dev-history.md) / [work-cici-history.md](work-cici/work-cici-history.md)).

**Principle:** Measure **learning velocity, friction, and follow-through** without turning journals into milestone logs or long dashboards. Entries stay **short**; metrics stay **light**.

---

## Phase 0 — Weekly check (no YAML required)

**Cadence:** ~5 minutes, end of week (or after dream). Open **last 2 entries** in each journal you use.

Ask:

1. **Tomorrow follow-through:** Did the prior entry’s “tomorrow / next” line get **advanced or explicitly superseded**? (Yes / partial / no.)
2. **Blocker carryover:** Is **any blocker** from the prior entry **still open** under the same name or the same underlying issue? (Count or list short labels.)
3. **Friction resolution:** For blockers **first named** in an older entry, is there a **resolution or new understanding** in a later entry? (Note approximate **journal-day gap** if obvious.)

If this habit sticks for a few weeks, consider **Phase 1** optional frontmatter on new entries only.

---

## Phase 1 — Optional YAML frontmatter (v1)

Add **only** when it feels cheap. Keep the **body** as the real journal; YAML is machine-readable hints.

**Placement:** Top of file, before `# Title`:

```yaml
---
journal_metrics:
  version: 1
  prior_tomorrow_addressed: 1   # 1=yes, 0=no, empty=not assessed
  blockers_carried_from_prior: 0 # count (same underlying issue still open)
  blockers_named: 1             # optional: count this entry
  wins: 1                       # optional
---
```

**Fields (minimal):**

| Field | Meaning |
|-------|---------|
| `prior_tomorrow_addressed` | Did you advance or clearly supersede **yesterday’s** “tomorrow” line? `1` / `0`. Leave empty if no prior entry. |
| `blockers_carried_from_prior` | How many **prior** blockers are **still open** (same issue, even if reworded). |
| `blockers_named` | How many **new** blockers named this entry (optional). |
| `wins` | Optional count of completed wins this entry. |

**Stable blocker labels (recommended):** When the same friction returns, reuse a **short id** in prose, e.g. `Blocker (harness-export): …` — makes carryover visible without NLP.

**What we are *not* automating in v1:** Focus drift, compression, reflection-to-action ratio — use Phase 0 judgment or a future v2.

---

## Core definitions (so numbers mean something)

**Tomorrow follow-through:** The **prior** entry had a “tomorrow / next” line; this entry shows **progress** (done, started, or explicit “deprioritized because …”). Partial counts as **partial**, not failure.

**Blocker carryover:** A blocker **first stated** in entry N is **still unresolved** in entry N+1 (same root cause). Rewording alone does not count as resolution.

**Friction resolution latency (journal days):** First journal day a blocker **b** appears → first day **b** is marked resolved, closed, or reframed into a **new** actionable with different root cause. Computed manually from Phase 0 or from stable `blocker_id` labels across files.

---

## Script

From repo root:

```bash
python3 scripts/journal_habit_snapshot.py
```

Prints **active days (last 14)** and **staleness** per journal from **filenames** (`*-day-*.md` under **dev-notebook/journal**; `YYYY-MM-DD.md` for cici-notebook). No frontmatter required.

---

## Boundary

If filling YAML **reduces** how often you journal, **drop YAML** and keep Phase 0 only. The habit matters more than the dashboard.
