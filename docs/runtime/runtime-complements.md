# Runtime Complements

## Status

WORK / runtime / non-canonical / optional.

## Purpose

**Runtime complements** are external or adjunct systems (e.g. future Letta, Mem0, OpenMemory, Thoth-style local tools, or bot runtimes) that may improve **live** interaction, quick recall, agent continuity, session summarization, or operator UX. They do **not** hold authority over Grace-Mar’s canonical **Record**.

## Core rule

> External runtimes may remember for themselves.  
> Grace-Mar remembers only through the **gate** ([`recursion-gate.md`](../../users/grace-mar/recursion-gate.md) → companion-approved merge; see [AGENTS.md](../../AGENTS.md)).

Runtime complements may **accelerate** context, continuity, and interaction. They may not become **memory**, **evidence**, or **identity** until **staged**, **reviewed**, and **merged** through that gate.

## What runtime complements may do

They may:

- consume **approved export bundles** produced by [export_runtime_context.py](../../scripts/runtime/export_runtime_context.py) (or operator-approved copies)
- maintain their own **ephemeral** or **vendor-local** state outside canonical paths
- produce **summaries**, **observations**, **retrieval hints**, and **receipts**
- produce **candidate** memory suggestions (still candidates until gated)
- produce **operator-review drafts** as plain files or JSON in the runtime complement paths only
- help route proposed actions through an **approval** step (pattern only; no bypass of Grace-Mar’s gate)

## What runtime complements may not do

They may not:

- edit **SELF** (`self.md`, SELF-knowledge, identity tables)
- edit **SELF-LIBRARY** / CIV-MEM in canonical form
- edit **SKILLS** (capability evidence files)
- edit **EVIDENCE** (`self-archive.md` and gated evidence) directly
- edit **`recursion-gate.md`** except through normal operator + companion **approve** + `process_approved_candidates` (or equivalent) workflows
- **merge** or auto-process candidates without companion approval
- rewrite **`bot/prompt.py`** or Voice runtime policy
- create **canonical facts** by silent update
- treat **runtime** or **vendor** memory as Grace-Mar memory
- **delete** or **prune** raw sources, Record files, or strategy notebook primary surfaces
- **bypass** human/operator review for anything that should be durable in the Record

## Allowed reads

Conservative, explicit surfaces only (no whole-repo scans of `users/<id>/` Record trees unless the operator or an approved export script names paths):

- **Approved export bundles** under [`runtime/runtime-complements/exports/`](../../runtime/runtime-complements/exports/) (JSON produced by the export script)
- **Selected docs** included via `--include-doc` on the export script (operator-chosen, repo-relative paths)
- **Selected WORK** docs (e.g. strategy notebook orientation, work-strategy specs) when explicitly **included** in a bundle
- **Strategy notebook** derived or orientation docs (e.g. [strategy-console README](../skill-work/work-strategy/strategy-notebook/strategy-console/README.md)) only when path-listed in a bundle
- Public **doctrine** / **architecture** files used as membrane context, when explicitly included

Direct reads of **Record** files by an external process should be avoided; prefer **export bundles** and operator-approved file lists. This doc does not grant permission to scrape `users/` for bulk ingest.

## Allowed writes

Runtime complements (and the import script in this repo) may write **only** to:

- `runtime/runtime-complements/inbox/` — imported observations (JSON)
- `runtime/runtime-complements/receipts/` — import receipts (JSON, schema: [`runtime-complement-receipt.v1.json`](../../schema-registry/runtime-complement-receipt.v1.json))
- `runtime/runtime-complements/exports/` — **export** bundles (JSON) from the export script
- `runtime/runtime-complements/examples/` — committed **examples** only (not live vendor secrets)

They may **not** write into **canonical Record** paths (`users/<id>/self.md`, `self-archive.md`, `self-skills.md`, `self-library.md` contents, `recursion-gate.md` except by normal human-driven edits, `bot/prompt.py`, etc.).

## Export path

**Grace-Mar–approved context** → **export bundle** (JSON) under `exports/` → consumed by a runtime complement (off-repo or local harness).

See [`scripts/runtime/export_runtime_context.py`](../../scripts/runtime/export_runtime_context.py).

## Import path

**Runtime complement** output (JSON) → [import_runtime_observation.py](../../scripts/runtime/import_runtime_observation.py) → **inbox** file + **receipt** → **human/operator review** → optional **manual** staging as `recursion-gate.md` **candidates** → **companion approval** → existing merge path.

No new merge API: promotion follows the same **gated pipeline** as any other profile or evidence change.

## Receipt requirement

Every imported runtime observation should have a **receipt** (see schema) with at least:

- **source** runtime label (`letta`, `mem0`, `openmemory`, `thoth`, `other`, …)
- **source session / conversation id** if available (optional `source_session_id` in receipt)
- **timestamp** (`generated_at`)
- **import mode** (e.g. observation vs session summary)
- **files written** (inbox + receipt paths)
- **canonical surfaces not touched** — `canonical_surfaces_touched: false` for compliant imports
- **promotion status** — default `runtime_only` until a human moves toward gate staging
- **human review required** — default **true**

## Vendor examples (non-binding)

| Example | Role | Note |
|--------|------|------|
| **Letta** | Stateful session runtime, bot continuity, multi-turn context | Example only; **no** live integration in the membrane v1 PR |
| **Mem0 / OpenMemory** | Fast recall, personalization **cache** outside Record | Example only; **verify** any suggestion against on-disk **WORK/Record** |
| **Thoth-style local assistant** | Local-first “propose then approve” UX pattern | **Inspiration** for routing; does **not** change Grace-Mar’s **recursion-gate** mechanics |

These are **illustrations**, not dependencies or endorsements. Future adapters may call the same
import/export CLIs with JSON payloads.

**Letta adapter example:** [bridges/runtime-complements/letta/](../../bridges/runtime-complements/letta/)
prepares Letta seed files and imports Letta summaries through the runtime complement membrane.

## Boundary statement

Runtime complements may **accelerate** context, continuity, and interaction. They may not become **memory**, **evidence**, or **identity** until **staged**, **reviewed**, and **merged** through Grace-Mar’s **existing gate**.

**See also:** [runtime-vs-record.md](../runtime-vs-record.md) · [runtime/complements README](../../runtime/runtime-complements/README.md)
