# Auto-Research

This directory holds transcript-faithful auto-research scaffolds adapted to Grace-Mar's governance model.

## Core rule

Auto-research may optimize proposals about the Record. It may not edit the live Record directly.

That means:

- `train.md` is the only editable surface inside a lane.
- `prepare.py` is protected and evaluates proposals in a sandbox.
- winning experiments are archived as accepted proposal artifacts
- promotion to `users/grace-mar/recursion-gate.md` is explicit and reviewable

The live merge path remains unchanged:

1. stage a pending candidate
2. review in the gate
3. approve
4. merge with `scripts/process_approved_candidates.py`

## First lane

`self-proposals/` is the first lane. It optimizes gate-ready proposal drafts for SELF-facing changes without touching `users/grace-mar/self.md`.
