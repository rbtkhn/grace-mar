# Operator Weekly Review — Checklist

**Purpose:** Recommended rhythm for operators to maintain the pipeline and keep the Record current. Adapted from Second Brain patterns — see [SECOND-BRAIN-PATTERNS](SECOND-BRAIN-PATTERNS.md) §4.

**Governed by:** [GRACE-MAR-CORE v2.0](GRACE-MAR-CORE.md)

---

## Checklist (30 minutes or less)

Block time weekly — e.g. Sunday evening or Monday morning. All steps optional but recommended.

| Step | Action | Time |
|------|--------|------|
| 1 | **Experience check** — *Did the Voice feel like the companion's Record when it knew, and clearly offer help when it didn't? Did abstention/lookup feel like honesty and support, not failure or deflection?* Note any drift; adjust prompt or add probes if the experience felt wrong. See [KNOWLEDGE-BOUNDARY-FRAMEWORK](KNOWLEDGE-BOUNDARY-FRAMEWORK.md) §1. | ~2 min |
| 2 | **Process PENDING-REVIEW** — Open `users/[id]/PENDING-REVIEW.md`. Review each pending candidate. Approve or reject. Run merge for approved (tell the assistant: "process the review queue"). If using CLI directly, generate + pass an approval receipt (`scripts/process_approved_candidates.py --generate-receipt ...` then `--apply --receipt ...`). | ~15 min |
| 3 | **Rotate MEMORY + SELF-ARCHIVE** — Run `python3 scripts/rotate_context.py --user [id] --apply` (or `/rotate` in Telegram) to prune dated MEMORY entries older than TTL and rotate SELF-ARCHIVE when thresholds are exceeded. | ~5 min |
| 4 | **Skim SESSION-TRANSCRIPT** — Glance at recent raw conversation in `users/[id]/SESSION-TRANSCRIPT.md`. Note resistance, recurring topics, and continuity cues for next session. SELF-ARCHIVE holds only approved/merged content. | ~5 min |
| 5 | **Optional: Gap Hunter** — When reviewing an exchange, ask: *What's missing in the Record for this exchange?* Surfaces candidates the analyst might have missed. Stage to PENDING-REVIEW if you find gaps. | ~5 min |
| 6 | **Optional: PRP refresh** — If merges were applied, run `python scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt` and commit. Keeps the anchor in sync. | ~2 min |

---

## Gap Hunter (operator prompt)

When reviewing an exchange or SESSION-TRANSCRIPT chunk, ask yourself:

> **What's missing in the Record for this exchange?**

- New knowledge, curiosity, or personality not yet in SELF?
- Something the user said or did that would enrich the profile but wasn't staged?
- A follow-up question the operator could ask to deepen the Record?

If you spot a gap, stage a candidate to PENDING-REVIEW manually (or describe it for the assistant to stage). This supplements automated analyst signal detection.

---

## Rationale

- **Process queue** — Prevents PENDING-REVIEW from growing unbounded. Human gates what enters the Record.
- **Rotate MEMORY** — Keeps ephemeral context fresh; avoids stale tone or resistance notes.
- **Skim SESSION-TRANSCRIPT** — Builds continuity; operator enters the next week with context.
- **PRP refresh** — Ensures PRP/URL bootstrap reflects the latest Record.
- **Reminder automation** — Set `GRACE_MAR_OPERATOR_CHAT_ID` and reminder env vars to receive operator-only queue-health nudges.

---

## Integration

- **AGENTS.md** — Operator in Pipeline mode follows this rhythm when processing.
- **SECOND-BRAIN-PATTERNS** — Pattern 4 (Weekly Review) and Pattern 5 (Two-Minute Rule) apply.
- **Meet them where they are** — If resistance notes exist in MEMORY, honor them; don't push.
