# Work-Dev Compound Dashboard

**Purpose:** One **derived** markdown page that summarizes the state of the work-dev **compound** layer: note inventory, gate-candidate pointers, stale/duplicate hints, presence of other generated reports, and links to related docs and scripts. It is an **operator-facing** view, not canonical memory.

**Inputs:** Markdown files under `docs/skill-work/work-dev/compound-notes/` (same shape as [compound-note-template.md](compound-note-template.md)), parsed via [scripts/work_dev/compound_notes.py](../../scripts/work_dev/compound_notes.py).

**Output:** Regenerable file `artifacts/work-dev-compound-dashboard.md` from:

```bash
python3 scripts/build_work_dev_compound_dashboard.py
```

Optional flags: `--notes-dir`, `--output`, `--repo-root`, `--include-sections` (comma-separated section ids; omit for all).

**Boundary rule:** This dashboard is part of the **WORK** loop only. It does **not** update the **Record**, SELF, SKILLS, EVIDENCE, or the Library; it does **not** write `users/grace-mar/recursion-gate.md`; it does **not** call `stage_gate_candidate.py`. Treating something as a **gate candidate** in a note or in the gate export is **not** approval.

**Authority metadata:** Generated output begins with a YAML block (`derived: true`, `recordAuthority: none`, `gateEffect: none`, `artifact_kind: …`); see [work-dev-derived-markdown-authority.md](work-dev-derived-markdown-authority.md) for the shared convention with the other compound `artifacts/work-dev-compound-*.md` files.

**Relationship to other docs**

| Doc | Role |
|-----|------|
| [compound-loop.md](compound-loop.md) | **Process:** Plan → Execute → Review → Compound → Gate; includes the **Operator index** of tools. |
| [compound-gate-export.md](compound-gate-export.md) | **Export** script and boundary for `artifacts/work-dev-compound-gate-candidates.md`. |
| [three-compounding-loops.md](three-compounding-loops.md) | How **Record**, **WORK**, and **CI** loops interact; gate is the only durable promotion path for Record change. |
| [derived-regeneration.md](derived-regeneration.md) | Derived artifacts and rebuildability in work-dev more broadly. |

The **refresh** report (`artifacts/work-dev-compound-refresh.md`) focuses on metadata aggregations and similar duplicate/stale heuristics; the **dashboard** adds a single at-a-glance page with artifact/doc/script inventory and suggested next actions. Regenerate the dashboard after running refresh or the gate export so counts stay aligned.
