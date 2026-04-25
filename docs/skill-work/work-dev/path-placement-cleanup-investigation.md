# Path Placement Cleanup Investigation

## Purpose

Record the factual outcome of the Path and Schema Placement Cleanup
investigation so follow-up formatting work stays aligned with the current
checkout rather than a stale or mismatched file list.

## Reported artifacts checked

### `docs/path-and-schema-placement.md`

- Not present in the current checkout.
- No git history was found for this exact path.
- No renamed or superseding markdown file with the same stem was found by
  repo-wide filename search.

### `scripts/audit_path_friction.py`

- Not present in the current checkout.
- No git history was found for this exact path.
- No renamed or superseding script with the same stem was found by
  repo-wide filename or content search.

### `tests/test_path_friction_audit.py`

- Not present in the current checkout.
- No git history was found for this exact path.
- No renamed or superseding test file with the same stem was found by
  repo-wide filename or content search.

## Current interpretation

Within this checkout, the three reported placement/path-friction artifacts
should be treated as absent rather than merely minified. The most likely
explanations are:

- they were described from another checkout or branch state,
- they were expected but never landed here, or
- they were discussed in planning/review language without becoming on-disk
  repo artifacts.

This note does **not** claim which of those explanations is true beyond
what the current checkout can prove.

## Formatting scope that remains valid

The following files are already line-broken and did not need the suspected
raw-view rescue:

- [`known-gaps.md`](known-gaps.md)
- [`../../../config/agent-surfaces.v1.json`](../../../config/agent-surfaces.v1.json)
- [`../../../config/doctrine-rules.v1.json`](../../../config/doctrine-rules.v1.json)

The review-hostile surfaces actually confirmed in this checkout were the
long markdown tables in:

- [`../../diagnostics-and-governance-tools.md`](../../diagnostics-and-governance-tools.md)
- [`diagnostics-control-plane.md`](diagnostics-control-plane.md)

## Boundary

This investigation note is factual and local to the current checkout. It is
not a recovery spec, not a doctrine file, and not evidence that the missing
artifacts should now be recreated automatically.
