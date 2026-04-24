# Cici notebook — synthesis sources

**Territory:** WORK / operator coaching — not Cici’s Record, not companion gate merge.

This document describes **what feeds** the generated day file from [`scripts/cici_journal_ob1_digest.py`](../../../../scripts/cici_journal_ob1_digest.py) and **how recursive learning** stays visible.

## Layers

| Layer | Source | In output |
|-------|--------|-----------|
| **L1** | GitHub API — commits on **Cici** `main` for the local calendar window | **Day overview (auto from commits)** + **OB1 repo activity (links to GitHub)** |
| **L2a** | [`inbox/`](inbox/README.md) markdown (manual Cursor/geo notes) | **Operator context** — **### Inbox** |
| **L2a′** | *(Workflow only)* [daily-cici-notebook-inbox.md](daily-cici-notebook-inbox.md) folded at **`dream`** into **`inbox/YYYY-MM-DD.md`** (rolling buffer not auto-cleared; prune when long — see inbox file) — not read by the digest directly | Becomes part of L2a after fold |
| **L2b** | Optional **[strategy-notebook](../../work-strategy/strategy-notebook/)** `chapters/YYYY-MM/days.md` — same `## YYYY-MM-DD` block (`--include-strategy-notebook` or `--full-day-synthesis`) | **### From strategy-notebook (same day)** — geopolitical / cross-territory judgment for that calendar day |
| **L2c** | Optional [`users/grace-mar/session-transcript.md`](../../../../users/grace-mar/session-transcript.md) (`--include-session-transcript` or `--full-day-synthesis`) | **### From session-transcript.md** |
| **L3** | YAML `artifacts:` in inbox frontmatter and/or `inbox/YYYY-MM-DD-artifacts.txt` | **Artifacts referenced** (repo-relative links; missing files warned on stderr) |

**Contract:** Nothing is pulled from Cursor’s cloud automatically. To **capture transcript discussion and geopolitical ideas** in each journal page, use **`--full-day-synthesis`** (or set env **`CICI_JOURNAL_FULL_DAY_SYNTHESIS=1`**) so the digest pulls **strategy-notebook + session-transcript** for the same calendar day, and/or add notes under **`inbox/`**.

## CLI flags (digest)

| Flag / env | Effect |
|------------|--------|
| `--full-day-synthesis` | Shorthand: enables **`--include-session-transcript`** and **`--include-strategy-notebook`**. |
| `CICI_JOURNAL_FULL_DAY_SYNTHESIS=1` | Same as `--full-day-synthesis` (unset when you want flags off). |
| `XAVIER_JOURNAL_FULL_DAY_SYNTHESIS=1` | Legacy alias — same as `CICI_JOURNAL_FULL_DAY_SYNTHESIS`. |
| `--no-inbox` | Skip `inbox/` and artifact sidecars — L1-only output. |
| `--include-session-transcript` | Transcript lines whose bracket date matches the calendar day (caps apply). |
| `--include-strategy-notebook` | Paste the **`## YYYY-MM-DD`** section from that month’s strategy **`days.md`** (max chars configurable). |
| `--strategy-notebook-max-chars` | Cap for the strategy excerpt (default 10000). |
| `--session-transcript-path` | Override path to session transcript (default: `users/grace-mar/session-transcript.md`). |
| `--repo-root` | Resolve artifact paths (default: grace-mar root). |

## Boundaries

- **Secrets:** Redact before inbox save; the script does not scrub bodies.
- **Record:** Do not treat journal text as RECURSION-GATE or SELF input without the normal pipeline.
- **Tension:** If L1 (commits) and L2 (notes) disagree, do **not** force resolution in code. Add a single **Tension:** line in inbox prose if surfacing the gap helps recursive learning.

## Recursive learning

1. **Promotion:** Strong days can motivate a milestone in [`work-cici-history.md`](../work-cici-history.md); optional human line `→ Promote to history:` in inbox (not parsed by the script in v1).
2. **Catch-up:** `--catch-up-from-last-dream` backfills missing days; empty days may mean quiet work or missing inbox — adjust habit, not blame.
3. **Rolling review:** Every few days, consider [harvest](../../../../.cursor/skills/harvest/SKILL.md) or a narrative pass using recent `cici-notebook/*.md` as context so the log stays **read**, not write-only.
4. **Ingest triage:** **accept / defer / reject** for inbox material (see [inbox/README.md](inbox/README.md)).
5. **Meta-defaults:** Quarterly, revisit whether full-day synthesis (transcript + strategy excerpt) is worth the size/noise; adjust `--strategy-notebook-max-chars` or caps in the script if needed.
6. **Rolling daily inbox:** Optional [daily-cici-notebook-inbox.md](daily-cici-notebook-inbox.md) → fold at **`dream`** into **`inbox/YYYY-MM-DD.md`** (becomes L2a); buffer prunes by length, not mandatory nightly reset — see README § *Daily inbox (rolling accumulator)*.

## Phase E backlog (future automation)

Not implemented in the digest by default; candidates if current L2 still feels insufficient:

- Same-day anchor line from **work-cici-history.md** (parse or manual).
- **work-cadence-events.md** lines for the calendar day (UTC date matching policy TBD).
- Cici **PRs/issues** and **GitHub Actions** conclusions (extra API scope).

Optional **LLM summarization** of operator context remains out of scope unless added later with an explicit flag and policy.
