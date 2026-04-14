# Long-horizon work (checkpoints and handoffs)

Grace-Mar can support **long work runs** without treating long-lived **runtime** state as **governed truth**. Checkpoints and handoff packets exist in the **work layer** only: they improve **legibility, resumability, and operator oversight** without replacing observations, memory briefs, review-orchestrator packets, or the gate.

## Doctrine

- **Runtime vs Record:** Checkpoints live under `artifacts/handoffs/` and are **not** SELF, SKILLS, EVIDENCE, or gate staging. See [runtime-vs-record.md](runtime-vs-record.md).
- **Checkpoint first, delegate later:** Prefer emitting a small checkpoint and a bounded next step over speculative autonomy or silent promotion of working notes into durable state.
- **Gate relevance visibility:** Every checkpoint includes a **Gate relevance** field (`none`, `maybe later`, `candidate likely`). This makes **drift toward durable proposals** visible; it does **not** stage candidates or merge into the Record.
- **Complements, not substitutes:** Checkpoints do **not** replace `log_observation.py` rows, `memory_brief.py` output, `build_context_from_observations.py`, or `review_orchestrator.py` packets—they **anchor continuity** across time.
- **Policy mode:** Checkpoints and handoffs may record **`Policy mode:`** (`--policy-mode` on `checkpoint_session.py` / `build_handoff_packet.py`) so resumption does not silently cross [policy envelopes](../policy-modes.md).

## Heuristics (lane dashboard)

The generated [artifacts/lane-dashboards/README.md](../../artifacts/lane-dashboards/README.md) lists, per lane:

- **Latest checkpoint** and **last handoff packet** (if any).
- **Stale (idle):** checkpoint file **mtime** older than **7 days**.
- **Stale (drift):** newest runtime observation **timestamp** for the lane is **newer** than the checkpoint `Built:` line (string compare on ISO timestamps is valid for the usual `YYYY-MM-DDTHH:MM:SSZ` form).

These flags are **hints** for human review, not automation triggers.

## Commands

**Create a checkpoint**

```bash
python3 scripts/runtime/checkpoint_session.py --lane work-strategy --title "Short label"
```

Optional seed from a memory brief (same headings as `memory_brief.py`: Best Matches, Expanded Takeaways):

```bash
python3 scripts/runtime/checkpoint_session.py \
  --lane work-strategy \
  --title "Synthesis" \
  --from-memory-brief path/to/brief.md
```

**Build a handoff packet** (for paste into a new session or operator review):

```bash
python3 scripts/runtime/build_handoff_packet.py \
  --lane work-strategy \
  --latest 3 \
  --output artifacts/handoffs/work-strategy-handoff.md
```

See [artifacts/handoffs/README.md](../../artifacts/handoffs/README.md) for layout and policy.

## Related

- Progressive retrieval: [memory-retrieval.md](memory-retrieval.md)
- Read hints / memory brief: [read-hints.md](read-hints.md)
- Review packets (multi-pass): [../orchestration/review-orchestrator.md](../orchestration/review-orchestrator.md)
