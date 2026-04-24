# Interface Artifact Spec

**Status:** Suggested v1 metadata shape for interface artifacts. The generator and validator scripts enforce this shape for routine use.

## Purpose

This spec defines a small JSON metadata shape for interface artifacts so the operator, assistant, and future tooling can see the same basic contract:

- what the artifact is
- what it reads
- what it generates
- what authority it does or does not have
- what should happen next

## Suggested JSON shape

```json
{
  "artifactId": "iface-20260424-example",
  "title": "Strategy Notebook Structure Map",
  "artifactKind": "html-visualizer",
  "status": "draft",
  "sourceInputs": [
    "docs/skill-work/work-strategy/strategy-notebook/"
  ],
  "generatedPaths": [
    "artifacts/work-strategy/strategy-notebook/strategy-notebook-visualizer.html"
  ],
  "intendedUse": "Help the operator inspect strategy-notebook structure before deciding whether to revise docs or scripts.",
  "mutationScope": "runtime-only",
  "canonicalRecordAccess": "none",
  "recordAuthority": "none",
  "gateEffect": "none",
  "inspectionStatus": "not-inspected",
  "relatedWorkbenchReceipt": null,
  "typicalNextStep": "inspect-in-workbench",
  "sourceContractRef": "docs/skill-work/work-strategy/strategy-notebook/demo-runs/workbench-visualizer/README.md"
}
```

## Field notes

| Field | Type | Meaning |
|------|------|---------|
| `artifactId` | string | Stable id for the artifact instance or concept. |
| `title` | string | Human-facing title. |
| `artifactKind` | string | Interface artifact class. See allowed values below. |
| `status` | string | Current lifecycle status. |
| `sourceInputs` | string[] | Repo-relative paths the artifact reads from. |
| `generatedPaths` | string[] | Repo-relative paths the artifact generates or rewrites. |
| `intendedUse` | string | What the operator should use the artifact for. |
| `mutationScope` | string | Usually `runtime-only` for interface artifacts. |
| `canonicalRecordAccess` | string | `none` or `read-only`. |
| `recordAuthority` | string | Must remain `none`. |
| `gateEffect` | string | Must remain `none`. |
| `inspectionStatus` | string | Whether the artifact has been inspected yet. |
| `relatedWorkbenchReceipt` | string or null | Optional link to a Workbench receipt path or id. |
| `typicalNextStep` | string | Likely operator action after inspection. |
| `sourceContractRef` | string (optional) | Governing doc or contract for the artifact. |

## Allowed `artifactKind` values

- `markdown-dashboard`
- `html-visualizer`
- `react-prototype`
- `svg-map`
- `cli-view`
- `review-cockpit`
- `comparison-view`
- `other-work-ui`

## Allowed `status` values

- `draft`
- `inspected`
- `revised`
- `discarded`
- `promoted-to-scripted-dashboard`
- `superseded`

## Suggested `inspectionStatus` values

- `not-inspected`
- `inspected-manually`
- `inspected-in-workbench`
- `inspection-not-needed`

## Validation rules

- `recordAuthority` must be `"none"`
- `gateEffect` must be `"none"`
- `canonicalRecordAccess` must be `"none"` or `"read-only"`
- `mutationScope` must not imply canonical Record writing
- `generatedPaths` should be a non-empty list
- `sourceInputs` should be a list, even when there is only one path
- `artifactKind` should come from the allowed enum
- `status` should come from the allowed enum

## Storage guidance

`generatedPaths` may use either storage pattern:

- `artifacts/work-dev/interface-artifacts/` for new cross-lane prototypes
- an established lane-specific derived bucket when that lane already has one, such as `artifacts/work-strategy/strategy-notebook/`

Use the storage pattern that matches the artifact's real home. The path does not change authority; both remain WORK-only and derived.

## Strategy-notebook compatibility

This spec fits the current strategy-notebook artifact family:

- visualizer pilot outputs
- Strategy Console outputs
- graph-derived JSON or companion views

Canonical strategy judgment still lives in:

- `experts/<id>/thread.md` `strategy-page` blocks
- `chapters/YYYY-MM/days.md`

See:

- [../../work-strategy/strategy-notebook/README.md](../../work-strategy/strategy-notebook/README.md)
- [../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md)

## Tooling

Current helpers:

- `scripts/work_dev/new_interface_artifact.py`
- `scripts/work_dev/validate_interface_artifact.py`
- `tests/test_interface_artifact_protocol.py`

Those tools enforce the doctrine in this spec; they do not expand the artifact's authority.
