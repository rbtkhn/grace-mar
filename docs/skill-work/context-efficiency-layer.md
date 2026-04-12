# Context Efficiency Layer (CEL)

**Purpose:** Make **governed** Grace-Mar state **cheap to load and use** in operator sessions, briefs, and harness output—without replacing the Record or smuggling ungated “truth” into the Voice.

**Scope:** Operator / **WORK execution layer** ([skills-modularity.md](../skills-modularity.md)). CEL is about **what to load, at what fidelity, and how much to paste**—not about changing **SELF / EVIDENCE / prompt** without the gate.

**Not:** A second Record. Not a license for the model to invent facts. Not default companion-facing bot prose ([AGENTS.md](../../AGENTS.md) knowledge boundary).

---

## Problem

Grace-Mar already enforces **durable truth** through the gate. The practical bottleneck is often: **too much context** in briefs and rituals, or **unclear recovery** from a summary back to source files. CEL treats that as a **systems** problem: tier, budget, and provenance-linked compaction.

---

## Operator-runtime tiers (hot / warm / cold)

These describe **loading priority for sessions and scripts**, not a second copy of MEMORY ([memory-template.md](../../memory-template.md)). You may **map** informally: hot ≈ what you need **this session**; warm ≈ **recent WORK**; cold ≈ **archive / library / older evidence**—without renaming MEMORY sections.

| Tier | Meaning | Examples |
|------|---------|----------|
| **Hot** | Load first for action | Pending gate rows, today’s territory focus, latest ACT tail |
| **Warm** | Relevant, not always inlined | work-dev/workspace, strategy-notebook week, open decision points |
| **Cold** | Provenance and retrieval | Older EVIDENCE clusters, self-library canon, historical gate logs |

---

## Representation ladder (per surface)

For **repeatedly loaded** surfaces, prefer a **cheaper action form** with **recovery** to source:

| Form | Role |
|------|------|
| **Source** | Canonical file or gate block (full fidelity) |
| **Working** | Operator summary in a notebook or WORK memo |
| **Brief** | Lines suitable for session brief / harness |
| **Runtime** | Smallest snippet for one task + path back |

See [context-compaction-protocol.md](context-compaction-protocol.md) for concrete formats.

---

## Existing machinery (do not duplicate)

- **[`config/context_budgets/`](../../config/context_budgets/)** — JSON caps on ritual paste size (`coffee.json`, `dream.json`, **`session_brief.json`**). Operator scaffolding only; not Record truth. See [README](../../config/context_budgets/README.md).
- **[`scripts/context_budget.py`](../../scripts/context_budget.py)** — `load_context_budget`, `get_int`, `get_bool`.
- **[`scripts/compress_active_lane.py`](../../scripts/compress_active_lane.py)** — one-lane **semantic** squeeze to `artifacts/context/` (not a budget cap). See [active-lane-compression.md](active-lane-compression.md).
- **[`scripts/session_brief.py`](../../scripts/session_brief.py)** — `--minimal`, `--compact` (recovery-first); optional **`--active-lane`**; tunable via `session_brief.json`.
- **[`scripts/generate_wap_daily_brief.py`](../../scripts/generate_wap_daily_brief.py)** (via `generate_work_politics_daily_brief.py`) — optional **§7** CEL footer on dated daily briefs; toggle via [`daily_brief.json`](../../config/context_budgets/daily_brief.json).
- **[`scripts/operator_daily_warmup.py`](../../scripts/operator_daily_warmup.py)** — uses `coffee` budget.

---

## Relationship to Reality Sprint Block

- **[reality-sprint-block.md](reality-sprint-block.md)** — compresses **one plan** into a single executable wedge (primary lane, first contact with reality, failure checks).
- **CEL** — assembles **cross-session** context (what is hot, what to paste, recovery links).

Use both: CEL to **load less**; Reality Sprint to **do one thing** with what you loaded.

---

## Governance and knowledge boundary

- Compact forms are **WORK / operator** artifacts unless promoted through **RECURSION-GATE** like any other change to the Record.
- Summaries shown to the **Voice** stay subject to Lexile and humane-purpose rules; do not ship CEL tables as default system prompts.

---

## Prompt budget doctrine (aspirational)

For major assemblers (daily brief, session brief, work-strategy, work-dev, gate-review), prefer explicit rules:

- **Always include** — e.g. pending count, authority reminder.
- **Include if active** — e.g. open watches, stale pending.
- **Include only by retrieval** — long EVIDENCE bodies, full library.
- **Never inline** — only path + one-line synopsis.

Enforcement is **incremental** via budgets and docs first; automation follows.

---

## Retrieval and `index_record.py` (design-only for now)

Vector index today: [`scripts/index_record.py`](../../scripts/index_record.py) embeds Record chunks in Chroma (one embedding per chunk). Multi-form retrieval (“brief” vs “full” snippet) needs a **schema decision** before implementation.

See **§ Multi-form retrieval (RFC)** below.

### Multi-form retrieval (RFC)

**Option A — Metadata on chunks:** Extend chunking / index build to attach `surface`, `tier_hint`, or `form` so retrieval can filter or rank. Touches [`bot/retriever`](../../bot/retriever.py) (and chunk pipeline) and index build.

**Option B — Sidecar summaries:** Operator-maintained or script-generated summary files under `docs/` or `users/<id>/`, keyed by source path; retrieval returns path + sidecar unless “full” requested.

**Rule:** No silent LLM summarization of Record into “truth”; provenance links required.

Until one option is chosen, **do not** promise four retrieval forms in production code.

---

## Single rule

**Every governed surface operators hit repeatedly should have a documented path to a cheaper, provenance-linked action form—with recovery to source.** CEL + [context-compaction-protocol.md](context-compaction-protocol.md) + [reality-sprint-block.md](reality-sprint-block.md) + [context budgets](../../config/context_budgets/) implement that split.
