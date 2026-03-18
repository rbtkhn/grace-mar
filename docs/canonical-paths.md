# Canonical user paths

**Purpose:** Single source of truth for per-user file paths. All tooling and docs should use these **lowercase** paths. No uppercase filenames (e.g. `SELF.md`, `EVIDENCE.md`) are canonical.

**Governed by:** [GRACE-MAR-CORE v2.0](grace-mar-core.md), [Identity Fork Protocol](identity-fork-protocol.md)

---

## Paths

| Concept | Canonical path |
|--------|-----------------|
| Identity + three-dimension mind (IX-A/B/C) | `users/[id]/self.md` |
| Activity log (ACT-*, READ-*, WRITE-*, CREATE-*) | `users/[id]/self-evidence.md` |
| Gated log of approved activity (voice + non-voice) | `users/[id]/self-archive.md` |
| Pipeline staging (candidates above `## Processed`) | `users/[id]/recursion-gate.md` |
| Session / interaction history | `users/[id]/session-log.md` |
| Capability containers (THINK, WRITE, etc.) | `users/[id]/skills.md` |
| Curated references, canon | `users/[id]/self-library.md` |

All paths are **lowercase** with hyphens where used (e.g. `self-evidence.md`, `recursion-gate.md`).

---

## Startup and tooling

Scripts and the bot resolve paths under `users/[id]/` using these names. If the expected files are missing, tooling should fail loudly. See `scripts/assert_canonical_paths.py` and env `GRACE_MAR_SKIP_PATH_CHECK` for optional skip.

**Legacy (do not create new):** `SELF.md`, `EVIDENCE.md`, `ARCHIVE.md`, `PENDING-REVIEW.md`, `SKILLS.md` (uppercase) are **not** canonical. Tooling and runtime expect only the table above.

**Migration:** `python scripts/migrate_legacy_user_filenames.py --user <id> --dry-run` then `--apply`. If both `PENDING-REVIEW.md` and `recursion-gate.md` exist, use `--merge-pending-review` to append or resolve manually.

**Startup:** Telegram bot, WeChat bot, `miniapp_server`, and `gate-review-app` call `assert_canonical_record_layout()` and **exit with an error** if any required file is missing. Override only for special environments: `GRACE_MAR_SKIP_PATH_CHECK=1`.
