# Seed Phase — Canonical stages (v2)

**Companion-Self template · Stage spec**

This document defines the **formation pipeline** before a companion instance is **activated**. Stages produce **inspectable artifacts** (see [seed-phase-artifacts.md](seed-phase-artifacts.md)), not a live merged Record. Activation requires passing the [readiness gate](seed-phase-readiness.md).

---

## Stage overview

| Stage | Name | Goal |
|-------|------|------|
| 0 | Intake | Capture constraints, use cases, and safety/education context. |
| 1 | Identity Scaffold | Companion name, role, boundaries, non-goals, invariants. |
| 2 | Curiosity Scaffold | Domains, question style, exploration policy. |
| 3 | Pedagogy Scaffold | Explanation style, scaffolding, correction, anti-spoonfeeding. |
| 4 | Expression Scaffold | Writing cadence, length norms, tone envelope. |
| 5 | Memory Contract | Memory classes, retention/deletion, sensitive categories, provenance. |
| 6 | Trial Interactions | Scripted scenarios; stability and safety fit. |
| 7 | Readiness Gate | Decision: pass, conditional pass, or fail; blocking issues enumerated. |

---

## Stage 0 — Intake

| | |
|--|--|
| **Purpose** | Establish who the companion is for, operational constraints, and allowed/disallowed domains — plus **operator workspace** preferences for **Cursor** (same survey: optional `cursor_operator_profile` in `seed_intake.json`). |
| **Required inputs** | Operator or guardian context; age band; primary use cases (may be partial at start). Optional: primary IDE, desired **rules pack preset** (`template_steward` / `instance_light` / `instance_operator`), WORK territory hints, whether to **generate `.cursor/` on activation** (future script). |
| **Required outputs** | `seed_intake.json` (see artifacts doc and [cursor-pack-from-seed.md](cursor-pack-from-seed.md)). |
| **Completion criteria** | Intake JSON validates; `completion.coverage_score` meets threshold in [readiness](seed-phase-readiness.md); no unresolved **blocking** contradictions on safety. |
| **Blocking conditions** | Missing age band when minor; empty disallowed_domains when high-risk topics declared; contradictory safety notes left unresolved. |

---

## Stage 1 — Identity Scaffold

| | |
|--|--|
| **Purpose** | Define the companion’s public stance: name, role, relationship to human, voice boundaries. |
| **Required inputs** | Intake constraints; optional founding narrative (prose may live outside JSON). |
| **Required outputs** | `seed_identity.json`. |
| **Completion criteria** | `companion_name`, `role_definition`, `relationship_stance` non-empty; `voice_boundaries` has ≥1 item; `identity_confidence` recorded. |
| **Blocking conditions** | Identity contradicts intake `disallowed_domains`; invariant_values empty when pedagogy requires value anchors. |

---

## Stage 2 — Curiosity Scaffold

| | |
|--|--|
| **Purpose** | Shape how curiosity is expressed and bounded. |
| **Required inputs** | Identity + intake education focus. |
| **Required outputs** | `seed_curiosity.json`. |
| **Completion criteria** | `domains` non-empty; `novelty_policy` and `depth_limits` set. |
| **Blocking conditions** | Domains entirely overlap disallowed_domains; curiosity_confidence below minimum per readiness doc. |

---

## Stage 3 — Pedagogy Scaffold

| | |
|--|--|
| **Purpose** | Teaching stance: scaffolding, difficulty ramp, corrections, encouragement vs spoonfeeding. |
| **Required inputs** | Intake + identity. |
| **Required outputs** | `seed_pedagogy.json`. |
| **Completion criteria** | All pedagogy subfields present; `anti_spoonfeeding_rules` ≥1. |
| **Blocking conditions** | Pedagogy contradicts memory contract on protected regions; pedagogy_confidence below minimum. |

---

## Stage 4 — Expression Scaffold

| | |
|--|--|
| **Purpose** | Output shape: length, format, tone envelope for WRITE/Voice-aligned behavior. |
| **Required inputs** | Identity + pedagogy hints. |
| **Required outputs** | `seed_expression.json`. |
| **Completion criteria** | `writing_cadence`, `length_norms`, `tone_envelope` populated. |
| **Blocking conditions** | Tone conflicts with safety_notes from intake without mitigation. |

---

## Stage 5 — Memory Contract

| | |
|--|--|
| **Purpose** | Govern what may be remembered, edited, deleted, and provenance expectations **before** instance EVIDENCE exists. |
| **Required inputs** | Intake sensitive categories; identity boundaries. |
| **Required outputs** | `seed_memory_contract.json` and **`memory_ops_contract.json`** (MemoryOps: taxonomy, TTL/auto-forget policy, export format, drift thresholds). |
| **Completion criteria** | `memory_classes`, `retention_rules`, `protected_regions`, `provenance_rules` populated; MemoryOps validates and aligns with deletion/export intent. |
| **Blocking conditions** | No deletion rules when sensitive_categories non-empty; editable_regions includes protected_regions without explicit exception. |

**MemoryOps note:** `seed_memory_contract.json` states *what* is governed (regions, classes, provenance). `memory_ops_contract.json` states *how memory is operated* (which taxonomies apply, retention automation, user rights, confidence-drift gates). Both are required at readiness once this template version is in use.

---

## Stage 6 — Trial Interactions

| | |
|--|--|
| **Purpose** | Validate behavior under tutoring, curiosity, correction, ambiguity, refusal, and tone scenarios. |
| **Required inputs** | Scenarios list (may be operator-run); prior stage JSON. |
| **Required outputs** | `seed_trial_report.json`. |
| **Completion criteria** | At least one trial per **required** scenario type in readiness doc; `stability_score` and `safety_fit_score` recorded. |
| **Blocking conditions** | Any trial **fail** on safety-critical scenario; stability below floor in readiness doc. |

---

## Stage 7 — Readiness Gate

| | |
|--|--|
| **Purpose** | **Hard gate:** binary/graded decision whether to activate an instance. Not advisory. |
| **Required inputs** | All prior artifacts + `seed_confidence_map.json`. |
| **Required outputs** | `seed_readiness.json`; human-readable `seed_dossier.md`. |
| **Completion criteria** | `readiness.decision` is `pass` or `conditional_pass` per [seed-phase-readiness.md](seed-phase-readiness.md); manifest lists all artifact paths. |
| **Blocking conditions** | `fail` decision; blocking_issues non-empty when policy requires zero blocking for pass; attempt to activate without dossier sign-off (operator process). |

---

## Relationship to the live Record

Stages 0–7 produce **pre-activation** artifacts only. **Merging into** `users/<id>/self.md`, self-knowledge, self-evidence, etc., happens **after** activation via the instance **identity fork protocol**, not by renaming seed JSON into Record files.

---

*Template doc · evolve via recursion gate in instance repos; template changes bump `seed_phase.version` in manifest.*
