# Cici AI work lanes implementation prompt

Paste this into a coding agent working in Xavier's Cici instance repo:

<https://github.com/Xavier-x01/Cici>

---

```markdown
You are working in Xavier's Cici instance repo:

https://github.com/Xavier-x01/Cici

Goal: implement a lightweight work-lane structure inspired by Grace-Mar's `work-cici` enhancements, adapted for this repo. Do not copy Grace-Mar Record files. This is an operator/workspace organization pass only.

## Create three active work lanes

Create:

```text
docs/work-lanes/
  README.md
  cici-ai-telegram/
    README.md
  cici-ai-core/
    README.md
  cici-ai-progress/
    README.md
```

## Lane definitions

### `cici-ai-telegram`

Purpose: coordinate the Telegram group as the social/cohort activation surface.

Include sections:

- Purpose
- Current scope
- Open loops
- Next action
- Key references

Initial scope:

- Group posts, pinned messages, welcome copy, applicant intake prompts, norms, replies.
- Route Telegram intros/GitHub links into evidence or progress tracking.
- Keep scholarship/employment/equity wording cautious and owner-reviewed.

Initial next action:
Draft the next Telegram post asking applicants to share their OB1 fork URL or screenshot.

### `cici-ai-core`

Purpose: coordinate the technical/governance core of Cici.

Include sections:

- Purpose
- Current scope
- Open loops
- Next action
- Key references

Initial scope:

- Governed-state doctrine, prompts, source-priority, memory policy, repo identity, safety checks.
- Keep Supabase/runtime subordinate to Git/governed-state truth.
- Track proposal-required changes.

Initial next action:
Audit active files for stale Xavier/current-owner identity mismatch and classify references as current-state or provenance.

### `cici-ai-progress`

Purpose: track member/applicant progress and cohort health.

Include sections:

- Purpose
- Current scope
- Open loops
- Next action
- Key references

Initial scope:

- Applicant/member table.
- GitHub account, OB1 fork status, first-task proof, skill estimate, scholarship readiness.
- Use evidence labels; do not overstate eligibility, employment, equity, or payment commitments.

Initial next action:
Create or update a dashboard table with: name, country, GitHub, self-reported experience, visible GitHub signal, OB1 fork status, first-task status, next prompt.

## Root lane hub

In `docs/work-lanes/README.md`, add a table:

| Lane | Purpose | Primary questions |
|---|---|---|
| `cici-ai-telegram` | Telegram group operations, posts, norms, applicant intake, and communication. | What should be posted? Who needs a reply? What needs recording from chat? |
| `cici-ai-core` | Cici/OB1 architecture, prompts, governed-state, repo migration, safety, and technical implementation. | What should change in the repo? What needs proposal/approval? What is safe to automate? |
| `cici-ai-progress` | Member progress, applicant table, task completion, proof packets, scholarships, and cohort metrics. | Who has done what? What is the next task? What evidence supports the status? |

Add this boundary rule:

Lane files may summarize, stage, and route. They must not silently rewrite governed-state, applicant claims, payment commitments, or identity facts.

## Existing docs

After creating the lane files, update any obvious index/navigation file in the repo, such as `README.md`, `docs/personal/README.md`, or another existing docs index, so the new lane hub is discoverable. Keep this minimal.

## Safety rules

- Do not edit secrets.
- Do not invent applicant facts.
- Do not rewrite approved proposal history.
- Do not merge governed-state changes unless the repo's existing approval/proposal rules allow it.
- Preserve historical Xavier references in proposal logs or evidence where they are provenance.
- Current-state docs should use current Cici/operator wording.

## Validation

Run:

```bash
python scripts/validate-governed-state.py
```

If available, also run any markdown/link or repo doctor checks that already exist. Then report:

- Files created
- Files updated
- Validation result
- Any remaining stale identity references that should be handled in a separate pass
```
