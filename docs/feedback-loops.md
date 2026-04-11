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

**Framing:** Rejecting bad AI output + staging a fix = **encoding taste** (see [design-notes §11.10](design-notes.md#1110-rejection-as-skill--recognition-articulation-encoding), [implementable-insights §13](implementable-insights.md#13-rejection-as-skill--recognition-articulation-encoding)).
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

**Manual only** — not emitted automatically at merge time; supports tuning and benchmark (merge quality). Do not treat it as a substitute for **instrumented** metrics (e.g. median review time by tier), which would require separate pipeline logging. See [recursion-gate-three-tier.md](recursion-gate-three-tier.md) § Metrics.

---

## Oversight cadence

For long OpenClaw sessions, run heartbeat every 2–4 hours:

```bash
python scripts/openclaw_heartbeat.py -u grace-mar
```

See [openclaw-integration.md](openclaw-integration.md) § Oversight cadence.

---

## Low-friction approval

**Bronze reference mode:** Every merge still goes through companion approval; this path is **low-friction UX** inside [identity-fork-protocol.md](identity-fork-protocol.md) §9.3 **Bronze** (manual each change). Future **Silver/Gold** batch modes are separate and not the same as “fast lane.”

**Machine eligibility** matches `ready_for_quick_merge` in [scripts/recursion_gate_review.py](../scripts/recursion_gate_review.py): among other checks, **`profile_target` must match IX-A/B/C** (`^IX-[ABC]\.`), with no multi-target, conflict markers, advisory flags, or duplicate hints. See [recursion-gate-three-tier.md](recursion-gate-three-tier.md) § Tier 1.

For eligible candidates, operators can one-tap approve:

- **In /review:** Click ✅ Approve — if low-risk, merges immediately (no receipt step).
- **Command:** `/approve CANDIDATE-0040` — same behavior for operator chats.

Set `GRACE_MAR_OPERATOR_NAME` for merge audit. Higher-risk candidates use the normal /merge receipt flow.

---

## See also

- [rejection-feedback.md](rejection-feedback.md) — rejection reasons
- [openclaw-integration.md](openclaw-integration.md) — session continuity, heartbeat
- [work-build-ai/economic-benchmarks.md](skill-work/work-build-ai/economic-benchmarks.md) — metrics sources
- [recursion-gate-three-tier.md](recursion-gate-three-tier.md) — tier lanes, metrics (instrumented vs manual)
