# Handoffs and session checkpoints

**Runtime work layer only.** Contents here are **not** Record truth. They exist so long-running work stays **legible, resumable, and reviewable** without conflating runtime scaffolding with governed state (`SELF`, `EVIDENCE`, `recursion-gate.md`). See [docs/runtime/long-horizon-work.md](../../docs/runtime/long-horizon-work.md).

## Layout

| Path | Role |
|------|------|
| `checkpoints/` | Dated session checkpoints (`checkpoint_session.py`). Safe to commit or keep local; not authoritative. |
| `*.md` (under this folder, not under `checkpoints/`) | Handoff packets built by `build_handoff_packet.py` for operator paste/resume. |

## Commands

**New checkpoint** (writes `checkpoints/YYYY-MM-DD_<lane>_<title-slug>.md`):

```bash
python3 scripts/runtime/checkpoint_session.py \
  --lane work-strategy \
  --title "Iran negotiation synthesis checkpoint"
```

Optional seed from a memory brief:

```bash
python3 scripts/runtime/checkpoint_session.py \
  --lane history-notebook \
  --title "Notebook closeout" \
  --from-memory-brief prepared-context/memory-brief.md
```

**Handoff packet** (bundles recent checkpoints ± optional memory brief):

```bash
python3 scripts/runtime/build_handoff_packet.py \
  --lane work-strategy \
  --latest 3 \
  --output artifacts/handoffs/work-strategy-handoff.md
```

```bash
python3 scripts/runtime/build_handoff_packet.py \
  --lane history-notebook \
  --include-memory-brief prepared-context/memory-brief.md \
  --include-checkpoint artifacts/handoffs/checkpoints/2026-04-14-history-notebook_notebook-closeout.md \
  --output artifacts/handoffs/history-notebook-handoff.md
```

## Policy

- Checkpoints and handoffs **do not** replace observations, memory briefs, or review-orchestrator packets; they **summarize continuity** for humans and agents.
- **Gate relevance** fields are **visibility only** — they do not stage candidates.
- Regenerate aggregate navigation with `python3 scripts/build_lane_dashboards.py` to surface latest checkpoint/handoff hints on the lane dashboard README.
