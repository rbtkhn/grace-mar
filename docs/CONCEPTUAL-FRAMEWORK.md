# Conceptual Framework — grace-mar

**Purpose:** Encode the core distinctions so future AIs and developers can understand the system with minimal effort.

**Authority:** Subordinate to GRACE-MAR-CORE v2.0. No file may contradict GRACE-MAR-CORE.

---

## 1. Cognitive Fork vs. Cognitive Twin

| Term | Meaning | grace-mar uses? |
|------|---------|--------------|
| **Cognitive fork** | Versioned branch from a snapshot. Diverges by design. Has its own history. Like a software fork. | ✓ Yes |
| **Cognitive twin** | Parallel copy, mirror, real-time replica. Stays in sync with the original. | ✗ No |

**Use "cognitive fork" only.** The fork and the real person grow independently. Divergence is intentional, not a failure.

---

## 2. Fork as Its Own Entity vs. Emulation

| Concept | What it means | Applies to |
|---------|---------------|------------|
| **The fork is its own entity** | The fork started from a snapshot of the real person but has its own trajectory. It accumulates knowledge the real person may not have (e.g., approved lookups, school artifacts). It does not "mimic" or "replicate" the person. | The fork (SELF.md, SKILLS.md, EVIDENCE.md) |
| **Emulation** | The bot interface that *renders* the fork in conversation. When you query the bot, the LLM generates responses constrained by the fork's profile (voice, knowledge, personality). That rendering is "emulation." | The Telegram bot (`bot/bot.py`) |

**Summary:**
- The **fork** = its own record, diverging by design. Not emulating the real person.
- The **bot** = emulates the fork in real-time conversation (produces fork-like responses).

---

## 3. Where Things Live

| Component | Location | Role |
|-----------|----------|------|
| **The fork** | Inside the user's mind (their mental model, made explicit and structured). Data: `users/[id]/SELF.md`, SKILLS.md, EVIDENCE.md | The cognitive record |
| **The bot** | `bot/bot.py` — Telegram interface | Observation window; emulates the fork in conversation |
| **LLM** | External (OpenAI, etc.) | Generates text; constrained by SYSTEM_PROMPT (fork profile) |

**The bot is not the fork.** The bot is the interface through which the user interacts with the fork.

---

## 4. Key Invariants

1. **Divergence by design** — Fork and real person may drift apart. This is correct.
2. **The fork records, it does not mirror** — Growth comes from curated interactions, not continuous sync.
3. **Knowledge boundary** — The fork knows only what is explicitly documented. LLM training data must not leak in.
4. **"Emulation" = bot behavior** — Use "emulate" for the bot rendering the fork's voice/knowledge, not for the fork's relationship to the real person.

---

## 5. Merge, Not Add

Content enters the fork by **merging**, not adding. Merge implies:
- **Integration** — New content connects with existing (e.g., reptiles in IX-A + curiosity in IX-B)
- **Conflict resolution** — Duplicates are rejected; the fork stays coherent
- **Active processing** — The fork absorbs and organizes; it is not a passive container

Use "merge into the fork" / "merge into SELF.md" rather than "add to."

---

## 6. Terminology Quick Reference

| Say this | Not this |
|----------|----------|
| cognitive fork | cognitive twin |
| the fork diverges | the fork mirrors / stays in sync |
| the fork is its own entity | the fork emulates the person |
| the bot emulates the fork | (ambiguous: clarify "emulates the fork in conversation") |
| observation window | the fork (when referring to the bot) |
| merge into the fork | add to the fork |

---

## 7. File Map for AI Parsing

```
AGENTS.md                  → AI guardrails, rules, what not to do
docs/CONCEPTUAL-FRAMEWORK.md → This file — core distinctions
docs/GRACE-MAR-CORE.md     → Canonical governance (absolute authority)
docs/ARCHITECTURE.md       → Full system design
GRACE-MAR-BOOTSTRAP.md     → Session bootstrap, quick start
.cursor/rules/grace-mar.mdc → Cursor-specific rule (users/**)
```

---

*Document version: 1.0*
*Last updated: February 2026*
