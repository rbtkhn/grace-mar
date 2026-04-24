# Cici (GitHub) — upstream path map

**Repo:** [Xavier-x01/Cici](https://github.com/Xavier-x01/Cici) · **default branch:** `main`

This table is a **convenience map** for the operator lane. **Re-verify** before treating paths as current: Cici’s `main` moves independently of grace-mar.

**Snapshot used for the tree check below:** `main` tip [`f8676b9`](https://github.com/Xavier-x01/Cici/commit/f8676b9) (fetched 2026-04-23 via [GitHub API](https://api.github.com/repos/Xavier-x01/Cici/git/trees/main?recursive=1)). Stale-OK — re-run the regen recipe.

## Regen recipe (no `gh` required)

1. **Tip commit:** `curl -sL 'https://api.github.com/repos/Xavier-x01/Cici/commits/main'` — use the `sha` field (first 7 characters are enough for a human check).
2. **Full file tree (recursive):** `curl -sL 'https://api.github.com/repos/Xavier-x01/Cici/git/trees/main?recursive=1'`
3. With `jq`: `.tree[] | select(.type=="blob") | .path` and filter, or use `python3 -c` to parse JSON and print paths with a given prefix (see [README in this folder](README.md) for context).

## Path table

| Path on `main` | Role (short) | History anchor (optional) | Verify |
|----------------|-------------|---------------------------|--------|
| [docs/governed-state-doctrine.md](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md) | Governed state doctrine (Phase 1) | [6379661](https://github.com/Xavier-x01/Cici/commit/6379661) | — |
| [docs/prompts/architect-system-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/prompts/architect-system-prompt.md) | Architect system prompt | [PR #6](https://github.com/Xavier-x01/Cici/pull/6) | — |
| [docs/prompts/end-user-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/prompts/end-user-prompt.md) | End-user prompt | [PR #6](https://github.com/Xavier-x01/Cici/pull/6) | — |
| [docs/session-bootstrap-prompt.md](https://github.com/Xavier-x01/Cici/blob/main/docs/session-bootstrap-prompt.md) | Session bootstrap (lives at `docs/`, not `docs/prompts/`) | [PR #7](https://github.com/Xavier-x01/Cici/pull/7) per [work-cici-history.md](../../../work-cici/work-cici-history.md) | — |
| [users/cici/governed-state/](https://github.com/Xavier-x01/Cici/tree/main/users/cici/governed-state) | Git-first governed state root | [6379661](https://github.com/Xavier-x01/Cici/commit/6379661) | — |
| [users/cici/governed-state/source-priority/policy.json](https://github.com/Xavier-x01/Cici/blob/main/users/cici/governed-state/source-priority/policy.json) | Source-priority policy | [PR #3](https://github.com/Xavier-x01/Cici/pull/3), [`3b25703`](https://github.com/Xavier-x01/Cici/commit/3b25703) | — |
| [users/cici/governed-state/memory-policy/policy.json](https://github.com/Xavier-x01/Cici/blob/main/users/cici/governed-state/memory-policy/policy.json) | Memory policy | [`b02b5da` chain](https://github.com/Xavier-x01/Cici); grace-mar: [cici-github-sync-2026-04-20](../../../work-cici/evidence/cici-github-sync-2026-04-20.md) | — |
| [users/cici/governed-state/operations/janitor-spec.md](https://github.com/Xavier-x01/Cici/blob/main/users/cici/governed-state/operations/janitor-spec.md) | Transient memory janitor spec | [PR #8](https://github.com/Xavier-x01/Cici/pull/8), tip [`f8676b9`](https://github.com/Xavier-x01/Cici/commit/f8676b9) | — |
| [scripts/janitor/purge_transient.py](https://github.com/Xavier-x01/Cici/blob/main/scripts/janitor/purge_transient.py) | Janitor script | [PR #8](https://github.com/Xavier-x01/Cici/pull/8) | — |
| [scripts/validate-governed-state.py](https://github.com/Xavier-x01/Cici/blob/main/scripts/validate-governed-state.py) | CI validation (Phase 1) | [6379661](https://github.com/Xavier-x01/Cici/commit/6379661) | — |
| [config/authority-map.json](https://github.com/Xavier-x01/Cici/blob/main/config/authority-map.json) | Authority map | [6379661](https://github.com/Xavier-x01/Cici/commit/6379661) | — |
| [CLAUDE.md](https://github.com/Xavier-x01/Cici/blob/main/CLAUDE.md) | Persona + operating contract | [901012d](https://github.com/Xavier-x01/Cici/commit/901012d) (companion: `.claude` layer; [2026-04-14 log](../../../work-cici/work-cici-history.md)) | — |
| [.claude/agents/self-directed-learning.md](https://github.com/Xavier-x01/Cici/blob/main/.claude/agents/self-directed-learning.md) | Self-directed learning agent | [`2e0f6ab`](https://github.com/Xavier-x01/Cici/commit/2e0f6ab) (per [2026-04-26 log](../../../work-cici/work-cici-history.md)) | — |
| [docs/skills/README.md](https://github.com/Xavier-x01/Cici/blob/main/docs/skills/README.md) | Built-in skills index (examples on `main`) | — | — |
| `docs/skills/brewmind-governed-steward.md` (target) | **Paste** body from [handoff](../../../work-cici/handoffs/cici-brewmind-governed-steward.md) | Merged in steward era [`d2358ce`](https://github.com/Xavier-x01/Cici/commit/d2358ce) (see history) | **Missing** on current `main` under `docs/skills/`; add via handoff. Canonical: [.cursor brewmind-governed-steward](../../../../../.cursor/skills/brewmind-governed-steward/SKILL.md) |
| [evidence/README.md](https://github.com/Xavier-x01/Cici/blob/main/evidence/README.md) | Instance evidence area | Phase 1 | — |

## Branch (not on `main`)

- **Telegram:** [`claude/telegram-bot-integration-Dvbdw`](https://github.com/Xavier-x01/Cici/tree/claude/telegram-bot-integration-Dvbdw) — advisor note: [cici-telegram-bot-tier-c-advisor-note](../../../work-cici/evidence/cici-telegram-bot-tier-c-advisor-note-2026-04-08.md)

## Related (not Cici instance repo)

- **brew_mind** (site): [work-cici-history.md](../../../work-cici/work-cici-history.md) · [brewmind-site sync](../../../work-cici/evidence/brewmind-site-github-sync-2026-04-15.md)
