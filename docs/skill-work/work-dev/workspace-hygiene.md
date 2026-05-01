# Workspace hygiene

WORK only; not Record.

## Purpose

This note classifies local clutter that can make audits and commits harder to read without changing system behavior. It is guidance for operators and coding agents, not a cleanup command.

## Local-only clutter classes

| Class | Examples | Default posture |
|-------|----------|-----------------|
| Audit clones | `.codex-audit/<repo>/` | Treat as operator-local evidence for a specific audit. Do not commit unless deliberately promoted into a bounded report. |
| Temp sandboxes | `.codex-tmp/`, `.pytest-tmp/`, `tmp*/` | Treat as disposable runtime scratch. Do not rely on them for source truth. |
| Pytest cache spill | `pytest-cache-files-*` | Treat as test-run byproduct. Prefer ignored local cleanup after any needed logs are copied into a real report. |
| Generated caches | `*.cache`, hidden JSON caches such as `.capability-shift-cache.json` | Classify owner and rebuild path before moving, deleting, or committing. |

## Agent rule

When these paths appear in `git status`, mention them as workspace noise unless the task explicitly asks to preserve or inspect them. Do not delete permission-protected temp trees during ordinary implementation. If cleanup is needed, do it as a separate operator-approved hygiene action.

## Commit rule

Before committing a complex branch, separate:

1. Source changes that define behavior or doctrine.
2. Rebuildable generated artifacts.
3. Audit/report outputs.
4. Local-only temp/cache/audit material.

Only the first three can be commit-worthy. The fourth should stay out of the commit unless the operator explicitly asks for an audit snapshot.
