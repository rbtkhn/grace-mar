# work-dev — claim–proof standard

**Purpose:** Any capability marked **`implemented`** in `artifacts/work-dev/capability-status.json` must cite **at least one** proof artifact.

## Acceptable proof kinds

1. **Automated test** — `tests/test_*.py` name or path.
2. **Runnable script + exit 0** — documented command in capability notes.
3. **Manual verification receipt** — operator log entry or dated markdown in [verification-runs/](verification-runs/).
4. **Demo artifact** — linked file under `docs/` or `research/` with explicit scope.

## Not sufficient

- Prose in README alone (unless the README embeds a command that reproduces behavior).
- “Implemented” in dashboard JSON without doc cross-link.

## Ledger

Optional rows in `artifacts/work-dev/proof_ledger.json` ([proof_ledger.schema.json](../../schemas/work_dev/proof_ledger.schema.json)).

Run [verify_work_dev_claims.py](../../../scripts/verify_work_dev_claims.py) locally or in CI advisory mode.
