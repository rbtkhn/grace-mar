# Interface Artifacts

**Status:** WORK-only v1. **Markdown-first, repo-native, additive.**

Interface artifacts are **generated operator-facing views or prototypes** used to inspect, compare, navigate, or decide. They are a lightweight protocol for turning an idea into an **inspectable artifact** without confusing that artifact with canonical truth.

This is **not** a new app platform. It is a named pattern for generated interfaces that already fit Grace-Mar's runtime-vs-Record boundary.

## Core doctrine

Interface artifacts:

- may help the operator **inspect**, **compare**, **navigate**, or **decide**
- are **WORK-only** and **derived**
- are **not** canonical Record surfaces
- are **not** EVIDENCE truth
- are **not** a merge path or gate authority
- may later inspire a gate candidate, scripted dashboard, or committed tool, but only through existing governed paths

Anchor sentence:

`strategy-notebook is markdown-canonical, with a growing family of derived interface artifacts for orientation, inspection, and navigation; those artifacts are WORK-only and non-canonical unless separately promoted through existing governed paths.`

## How this fits

### Relation to Workbench

The **Interface Artifact Protocol** defines the **object and pattern**: what an artifact is, what it reads, what it generates, and what authority it does or does not have.

The **Workbench Harness** remains the **inspection layer**: generate -> run -> inspect -> revise -> workbench receipt -> operator review. Workbench receipts prove **artifact behavior under stated conditions**, not external truth.

See:

- [../workbench/README.md](../workbench/README.md)
- [../workbench/WORKBENCH-RECEIPT-SPEC.md](../workbench/WORKBENCH-RECEIPT-SPEC.md)

### Relation to strategy-notebook

Strategy-notebook remains **markdown-canonical**. Its canonical judgment lives in `strategy-page` blocks and `days.md`, per [../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md).

Interface artifacts name the **derived orientation layer** around that notebook: visualizers, console views, graph-based maps, cockpit mockups, and similar operator-facing surfaces.

Current strategy-facing anchors:

- [../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md](../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md)
- [../../work-strategy/strategy-notebook/strategy-console/README.md](../../work-strategy/strategy-notebook/strategy-console/README.md)
- [../../work-strategy/strategy-notebook/GRAPH-SCHEMA.md](../../work-strategy/strategy-notebook/GRAPH-SCHEMA.md)

### Relation to operator dashboards

Operator dashboards are a **stable scripted subclass** of interface artifacts. Their generated Markdown remains **derived and non-canonical**. Existing dashboard builders remain authoritative for those files.

See [../../../operator-dashboards.md](../../../operator-dashboards.md).

### Relation to Claude Surface Contract

Interface artifacts should declare **surface type**, **purpose**, **inputs**, **outputs**, **mutation scope**, **canonical Record access**, and **typical next step** using the same vocabulary as the [../../../claude-surface-contract.md](../../../claude-surface-contract.md).

## Storage rule

Use one clear default:

- **New cross-lane prototypes** default to `artifacts/work-dev/interface-artifacts/`
- **Established lane-specific derived artifacts** stay in their existing lane bucket, such as `artifacts/work-strategy/strategy-notebook/`

## Script support

- `scripts/work_dev/new_interface_artifact.py` — create interface-artifact metadata JSON with safe defaults
- `scripts/work_dev/validate_interface_artifact.py` — validate one metadata file; exits non-zero on errors

These scripts do **not** stage to the gate, do **not** merge into the Record, and do **not** create authority beyond the metadata they write.

## Typical examples

- strategy-notebook visualizer
- gate-review cockpit mockup
- self-library map
- review dashboard variant
- history/strategy thread browser
- moonshot orchestration map

## Non-goals

- creating a new canonical surface
- bypassing `recursion-gate.md`
- proving external claims through screenshots or UI state
- replacing lane-specific doctrine such as strategy-notebook architecture

## Rollout note

This v1 stays intentionally small: doctrine, examples, light tooling, and focused tests. It names the pattern without turning interface artifacts into a new app framework.
