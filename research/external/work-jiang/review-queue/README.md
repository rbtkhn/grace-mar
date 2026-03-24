# Review Queue — agent-produced work staging

Agent-produced content lands here before promotion to canonical locations. Nothing in `review-queue/` is authoritative until the operator approves and promotes it.

## Structure

```
review-queue/
  ch07/
    draft.md              # Chapter draft
    predictions.json      # Extracted predictions for registration
    notes.md              # Agent reasoning / decision log
  asr/
    replacements-sh08.txt # Proposed ASR replacement rules
  pedagogy/
    method-notes-sh07.md  # Pedagogical analysis notes
  archive/                # Promoted items moved here
```

## Workflow

1. Agent completes a task and places output in `review-queue/<scope>/`
2. Agent runs `emit_task_event.py submit <task_id>` to mark the task as submitted
3. Operator reviews the content
4. Operator promotes: `python3 scripts/work_jiang/promote_from_review_queue.py <scope> --approve`
5. Script moves files to canonical locations and marks the task as merged

## Promotion targets

| Review-queue path | Canonical destination |
|---|---|
| `ch<NN>/draft.md` | `chapters/ch<NN>/draft.md` |
| `ch<NN>/predictions.json` | `prediction-tracking/staging/` |
| `ch<NN>/notes.md` | `chapters/ch<NN>/notes.md` |
| `asr/replacements-*.txt` | Manual merge into `asr_transcript_replacements.py` |
| `pedagogy/*.md` | Operator discretion |

## Related

- [MULTI-AGENT.md](../MULTI-AGENT.md) — full conventions
- [tasks.jsonl](../tasks.jsonl) — task manifest
