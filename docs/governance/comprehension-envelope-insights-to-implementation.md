# Comprehension Envelope — insights extraction → implementation design

**Status:** WORK / governance design artifact (not Record truth).  
**Purpose:** Satisfy the insights-to-implementations workflow (operator plan under `.cursor/plans/` — do not treat this file as that plan file).  
**Audience:** Repo owner and companion deciding whether to ship the Comprehension Envelope PR sequence.

---

## Phase 1 — Insight table (atomic findings)

Tag legend: `must_fix` | `should_fix` | `defer` | `reject` | `already_solved`

Boundary legend: `runtime` | `gate` | `review-queue` | `Record` | `notebook` | `observability` | `docs_only`

| # | Insight | Tag | Boundary | Depends on | Blocks |
|---|---------|-----|----------|------------|--------|
| 1 | New requirement must **not** reuse the name “Tier 0/1/2” for traffic/quick-merge semantics; repo already defines **gate traffic** tiers ([recursion-gate-three-tier.md](../recursion-gate-three-tier.md)) and machine `risk_tier` (`quick_merge_eligible` / `review_batch` / `manual_escalate`). | must_fix | gate, docs_only | None | All UX copy and schema field names |
| 2 | Introduce a **distinct** concept: `comprehension_tier` or `envelope_class` (`none` \| `optional` \| `required`) with an explicit **“not the same as `risk_tier`”** mapping table. | must_fix | docs_only | #1 | Templates, validators |
| 3 | `change-proposal.v1.json` already has `riskLevel`, `queueSummary`, `materiality`; envelope bullets must **complement** summaries, not duplicate them (authoring rule). | should_fix | review-queue | Proposal path chosen | JSON PR |
| 4 | “Strategy-significant notebook” is undefined; triggers must be **operational** (path prefix, `[promote]`, touch to `STRATEGY.md`, or explicit YAML tag). | should_fix | notebook, gate | Operator convention agreed | Tier assignment |
| 5 | PR1 should pick **one authoring surface**: markdown blocks in `recursion-gate.md` **or** JSON proposals — not both as equal sources of truth without a declared primary. | must_fix | gate | #2 | Validation scope |
| 6 | Validation behavior must be explicit: **warn-only** vs **exit non-zero** before `process_approved_candidates.py`; companion workflow must stay aligned with [AGENTS.md](../../AGENTS.md). | should_fix | gate | #5 | Merge scripts |
| 7 | “Tier 1 optional / recommended” is hard to enforce without noise; v1 can ship **required vs not required** only. | should_fix | docs_only | None | Template complexity |
| 8 | Extend `change-proposal` schema + merge script checks for envelope fields. | defer | review-queue | Stable envelope shape in markdown | Early PR quality |
| 9 | Gate-review UI highlights missing envelope for required class. | defer | gate | Markdown/schema stable | Reviewer experience |
|10 | Observability / SKILLS / EVIDENCE enrichment from envelope text. | defer | observability | Real examples in gate | Dashboard PRs |
|11 | Rename existing `risk_tier` machine values to match comprehension tiers. | reject | gate | N/A | Would break [recursion_gate_review.py](../../scripts/recursion_gate_review.py) consumers |
|12 | Collapse gate vs change-review boundaries for speed. | reject | gate | N/A | Violates [gate-vs-change-review.md](../gate-vs-change-review.md) |

**Deduplication note:** “Right membrane” (gate vs runtime) appears once as #1–#2; purpose/rationale prose from the draft PR collapses into **Phase 2 thesis**.

**Stop check:** Every `must_fix` / `should_fix` row has boundary + dependency; no orphan tasks.

---

## Phase 2 — Design note (minimum viable)

### Thesis (one sentence)

After merge, **high-impact gate candidates** can carry a **short, structured Comprehension Envelope** (operator understanding: what / why / blast radius / override) that is **required only** when `envelope_class` is `required`, without changing Record schema or merge authority.

### Authoring surface (PR1 recommendation)

| Choice | Primary for PR1 | Rationale |
|--------|------------------|-----------|
| **Markdown** — `### Comprehension Envelope` under each `### CANDIDATE-XXXX` block in `users/<id>/recursion-gate.md` | **Yes** | Companion-facing, matches current staging; no schema migration. |
| **JSON** — optional fields on `review-queue/proposals/*.json` | **Defer** | Add in a follow-on PR once heading shape is stable; avoid double validation. |

**Source of truth for PR1:** the **gate markdown file**. Proposals may later mirror envelope text; until then, escalations exported to change-review carry gate context in the export flow as today.

### Field names (machine)

Use **`envelope_class`** (avoid `tier` alone): `none` | `optional` | `required`.

Optional YAML frontmatter per candidate (future): `envelope_class: required` — only if markdown parsing proves brittle; not required for PR1.

### Comprehension Envelope block (canonical)

```markdown
### Comprehension Envelope
- What this is:
- Why this path:
- Why not the next-best option:
- Blast radius:
- Assumptions / fragile points:
- Human override applied:
```

Authoring rules: 1–2 sentences per bullet; concrete surfaces; `unknown` allowed; no motivational filler; do not restate full diff.

### Validation story (PR1)

- **Minimum:** Documentary — companion / operator checks before approve.
- **PR2–3:** Optional script `scripts/validate_gate_comprehension_envelope.py --user <id>` that:
  - for each pending candidate with `envelope_class: required` (from convention or tag), checks for non-empty `### Comprehension Envelope` and non-empty first line under each bullet **or** exits 1.
- **`process_approved_candidates.py`:** Do not block merge in PR1; add optional `--strict-envelope` later if companion wants hard fail.

### Anti-goals (max five)

1. No second “tier ladder” that renames or overloads `risk_tier` / IFP Tier 1–3.
2. No collapse of **gate** vs **change-review** ([gate-vs-change-review.md](../gate-vs-change-review.md)).
3. No mandatory long-form essays or AI tone scoring.
4. No SKILLS/EVIDENCE/observability pipelines in the first implementation PR.
5. No universal envelope for every candidate.

### Files touched (estimated)

| Area | Files |
|------|--------|
| Doctrine | This file; [comprehension-envelope-gate.md](comprehension-envelope-gate.md) (vocabulary + mapping); link from [recursion-gate-three-tier.md](../recursion-gate-three-tier.md) |
| Template | [users/_template/recursion-gate.md](../../users/_template/recursion-gate.md); optional instance README under `users/` |
| Validation | New script under `scripts/` (follow-on PR) |
| UI | [apps/gate-review-app.py](../../apps/gate-review-app.py) (follow-on PR) |
| Schema | [schema-registry/change-proposal.v1.json](../../schema-registry/change-proposal.v1.json) (defer) |

### Acceptance criteria (design phase complete)

- [x] Insight table with boundaries and dependencies.
- [x] Single primary authoring path for v1 (markdown gate).
- [x] Distinct naming (`envelope_class` vs `risk_tier`).
- [x] Validation story documented (soft then strict optional).
- [x] Ordered PR list below.

---

## Phase 3 — PR sequence (6 PRs)

### PR1 — Doctrine: two systems + envelope vocabulary

- **Purpose:** Add [comprehension-envelope-gate.md](comprehension-envelope-gate.md) (mapping: traffic `risk_tier` vs `envelope_class`). Link from [recursion-gate-three-tier.md](../recursion-gate-three-tier.md) § See also.
- **Why first:** Prevents operator confusion before any template or code.
- **Capability:** Shared language; no behavior change.
- **Acceptance:** Doc merged; See also link; no contradictions with IFP / gate-vs-change-review.
- **Anti-goals:** No template edits; no validator.

### PR2 — Template: stub + `users/_template` + guidance

- **Purpose:** Add Comprehension Envelope stub and `envelope_class` guidance to [users/_template/recursion-gate.md](../../users/_template/recursion-gate.md) and short operator blurb in docs.
- **Why second:** New instances get correct shape.
- **Capability:** Copy-paste correctness.
- **Acceptance:** Template renders; examples for `none` vs `required` classes.
- **Anti-goals:** No CI enforcement yet.

### PR3 — Validation script (optional CI)

- **Purpose:** `scripts/validate_gate_comprehension_envelope.py` — parse `recursion-gate.md` for `CANDIDATE-*` + envelope heading; warn or `--strict` exit 1.
- **Why third:** Shape is stable from PR2.
- **Capability:** Mechanical check for missing required envelopes when tagging convention exists.
- **Acceptance:** Dry-run on template; docs for flags.
- **Anti-goals:** Do not wire to merge script without companion approval.

### PR4 — Gate-review UI: scan order + prominence

- **Purpose:** [apps/gate-review-app.py](../../apps/gate-review-app.py) (or doc-only if UI minimal): show envelope block first for `required` class; flag missing.
- **Why fourth:** Human scan path after automation exists.
- **Capability:** Reviewer UX.
- **Acceptance:** Screenshot or behavior note in PR; missing envelope visible for required class.
- **Anti-goals:** No Record writes.

### PR5 — Change-proposal optional fields (mirror)

- **Purpose:** Optional `envelope` object or parallel fields in [schema-registry/change-proposal.v1.json](../../schema-registry/change-proposal.v1.json) for review-queue proposals; validation in `validate-change-review.py` path.
- **Why fifth:** JSON path catches material escalations.
- **Capability:** Single envelope when proposal is SSOT for that change.
- **Acceptance:** Schema validates; one fixture example.
- **Anti-goals:** Do not require proposals to duplicate gate markdown for the same candidate without migration note.

### PR6 — Examples + rollout note

- **Purpose:** Add 2 worked examples (Tier `none` / `required`) in docs; “Phase 2 refine tiers” note.
- **Why last:** Training material after machinery exists.
- **Capability:** Onboarding.
- **Acceptance:** Examples copy-paste clean.
- **Anti-goals:** No new scope creep.

**Follow-on (not in this sequence):** observability of envelope completion rate; human-override ledger export; archival summaries.

---

## Running example — Comprehension Envelope critique → implementation handles

| Critique / insight | Implementation handle |
|--------------------|------------------------|
| Tier name collision with gate traffic tiers | PR1 + `envelope_class` vocabulary doc |
| Duplicate `riskLevel` / `queueSummary` | Authoring rule: envelope complements summary; one line in template |
| “Strategy-significant” vague | Tie `required` to explicit triggers: e.g. `targetSurface` in `SELF`, `bot/prompt.py`, `schema-registry/*`, `STRATEGY.md`, `export` / handoff paths — list in [comprehension-envelope-gate.md](comprehension-envelope-gate.md) |
| Markdown vs JSON both | PR1 markdown primary; PR5 JSON mirror |
| Validation failure mode undefined | Phase 2: soft human + optional script; `--strict` documented; merge script unchanged until companion asks |
| Tier 1 “recommended” fuzzy | v1: only `none` vs `optional` vs `required`; drop “recommended” or map `optional` to soft lint only |

---

## Reject list (v1)

| Idea | Reason |
|------|--------|
| Merge envelope into SKILLS or EVIDENCE as proof | Out of scope; gate-local first |
| Public-by-default proof | Contradicts governance-first posture |
| Mandatory envelope on every candidate | Explicit non-goal |
| AI judgment of “comprehension quality” | Non-goal; style not scored |
| Rename `risk_tier` values | Breaks [recursion_gate_review.py](../../scripts/recursion_gate_review.py) |
| Single tier system merging traffic + comprehension | Collapses two orthogonal axes |

---

## Deliverables checklist (plan)

- [x] Insight table (Phase 1) — § Phase 1
- [x] Design note with single authoring surface for v1 (Phase 2) — § Phase 2
- [x] Six PR titles in order with acceptance criteria (Phase 3) — § Phase 3
- [x] Reject list — § Reject list

---

## See also

- [recursion-gate-three-tier.md](../recursion-gate-three-tier.md) — traffic tiers
- [gate-vs-change-review.md](../gate-vs-change-review.md)
- [identity-fork-protocol.md](../identity-fork-protocol.md)
- [AGENTS.md](../../AGENTS.md) — Sovereign Merge Rule
