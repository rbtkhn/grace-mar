# User instance template (documentation)

This folder documents **required filenames** for a Grace-Mar instance. It is **not** a runtime template copied by automation today; the live instance is [`../grace-mar/`](../grace-mar/).

**Canonical paths** (flat under `users/<id>/`): see [docs/canonical-paths.md](../../docs/canonical-paths.md).

| File | Role |
|------|------|
| `self.md` | SELF — identity + IX-A/B/C |
| `skills.md` | SKILLS |
| `self-archive.md` | EVIDENCE — activity log + § VIII gated approved |
| `self-evidence.md` | optional compatibility pointer to `self-archive.md` |
| `recursion-gate.md` | Pipeline staging |
| `session-log.md` | Session history |
| `self-archive.md` | Gated approved activity log |
| `self-library.md` | SELF-LIBRARY (optional) |

A future subdirectory layout is discussed in [docs/adr/0001-users-directory-layout-future.md](../../docs/adr/0001-users-directory-layout-future.md); until then, keep the flat layout.

**Large binaries:** prefer [Git LFS](https://git-lfs.com/) for committed media under `users/<id>/artifacts/`; see `.gitignore` notes for local-only patterns.
