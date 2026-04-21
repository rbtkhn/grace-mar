# Strategy raw input (full retention, 7 days)

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim — without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**Relation to other surfaces:**

| Surface | Role |
|--------|------|
| **daily-strategy-inbox.md** | Paste-ready **stubs** + grep registry; optional short excerpts only |
| **experts/`<id>`/transcript.md** | 7-day rolling **triage** corpus from inbox `thread:` blocks (word caps per architecture) |
| **`raw-input/` (this tree)** | **Unabridged** text and bundled inputs for **7 calendar days**, then **deleted** from this folder by prune (git history may still hold copies if committed) |

WORK only; not Record.

## Layout

Use **one subdirectory per local ingest day** (the day you save the file — typically “today” when you paste):

```text
raw-input/
  README.md          ← this file
  YYYY-MM-DD/        ← e.g. 2026-04-20/
    <slug>.md        ← one file per capture (or per bundle)
```

**Slug:** `kebab-case`, unique within that day — e.g. `ritter-judging-freedom-2026-04-20.md`, `davis-johnson-hormuz-full.md`.

**Optional:** Add non-markdown payloads next to the `.md` file in the same folder (e.g. `.txt` exports) if you truly need byte-identical dumps; keep filenames descriptive.

## File template (recommended)

Each `.md` file should start with a short metadata block so greps and future tooling can link back to expert lanes and URLs:

```markdown
---
ingest_date: YYYY-MM-DD
aired_date: YYYY-MM-DD
thread: expert_id
source_url: https://...
kind: transcript | paste-bundle | screenshot-list | x-screenshots-index | x-post-text | mixed
---

# Human-readable title

…full body…
```

`thread:` may be omitted for non-expert material (e.g. raw wire paste with no `thread:` lane yet). `aired_date` is the show/publication day when it differs from ingest day. Prefer **`kind: x-post-text`** when you paste X copy directly; legacy screenshot captures are indexed as **`x-screenshots-index`** (links to `assets/**/*.png`, no OCR).

## Harvest / backfill

To **populate** `raw-input/` from material already on disk (standalone `*verbatim*.md` at the strategy-notebook root, per-expert `experts/<id>/transcript.md` date sections, and `assets/**/x-*.png` grouped by date in the filename), run from repo root:

```bash
python3 scripts/populate_strategy_raw_input.py --dry-run
python3 scripts/populate_strategy_raw_input.py --apply
```

**Window:** dates **`d`** where **`d > today − 7`** local days (same as expert transcript triage and `prune_strategy_raw_input.py`). **`--days N`**, **`--today YYYY-MM-DD`** (tests), **`--force`** (overwrite changed files), and **`--notebook-root`** / **`--root`** are supported.

Idempotent: unchanged files are skipped (content hash). See [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py).

## Pruning

Retention matches expert **`transcript.md`**: folders named **`YYYY-MM-DD`** are **removed** when that date is **not** strictly after **`today − 7`** local calendar days (same rule as `scripts/strategy_expert_transcript.py` — the oldest kept folder is **today − 6** through **today** when `days=7`).

From repo root:

```bash
# Preview what would be deleted
python3 scripts/prune_strategy_raw_input.py --dry-run

# Apply deletion
python3 scripts/prune_strategy_raw_input.py --apply
```

Default root: `docs/skill-work/work-strategy/strategy-notebook/raw-input`. Override with `--root <path>` if needed.

**Note:** This does **not** replace git history. If you need recovery after prune, use `git checkout` on the removed paths.

## Assistant default

When the operator asks for **full transcript on disk** or **store everything**, write the body under **`raw-input/YYYY-MM-DD/<slug>.md`** and keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to a **stub line** (with `thread:` + URL + `verify:`) pointing at this file, e.g. `verify:full-text+raw-input/2026-04-20/slug.md`.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Raw input archive (7-day full retention)*.
