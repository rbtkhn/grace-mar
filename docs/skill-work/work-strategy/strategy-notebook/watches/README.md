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

Pages replaced knots as the primary analytical unit. Instead of standalone files under `chapters/YYYY-MM/knots/`, pages live inside expert thread files as marker-fenced blocks within monthly chapters.

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

### `weave` — integrated analysis (Think lane)

Cross-expert analysis of named topics, experts, or watches. Read-only; produces analysis to stdout. Also refreshes the batch-analysis snapshot.

```
python3 scripts/strategy_weave.py davis barnes hormuz
python3 scripts/strategy_weave.py --watch hormuz
python3 scripts/strategy_weave.py escalation blockade --json
```

### `page` — compose a page (Ship lane)

Creates a page block in each named expert's thread file. The Ship-lane complement to `weave`.

```
python3 scripts/strategy_page.py davis barnes --watch hormuz
python3 scripts/strategy_page.py pape --id zero-sum-hormuz
python3 scripts/strategy_page.py davis barnes --dry-run
```

### `watch` — cross-expert watch views

Lists watches or shows detail for one watch, including tension relations from `knot-connections.yaml`.

```
python3 scripts/strategy_watch.py                        # list all watches
python3 scripts/strategy_watch.py --watch hormuz          # one watch detail
python3 scripts/strategy_watch.py --watch hormuz --json   # machine-readable
python3 scripts/strategy_watch.py --tensions-only         # only disagreements
```

## Daily rhythm

1. **thread** — triage inbox, extract to machine layers, see page candidates
2. **weave** — integrated analysis of topics that emerged
3. **page** — record what crystallized as a page in thread files
4. **watch** — track named situations across experts over time

## Migration

Existing knot files under `chapters/YYYY-MM/knots/` remain on disk until the operator removes them. The migration script (`scripts/migrate_knots_to_pages.py`) converts knots into page blocks and moves flat expert files into per-expert folders.

## What this does NOT replace

- The machine layer (`strategy-expert-thread:start/end` markers) is unchanged
- `strategy_thread.py` still writes the machine layer
- `knot-index.yaml` and `knot-connections.yaml` remain as the migration source and tension/connection reference
- No new Python packages, JSON stores, or state directories
