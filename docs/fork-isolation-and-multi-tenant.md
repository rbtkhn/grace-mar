# Fork Isolation and Multi-Tenant Design

**Purpose:** Define clean boundaries so each cognitive fork is isolated by namespace, with room for per-fork quotas, retention, permissions, and export/import — even when the pilot runs a single fork. Designing for multi-tenant boundaries now avoids a painful rewrite when adding a second fork or family mesh.

**Status:** Design adopted; implementation uses `users/<fork_id>/` as the sole namespace. Quotas and retention are specified here and wired via optional config; enforcement can be added incrementally.

**Authority:** Subordinate to [GRACE-MAR-CORE](grace-mar-core.md) and [Identity Fork Protocol](identity-fork-protocol.md).

---

## 1. Fork namespace

Each fork has a **stable identifier** (e.g. `grace-mar`, `pilot-002`). All fork-owned data lives under one directory:

```
users/<fork_id>/
├── self.md
├── self-evidence.md
├── recursion-gate.md
├── session-log.md
├── session-transcript.md
├── self-archive.md
├── memory.md
├── pipeline-events.jsonl
├── artifacts/
├── fork-config.json   # optional: quotas, retention, overrides (see §7)
└── ...
```

- **No cross-fork paths:** Scripts and services resolve paths via `profile_dir(fork_id)` (or equivalent). There is no shared writable space between forks.
- **Default fork:** The pilot and single-user deployments use `GRACE_MAR_USER_ID` (default `grace-mar`) as the active fork. All code that today reads `USER_ID` or `PROFILE_DIR` is effectively “current fork”; multi-tenant routing (e.g. by URL or header) passes `fork_id` into the same resolution.
- **Discovery:** `list_forks()` (or equivalent) enumerates fork IDs by scanning `users/` for directories that contain at least one canonical file (e.g. `self.md` or `recursion-gate.md`) so tooling and dashboards can show “which forks exist” without hardcoding.

---

## 2. Permissions model

- **Per-fork operator:** Each fork can have an operator (or operator set) that can approve/reject candidates, submit observations, and run merge for that fork only. Stored as config or env (e.g. `GRACE_MAR_OPERATOR_*` for default fork; future: `users/<id>/fork-config.yaml` or operator registry).
- **Global operator (optional):** A super-operator or admin who can act on any fork is an explicit choice: either one shared secret with access to all fork APIs, or a per-fork token. The design prefers **per-fork tokens** for audit and isolation; a global role can be implemented as “holds all per-fork tokens” or a separate permission layer.
- **Companion / family:** The companion (and, for minors, parent/guardian) is the sovereign over the fork. Operator actions are on behalf of the companion; they do not create a second authority. Permissions are “who can act as operator for this fork,” not “who owns the Record” (ownership stays with the companion).

No cross-fork access: a request scoped to fork A must never read or write fork B’s directory or pipeline.

---

## 3. Quotas (per-fork)

Quotas are defined per fork so that one busy or abusive fork cannot exhaust shared resources. Implemented when needed; schema and resolution are defined now.

| Quota | Scope | Default (pilot) | Enforcement |
|-------|--------|------------------|-------------|
| **Artifact storage** | Total size under `users/<id>/artifacts/` | None (or e.g. 500 MB) | Reject uploads when over; optional background check |
| **Pipeline events** | Lines in `pipeline-events.jsonl` | None (or e.g. 50k) | Rotate or trim oldest when over |
| **Pending candidates** | Count in `recursion-gate.md` | None (or e.g. 200) | Warn operator; optional hard cap on staging |
| **Session transcript** | Size or lines of `session-transcript.md` | None | Rotate or trim when over |
| **Compute / API** | Token or request limits per fork | Per provider | Rate-limit by `fork_id` in ledger or gateway |

Quota values and overrides live in **fork config** (see below). Scripts and services that perform the constrained operation (upload, stage, append event) resolve the fork’s config and check before proceeding.

---

## 4. Retention rules (per-fork)

Retention defines how long data is kept and when it is rotated or pruned. Per-fork so one fork can have strict retention and another long-term.

| Data | Rule | Default (pilot) |
|------|------|------------------|
| **MEMORY** | Ephemeral; prune entries older than TTL | e.g. 14 days (see `rotate_context.py`) |
| **SELF-ARCHIVE** | Rotate when size/count threshold | e.g. ~1 MB or 2,500 entries (see `rotate_telegram_archive.py`) |
| **Session transcript** | Optional trim or rotate | Keep all (or cap size) |
| **Pipeline events** | Optional trim oldest | Keep all (or cap lines) |
| **Artifacts** | Optional delete or archive by age | Keep all |

Retention is expressed in **fork config** (e.g. `memory_ttl_days`, `archive_rotate_entries`). Scripts like `rotate_context.py` and `rotate_telegram_archive.py` take `--user <fork_id>` and read that fork’s config so each fork can have different rules.

---

## 5. Export / import (per-fork)

- **Export:** All export scripts (`export_fork.py`, `export_prp.py`, `export_runtime_bundle.py`, `export_user_identity.py`, etc.) take `-u <fork_id>`. Export output is a snapshot of that fork only; no other fork’s data is included.
- **Import:** Future “import fork” or “restore from backup” should write only under `users/<target_fork_id>/` and optionally create the fork if it does not exist. Import must validate and sanitize so one fork’s import cannot overwrite another’s.
- **Portability:** Per [Portability](portability.md), the companion owns their Record; export is for transfer or consumption. Each fork’s export is self-contained and identifiable by `user_id` / `fork_id` in the manifest.

---

## 6. Deployment

- **Single process, single fork (pilot):** One server process with `GRACE_MAR_USER_ID=grace-mar`. All requests are for that fork. No routing; paths and permissions are as today.
- **Single process, multi-fork:** One server (e.g. `apps/miniapp_server.py`, `apps/gate-review-app.py`) with tenant resolution: fork ID from URL path (e.g. `/operator/grace-mar/console`), subdomain (e.g. `grace-mar.grace-mar.com`), or header (e.g. `X-Fork-Id`). Each request resolves `profile_dir(fork_id)` and uses that fork’s config and permissions. No cross-fork access.
- **One process per fork:** Each fork runs in its own process (or container) with its own `GRACE_MAR_USER_ID`. Simple isolation; operational cost scales with fork count. Good for strict isolation or when quotas/retention are enforced at the process boundary.

The filesystem and permissions model support all three; deployment chooses one.

---

## 7. Fork config (optional)

Optional file `users/<fork_id>/fork-config.json` overrides defaults and supplies quotas and retention without code changes. Implemented in `scripts/repo_io.py`: `load_fork_config(fork_id)` returns the dict or `None`.

**Example schema:**

```json
{
  "fork_id": "grace-mar",
  "display_name": "Grace-Mar",
  "quotas": {
    "artifact_storage_mb": 500,
    "pipeline_events_max": 50000,
    "pending_candidates_max": 200
  },
  "retention": {
    "memory_ttl_days": 14,
    "archive_rotate_entries": 2500,
    "session_transcript_max_mb": 10
  }
}
```

Omit keys for no limit or default. Scripts that need quotas or retention call `load_fork_config(fork_id)` and use values when present; otherwise fall back to env or code defaults.

---

## 8. Cross-instance collaboration (separate repos)

When a companion’s fork lives in **another repository** (e.g. peer instance from companion-self), mentor and peer still follow **one protocol per fork**, but **no shared `users/` tree**. Boundaries, optional leakage scans, and advisor work modules are spelled out in [cross-instance-boundary.md](cross-instance-boundary.md).

---

## 9. Summary

| Concern | Design choice |
|--------|----------------|
| **Namespace** | One directory per fork: `users/<fork_id>/`. All resolution goes through a single helper (e.g. `profile_dir(fork_id)`). |
| **Permissions** | Per-fork operator; optional global role. No cross-fork access. |
| **Quotas** | Per-fork; defined in config or env; enforcement at upload/stage/append. |
| **Retention** | Per-fork; defined in config or env; rotation scripts take `fork_id`. |
| **Export/import** | Export always scoped to one fork; import writes only to target fork. |
| **Deployment** | Single-fork (pilot), single-process multi-fork, or one-process-per-fork; same filesystem model. |

The pilot remains single-user with `GRACE_MAR_USER_ID` defaulting to `grace-mar`. The same codebase and repo layout support multiple forks with clean boundaries; adding a second fork is then configuration and routing, not a rewrite. For **two repositories** (mentor + external peer), see §8 and [cross-instance-boundary.md](cross-instance-boundary.md).
