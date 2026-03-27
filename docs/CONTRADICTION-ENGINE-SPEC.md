# CONTRADICTION-ENGINE-SPEC

**Status:** implementation-ready engineering spec  
**Purpose:** define a first-class contradiction and change-review engine for Grace-Mar that upgrades conflict handling from a passive flag into a governed identity-diff workflow.  
**Scope:** `recursion-gate.md`, review UI, merge logic, temporal validity, and audit events.  
**Non-Goal:** replace the canonical queue, bypass the human gate, or introduce autonomous merge authority.

**Primary sources:**  
- [readme.md](../readme.md)
- [approval-inbox-spec.md](approval-inbox-spec.md)
- [contradiction-resolution.md](contradiction-resolution.md)
- [contradiction-timeline.md](contradiction-timeline.md) (time-ordered view; pipeline + git)
- [apps/gate-review-app.py](../apps/gate-review-app.py)
- [scripts/generate_gate_dashboard.py](../scripts/generate_gate_dashboard.py)

**See also (template doctrine, local mirrors):** [change-review.md](change-review.md), [contradiction-policy.md](contradiction-policy.md), [change-types.md](change-types.md), [change-review-lifecycle.md](change-review-lifecycle.md); [companion-self CONTRADICTION-ENGINE-SPEC](https://github.com/rbtkhn/companion-self/blob/main/docs/CONTRADICTION-ENGINE-SPEC.md) — instance-agnostic mirror; template spec operationalizes the doctrine.

---

## 1. Goal

Turn contradiction handling into a first-class review flow that answers:

**How should the identity model change in light of new evidence?**

This engine must:
- detect when a staged candidate materially conflicts with an active SELF or SKILLS claim
- render a structured “before / proposed / after” diff
- require an explicit human resolution type
- preserve full history
- update active state deterministically after approval
- keep all actions audit-visible

This is a **review and merge-governance layer**, not a replacement memory system.

---

## 2. Architectural Constraints (MUST PRESERVE)

The engine must preserve these already-established rules:

- the agent may stage; it may not merge
- `recursion-gate.md` remains the canonical queue
- `status: pending | approved | rejected` remains the canonical candidate state
- approved candidates remain in queue until merge runs
- all review actions remain audit-visible through `pipeline-events.jsonl`
- derived UI fields and helper artifacts are allowed
- no second source of truth may be introduced

Contradiction handling must therefore be implemented as:

1. canonical staged candidate in queue  
2. derived contradiction analysis object  
3. explicit operator resolution  
4. deterministic merge into canonical profile/history files

---

## 3. Problem Statement

Current contradiction handling is useful but incomplete.

Today:
- staging can already detect some contradictions
- contradictions are surfaced in candidate YAML
- user resolution is required
- history preservation is the intended rule

But the current workflow still presents the operator primarily with a **candidate**, not with an **identity change decision**.

The actual user decision is rarely:
> “Should I approve this candidate?”

The real decision is:
> “Does this new evidence reinforce, refine, contextualize, contradict, or replace the current model of the person?”

This spec formalizes that distinction.

---

## 4. Product Definition

A **contradiction** is not merely a flagged candidate.

A contradiction becomes a **first-class identity-diff object** when all of the following are true:

- there is an active existing claim in SELF or SKILLS
- a staged candidate materially overlaps the same domain, topic, or trait
- the relationship is not best explained as simple reinforcement or duplication
- a human reviewer would reasonably need to decide how the active model should change

Examples:
- “fearful of swimming” vs “joined swim team confidently”
- “dependent in group work” vs “independent self-starter in projects”
- “dislikes drawing” vs repeated observed drawing enthusiasm

---

## 5. Relation Classification Model

Before contradiction UI is shown, every staged candidate MUST be classified into one of these relation types against relevant active entries:

### 5.1 `reinforcement`
The new evidence strengthens an existing claim.

Action:
- no contradiction workflow
- allow standard review path
- optional confidence increase / evidence append on merge

### 5.2 `duplicate`
The candidate restages substantially the same claim.

Action:
- show duplicate hint
- no contradiction workflow unless operator overrides
- merge may be rejected as redundant

### 5.3 `refinement`
The candidate narrows, qualifies, or contextualizes an existing claim without displacing it.

Action:
- show refinement marker
- standard review path or light contextual-merge path

### 5.4 `contradiction`
The candidate materially competes with the active interpretation.

Action:
- contradiction workflow required
- quick merge disabled
- explicit resolution required before merge

---

## 6. Canonical vs Derived Data

### 6.1 Canonical
Canonical sources remain:

- `users/<id>/recursion-gate.md`
- `users/<id>/self.md`
- `users/<id>/skills.md`
- `users/<id>/self-evidence.md`
- `users/<id>/pipeline-events.jsonl`

### 6.2 Derived
The engine may generate structured sidecar artifacts, for example:

- `users/<id>/derived/conflicts/CONFLICT-0001.json`
- `users/<id>/derived/conflict-index.json`
- dashboard-only computed fields

Derived artifacts are disposable and rebuildable. Prefer **gitignore** on `users/*/derived/` so they are not treated as a second canonical layer in version control (regenerate from queue + profile).

They must never outrank the canonical queue or profile files.

---

## 7. Contradiction Object Schema

Each contradiction MUST be represented as a structured object.

Example:

```json
{
  "conflict_id": "CONFLICT-0007",
  "candidate_id": "CANDIDATE-0142",
  "status": "pending_review",
  "profile_target": "IX-C",
  "mind_category": "personality",

  "existing_entry_id": "PER-0018",
  "existing_claim_text": "fearful of swimming in deep water",
  "existing_claim_confidence": 0.82,
  "existing_claim_valid_from": "2025-09-12",
  "existing_claim_valid_until": null,

  "incoming_evidence_id": "ACT-0039",
  "incoming_summary": "joined swim team and completed first practice confidently",
  "incoming_excerpt": "She got in confidently and finished the drills.",
  "incoming_evidence_confidence": 0.88,

  "relationship_type": "contradiction",
  "conflict_strength": 0.91,
  "confidence_delta": 0.37,
  "recommended_resolution": "growth",

  "why_flagged": [
    "same domain: swimming",
    "semantic opposition detected",
    "same profile lane IX-C",
    "new evidence is more recent"
  ],

  "prompt_impact": {
    "has_prompt_change": true,
    "sections": ["personality", "activities"],
    "estimated_behavioral_impact": "medium"
  },

  "operator_decision": null,
  "operator_note": null,
  "resolved_at": null,
  "resolved_by": null
}
```

### 7.1 Required fields

* `conflict_id`
* `candidate_id`
* `status`
* `existing_entry_id`
* `incoming_summary`
* `relationship_type`
* `conflict_strength`
* `recommended_resolution`

### 7.2 Optional fields

* `prompt_impact`
* `confidence_delta`
* `incoming_excerpt`
* `operator_note`
* `resolved_by`

---

## 8. Scoring Model

The engine MUST compute three distinct scores.

### 8.1 Existing Claim Confidence

How strong is the current active claim?

Inputs may include:

* count of supporting evidence refs
* recency
* source diversity
* number of confirmations
* whether claim came from seed only or repeated observation

Range:

* `0.00` to `1.00`

### 8.2 Incoming Evidence Confidence

How strong is the new evidence?

Inputs may include:

* operator observation vs inferred summary
* artifact-backed vs text-only
* specificity
* freshness
* corroboration

Range:

* `0.00` to `1.00`

### 8.3 Conflict Strength

How strongly do the two claims collide?

Inputs may include:

* semantic opposition
* same topic/domain
* same context
* same profile lane
* low coexistence probability

Range:

* `0.00` to `1.00`

### 8.4 Confidence Delta

A derived estimate of how much the active interpretation should move if the candidate is approved.

Use:

* queue prioritization
* review fatigue reduction
* prompt-impact triage

---

## 9. Resolution Types

The contradiction-resolution vocabulary is fixed:

* `growth`
* `correction`
* `context`
* `reject_new`
* `exception`

Every contradiction resolution MUST choose one.

### 9.1 `growth`

Meaning:

* the old claim was true then
* the new claim is true now

Merge behavior:

* old entry remains in history
* old entry gets `valid_until` and/or `superseded_by`
* new entry becomes active
* developmental arc is preserved

### 9.2 `correction`

Meaning:

* the old claim was wrong
* the new evidence corrects it

Merge behavior:

* old entry remains in history
* old entry becomes inactive as corrected
* new entry becomes active
* do not imply developmental change

### 9.3 `context`

Meaning:

* both claims can be true in different settings

Merge behavior:

* neither entry is discarded
* both entries receive context qualifiers
* state resolver becomes scope-aware

### 9.4 `reject_new`

Meaning:

* operator rejects the new evidence or interpretation

Merge behavior:

* no active-state change
* candidate remains in review history as rejected
* rejection reason logged

### 9.5 `exception`

Meaning:

* the contradiction is real but not stable enough to generalize

Merge behavior:

* both retained
* no supersession
* mark incoming evidence as limited-scope or edge case

---

## 10. Temporal Validity Model

Temporal validity is required for contradiction handling to become coherent.

Every entry touched by contradiction resolution SHOULD support:

* `valid_from`
* `valid_until`
* `superseded_by`
* `active`
* `resolution`
* `resolution_note`

Example superseded entry:

```yaml
id: PER-0018
observation: "fearful of swimming in deep water"
evidence_refs:
  - ACT-0011
valid_from: 2025-09-12
valid_until: 2026-02-25
superseded_by: PER-0029
resolution: growth
resolution_note: "Overcame earlier fear; joined swim team."
active: false
confidence: 0.82
```

Example successor entry:

```yaml
id: PER-0029
observation: "overcame earlier fear of deep water; joined swim team"
evidence_refs:
  - ACT-0039
valid_from: 2026-02-25
valid_until: null
active: true
confidence: 0.88
```

### 10.1 Active-state rule

Fork state at time `T` is computed from entries where:

* `valid_from <= T`
* and (`valid_until` is null or `valid_until > T`)

---

## 11. Review UI Requirements

Every contradiction review card MUST show:

### 11.1 Before

* existing claim text
* entry id
* confidence
* evidence refs
* active date range

### 11.2 Proposed

* candidate summary
* source excerpt
* incoming evidence confidence
* conflict reasons
* recommended resolution
* conflict strength

### 11.3 After

A live preview of:

* resulting active claim(s)
* superseded entry changes
* date validity changes
* confidence changes
* prompt-impact preview

### 11.4 Required user actions

* choose resolution type
* add optional operator note
* approve / reject / defer
* confirm prompt impact when present

---

## 12. Queue and Risk Rules

Contradiction candidates MUST be treated as review-escalated items.

### 12.1 Quick merge rule

Any candidate with a contradiction object attached is **not** `quick_merge_eligible`.

### 12.2 Risk tier

Contradiction candidates default to:

* `manual_escalate`

unless future policy explicitly introduces narrower subclasses.

### 12.3 Derived UI fields

The inbox/dashboard MAY compute and render:

* `has_conflict_markers`
* `conflict_strength`
* `recommended_resolution`
* `prompt_impact_level`
* `duplicate_vs_contradiction`
* `stale_conflict_age_days`

These fields are not written back to canonical queue text unless a deliberate schema upgrade is adopted.

---

## 13. API Surface

The contradiction engine should be exposed as helper endpoints on the **operator review layer** (e.g. [apps/gate-review-app.py](../apps/gate-review-app.py) or the browser inbox described in [approval-inbox-spec.md](approval-inbox-spec.md)), not necessarily the companion Mini App server.

### 13.1 `GET /api/review/conflicts`

Returns unresolved contradiction objects.

Query params:

* `status`
* `profile_target`
* `mind_category`
* `min_conflict_strength`
* `prompt_impact`
* `age_days_gt`

### 13.2 `GET /api/review/conflicts/<conflict_id>`

Returns one full contradiction review payload, including before/proposed/after render data.

### 13.3 `GET /api/review/preview/<candidate_id>`

Returns merge preview without committing any changes.

### 13.4 `POST /api/review/conflicts/<conflict_id>/resolve`

Request body:

```json
{
  "decision": "growth",
  "note": "This is development, not a bad earlier claim.",
  "approve_candidate": true,
  "apply_prompt_delta": true
}
```

Behavior:

* validates that candidate is still pending
* validates conflict object exists
* validates decision is in allowed resolution set
* writes review action to audit log
* transitions queue state or merge receipt as allowed by existing governance

### 13.5 `GET /api/review/history`

Returns resolved contradiction events for audit/history UI.

---

## 14. Merge Logic

### Step 1 — Staging

Candidate is appended to the canonical queue as usual.

### Step 2 — Detection

Detection layer compares candidate to relevant active SELF/SKILLS entries.

### Step 3 — Classification

Candidate is classified as:

* reinforcement
* duplicate
* refinement
* contradiction

### Step 4 — Conflict object generation

If contradiction:

* generate derived `CONFLICT-*` object
* mark review payload with `has_conflict_markers: true`
* disable quick merge path

### Step 5 — Human resolution

Operator chooses:

* `growth`
* `correction`
* `context`
* `reject_new`
* `exception`

### Step 6 — Merge execution

Resolution-specific merge updates:

* canonical queue status
* SELF/SKILLS entries
* evidence refs
* temporal validity metadata
* prompt deltas if approved
* pipeline events

### Step 7 — History persistence

Write contradiction-specific audit events and retain derived conflict object or archive summary.

---

## 15. Audit Events

All contradiction lifecycle events MUST be written to `pipeline-events.jsonl`.

Recommended events:

```json
{"ts":"2026-03-18T09:12:44Z","event":"conflict_detected","candidate_id":"CANDIDATE-0142","conflict_id":"CONFLICT-0007","existing_entry_id":"PER-0018","relationship":"contradiction","conflict_strength":0.91}
{"ts":"2026-03-18T09:14:02Z","event":"conflict_resolved","candidate_id":"CANDIDATE-0142","conflict_id":"CONFLICT-0007","decision":"growth","operator":"operator-web"}
{"ts":"2026-03-18T09:14:03Z","event":"identity_superseded","old_entry_id":"PER-0018","new_entry_id":"PER-0029","resolution":"growth"}
{"ts":"2026-03-18T09:14:04Z","event":"prompt_delta_applied","candidate_id":"CANDIDATE-0142","sections":["personality","activities"]}
```

These events are additive.
They do not replace the existing queue state model.

---

## 16. Dashboard Requirements

The gate dashboard ([generate_gate_dashboard.py](../scripts/generate_gate_dashboard.py)) should be extended with a contradiction review section.

### 16.1 New summary metrics

* unresolved contradictions
* high-severity contradictions
* likely growth items
* likely corrections
* stale contradictions > N days
* contradictions with prompt impact
* contradiction count by lane (`IX-A`, `IX-B`, `IX-C`, `SKILLS`)

### 16.2 Saved review views

* `likely_growth`
* `likely_correction`
* `needs_context_split`
* `prompt_impact_high`
* `duplicate_not_conflict`
* `stale_unresolved`

### 16.3 Card display

Conflict cards should be visually distinct from ordinary pending candidates.

Minimum visible fields in collapsed state:

* candidate id
* existing entry id
* summary
* conflict strength
* recommended resolution
* age
* prompt-impact badge

Expanded state must include before/proposed/after details.

---

## 17. Prompt Safety Rule

Because approved changes may affect profile and prompt together, contradiction resolution MUST never silently change the emulation prompt.

Rule:

* every contradiction card must compute prompt impact
* any prompt delta must be previewed
* operator must explicitly allow prompt update when prompt impact exists
* audit trail must record whether prompt delta was applied

---

## 18. File and Script Additions

Recommended new files:

* `docs/CONTRADICTION-ENGINE-SPEC.md` (this doc)
* `docs/CONTRADICTION-ENGINE-FLOW.md` (detect → review → merge pseudocode)
* `docs/schemas/conflict-object.schema.json` (JSON Schema for §7 object)
* `scripts/build_conflict_index.py`
* `scripts/resolve_conflict.py`
* `scripts/render_conflict_cards.py`

Recommended new directories:

* `users/<id>/derived/conflicts/` (typically gitignored)

Recommended existing files to extend:

* `scripts/generate_gate_dashboard.py`
* queue parsing/review helpers
* merge tooling (`scripts/process_approved_candidates.py`)
* gate-review-app (or inbox server)
* pipeline event writers

---

## 19. Implementation Phases

### Phase 1 — Detection + sidecar generation

* classify candidate relationships
* generate `CONFLICT-*` sidecars
* add contradiction counts to dashboard

### Phase 2 — Review UI

* before/proposed/after rendering
* manual resolution selection
* prompt-impact preview

### Phase 3 — Temporal merge

* add `valid_from`, `valid_until`, `superseded_by`
* recompute active state from dates

### Phase 4 — Analytics

* conflict heatmap
* volatility by lane
* unresolved conflict aging
* reviewer-fatigue metrics

---

## 20. Minimum Viable Version

A version is MVP-complete when it can:

* detect contradiction vs duplicate vs reinforcement
* generate a derived contradiction object
* render contradiction cards in the review surface
* require one resolution type before merge
* write supersession metadata on merge
* emit contradiction lifecycle events

That is sufficient to turn contradiction handling from a passive flag into a governed identity revision workflow.

---

## 21. Design Principle

**Never ask the operator to approve a raw candidate when the real question is how the identity model should change.**

That principle governs this entire spec.

---

## 22. Related artifacts

| Artifact | Path |
|----------|------|
| Flow (pseudocode) | [CONTRADICTION-ENGINE-FLOW.md](CONTRADICTION-ENGINE-FLOW.md) |
| JSON Schema | [schemas/conflict-object.schema.json](schemas/conflict-object.schema.json) |

---

*Reference implementation: Grace-Mar. Template mirror: companion-self `docs/CONTRADICTION-ENGINE-SPEC.md`.*
