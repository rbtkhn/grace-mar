# Skill-work-health-fitness — Roadmap

**Status:** Draft. Phases are aspirational; implementation requires companion approval and aligns with AGENTS rules (gated pipeline, meet where they are).

---

## Phase 0 — Foundation (current)

**Scope:** Record-only. No external APIs. Voice supports health/fitness via documented preferences and wisdom questions.

| Deliverable | Description |
|-------------|-------------|
| Record-driven prompts | Companion documents health preferences (e.g., sleep goals, movement type) in SELF or MEMORY. Lesson prompts, wisdom questions, or checkpoint reflections can reference them when companion consents. |
| Wisdom questions | Add health/fitness questions to [wisdom-questions.md](../../wisdom-questions.md) — e.g., "how did you sleep last night?", "what movement felt good today?" — optional, companion-led. |
| Integration with existing flows | Health cues woven into `generate_lesson_prompt.py` or checkpoint flows only when companion has documented interest. |

**No API integration.** All data flows from companion self-report or operator input.

---

## Phase 1 — Manual / lookup support

**Scope:** Nutrition lookup via public APIs. Voice can answer nutrition questions using USDA data; no companion account linkage.

| Deliverable | Description |
|-------------|-------------|
| USDA FoodData Central | [fdc.nal.usda.gov/api-guide](https://fdc.nal.usda.gov/api-guide) — Free, public domain. Add lookup path: companion asks "how much protein in X?" → Voice queries USDA → rephrase in Record voice. Calibrated abstention for foods not in database. |
| Record alignment | Answers framed by companion's Lexile, interests. No health data stored in Record; lookup is ephemeral. |

**APIs:** USDA FoodData Central (free, data.gov key).

---

## Phase 2 — Opt-in single-source integration

**Scope:** Companion links one wearable or app. Data used for contextual prompts only; minimal Record footprint.

| Option | API | Data | Use case |
|--------|-----|------|----------|
| **Strava** | [developers.strava.com](https://developers.strava.com) | Activities, runs, rides | Companion runs or cycles; Voice can reference "you ran 3 miles today" in checkpoints if companion opts in. |
| **Oura** | [developer.ouraring.com](https://developer.ouraring.com) | Sleep, readiness, stress | Companion wears Oura; Voice can gently note "readiness was lower today" only when companion asks. |
| **Fitbit** | [dev.fitbit.com](https://dev.fitbit.com) | Sleep, steps, HR, nutrition | Broad metrics; companion already on Fitbit. |
| **Garmin** | [developer.garmin.com](https://developer.garmin.com) | Steps, HR, sleep, workouts | Runner/athlete companion. Approval required. |

**Constraints:**
- Companion must explicitly link account. OAuth flow; revocable.
- Data used for Voice context (e.g., "you slept 6 hours — want to talk about rest?") — never auto-pushed.
- No raw health data in Record unless companion approves via pipeline (e.g., "add sleep goal to MEMORY").
- Meet where they are: if companion deflects, drop the topic.

---

## Phase 3 — Aggregation (multi-source)

**Scope:** One integration for 500+ sources. Companion links preferred devices; Terra normalizes and pushes via webhook.

| Product | API | Benefit |
|---------|-----|---------|
| **Terra** | [docs.tryterra.co](https://docs.tryterra.co) | Single integration for Garmin, Fitbit, Oura, Strava, Apple Health (via SDK), Google Fit, etc. Webhook-based; standardized JSON. |

**Use case:** Companion uses multiple devices (e.g., Oura + Strava). One backend receives all data; Voice has unified view for contextual prompts when companion opts in.

**Constraints:** Same as Phase 2 — companion-led, minimal Record footprint, no prescription.

---

## Phase 4 — Proactive / agentic (future)

**Scope:** Agentic Voice proposes health-aware prompts (e.g., "readiness was low — want a lighter lesson today?") — still proposal-only; companion approves.

| Capability | Description |
|------------|-------------|
| Proactive cues | Voice notices patterns (e.g., low sleep 3 nights) and offers reflection or lighter pacing — never prescribes. |
| Integration with lesson generator | `generate_lesson_prompt.py` can accept optional health context (e.g., energy level) to modulate intensity. |
| Agentic Legos | Health data as one input to agentic Voice; combined with Record, lookup, pipeline. |

**Requires:** Phase 2 or 3 data; agentic Voice (AGENTS.md notes future agentic). Companion remains sovereign.

---

## Design guardrails (all phases)

1. **Companion-led** — Goals, pacing, and data sharing are companion choices. System supports; does not compel.
2. **Meet where they are** — No pushing through resistance. Respect deflection. (AGENTS rule 7.)
3. **Minimal Record footprint** — Health data stays in external systems or ephemeral context. Only companion-approved summaries enter Record (e.g., "companion prefers morning movement").
4. **Privacy** — Sensitive data. Minimal retention; clear consent; revocable links.
5. **Gated pipeline** — Any health-derived content for SELF/EVIDENCE goes through PENDING-REVIEW. Agent stages; companion merges.

---

## Summary

| Phase | APIs | Record impact | Companion action |
|-------|------|---------------|------------------|
| 0 | None | Preferences in SELF/MEMORY | Self-report |
| 1 | USDA FoodData Central | None | Asks nutrition questions |
| 2 | Strava, Oura, Fitbit, or Garmin | Optional MEMORY | Links one account |
| 3 | Terra (aggregation) | Optional MEMORY | Links multiple sources |
| 4 | Same as 2 or 3 | Same | Agentic proposals; companion approves |
