# Canonical user paths

**Purpose:** Single source of truth for per-user file paths. All tooling and docs should use these **lowercase** paths. No uppercase filenames (e.g. `SELF.md`, `EVIDENCE.md`) are canonical.

**See also:** [Date and time formats](date-time-conventions.md) — `YYYY-MM-DD` for dated artifacts and CLI vs compact ids (`YYYYMMDD`, directory sharding).

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md), [Identity Fork Protocol](identity-fork-protocol.md)

---

## Paths

| Concept | Canonical path |
|--------|-----------------|
| Identity + three-dimension mind (IX-A/B/C) | `users/[id]/self.md` |
| Durable identity commitments (optional split surface) | `users/[id]/self-identity.md` |
| Activity log (ACT-*, READ-*, WRITE-*, CREATE-*) + gated approved log § VIII | **`users/[id]/self-archive.md`** — single canonical **EVIDENCE** file |
| `self-evidence.md` | **Optional compatibility pointer** for old bookmarks; tooling reads **`self-archive.md`**. Do not rely on this path for new instances. |
| Gated approved activity (voice + non-voice) | **`self-archive.md` § `## VIII. GATED APPROVED LOG (SELF-ARCHIVE)`** — appended only by `process_approved_candidates.py` |
| Pipeline staging (candidates above `## Processed`) | `users/[id]/recursion-gate.md` |
| Session / interaction history | `users/[id]/session-log.md` |
| Capability index (THINK, WRITE, etc.) | **`users/[id]/self-skills.md`** — legacy `skills.md` is still read if present (see `scripts/repo_io.py` `resolve_surface_markdown_path`) |
| Curated references, canon | `users/[id]/self-library.md` |
| Self-memory (continuity — short/medium/long; not Record) | **`users/[id]/self-memory.md`** — standard label **self-memory**. Legacy instances may still have **`memory.md`**; readers resolve **self-memory first**, then **memory.md**, via `scripts/repo_io.py` `resolve_self_memory_path`. |
| Intent (goals, tradeoffs — YAML in fenced block; see [intent-template.md](intent-template.md)) | `users/[id]/intent.md` |

All paths are **lowercase** with hyphens where used (e.g. `self-archive.md`, `recursion-gate.md`).

**`self-*` labels in prose:** Standard companion-self component names (**self-knowledge**, **self-identity**, **self-library**, …) and formal surfaces (**SELF-KNOWLEDGE**, **SELF-LIBRARY**) are defined in [id-taxonomy.md — Capitalization and format](id-taxonomy.md#capitalization-and-format).

**`intent.md`:** Not required by `assert_canonical_record_layout()` for minimal bot startup; when present it is the canonical source for `export_intent_snapshot` / manifest policy and clears export **degraded** mode when valid.

---

## Startup and tooling

Scripts and the bot resolve paths under `users/[id]/` using these names. If the expected files are missing, tooling should fail loudly. See `scripts/assert_canonical_paths.py` and env `GRACE_MAR_SKIP_PATH_CHECK` for optional skip.

**Legacy (do not create new):** `SELF.md`, `EVIDENCE.md`, `ARCHIVE.md`, `PENDING-REVIEW.md`, `SKILLS.md` (uppercase), **`skills.md`** (old capability index name), and **`memory.md`** (old self-memory filename) are **not** canonical for new work — use **`self-skills.md`** and **`self-memory.md`**. The migration script renames `skills.md` → `self-skills.md` and **`memory.md` → `self-memory.md`** when the canonical file is absent.

**Surface registry:** Internal keys and display labels (`self_skills` → Skills, `self_evidence` → Evidence, etc.) live in **`scripts/surface_aliases.py`**.

**Migration:** `python scripts/migrate_legacy_user_filenames.py --user <id> --dry-run` then `--apply`. If both `PENDING-REVIEW.md` and `recursion-gate.md` exist, use `--merge-pending-review` to append or resolve manually.

**Startup:** Telegram bot, WeChat bot, `apps/miniapp_server.py`, and `apps/gate-review-app.py` call `assert_canonical_record_layout()` and **exit with an error** if any required file is missing. Override only for special environments: `GRACE_MAR_SKIP_PATH_CHECK=1`.
