# Governance posture (generated)

_Technical operations summary for this repository instance. **Not** legal, regulatory, or medical compliance advice; for operational visibility and partner conversations only._

- **User id:** `grace-mar`
- **Generated (UTC):** 2026-04-24T16:19:06Z
- **Repo `HEAD` (short):** `93db2f2f`

## Triad (where authority sits)

- **Mind (human):** holds merge authority and meaning.
- **Record:** documented self in `self.md`, evidence in `self-archive.md` — updated **only** through the gated pipeline after companion approval.
- **Voice:** `bot/` renders the Record when queried; it does **not** replace the pipeline. See [docs/conceptual-framework.md](../docs/conceptual-framework.md) for the full distinction.

## No silent merge

1. Proposals land as **`### CANDIDATE-…`** blocks in `recursion-gate.md` (staging).
2. The **companion** approves; the operator runs `python3 scripts/process_approved_candidates.py --apply` (see [AGENTS.md](../AGENTS.md)).
3. **OpenClaw and assistants stage only** — they do not write SELF, EVIDENCE, or `bot/prompt.py` without that merge. Chat is not proof of Record truth.

## Inspectability (what “safe” means here)

Same dimensions as [safety-story-ux.md](../docs/skill-work/work-dev/safety-story-ux.md), with paths for **`users/grace-mar/`**:

| Dimension | Question | Where |
|-----------|----------|-------|
| **Pending vs approved** | Waiting on a human, or already processed? | `users/grace-mar/recursion-gate.md` |
| **Staged vs merged** | Staged only, or written to the Record? | Staging → gate; merge → `process_approved_candidates.py` ([AGENTS.md](../AGENTS.md)) |
| **Receipts** | What batch landed? | `users/grace-mar/merge-receipts.jsonl` |
| **Pipeline events** | Staged vs applied linked? | `users/grace-mar/pipeline-events.jsonl` |
| **Last merge footprint** | Evidence / session line? | `users/grace-mar/self-evidence.md` (if used), `users/grace-mar/session-log.md` |
| **Harness / replay** | Explain a candidate or event? | `users/grace-mar/harness-events.jsonl` + `python3 scripts/replay_harness_event.py` ([harness-replay.md](../docs/harness-replay.md)) |

**Partner-facing line:** *We separate “suggested” from “committed” — receipts and gate state are inspectable on disk.*

## Audit file presence (`grace-mar`)

| Path | Status | Note |
|------|--------|------|
| `users/grace-mar/recursion-gate.md` | present | Gate queue and candidate YAML |
| `users/grace-mar/self.md` | present | Record profile (canonical identity) |
| `users/grace-mar/self-archive.md` | present | EVIDENCE (dated spine) |
| `users/grace-mar/merge-receipts.jsonl` | present | Merge batch receipts (append-only) |
| `users/grace-mar/pipeline-events.jsonl` | present | Pipeline staged vs applied |
| `users/grace-mar/harness-events.jsonl` | present | Harness / audit-lane events |
| `users/grace-mar/session-log.md` | present | Session and merge footnotes |
| `users/grace-mar/self-evidence.md` | present | Optional ACT pointer / alternate evidence entry |

## Verification (copy-paste)

Replace the user id if needed.

```bash
python3 scripts/validate-integrity.py --user grace-mar
python3 scripts/run_voice_benchmark.py -o users/grace-mar/artifacts/voice_benchmark_results.json
python3 scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0000   # example; use a real id
python3 scripts/report_governance_posture.py -u grace-mar
```

Further reading: [voice-benchmark-suite.md](../docs/voice-benchmark-suite.md), [openclaw-integration.md](../docs/openclaw-integration.md).

---

_Operator / audit lane only. For identity truth, use approved Record files under `users/`. This file is derived and safe to regenerate._
