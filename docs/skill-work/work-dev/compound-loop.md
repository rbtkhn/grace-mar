# Compound Work Loop (work-dev)

**Status:** WORK-layer process. **Not** canonical memory. **Not** automatic Record.

## What it is

A **lightweight loop** for coding-agent work inside Grace-Mar:

1. **Plan** — smallest safe change, files to touch, governance risks identified before code.
2. **Execute** — implement with minimal additive diffs; run checks; summarize what changed.
3. **Review** — use the [reviewer matrix](reviewer-matrix.md) to structure findings (not seven separate agents by default—one pass, seven lenses).
4. **Compound** — capture **reusable lessons** in [compound notes](compound-note-template.md) under `compound-notes/` (WORK artifacts only).
5. **Gate** — the **only** path by which anything becomes a durable **Record** candidate; compound notes may *recommend* gate action but do not merge or promote by themselves.

**Compound** here means: produce **reusable WORK-layer learning** (patterns, failure modes, test ideas, UX fixes)—**not** merge, **not** silent updates to SELF, SKILLS, EVIDENCE, Library, or other durable surfaces.

## Why this exists

Grace-Mar already compounds cognition through **governed memory and evidence** (Record loop) and through **tests and CI** (repo loop); see [three-compounding-loops.md](three-compounding-loops.md). This document adds a **visible, reviewable** way for **coding-agent sessions** to compound **implementation and review lessons** in the WORK lane—without creating a parallel “agent memory” or bypassing the companion gate.

Related: [claim-proof-standard.md](claim-proof-standard.md) (proof bar for “implemented”), [workbench/README.md](workbench/README.md) (inspection receipts; not merge receipts).

## Boundary rule

| Stage | May produce | May not |
|-------|-------------|---------|
| Runtime / agent work | Code diffs, logs, **compound notes** (markdown in `compound-notes/`) | Direct edits to canonical Record paths |
| Compound notes | Text, `gate_candidate: true` **recommendation** only | Automatic staging or merge to SELF, SKILLS, EVIDENCE, etc. |
| Gate (existing process) | Approved promotion per Grace-Mar rules | N/A (this layer does not implement the gate) |

**Nothing skips the gate.** A compound note may be marked as a **gate candidate**; that is a **staging recommendation** for human/companion review, not approval.

**No script in this layer** may edit canonical Record surfaces.

## Artifacts and scripts

| Artifact / tool | Role |
|-----------------|------|
| [compound-note-template.md](compound-note-template.md) | Shape of a compound note. |
| [reviewer-matrix.md](reviewer-matrix.md) | Seven reviewer lenses; conservative promotion rules. |
| [agent-prompts/](agent-prompts/) | Reusable agent instructions (Plan / Execute / Review / Compound / Refresh). |
| `compound-notes/*.md` | Append-only or additive notes (operator may archive/delete; not Record). |
| `python3 scripts/new_work_dev_compound_note.py` | Create a new compound note from the template. |
| `python3 scripts/work_dev_compound_refresh.py` | Derived report on existing notes; **regenerable**; see `artifacts/work-dev-compound-refresh.md`. |

## Non-goals

- Replacing [implementation-ledger.md](implementation-ledger.md) JSON machinery or the recursion gate pipeline.
- Spawning many autonomous agents; use **one** review pass with the **matrix**, not a fleet.
