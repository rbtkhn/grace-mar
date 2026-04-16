# Strategy expert — templates (WORK only)

**Single source** for the three on-disk files each commentator uses. When adding someone new, either copy **each** section below into its own file (name on the section heading) or run `python3 scripts/expand_strategy_expert_template.py --expert-id <slug> [--full-name "..."]` from the repo root (`--dry-run` to preview). `validate_expert_profiles.py` still validates real `strategy-expert-<id>.md` profiles only; this bundle file is skipped.

Jump: [Profile](#profile-template) · [Thread](#thread-template) · [Transcript](#transcript-template)

---

<a id="profile-template"></a>

## Profile → `strategy-expert-<expert_id>.md`

# Strategy expert — <Full name> (`<expert_id>`)

WORK only; not Record.

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) — **`<expert_id>`** lane.

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | <full name> |
| **expert_id** | `<expert_id>` |
| **Role** | <one-line lane description> |
| **Default grep tags** | <tags in cold> |
| **Typical pairings** | <batch-analysis partners> |

## Convergence fingerprint

### Recurrent convergences

- `<expert_id>` + `<partner_id>` — <shared mechanism / shared claim>

### Convergence conditions

- This expert usually converges when:
  - <condition>

## Tension fingerprint

### Recurrent tensions

- `<expert_id>` x `<partner_id>` — <recurring disagreement>

### Tension conditions

- This expert usually tensions when:
  - <condition>

## Signature mechanisms

- <mechanism this expert returns to repeatedly>

## Recurrent claims

- <claim this expert makes across episodes>

## Failure modes / overreads

- <where this expert overstates / flattens / misses>

## Predictive drift / accuracy notes

- <what changed over time>
- <where prior calls held / failed>

## Active weave cues

- Pull this expert into weave when:
  - <condition>

## Knot-use guidance

- Best used for: <page types / question shapes>
- Usually insufficient alone for: <what needs pairing>

## History resonance defaults

- Typical HN chapter families: <history-notebook chapter ids>
- Typical mechanism hooks: <mechanism pointers>

## Published sources (operator web index)

1. <url>
2. <url>
3. <url>

## Seed

<operator standing notes>

---

**Companion files:** [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day rolling verbatim) and [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled analytical thread).

---

<a id="thread-template"></a>

## Thread → `strategy-expert-<expert_id>-thread.md`

# Expert thread — `<expert_id>`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (verbatim ingests) + relevant **knot** files (where this expert’s material was used).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine extraction** block between markers. Operator / assistant maintains the **narrative journal** above the markers in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; machine block — when you run **`thread`**.
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile) and [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day verbatim).

---

## Narrative journal

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. This section is **not** overwritten by the **`thread`** script._

_(No narrative distillation yet — add prose above the markers, not inside them.)_

---

<!-- strategy-expert-thread:start -->

### Machine extraction (script-maintained)

_The block between the HTML comments is replaced on each `thread` run. Do not put the narrative journal here._

_(No transcript or knot material for extraction.)_

<!-- strategy-expert-thread:end -->

<!-- Optional: stable machine-readable ledger (YAML/JSON). Not overwritten by default extraction. Uncomment and edit if tooling needs it.

```thread-ledger
expert_id: <expert_id>
last_thread_run: null
knot_paths: []
```

-->

---

<a id="transcript-template"></a>

## Transcript → `strategy-expert-<expert_id>-transcript.md`

# Expert transcript — `<expert_id>`

WORK only; not Record.

**Source:** Verbatim lines from [`daily-strategy-inbox.md`](daily-strategy-inbox.md) that include `thread:<expert_id>`, routed automatically on ingest.
**Retention:** 7-day rolling window; date sections older than 7 days are pruned automatically.
**Editing:** Operator may lightly edit for clarity after triage. Edits are preserved across triage runs (append-only, not overwrite).
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile) and [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled thread).

---

<!-- Triage appends new date sections below. Do not add content above this line. -->
