# Schema and API contract

**Companion-Self template · Minimal schema for Record and pipeline**

This document defines the Record schema, recursion-gate shape, and API contracts for the 6-week student interface and future extensions. See [CONCEPT](concept.md), [IDENTITY-FORK-PROTOCOL](identity-fork-protocol.md), and [PROJECT-6WEEK-CODING](project-6week-coding.md).

---

## Record schema

| Component | File | Fields / structure |
|-----------|------|--------------------|
| **SELF** | self.md | Identity baseline (I–VIII); optional pointer to IX. |
| **KNOWLEDGE** | self-knowledge.md | Topics, facts, understanding; one line per entry; optional evidence id. |
| **IDENTITY** | self-identity.md | Durable identity commitments, boundaries, role commitments, long-horizon identity direction. |
| **IX-B** | self-curiosity.md | Interests, questions; one line per entry; optional evidence id. |
| **IX-C** | self-personality.md | Voice, preferences, values, narrative; one line per entry; optional evidence id. |
| **THINK** | self-skill-think.md | Intake and comprehension; evidence links. |
| **WRITE** | self-skill-write.md | Expression and voice; evidence links. |
| **WORK** | self-skill-work.md | Making and doing; evidence links. See **WORK objectives and tasks** below. |
| **STEWARD** | self-skill-steward.md | Governance literacy — gate participation, boundary vocabulary; evidence links. Does not grant merge authority. |
| **self-evidence** | self-evidence.md | Activity log entries: `id`, `date`, `summary`, `skill_tag` (THINK \| WRITE \| WORK \| STEWARD). |

All Record files live under `users/<id>/`. Split growth files (`self-knowledge`, `self-identity`, `self-curiosity`, `self-personality`) are the source of truth for post-seed growth.

---

## WORK (self-skill-work): objectives and tasks standard

Standard modular structure for objectives and tasks in `self-skill-work.md`. Instances may extend (e.g. add levels, creative context) but these fields are the template contract.

### Objectives

| Element | Type | Description |
|--------|------|--------------|
| **module_intent** | string | One sentence: WORK as tutor; edge, scaffolding, work goals, life mission; human-gated. |
| **default_objectives** | list of { label, description } | **Default objectives for new users** (standard set of six): Learn and grow, Express and create, Build and ship, Make progress visible, Stay within the design, Recursively improve. See [Evolving practice and recursive improvement](evolving-practice-recursive-improvement.md) for how this objective connects to context/intent/specification practice as technology advances. Instance may replace or extend. In markdown: `- **Label** — description`. |
| **work_goals** | object | Companion's own goals; evidence-linked when captured. |
| **work_goals.near_term** | string[] | Near-term goals (e.g. "finish X", "learn Y"). May be empty. |
| **work_goals.horizon** | string[] | Longer-term goals (e.g. "SAT ≥ 1200"). May be empty. |
| **work_goals.source** | string (optional) | Evidence id when goals were captured. |
| **life_mission_ref** | string | Pointer to SELF (e.g. `self.md § VALUES`). WORK goals align with life mission. |

### Tasks

Planning and execution items (projects, next steps, deliverables). Each task:

| Field | Type | Description |
|-------|------|-------------|
| **id** | string (optional) | Stable id for linking (e.g. `task-1`, `T-001`). |
| **summary** | string | Short description of the task. |
| **status** | string | One of: `pending`, `in_progress`, `done`. |
| **evidence_id** | string (optional) | Evidence id when task is completed and recorded (links to self-evidence). |
| **updated** | string (optional) | ISO date or timestamp of last change. |

**Markdown representation:** Use a table or a consistent list form. Example table:

```markdown
| id | summary | status | evidence_id |
|----|---------|--------|-------------|
| T-001 | Finish dragon drawing | done | ACT-xxx |
| T-002 | Next chapter read-aloud | pending | — |
```

Or list form: `- **summary** — status (evidence_id)`.

Instances may add fields (e.g. priority, target_date, skill_tag). The minimum for template compliance is **summary** and **status**.

---

## Recursive-gate shape

Array of candidates. Each candidate:

| Field | Type | Description |
|-------|------|--------------|
| id | string | Unique id (uuid or timestamp). |
| raw_text | string | Raw "we did X" or activity text. |
| skill_tag | string | THINK, WRITE, WORK, or STEWARD. |
| mind_category | string | knowledge, curiosity, or personality (keyword or default). |
| suggested_ix_section | string | IX-A, IX-B, or IX-C (target dimension). |
| created_at | string | ISO date or timestamp. |
| status | string | "pending" until approved/rejected. |

**Format:** `users/<id>/recursion-gate.json` — JSON array, append-only on stage. Candidates are removed on approve (merge) or reject.

### Default skill → dimension mapping

When staging or merging, the default mapping from **skill_tag** to **suggested_ix_section** (dimension file) is:

| skill_tag | suggested_ix_section | Dimension file |
|-----------|----------------------|----------------|
| THINK     | IX-A                 | self-knowledge.md |
| WRITE     | IX-C                 | self-personality.md |
| WORK      | IX-B                 | self-curiosity.md |
| STEWARD   | IX-C                 | self-personality.md (default: values, boundaries, consent vocabulary) |

Instances may override (e.g. per-activity or LLM-suggested section); this is the template default.

---

## Acceptance criteria for staging and merge

**Transcript primitive:** For every task you delegate, write sentences that an independent observer could use to verify the output without asking you any questions.

**Staged candidate (good):**

1. **Self-contained** — `raw_text` describes what was done with enough context that a reviewer who wasn’t present can understand the activity and reason about where it belongs (dimension/skill).
2. **Schema-valid** — Has required fields (id, raw_text, skill_tag, mind_category, suggested_ix_section, created_at, status) and values are in allowed sets (THINK/WRITE/WORK/STEWARD; IX-A/IX-B/IX-C).
3. **Merge-ready** — After approve, the merge logic can write exactly one evidence entry and, when applicable, one dimension line to the correct file without guessing.

**Merge outcome (good):**

1. **Evidence** — One new activity log entry in self-evidence with id, date, summary, skill_tag; id is stable and referenceable (format e.g. ACT-YYYY-MM-DD-&lt;suffix&gt;).
2. **Dimension (if applicable)** — One new line in the correct growth file (`self-knowledge`, `self-identity`, `self-curiosity`, or `self-personality`) when target section was set; line format matches existing bullets; no duplicate or overwrite of unrelated lines.
3. **Skill file** — One new line in the matching skill file (THINK → self-skill-think.md, WRITE → self-skill-write.md, WORK → self-skill-work.md, STEWARD → self-skill-steward.md); line includes evidence id for linking.
4. **Gate** — Candidate removed from recursion-gate; no other candidates modified.
5. **Receipt** — One line appended to merge-receipts.jsonl (candidate_id, raw_text, suggested_ix_section, merged_at).

An independent observer can verify by: (a) reading the candidate and the Record before merge, (b) running approve, (c) reading the Record and receipts after merge, and (d) confirming the five points above without asking the operator.

---

## Edge response shape (Week 5)

GET `/api/edge` returns suggested next focus per THINK, WRITE, WORK, and optionally STEWARD. Also included in GET `/api/record` and `/api/export` curriculum profile.

| Field | Type | Description |
|-------|------|--------------|
| THINK | string | Suggested next focus for intake/comprehension (e.g. "Keep reading", "Continue with: topic"). |
| WRITE | string | Suggested next focus for expression (e.g. "Try a short story", "Build on: …"). |
| WORK | string | Suggested next focus for making/doing. Phrased using self-personality (IX-C) when available. See [CONCEPT](concept.md) §4 "How WORK utilizes self-personality (IX-C)". |
| STEWARD | string (optional) | Suggested next focus for gate literacy (e.g. "Review one pending candidate with a trusted adult"). Omit if the instance does not use STEWARD. |

**Example:** `{ "THINK": "Keep reading", "WRITE": "Try a short story", "WORK": "One small project", "STEWARD": "Name the gate in your own words" }`

---

## Record-derived lesson prompt (minimal shape)

For **Record-driven prompts** (paste into any LLM to trigger a personalized lesson), the template defines a minimal prompt shape. See [Alpha School reference (skill-work-alpha-school)](skill-work/skill-work-alpha-school/alpha-school-reference.md) §4.1 for context and typical flow (3–5 lessons per day, transcript → skill-think).

**Required Record fields for the prompt:** knowledge (IX-A), curiosity (IX-B), personality (IX-C), edge (what’s next per THINK/WRITE/WORK). Optional but useful: skills (THINK, WRITE, WORK arrays) for level and recent activity.

**Data source:** Use **GET `/api/record`** to build the prompt; it returns knowledge, curiosity, personality, skills, edge, and pending count. **GET `/api/export`** returns the curriculum profile (knowledge, curiosity, personality, edge, evidenceCount, exportDate, screen_time_target_minutes) for tutor/curriculum consumers; use it when a single portable payload is needed and skills are not required.

**Example prompt template (minimal):**

```
You are tutoring a learner one-on-one. Use only the following about them to personalize this lesson.

What they know (topics): [knowledge]
What they're curious about: [curiosity]
Voice/preferences: [personality]
What to teach or do next — THINK: [edge.THINK], WRITE: [edge.WRITE], WORK: [edge.WORK]

Deliver one short, focused lesson (or activity) suited to their level and interests. Do not add facts about them to your reply; the learner will capture what was done via their own system.
```

**Optional — explicit timebox:** Operators may append **one sentence** about pacing (e.g. a single 25-minute focus block, or staying within the 2-hour ceiling across several activities) without adding new factual claims about the learner. See [skill-work/work-dev/pomodoro-and-timeboxing.md](skill-work/work-dev/pomodoro-and-timeboxing.md).

Instances may extend the template (e.g. add skills, evidence count, or screen_time_target_minutes). The prompt must draw only from Record/export content (knowledge boundary); no LLM inference is written back into the Record until the companion approves via the gate.

---

## Seed-phase artifact schemas

**Seed phase** artifacts are **pre-activation** formation outputs. They are **distinct** from instance Record schemas (`self.md`, `self-evidence`, IX files). They live under `users/_template/seed-phase/` (scaffold), `users/demo/seed-phase/` (synthetic example), or an instance-managed directory **before** `users/<id>/` is activated.

JSON Schemas (Draft 2020-12) in `schema-registry/`:

| Schema file | Validates on-disk file |
|-------------|-------------------------|
| `seed-phase-manifest.v1.json` | `seed-phase-manifest.json` |
| `seed-intake.v1.json` | `seed_intake.json` |
| `seed-intent.v1.json` | `seed_intent.json` |
| `seed-identity.v1.json` | `seed_identity.json` |
| `seed-curiosity.v1.json` | `seed_curiosity.json` |
| `seed-pedagogy.v1.json` | `seed_pedagogy.json` |
| `seed-expression.v1.json` | `seed_expression.json` |
| `seed-memory-contract.v1.json` | `seed_memory_contract.json` |
| `seed-memory-ops-contract.v1.json` | `memory_ops_contract.json` |
| `seed-trial-report.v1.json` | `seed_trial_report.json` |
| `seed-readiness.v1.json` | `seed_readiness.json` |
| `seed-confidence-map.v1.json` | `seed_confidence_map.json` |
| `work-business-seed.v1.json` | `work_business_seed.json` |
| `work-dev-seed.v1.json` | `work_dev_seed.json` |
| `seed-constitution.v1.json` | `seed_constitution.json` |

Protocol and validation: [seed-phase.md](seed-phase.md), [seed-phase-validation.md](seed-phase-validation.md). `template-manifest.json` exposes paths under `seed_phase.schemas`.

**Constitution (optional Voice self-critique):** `seed_constitution.json` is generated offline (`scripts/generate-constitution.py`) after strict seed validation. It does not add SELF facts; enabling critique in production uses repo-root **`runtime_config.json`** (see `runtime_config.example.json`). Material changes to critique policy belong in **change review** or operator governance, not silent edits to `bot/prompt.py` — see [change-review.md](change-review.md) and [gate-vs-change-review.md](gate-vs-change-review.md).

---

## Change-review schemas

The change-review subsystem uses separate schemas from the live Record and from seed-phase artifacts.

These schemas govern proposed changes, decisions, visible diffs, review queues, and event history.

- change-proposal.v1.json
- change-decision.v1.json
- identity-diff.v1.json
- change-review-queue.v1.json
- change-event-log.v1.json

Doctrine and lifecycle: [change-review.md](change-review.md), [change-review-lifecycle.md](change-review-lifecycle.md). `template-manifest.json` lists these under `change_review.schemas`.

**Validation:** `python3 scripts/validate-change-review.py users/demo/change-review` — uses Draft 2020-12 validators via `jsonschema` (install from `scripts/requirements-seed-phase.txt`). Demo artifacts live under `users/demo/change-review/`.
