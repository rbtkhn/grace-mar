# Backfill sources registry
<!-- word_count: 521 -->

WORK only; not Record.

## Purpose

This file is the routing registry for strategy-notebook backfill scripts. It does not replace the scripts, raw captures, expert profiles, or validation. It exists to reduce wrapper sprawl by making each backfill script answer one question:

> Is this a generic capture family, a source-specific adapter, or a temporary recovery script?

New backfill work should prefer a generic family first, then add the thinnest source-specific adapter only when the source shape actually requires it.

## Source families

| Family | Preferred generic script | Source-specific adapters | Default role |
|--------|--------------------------|--------------------------|--------------|
| Substack archive / post body | `scripts/backfill_substack_raw_input.py` | `backfill_*_substack_raw_input.py` | Capture substantial posts into `raw-input/<pub_date>/`; source adapters should mostly pin host, thread, and defaults. |
| Public X profile / status pages | `scripts/backfill_x_profile_raw_input.py` | `backfill_*_x_raw_input.py` | Best-effort public crawl or explicit status URL capture; source adapters should mostly pin handle and thread. |
| Public author archive pages | `scripts/backfill_author_page_raw_input.py` | `backfill_*_site_raw_input.py`, `backfill_*_grayzone_raw_input.py`, `backfill_*_responsiblestatecraft_raw_input.py` | Discover article URLs and write source captures; source adapters should pin archive URL shape and parser hints. |
| Transcript salvage from local chat/log text | No default generic family yet | `backfill_*_raw_input_from_transcript.py` | Recovery only when a session failed to write `raw-input/` directly. Regex- and shape-dependent; not policy. |
| Expert thread/profile enrichment | `scripts/backfill_expert_thread.py` and related scoring/refinement helpers | n/a | Separate from raw source capture unless a commit explicitly groups both with a receipt. |

## Wrapper policy

- Keep wrappers thin: source defaults, URL patterns, thread ids, and parser hints.
- Do not duplicate generic fetch, Markdown rendering, YAML writing, duplicate detection, or date parsing in every adapter unless the source forces it.
- If two wrappers share more than source constants and parser hints, prefer lifting that behavior into the generic family in a later commit.
- Do not treat archive completeness as mandatory. Backfill substantial items worth preserving; skip low-signal or repetitive items when that is better editorial judgment.
- Keep source capture and expert profile enrichment as separate commit arcs unless the profile change is only a pointer to the captured source.

## Preflight before committing a backfill cluster

Run or inspect these before committing strategy backfill work:

```bash
python3 scripts/validate_strategy_pages.py
git diff --check
```

When a script has focused tests, run those too. At minimum, the commit message or PR body should say which source family was used and whether the script is generic, source-specific, or recovery-only.

## Future reduction path

The low-risk path is registry first, consolidation later:

1. Label each existing wrapper by family.
2. Add focused tests around the generic families.
3. Move duplicated behavior into the generic scripts only after tests cover the shared path.
4. Retire wrappers only when their source defaults can be represented by config or a short documented command.
