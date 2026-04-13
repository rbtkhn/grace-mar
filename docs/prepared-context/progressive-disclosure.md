# Progressive disclosure for prepared context

Prepared context should follow **index → timeline slice → full expansion**, not raw notebook dumps in the default path.

## Layers

1. **Compact index** — Runtime observation summaries (see `scripts/prepared_context/build_context_index.py`), lane compressions, or brief pointers. Mark clearly as **runtime / work-lane** material.
2. **Timeline slice** — Short chronological neighborhood around a selected `obs_id` (use `scripts/runtime/lane_timeline.py`).
3. **Full expansion** — Bounded fields via `scripts/runtime/expand_observations.py` (explicit IDs only).
4. **Prepared-context bundle** — `scripts/prepared_context/build_context_from_observations.py` emits a lane-scoped Markdown block (see [observation-expansion.md](../runtime/observation-expansion.md)).

## Truth boundary

Content assembled this way may cite **runtime observations** and WORK artifacts. It must **not** be labeled as approved Record truth until merged through `recursion-gate.md` and `process_approved_candidates.py`.

See [prepared-context/README.md](../../prepared-context/README.md), [runtime-vs-record.md](../runtime-vs-record.md), and [memory-retrieval.md](../runtime/memory-retrieval.md).
