# work-strategy — observability

**Lane:** WORK (`work-strategy`). Observability here is **process-oriented**: volume, hygiene, and tooling usage — **not** strategic truth and **not** Record.

See [runtime-vs-record.md](../../runtime-vs-record.md) and [AGENTS.md](../../../AGENTS.md).

---

## Two complementary surfaces

| Surface | Script | Output | What it measures |
|--------|--------|--------|------------------|
| **Notebook / doctrine hygiene** | [`scripts/build_strategy_observability.py`](../../../scripts/build_strategy_observability.py) | `artifacts/work-strategy/strategy-observability.json` | Decision points, inbox depth, `days.md` structure, STRATEGY promotion proxies — judgment **notebook** health. |
| **Carry-stack / runtime JSON** | [`scripts/work_strategy/summarize_carry_receipts.py`](../../../scripts/work_strategy/summarize_carry_receipts.py) | e.g. `runtime/work-strategy/observability/summary.json` + optional `.md` | Carry receipts, validation reports, task-shape reports, review packets — optional **task-run** tooling usage and outcomes. |

They are intentionally separate: the first reflects **long-form strategy notebook** posture; the second reflects **bounded harness / validator / classifier / review-packet** runs under `runtime/work-strategy/`. Neither replaces the other; neither is canonical Record.

---

## Carry-stack observability (PR 5)

### Purpose

Give the operator a **compact, regenerable** summary of how often the carry harness, validators, task-shape classifier, and review-packet builder are used and how often outcomes land in **pass** / **fail** / **needs_review**, without adding a database, a web dashboard, or a new source of truth.

### Source inputs

Read-only JSON under configurable directories (defaults relative to `--runtime-root`, usually `runtime/work-strategy/`):

| Subdirectory | Role |
|--------------|------|
| `carry-receipts/` | [`run_carry_harness.py`](../../../scripts/work_strategy/run_carry_harness.py) receipts |
| `validation-reports/` | [`validate_strategy_packet.py`](../../../scripts/work_strategy/validate_strategy_packet.py) reports |
| `task-shape-reports/` | [`classify_task_shape.py`](../../../scripts/work_strategy/classify_task_shape.py) reports |
| `review-packets/` | [`build_review_packet.py`](../../../scripts/work_strategy/build_review_packet.py) packets |

Optional overrides: `--receipts-dir`, `--validation-dir`, `--task-shape-dir`, `--review-packet-dir` (each resolved under `--runtime-root` when relative).

Schemas: [`schemas/work_strategy_observability_report.schema.json`](../../../schemas/work_strategy_observability_report.schema.json).

### Metrics emitted (machine-readable)

Top-level fields include `window`, `counts`, `task_shapes`, `validation` (validator id rollups), `review_packets` (coverage of validation/task-shape/gate fields), `gate_prep`, `files_scanned`, and `notes`.

- **Carry outcomes:** `pass_total`, `fail_total`, `needs_review_total` come from carry receipts’ `result` (with fallback to `summary.status` when needed).
- **Validation reports:** separate counts for `summary.status` on validation JSON files; `top_failed_checks` / `top_needs_review_checks` aggregate validator row ids across files.
- **Task shapes:** frequencies of `classification.primary_shape` in task-shape JSON files.
- **Review packets:** how many packets declare validation/task-shape paths in `inputs`; how many have `gate_prep.snippet_present`.
- **Gate prep:** counts of snippet-ready / non-empty signals from carry receipts and review packets (combined totals in `snippet_present_count` / `snippet_non_empty_count`).

### What it does not summarize

- Strategic correctness, geopolitical claims, or notebook judgment quality (beyond what validators encode structurally).
- Record merges, gate approvals, or Voice behavior.
- Anything outside the scanned JSON files (if you never write receipts, counts stay zero).

### Interpretation guidance

- Metrics describe **tooling and process**, not “was the strategy right.”
- Summaries are only as good as the receipts on disk; sparse runtime directories yield sparse reports.
- Repeated validator ids under **failed** / **needs_review** point to **weak seams** or noisy artifacts worth fixing upstream.
- Low `review_packets_total` with high carry runs suggests review packets are optional and may simply not be in use yet.

### Regeneration

From repo root:

```bash
python3 scripts/work_strategy/summarize_carry_receipts.py \
  --runtime-root runtime/work-strategy \
  --out runtime/work-strategy/observability/summary.json \
  --markdown-out runtime/work-strategy/observability/summary.md
```

Optional: `--last N` (per artifact class, most recent by timestamp), `--since YYYY-MM-DD`, `--json` (stdout). Outputs must not target forbidden roots (`users/**`, blocked `bot/` files); the script refuses those paths.

### Runtime vs Record reminder

These artifacts are **derived** and **rebuildable**. They do **not** authorize merges into `self.md`, `self-archive.md`, or `bot/prompt.py`. The companion gate remains the only merge path for durable Record changes.

---

## Notebook-centric observability (legacy section)

**Artifact:** `artifacts/work-strategy/strategy-observability.json` via [`build_strategy_observability.py`](../../../scripts/build_strategy_observability.py).

### Metrics — structure (v1)

| Field | Meaning |
|-------|---------|
| `structure.decision_point_files` | Markdown files under `decision-points/` (excl. README) |
| `structure.decision_points_open` | Files whose `**Status:**` line is `open` |
| `structure.authorized_sources_yaml_entries` | Rows in `authorized-sources.yaml` |
| `structure.promotion_policy_present` | `promotion-policy.json` exists |

### Metrics — judgment quality (v2)

| Field | Meaning | Healthy range |
|-------|---------|----------------|
| `judgment_quality.notebook_entries_total` | Total `## YYYY-MM-DD` blocks across all months | Growing; 0 early is fine |
| `judgment_quality.inbox_pending_lines` | Non-blank lines below the append marker in `daily-strategy-inbox.md` | 0–30 normal; >50 = overdue weave or prune |
| `judgment_quality.promotion_date_mentions` | Date strings found in `STRATEGY.md` (proxy for promotion activity) | 0 fine early; sustained 0 over months = notebook may not feed STRATEGY |
| `months.<YYYY-MM>.dated_entries` | Entries that month | Variable |
| `months.<YYYY-MM>.avg_sections_per_entry` | Average of Chronicle/Reflection/References/Open present per entry | 4.0 = all four; <3.0 = sections skipped regularly |
| `months.<YYYY-MM>.avg_links_per_entry` | Average link/path references per `### References` section | >2 healthy; <1 = under-cited judgment |
| `months.<YYYY-MM>.open_carry_forward` | Open sections with unresolved items (verify, deferred, questions) | Active threads normal; very high relative to entries = debt |

**Not yet auto-computed:** recommendation acceptance/rejection, cross-lane reference counts — require operator logging convention.

**Notebook markers (`[watch]`, `[decision]`, `[promote]`):** not counted in this JSON; definitions live in [NOTEBOOK-PREFERENCES.md](strategy-notebook/NOTEBOOK-PREFERENCES.md#escalation-marker-preference). Extend [`build_strategy_observability.py`](../../../scripts/build_strategy_observability.py) before documenting marker counts here.

### Alignment

Optional alignment with [schema-registry/observability-report.v1.json](../../../schema-registry/observability-report.v1.json) for top-level dashboards is a future mapping; `strategy-observability.json` uses `schemaVersion` `2.0.0-work-strategy`.

**Authority:** Observability does **not** trigger Record merges. See [promotion-ladder.md](promotion-ladder.md).
