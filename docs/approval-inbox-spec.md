# Approval Inbox Spec

**Status:** implementation-ready product spec

**Purpose:** define a first-class approval inbox for `RECURSION-GATE` that reduces operator fatigue without weakening the Sovereign Merge Rule.

**Primary sources:** `docs/identity-fork-protocol.md`, `docs/pipeline-map.md`, `docs/operator-weekly-review.md`, `docs/web-app-plan.md`, `docs/miniapp-setup.md`, `users/grace-mar/recursion-gate.md`, `bot/core.py`, `bot/bot.py`, `scripts/process_approved_candidates.py`, `scripts/generate_gate_dashboard.py`, `apps/miniapp_server.py`

---

## 1. Goal

Turn the current markdown queue plus Telegram review helpers into one browser-first operator surface that:

- shows all pending candidates in a structured inbox
- lets the operator approve, reject, batch-review, or defer candidates
- preserves the existing human gate exactly
- reuses current queue shape, quick-merge rules, and pipeline event logging

This is a **review surface**, not a new memory system. The inbox surfaces the existing gate; it does not replace it.

---

## 2. Current System Constraints

The spec must preserve these already-implemented rules:

- The agent may stage. It may not merge.
- `recursion-gate.md` remains the canonical queue.
- `status: pending | approved | rejected` remains the canonical candidate state field inside the queue.
- Approved candidates remain above `## Processed` until merge runs.
- Quick merge is only allowed for candidates that already satisfy `bot/core.py:is_low_risk_candidate()`.
- Receipt-based merge remains the default batch merge path.
- All review actions must stay audit-visible through `pipeline-events.jsonl`.

The inbox may add **derived UI fields** and **helper endpoints**, but it must not create a second source of truth.

**Contradiction workflow:** Candidates that require an identity-diff decision (not just approve/reject) follow [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md): escalation, before/proposed/after, resolution types, no quick-merge on active contradictions.

---

## 3. User Problem

Today the operator has three fragmented review modes:

- edit `recursion-gate.md` manually
- review one-by-one in Telegram with `A / R / N / Q`
- use a read-only HTML dashboard with no actions

This creates friction:

- hard to scan many candidates at once
- hard to see duplicates or risk level quickly
- hard to batch obvious approvals or rejections
- hard to distinguish "safe to quick-merge" from "needs human thought"
- hard to keep web review aligned with the exact markdown queue and audit trail

The inbox should make review legible and fast while keeping final judgment human.

---

## 4. Non-Goals

- No autonomous merge path
- No direct editing of `self.md`, `self-evidence.md`, or `bot/prompt.py`
- No replacement of `recursion-gate.md`
- No silent dedupe that alters candidate text automatically
- No new agent authority beyond staging and existing quick-merge rules

---

## 5. Canonical Candidate Card

Each inbox row renders one candidate block from `recursion-gate.md`.

### 5.1 Stored fields

These come directly from the markdown YAML when present:

```yaml
id: CANDIDATE-XXXX
status: pending | approved | rejected
timestamp: 2026-02-24 14:07:50
channel_key: telegram:343513797
territory: work-politics | omitted
source: operator-submitted homework artifacts
mind_category: knowledge | curiosity | personality | skills_build | ...
signal_type: knowledge | engagement | value | checkpoint / we_did | ...
priority_score: 1-5
summary: short operator-facing summary
profile_target: IX-A. KNOWLEDGE
example_from_exchange: quoted excerpt
source_exchange: nested source context
suggested_entry: proposed Record addition
prompt_section: YOUR KNOWLEDGE
prompt_addition: proposed prompt delta
suggested_followup: optional next question
```

### 5.2 Derived UI fields

These are computed at render time and are not written back into the queue:

```yaml
risk_tier: quick_merge_eligible | review_batch | manual_escalate
territory_label: Companion | Work-politics | other
age_days: integer
has_conflict_markers: true | false
has_prompt_change: true | false
has_multi_target: true | false
has_artifact_payload: true | false
duplicate_hints:
  - CANDIDATE-0084 overlaps existing IX-A Mars knowledge
ready_for_quick_merge: true | false
```

### 5.3 Card layout

Each card should show, in this order:

1. `candidate_id`
2. `risk_tier` badge
3. `territory` badge
4. `mind_category` and `signal_type`
5. `summary`
6. `profile_target`
7. source line: `channel_key`, `source`, timestamp, age
8. expandable detail section:
   - `example_from_exchange` or short `source_exchange`
   - `suggested_entry`
   - `prompt_addition`
   - duplicate hints
   - audit trail snippet

The collapsed state should be enough for triage; the expanded state should be enough for judgment.

---

## 6. Risk Tiers

Risk tiers are UI labels that map directly to current governance.

### 6.1 `quick_merge_eligible`

Definition: candidate satisfies the current low-risk rule already implemented in `bot/core.py:is_low_risk_candidate()`.

Criteria:

- `status: pending`
- exactly one `profile_target`
- target is one of `IX-A`, `IX-B`, or `IX-C`
- no conflict markers in the candidate block
- no recent `intent_constitutional_critique` event with `status=advisory_flagged`

Allowed actions:

- approve + quick merge
- approve only
- reject
- defer

### 6.2 `review_batch`

Definition: candidate is structurally normal but not safe for automatic quick merge.

Typical reasons:

- multi-target profile update
- includes prompt additions across multiple sections
- work/context evidence needs human interpretation
- candidate has richer artifact payload or follow-up judgment

Allowed actions:

- approve
- reject
- defer
- include in a selected batch for receipt-based merge

### 6.3 `manual_escalate`

Definition: candidate needs especially careful review.

Triggers:

- explicit conflict or contradiction markers
- advisory-flagged intent event
- unclear provenance
- duplicate pressure against an existing IX lane
- unusually broad or operator-sensitive candidate

Allowed actions:

- reject
- defer
- approve only after expanding details

The UI should visually slow the operator down here: expanded by default, warning color, no inline quick-merge affordance.

---

## 7. Filters And Views

The inbox needs fast filters because fatigue is mostly a scanning problem.

Required filters:

- `status`: pending, approved-not-yet-merged, rejected
- `risk_tier`
- `territory`
- `mind_category`
- `channel`
- `age`: today, 7d+, 30d+
- `has_duplicate_hint`
- `quick_merge_eligible`

Required sort options:

- newest first
- oldest first
- highest priority first
- quick-merge eligible first

Required saved views:

- `All pending`
- `Quick approvals`
- `Needs judgment`
- `Work-politics`
- `Companion`
- `Approved awaiting merge`

---

## 8. Actions

### 8.1 Single-candidate actions

- `Approve`
- `Reject`
- `Defer`
- `Approve + quick merge` when `risk_tier=quick_merge_eligible`

Behavior:

- `Approve` writes `status: approved` via the same status update path used today.
- `Reject` writes `status: rejected` and optionally records `rejection_reason`.
- `Defer` writes nothing; it is a UI-only state for the current session.
- `Approve + quick merge` first approves, then calls the existing quick-merge flow.

### 8.2 Batch actions

- `Approve selected`
- `Reject selected`
- `Generate merge batch`

Behavior:

- batch approve updates each selected pending candidate to `approved`
- batch reject updates each selected pending candidate to `rejected`
- merge batch creates a receipt for currently approved selected candidates and shows the exact apply step

The first version does **not** need multi-candidate quick merge. Quick merge stays single-candidate.

---

## 9. Dedupe And Merge Suggestions

The inbox should not auto-rewrite candidates, but it should surface likely duplication.

### 9.1 Duplicate hint rules

Show a duplicate hint when any of these are true:

- same `profile_target` and highly similar `summary`
- same `profile_target` and same `suggested_entry`
- same `channel_key` plus same or near-identical `example_from_exchange`
- candidate appears to restage knowledge already present in `self.md`
- candidate appears to overlap another pending candidate in the same lane

### 9.2 Suggestion types

- `Likely duplicate of existing IX entry`
- `Likely duplicate of pending candidate CANDIDATE-XXXX`
- `Possible fold: combine with candidate CANDIDATE-XXXX before approve`
- `Prompt addition appears empty or redundant`

### 9.3 Operator choices when dedupe appears

- approve only one candidate
- reject the weaker duplicate
- defer both and edit the markdown manually if a combined candidate is better

The inbox should encourage cleaner review, not automatic synthesis.

---

## 10. Post-Action State Model

### 10.1 Canonical state transitions

```text
pending
  -> approved
  -> rejected

approved
  -> merged
  -> merge_failed
  -> reverted_to_pending (rare manual correction)

rejected
  -> terminal in queue history
```

### 10.2 Storage rules

- `pending`, `approved`, and `rejected` live in `recursion-gate.md`
- `merged` is represented by movement under `## Processed` with action text written by merge tooling
- `merge_failed` is not a queue state; it is an event-state visible in the audit trail
- `deferred` is a UI session label only, not a persisted queue status

---

## 11. Audit Trail Behavior

Every action from the inbox must emit pipeline events with enough context to reconstruct review history.

Required event behavior:

- approve -> `approved`
- reject -> `rejected`
- quick merge success -> existing applied/merge events from merge tooling
- merge failure -> `validation_failed` or merge stderr surfaced to operator

Each event should include when available:

```json
{
  "ts": "2026-03-13T12:34:56",
  "event": "approved",
  "candidate_id": "CANDIDATE-0084",
  "channel_key": "miniapp:approval_inbox",
  "actor": "operator:web",
  "source": "approval_inbox"
}
```

Rejections should support an optional short reason chosen from common categories plus free text:

- duplicate
- too weak
- unclear provenance
- not merge-ready
- contradicts Record
- other

This keeps rejection data usable for future operator-fatigue analysis.

---

## 12. API Surface

The first implementation should add authenticated operator endpoints to `apps/miniapp_server.py`.

### 12.1 Read endpoints

- `GET /operator/approval-inbox`
  - returns structured pending and approved-not-yet-merged candidates as JSON
- `GET /operator/approval-inbox/<candidate_id>`
  - returns one fully expanded card payload
- `GET /operator/approval-inbox/health`
  - returns queue stats and recent audit summary

### 12.2 Write endpoints

- `POST /operator/approval-inbox/<candidate_id>/approve`
- `POST /operator/approval-inbox/<candidate_id>/reject`
- `POST /operator/approval-inbox/<candidate_id>/quick-merge`
- `POST /operator/approval-inbox/batch/approve`
- `POST /operator/approval-inbox/batch/reject`
- `POST /operator/approval-inbox/batch/receipt`

Auth should reuse `OPERATOR_FETCH_SECRET` bearer auth in the first pass.

---

## 13. Implementation Path

### Phase 1: Structured read model

Reuse the existing markdown parsing logic from `scripts/generate_gate_dashboard.py` and `bot/core.py`.

Deliver:

- structured parser shared by dashboard, bot review, and inbox API
- JSON endpoint for pending candidates
- browser page that renders cards, filters, and risk badges

### Phase 2: Review actions

Reuse existing write paths rather than inventing new ones.

Single-candidate actions:

- call `update_candidate_status()` for approve/reject
- call `quick_merge_candidate()` only when `ready_for_quick_merge=true`

Batch actions:

- use a new thin wrapper around `scripts/process_approved_candidates.py --generate-receipt`
- allow the operator to download or preview the receipt before apply

### Phase 3: Merge handoff

For approved candidates:

- show the exact command or API-backed apply step
- show success/failure state
- refresh the inbox so merged candidates disappear from pending views

The first implementation should prefer **browser/miniapp operator review** over Telegram changes, because the browser already has authenticated fetch surfaces and the dashboard already exists.

---

## 14. UI Requirements

Required UX details:

- cards must support keyboard navigation
- bulk select must work on desktop and mobile
- detail drawers should preserve scroll position
- warning badges must be visually obvious but not noisy
- default landing view should be `Quick approvals` + `Needs judgment` counts side by side

Recommended layout:

- left rail or top tabs for saved views
- main grid/list of cards
- right-side detail pane on desktop; expandable drawer on mobile
- top summary strip:
  - pending count
  - approved awaiting merge
  - oldest pending age
  - quick-merge eligible count

---

## 15. Acceptance Criteria

The inbox is complete when:

- an operator can review the queue without opening `recursion-gate.md`
- quick-merge eligible items are visibly distinct from normal approvals
- the UI never bypasses the existing human gate or low-risk rule
- approve/reject actions leave a usable event trail
- batch review is faster than the current markdown or Telegram flow
- another developer can implement from this spec without redesigning the state model

---

## 16. Open Questions For Implementation

These do not block the spec, but the implementer must choose:

- whether the first UI lives under `miniapp/` or a new `profile/review/` surface
- whether receipt generation stays CLI-backed or gets a small Python wrapper callable from Flask
- whether duplicate hints inspect only pending candidates first, or also current `self.md` in v1

Recommended default:

- UI in the existing miniapp/web surface
- Python wrapper for receipt generation
- duplicate hints against both pending candidates and current `self.md`

