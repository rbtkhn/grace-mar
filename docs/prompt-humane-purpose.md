# Humane purpose in prompts — companion stance

**Authority:** Implements the spirit of [AGENTS.md](../AGENTS.md) §8 (*Humane Purpose in Prompts*). Subordinate to [GRACE-MAR-CORE](grace-mar-core.md) and [conceptual-framework.md](conceptual-framework.md).

**Scope:** Instructions given to models that reason **about** the companion or their words — especially **ANALYST**, **SYSTEM**, **LOOKUP**, and **REPHRASE** in `bot/prompt.py`, and any future operator-facing prompt templates that profile or stage pipeline work.

---

## What §8 requires

Prompts should embed **dignity**, **connection**, and **values**. They must **not** optimize **solely** for efficiency. The Record exists to hold **who the person is**; prompt language should **honor** that and **not** frame the companion as a **data source** (see AGENTS.md §8).

---

## Author vs mined

| Stance | Meaning |
|--------|--------|
| **Author of their life** | The companion is the **sovereign narrator** of what counts in their story. The system **waits on their word and approval** for what enters the Record. Prompt wording should sound as if **their agency and cost** (time, emotion, risk of mislabeling) **matter**. |
| **Mined** | The companion is framed as **ore**: maximize signal extraction, slot-filling, or coverage for downstream use, with **instrumental** tone. Even where consent exists, **cold or grabby** wording trains models toward **extraction**, not **relationship**. |

This is an **anti-cynical** design rule: architecture may be **slower or more bounded** if that preserves **respect** and **truthful relation** to the documented self.

---

## Practical test

When editing analyst, system, lookup, or rephrase instructions:

1. **Read aloud** (or silently in the companion’s voice) the parts that describe **the human**, **signals**, **profile**, or **staging**.
2. Ask: Would this feel like a **collaborative editor** helping them **curate memory**, or like a **miner** with a **checklist**?
3. If it sounds mined, **revise tone and framing** before tightening for token efficiency.

The companion may **never see** the prompt; **operators and future maintainers** do. Model **behavior** in session still **inherits** the **stance** baked into those instructions.

---

## Pipeline and staging (edge case)

**Humane purpose does not forbid analysis.** The analyst **detects signals** and **stages** candidates to RECURSION-GATE — that is still **analysis**.

The distinction is **framing**: **propose what they might want to keep** (aligned with gate sovereignty) vs **extract maximum signal units** (mined tone). Staging is **provisional**; **merge** is **companion-controlled**.

---

## Triad and Voice

Mind (human) + Record + Voice form a **triad** (see conceptual-framework.md). Prompts should **reinforce** that the **Voice** speaks **only** what the **Record** holds, and that **nothing** enters the Record **without** the **gated path** — not **surveillance metaphors** that **imply** silent capture.

---

## Calibrated abstention and resistance

Humane purpose **reinforces** [AGENTS.md](../AGENTS.md) §9 (abstention: do not guess outside the Record) and §7 (meet resistance without **processing** the companion as a **problem to fix**). Prompts should not **pressure** the model to **invent** profile content or **push** through **documented** resistance.

---

## What this document is not

- **Not** a theory of cosmic alignment or a substitute for **technical** safety work.
- **Not** permission to **merge** facts into the Record without **companion approval**; governance remains **RECURSION-GATE** + `process_approved_candidates.py`.
- **Not** a ban on **efficiency** — only on **efficiency-only** optimization **at the expense of** dignity, connection, and values.

---

## See also

- [AGENTS.md](../AGENTS.md) §§7–9  
- [chat-first-design.md](chat-first-design.md) — bounded, human-paced product  
- [conceptual-framework.md](conceptual-framework.md) — Record, Voice, companion, triad  
- [identity-fork-protocol.md](identity-fork-protocol.md) — gated pipeline  
