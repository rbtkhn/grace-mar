# Expert naming — residual audit and upstream sync

WORK-only reference. Not Record.

## Residual audit (maintenance)

**Last run:** 2026-04-16.

**Checks** (repository text search):

- **Legacy pre-migration slugs** (`alexander-mercouris`, `john-mearsheimer`, `jiang-xueqin`, etc.): **none** in tracked `*.md` / `*.py` / `*.json` / `*.yaml` sources reviewed for the last-name migration.
- **`thread:` with multiple hyphen segments** in strategy-notebook: only **non-expert** topic ids in commentary (for example `hormuz-story-fork` in [strategy-commentator-threads.md](strategy-commentator-threads.md) archive prose). Inbox **`thread:<expert_id>`** lines use **single-segment** ids aligned with [`scripts/strategy_expert_corpus.py`](../../../../scripts/strategy_expert_corpus.py) `CANONICAL_EXPERT_IDS`.
- **`strategy-expert-<a>-<b>-` pattern:** spurious hits are **HTML comment** markers such as `strategy-expert-thread:start`, not legacy `strategy-expert-<given>-<family>-*.md` filenames.

**Re-run:** search for old double-name expert stems if you add new docs; `python3 scripts/validate_expert_profiles.py` from repo root.

## Upstream `civilization_memory` (optional diff)

| | Grace-Mar | civilization_memory (when `research/repos/civilization_memory` is present) |
|---|-----------|--------------------------------------------------------------------------------|
| Tri-mind templates | [`strategy-notebook/minds/CIV-MIND-*.md`](minds/) — ASCII hyphen; **redirect** to `strategy-expert-*-mind.md` | `docs/templates/CIV–MIND–*.md` — **en-dash** in filename per upstream convention |
| Full fingerprint bodies | **SSOT:** `strategy-expert-<expert_id>-mind.md` at strategy-notebook root | Optional governance / longer templates — diff for drift only |

**Policy:** Grace-Mar keeps full mind bodies in-repo without requiring civ-mem. Pulling changes from upstream is **operator-reviewed**; not an automatic sync.

**Optional diff** (when both trees exist), example:

```bash
diff -u \
  research/repos/civilization_memory/docs/templates/CIV–MIND–MEARSHEIMER.md \
  docs/skill-work/work-strategy/strategy-notebook/strategy-expert-mearsheimer-mind.md
```

Use the **redirect** path when comparing bookmark stability: `minds/CIV-MIND-MEARSHEIMER.md` → same body as `strategy-expert-mearsheimer-mind.md`.

If the submodule directory is missing, skip or update the checkout per instance bootstrap; see cross-links in [AGENTS.md](../../../../AGENTS.md) and [minds/README.md](minds/README.md).

## Lens-fold verify token

Inbox and transcripts use **`verify:lens-fold+<expert_id>`** (same id as **`thread:<expert_id>`**). Documented in [strategy-expert-template.md](strategy-expert-template.md) (journal layer, *Lens vs lane*) and [.cursor/skills/skill-strategy/SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md).
