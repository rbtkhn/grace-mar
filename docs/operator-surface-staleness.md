# Operator surface staleness

## 1. Purpose

Grace-Mar uses **derived** operator-facing surfaces (under `artifacts/`, in `docs/workflows/`, and similar) to make **review, navigation, workflow observation, and lane work** easier to scan. Many of these outputs are **generated or semi-generated**. Each **major** surface should make its **freshness expectations** easy to reason about: what built it, what source inputs it reflects, whether it is plausibly **current**, and how to **rebuild** or re-check it.

**Staleness** is about **operator legibility**, not a second authority layer. Staleness notes do **not** change who may merge, gate, or write the Record. See [§6 Anti-authority rule](#6-anti-authority-rule).

**Related:** [operator surface registry](operator-surface-registry.md) (taxonomy), [runtime vs Record](runtime-vs-record.md) (canonical vs derived), [artifacts README](../artifacts/README.md) (producer table).

## 2. Staleness principle

A **stale** operator surface may still be **useful as a historical** snapshot (e.g. last run, last gate parse), but it must **not** be treated as the **only** or **binding** view of current operational reality when the **declared source inputs** have changed.

**Canonical** durable state (Record, gate file for pending candidates, and other governance-declared sources) lives where [AGENTS.md](../AGENTS.md) and [runtime vs Record](runtime-vs-record.md) say it lives—not in a derived dashboard, report, or JSON feed, **regardless of freshness**. If a surface is out of date, **refresh the surface** (regenerate) or **read the source**; do not treat staleness as “more true” or “less binding” of the *canonical* path—**canonical** is not determined by the artifact timestamp.

**Authority:** A stale line in a **derived** file does not grant or remove **merge** authority, **gate** effect, or **Record** write access.

## 3. Staleness note format (Markdown)

Use a **blockquote** so the note is visually distinct. Full template (shorten for small hand-maintained files):

```markdown
> **Staleness note:** This surface is derived from [name source inputs]. It is current only as of its last generation or manual review. If the source inputs have changed, **regenerate** or **re-check the source** before using this file alone for time-sensitive operator decisions.
>
> - **Surface class:** one of: dashboard, index, report, receipt, packet, sidecar, machine feed, lane-local surface
> - **Authority status (operator surface):** e.g. derived_non_authoritative, advisory, review_support, machine_feed — see [operator surface registry](operator-surface-registry.md) §3
> - **Source inputs:** …
> - **Producer / rebuild:** …
> - **Last generated / reviewed:** unknown in file unless the artifact or sidecar states it
```

**Short form** (when a long block is noisy):

> **Staleness note:** Derived, non-canonical. Confirm against declared **source inputs** and **rebuild** if you need a current view.

**JSON / machine feeds:** Do not rely on `//` comments in JSON. Put staleness in **sibling** README or the **enclosing** doc (e.g. [operator surface registry](operator-surface-registry.md) row, [artifacts README](../artifacts/README.md) policy), or in **metadata** fields the schema allows.

**Script-generated files:** If a file is normally **overwritten** by a script, **do not** hand-edit a staleness block into it for long—prefer the convention in this document plus the registry, or (future) extend the **generator** to emit a standard line. Hand edits will be clobbered on the next regen.

## 4. Staleness levels

Use these labels in registry metadata, JSON, or human prose when you need a **shared vocabulary**. They are **heuristic**—not automation.

| Level | Meaning |
|--------|--------|
| `current_declared` | The artifact or sidecar **states** a generation or review time and the **source inputs** are known; you can compare to source change times. |
| `current_unknown` | The file **exists** but you cannot determine freshness from the artifact **alone** (no timestamp, unclear inputs). |
| `stale_possible` | The artifact is **derived** from sources that **may** have changed since the last regen; assume verify if the decision is load-bearing. |
| `stale_likely` | The artifact is **older** than a reasonable regen/review cadence, or is **missing** source context, so fresh output is **unlikely** without action. |
| `historical_only` | The artifact is a **record of a past** run, snapshot, or receipt—**not** a live “current system state” view unless regenerated. |

**Staleness does not flip authority status:** a `current_declared` derived file is still **derived** (non-Record) unless doctrine elsewhere names it canonical.

## 5. Surface-specific guidance

### Dashboards

- Should **declare** source inputs and regen path (script name, link to [artifacts README](../artifacts/README.md), or sidecar). Often **`stale_possible`** after any edit to a listed source. Confirm against **source** (e.g. `recursion-gate.md` for gate dashboards) for decisions that must match the live file.

### Reports

- Often **snapshots** in time. Treat as **`stale_possible`** or **`historical_only`** unless you just ran the report. **Do not** treat an old report as the current state of a lane without re-run.

### Receipts

- **Historical by design** (what happened in a run). **Do not** “update” a receipt to look current. Level is often **`historical_only`**. Use a **new** receipt for a new run.

### Packets

- Bound to a **task** and evidence set. Stale if the **underlying** candidate, paths, or evidence **changed**—rebuild or re-export the packet.

### Sidecars

- Must stay **paired** with the artifact they describe (`*.derived-rationale.json` next to the same stem). Stale if the **primary** artifact is stale or inputs drifted; **regenerate** the target artifact’s pipeline.

### Machine feeds

- Document freshness in a **folder README**, **registry** row, or **wrapper** doc—**not** invalid inline JSON comments. Pair JSON with `generatedAt`-style fields when the schema provides them.

### Lane-local surfaces

- Declare the **lane** in path or title. Note whether the surface is **operator-maintained** (rare) or **generated**; generated surfaces follow the same staleness pattern as other scripts.

## 6. Anti-authority rule

A **staleness note** or **staleness level** is **not**:

- a grant to write the **Record**;
- a bypass of [`recursion-gate.md`](../users/grace-mar/recursion-gate.md) or companion approval;
- a promotion of a candidate, merge, or `process_approved_candidates.py` path;
- an **expansion** of `authority_class` (see [authority map](authority-map.md)) for workflows, tools, or agents;
- a substitute for **reading** the canonical file when the decision is identity- or merge-bearing.

**Reminder:** [operator surface registry](operator-surface-registry.md) and this doc describe **operator navigation**; they are **not** merge authority. See [AGENTS.md](../AGENTS.md) gated pipeline.

## 7. Minimal adoption policy (this repo)

- Prefer **convention in this file** + **pointers** from the [operator surface registry](operator-surface-registry.md) and [artifacts README](../artifacts/README.md) over **adding long blockquotes to every** generated `artifacts/*.md` (many are **overwritten** by scripts).
- Add hand-written staleness text only to **durable, hand-edited** docs (e.g. a lane README) where a short line **helps** and will **not** be clobbered.
- **Do not** mechanically edit every generated artifact in one PR; focus on high-signal **documentation** first.

## 8. Future automation

A later change might **validate** or **emit** staleness metadata (e.g. compare `generatedAt` to source mtime, CI guard). **This** document and PR are **documentation-only**: no new automation, no new dashboard, and no change to default generation behavior unless explicitly specified in a future PR.
