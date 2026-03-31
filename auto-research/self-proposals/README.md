# Self Proposals Lane

This lane keeps the Karpathy-style auto-research loop while protecting Grace-Mar's live Record.

## Lifecycle

1. Edit `train.md` only.
2. Run `prepare.py` to validate and score the proposal in a sandbox.
3. If the score is better, archive the result under `accepted/`.
4. When the operator wants a reviewable candidate, run `promote_to_gate.py`.

## Grounding modes

- `grounding_mode: "strict"` is the real operating mode. Strict grounding rejects placeholder or scaffold-style source text before sandbox scoring.
- `grounding_mode: "scaffold"` exists only for local setup and examples. It should not be promoted into the gate.
- `prepare.py` runs with strict grounding by default. Use the scaffold opt-out only when validating the lane itself.

## Protected surfaces

These files must never be edited by the auto-research loop:

- `users/grace-mar/self.md`
- `users/grace-mar/self-archive.md`
- `users/grace-mar/recursion-gate.md`
- `bot/prompt.py`

The only supported path into the Record remains the gate plus `scripts/process_approved_candidates.py`.

## Accepted artifacts

Accepted artifacts are research memory, not approved Record truth.

Each accepted artifact should be read as:

- accepted for research, not approved for Record
- source-first review packet
- scalar and score components for triage
- still subject to explicit operator judgment before promotion

## Promotion

Promotion requires:

- an explicit accepted artifact path
- an explicit operator review note
- non-scaffold grounding
- no prior promotion recorded on the artifact
