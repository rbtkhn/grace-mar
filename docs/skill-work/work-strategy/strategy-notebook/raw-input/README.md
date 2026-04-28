# Strategy raw input (full retention, 7 days)
<!-- word_count: 1395 -->

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim — without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**SSOT role:** This tree is the **SSOT for literal text** of each capture. **[`refined-page-template.md`](../refined-page-template.md)** defines the **next layer:** standalone **`experts/…/ *-page-*.md`** files carry **`### Verbatim`** (and analysis) and are the **SSOT for thread / `days.md` / strategy work** — cite those pages for judgment; use **`raw-input/`** when you must verify or edit the **exact words**.

**Expert-agnostic:** This tree is **raw material for analysis**, not only dumps tied to a [strategy-commentator-threads.md](../strategy-commentator-threads.md) **`expert_id`**. Substack essays, wire bundles, institutional statements, screenshot indexes, and mixed paste-bundles belong here even when there is **no** `thread:` lane yet (or ever). The inbox stub may use **`membrane:single`** and omit **`thread:`**; frontmatter **`thread:`** is optional (see § File template).

## Publication vocabulary (formal pin)

- **Machine (grep / YAML / cold lines, `verify:` tails):** use **`pub_date`** and the tag **`pub_date:YYYY-MM-DD`**. **Do not** introduce new **`aired:`** tags; **`ingest_date`** remains “when the file entered this tree,” distinct from **publication**.
- **Human (preambles, spec prose):** use **Published** / “publication day” — not an “aired” block as the norm. Same calendar anchor as **`pub_date`**; see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) publication vocabulary and [refined-page-template.md](../refined-page-template.md).
- **Legacy (until bulk migration):** folder **`_aired-pending/`** and existing **`aired:`** / “aired” in older **daily-strategy-inbox.md** and captures stay on disk; new material and new edits follow this pin.

## Automated fetch (RSS → raw-input)

**Script:** [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) — pulls **RSS/Atom** items (e.g. Substack `/feed`) into **`raw-input/<pub_date>/`** as markdown with YAML frontmatter (`kind: rss-item`). When a feed sets **`"thread": "<expert_id>"`**, new items **append** into **`raw-input/<pub_date>/<pub_date>-<expert_id>.md`** (multiple ingests = multiple `---` … `---` blocks; duplicates skipped by `guid:`). **Refined pages** (operator judgment artifacts) live under **`experts/<expert_id>/`** — e.g. **`mercouris-page-YYYY-MM-DD.md`** — not in this tree. Feeds **without** `thread` still write **one markdown file per RSS item** (slug + hash basename). Optional **`thread:`** in YAML drives **`python3 scripts/strategy_thread.py`** triage: one-line RSS stubs merge into that expert’s **`experts/<id>/transcript.md`** (after inbox lines for the same date).

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

**Future extensions (not implemented yet):** authenticated X/YouTube/API pulls and wire paywall fetchers — each needs its own gate (tokens, ToS, tier tags).

**Relation to other surfaces:**

| Surface | Role |
|--------|------|
| **daily-strategy-inbox.md** | Paste-ready **stubs** + grep registry; optional short excerpts only — **index before (or in the same step as)** full verbatim on disk |
| **experts/`<id>`/transcript.md** | 7-day rolling **triage** corpus from inbox `thread:` blocks (word caps per architecture); **pointers** when the same material is already under **`raw-input/`** |
| **`raw-input/` (this tree)** | **Unabridged** text and bundled inputs; **pruning is operator-initiated only** (see § Pruning). Nothing in CI auto-deletes this tree. |

**`kind:` values (YAML) and automation** — files with **`thread: <expert_id>`** and a parseable publication day (folder + front matter) participate in **`thread`** triage and the **machine layer** “Recent raw-input” list, except **index-only** kinds that would duplicate assets without adding speech text:

| `kind` | Merged into transcript (one-line stub) | Notes |
|--------|----------------------------------------|--------|
| `rss-item`, `transcript`, `paste-bundle`, `x-post-text`, `mixed`, `verbatim-sidecar`, … | **Yes** (if `thread:` set) | Default: any `kind` **except** the exclude list below. |
| `screenshot-list`, `x-screenshots-index` | **No** | Image / index rolls only; not expert speech stubs. |

**Transcript file optional (advanced):** The per-expert rolling **`experts/<id>/transcript.md`** can stay **empty or pointer-only** when **`thread`** is run regularly — the **machine layer** still gets **Recent raw-input (lane)** from on-disk + inbox. Fully **removing** `transcript.md` from the tree is a separate hygiene choice (only after the operator bakes in raw-input + inbox registry habits).

**End-of-day strategy session (notebook compose):** Default **sole** window for writing **`strategy-page`** blocks + `days.md` judgment is the **once-per-day** session you open with **`strategy page`** or **`strategy page compose`** (operator phrases — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *End-of-day strategy session*). **Primary bulk evidence:** **this folder’s** dated files plus inbox stubs. The operator token **`weave`** is **deprecated** for that compose step.

WORK only; not Record.

## Layout

Use **one subdirectory per publication day** — the folder name **`YYYY-MM-DD`** matches **`pub_date`** in the file’s frontmatter (when the source went public: livestream go-live, YouTube publish, Substack `pubDate`, RSS item date, etc.). This matches [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) (writes under **`raw-input/<pub_date>/`**) and [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) (uses section / filename **publication** dates).

**Not** the folder for “the day I saved the file” — that belongs in **`ingest_date`** in YAML only. If **`pub_date`** is still unknown (e.g. transcript paste before the canonical `watch?v=` is pinned), use **`_aired-pending/`** for the markdown file; move it into **`raw-input/<pub_date>/`** once the air day is fixed.

```text
raw-input/
  README.md          ← this file
  _aired-pending/    ← optional: captures whose pub_date is not fixed yet (move when pinned)
  YYYY-MM-DD/        ← = pub_date / air day (e.g. 2026-04-20/)
    YYYY-MM-DD-<expert_id>.md   ← raw capture: RSS `thread:` merge target + populate mirror (append ingests)
    <slug>.md        ← other captures: verbatim sidecars, RSS without thread:, bundles, indexes
```

**Refined page (not here):** **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** — Chronicle / Reflection / Foresight; links back to **verbatim** in this tree. **Multiple refined pages for the same publication date are allowed:** **`…-page-YYYY-MM-DD-<slug>.md`** (slug from `raw-input` stem) **or** one consolidated file with **A / B / C** Chronicle blocks per [refined-page-template.md](../refined-page-template.md) (each expert’s **`*-page-template.md`** is a **compat stub** linking that canonical). Distinct from **`strategy-page`** in `thread.md` unless mirrored during EOD compose.

**Raw capture:** e.g. **`2026-04-21-mercouris-verbatim.md`** under **`2026-04-21/`** because the episode **published** ( **`pub_date`** ) on that calendar day; RSS **`thread: mercouris`** appends to **`2026-04-21-mercouris.md`** in that same folder.

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

`thread:` may be omitted for non-expert material (e.g. raw wire paste with no `thread:` lane yet). **`pub_date`** is the calendar day the source went public (live, YouTube/Substack publish, RSS `pubDate`, etc.), distinct from **`ingest_date`** (when you saved or ingested the file into this tree). **On disk,** the parent folder `raw-input/YYYY-MM-DD/` **should match `pub_date`** once known (or **`_aired-pending/`** until then). The legacy key **`published_date`** is **removed** from this tree—use **`pub_date`** only. RSS triage reads **`pub_date`**, then **`ingest_date`**, then the folder name. Prefer **`kind: x-post-text`** when you paste X copy directly; legacy screenshot captures are indexed as **`x-screenshots-index`** (links to `assets/**/*.png`, no OCR).

## Harvest / backfill

To **populate** `raw-input/` from material already on disk (standalone `*verbatim*.md` at the strategy-notebook root, per-expert `experts/<id>/transcript.md` date sections, and `assets/**/x-*.png` grouped by date in the filename), run from repo root:

```bash
python3 scripts/populate_strategy_raw_input.py --dry-run
python3 scripts/populate_strategy_raw_input.py --apply
```

**Window:** dates **`d`** where **`d > today − 7`** local days (same as expert transcript triage and `prune_strategy_raw_input.py`). **`--days N`**, **`--today YYYY-MM-DD`** (tests), **`--force`** (overwrite changed files), and **`--notebook-root`** / **`--root`** are supported.

Idempotent: unchanged files are skipped (content hash). See [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py).

## Outlet inventories (tracker docs)

- **Dialogue Works** (Nima Alkhorshid): [dialogue-works-inventory.md](dialogue-works-inventory.md) — which **`raw-input/`** files are confirmed vs lane-stub references; maintenance grep at bottom.

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

When the operator asks for **full transcript on disk**, write **verbatim** under **`raw-input/YYYY-MM-DD/<descriptive-slug>.md`** (or **`YYYY-MM-DD-<expert_id>.md`** when matching RSS merge). Place **refined pages** under **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** (and **`…-page-YYYY-MM-DD-<slug>.md`** when splitting multiple primaries on the same date — see [PAGE-CONTRACT.md](../PAGE-CONTRACT.md) § Refined pages). Keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to **stub lines** pointing at **verbatim** for `verify:` and optionally at the **expert page** for composed judgment, e.g. `verify:full-text+raw-input/2026-04-21/2026-04-21-mercouris-verbatim.md`.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Split ingest model](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#split-ingest-model).
