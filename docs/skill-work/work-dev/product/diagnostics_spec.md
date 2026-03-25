# Diagnostics product spec (work-dev)

Repeatable **boundary / provenance / continuity** audit for partner conversations.

- **Inputs:** control plane YAML, optional `pipeline-events.jsonl`, operator checklist answers.
- **Outputs:** JSON findings + scored markdown report (`scripts/work_dev/run_diagnostics.py`).
- **Dimensions:** truth-source clarity, identity vs Library separation, continuity explicitness, provenance across handback, lane discipline, observability maturity.

See `findings_taxonomy.yaml`, `maturity_scorecard.yaml`, and `examples/diagnostics/`.
