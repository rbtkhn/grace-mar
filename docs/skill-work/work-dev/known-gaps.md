# Work-Dev Known Gaps

## Purpose

This file records small inefficiencies, partial implementations, review friction, and hardening opportunities in the `work-dev` lane. It is not a doctrine file, not a gate queue, not a commitment to implement everything, and not approval or Record. It helps operators and coding agents choose small safe follow-up PRs.

## Scope

Include:
- diagnostics/control-plane seams
- formatting/review ergonomics
- CI and local-runner gaps
- authority-boundary hardening
- documentation discoverability
- naming/path friction
- schema duplication
- examples/smoke-test gaps
- agent-surface registry gaps

Exclude:
- canonical Record changes
- recursion-gate decisions
- broad strategy doctrine
- major architecture rewrites
- speculative product roadmap items

## Gap format

Use a simple repeatable format:

### GAP-WD-001 — Title

Status: open
Type: formatting | docs | test | CI | schema | authority | registry | naming | example | ergonomics
Severity: low | medium | high
Affected paths:
- path
Issue:
Short description.
Why it matters:
Short explanation.
Suggested next PR:
Short action.
Do not:
Guardrails.

### GAP-WD-001 — Pretty-format diagnostics and control-plane files

Status: open
Type: formatting
Severity: medium
Affected paths:
- `config/agent-surfaces.v1.json`
- `config/doctrine-rules.v1.json`
- `schema-registry/counterfactual-simulation-report.v1.json`
- `schema-registry/emulation-bundle-envelope.v1.json`
- `scripts/simulate_counterfactual_fork.py`
- `scripts/work_dev/audit_agent_sprawl.py`
- `tests/test_counterfactual_fork_simulator.py`
- `tests/test_agent_sprawl_control_plane.py`
Issue:
Several new governance/control-plane files are compressed into very long lines, making diffs, traceback line numbers, reviews, and future agent edits harder.
Why it matters:
These files carry important boundary logic; reviewability is part of governance.
Suggested next PR:
Formatting-only pass over recent diagnostics/control-plane files.
Do not:
Change behavior, schemas, authority values, or doctrine.

### GAP-WD-002 — Keep diagnostics map current

Status: open
Type: docs
Severity: low
Affected paths:
- `docs/diagnostics-and-governance-tools.md`
- `docs/skill-work/work-dev/diagnostics-control-plane.md`
- `docs/skill-work/work-dev/README.md`
Issue:
New diagnostics tools may be added without updating the map.
Why it matters:
The map prevents future agents from rediscovering tools piecemeal.
Suggested next PR:
Add a checklist note: any new diagnostic/control-plane tool should update both maps.
Do not:
Turn the map into a second README.

### GAP-WD-003 — Deterministic diagnostics should stay secret-free

Status: open
Type: CI
Severity: medium
Affected paths:
- `scripts/run_deterministic_diagnostics.py`
- `.github/workflows/test.yml`
- `.github/workflows/governance.yml`
Issue:
Deterministic diagnostics must remain separate from API-key harnesses.
Why it matters:
Doctrine, agent-sprawl, and counterfactual smoke checks should be runnable by any contributor or agent without secrets.
Suggested next PR:
Confirm CI runs deterministic diagnostics in a non-secret job.
Do not:
Add `OPENAI_API_KEY` or external service dependency.

### GAP-WD-004 — Counterfactual simulator needs more examples

Status: open
Type: example
Severity: low
Affected paths:
- `examples/diagnostics/`
- `docs/counterfactual-fork-simulator.md`
Issue:
Only one example proposal exists; it may not cover dangerous authority escalation or docs-only changes.
Why it matters:
Examples teach future agents how to use the simulator safely.
Suggested next PR:
Add two examples:
1. clean docs-only proposal
2. dangerous merge-authority proposal
Do not:
Make examples look like approved changes.

### GAP-WD-005 — Counterfactual artifact directory needs README

Status: open
Type: docs
Severity: low
Affected paths:
- `artifacts/counterfactual-simulations/`
Issue:
Scratch simulation outputs need local boundary language.
Why it matters:
Reports are advisory, not evidence, not Record, and not approval.
Suggested next PR:
Add `artifacts/counterfactual-simulations/README.md`.
Do not:
Treat generated simulation reports as durable truth.

### GAP-WD-006 — Agent surface registry exemptions should be visible

Status: open
Type: registry
Severity: medium
Affected paths:
- `config/agent-surfaces.v1.json`
- `docs/skill-work/work-dev/agent-sprawl-control-plane.md`
Issue:
Some implemented or partial surfaces may need exemptions from capability-contract or receipt rules.
Why it matters:
Exemptions are useful during migration but should not become invisible debt.
Suggested next PR:
Add explicit `exempt_reason` and `review_after` fields for exempted entries.
Do not:
Fail legacy surfaces abruptly without migration path.

### GAP-WD-007 — Agent surface registry should produce a human-readable table

Status: open
Type: ergonomics
Severity: low
Affected paths:
- `config/agent-surfaces.v1.json`
- `artifacts/work-dev/`
- `docs/skill-work/work-dev/agent-sprawl-control-plane.md`
Issue:
The JSON registry is machine-readable but not ideal for operator review.
Why it matters:
Agent sprawl is easier to manage when humans can scan a table.
Suggested next PR:
Add a script to render the agent surface registry to a Markdown artifact.
Do not:
Make the generated table authoritative over the JSON registry.

### GAP-WD-008 — Authority constants are repeated

Status: open
Type: schema
Severity: medium
Affected paths:
- `schema-registry/`
- `config/doctrine-rules.v1.json`
- `docs/portability/emulation/`
- `docs/skill-work/work-dev/interface-artifacts/`
- `scripts/`
Issue:
Values like `recordAuthority=none`, `gateEffect=none`, `mergeAuthority=none`, and `simulationOnly=true` are repeated across schemas, docs, scripts, and tests.
Why it matters:
Repeated authority constants can drift.
Suggested next PR:
Consider a small authority-values reference file or explicit note identifying source-of-truth constants.
Do not:
Over-engineer a dynamic schema compiler in the first pass.

### GAP-WD-009 — Portable emulation schemas need usage clarification

Status: open
Type: docs
Severity: low
Affected paths:
- `docs/portability/emulation/emulation-bundle-schema.v1.json`
- `schema-registry/emulation-bundle-envelope.v1.json`
- `docs/portability/emulation/README.md`
Issue:
There is a docs-facing rich schema and a narrower operational envelope schema.
Why it matters:
Future agents may not know which schema to validate against.
Suggested next PR:
Add a "which schema to use when" section.
Do not:
Delete either schema without migration.

### GAP-WD-010 — Doctrine Drift Radar severity levels

Status: open
Type: authority
Severity: medium
Affected paths:
- `config/doctrine-rules.v1.json`
- `scripts/audit_doctrine_drift.py`
- `tests/test_doctrine_drift.py`
Issue:
Doctrine rules could benefit from explicit severity: error vs warning.
Why it matters:
Not all drift signals should fail CI; some should inform review.
Suggested next PR:
Add an optional severity field and preserve current behavior for existing hard-error rules.
Do not:
Weaken existing hard authority-boundary checks.

### GAP-WD-011 — Work-dev README is becoming overloaded

Status: open
Type: docs
Severity: medium
Affected paths:
- `docs/skill-work/work-dev/README.md`
Issue:
The `work-dev` README now functions as mission statement, index, operations catalog, research map, and product-positioning index.
Why it matters:
A single large table makes important operational tools easy to bury.
Suggested next PR:
Split or group contents into sections:
- Diagnostics / Control Plane
- Portability / Runtime
- Workbench / Artifacts
- Research Notes
- Business / Positioning
Do not:
Remove links or rewrite the lane's doctrine.

### GAP-WD-012 — Central docs index may lag new tools

Status: open
Type: docs
Severity: low
Affected paths:
- `docs/readme.md`
- `docs/start-here.md`
- `mkdocs.yml`
Issue:
New tools may be linked from `work-dev` but not surfaced in central documentation.
Why it matters:
Onboarding agents need a stable path to current governance tools.
Suggested next PR:
Add or verify links to diagnostics map, doctrine drift, counterfactual simulator, and agent sprawl docs.
Do not:
Over-expand `mkdocs.yml` unless consistent with repo style.

### GAP-WD-013 — Schema-registry vs schemas needs clarification

Status: open
Type: naming
Severity: low
Affected paths:
- `schema-registry/`
- `schemas/`
- `docs/`
Issue:
Both `schema-registry` and `schemas` exist at root.
Why it matters:
Contributors may place new schemas in the wrong location.
Suggested next PR:
Add a short schema placement note.
Do not:
Rename directories in this pass.

### GAP-WD-014 — Path names with spaces should be audited

Status: open
Type: naming
Severity: medium
Affected paths:
- `root tree`
- `scripts/`
Issue:
Some paths appear in GitHub listings with spaces, such as `app/ observability` or `examples/ diagnostics`. It is unclear whether these are real path spaces or rendering artifacts.
Why it matters:
Real spaces in repo paths create shell quoting and agent navigation friction.
Suggested next PR:
Add a read-only path-space audit or naming note.
Do not:
Rename paths without a migration plan.

### GAP-WD-015 — Claim-proof and agent-sprawl should cross-reference

Status: open
Type: docs
Severity: low
Affected paths:
- `docs/skill-work/work-dev/claim-proof-standard.md`
- `docs/skill-work/work-dev/agent-sprawl-control-plane.md`
Issue:
Agent surfaces and claimed capabilities overlap but may not always be linked.
Why it matters:
New agents should declare capability contracts and proof obligations.
Suggested next PR:
Add short cross-links.
Do not:
Make claim-proof a merge authority.

### GAP-WD-016 — Workbench receipts vs evidence truth needs repeated guardrail

Status: open
Type: authority
Severity: low
Affected paths:
- `docs/skill-work/work-dev/workbench/README.md`
- `docs/diagnostics-and-governance-tools.md`
- `config/doctrine-rules.v1.json`
Issue:
Workbench verifies artifact behavior, not external truth.
Why it matters:
Generated artifacts can run correctly while still being wrong about the world.
Suggested next PR:
Ensure this warning appears in Workbench, diagnostics map, and doctrine rules.
Do not:
Treat Workbench receipts as EVIDENCE.

### GAP-WD-017 — Counterfactual simulator should eventually read real proposal files

Status: open
Type: roadmap
Severity: medium
Affected paths:
- `scripts/simulate_counterfactual_fork.py`
- `docs/counterfactual-fork-simulator.md`
Issue:
Phase 1 uses proposal-like JSON; later phases may need to simulate actual review proposals or gate blocks.
Why it matters:
The simulator becomes more useful when connected to real pending changes.
Suggested next PR:
Design-only Phase 2 note for proposal/gate-block adapters.
Do not:
Parse `recursion-gate.md` or write gate outputs in this PR.

### GAP-WD-018 — Local diagnostic runner output should be documented

Status: open
Type: ergonomics
Severity: low
Affected paths:
- `scripts/run_deterministic_diagnostics.py`
- `docs/diagnostics-and-governance-tools.md`
Issue:
Users need to know how to interpret failures from the combined diagnostic runner.
Why it matters:
A combined runner is only useful if failures point to the right next action.
Suggested next PR:
Add a "how to interpret diagnostic failures" section.
Do not:
Hide individual tool outputs.

### GAP-WD-019 — Known gaps should remain lightweight

Status: open
Type: docs
Severity: low
Affected paths:
- `docs/skill-work/work-dev/known-gaps.md`
Issue:
This file can become a dumping ground if not constrained.
Why it matters:
A bloated gap list becomes another inefficiency.
Suggested next PR:
Add a maintenance rule: close, split, or archive gaps when implemented or obsolete.
Do not:
Use `known-gaps.md` as a substitute for gate review or issues.

### GAP-WD-020 — Diagnostics tools should not become authority layers

Status: open
Type: authority
Severity: high
Affected paths:
- `docs/diagnostics-and-governance-tools.md`
- `docs/skill-work/work-dev/diagnostics-control-plane.md`
- `docs/doctrine-drift-radar.md`
- `docs/counterfactual-fork-simulator.md`
- `docs/skill-work/work-dev/agent-sprawl-control-plane.md`
Issue:
As diagnostics tools become more central, future agents may treat their outputs as approval.
Why it matters:
Diagnostics inspect, simulate, or warn; they do not merge.
Suggested next PR:
Add repeated "diagnostics are not approval" language in the diagnostics map and known-gaps file.
Do not:
Grant any diagnostic tool gate or Record authority.

## Maintenance rule

- Keep gaps small and actionable.
- Prefer one small PR per gap.
- Close gaps when implemented.
- Split gaps that become architecture proposals.
- Move speculative ideas elsewhere.
- Do not use this file as a second gate or approval queue.
