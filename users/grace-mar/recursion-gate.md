# RECURSION GATE — grace-mar

> Staging file for the gated profile pipeline — **one queue per companion, every channel.**
> Writers include **Telegram**, **WeChat**, **operator/Cursor** (activity reports, `calibrate_from_miss`, `parse_we_did`), **Mini App** (when wired), and **test/harness** runs. Each candidate carries **`channel_key`** (e.g. `telegram:…`, `operator:cursor`, `test:…`) so you can see the source. **Same gate, same merge** — not Telegram-only.
>
> **Workflow (one gate):**
> 1. Review each candidate below
> 2. Change `status: pending` to `status: approved` or `status: rejected`
> 3. Tell the assistant: **"approve"** — the agent immediately processes approved candidates into self.md, self-evidence.md, session-log.md, and prompt.py. No separate "process the review queue" step.
>
> **Merge checklist (correctness before approve):**
> 1. **Grounded** — Tied to something the companion actually said or did (or artifact), not invented or world-knowledge leakage.
> 2. **Merge-ready** — Would you ship this to SELF/EVIDENCE without embarrassment? If it feels like filler or duplicate IX, reject or edit.
> 3. **No duplicate lane** — Same fact already in IX-A/B/C? Reject or fold into existing entry instead of piling candidates.
> 4. **Human pass** — If only the analyst saw the exchange, one quick re-read of `example_from_exchange` / source lines.
> 5. **Portability** — For `portable-working-identity` candidates, also check [portability review checklist](../../docs/portable-record/portability-review-checklist.md).
>
> **Review checklist** (legacy one-liner): Grounded in the exchange? No LLM inference beyond it? No contradiction with existing Record?
>
> **Intent (before approve — long agents / optimization framing):** Models optimize toward task completion; constraints must be explicit. Ask: (1) **What would I not want** even if this candidate "succeeds"? (2) **When should we stop and ask** the companion? (3) **If this conflicts with INTENT**, companion + INTENT win — reject or revise. See **design-notes §11.9** (Misalignment at the interface).
>
> Machine-written by **`bot/core.py`** (Telegram, WeChat, activity reports) and by **operator scripts** that stage here — only edit the `status` field (and optional rejection notes).
>
> **Territory (work-politics vs companion):** For **work-politics** candidates, set **`territory: work-politics`** or **`channel_key: operator:wap`** (optionally `operator:wap:brief-name`). Operator tools then filter: `python scripts/operator_blocker_report.py -u grace-mar --territory wap` (work-politics territory only) or `--territory companion` (Record only). Same file, different lens.
>
> **Invariant:** Every **pending** or **approved-not-yet-merged** candidate must sit **above** `## Processed`. The bot inserts new blocks immediately before `## Processed`. If anything pending appears below Processed, move it up or merge will not see it.

---

## Candidate classification (Comprehension Envelope)

Optional YAML keys on each `### CANDIDATE-…` fenced block. **Orthogonal** to traffic **`risk_tier`** (`quick_merge_eligible` / `review_batch` / `manual_escalate` from [recursion-gate-three-tier.md](../../docs/recursion-gate-three-tier.md) and [recursion_gate_review.py](../../scripts/recursion_gate_review.py)) — do **not** reuse `risk_tier` for a `low`/`medium`/`high` blast-radius ladder.

| Field | Values | Role |
|-------|--------|------|
| **`impact_tier`** | `low` \| `medium` \| `high` \| `boundary` | Blast radius / promotion sensitivity of **this** merge (content), not review traffic. |
| **`envelope_class`** | `none` \| `optional` \| `required` | Whether a **Comprehension Envelope** block is omitted, recommended, or required. |

**Intended pairing:** `low` → `none`; `medium` → `optional`; `high` or `boundary` → `required`. Full vocabulary: [comprehension-envelope-gate.md](../../docs/governance/comprehension-envelope-gate.md).

**Optional check:** `python3 scripts/validate_gate_comprehension_envelope.py -u grace-mar` (warns if `envelope_class: required` but envelope missing; `--strict` exits non-zero).

### Comprehension Envelope template

Place **below** the closing YAML fence of the candidate block, still under the same `### CANDIDATE-…` section:

```markdown
### Comprehension Envelope
- What this is:
- Why this path:
- Why not the next-best option:
- Blast radius:
- Assumptions / fragile points:
- Human override applied:
```

**Authoring:** 1–2 sentences per bullet; name concrete surfaces; `unknown` allowed; no motivational filler; reviewer scannable in ~30 seconds.

### Examples (illustrative)

Not live candidates — copy the shape when adding real **pending** blocks above `## Processed`.

**Example A — low impact, no envelope**

```yaml
impact_tier: low
envelope_class: none
status: pending
# … other required candidate keys …
```

*(No `### Comprehension Envelope` block for this class.)*

**Example B — boundary impact, envelope required**

```yaml
impact_tier: boundary
envelope_class: required
status: pending
# … other required candidate keys …
```

```markdown
### Comprehension Envelope
- What this is: One IX-A line from a daily-brief claim already verified under Links with dated citations.
- Why this path: Knowledge belongs in SELF when stable; the brief was intake only.
- Why not the next-best option: Pasting the full brief into SELF would bloat IX-A; leaving it only in days.md would skip the Record.
- Blast radius: Single IX-A bullet; no prompt or abstention rule change.
- Assumptions / fragile points: Source may need refresh if the situation moves; companion may narrow wording on approve.
- Human override applied: none.
```

---

## Candidates

## Processed

### CANDIDATE-0014 through CANDIDATE-0018 — rejected 2026-04-17

```yaml
profile_target: IX-A. KNOWLEDGE
status: rejected
reason: "Operator deferred all IX-A population — will seed knowledge entries in a future session"
```

### CANDIDATE-0007 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-strategy/README.md, strategy-notebook (64 expert files)
summary: "Geopolitics and international relations"
merged_as: CUR-0001
```

### CANDIDATE-0008 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: users/grace-mar/work-jiang.md, LIB-0149
summary: "Jiang philosophy and Predictive History"
merged_as: CUR-0002
```

### CANDIDATE-0009 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-dev/README.md, work-companion-self/README.md
summary: "AI systems design and companion-self architecture"
merged_as: CUR-0003
```

### CANDIDATE-0010 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-politics/README.md
summary: "Political consulting (interest only)"
merged_as: CUR-0004
```

### CANDIDATE-0011 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-civ-mem/README.md, LIB-0157
summary: "Civilizational history and structured knowledge"
merged_as: CUR-0005
```

### CANDIDATE-0012 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: library_shelf
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: users/grace-mar/self-library.md
summary: "Theology"
merged_as: CUR-0006
```

### CANDIDATE-0013 — approved 2026-04-17

```yaml
mind_category: curiosity
signal_type: lane_engagement
profile_target: IX-B. CURIOSITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-xavier/README.md, work-alpha-school/README.md
summary: "Mentoring and teaching methodology"
merged_as: CUR-0007
```

### CANDIDATE-0001 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-decisions.md, operator-rhythm.md
summary: "Cognitive style — evaluate-then-pick with compression"
merged_as: PERS-001
```

### CANDIDATE-0002 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-rhythm.md, operator-decisions.md
summary: "Interaction mode — short prompts, menu-driven selection"
merged_as: PERS-002
```

### CANDIDATE-0003 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-thresholds.md
summary: "Quality standard — falsifiable thesis + attributed sources + named tensions"
merged_as: PERS-003
```

### CANDIDATE-0004 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-rhythm.md
summary: "Work rhythm — punctuated resets"
merged_as: PERS-004
```

### CANDIDATE-0005 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-decisions.md
summary: "Decision failure sensitivity"
merged_as: PERS-005
```

### CANDIDATE-0006 — approved 2026-04-17

```yaml
mind_category: personality
signal_type: elicitation_extract
profile_target: IX-C. PERSONALITY
status: approved
channel_key: operator:cursor
source: docs/skill-work/work-elicitation/operator-frictions.md
summary: "Friction signature — cold-thread context loss and premature infrastructure"
merged_as: PERS-006
```

*(Cleared at reseed 2026-04-14. Previous candidates archived in `archive/companion-freeze-abby-2026-04-14/`. Full history in git tag `companion-freeze/abby-2026-04-14`.)*
