# User instance template (documentation)

This folder documents **required filenames** for a Grace-Mar instance. It is **not** a runtime template copied by automation today; the live instance is [`../grace-mar/`](../grace-mar/).

**Canonical paths** (flat under `users/<id>/`): see [docs/canonical-paths.md](../../docs/canonical-paths.md).

| File | Role |
|------|------|
| `self.md` | SELF — identity + IX-A/B/C |
| `self-skills.md` | SKILLS — capability index (legacy `skills.md` still resolved until migrated) |
| `self-archive.md` | EVIDENCE — activity log + § VIII gated approved |
| `self-evidence.md` | optional compatibility pointer to `self-archive.md` |
| `recursion-gate.md` | Pipeline staging |
| `session-log.md` | Session history |
| `self-library.md` | SELF-LIBRARY (optional) |
| `work-dev.md` | WORK — development and technical-systems context for this companion (starts blank; seeded via `seed-phase/work_dev_seed.json`; not the same as operator `docs/skill-work/work-dev/`) |

**`work-dev.md`** begins as a blank module and is populated only from seed-survey evidence, explicit user input, or later governed work-layer updates. It is distinct from **`self-skill-work`**: the skill file tracks work-related capability claims, while **`work-dev.md`** tracks user-specific development and technical-systems context.

A future subdirectory layout is discussed in [docs/adr/0001-users-directory-layout-future.md](../../docs/adr/0001-users-directory-layout-future.md); until then, keep the flat layout.

**Large binaries:** prefer [Git LFS](https://git-lfs.com/) for committed media under `users/<id>/artifacts/`; see `.gitignore` notes for local-only patterns.
