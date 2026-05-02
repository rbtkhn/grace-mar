---
name: observability-to-cadence-capture
title: Observability to Cadence Capture
preferred_activation: observability capture
description: "Capture repeated observability and regeneration patterns into governed WORK or portable-skill workflows."
version: 0.1.0
portable: true
tags:
  - operator
  - work-dev
  - cadence
  - observability
  - recursive-improvement
---

# Observability to Cadence Capture

**Preferred activation (operator):** say **`observability capture`**. **Aliases:** **`Hermes skill capture`**, **`cadence observability pattern`**.

## Purpose

Capture repeated operational observability, cadence, and regeneration patterns into the correct governed surface. The skill turns recursive self-improvement signals into a reviewable capture packet, not an automatic Record merge.

Hermes-style agents are advisory only: they detect and propose. They do not merge, promote, or write Record truth.

## When to Use

- A bridge, dream, or conductor pass repeatedly surfaces the same observability gap.
- A workflow hardening pattern appears across two or more related commits.
- Derived regeneration or cadence wiring starts requiring repeated manual judgment.
- The operator asks whether a recent workflow pattern should become a portable skill, work-dev note, or gate candidate.

Do not trigger this from one clever commit unless the operator explicitly requests a skill-capture review.

## Inputs

Collect a small evidence packet before recommending any destination:

- Working name for the candidate skill or workflow.
- Trigger phrase an operator would actually use.
- Evidence commits, bridge notes, dream notes, or conductor outcomes.
- Changed surfaces: Record, WORK docs, scripts, runtime/derived artifacts, or portable skills.
- What repeats across the evidence.
- What operator pain or manual load was reduced.
- What must not be automated.

## Surface Classification

Use this classification before writing anything:

| Surface | Destination | Rule |
|---------|-------------|------|
| Record | `users/<id>/recursion-gate.md` | Only for explicit SELF, EVIDENCE, prompt, or Voice truth candidates. |
| WORK | `docs/skill-work/`, work-dev notes, or skill-candidate pointer | Cadence, scripts, strategy, and workflow method stay out of the Record gate. |
| Runtime / derived | Artifacts, dashboards, manifests, receipts, or rebuild docs | Treat as rebuildable observability, not Record truth. |
| Portable skill | `skills-portable/skill-candidates.md`, `_drafts/`, then listed skill after approval | Use the skill discovery ladder; do not jump to manifest without operator approval. |

If a pattern touches more than one surface, name the primary destination and list the excluded surfaces.

## Boundary Ambiguity

When the repeated pattern is mainly about continuity surface confusion, use `docs/record-continuity-surface-map.md` before recommending any capture destination. Treat that map as source doctrine; this draft only provides the reusable capture packet.

- Boundary check: pass / watch / block
- Primary surface:
- Excluded surfaces:
- Gate required: yes/no
- Correct destination:
- Reason:

## Procedure

1. **Identify the repeated pattern.** Require two or more related commits, or a clear bridge/dream/conductor recurrence.
2. **Classify the surface.** Decide whether the pattern belongs to Record, WORK, runtime/derived, or portable skill.
3. **Create a capture packet.** Include working name, trigger phrase, evidence, repeats, reusable method, non-automation boundary, and recommended destination.
4. **Choose the ladder rung.**
   - Weak or first sighting: add or recommend one row in `skills-portable/skill-candidates.md`.
   - Strong repeatable pattern: draft `skills-portable/_drafts/<name>/SKILL.md`.
   - Mature and operator-approved: promote to `skills-portable/<name>/SKILL.md`, add `manifest.yaml`, sync Cursor skill, and validate.
5. **Verify boundaries.** Confirm WORK-only methodology did not create a `recursion-gate.md` candidate.

## Output Shape

Use this compact packet when proposing a capture:

```markdown
## Skill Capture Packet

- Working name:
- Trigger phrase:
- Evidence:
- Changed surfaces:
- What repeats:
- What should be reused:
- What must not be automated:
- Recommended destination:
- Boundary check:
```

## Never Do

- Do not stage WORK, cadence, runtime, or derived-output methodology directly to `recursion-gate.md`.
- Do not let Hermes or any sub-agent approve, merge, or promote its own proposal.
- Do not promote a listed portable skill after one clever commit unless the operator explicitly asks.
- Do not invent success metrics that the repo does not measure.
- Do not hand-edit generated `.cursor/skills/*/SKILL.md`; promote through the portable skill ladder and sync.

## Verification

- For pointer-only changes: confirm `recursion-gate.md`, `manifest.yaml`, and generated `.cursor/skills/*/SKILL.md` are untouched.
- For draft changes: inspect the draft and run the repo skill validator if available.
- For listed-skill promotion: run `scripts/sync_portable_skills.py --verify` and `scripts/validate_skills.py`.

## Seed Evidence

Initial pattern evidence:

- `93cf015` - wired memory observability into cadence.
- `a9d2dd1` - hardened memory observability wiring.
- `65f2cc4` - reduced workflow complexity and expanded strategy backfills.
- `c1368ff` - added ideation engine and decision-fatigue defaults.

The extracted lesson is not "stage observability to the Record." The lesson is "when repeated operational observability work lowers conductor load, capture the method in the portable skill ladder or work-dev surface."
