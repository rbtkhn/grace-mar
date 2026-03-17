# Forks directory

Each subdirectory is one **cognitive fork**: an isolated namespace for that fork’s Record, pipeline, artifacts, and logs. The filesystem and permissions model are designed for multi-tenant boundaries so multiple forks can coexist with clean separation; the pilot runs a single fork (grace-mar). See [Fork isolation and multi-tenant design](../docs/fork-isolation-and-multi-tenant.md).

## Structure

```
users/
├── fork-config.json.example   # Example per-fork config (copy to <fork_id>/fork-config.json to override quotas/retention)
├── grace-mar/                  # Active pilot fork
│   ├── self.md
│   ├── skills.md
│   ├── self-evidence.md
│   ├── session-log.md
│   ├── recursion-gate.md
│   ├── self-archive.md
│   ├── artifacts/
│   ├── fork-config.json       # optional: quotas, retention (see example)
│   └── ...
└── <future-fork-id>/           # Each new fork gets its own directory; no shared writable space
```

- **Namespace:** All fork-owned data lives under `users/<fork_id>/`. No cross-fork paths.
- **Discovery:** Scripts use `list_forks()` ([repo_io](scripts/repo_io.py)) to enumerate fork IDs (directories that contain `self.md` or `recursion-gate.md`).
- **Default fork:** Runtime default is `GRACE_MAR_USER_ID` (default `grace-mar`). Export, merge, and operator scripts take `-u <fork_id>`.

## Quotas and retention (per-fork)

Quotas and retention are defined per fork so one fork cannot exhaust shared resources and each can have different rules. Optional `users/<fork_id>/fork-config.json` can set:

- **Quotas:** e.g. `artifact_storage_mb`, `pipeline_events_max`, `pending_candidates_max`
- **Retention:** e.g. `memory_ttl_days`, `archive_rotate_entries`, `session_transcript_max_mb`

See `fork-config.json.example` and [Fork isolation §7](../docs/fork-isolation-and-multi-tenant.md#7-fork-config-optional). Scripts that enforce quotas or retention use `load_fork_config(fork_id)` and fall back to defaults when the file is missing.

## Export and import (per-fork)

- **Export:** All export commands are scoped to one fork: `export_fork.py -u <id>`, `export_prp.py -u <id>`, `export_runtime_bundle.py -u <id>`, etc. Output is a snapshot of that fork only.
- **Import:** Future import/restore must write only under `users/<target_fork_id>/` and must not touch other forks.

## Storage and privacy

- **Audit trail:** Git commit history
- **Versioning:** Every update is a commit
- **Backup:** GitHub remote; per-fork export for portability
- **Privacy:** Fork data is sensitive. Repo should remain private. Per-fork access is enforced by namespace and operator permissions (see [Fork isolation §2](../docs/fork-isolation-and-multi-tenant.md#2-permissions-model)).

---

*Last updated: March 2026*
