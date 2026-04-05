# Date and time formats (repository-wide)

**Purpose:** One place for how **dates** appear in **filenames**, **CLI arguments**, and **machine-readable fields** so new scripts and docs stay consistent.

**Related:** [canonical-paths.md](canonical-paths.md) (per-user filenames), [daily-brief-template.md](skill-work/work-strategy/daily-brief-template.md) (dated WORK output).

---

## Calendar dates in paths and CLI — `YYYY-MM-DD`

Use **ISO 8601 calendar dates** (hyphenated) when the intent is a **human-readable day** tied to the repo or operator workflow:

| Use | Example |
|-----|---------|
| Dated markdown artifacts | `daily-brief-2026-03-29.md`, `weekly-brief-2026-03-09.md` |
| Shell | `$(date +%Y-%m-%d)` in `-o` paths |
| Script flags | e.g. `--start YYYY-MM-DD` for weekly brief scaffolds |
| Doc placeholders | `YYYY-MM-DD` in templates and YAML examples |

**Do not** introduce **MM/DD/YYYY** or **DD/MM/YYYY** for new repo conventions, filenames, or documented CLI args.

---

## Timestamps with time — ISO-8601 UTC in logs and JSON

For **instant** fields (pipeline events, session manifests, sidecars), prefer:

- `YYYY-MM-DDTHH:MM:SSZ` (UTC, `Z` suffix), or
- `YYYY-MM-DD HH:MM:SS` in prose logs when timezone is stated separately (`UTC`).

**Operator session clock (optional paste):** `python3 scripts/operator_clock.py` prints one current UTC instant on a single line; `--date-only` prints `YYYY-MM-DD` (UTC calendar day). Use when you want one authoritative “now” alongside Cursor **user_info** or external doc dates.

---

## Compact forms — ids, stamps, and sharding (not hyphenated day)

These are **intentionally not** `YYYY-MM-DD` in one token; changing them would break existing ids and on-disk layout.

| Pattern | Role |
|---------|------|
| **`YYYYMMDD`** | Compact **day** in ids and filenames where punctuation is awkward (e.g. session ids `SES-YYYYMMDD-NNN`, some task/event prefixes, compression JSON `*-YYYYMMDD.json` per work-jiang docs). |
| **`YYYYMMDD_HHMMSS`** or **`YYYYMMDDTHHMMSSZ`** | Sortable **one-blob** stamps (backups, envelopes). |
| **`YYYY/MM/`** directories | **Sharding** for session manifests under `users/[id]/sessions/` (year and month segments; still year-first). See [fork-lifecycle.md](fork-lifecycle.md). |
| **`YYYY-Www`** | **ISO week** labels where the unit is a week, not a calendar day (e.g. analytics). |

---

## Parsing human prose dates

Some tooling **accepts** multiple inputs when reading **calendar prose** (e.g. `May 19, 2026`). ISO `YYYY-MM-DD` is tried **first**; English month names are fallbacks for parsing only — not the canonical **output** shape for new artifacts. See `scripts/work_politics_ops.py` (`_parse_date`) for the pattern.

---

## JavaScript and external trees

In-repo JS that needs a calendar day for filenames often uses `new Date().toISOString().split('T')[0]` — equivalent to **`YYYY-MM-DD`**. Vendored or mirror trees (e.g. under `research/repos/`) may follow their own upstream rules; this doc applies to **Grace-Mar first-party** conventions.
