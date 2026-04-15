# skill-think — doctrine hub

**Purpose:** First-class **operator + agent** documentation for the **THINK** capability module — intake, learning, and evidenced cognitive growth — **without** duplicating [skills-modularity.md](../skills-modularity.md) or [conceptual-framework.md](../conceptual-framework.md).

**Territory:** Record-bound **SKILLS** (THINK), not SELF identity, not WORK execution. Per-instance prose lives under `users/[id]/` (e.g. `skill-think.md` or `self-skill-think.md` — see [think-purpose-and-boundary.md](think-purpose-and-boundary.md)).

## Contents

| Doc | Role |
|-----|------|
| [think-purpose-and-boundary.md](think-purpose-and-boundary.md) | What THINK is, gate behavior, naming map |
| [think-vs-self-vs-work.md](think-vs-self-vs-work.md) | THINK vs IX vs WORK lanes |
| [think-taxonomy.md](think-taxonomy.md) | Capability types |
| [think-levels.md](think-levels.md) | Maturity levels |
| [think-evidence-standard.md](think-evidence-standard.md) | Evidence-backed claims + SSOT |
| [think-claim-template.md](think-claim-template.md) | Copy-paste claim stub |
| [think-to-ix-promotion-rules.md](think-to-ix-promotion-rules.md) | When THINK stays intake vs promotes to IX |
| [ix-promotion-examples.md](ix-promotion-examples.md) | Examples |
| [think-exercises.md](think-exercises.md) | Test types, prompts, scaffolding |
| [think-update-ritual.md](think-update-ritual.md) | Operator ritual + receipts |
| [observability.md](observability.md) | Metrics artifact + builder |

## Pipelines (read first)

- [we-read-think-self-pipeline.md](../we-read-think-self-pipeline.md) — READ → THINK → optional IX
- [pipeline-map.md](../pipeline-map.md) — READ flow
- [skills-modularity.md](../skills-modularity.md) §5 — module boundaries

## Machine artifacts (repo-level)

- `artifacts/skill-think/think-claims.json` — structured claims index (Phase A: companion to prose)
- `artifacts/skill-think/think-observability.json` — generated metrics (sibling to other lane observability JSON; **not** merged into change-proposal `observability-report.v1` without schema extension)
- `artifacts/skill-think/update-receipts/` — optional JSONL receipts from [record_think_update.py](../../scripts/record_think_update.py)

## Scripts

| Script | Role |
|--------|------|
| [validate_think_claims.py](../../scripts/validate_think_claims.py) | Schema + advisory checks |
| [build_think_observability.py](../../scripts/build_think_observability.py) | Emit `think-observability.json` |
| [record_think_update.py](../../scripts/record_think_update.py) | Append audit receipt |
| [propose_think_claims_from_read.py](../../scripts/propose_think_claims_from_read.py) | Assistive stubs from READ ids (stdout only) |
