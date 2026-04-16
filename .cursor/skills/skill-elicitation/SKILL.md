---
name: skill-elicitation
preferred_activation: elicit
description: "Bounded elicitation pass extracting tacit operator knowledge into five structured WORK files (rhythm, decisions, dependencies, friction, thresholds). Review-first; not Record truth. Upstream model: OB1 Work Operating Model Activation."
---

# Elicitation (operator knowledge extraction)

**Preferred activation (operator):** say **`elicit`**, **`elicit [layer]`**, or **`elicitation pass`**.

Extract tacit operator knowledge into explicit, reviewable WORK artifacts. The target is **operational clarity** — not abstract self-description, not personality biography.

---

## When to use

- Populating a new `work-elicitation/` lane from scratch (full five-layer pass).
- Refreshing one or two layers after a role change, workflow shift, or accumulated drift.
- Grounding a downstream lane (cadence, strategy, think, write) with operator-specific context it currently lacks.
- Operator says "elicit," "interview me," "extract my workflow," or equivalent.

**Not for:** Record/SELF updates (use RECURSION-GATE), personality profiling (use IX-C pipeline), or abstract values work.

---

## Five layers

| Layer | File | Core question |
|-------|------|---------------|
| 1. **Rhythms** | `operator-rhythm.md` | How do you actually work across day / week / month? |
| 2. **Decisions** | `operator-decisions.md` | What judgments recur? What makes them easy or hard? |
| 3. **Dependencies** | `operator-dependencies.md` | What people, systems, sources, and timing shape the work? |
| 4. **Friction** | `operator-frictions.md` | What repeatedly wastes attention, time, or momentum? |
| 5. **Thresholds** | `operator-thresholds.md` | What counts as good enough? When escalate, stop, continue, or ask? |

All files live under `docs/skill-work/work-elicitation/`.

---

## Modes

### Full pass (`elicit` or `elicitation pass`)

Run all five layers in order. Each layer is a bounded interview block:

1. Ask concrete questions (prefer examples over abstractions).
2. Distinguish ideal pattern from real pattern.
3. Identify repeated judgment calls.
4. Note uncertainty honestly.
5. Show the operator a checkpoint summary of what was captured.
6. Wait for confirmation before writing to the file.

### Single-layer pass (`elicit rhythm`, `elicit friction`, etc.)

Run one layer only. Same interview discipline, scoped to that layer's file.

### Telemetry-grounded pass (`elicit from telemetry`)

Skip the interview. Read `work-cadence-events.md`, session transcripts, and git history to populate layers from observed data. Present findings for operator review before writing.

---

## Steps (agent)

1. **Read current state.** Open the target file(s) under `docs/skill-work/work-elicitation/`. Note what's already populated and what's blank.

2. **Choose mode.** Full pass, single-layer, or telemetry-grounded (based on operator's trigger or agent judgment).

3. **For each layer:**
   - Ask 3–5 concrete questions. Prefer "what do you actually do" over "what do you value."
   - When the operator answers, extract structured entries that match the file's template.
   - Show a checkpoint summary: "Here's what I'd write to `operator-rhythm.md` — confirm or edit?"
   - On confirmation, write to the file using StrReplace (preserve existing content; append or refine).

4. **Contradiction pass** (after completing 2+ layers or a full pass):
   - Cross-check across layers: do stated rhythms match stated frictions? Do thresholds contradict decision logic? Does the dependency map explain the friction log?
   - Surface contradictions to the operator: "Your rhythm says mornings are best for strategy, but your friction log shows meetings every morning. Which is more accurate?"
   - Do not resolve contradictions silently — present them.

5. **Write session note** (optional): save raw interview material to `elicitation-sessions/YYYY-MM-DD-[layer]-pass.md` if the session produced substantial raw content worth preserving.

6. **Update history:** append one line to `work-elicitation-history.md` summarizing what was captured and which layers changed.

---

## Interview principles

- **Concrete over abstract.** "Walk me through yesterday" beats "describe your ideal day."
- **Real over ideal.** "What actually happens when you're interrupted" beats "how do you handle interruptions."
- **Examples over categories.** "Give me a recent decision that was hard" beats "what types of decisions are hard."
- **Repeated patterns over one-offs.** A friction that happens weekly matters more than a friction that happened once.
- **Operational over biographical.** "What do you check first when you sit down" beats "what motivates you."
- **Short questions, long answers.** The operator's time is the scarce resource; the agent's job is to ask tight questions and capture the full answer.

---

## Guardrails

- **WORK only.** No edits to `self.md`, `self-archive.md`, or `bot/prompt.py`.
- **Review-first.** Show checkpoint summaries before writing. Do not populate files silently.
- **Not Record truth.** Elicitation outputs are operator working notes, not identity claims. They inform downstream lanes by reference, not automatic propagation.
- **Not a dumping ground.** Each entry should be useful to at least one downstream lane. If it's not actionable, it doesn't belong.
- **Operator can veto.** Any captured entry can be removed or edited by the operator at any time.

---

## Relation to other skills and lanes

| Skill / lane | Relation |
|--------------|----------|
| **coffee** | Rhythm layer informs what coffee should emphasize at reentry |
| **dream** | Rhythm + friction layers inform what dream should check at closeout |
| **bridge** | Rhythm layer informs when bridge is most useful |
| **skill-strategy** | Decisions + thresholds layers inform strategy judgment quality |
| **work-cadence** | Telemetry-grounded mode reads cadence events as input |
| **lane-survey** | Run a lane survey before creating work-elicitation if evaluating alternatives |

---

## Related files

- `docs/skill-work/work-elicitation/README.md` — lane boundary and contents
- `docs/skill-work/work-elicitation/work-elicitation-history.md` — append-only log
- `docs/skill-work/work-template.md` — lane creation checklist
- Upstream model: [OB1 Work Operating Model Activation](https://github.com/NateBJones-Projects/OB1/tree/main/recipes/work-operating-model-activation)
