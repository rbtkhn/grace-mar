# Moonshot program — template

**WORK / staging.** Copy into `users/<id>/self-moonshots.md` or a month folder. **Not** Record until promoted through the gate.

## Header (required)

- **moonshot_id:** `<short-kebab-slug>` (e.g. `one-person-studio-2027`)
- **status:** `draft` | `active` | `parked`
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

### Baseline (optional v0.1)

Where things stand today — **no** medical, legal, or financial claims without professional context; **no** fabricated numbers.

### Experiments (n=1 loop)

| Week / date | Hypothesis | Action | Result | Next |
|-------------|------------|--------|--------|------|
| … | … | … | … | … |

### Gate promotion checklist

When ready to merge durable lines into **SELF** or a dated line into **EVIDENCE:**

1. Open **`recursion-gate.md`** with a `CANDIDATE-*` block (see [moonshot-operating-model.md](../../moonshot-operating-model.md#example-recursion-gate-block-moonshot-promotion)).
2. Companion sets `status: approved` and runs `process_approved_candidates.py --apply` per [instance-doctrine.md](../../../users/grace-mar/instance-doctrine.md).

### Security / discipline

- **No** API keys, passwords, or raw credentials.
- **No** unfounded legal, medical, or financial advice; cite professional sources when load-bearing.
