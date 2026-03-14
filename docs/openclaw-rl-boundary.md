# OpenClaw-RL / RL data boundary (Grace-Mar)

This doc sets **what may and may not** flow into **reinforcement learning**, **fine-tuning**, or **shared training datasets** when you use tools such as [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) alongside Grace-Mar. It does **not** change the gated pipeline for **SELF / EVIDENCE / prompt** — only **optional downstream use** of exported logs.

---

## Principles

1. **Record ≠ training set** — Merged **SELF** is authoritative for the Voice. RL updates **model weights**; that is a **different** surface from **human-approved profile text**. Do not treat automatic trajectory export as consent to train on the child’s identity without explicit operator policy.

2. **Minors** — If the companion is a minor, assume **no** raw chat in third-party or pooled RL until a guardian-defined policy says otherwise. Prefer **operator-curated, redacted** snippets only.

3. **No secrets in trajectories** — Same as OpenClaw-RL’s README: never export API keys, tokens, passwords, or medical/legal identifiers into JSONL you might share or upload.

4. **Staging is not canonical** — **RECURSION-GATE** pending text can be wrong, duplicate, or analyst-inferred. Do not use pending candidates as **ground truth** for RL labels; **applied** merges are closer to “approved signal” only when operator intended that.

5. **Knowledge boundary** — Do not use RL to **inject** facts into the Record. Grace-Mar merges only through **RECURSION-GATE + approval**. RL may tune **style or tool use in harness**; it does not replace the gate.

6. **Runtime memory boundary** — A Hindsight-style retain/recall layer may improve session continuity inside a downstream runtime, but it remains **runtime state**, not Record state. Auto-retained summaries, extracted entities, or recalled snippets must not be treated as canonical identity truth.

---

## Next-state signals

Every action produces a **next-state signal**: a user reply, operator correction, gate outcome, tool result, validation failure, UI transition, or other post-action state that reveals something about the previous step. Grace-Mar should recover these signals as feedback for **workflow** and **policy** improvement, while keeping **Record** change sovereign and gated.

Next-state signals contain two different kinds of information:

- **Evaluative signals** — indicate whether the action worked: approve/reject, pass/fail, good/bad, satisfied/unsatisfied
- **Directive signals** — indicate how the action should have been different: "check the file first", "wrong layer", "use fake data first", "this belongs in WORK, not SELF"

Grace-Mar is especially rich in **directive** signals because many failures are category mistakes, workflow-order mistakes, or ontology mistakes rather than simple output failures.

### Safe adaptation target

By default, next-state signals may improve:

- **workflow** — task order, review rhythm, validation habits, handoff discipline
- **policy** — prompting, routing, tool choice, search behavior, shell-first implementation rhythm

They must **not** directly update:

- **SELF / Record truth**
- **IX-A / IX-B / IX-C**
- **prompt knowledge**
- any other companion-owned identity surface

Compressed rule: **use next-state signals freely for process improvement, cautiously for policy improvement, and never ungated for identity improvement.**

---

## Boundary model

### Runtime memory is workflow state, not Record truth

Hindsight-style memory systems may:

- retain recent conversation for continuity
- recall context before the next turn
- improve local runtime behavior

They may not:

- write to SELF / EVIDENCE / prompt knowledge
- bypass RECURSION-GATE
- turn background extraction into approved identity facts

If runtime memory produces a useful observation, split it:

- use it immediately as runtime continuity if helpful
- stage it separately if it might matter to the Record

Do not let runtime memory collapse these two functions into one.

### Safe for workflow adaptation

- repeated validation misses
- repeated handoff omissions
- repeated task-order mistakes
- deterministic integrity / governance failures

These may justify changes to process, checklists, reminders, or task decomposition.

### Safe for bounded policy adaptation

- operator corrections about search order, file reading order, or scope control
- repeated misses like "too broad", "wrong layer", "should have checked X first"
- recurring routing mistakes between `SELF`, `SKILLS`, `WORK`, and `LIBRARY`

These may justify visible prompt, routing, or harness changes, but not silent Record edits.

### Never direct Record adaptation

- companion replies that imply new knowledge or personality
- external lookup results
- tool success or failure
- environment success or failure
- general reinforcement from use

These may inform workflow or policy, but they do not become companion knowledge or identity without explicit staging and approval.

### Mixed signals must be split

A single next-state signal may contain:

- a **workflow/policy** lesson
- a possible **Record** lesson

Example: "That answer was wrong, and I really care about Roman history."

- "That answer was wrong" may improve policy or workflow.
- "I really care about Roman history" may be a curiosity signal, but only through the normal gate.

Do not collapse these into one undifferentiated learning channel.

---

## Green / yellow / red (rough guide)

| Zone | Examples | RL / export |
|------|----------|-------------|
| **Green** | Operator-approved anonymized tool traces; synthetic tasks; public system prompts you authored | OK for local experiments if policy allows |
| **Yellow** | `export_conversation_trajectories.py` output from **session-transcript** — use **last-n** slices, review before upload | Review + redact; prefer local self-hosted stack only |
| **Red** | Full child transcripts, medical/education identifiers, gate drafts with rejection reasons tied to real events, any content you would not email to a stranger | Do not pool; do not upload to public datasets |

---

## Script contract

- **`scripts/export_conversation_trajectories.py`** — **Read-only**; emits JSONL for **your** disks. It does **not** call training APIs. Operator decides destination and retention.
- Default output includes **turn, role, channel, text, ts** and optional **pipeline_events** near each turn (best-effort time window). Not a full OpenClaw-RL schema — adapt downstream if needed.

---

## Alignment with AGENTS

- **Gated pipeline** unchanged.
- **OpenClaw** may stage; may not merge.
- **RL** (if used) is **harness-level** unless you explicitly run a separate, guardian-approved process — never a back door into SELF.

---

## References

- [OpenClaw integration](openclaw-integration.md) — export + trajectory section
- [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) — upstream README (PII reminder, self-hosted stack)
- [AGENTS.md](../AGENTS.md) — knowledge boundary, permission boundaries
