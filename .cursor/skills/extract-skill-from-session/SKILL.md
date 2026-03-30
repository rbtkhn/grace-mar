---
name: extract-skill-from-session
preferred_activation: save skill
description: After a successful multi-step task or workflow in Cursor, codify it as a Cursor skill (SKILL.md) so the same workflow can be invoked again. Use when the user says "add a skill from this," "turn this into a skill," "save this as a skill," or wants to reuse a workflow from the current or a recent session.
---

# Extract Skill From Session

**Preferred activation (operator):** say **`save skill`** (or **`skill from session`**).

Use this skill when the operator has just completed (or is in the middle of) a task that worked well and wants it captured as a reusable Cursor skill — the same idea as "turn this into a skill" in Claude Co-work: never repeat the instructions manually again.

## When to run

- User says "add a skill from this," "turn this into a skill," "save as a skill," or similar.
- User describes a workflow they want to repeat and want it documented as a skill.
- A session just produced a clear, repeatable process (e.g. test-and-report, gate review, MEM-Persia integration) and the user wants it reusable.

## Steps

1. **Identify what was done**
   - Main steps (in order).
   - Scope: which files, folders, or territories.
   - Key decisions or guardrails (what not to do).
   - Any commands, scripts, or tools used.

2. **Name the skill**
   - Lowercase, hyphens only; max 64 chars.
   - Example: `extract-skill-from-session`, `gate-review-pass`, `pol-pulse`.

3. **Write the description (frontmatter)**
   - Third person.
   - WHAT: what the skill does in one sentence.
   - WHEN: trigger phrases or situations (e.g. "Use when reviewing the gate" or "Use when the user asks for a warmup").
   - Keep under 1024 chars.

4. **Write the body**
   - Short "Use this skill when…" opener.
   - Instructions: numbered or bullet steps; concise.
   - Optional: default command, guardrails, related files.
   - No fluff; assume the agent is capable.

5. **Create the skill file**
   - **grace-mar portable ladder:** Prefer a **portable** core under `skills-portable/_drafts/<skill-name>/SKILL.md` (then promote to `skills-portable/<skill-name>/` + `manifest.yaml` + `sync_portable_skills.py` per [skills-portable/README.md](../../skills-portable/README.md)). Log a one-liner first in [skills-portable/skill-candidates.md](../../skills-portable/skill-candidates.md) when the operator only wants a pointer.
   - **Direct Cursor skill:** `.cursor/skills/<skill-name>/SKILL.md` (project) or `~/.cursor/skills/<skill-name>/SKILL.md` (personal) when not using the portable pipeline.
   - YAML frontmatter with `name` and `description`, then markdown body.
   - Keep SKILL.md under 500 lines; put long reference in a separate file if needed.

## Output

- Create `.cursor/skills/<skill-name>/SKILL.md` with the new skill.
- Tell the operator the skill name and how to trigger it (e.g. "Ask for a gate review" or "Say 'run warmup'").

## Guardrails

- Do not overwrite an existing skill without explicit confirmation.
- If the session context is thin, ask the operator to briefly describe the workflow or paste the relevant part of the conversation before generating the skill.
- Follow the project's existing skill style (see e.g. `gate-review-pass`, `pol-pulse`) for tone and length.

## Reference

- Skill format and best practices: `~/.cursor/skills-cursor/create-skill/SKILL.md` (read when refining or when the operator wants full compliance with Cursor skill authoring).
