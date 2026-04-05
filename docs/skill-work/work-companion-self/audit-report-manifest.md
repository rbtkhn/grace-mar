## work-companion-self — Template Diff Report

Companion-self: /Users/robertkuhne/Documents/grace-mar/companion-self
Instance (grace-mar): /Users/robertkuhne/Documents/grace-mar
Paths: companion-self template-manifest.json

### Pull needed (in template, not in instance)
  - scripts/cadence-coffee.py
  - scripts/cadence-dream.py

### Differ (both exist, content differs — review)
  - docs/CONTRADICTION-ENGINE-SPEC.md
  - docs/approval-inbox-spec.md
  - docs/concept.md
  - docs/layer-map.json
  - docs/seed-phase-stages.md
  - docs/skill-work/README.md
  - docs/skill-work/work-cadence/README.md
  - docs/skill-work/work-cadence/harvest-packet-contract.md
  - docs/skill-work/work-cadence/work-cadence-events.md
  - scripts/log_cadence_event.py
  - scripts/session_harvest.py
  - users/_template/recursion-gate.md
  - users/_template/review-queue/README.md
  - users/_template/seed-phase/seed_dossier.md
  - users/_template/seed-phase/seed_intake.json
  - users/_template/self-memory.md
  - users/demo/seed-phase/seed_dossier.md
  - users/demo/seed-phase/seed_intake.json
  - users/demo/seed-phase/work_dev_seed.json

### Expected drift (policy-documented; not a parity defect)
  - **docs/identity-fork-protocol.md** — Grace-mar holds IFP v1.0 full reference spec; companion-self ships the short form with a link to the full spec. Do not overwrite the instance file with the template short form on bulk sync.

Machine list: `docs/skill-work/work-companion-self/expected-template-drift.json`

### Same (no action)
  - bridges/bridge-schema.json
  - config/source-of-truth.json
  - docs/change-review-lifecycle.md
  - docs/change-review-validation.md
  - docs/change-review.md
  - docs/change-types.md
  - docs/conflict-resolution-order.md
  - docs/contradiction-policy.md
  - docs/contradiction-resolution.md
  - docs/evidence-layer.md
  - docs/evidence-to-context-pipeline.md
  - docs/governed-state-layer.md
  - docs/instance-patterns.md
  - docs/long-term-objective.md
  - docs/pipeline/evidence-to-proposal.md
  ... and 92 more

Summary: same=107 differ=19 expected_drift=1 only_template=2 only_instance=0