# Cici operator screenshots ingest - janitor safety + cici-ai launch

**Captured / supplied:** 2026-04-30 operator input; one screenshot is dated 2026-04-24 in filename.
**Lane:** [work-cici](../README.md) - WORK-only advisor evidence; not Cici's Record and not Grace-Mar Record truth.
**Confidence:** B - operator-supplied screenshots of Cici/Claude mobile threads; not independently reverified against GitHub or Telegram in this ingest.

## Files

- [cici-janitor-safe-transient-purge-thread-2026-04-24.jpg](cici-janitor-safe-transient-purge-thread-2026-04-24.jpg)
- [cici-ai-telegram-avatar-setup-thread-2026-04-30-a.jpg](cici-ai-telegram-avatar-setup-thread-2026-04-30-a.jpg)
- [cici-ai-telegram-avatar-setup-thread-2026-04-30-b.jpg](cici-ai-telegram-avatar-setup-thread-2026-04-30-b.jpg)

The two 2026-04-30 Telegram-avatar screenshots appear to capture the same thread state; both are retained because both source files were supplied.

## 1. Janitor safety thread

The 2026-04-24 screenshot captures a Cici repo thread about adding/refining a janitor script for transient-data cleanup.

Observed points from the screenshot:

- The assistant checks repository state before changes and notes `scripts/janitor/` and `users/cici/governed-state/operations/` did not initially exist.
- The safety model distinguishes governed persistent state from transient operational data.
- A "governed first, delete second" rule is articulated: preserve rows tagged as governed/persistent/unknown and delete only records explicitly tagged transient.
- A dry-run mode is introduced before live delete behavior.
- The thread references `scripts/janitor/purge_transient.py` and `users/cici/governed-state/operations/janitor-spec.md`.
- The assistant states the files were committed/pushed to a branch and later describes the dry-run behavior: list candidate rows and require `--execute` for real deletion.
- Safety rationale: Git remains the source of truth for doctrine/specs; Supabase is treated as operational runtime state.

Operational implication:

- This reinforces the existing work-cici pattern: Cici's runtime cleanup should be governed by explicit metadata, dry-run defaults, and Git-backed doctrine/specs. It should not silently delete ambiguous or governed rows.

Follow-up:

- On the next Cici GitHub sync, verify the current `purge_transient.py` and janitor spec on `main` or the relevant merged branch before treating this screenshot as final repo state.

## 2. cici-ai Telegram launch / avatar thread

The 2026-04-30 screenshots capture a Cici repo thread about setting up the Telegram group pinned message and group avatar.

Observed points from the screenshots:

- A PNG group avatar was generated/committed in the Cici repo, with instructions to download `docs/brand/cici-ai-avatar.png` from GitHub.
- The screenshot references branch `claude/setup-telegram-group-6iHXY`.
- The operator then uploaded the group photo in Telegram.
- Final status in the thread says:
  - section 1 pinned in `cici-ai`
  - section 2 welcome sent
  - join link recorded in evidence note
  - group avatar live, described as "navy C + teal node"
  - brand SVGs + PNG committed for future social headers
  - section 3 group description remains optional
- The operator chose "later" for the optional group description.
- The assistant states the remaining item is tracked in `cici-progress-log.md`.

Operational implication:

- The `cici-ai` launch surface is materially more complete than the older group-created evidence alone: pin, welcome, avatar, and brand assets are reportedly live/committed.
- The remaining lightweight closeout item is the one-line Telegram group description.

Follow-up:

- Verify the Cici repo branch/main state for `docs/brand/cici-ai-avatar.png` and related brand assets.
- If the optional group description becomes useful, draft a one-line description for Telegram and record whether it was applied.

## Boundary note

These screenshots are advisor evidence for work-cici. They do not approve any Cici governed-state change and do not create identity facts in Grace-Mar. Any durable Cici policy or Record-facing update belongs in Cici's own repo and approval path.
