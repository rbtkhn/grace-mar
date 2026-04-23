# Watches — strategy-notebook

WORK only; not Record.

## What changed

Expert files moved from flat naming (`strategy-expert-<id>-thread.md`) into per-expert folders:

```
strategy-notebook/experts/<id>/profile.md
strategy-notebook/experts/<id>/transcript.md
strategy-notebook/experts/<id>/thread.md
strategy-notebook/experts/<id>/mind.md       (if exists)
```

**Pages** are the primary analytical unit. Standalone files under the old `chapters/YYYY-MM/knots/` tree (git history) are superseded; current work uses marker-fenced **`strategy-page`** blocks in expert **thread** files.

## Page format

Pages are marker-fenced blocks in the journal layer of a thread file (above the machine-layer markers):

```markdown
## 2026-04

<!-- strategy-page:start id="escalation-blockade" date="2026-04-16" watch="hormuz" -->
### Page: escalation-blockade

**Date:** 2026-04-16
**Watch:** hormuz
**Also in:** ritter, mercouris

(page content)
<!-- strategy-page:end -->
```

Properties:
- `id` — page slug
- `date` — calendar date
- `watch` — named evolving situation this page tracks (optional)
- Multi-expert pages are **duplicated** into each involved expert's thread file
- Multiple pages per chapter are normal
- The machine layer (between `strategy-expert-thread:start/end`) is unchanged

## Watches

A **watch** is a named evolving situation tracked across multiple experts. Watches are derived from `watch=` attributes on pages. The watch tool reads pages across all expert threads to surface cross-expert positions and tensions.

## Commands

### `thread` — triage + extract

Triages inbox to transcripts, extracts material to thread file machine layers. Suggests page candidates when cross-expert material is detected.

```
python3 scripts/strategy_thread.py
```

### `strategy_weave.py` — integrated analysis (Think lane)

**Not** the deprecated operator **`weave`** token for notebook composition — this is the **read-only** script for cross-expert analysis of named topics, experts, or watches (stdout). Also refreshes the batch-analysis snapshot. Notebook **`strategy-page`** + `days.md` writes happen in the **EOD strategy session** ([architecture § End-of-day strategy session](../STRATEGY-NOTEBOOK-ARCHITECTURE.md)).

```
python3 scripts/strategy_weave.py davis barnes hormuz
python3 scripts/strategy_weave.py --watch hormuz
python3 scripts/strategy_weave.py escalation blockade --json
```

### `page` — compose a page (Ship lane)

Creates a page block in each named expert's thread file. Ship-lane complement to **`strategy_weave.py`** analysis (above).

```
python3 scripts/strategy_page.py davis barnes --watch hormuz
python3 scripts/strategy_page.py pape --id zero-sum-hormuz
python3 scripts/strategy_page.py davis barnes --dry-run
```

### `watch` — cross-expert watch views

Lists watches or shows detail for one watch, including optional tension relations from the connections YAML (on-disk name `knot-connections.yaml`; often empty — page-level graph TBD).

```
python3 scripts/strategy_watch.py                        # list all watches
python3 scripts/strategy_watch.py --watch hormuz          # one watch detail
python3 scripts/strategy_watch.py --watch hormuz --json   # machine-readable
python3 scripts/strategy_watch.py --tensions-only         # only disagreements
```

<a id="recovery-quick-path"></a>

## Recovery quick path (“what is live?”)

Use this when you need **situational recovery** (crisis, fast re-entry) without re-reading the full [architecture doc](../STRATEGY-NOTEBOOK-ARCHITECTURE.md).

1. **Named situation → pages across experts** — run `python3 scripts/strategy_watch.py` to list `watch=` ids, then `... --watch <id>` to see pages; optional `--tensions-only` for disagreement-focused recovery.
2. **Chronology and open threads** — tail the current [`chapters/YYYY-MM/days.md`](../chapters/2026-04/days.md) (especially **`### Open`** and latest **`## YYYY-MM-DD`**).
3. **Bundled long read (optional, derived)** — [compiled-views — Browse intent → mechanism](../compiled-views/README.md#browse-intent--mechanism) for `compile_strategy_view.py` when a single file helps; **SSOT** remains expert threads + `days.md`.

A **human-curated** per-watch index (if you ever need one) would be **not SSOT** and is **not** required by default — this section + `strategy_watch.py` are enough for recovery.

## Daily rhythm

1. **thread** — triage inbox, extract to machine layers, see page candidates
2. **weave** — integrated analysis of topics that emerged
3. **page** — record what crystallized as a page in thread files
4. **watch** — track named situations across experts over time

## Migration

Legacy standalone markdown under `chapters/YYYY-MM/knots/` was folded into expert **`strategy-page`** blocks via `scripts/migrate_knots_to_pages.py`; git may retain old paths. Flat expert files may still exist in some trees—per-expert folders under `experts/<id>/` are canonical for new work.

## What this does NOT replace

- The machine layer (`strategy-expert-thread:start/end` markers) is unchanged
- `strategy_thread.py` still writes the machine layer
- On-disk `knot-index.yaml` / `knot-connections.yaml` (legacy filenames) are not live inventory; page inventory comes from expert threads + validators
- No new Python packages, JSON stores, or state directories
