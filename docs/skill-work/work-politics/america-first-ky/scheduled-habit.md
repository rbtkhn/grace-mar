# Scheduled habit (cron) — America-First-KY

**Purpose:** Copy-paste examples for **operator** automation. Nothing here merges the Record or edits `bot/prompt.py` automatically.

**Rules:** Use `python3` (or activate your venv), `cd` to the repo root first. Cron on macOS/Linux — use `crontab -e`; test commands manually before relying on cron.

---

## Safe commands (WORK only)

| Habit | Example command | Why it is safe |
|-------|-----------------|----------------|
| Morning brief | `cd /path/to/grace-mar && python3 scripts/generate_wap_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md` | Writes markdown under `docs/`; no SELF/EVIDENCE merge |
| Daily loop scaffold | `cd /path/to/grace-mar && python3 scripts/scaffold_daily_loop_brief.py morning` | Writes only under [america-first-ky/](.) |
| Loop pipeline event | `cd /path/to/grace-mar && python3 scripts/emit_loop_event.py --phase started territory=wap` | Appends JSONL to `users/<user>/pipeline-events.jsonl` only |
| Stress-test brief | `cd /path/to/grace-mar && python3 scripts/scaffold_stress_test_brief.py war-powers-vote` | Same folder as daily scaffold |

Replace `/path/to/grace-mar` with your clone path (or `$HOME/Documents/grace-mar`).

---

## `emit_loop_event.py` wrapper

Maps `--phase` to event types documented in [README.md](README.md):

| `--phase` | `event_type` |
|-----------|----------------|
| `started` | `loop_cycle_started` |
| `staged` | `loop_cycle_staged` |
| `approved` | `loop_cycle_approved` |

Example:

```bash
python3 scripts/emit_loop_event.py -u grace-mar --phase started territory=wap
python3 scripts/emit_loop_event.py --phase staged cycle=daily-loop-brief
```

Equivalent without the wrapper:

```bash
python3 scripts/emit_pipeline_event.py -u grace-mar loop_cycle_started none territory=wap
```

---

## Example crontab lines (illustrative)

```cron
# 06:05 local — daily work-politics/strategy brief (adjust path and user)
5 6 * * * cd /path/to/grace-mar && /usr/bin/python3 scripts/generate_wap_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +\%Y-\%m-\%d).md >> /tmp/grace-mar-brief.log 2>&1

# 06:10 — optional loop event audit trail only
10 6 * * * cd /path/to/grace-mar && /usr/bin/python3 scripts/emit_loop_event.py --phase started source=cron >> /tmp/grace-mar-loop.log 2>&1
```

**Note:** In crontab, `%` must be escaped as `\%` in the `date` command line.

---

## Non-goals

- Do **not** run `process_approved_candidates.py` or edit `users/` from cron without explicit human approval design.
- Do **not** paste shell blocks that append to `governance_checker.py` or `skills.md` — see [AGENT-SESSION-BRIEF.md](AGENT-SESSION-BRIEF.md).
