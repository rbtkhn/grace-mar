# SEED-MANIFEST — companion-xavier v1 (grace-mar monorepo)

**Status:** Initial scaffold. **Visibility:** Private repo — treat seeded job/SMM docs as sensitive.

## Allowed roots (grace-mar surfaces)

| Root | Path | v1 note |
|------|------|---------|
| work-politics | [docs/skill-work/work-politics/](../../work-politics/) | **Links** from [seed-context README](companion-xavier/docs/seed-context/README.md); not full copy of territory |
| work-companion-xavier | This folder | Interface + policy |
| work-dev | [docs/skill-work/work-dev/](../../work-dev/) | Linked from seed-context |
| work-business | [docs/skill-work/work-business/](../../work-business/) | Linked from seed-context |
| self-work | [docs/skill-work/self-work/](../self-work/) | Territory README + pattern; instance file under `users/xavier/self-work.md` is **placeholder** |
| SELF-LIBRARY governance | [docs/library-schema.md](../../../library-schema.md), [boundary doc](../../../boundary-self-knowledge-self-library.md) | Merged into **`companion-xavier/users/xavier/self-library.md`** — **empty `entries:`** |

## `users/xavier/` (subtree) — placeholder flags

| File | v1 |
|------|-----|
| `self-library.md` | **Merged** — governance + `entries: []` only (no grace-mar LIB rows) |
| `self.md`, `self-evidence.md`, `recursion-gate.md`, `session-log.md`, `self-archive.md`, `intent.md`, `memory.md`, `self-work.md`, `skills.md`, `skill-think.md`, `skill-write.md` | **Placeholder** — minimal shells until Session 0 MCQ → gate → approve |
| `FORK-ID.md` | **Human/agent hint** — `fork_id: xavier` |

## Repo root symlink

| Artifact | Purpose |
|----------|---------|
| `users/xavier` → `../docs/skill-work/work-companion-xavier/companion-xavier/users/xavier` (symlink from repo `users/`) | So `scripts/validate-integrity.py --user xavier` and tooling resolve [canonical paths](../../canonical-paths.md) |

## Explicit non-goals (v1)

- No copy of `users/grace-mar/**` Record.
- No automated MCQ → candidate parser (manual staging).
- Voice/bot optional; MVP = files + survey + gate.
