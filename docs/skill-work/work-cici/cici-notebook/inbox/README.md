# Cici notebook — inbox (L2 operator context)

Drop **repo-local** markdown here so [`scripts/cici_journal_ob1_digest.py`](../../../../../scripts/cici_journal_ob1_digest.py) can merge it into the generated day file under **Operator context (ingested)**.

**Rolling buffer:** Prefer capturing rough notes in [../daily-cici-notebook-inbox.md](../daily-cici-notebook-inbox.md) during the day; at **`dream`**, fold into **`YYYY-MM-DD.md`** here (rolling file is not auto-cleared; prune when long — see that file). See [cici-notebook README](../README.md#daily-inbox-rolling-accumulator).

**Together with automated pulls:** If you run **`--full-day-synthesis`** (strategy-notebook + session-transcript for that date), use this folder for **extra** transcript/geo notes that did not land in those files — so the journal still has one place for spillover.

## Layout

| Path | Purpose |
|------|---------|
| **`YYYY-MM-DD.md`** | Single file for that calendar day. Optional YAML frontmatter (see below). Body is merged **first**. |
| **`YYYY-MM-DD/*.md`** | Optional folder: all `*.md` files are concatenated in **sorted filename order** **after** the single file (if present). |
| **`YYYY-MM-DD-artifacts.txt`** | One **repo-relative** path per line (from grace-mar root). Listed under **Artifacts referenced** in the journal. Lines starting with `#` are ignored. |

**Precedence:** If both `YYYY-MM-DD.md` and `YYYY-MM-DD/` exist, the digest processes **`YYYY-MM-DD.md` first**, then **`YYYY-MM-DD/*.md`**.

## YAML frontmatter (optional)

At the top of `YYYY-MM-DD.md` (or any fragment in `YYYY-MM-DD/`):

```yaml
---
artifacts:
  - docs/skill-work/work-cici/README.md
---
Your notes and Cursor exports go here.
```

Paths under **`artifacts`** must be **vouched by the operator** and must stay **secret-free**. The digest resolves them under the repo root; missing paths are skipped with a stderr warning.

## Governance

- **Redact** secrets before saving (tokens, keys, private URLs).
- **WORK only** — not Xavier’s Record, not companion gate merge.
- **Ingest triage (accept / defer / reject):** keep quality high — defer snippets to a future date’s file if needed; reject material that should not live in the repo.

## `→ Promote to history:` (human convention)

Optional last line in a day file, e.g. `→ Promote to history: phase-1 foundation shipped`. The digest does not parse this in v1; use it as a reminder when updating [`work-cici-history.md`](../../work-cici-history.md).
