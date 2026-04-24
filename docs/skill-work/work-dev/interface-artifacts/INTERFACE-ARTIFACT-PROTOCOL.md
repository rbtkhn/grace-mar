# Interface Artifact Protocol

**Status:** WORK-only. **Not** Record, **not** EVIDENCE truth, **not** gate authority.

## Purpose

This protocol defines a lightweight, governance-safe pattern for **generated operator-facing interface artifacts**: dashboards, visualizers, prototype pages, review cockpits, strategy-notebook views, and small HTML/React/SVG/CLI tools.

It does **not** create a new app platform. It creates a governed way to say:

- what the artifact is
- what it reads
- what it generates
- how it should be inspected
- what it can never claim or mutate

## What counts as an interface artifact

An interface artifact is a **derived operator-facing surface** that helps the operator:

- inspect structure or state
- compare candidates or paths
- navigate a lane or notebook
- orient before judgment
- rehearse or preview a workflow before deciding whether to formalize it

Common examples:

- generated Markdown dashboards
- HTML visualizers
- React prototypes
- SVG maps
- CLI views
- review cockpits
- comparison views

### Strategy views

Within this protocol, **strategy views** are a narrow subclass of interface artifacts: derived views that help the operator navigate notebook structure, recent movement, or cross-file relationships before judgment.

They do **not** replace canonical notebook judgment. Strategy-notebook remains markdown-canonical, with derived interface artifacts around it for orientation, inspection, and navigation.

Current anchors:

- [../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md](../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md)
- [../../work-strategy/strategy-notebook/strategy-console/README.md](../../work-strategy/strategy-notebook/strategy-console/README.md)
- [../../work-strategy/strategy-notebook/GRAPH-SCHEMA.md](../../work-strategy/strategy-notebook/GRAPH-SCHEMA.md)

## What does not count

These are **not** interface artifacts:

- canonical Record surfaces
- EVIDENCE entries
- gate blocks or review-queue truth
- merge receipts
- action receipts
- a notebook's primary judgment surface when that judgment is already defined elsewhere

For strategy-notebook specifically, **`strategy-page`** blocks and `days.md` are **canonical markdown judgment**, not interface artifacts.

## Lifecycle

1. **Intent**  
   Decide what the operator needs to inspect, compare, or navigate.

2. **Source inputs**  
   Identify the notebook files, derived JSON, dashboards, or other repo surfaces the artifact reads.

3. **Generated artifact**  
   Produce a derived view or prototype under a WORK-only path.

4. **Inspection path**  
   If behavior matters, inspect the artifact through Workbench or a comparable bounded runtime path.

5. **Receipt path**  
   Choose the right audit channel for what happened.

6. **Operator decision**  
   Keep, revise, discard, inspect further, or manually promote through an existing governed path.

7. **Optional governed follow-up**  
   If the artifact points to a real next move, stage that move through the normal lane or gate process rather than giving the artifact authority by itself.

## Required metadata block

Each interface artifact should declare a compact metadata block with at least:

- `artifactId`
- `title`
- `artifactKind`
- `sourceInputs`
- `generatedPaths`
- `intendedUse`
- `mutationScope`
- `canonicalRecordAccess`
- `recordAuthority`
- `gateEffect`
- `inspectionStatus`
- `relatedWorkbenchReceipt`
- `typicalNextStep`

See [INTERFACE-ARTIFACT-SPEC.md](INTERFACE-ARTIFACT-SPEC.md) for the suggested JSON shape.

## Allowed artifact kinds

- `markdown-dashboard`
- `html-visualizer`
- `react-prototype`
- `svg-map`
- `cli-view`
- `review-cockpit`
- `comparison-view`
- `other-work-ui`

## Three audit channels

Keep the audit paths distinct:

- **Interface artifact metadata** classifies the artifact: what it is, what it reads, what it generates, and what authority it does not have.
- **Workbench receipt** records that a generated UI or tool ran and was inspected.
- **Strategy notebook trace receipt** records notebook-affecting reads and writes for strategy tooling.

Rule of thumb:

- if an artifact is **view-only**, it may have interface-artifact metadata and optionally a Workbench receipt
- if a command also **writes notebook files**, it should still use the existing strategy trace contract
- interface-artifact metadata is **not** a replacement for either receipt family

Relevant specs:

- [../workbench/WORKBENCH-RECEIPT-SPEC.md](../workbench/WORKBENCH-RECEIPT-SPEC.md)
- [../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-TRACE-CONTRACT.md)

## Storage rule

Use the dual-path rule:

- store **new cross-lane prototypes** under `artifacts/work-dev/interface-artifacts/`
- keep **established lane-specific derived artifacts** in their existing bucket, such as `artifacts/work-strategy/strategy-notebook/`

The storage path does **not** change the artifact's authority. Both paths remain WORK-only and derived.

## Forbidden uses

An interface artifact must **not** be used as:

- canonical truth
- evidence truth
- direct merge authority
- automatic gate staging
- policy override
- silent proof of a user-facing or external claim

## Decision vocabulary

Recommended operator decisions:

- `discard`
- `revise`
- `inspect-in-workbench`
- `keep-as-derived-artifact`
- `convert-to-scripted-dashboard`
- `create-gate-candidate-manually`
- `implement-as-work-dev-tool`

## Doctrine

- `recordAuthority` must remain `none`
- `gateEffect` must remain `none`
- interface artifacts may inspire a candidate, but cannot stage or approve one by themselves
- screenshots, logs, and demos prove **artifact behavior under stated conditions**, not external truth

## First-class example

Use the strategy-notebook visualizer pilot as the primary worked example of this pattern:

- [../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md](../../work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md)

It already makes the key boundaries legible:

- structure/path truth, not strategic truth
- `recordAuthority: none`
- `gateEffect: none`
- Workbench as the inspection path
