# Safety story — visible state, not chat-only reassurance

**Purpose:** Position **audit continuity** as a **first-class UX metaphor** — the thing that calms the “silent failure” fear — not as back-office trivia.

---

## The fear (user class)

Many operators carry a **production database** mental model: *something important changed and nobody saw it until it was too late.* In agent systems, the scarier variant is: *the model **acted** as if truth updated, but canonical identity did not.*

**Design implication:** Reassurance must live in **visible, inspectable state** — not “trust the chat” or “the agent should remember.”

---

## What “safe” looks like (inspectable dimensions)

| Dimension | Question it answers | Where it lives (repo) |
|-----------|---------------------|------------------------|
| **Pending vs approved** | Is this suggestion waiting on a human, or already committed? | `users/[id]/recursion-gate.md` — candidate blocks (`status: pending` → approved/rejected) |
| **Staged vs merged** | Did OpenClaw (or the analyst) only **stage**, or did a merge **write** SELF/EVIDENCE? | Staging ≠ merge: handback ends in RECURSION-GATE; merge is `process_approved_candidates.py` (see AGENTS.md). **Chat is not proof.** |
| **Receipts** | What batch just landed, and with what checksums? | `users/[id]/merge-receipts.jsonl` (append-only audit) |
| **Pipeline events** | When did **staged** vs **applied** happen, and can they be linked? | `users/[id]/pipeline-events.jsonl` — e.g. `parent_event_id` linking rows |
| **Last merge footprint** | What ACT- or session line proves the last integration moment? | `self-evidence.md` (ACT-*), `session-log.md` pipeline merge section |
| **Harness / replay** | Can we re-run or explain a merge from events? | `harness-events.jsonl`, tools like `replay_harness_event.py` (where documented) |

**Partner-facing line:** *We separate “suggested” from “committed” — and we keep receipts so you’re not guessing from chat.*

---

## OpenClaw-specific clarity

| State | Meaning |
|-------|---------|
| **Exported identity** | OpenClaw reads **USER.md / bundle** — reflects **last approved** Record snapshot, not live chat. |
| **Staging from OpenClaw** | `openclaw_stage` / “we did X” paths → **candidates in RECURSION-GATE** only. |
| **Merged Record** | Only after companion approval + `process_approved_candidates.py` — **then** SELF, EVIDENCE, prompt, SESSION-LOG, SELF-ARCHIVE update together. |

If UX conflates “the agent said it” with “it’s in the fork,” you recreate silent failure. **Explicit labels** in docs and UI copy should preserve **staged vs merged**.

---

## Strategy: audit continuity as primary story

**Not admin trivia:** Receipts, gate queues, and event logs are how a serious system **shows its working** — same tier as “the Voice stays inside the knowledge boundary” (see [quality-gates-narrative.md](quality-gates-narrative.md)).

**Not optional lore for power users:** New operators should meet **pending vs approved** and **where last merge is visible** as early as **how to chat**.

**Product direction:** Any “operator dashboard” or miniapp surface should foreground **state** (queue depth, last merge, receipt pointer) before secondary metrics — aligned with the [quality-gates-narrative.md](quality-gates-narrative.md) dashboard sketch.

---

## Relation to other contracts

- **[session-continuity-contract.md](session-continuity-contract.md)** — Continuity = files + scripts + CI; **this doc** adds **safety = visible pipeline state**.
- **[openclaw-integration.md](../../openclaw-integration.md)** — Staging permissions and handback path.
- **[provenance-checklist.md](provenance-checklist.md)** — Repeatable verification for export and handback.
- **Architecture — audit lane** — `docs/architecture.md` (append-only audit files).

---

## Guardrail

Receipts and events **prove process**, not **correctness** of content. The companion gate remains the authority for **what** enters the Record; the safety story is that **nothing enters without a visible path**.
