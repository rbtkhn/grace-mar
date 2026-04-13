# Read hints (soft)

Grace-Mar’s analogue to “file-read decision” tools elsewhere: **surface relevant runtime observations** before you re-open a large file or notebook. This is a **hinting layer**, not a block — the operator or companion always chooses whether to read again.

See [memory-retrieval.md](memory-retrieval.md) for the full retrieval stack.

## Principles

- **Suggest, do not deny** — Never block `read()`; print recommendations only.
- **Compact first** — List observation IDs and titles; no full `notes` dumps in the default path.
- **No mutation** — Does not write `recursion-gate.md`, SELF, SKILLS, or other Record surfaces.

## `read_hint.py`

Before reopening a path or revisiting a topic:

```bash
python3 scripts/runtime/read_hint.py \
  --lane work-strategy \
  --path docs/strategy-notebook.md

python3 scripts/runtime/read_hint.py \
  --lane history-notebook \
  --query "corridor connectivity"
```

- Provide **at least one** of `--path` or `--query` (`-q`).
- Optional `--lane` restricts the pool (exact lane string).
- `--limit` caps listed observations (default 5).

Matching uses `source_path`, `source_refs`, `title`, `summary`, and `tags`. With `--query`, ranking follows the same scoring family as `lane_search` (keyword / phrase / recency).

When hits exist, the script prints suggested **`lane_timeline`** and **`memory_brief`** commands and reminds you that **you may still read the file directly**.

## `memory_brief.py`

Single command that chains **search → timeline → bounded expansion** into one Markdown brief (runtime-only).

```bash
python3 scripts/runtime/memory_brief.py \
  --lane work-strategy \
  --query "iran negotiation framing" \
  --limit 5 \
  --expand 3 \
  --timeline-before 2 \
  --timeline-after 2 \
  --output prepared-context/memory-brief.md
```

Backward-compatible positional form (same flags otherwise; do not mix with `--lane`):

```bash
python3 scripts/runtime/memory_brief.py work-strategy "iran negotiation framing"
```

- **`--lane`** and **`--query`** are required unless you pass **positional** `LANE` and optional query words.
- **`--cross-lane`** — search pool can include all lanes (use sparingly); timeline behavior matches `lane_timeline.py --cross-lane`.
- **`--output` / `-o`** — optional file write; parent directories are created as needed.
- Default caps: `--limit 5`, `--expand 3`, `--timeline-before 2`, `--timeline-after 2`.

Output sections: **Best Matches**, **Timeline Context**, **Expanded Takeaways**, **Recommended Next Move**, plus an explicit **Boundary** that this is not Record truth.

Optional: set `GRACE_MAR_RUNTIME_LEDGER_ROOT` to isolate the ledger in tests or sandboxes.

Generated `prepared-context/memory-brief.md` is **gitignored** by default so operator output is not committed accidentally.
