# Moonshot program — template

**WORK / staging.** Copy into `users/<id>/self-moonshots.md`, a mission folder under [`missions/`](missions/README.md), or a month folder. **Not** Record until promoted through the gate.

## Header (required)

- **moonshot_id:** `<short-kebab-slug>` (e.g. `one-person-studio-2027`)
- **display_id (optional):** `MS-XXX` if you use numeric labels alongside the slug (operator convention only; not a second authority).
- **status:** `draft` | `active` | `parked` | `archived`
- **declared (date):** `YYYY-MM-DD`
- **owner:** Instance / operator name (informational)
- **Lexile / Voice note:** Text intended for eventual merge into **`self.md`** should match the instance **Lexile ceiling** (grace-mar: **600L** unless evidence supports raising it) and [humane-purpose](../../prompt-humane-purpose.md) framing.

## Sections

### Goal

One paragraph: what “done” looks like (measurable where possible).

### Why (alignment)

Why this moonshot matters — ties to **SELF** IX-B / IX-C themes without assuming merge (staging language OK).

### Success metrics

| Metric | Target | How measured |
|--------|--------|----------------|
| … | … | … |

### Failure or stop conditions

When you would **pause**, **pivot**, or **archive** this moonshot (concrete signals, not vague discouragement).

### Constraints and forbidden shortcuts

- **Constraints:** time, scope, dependencies, or jurisdiction you accept up front.
- **Forbidden shortcuts:** what you will **not** do to claim progress (e.g. hollow metrics, unsafe automation).

### Baseline (optional)

Where things stand today — **no** medical, legal, or financial claims without professional context; **no** fabricated numbers. If you cite **EVIDENCE**, point to **merged** `self-archive.md` entries or staged facts—nothing here **auto-merges** into EVIDENCE.

### Related WORK surfaces (optional)

Link-only; all **non-canonical** until promoted through the gate.

| Kind | Where to link |
|------|----------------|
| Mission-scale spec | `missions/<slug>/mission-spec.md` ([mission-spec-template.md](mission-spec-template.md)) |
| Tacit / experiments | [tacit-capture](../../tacit-capture/README.md) → normalized → candidates → mission `intake/` |
| Strategy experts (threads) | `docs/skill-work/work-strategy/strategy-notebook/experts/<name>/` (WORK; not Voice Record) |

Do **not** treat helpers, bots, or “sub-agents” as bypassing **recursion-gate** or merge scripts.

### Experiments (n=1 loop)

| Week / date | Hypothesis | Action | Result | Next |
|-------------|------------|--------|--------|------|
| … | … | … | … | … |

### Cross-moonshot links (optional)

- **Synergies:** other moonshots or missions this reinforces.
- **Trade-offs:** where progress here costs attention elsewhere.

### Operator snapshot (optional, manual)

Simple table you fill by hand—**not** auto-generated Record truth.

| Field | Value |
|-------|--------|
| Last reviewed | |
| Next experiment due | |
| Open recursion-gate items | _(ids, if any)_ |

### Gate promotion checklist

When ready to merge durable lines into **SELF** or a dated line into **EVIDENCE:**

1. Open **`recursion-gate.md`** with a `CANDIDATE-*` block (see [moonshot-operating-model.md](../../moonshot-operating-model.md#example-recursion-gate-block-moonshot-promotion)).
2. Companion sets `status: approved` and runs `process_approved_candidates.py --apply` per [instance-doctrine.md](../../../users/grace-mar/instance-doctrine.md).

### Security / discipline

- **No** API keys, passwords, or raw credentials.
- **No** unfounded legal, medical, or financial advice; cite professional sources when load-bearing.
