# Active lane compression (CEL)

**Purpose:** One **operator-facing command** that turns a single `docs/skill-work/work-*` lane into the smallest useful **action form** with **recovery links** — aligned with the [Context Efficiency Layer](context-efficiency-layer.md) (CEL), not a second Record.

**Script:** [`scripts/compress_active_lane.py`](../../scripts/compress_active_lane.py)

**Default output:** `artifacts/context/active-lane-<lane>.md` (or `.json` with `--json`)

---

## Not the same as JSON context budgets

| Mechanism | Role |
|-----------|------|
| **[`config/context_budgets/`](../../config/context_budgets/)** | Caps **paste size** for rituals (`session_brief.json`, `coffee.json`, …) — machine-readable limits. |
| **`compress_active_lane.py`** | One **semantic** squeeze of **one lane** (objective, next step, risks, paths) — operator memo, not a cap table. |

Do not merge the two stories: budgets **truncate**; lane compression **selects and points**. Both live under CEL as “load less, recover fast.”

---

## Relationship to other CEL tools

- **[`scripts/session_brief.py`](../../scripts/session_brief.py)** — `--minimal` / `--compact` can take **`--active-lane work-<id>`** to append the same compressed block (no separate file required for that run).
- **[`docs/skill-work/context-efficiency-layer.md`](context-efficiency-layer.md)** — operator-runtime tiers and representation ladder.
- **[Reality sprint block](reality-sprint-block.md)** — one **plan** wedge; lane compression orients one **territory** folder.

---

## Usage

```bash
python3 scripts/compress_active_lane.py --lane work-strategy
python3 scripts/compress_active_lane.py --lane strategy   # normalized to work-strategy
python3 scripts/compress_active_lane.py --lane work-dev --json
```

Governance: output is **WORK / operator** only. It does not merge into SELF, EVIDENCE, or prompt without the gate.
