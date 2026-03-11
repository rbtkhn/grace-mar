# work-health-fitness

**Digital trainer.** work-health-fitness is a multi-user health and fitness support layer: it can handle multiple users, each with their own profile (growth baseline, preferences, goals). The trainer supports — sleep, movement, nutrition, recovery — in a companion-led way: it offers structure and prompts; it does not prescribe.

**Current users:** Abigail (Abby), Hannah. Profiles live in `users/grace-mar/`: `health-fitness-profile.md` (Abigail), `health-fitness-profile-hannah.md` (Hannah).

---

## Purpose

| Role | Description |
|------|-------------|
| **Digital trainer** | One capability layer serving multiple users. Per-user profiles (identity, growth baseline, preferences) inform prompts, wisdom questions, and optional lesson/checkpoint integration. |
| **User-led** | Each user (or their caregiver) sets goals and pacing. The trainer supports; it does not compel. Meet where they are (AGENTS rule 7). |

work-health-fitness does not prescribe; it offers structure and prompts that each user can adopt, adapt, or ignore.

---

## Users and profiles

| User | Profile file | Notes |
|------|--------------|-------|
| **Abigail** (Abby) | [health-fitness-profile.md](../../../users/grace-mar/health-fitness-profile.md) | First user; growth baseline and movement preferences documented. |
| **Hannah** | [health-fitness-profile-hannah.md](../../../users/grace-mar/health-fitness-profile-hannah.md) | Second user; profile placeholder. |

Additional users: add `health-fitness-profile-<slug>.md` in `users/grace-mar/` and list here.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Digital trainer framing, users, scope, and principles. |
| **[roadmap.md](roadmap.md)** | Phased roadmap: Phase 0 (Record-only) → Phase 1 (USDA lookup) → Phase 2 (single-source API) → Phase 3 (Terra aggregation) → Phase 4 (agentic). APIs, constraints, and design guardrails. |

---

## Principles

1. **Meet each user where they are** — No pushing through resistance. If a user deflects or shows resistance, respect the boundary. (AGENTS rule 7.)
2. **User-led** — Health and fitness goals, pacing, and activities are set by the user (or caregiver). The trainer supports; it does not compel.
3. **Evidence-based** — When the trainer or Voice offers suggestions, base them on that user's documented profile (preferences, growth baseline) or on safe, general principles. Calibrated abstention when outside knowledge.
4. **Integrate with existing flows** — Health/fitness can be woven into lesson prompts, wisdom questions, or checkpoint reflections when the user consents.

---

## Cross-references

- [Architecture](../../architecture.md) — Tricameral mind, companion sovereignty
- [AGENTS.md](../../../AGENTS.md) — Rule 7 (meet where they are), gated pipeline
- [CHAT-FIRST-DESIGN](../../chat-first-design.md) — Deliver within chat; bounded sessions
