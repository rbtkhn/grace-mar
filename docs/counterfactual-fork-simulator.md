# Counterfactual Fork Simulator

**Purpose:** Counterfactual Fork Simulator is a scratch-only governance
foresight tool. It simulates the consequences of accepting a proposed
change without applying that change to canonical state.

## What it is not

- not a merge engine
- not a Record writer
- not a replacement for `recursion-gate.md`
- not a contradiction resolver
- not proof that a proposal is safe
- not an autonomous reviewer

## Lifecycle

proposal / proposed change
-> counterfactual simulation input
-> read current repo state
-> estimate affected paths and surfaces
-> check contradiction/doctrine-risk heuristics
-> emit simulation report
-> operator reviews report
-> proposal may be revised, split, deferred, rejected, or routed through existing gate

## Authority model

| Action | Status |
|---|---|
| read current repo | allowed |
| write scratch report | allowed |
| write Record | forbidden |
| write `recursion-gate.md` | forbidden |
| approve proposal | forbidden |
| merge | forbidden |
| resolve contradiction | forbidden |
| recommend next action | allowed |

The simulator may write only advisory output under
`artifacts/counterfactual-simulations/`. A simulation report is
WORK/audit-only and must not be mistaken for evidence, Record,
approval, or a merge receipt.

## Relationship to Doctrine Drift Radar

Doctrine Drift Radar asks:

`Does the current repo already violate doctrine?`

Counterfactual Fork Simulator asks:

`If this change were accepted, what doctrine drift might it introduce?`

They are complementary:

- Doctrine Drift Radar is a current-state audit.
- Counterfactual Fork Simulator is a hypothetical-change preview.

See also: [doctrine-drift-radar.md](doctrine-drift-radar.md).

## Relationship to Portable Emulation

Portable Emulation lets a foreign runtime behave under Grace-Mar boundaries.
Counterfactual Fork Simulator lets Grace-Mar test hypothetical changes before accepting them.

Portable emulation is about bounded downstream behavior.
Counterfactual simulation is about bounded upstream review.

## Relationship to Interface Artifacts

Interface artifacts can be simulated as proposed operator-facing
additions. The simulator may report whether an artifact risks claiming
Record authority, gate authority, or evidence truth.

This keeps interface-artifact review aligned with the existing
non-authority contract rather than letting a prototype silently drift
into governance language it does not possess.

## Failure modes

- simulator treated as approval
- scratch report mistaken for evidence
- proposed change overbroad
- target surfaces unspecified
- contradiction risk hidden by vague summary
- dynamic path mutation missed
- stale repo state used

## How to interpret recommendations

- `accept` = no obvious risk detected in this narrow pass; still not approval
- `revise` = fix wording, scope, or authority-risk language before routing the proposal onward
- `split` = the proposal appears too broad and should become smaller governed changes
- `defer` = the proposal likely needs more narrowing, context, or follow-up before it is worth routing
- `reject` = the proposal appears to violate a core authority boundary
- `needs_review` = the proposal is underspecified, especially around target surfaces

## Scope for Phase 1

Phase 1 is intentionally narrow:

- small proposal-like JSON input
- heuristic consequence preview
- JSON report output
- no repo copy
- no patch application engine
- no autonomous proposal acceptance

This tool exists to make consequence review cheaper and more legible before a human decides what to do next.

## Example input

See
[`../examples/diagnostics/counterfactual-proposal.example.json`](../examples/diagnostics/counterfactual-proposal.example.json)
for a small proposal payload that exercises the Phase 1 input shape
without touching canonical Record paths.
