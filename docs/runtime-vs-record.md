# Runtime vs durable Record

**Purpose:** One-screen map of what is **canonical and governed** versus what is **temporary, derived, or operator-only** — so skill cards, lane compression, and harness output stay in the right bucket.

**Companion:** [operator-mental-model.md](operator-mental-model.md) (navigation-oriented summary).

---

## Durable Record (four surfaces)

These change only through the **gated pipeline** and companion-approved merge ([AGENTS.md](../AGENTS.md)):

| Surface | On-disk anchors (typical) | Holds |
|---------|---------------------------|--------|
| **SELF** | `users/<id>/self.md` | Identity, SELF-KNOWLEDGE (IX-A/B/C), narrative |
| **SELF-LIBRARY** | `users/<id>/self-library.md` | Governed reference, CIV-MEM scopes |
| **SKILLS** | `users/<id>/self-skills.md` | Capability index (THINK / WRITE / WORK skills as documented) |
| **EVIDENCE** | `users/<id>/self-archive.md` | Activity log, artifacts log, approved evidence |

**Approval Inbox:** `users/<id>/recursion-gate.md` — staging only until processed.

---

## Work territories (`docs/skill-work/work-*`)

**WORK** lanes are for planning, judgment, notebooks, and execution support. They are **not** Record truth. Promotion into SELF / EVIDENCE / prompt requires the same **gate + merge script** as any other profile change.

---

## Runtime-only and derived (not Record)

| Kind | Examples | Rule |
|------|------------|------|
| **Session / harness paste** | Warmup output, operator menus, chat context | Weather, not policy; do not treat as SELF |
| **MEMORY** | `users/<id>/self-memory.md` | Continuity; **not** a substitute for gated facts |
| **Skill cards** | `artifacts/skill-cards/*.json` from [`build_skill_cards.py`](../scripts/build_skill_cards.py) | Derived from portable skills; [spec](skills/skill-card-spec.md) |
| **Active lane compression** | `artifacts/context/active-lane-*.md` from [`compress_active_lane.py`](../scripts/compress_active_lane.py) | Points back to lane README and `self-work.md`; [doc](skill-work/active-lane-compression.md) |
| **Vector index** | `users/<id>/.chroma` | Retrieval aid; rebuild from Record |
| **Runtime observations ledger** | `runtime/observations/index.jsonl` | Append-only work-lane notes; [README](../runtime/observations/README.md); not Record |

---

## Must never bypass approval

- No “helpful” merges into `self.md`, `self-archive.md`, or `bot/prompt.py` without **RECURSION-GATE** + documented merge path.
- No treating **derived** summaries as new facts in the Voice or Record.

---

## Forecasting boundary

Forecast outputs belong to WORK unless and until a human separately stages a downstream conclusion for review.
A forecast artifact is not a Record fact.
It is a provisional planning object with explicit assumptions, invalidators, and uncertainty.
See [docs/skill-work/work-forecast/forecast-protocol.md](skill-work/work-forecast/forecast-protocol.md).

## Forecast receipts and observability

Forecast artifacts, forecast receipts, and forecast observability reports belong to WORK.
They are rebuildable legibility surfaces, not Record truth.

A forecast may inform planning.
A forecast may not directly redefine identity, memory, or canonical claims.

## Forecast references inside work-strategy

Forecast artifacts may be cited inside watches, notebooks, and decision points in WORK.
That citation does not make the forecast a Record fact.

Forecasting belongs to planning and judgment support.
Record changes still require separate staging and approval.

---

## Where to read next

- [conceptual-framework.md](conceptual-framework.md) — triad and knowledge boundary  
- [docs/skill-work/context-efficiency-layer.md](skill-work/context-efficiency-layer.md) — CEL  
- [artifacts/README.md](../artifacts/README.md) — derived artifact policy  
