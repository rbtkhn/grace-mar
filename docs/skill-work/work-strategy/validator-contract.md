# Work-strategy validator contract

**Purpose:** The validator layer gives **minimum structural integrity** checks on a strategy **packet** (task intake, sources, derived artifacts, optional gate snippet) **before** human review. It improves **pre-review signal quality** and boring backend hygiene; it does **not** adjudicate strategic truth.

**What it validates**

- Declared paths resolve where expected (artifacts vs sources behaviour differs by validator — see script output).
- Text/markdown artifacts have enough substance for review under a simple word-count heuristic (default threshold: 50 words per text artifact for “non-trivial”).
- Optional gate snippet presence when requested.
- Derived JSON output paths stay outside forbidden Record-adjacent locations (`users/**`, selected `bot/` files).
- Light scans for explicit placeholder / tension markers (surfaced as `needs_review`, not hidden).

**What it does not validate**

- Correctness of judgment, forecasts, or notebook weave quality.
- Alignment with `skill-strategy`, STRATEGY promotion rules, or VERIFY tiers.
- Gate staging, merges, or RECURSION-GATE semantics (validators never auto-edit `recursion-gate.md`).
- Identity-facing Record truth under `users/**` (validators **read** WORK paths only; they do **not** write canonical Record).

**Statuses**

| Status | Meaning |
|--------|---------|
| `pass` | Structurally **reviewable** for this layer — **not** “strategically correct.” |
| `needs_review` | Legible but incomplete, ambiguous, thin, or flagged for human attention (markers, tension language). |
| `fail` | **Not ready** as a serious handoff for review (e.g. missing expected artifact file, forbidden output path). |

Overall summary rolls up as: any `fail` → overall `fail`; else any `needs_review` → overall `needs_review`; else `pass`.

**Relation to the carry harness**

[`carry-harness.md`](carry-harness.md) receipts describe intake + artifact probes. When [`scripts/work_strategy/run_carry_harness.py`](../../../scripts/work_strategy/run_carry_harness.py) is run with **`--run-validators`**, it optionally runs [`scripts/work_strategy/validate_strategy_packet.py`](../../../scripts/work_strategy/validate_strategy_packet.py) and may embed **`validation_summary`** (and **`validation_report_path`** when a validation JSON file is written). Harness receipts remain **WORK-derived**; validators remain **optional** unless explicitly requested.

**Validator families (v1)**

| Family | Role |
|--------|------|
| Required artifact | Paths passed as `--artifact` must exist (`fail` if missing). |
| Source presence | Declared `--source` paths: missing → `needs_review`. |
| Artifact substance | Word-count heuristic on text/markdown; all thin → `needs_review`; no artifacts → `fail`. |
| Gate snippet | If `--gate-snippet` omitted → pass (“not requested”). If provided → non-empty expected. |
| Boundary | Output JSON must not target forbidden canonical paths. |
| Unresolved markers | `TODO`, `TBD`, `UNRESOLVED`, `NEEDS REVIEW`, `???` in artifact text → `needs_review` with counts. |
| Contradiction / tension markers | Substrings such as “contradiction”, “conflict”, “in tension”, “uncertain” → usually `needs_review` (surface tensions, do not erase them). |
| Markdown metadata | Light check: substantial markdown without any heading → `needs_review`. |

**Doctrine**

- Validators are **pre-review hygiene**, not truth adjudicators.
- They stay **WORK-only** and **derived** (JSON under `runtime/work-strategy/` or operator-chosen paths outside forbidden zones).
- Receipts and validation reports **must not** mutate canonical Record or Voice wiring.

Schema: [`schemas/work_strategy_validation_report.schema.json`](../../../schemas/work_strategy_validation_report.schema.json).
