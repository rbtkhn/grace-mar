# Doctrine Drift Radar

**Purpose:** catch small doctrinal slips before they harden into new behavior.

The doctrine drift radar is a read-only audit pass over repo files that are especially likely to drift:

- scripts that might start writing governed Record surfaces
- derived artifacts that might quietly claim more authority than they have
- WORK docs that might start speaking as if they can merge
- proposal surfaces that might stop requiring human review

The radar is intentionally narrow. It does not try to prove the whole repo is doctrinally pure. It checks a short list of high-leverage invariants that are easy to regress and expensive to clean up later.

## Files

- `config/doctrine-rules.v1.json` — initial rule set
- `scripts/audit_doctrine_drift.py` — read-only auditor
- `tests/test_doctrine_drift.py` — focused regression tests

## Initial rules

1. No file outside approved scripts may write canonical Record paths.
2. Interface artifacts must keep `recordAuthority = none` and `gateEffect = none`.
3. Portable emulation must keep `mergeAuthority = none`.
4. Workbench receipts must not claim evidence truth.
5. WORK docs must not claim canonical merge authority.
6. Proposal envelopes must require human review.
7. Portable-emulation proposal envelopes must preserve `recordAuthority = none`, `gateEffect = none`, `mergeAuthority = none`, and `requires_human_review = true`.

## Usage

```bash
python3 scripts/audit_doctrine_drift.py
python3 scripts/audit_doctrine_drift.py --json
```

By default the script reads `config/doctrine-rules.v1.json` from the repo root and exits non-zero when it finds violations.

## Detection style

The radar is heuristic by design.

- The canonical-writer rule is an allowlist check over likely Python write paths, not a full program-analysis engine.
- JSON rules look for known envelope or artifact shapes and then verify required constants.
- Text rules are phrase-level drift guards for doctrine pages where wording matters.

That means:

- a clean run is useful, but not absolute proof
- a violation is a review prompt, not automatic truth

The point is early visibility. If doctrine starts drifting, the radar should make the drift easy to see while it is still cheap to correct.

See also: [counterfactual-fork-simulator.md](counterfactual-fork-simulator.md) for the forward-looking companion tool that asks what doctrine drift a proposed change might introduce before it is accepted.
