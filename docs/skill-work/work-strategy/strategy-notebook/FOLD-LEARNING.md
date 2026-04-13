# Fold learning — metrics and recursive review

**Purpose:** Optional **append-only** ledger for **strategy-notebook folds** so you can compare sessions over time (compression proxies, verification surface, fold kind) and calibrate **how** you fold—not to claim a single objective “insight score.”

**Governed by:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Fold choice and section weighting* · [daily-strategy-inbox.md](daily-strategy-inbox.md) · [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md).

**Boundary:** **WORK / operator coaching** — not Record, not **MEMORY**, not **RECURSION-GATE**. Data file: `users/<id>/strategy-fold-events.jsonl` (same namespace as `pipeline-events.jsonl`; different purpose).

---

## Ledger file

**Path:** `users/<id>/strategy-fold-events.jsonl` — one **JSON object per line** (JSONL).

**Minimum fields (each line):**

| Field | Required | Description |
|-------|------------|-------------|
| `ts` | yes | ISO-8601 UTC timestamp when the log line was written |
| `notebook_date` | yes | `YYYY-MM-DD` — target `##` heading in `chapters/YYYY-MM/days.md` |
| `fold_kind` | yes | `manual` (operator **`fold`**), `dream` ( **`dream`** closeout), or `explicit` (other explicit instruction) |

**Optional fields:**

| Field | Description |
|-------|-------------|
| `inbox_chars` | Size of inbox scratch below the append line **before** the fold (characters), if measured |
| `days_delta_chars` | Net characters added/changed in that day’s `##` block for this fold, if measured (e.g. from diff) |
| `counts` | Object with integer counts, e.g. `signal_bullets`, `judgment_bullets`, `links_items`, `open_bullets` — **manual** entry unless you add automation later |
| `ratings` | Honor-system: `verify_depth` 1–3, `judgment_freshness` 1–3 (optional) |
| `would_reread` | Boolean — would you reread this block in a month? |
| `note` | Single line, ≤200 characters — what worked, what to try next |
| `git_ref` | Commit SHA if the fold shipped in the same session |

Incomplete rows are **valid**; trends use whatever fields exist.

---

## Compression proxy (factual, limited)

When **both** `inbox_chars` and `days_delta_chars` are present and `inbox_chars` > 0:

**compression_proxy** = `days_delta_chars / inbox_chars`

**Interpretation (heuristic):** Lower values mean the **notebook delta was small relative to scratch** (tight synthesis, heavy deletion from buffer). Higher values mean **large net write to the page per unit of scratch** (expansive fold or large paste promotion). Neither is automatically “good”; pair with **note** and qualitative read.

The report script labels **tightest** (minimum ratio) and **loosest** (maximum ratio) folds in the window for review—not “best insight.”

---

## Commands

**Log one fold** (after you fold, optional):

```bash
python3 scripts/log_strategy_fold.py -u grace-mar \
  --notebook-date 2026-04-13 \
  --fold-kind manual \
  --inbox-chars 12000 \
  --days-delta-chars 4200 \
  --ratings verify_depth=2,judgment_freshness=3 \
  --would-reread \
  --note "Marandi+Parsi merge; trimmed duplicate batch lines"
```

**Read-only report** (stdout, markdown):

```bash
python3 scripts/report_strategy_fold_learning.py -u grace-mar --days 30
```

Optional: `--jsonl /path/to/file.jsonl` for testing or relocation; `--max-events` to cap rows.

**Auto git SHA:** `python3 scripts/log_strategy_fold.py ... --auto-git` (uses `git rev-parse HEAD`; ignores failure silently).

---

## Monthly ritual (recursive learning)

1. Run `report_strategy_fold_learning.py` for **30** or **90** days.
2. Read **tightest** vs **loosest** folds and your **notes**—look for **patterns** (e.g. intra-day folds always loose; dream folds tighter).
3. Adjust **one habit** in [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) or your fold practice—not the metric target.

---

## Anti-patterns (gaming)

- Maximizing **volume** or **self-ratings** to “win” the ledger.
- Treating **compression_proxy** as truth without reading the **day block**.
- Logging **without** folding or logging **every** session mechanically when it adds no signal—**optional** tool.

---

## Phase 2 (not required for v1)

- Parse `git show` to estimate `days_delta_chars` for a section (fragile).
- Bullet counters scoped to `## notebook_date` in `days.md` (regex-boundary careful).

---

## See also

- [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Fold choice and section weighting](STRATEGY-NOTEBOOK-ARCHITECTURE.md#fold-choice-and-section-weighting-inbox--yyyy-mm-dd)
- [`.cursor/skills/dream/SKILL.md`](../../../../.cursor/skills/dream/SKILL.md) — optional log after **`dream`** fold
