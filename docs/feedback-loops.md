# Feedback Loops — Grace-Mar

**Purpose:** Document feedback mechanisms that close the loop between pipeline actions and outcomes. Optional; operator records when helpful.

---

## Proactive proposal brief

Generate 3–5 concrete activities from Record, INTENT, LIBRARY, and gaps:

```bash
python scripts/proposal_brief.py -u grace-mar
python scripts/proposal_brief.py -u grace-mar -n 5
```

Output: proposed activities with rationale. Companion chooses what to do. Run before a session or via cron.

---

## Calibrate-on-miss

When the companion reports "Voice didn't know X" or "that was wrong", stage a candidate to fix the Record:

```bash
python scripts/calibrate_from_miss.py -u grace-mar --miss "Voice didn't know we went to the aquarium"
python scripts/calibrate_from_miss.py -u grace-mar --miss "Voice gave wrong Casa Bonita date" --suggested "Add to IX-A: Casa Bonita reopened 2023"
```

See [rejection-feedback.md](rejection-feedback.md) for rejection reasons.

---

## Closed-loop verification

Optional events to record whether pipeline actions had impact.

### Export used

After running `openclaw_hook` or `export_user_identity`, if the export was consumed in an OpenClaw session:

```bash
python scripts/emit_pipeline_event.py export_used none export_id=<short_id> used_in_openclaw=true
```

Manual; helps economic benchmarks (Record → OpenClaw delivery).

### Merge feedback

After a merge, record whether it helped (e.g. next session felt better, Voice recalled correctly):

```bash
python scripts/emit_pipeline_event.py merge_feedback CANDIDATE-0040 helpful=true
python scripts/emit_pipeline_event.py merge_feedback CANDIDATE-0041 helpful=false note="Voice still didn't use it"
```

Manual; supports tuning and benchmark (merge quality).

---

## Oversight cadence

For long OpenClaw sessions, run heartbeat every 2–4 hours:

```bash
python scripts/openclaw_heartbeat.py -u grace-mar
```

See [openclaw-integration.md](openclaw-integration.md) § Oversight cadence.

---

## Low-friction approval

For low-risk candidates (single IX target, no conflicts, no advisory flags), operators can one-tap approve:

- **In /review:** Click ✅ Approve — if low-risk, merges immediately (no receipt step).
- **Command:** `/approve CANDIDATE-0040` — same behavior for operator chats.

Set `GRACE_MAR_OPERATOR_NAME` for merge audit. Higher-risk candidates use the normal /merge receipt flow.

---

## See also

- [rejection-feedback.md](rejection-feedback.md) — rejection reasons
- [openclaw-integration.md](openclaw-integration.md) — session continuity, heartbeat
- [work-build-ai/economic-benchmarks.md](skill-work/work-build-ai/economic-benchmarks.md) — metrics sources
