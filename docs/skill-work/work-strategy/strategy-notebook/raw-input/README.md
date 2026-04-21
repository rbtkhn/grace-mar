# Strategy raw input (full retention, 7 days)

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim — without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**Relation to other surfaces:**

| Surface | Role |
|--------|------|
| **daily-strategy-inbox.md** | Paste-ready **stubs** + grep registry; optional short excerpts only |
| **experts/`<id>`/transcript.md** | 7-day rolling **triage** corpus from inbox `thread:` blocks (word caps per architecture) |
| **`raw-input/` (this tree)** | **Unabridged** text and bundled inputs; **pruning is operator-initiated only** (see § Pruning). Nothing in CI auto-deletes this tree. |

**End-of-day strategy session (notebook compose):** Default **sole** window for writing **`strategy-page`** blocks + `days.md` judgment is the **once-per-day** session you open with **`strategy page`** or **`strategy page compose`** (operator phrases — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *End-of-day strategy session*). **Primary bulk evidence:** **this folder’s** dated files plus inbox stubs. The operator token **`weave`** is **deprecated** for that compose step.

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

**Policy:** There is **no** scheduled or CI-driven prune in this repo — **you** run the script when you want to reclaim disk space. A marker file **[`.pruning-suspended`](.pruning-suspended)** is committed: **`python3 scripts/prune_strategy_raw_input.py --apply`** **refuses** to delete until you either pass **`--override`** with **`--apply`** or **remove** the marker file. **`--dry-run`** (or default preview mode) **always** works so you can see what would be removed.

Retention (when you do prune) matches expert **`transcript.md`**: folders named **`YYYY-MM-DD`** are **removed** when that date is **`<= today − N`** (default **`N = 7`** via **`--days`**) — same calendar window as `scripts/strategy_expert_transcript.py`.

From repo root:

```bash
# Preview what would be deleted
python3 scripts/prune_strategy_raw_input.py --dry-run

# Apply deletion (only when not suspended, or with override)
python3 scripts/prune_strategy_raw_input.py --apply --override
```

Default root: `docs/skill-work/work-strategy/strategy-notebook/raw-input`. Override with `--root <path>` if needed.

**Note:** This does **not** replace git history. If you need recovery after prune, use `git checkout` on the removed paths.

## Assistant default

When the operator asks for **full transcript on disk** or **store everything**, write the body under **`raw-input/YYYY-MM-DD/<slug>.md`** and keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to a **stub line** (with `thread:` + URL + `verify:`) pointing at this file, e.g. `verify:full-text+raw-input/2026-04-20/slug.md`.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Raw input archive (7-day full retention)*.
