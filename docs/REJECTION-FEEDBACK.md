# Rejection Feedback — Learning from Pipeline Rejections

**Purpose:** Capture optional "why" when rejecting pipeline candidates. Use this feedback to refine the analyst and reduce future low-signal staging.

---

## How It Works

1. **When rejecting via button** (Telegram /review): No reason is captured. Event is still emitted as `rejected`.

2. **When rejecting via command**: Use `/reject CANDIDATE-123 [reason]` to add optional feedback:
   ```
   /reject CANDIDATE-0045 too trivial
   /reject CANDIDATE-0041 not actually a signal
   ```

3. **Pipeline event**: Rejections with reason are logged in `PIPELINE-EVENTS.jsonl`:
   ```json
   {"ts": "...", "event": "rejected", "candidate_id": "CANDIDATE-0045", "rejection_reason": "too trivial"}
   ```

4. **Operator workflow**: When processing the review queue manually, you can add `summary:` to rejected blocks in PENDING-REVIEW (e.g. "Barbie — watched during sleepover; user rejected"). For programmatic capture, use `/reject` with reason or run:
   ```
   python scripts/emit_pipeline_event.py rejected CANDIDATE-0045 rejection_reason="too trivial"
   ```

---

## Using Feedback to Improve the Analyst

Periodically review rejections with reasons:

```bash
grep '"event":"rejected"' users/grace-mar/PIPELINE-EVENTS.jsonl | grep rejection_reason
```

Consider:
- Adding negative examples to `ANALYST_PROMPT` (e.g. "Do NOT stage: X")
- Tightening the Rules section ("Only flag GENUINE signals...")
- Updating the dedup list or priority_score guidance

Do not over-tighten — some rejections are subjective. Use feedback to reduce clear false positives (trivial, already-known, not-a-signal).

---

## See Also

- AGENTS.md § Gated Pipeline
- PIPELINE-MAP.md
- bot/prompt.py (ANALYST_PROMPT)
