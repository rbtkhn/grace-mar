# Authority Values

## Purpose

Grace-Mar uses repeated authority fields to prevent derived artifacts,
diagnostics, foreign runtimes, and runtime observations from being
mistaken for canonical Record updates or merge authority.

This file defines the shared vocabulary. It does not grant authority and
does not replace schemas or validation scripts.

## Core rule

Only the governed merge path may update canonical Record.

Diagnostics, simulations, receipts, interface artifacts, portable
emulation bundles, and agent registries may inspect, warn, stage, or
propose depending on their lane, but they do not approve or merge.

## Naming note

Grace-Mar currently uses two naming styles for closely related
authority-boundary fields:

- camelCase in interface-artifact, portable-emulation, and
  counterfactual-simulation surfaces
- snake_case in some registry and runtime-policy surfaces such as
  `canonical_record_access`, `merge_authority`, `gate_effect`, and
  `requires_human_review`

That split is currently intentional. This reference defines the shared
vocabulary, not a forced rename.

## Fields

### `recordAuthority`

Meaning:
Whether an artifact, tool, or output may create or modify canonical
Record.

Allowed values:

- `none`

Notes:
For current diagnostics, control-plane artifacts, interface artifacts,
portable emulation bundles, and workbench receipts, this must remain
`none`.

### `gateEffect`

Meaning:
Whether an artifact, tool, or output changes gate state.

Allowed values:

- `none`
- `stage-only`
- `advisory-only`

Notes:
Most diagnostics should be `none` or `advisory-only`. Proposal-return
envelopes may be `stage-only` only when they explicitly produce material
for later review.

### `mergeAuthority`

Meaning:
Whether an artifact, tool, or output may approve or merge durable
changes.

Allowed values:

- `none`

Notes:
Foreign runtimes, diagnostics, simulations, workbench receipts, and
interface artifacts must not have merge authority.

### `canonicalRecordAccess`

Meaning:
Whether a runtime or tool can read canonical Record context.

Allowed values:

- `none`
- `read-only`
- `write-forbidden`

Notes:
`write-forbidden` means explicitly forbidden to write, even if the
surface can read or reference Record context. Some current schema
surfaces only use the narrower subset `none | read-only`; this reference
records the broader shared vocabulary.

### `proposalAuthority`

Meaning:
Whether an artifact, tool, or output may produce proposal material for
human review.

Allowed values:

- `none`
- `stage-only`
- `proposal-only`

Notes:
Proposal authority is not merge authority.

### `contradictionAuthority`

Meaning:
Whether an artifact, tool, or output may detect, surface, or resolve
contradictions.

Allowed values:

- `none`
- `surface-only`
- `proposal-only`

Notes:
`proposal-only` means a surface may emit a proposed contradiction
resolution for review, not decide canonical resolution.

### `workLaneAuthority`

Meaning:
Whether a runtime or tool may create non-canonical WORK observations or
scratch notes.

Allowed values:

- `none`
- `local-runtime-only`
- `work-only`

Notes:
WORK is not Record.

### `simulationOnly`

Meaning:
Whether a report is explicitly counterfactual or advisory.

Allowed values:

- `true`

Notes:
`simulationOnly=true` means not evidence, not approval, and not Record.

### `requires_human_review`

Meaning:
Whether material must be reviewed by a human before durable
incorporation.

Allowed values in the proposal-envelope / external-runtime-return
surfaces covered by this reference:

- `true`

Notes:
For proposal envelopes and external-runtime returns, this must be
`true`. Other runtime policy and execution-receipt surfaces may use
broader boolean or nullable forms; those local validators remain
authoritative for their own contracts.

## Authority ladder

1. read-only audit
2. advisory scratch report
3. derived artifact
4. receipt
5. proposal envelope
6. gate candidate
7. approved merge

Levels 1-5 are not approval.

Level 6 is pending review.

Only level 7 updates canonical Record.

## Common safe combinations

### Interface artifact metadata

- `recordAuthority: none`
- `gateEffect: none`
- `canonicalRecordAccess: none`

### Workbench receipt

- `recordAuthority: none`
- `gateEffect: none`
- evidence-truth boundary language must remain explicit

### Portable emulation bundle

- `recordAuthority: none`
- `gateEffect: none`
- `mergeAuthority: none`
- `proposalAuthority: stage-only`
- `contradictionAuthority: proposal-only`
- `workLaneAuthority: local-runtime-only`

### Counterfactual simulation report

- `recordAuthority: none`
- `gateEffect: none`
- `mergeAuthority: none`
- `simulationOnly: true`

### Agent surface registry entry

- `canonical_record_access: none | read-only | write-forbidden`
- `merge_authority: none`
- `gate_effect: none | stage-only | advisory-only`

## Common unsafe combinations

- `mergeAuthority: approve`
- `recordAuthority: write`
- `gateEffect: merge`
- `simulationOnly: false` for a counterfactual report
- `requires_human_review: false` for a proposal return
- foreign runtime with canonical write authority
- workbench receipt claiming evidence truth

## Non-goals

- not a dynamic compiler
- not a schema replacement
- not a new authority layer
- not a merge path
- not a gate
- not a Record surface

## See also

- [`portability/emulation/emulation-bundle-schema.v1.json`](portability/emulation/emulation-bundle-schema.v1.json)
- [`../schema-registry/counterfactual-simulation-report.v1.json`](../schema-registry/counterfactual-simulation-report.v1.json)
- [`../config/agent-surfaces.v1.json`](../config/agent-surfaces.v1.json)
