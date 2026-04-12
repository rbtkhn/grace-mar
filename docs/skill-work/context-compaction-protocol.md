# Context compaction protocol

**Purpose:** Standard **shapes** for compact representations of Grace-Mar WORK and Record-adjacent surfaces. Formats are **documentation-first**; automation may follow.

**Governance:** Compacted text is **operator scaffolding** unless it becomes a gated candidate. Recovery links point at **canonical** paths—not paraphrase as authority.

---

## Provenance block (required when compacting)

Any compact block should carry:

- **Source path** (repo-relative): e.g. `users/grace-mar/recursion-gate.md`
- **Anchor or id** when applicable: e.g. `CANDIDATE-0098`
- **Freshness:** file mtime or explicit “as of YYYY-MM-DD” for notebooks

---

## Gate pending (one-liner per candidate)

```
CANDIDATE-XXXX — <one-line summary from gate YAML> — `users/<id>/recursion-gate.md`
```

Use with **candidate impact preview** when merge risk matters:

- CLI: `python3 scripts/preview_candidate_impact.py` (see work-dev tooling)
- Dashboard: `apps/gate-review-app.py` (compact “why this matters” + impact box)

**Compact review bundle:** summary line + source path + optional impact preview output—not full surrounding markdown.

---

## Decision point (WORK-strategy)

From [decision-point-template.md](work-strategy/decision-point-template.md), compact to:

- **Question** (one line)
- **Recommended option** + **one** “what would change my mind”
- **Recovery:** path to full memo

---

## work-dev lane

From [work-dev/workspace.md](work-dev/workspace.md) mindset:

- **Lane name** — one line
- **Next action** — one line
- **Open uncertainty** — optional one line
- **Recovery:** `docs/skill-work/work-dev/workspace.md`

---

## Archive / evidence cluster

- **One paragraph** retrieval synopsis + **section anchor** or ACT id
- **Recovery:** `users/<id>/self-archive.md` section

---

## Session brief output

- **Minimal / compact:** pending IDs + last ACT one-liner + **recovery links** (see `session_brief.py --compact`)
- Budgets: [`config/context_budgets/session_brief.json`](../../config/context_budgets/session_brief.json)

---

## Cross-reference

- [context-efficiency-layer.md](context-efficiency-layer.md) — tiers, boundaries, `index_record` RFC
- [reality-sprint-block.md](reality-sprint-block.md) — post-plan execution wedge
