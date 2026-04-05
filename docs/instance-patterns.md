# Instance patterns and reference implementation

**Companion-Self template · Patterns from advanced instances**

---

## Reference implementation: Grace-Mar

**Grace-Mar** (https://github.com/rbtkhn/grace-mar) is the first and currently only instance. It implements bot (Telegram, WeChat), LLM analyst, full pipeline, profile, miniapp, export, and metrics. Instances can reference it for implementation patterns.

The template stays code-light and protocol-first; Grace-Mar diverges in several ways (see below). These divergences are documented so the template remains minimal while instances know what extensions are possible.

**Current alignment note:** Grace-Mar’s canonical staging file is **`recursion-gate.md`**. Older references to **`pending-review.md`** should be treated as **legacy documentation**, not current implementation.

---

## Instance variations

| Area | Template | Grace-Mar |
|------|----------|-----------|
| Intake | skill THINK (`self-skill-think`) | Grace-Mar also uses THINK (semantically equivalent: intake, comprehension). |
| Staging contract | Gate queue abstraction; instance may choose file encoding | `recursion-gate.md` under canonical instance paths. |
| Analyst | Out of scope for 6 weeks | LLM analyst runs on conversation and “we did X”; stages candidates automatically. |
| Voice | Not implemented | Telegram + WeChat bots. |
| Archive | `self-memory.md` (ephemeral, optional) | `self-archive.md` (gated log, rotation when large). |
| Lesson delivery | Optional: prompt generator + any LLM | **LLM-lesson method:** Record-derived prompts pasted into ChatGPT, Grok, or any LLM; 3–5 personalized lessons per day; transcript flows into skill-think for processing. No bot install; often easier for many users than a dedicated bot. Grace-Mar may offer both. See [Alpha School reference (skill-work-alpha-school)](skill-work/skill-work-alpha-school/alpha-school-reference.md) §4.1. |

* * *

## Staging contract

The template defines a single canonical abstraction: the **gate queue**.

Required invariants:

- candidates can be staged without merge
- the user reviews, rejects, modifies, or approves
- no governed state changes without explicit approval
- merge logic consumes approved candidates only

Instance file format is implementation-specific. Supported examples include:

- `recursion-gate.json` — structured JSON queue
- `recursion-gate.md` — Markdown gate file
- legacy queue documents such as `pending-review.md` only when an instance explicitly adopts them

Grace-Mar’s current canonical staging file is **`recursion-gate.md`**, not **`pending-review.md`**.

The contract is about lifecycle and authority, not filename.

---

## Evidence and prepared context (extensions)

Instances may add their own **evidence ingestion** and **staging** machinery (directories, ETL, vendor connectors). They should **preserve provenance**, keep [prepared context](prepared-context-layer.md) traceable to sources, and **not** treat staging outputs as durable **Record** or governed state without the gate or change-review path. Template reference: [prepared-context-doctrine.md](prepared-context-doctrine.md), [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md).

---

## Analyst output contract (optional)

When an instance adds an **LLM analyst** that stages candidates from conversation or activity, the analyst output should conform to a contract so merge logic can consume it. Grace-Mar uses flat YAML with these required fields:

| Field | Meaning |
|-------|---------|
| mind_category | One of: knowledge, curiosity, personality (maps to IX-A, IX-B, IX-C). |
| signal_type | Kind of signal (e.g. lookup, knowledge, teach, new_interest, personality). |
| summary | Brief description of what was observed. |
| profile_target | Target dimension/section (e.g. IX-A, IX-B, IX-C). |
| suggested_entry | Proposed line for the dimension file. |
| prompt_section | Section of prompt/Record this relates to. |
| prompt_addition | Proposed addition to that section. |

Optional: `priority_score` (1–5), `tension_with` or `alternative_interpretation` when the signal conflicts with existing profile. Analyst may return `NONE` when no signal is detected.

**Design principle:** The analyst detects and stages; the companion gates. No merge without approval.

---

## Session brief (operator tool)

**Session brief** — Before or during a session, the operator (or companion) may want a short summary: what's pending at the gate, recent activity, suggested next focus. This is an **operator tool pattern**, not a template requirement.

Instances that support it can expose: pending count, list of candidate summaries, recent merges, edge ("what's next"). Useful for "quick sync" before processing the gate or starting a session. When a human teacher is present, the session brief supports **reading** skill-think and edge so they can **modulate** focus and gate; see [Human teacher objectives (skill-work-human-teacher)](skill-work/skill-work-human-teacher/human-teacher-objectives.md).

---

## Conflict check (optional)

Before merge, an instance may run a **conflict check** on a candidate: compare suggested content against existing Record (e.g. IX-A, IX-B, IX-C) and flag potential contradictions or overlap. Surfaces for user resolution; does not block staging. The companion still decides at the gate; conflict check is advisory.

Full governed workflow (identity-diff UI, resolution types, temporal merge, audit): [CONTRADICTION-ENGINE-SPEC](CONTRADICTION-ENGINE-SPEC.md). Resolution vocabulary: [contradiction-resolution](contradiction-resolution.md).

---

## Seed-visible instance (`seed-visible-instance`)

**Use when:** You want formation work to be **inspectable** before activation.

**Pattern:** Keep `users/<id>/seed-phase/` (or a repo-local `seed-phase/` directory) with the canonical JSON set + `seed_dossier.md` **outside** merged Record files until readiness **pass**. Point operators at [seed-phase-artifacts.md](seed-phase-artifacts.md) and validate with `scripts/validate-seed-phase.py`.

---

## Seed revalidation after upgrade (`seed-revalidation-after-upgrade`)

**Use when:** The template bumps `seed_phase.version` or JSON Schemas.

**Pattern:** Preserve existing seed JSON (git tag or copy); run strict validation; if invalid, run a documented migration or re-collect affected stages — do not silently replace files. See [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md) § Seed-phase upgrade compatibility.

---

## Review-gated instance

A review-gated instance does not apply materially important governed changes directly.

Instead, it routes significant post-seed changes through:

- proposal
- classification
- visible diff
- decision
- event log

Use this pattern when:

- the instance is intended to be stable across long periods
- pedagogy and identity coherence matter
- auditability matters more than convenience

See [change-review.md](change-review.md) and [change-review-lifecycle.md](change-review-lifecycle.md).

---

## Upgrade-collision review

An upgrade-collision review pattern treats template-instance collisions as governance events rather than silent merges.

Use this pattern when:

- template evolution is expected to be frequent
- the instance has already accumulated reviewed local commitments
- the cost of silent drift is high

See [how-instances-consume-upgrades.md](../how-instances-consume-upgrades.md) (section **Template upgrade collisions**).

---

## High-trust governed instance

A high-trust governed instance combines:

- formal [seed phase](seed-phase.md)
- readiness gate
- review-gated post-seed revision
- upgrade-collision review

Use this pattern when identity coherence, boundary clarity, auditability, and controlled evolution matter more than convenience.

---

## Cross-references

- [Concept](concept.md) — READ/WRITE/WORK, identity and instrument.
- [Schema and API contract](schema-record-api.md) — Record schema; **WORK objectives and tasks standard** (objectives, work_goals, tasks with summary/status/evidence_id).
- [Ingestion and sources](ingestion-and-sources.md) — Many sources → staging → gate → Record; triggers for suggested merges.
- [Identity Fork Protocol](identity-fork-protocol.md) — Sovereign Merge Rule, schema, Process the gate.
- [Project 6-week coding](project-6week-coding.md) — Minimal companion app (no analyst, no Voice).
