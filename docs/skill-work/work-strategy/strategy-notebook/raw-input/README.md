# Strategy raw input (full retention, 7 days)

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim — without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**Expert-agnostic:** This tree is **raw material for analysis**, not only dumps tied to a [strategy-commentator-threads.md](../strategy-commentator-threads.md) **`expert_id`**. Substack essays, wire bundles, institutional statements, screenshot indexes, and mixed paste-bundles belong here even when there is **no** `thread:` lane yet (or ever). The inbox stub may use **`membrane:single`** and omit **`thread:`**; frontmatter **`thread:`** is optional (see § File template).

## Automated fetch (RSS → raw-input)

**Script:** [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) — pulls **RSS/Atom** items (e.g. Substack `/feed`) into **`raw-input/<pub_date>/`** as markdown with YAML frontmatter (`kind: rss-item`). When a feed sets **`"thread": "<expert_id>"`**, new items **append** into **`raw-input/<pub_date>/<pub_date>-<expert_id>.md`** (multiple ingests = multiple `---` … `---` blocks; duplicates skipped by `guid:`). **Refined day pages** (operator judgment artifacts) live under **`experts/<expert_id>/`** — e.g. **`mercouris-page-YYYY-MM-DD.md`** — not in this tree. Feeds **without** `thread` still write **one markdown file per RSS item** (slug + hash basename). Optional **`thread:`** in YAML drives **`python3 scripts/strategy_thread.py`** triage: one-line RSS stubs merge into that expert’s **`experts/<id>/transcript.md`** (after inbox lines for the same date).

**Setup:**

1. Edit **`fetch-sources.json`** in this directory (default includes Simplicius, Big Serge, Greenwald with `thread` set). To add feeds, copy from [fetch-sources.example.json](fetch-sources.example.json) or append another object under `rss_feeds` (`url`, `slug_prefix`, `max_items`, `enabled`, optional `thread`).
2. Preview: `python3 scripts/fetch_strategy_raw_input.py` (dry-run by default).
3. Write: `python3 scripts/fetch_strategy_raw_input.py --apply`.

**Config path override:** set env **`FETCH_STRATEGY_SOURCES`** to an absolute path, or pass **`--config`**.

**Scheduling:** use **cron**, **launchd**, or a personal runner — e.g. daily at 06:00 local:

`0 6 * * * cd /path/to/grace-mar && /usr/bin/python3 scripts/fetch_strategy_raw_input.py --apply >> ~/logs/strategy-fetch.log 2>&1`

Optional local override file (gitignored): **`fetch-sources.local.json`** — merge story is manual (copy entries into `fetch-sources.json` or swap path via env); the repo does not auto-merge two JSON files.

**Backfill / mirror (no network):** unchanged — [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) copies existing transcripts and verbatim sidecars into `raw-input/`; run it after local edits when you want a unified archive layout.

**Substack year backfill (full post body):** [`scripts/backfill_substack_raw_input.py`](../../../../scripts/backfill_substack_raw_input.py) — paginates `api/v1/archive`, fetches `api/v1/posts/{slug}`, writes `raw-input/<date>/substack-*.md` with optional YAML `thread: simplicius` (or other id). Example:  
`python3 scripts/backfill_substack_raw_input.py --hostname simplicius76.substack.com --year 2026 --thread simplicius --apply`

**Future extensions (not implemented yet):** authenticated X/YouTube/API pulls, wire paywall fetchers, and inbox stub append — each needs its own gate (tokens, ToS, tier tags).

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
    YYYY-MM-DD-<expert_id>.md   ← raw capture: RSS `thread:` merge target + populate mirror (append ingests)
    <slug>.md        ← other captures: verbatim sidecars, RSS without thread:, bundles, indexes
```

**Refined day page (not here):** **`experts/<expert_id>/mercouris-page-YYYY-MM-DD.md`** (Mercouris) — Chronicle / Reflection / Foresight; links back to **verbatim** in this tree. Distinct from **`strategy-page`** in `thread.md` unless mirrored during EOD compose.

**Raw capture:** e.g. **`2026-04-21-mercouris-verbatim.md`** for full operator transcript; RSS **`thread: mercouris`** appends to **`2026-04-21-mercouris.md`**.

**Other slugs:** `kebab-case`, unique within that day — e.g. `ritter-judging-freedom-2026-04-20.md`, `substack-simplicius-….md`, `davis-johnson-hormuz-full.md`.

**Optional:** Add non-markdown payloads next to the `.md` file in the same folder (e.g. `.txt` exports) if you truly need byte-identical dumps; keep filenames descriptive.

## File template (recommended)

Each `.md` file should start with a short metadata block so greps and future tooling can link back to expert lanes and URLs:

```markdown
---
ingest_date: YYYY-MM-DD
pub_date: YYYY-MM-DD
thread: expert_id
source_url: https://...
kind: transcript | paste-bundle | screenshot-list | x-screenshots-index | x-post-text | mixed
---

# Human-readable title

…full body…
```

`thread:` may be omitted for non-expert material (e.g. raw wire paste with no `thread:` lane yet). **`pub_date` and `published_date` are the same field** in meaning: the calendar day the source went public (air, YouTube/Substack publish, RSS `pubDate`, etc.), as distinct from **`ingest_date`** (when you saved the file). Use **`pub_date`** in new frontmatter. Older files may still say **`published_date` only**; some older operator ingests have **both** with identical values—redundant, safe to delete one. RSS triage and related scripts read **`published_date` first, then `pub_date`, then `ingest_date`**, then the folder name. Prefer **`kind: x-post-text`** when you paste X copy directly; legacy screenshot captures are indexed as **`x-screenshots-index`** (links to `assets/**/*.png`, no OCR).

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

When the operator asks for **full transcript on disk**, write **verbatim** under **`raw-input/YYYY-MM-DD/<descriptive-slug>.md`** (or **`YYYY-MM-DD-<expert_id>.md`** when matching RSS merge). Place **refined day pages** under **`experts/<expert_id>/mercouris-page-YYYY-MM-DD.md`** (or an equivalent convention per expert). Keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to **stub lines** pointing at **verbatim** for `verify:` and optionally at the **expert page** for composed judgment, e.g. `verify:full-text+raw-input/2026-04-21/2026-04-21-mercouris-verbatim.md`.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Raw input archive (7-day full retention)*.
