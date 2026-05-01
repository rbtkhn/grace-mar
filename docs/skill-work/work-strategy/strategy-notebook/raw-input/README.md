# Strategy raw input (full retention, 7 days)
<!-- word_count: 1720 -->

**Purpose:** Store **complete** transcripts and **all** strategy-ingest source material you want kept verbatim â€” without bloating [daily-strategy-inbox.md](../daily-strategy-inbox.md) or hitting the **~2000 word** per-block budget on [experts/*/transcript.md](../experts/ritter/transcript.md) that **`thread`** triage targets.

**SSOT role:** This tree is the **SSOT for literal text** of each capture. **[`refined-page-template.md`](../refined-page-template.md)** defines the **next layer:** standalone **`experts/â€¦/ *-page-*.md`** files carry **`### Verbatim`** (and analysis) and are the **SSOT for thread / `days.md` / strategy work** â€” cite those pages for judgment; use **`raw-input/`** when you must verify or edit the **exact words**.

**Expert-agnostic:** This tree is **raw material for analysis**, not only dumps tied to a [strategy-commentator-threads.md](../strategy-commentator-threads.md) **`expert_id`**. Substack essays, wire bundles, institutional statements, screenshot indexes, and mixed paste-bundles belong here even when there is **no** `thread:` lane yet (or ever). The inbox stub may use **`membrane:single`** and omit **`thread:`**; frontmatter **`thread:`** is optional (see Â§ File template).

**Unlisted speakers / no lane yet:** If a capture is worth keeping but the speaker or outlet does **not** map to an existing expert folder, still ingest it here as source-first raw input. Leave **`thread:`** out unless you later decide to route it into an existing lane.

**Capture-type calibration (essay / transcript / social / wireâ€“PDF):** For **type-specific** defaults â€” **`kind:`**, **`thread:`**, inbox stub shape, refined-page **`### Verbatim`** expectations â€” see **[`CAPTURE-TYPES.md`](CAPTURE-TYPES.md)** (grep-friendly **`##`** headings). Operator + assistant ingest should align that doc with this READMEâ€™s YAML and [refined-page-template.md](../refined-page-template.md).

## Publication vocabulary (formal pin)

- **Machine (grep / YAML / cold lines, `verify:` tails):** use **`pub_date`** and the tag **`pub_date:YYYY-MM-DD`**. **Do not** introduce new **`aired:`** tags; **`ingest_date`** remains â€œwhen the file entered this tree,â€ distinct from **publication**.
- **Human (preambles, spec prose):** use **Published** / â€œpublication dayâ€ â€” not an â€œairedâ€ block as the norm. Same calendar anchor as **`pub_date`**; see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) publication vocabulary and [refined-page-template.md](../refined-page-template.md).
- **Legacy (until bulk migration):** folder **`_aired-pending/`** and existing **`aired:`** / â€œairedâ€ in older **daily-strategy-inbox.md** and captures stay on disk; new material and new edits follow this pin.

## Three capture channels (normative vs recovery)

Do **not** conflate **Cursor agent transcript JSONL** (machine-local logs of chat turns, including `<user_query>`) with **`experts/<expert_id>/transcript.md`** (rolling **in-repo** triage corpus). They are different surfaces with different roles.

| Channel | What it is | Role |
|---------|------------|------|
| **1 â€” Direct / assistant write** | Markdown under **`raw-input/<pub_date>/`** with YAML (`kind: paste-bundle`, `rss-item`, etc.), written in-session or by automation | **Normative** for manual strategy inputs â€” matches [`.cursor/rules/strategy-input-raw-ingest.mdc`](../../../../../.cursor/rules/strategy-input-raw-ingest.mdc). |
| **2 â€” Populate** | [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) copies **`experts/.../transcript.md`** date sections, standalone `*verbatim*.md`, X indexes â€” **repo artifacts only** | **Mirror / backfill** from material already committed; **does not** read Cursor JSONL. |
| **3 â€” Agent JSONL scripts** | Ad hoc parsers (e.g. [`scripts/backfill_crooke_raw_input_from_transcript.py`](../../../../scripts/backfill_crooke_raw_input_from_transcript.py)) | **Salvage** when chat never wrote **`raw-input/`** â€” regex- and shape-dependent; **not** policy. |

**RSS / Substack API** ([`fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py), [`backfill_substack_raw_input.py`](../../../../scripts/backfill_substack_raw_input.py)) write **`raw-input/`** directly â€” **preferred** when a feed or API path exists (zero chat overhead).

### Pruning vs recovery

**Pruning** ([Â§ Pruning](#pruning)) is **optional disk reclaim** (`prune_strategy_raw_input.py`), operator-triggered. It is **not** the next step after â€œrecover missed verbatim,â€ and it is **not** CI-scheduled. Recovery **after** mistaken deletion uses **`git checkout`** on removed paths ([Â§ Pruning](#pruning) note).

Do **not** bundle â€œdefault rolling window â‰ˆ 7 daysâ€ with **recovery**: the same **`N`** aligns expert **`transcript.md`** tooling and **`prune_strategy_raw_input.py`**, but **prune** is **hygiene**, not ingest salvage.

## Automated fetch (RSS â†’ raw-input)

**Script:** [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) â€” pulls **RSS/Atom** items (e.g. Substack `/feed`) into **`raw-input/<pub_date>/`** as markdown with YAML frontmatter (`kind: rss-item`). When a feed sets **`"thread": "<expert_id>"`**, new items **append** into **`raw-input/<pub_date>/<pub_date>-<expert_id>.md`** (multiple ingests = multiple `---` â€¦ `---` blocks; duplicates skipped by `guid:`). **Refined pages** (operator judgment artifacts) live under **`experts/<expert_id>/`** â€” e.g. **`mercouris-page-YYYY-MM-DD.md`** â€” not in this tree. Feeds **without** `thread` still write **one markdown file per RSS item** (slug + hash basename). Optional **`thread:`** in YAML drives **`python3 scripts/strategy_thread.py`** triage: one-line RSS stubs merge into that expertâ€™s **`experts/<id>/transcript.md`** (after inbox lines for the same date).

**Setup:**

1. Edit **`fetch-sources.json`** in this directory (default includes Simplicius, Big Serge, Greenwald with `thread` set). To add feeds, copy from [fetch-sources.example.json](fetch-sources.example.json) or append another object under `rss_feeds` (`url`, `slug_prefix`, `max_items`, `enabled`, optional `thread`).
2. Preview: `python3 scripts/fetch_strategy_raw_input.py` (dry-run by default).
3. Write: `python3 scripts/fetch_strategy_raw_input.py --apply`.

**Config path override:** set env **`FETCH_STRATEGY_SOURCES`** to an absolute path, or pass **`--config`**.

**Scheduling:** use **cron**, **launchd**, or a personal runner â€” e.g. daily at 06:00 local:

`0 6 * * * cd /path/to/grace-mar && /usr/bin/python3 scripts/fetch_strategy_raw_input.py --apply >> ~/logs/strategy-fetch.log 2>&1`

Optional local override file (gitignored): **`fetch-sources.local.json`** â€” merge story is manual (copy entries into `fetch-sources.json` or swap path via env); the repo does not auto-merge two JSON files.

**Backfill / mirror (no network):** [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) copies **on-disk** **`experts/<id>/transcript.md`** sections and verbatim sidecars into **`raw-input/`** â€” **not** Cursor agent JSONL (see [Â§ Three capture channels](#three-capture-channels-normative-vs-recovery)). Run after local edits when you want a unified archive layout.

**Backfill source registry:** before adding another `backfill_*` wrapper, check [BACKFILL-SOURCES.md](BACKFILL-SOURCES.md). It classifies generic source families, source-specific adapters, and recovery-only scripts so the notebook can reduce wrapper sprawl without deleting useful tools prematurely.

**Substack year backfill (full post body):** [`scripts/backfill_substack_raw_input.py`](../../../../scripts/backfill_substack_raw_input.py) â€” paginates `api/v1/archive`, fetches `api/v1/posts/{slug}`, writes `raw-input/<date>/substack-*.md` with optional YAML `thread: simplicius` (or other id). Treat the archive as a discovery index, not a completeness mandate: backfill the substantial posts you want preserved, and leave light or repetitive archive-visible items out when that is the better editorial call. Example:
`python3 scripts/backfill_substack_raw_input.py --hostname simplicius76.substack.com --year 2026 --thread simplicius --apply`

**X profile backfill (best-effort public crawl):** [`scripts/backfill_x_profile_raw_input.py`](../../../../scripts/backfill_x_profile_raw_input.py) â€” crawls a public X profile for visible `status/` links, fetches each status page, and writes `kind: x-post-text` captures into `raw-input/<date>/`. Use this for Ritter or any other public profile when you want profile discovery plus one-file-per-post capture; pass explicit `--status-url` values when you already know the exact post URLs.

**Responsible Statecraft author crawl (public articles):** [`scripts/backfill_responsiblestatecraft_author_raw_input.py`](../../../../scripts/backfill_responsiblestatecraft_author_raw_input.py) â€” crawls a public author page, fetches each linked article page, and writes `kind: rss-item` captures into `raw-input/<date>/`. Use this for Parsi when the public author archive is the discovery surface; pass explicit `--article-url` values when you already know the exact article URLs.


**Crooke partial backfill (public archive discovery):** [`scripts/backfill_crooke_substack_raw_input.py`](../../../../scripts/backfill_crooke_substack_raw_input.py) Ã¢â‚¬â€ uses the public Conflicts Forum archive to discover 2026 posts, compares them against existing `thread: crooke` raw-input files, and writes `substack-post` stubs when a post needs a public-preview placeholder. Use this when the public archive proves the post exists but the paid body still needs manual completion.

**Compose boundary:** Automated capture writes **`raw-input/`** only; new `experts/<expert_id>/*page*.md` files are created later in a separate compose pass.
**Future extensions (not implemented yet):** authenticated/private X and wire paywall fetchers â€” public X profile crawl and public YouTube transcript fetches are implemented, but authenticated sessions still need their own gate (tokens, ToS, tier tags).

**Relation to other surfaces:**

| Surface | Role |
|--------|------|
| **daily-strategy-inbox.md** | Paste-ready **stubs** + grep registry; optional short excerpts only â€” **index before (or in the same step as)** full verbatim on disk |
| **experts/`<id>`/transcript.md** | 7-day rolling **triage** corpus from inbox `thread:` blocks (word caps per architecture); **pointers** when the same material is already under **`raw-input/`** |
| **`raw-input/` (this tree)** | **Unabridged** text and bundled inputs; **pruning is operator-initiated only** (see Â§ Pruning). Nothing in CI auto-deletes this tree. |

**`kind:` values (YAML) and automation** â€” files with **`thread: <expert_id>`** and a parseable publication day (folder + front matter) participate in **`thread`** triage and the **machine layer** â€œRecent raw-inputâ€ list, except **index-only** kinds that would duplicate assets without adding speech text:

| `kind` | Merged into transcript (one-line stub) | Notes |
|--------|----------------------------------------|--------|
| `rss-item`, `transcript`, `paste-bundle`, `x-post-text`, `mixed`, `verbatim-sidecar`, â€¦ | **Yes** (if `thread:` set) | Default: any `kind` **except** the exclude list below. |
| `screenshot-list`, `x-screenshots-index` | **No** | Image / index rolls only; not expert speech stubs. |

**Transcript file optional (advanced):** The per-expert rolling **`experts/<id>/transcript.md`** can stay **empty or pointer-only** when **`thread`** is run regularly â€” the **machine layer** still gets **Recent raw-input (lane)** from on-disk + inbox. Fully **removing** `transcript.md` from the tree is a separate hygiene choice (only after the operator bakes in raw-input + inbox registry habits).

**End-of-day strategy session (notebook compose):** Default **sole** window for writing **`strategy-page`** blocks + `days.md` judgment is the **once-per-day** session you open with **`strategy page`** or **`strategy page compose`** (operator phrases â€” see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../STRATEGY-NOTEBOOK-ARCHITECTURE.md) Â§ *End-of-day strategy session*). **Primary bulk evidence:** **this folderâ€™s** dated files plus inbox stubs. The operator token **`weave`** is **deprecated** for that compose step.

WORK only; not Record.

## Layout

Use **one subdirectory per publication day** â€” the folder name **`YYYY-MM-DD`** matches **`pub_date`** in the fileâ€™s frontmatter (when the source went public: livestream go-live, YouTube publish, Substack `pubDate`, RSS item date, etc.). This matches [`scripts/fetch_strategy_raw_input.py`](../../../../scripts/fetch_strategy_raw_input.py) (writes under **`raw-input/<pub_date>/`**) and [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py) (uses section / filename **publication** dates).

**Not** the folder for â€œthe day I saved the fileâ€ â€” that belongs in **`ingest_date`** in YAML only. If **`pub_date`** is still unknown (e.g. transcript paste before the canonical `watch?v=` is pinned), use **`_aired-pending/`** for the markdown file; move it into **`raw-input/<pub_date>/`** once the air day is fixed.

```text
raw-input/
  README.md          â† this file
  _aired-pending/    â† optional: captures whose pub_date is not fixed yet (move when pinned)
  YYYY-MM-DD/        â† = pub_date / air day (e.g. 2026-04-20/)
    YYYY-MM-DD-<expert_id>.md   â† raw capture: RSS `thread:` merge target + populate mirror (append ingests)
    <slug>.md        â† other captures: verbatim sidecars, RSS without thread:, bundles, indexes
```

**Refined page (not here):** **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** â€” Verbatim / Reflection / Predictive Outlook; links back to **verbatim** in this tree. **Multiple refined pages for the same publication date are allowed:** **`â€¦-page-YYYY-MM-DD-<slug>.md`** (slug from `raw-input` stem) **or** one consolidated file with **A / B / C** Verbatim blocks per [refined-page-template.md](../refined-page-template.md) (each expertâ€™s **`*-page-template.md`** is a **compat stub** linking that canonical). Distinct from **`strategy-page`** in `thread.md` unless mirrored during EOD compose.

**Raw capture:** e.g. **`2026-04-21-mercouris-verbatim.md`** under **`2026-04-21/`** because the episode **published** ( **`pub_date`** ) on that calendar day; RSS **`thread: mercouris`** appends to **`2026-04-21-mercouris.md`** in that same folder.

**Other slugs:** `kebab-case`, unique within that day â€” e.g. `ritter-judging-freedom-2026-04-20.md`, `substack-simplicius-â€¦.md`, `davis-johnson-hormuz-full.md`.

**Optional:** Add non-markdown payloads next to the `.md` file in the same folder (e.g. `.txt` exports) if you truly need byte-identical dumps; keep filenames descriptive.

## File template (recommended)

Each `.md` file should start with a short metadata block so greps and future tooling can link back to expert lanes and URLs:

```markdown
---
ingest_date: YYYY-MM-DD
pub_date: YYYY-MM-DD
thread: expert_id
source_url: https://...
kind: transcript | paste-bundle | screenshot-list | x-screenshots-index | x-post-text | mixed | substack-post
---

# Human-readable title

â€¦full bodyâ€¦
```

`thread:` may be omitted for non-expert material (e.g. raw wire paste with no `thread:` lane yet). **`pub_date`** is the calendar day the source went public (live, YouTube/Substack publish, RSS `pubDate`, etc.), distinct from **`ingest_date`** (when you saved or ingested the file into this tree). **On disk,** the parent folder `raw-input/YYYY-MM-DD/` **should match `pub_date`** once known (or **`_aired-pending/`** until then). The legacy key **`published_date`** is **removed** from this treeâ€”use **`pub_date`** only. RSS triage reads **`pub_date`**, then **`ingest_date`**, then the folder name. Prefer **`kind: x-post-text`** when you paste X copy directly; legacy screenshot captures are indexed as **`x-screenshots-index`** (links to `assets/**/*.png`, no OCR).

## Harvest / backfill

To **populate** `raw-input/` from material already on disk (standalone `*verbatim*.md` at the strategy-notebook root, per-expert `experts/<id>/transcript.md` date sections, and `assets/**/x-*.png` grouped by date in the filename), run from repo root:

```bash
python3 scripts/populate_strategy_raw_input.py --dry-run
python3 scripts/populate_strategy_raw_input.py --apply
```

**Window:** dates **`d`** where **`d > today âˆ’ 7`** local days (same as expert transcript triage and `prune_strategy_raw_input.py`). **`--days N`**, **`--today YYYY-MM-DD`** (tests), **`--force`** (overwrite changed files), and **`--notebook-root`** / **`--root`** are supported.

Idempotent: unchanged files are skipped (content hash). See [`scripts/populate_strategy_raw_input.py`](../../../../scripts/populate_strategy_raw_input.py).

**Advisory gap hint:** [`scripts/strategy_raw_input_gap_hint.py`](../../../../scripts/strategy_raw_input_gap_hint.py) â€” compares **`daily-strategy-inbox.md`** URLs to **`source_url`** in **`raw-input/`** YAML (default: article-ish URLs such as Substack `/p/`, Conflicts Forum, YouTube `watch`; **`--all-urls`** for full inbox scrape â€” noisy). **Not** CI or policy; operator judgment only.

## Outlet inventories (tracker docs)

- **Dialogue Works** (Nima Alkhorshid): [dialogue-works-inventory.md](dialogue-works-inventory.md) â€” which **`raw-input/`** files are confirmed vs lane-stub references; maintenance grep at bottom.

## Pruning

**Policy:** There is **no** scheduled or CI-driven prune in this repo â€” **you** run the script when you want to reclaim disk space. A marker file **[`.pruning-suspended`](.pruning-suspended)** is committed: **`python3 scripts/prune_strategy_raw_input.py --apply`** **refuses** to delete until you either pass **`--override`** with **`--apply`** or **remove** the marker file. **`--dry-run`** (or default preview mode) **always** works so you can see what would be removed.

Retention (when you do prune) matches expert **`transcript.md`**: folders named **`YYYY-MM-DD`** are **removed** when that date is **`<= today âˆ’ N`** (default **`N = 7`** via **`--days`**) â€” same calendar window as `scripts/strategy_expert_transcript.py`.

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

When the operator asks for **full transcript on disk**, write **verbatim** under **`raw-input/YYYY-MM-DD/<descriptive-slug>.md`** (or **`YYYY-MM-DD-<expert_id>.md`** when matching RSS merge). Place **refined pages** under **`experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`** (and **`â€¦-page-YYYY-MM-DD-<slug>.md`** when splitting multiple primaries on the same date â€” see [NOTEBOOK-CONTRACT.md](../NOTEBOOK-CONTRACT.md) Â§ Refined pages). Keep [daily-strategy-inbox.md](../daily-strategy-inbox.md) to **stub lines** pointing at **verbatim** for `verify:` and optionally at the **expert page** for composed judgment, e.g. `verify:full-text+raw-input/2026-04-21/2026-04-21-mercouris-verbatim.md`.

**Provenance:** YAML frontmatter does not record **operator vs assistant** author by default; **git commits** carry **who / when** for audit. Optional YAML (`note:`) may name capture context.

**Paste-bundle starter:** [snippets/new-paste-bundle.md](snippets/new-paste-bundle.md) â€” copy headers + replace placeholders before pasting body.

Full contract: [STRATEGY-NOTEBOOK-ARCHITECTURE.md Â§ Split ingest model](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#split-ingest-model).
