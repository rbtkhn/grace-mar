# Portable Emulation Proposal Envelope v1

Portable emulation may return durable-change suggestions in a proposal envelope such as:

```json
{
  "type": "emulation-proposal-envelope-v1",
  "source_bundle": {
    "fork_id": "...",
    "bundle_version": "...",
    "exported_at": "...",
    "checksum": "..."
  },
  "proposal_kind": "record_change | contradiction | skill_update | evidence_addition | library_update | other",
  "target_surfaces": [],
  "source_observation": "",
  "evidence_refs": [],
  "proposed_change": "",
  "contradiction_check": {
    "status": "none | possible | likely | unknown",
    "active_claim_refs": [],
    "notes": ""
  },
  "authority": {
    "recordAuthority": "none",
    "gateEffect": "none",
    "mergeAuthority": "none",
    "proposalAuthority": "stage-only"
  },
  "requires_human_review": true
}
```

## Interpretation rules

- This envelope is **not** an approved change.
- This envelope is **not** a merge receipt.
- This envelope is **not** Record.
- Importing it into Grace-Mar still **REQUIRES** validation and human review.

## Required behavior

- Proposal envelopes **MUST** preserve source bundle metadata.
- Proposal envelopes **MUST NOT** imply approval.
- Proposal envelopes **MUST NOT** claim merge authority.
