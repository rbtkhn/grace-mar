# Read hints (soft)

## Invocation contract

**Surface type:** helper  
**Primary purpose:** suggest when existing runtime observations may make a fresh file read unnecessary  
**When to use:** before reopening a notebook, file, or familiar topic  
**Inputs:** lane plus path or query  
**Outputs:** compact hint list and suggested next retrieval step  
**Mutation scope:** runtime-only  
**Canonical Record access:** none  
**Typical next step:** `lane_timeline.py` or `memory_brief.py`  
**Do not use for:** blocking operator judgment or replacing a deliberate fresh read  

Grace-Mar’s analogue to “file-read decision” tools elsewhere: **surface relevant runtime observations** before you re-open a large file or notebook. This is a **hinting layer**, not a block — the operator or companion always chooses whether to read again.

**Normative workflow, rules, and policy:** [memory-retrieval.md](memory-retrieval.md). **Abstention / uncertainty envelopes:** [abstention-policy.md](../abstention-policy.md). This page covers **`read_hint.py`** and **`memory_brief.py`** only.

## Principles

- **Suggest, do not deny** — Never block `read()`; print recommendations only.
- **No Record mutation** — These tools do not write `recursion-gate.md`, SELF, SKILLS, or other Record surfaces (see normative doc for the full boundary).

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
- **`--budgeted-follow-on PATH`** — after writing `-o`, runs `build_budgeted_context.py` with the brief as `--include-memory-brief`. Without **`--workflow-depth` / `--depth`**, pass-through mode uses **`--budgeted-mode`** (default `compact`). With **`--workflow-depth`**, **`--task-anchor`** is required (same rule as prepared context); see [workflow-depth.md](workflow-depth.md).

Output sections: **Best Matches**, **Timeline Context**, **Expanded Takeaways**, **Recommended Next Move**, plus an explicit **Boundary** that this is not Record truth.

Optional: set `GRACE_MAR_RUNTIME_LEDGER_ROOT` to isolate the ledger in tests or sandboxes.

Generated `prepared-context/memory-brief.md` is **gitignored** by default so operator output is not committed accidentally.
