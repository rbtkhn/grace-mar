# Moonshot Orchestration

- **Status:** WORK-only module
- **Surface:** `docs/skill-work/work-strategy/modules/moonshot-orchestration/`
- **Record status:** Not Record truth
- **Skill status:** Not a canonical skill
- **Execution status:** Not external infrastructure authority

## Purpose

Moonshot Orchestration is a WORK-layer module for converting high-variance civilizational opportunity signals into bounded contribution maps, source-tier assessments, boundary checks, dashboard entries, and optional gated proposals.

It does not alter the Record, does not create autonomous commitments, and does not promote itself into SKILLS without later review.

This module is inspired by the proposed `SKILL-0018: Moonshot Orchestration`, but it is deliberately implemented first as a WORK-layer strategy module rather than a canonical skill.

## What counts as a moonshot

A moonshot is an audacious civilizational-scale project or opportunity that may target 10x–100x gains in capability, resilience, abundance, computation, infrastructure, science, or coordination.

Examples may include:

- orbital or energy-scale computing concepts
- advanced AI governance and runtime architectures
- recursive self-improvement infrastructure
- abundance engineering
- civilization-scale scientific or economic projects
- personal cognitive fork scaling pathways

Mentioning a moonshot here does not imply endorsement, feasibility, capability, or authorization.

## Relationship to work-strategy

This module belongs under `work-strategy` because moonshot assessment is a form of governed strategic judgment.

**Allowed functions:**

1. observe signals
2. classify source strength
3. map possible contributions
4. identify strategic relevance
5. surface contradictions and hype flags
6. propose small experiments
7. stage candidate proposals for human review

**Forbidden functions:**

1. direct Record edits
2. canonical skill creation
3. autonomous external execution
4. unsupported capability claims
5. unreviewed promotion into SELF, SELF-LIBRARY, SKILLS, or EVIDENCE

## Relationship to runtime complements

External runtimes, agents, caches, or orchestration systems may be discussed as possible moonshot-relevant infrastructure, but this module does not wire, authorize, or control them.

Runtime complements remain accelerators only. They are not memory, identity, evidence, or canonical authority.

## Relationship to the recursion-gate

Any durable downstream claim or proposed change to Record surfaces must be staged separately through the normal gate process.

This module may produce a candidate proposal. It may not approve, merge, or execute that proposal.

## Artifacts

| File | Role |
| --- | --- |
| `moonshot-boundary.md` | Hard boundaries and governance rules |
| `moonshot-lifecycle.md` | Operating lifecycle from signal to possible proposal |
| `moonshot-map-template.md` | Reusable contribution-map template |
| `moonshot-dashboard.md` | Derived WORK dashboard |
| `moonshot-source-policy.md` | Source and claim-tier discipline |
| [`maps/`](maps/) | Dated Moonshot Contribution Map instances generated from the template |
| [`scripts/new_moonshot_map.py`](../../../../../scripts/new_moonshot_map.py) | Helper for creating dated map instances; does not auto-edit the dashboard |

## Helper script

`new_moonshot_map.py` creates dated **WORK-only** contribution-map instances from `moonshot-map-template.md`.

Example:

```bash
python3 scripts/new_moonshot_map.py --slug dyson-swarm-compute --title "Dyson Swarm Compute"
```

The helper does not edit `moonshot-dashboard.md`, does not stage proposals, and does not touch Record surfaces.

## Default operating path

1. Capture moonshot signal.
2. Classify source tier.
3. Create or update a Moonshot Contribution Map.
4. Run boundary check.
5. Add or update dashboard row.
6. If actionable, draft a gated proposal candidate.
7. Do not execute externally without explicit approval.

## Design principle

The module exists to make Grace-Mar better at asking:

- Is this moonshot real, speculative, or mostly narrative?
- What evidence tier supports it?
- What would a sane small experiment look like?
- Which part belongs in strategy, work-dev, CIV-MEM, SELF-LIBRARY, or nowhere?
- What would prove this deserves more attention?
- What would falsify it?
- What can the operator safely do next?

Moonshot Orchestration is therefore not hype acceleration. It is governed opportunity filtering.
