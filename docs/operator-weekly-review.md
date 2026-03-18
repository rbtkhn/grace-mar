# Operator Weekly Review — Checklist

**Purpose:** Recommended rhythm for operators to maintain the pipeline and keep the Record current. Adapted from Second Brain patterns — see [SECOND-BRAIN-PATTERNS](second-brain-patterns.md) §4.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md)

---

## Checklist (30 minutes or less)

Block time weekly — e.g. Sunday evening or Monday morning. All steps optional but recommended.

| Step | Action | Time |
|------|--------|------|
| 1 | **Experience check** — *Did the Voice feel like the companion's Record when it knew, and clearly offer help when it didn't? Did abstention/lookup feel like honesty and support, not failure or deflection?* Note any drift; adjust prompt or add probes if the experience felt wrong. See [KNOWLEDGE-BOUNDARY-FRAMEWORK](knowledge-boundary-framework.md) §1. | ~2 min |
| 2 | **Process RECURSION-GATE** — **Without opening markdown:** [Operator Console](operator-console.md) `/operator/console` or [Approval Inbox](approval-inbox-spec.md) `/operator/inbox`: approve/reject; then **Merge approved (companion)** (or all / WAP) to write the Record. Or CLI receipt flow. **With files:** `operator_gate_snapshot.py`; or open `recursion-gate.md` and approve in Cursor + merge. | ~15 min |
| 3 | **Rotate MEMORY + SELF-ARCHIVE** — Run `python3 scripts/rotate_context.py --user [id] --apply` (or `/rotate` in Telegram) to prune dated MEMORY entries older than TTL and rotate SELF-ARCHIVE when thresholds are exceeded. | ~5 min |
| 4 | **Skim SESSION-TRANSCRIPT** — Glance at recent raw conversation in `users/[id]/session-transcript.md`. Note resistance, recurring topics, and continuity cues for next session. SELF-ARCHIVE holds only approved/merged content. | ~5 min |
| 5 | **Intake vs IX (when you read/studied with the companion)** — (1) Log **READ-*** (or relevant evidence) and update **skill-think** if needed. (2) **Separately** stage/approve **RECURSION-GATE** candidates for IX-A/B/C if you want those facts or interests in SELF. THINK does not auto-merge to IX. See [we-read-think-self-pipeline.md](we-read-think-self-pipeline.md). | ~5 min |
| 6 | **Optional: Gap Hunter** — When reviewing an exchange, ask: *What's missing in the Record for this exchange?* Surfaces candidates the analyst might have missed. Stage to RECURSION-GATE if you find gaps. | ~5 min |
| 7 | **Optional: PRP refresh** — If merges were applied, run `python scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt` and commit. Keeps the anchor in sync. | ~2 min |
| 8 | **Optional: Template sync** — When companion-self (template) has been updated, pull upgrades into grace-mar per [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md): diff template paths, merge into grace-mar's docs, validate, log the sync. Not needed every week; do when template or instance governance changes. | ~10 min |

---

## Feedback loops

- **Calibrate-on-miss** — When Voice missed or was wrong: `python scripts/calibrate_from_miss.py -u [id] --miss "…"` (see [feedback-loops.md](feedback-loops.md))
- **Closed-loop verification** — Optional: `emit_pipeline_event.py export_used` and `merge_feedback` for benchmarks

## Gap Hunter (operator prompt)

When reviewing an exchange or SESSION-TRANSCRIPT chunk, ask yourself:

> **What's missing in the Record for this exchange?**

- New knowledge, curiosity, or personality not yet in SELF?
- Something the user said or did that would enrich the profile but wasn't staged?
- A follow-up question the operator could ask to deepen the Record?

If you spot a gap, stage a candidate to RECURSION-GATE manually (or describe it for the assistant to stage). This supplements automated analyst signal detection.

---

## Rationale

- **Feed the gate** — During the week, say **"we did X"** in Telegram (or submit an observation in the [Operator Console](operator-console.md) Observe tab) after calls, readings, decisions, milestones so the agent stages candidates. See [we-did-x-habit.md](we-did-x-habit.md). The gate then reflects real activity; weekly review has real items to approve or reject.
- **Process queue** — Prevents RECURSION-GATE from growing unbounded. Human gates what enters the Record.
- **Rotate MEMORY** — Keeps ephemeral context fresh; avoids stale tone or resistance notes.
- **Skim SESSION-TRANSCRIPT** — Builds continuity; operator enters the next week with context.
- **PRP refresh** — Ensures PRP/URL bootstrap reflects the latest Record.
- **Reminder automation** — Set `GRACE_MAR_OPERATOR_CHAT_ID` and reminder env vars to receive operator-only queue-health nudges.

---

## Integration

- **agents.md** — Operator in Pipeline mode follows this rhythm when processing.
- **SECOND-BRAIN-PATTERNS** — Pattern 4 (Weekly Review) and Pattern 5 (Two-Minute Rule) apply.
- **Meet them where they are** — If resistance notes exist in MEMORY, honor them; don't push.
