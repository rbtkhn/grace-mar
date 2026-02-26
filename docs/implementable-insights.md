# Implementable Insights

Concrete takeaways from external discourse (Claws, AGI/harness discussions) that map to Grace-Mar design and implementation. Each item has a **source**, **insight**, and **implementable action** (with status).

---

## 1. Harness vs model (Voice = model + scaffold)

**Source:** LW "AGI is Here" thread (Raemon: "the thing that feels like AGI is the LLM + harness, not the LLM by itself").

**Insight:** What the companion experiences as "the Voice" is the model plus prompt, pipeline, tools, and approval gate. Improving prompt, pipeline, or tooling is first-class; don't treat the model as the only lever.

**Implementable actions:**
- Document explicitly that **Voice = model + prompt + pipeline + tools**. See [ARCHITECTURE § System boundaries and harness](architecture.md#system-boundaries-and-harness) (and same doc for non-goals below).
- When debugging behavior, ask: is this a model limit, a prompt gap, a pipeline miss, or a tool/context issue?

**Status:** Documented in ARCHITECTURE.

---

## 2. Continual learning = architecture, not model self-edit

**Source:** LW thread (RogerDearnaley: continual learning for LLMs is architectural/framework, not scaling).

**Insight:** Grace-Mar implements "learning" as human-gated writes to SELF/EVIDENCE; the model does not edit its own memory or weights.

**Implementable actions:**
- State this in protocol and architecture. See [IDENTITY-FORK-PROTOCOL § 2.1](identity-fork-protocol.md) and agents.md.
- Reject any design that lets the model write directly to SELF or EVIDENCE without staging and approval.

**Status:** Documented in IDENTITY-FORK-PROTOCOL and AGENTS.

---

## 3. Explicit system boundaries (no autonomous goals)

**Source:** LW thread (paperclip maximizers, "what the system can't do"; Byrnes: autonomous company-running as AGI bar).

**Insight:** Grace-Mar has no autonomous long-horizon goal. The only "goals" are: (1) reflect the Record when queried, (2) stage candidates for companion approval. That prevents the system from being turned into an autonomous optimizer.

**Implementable actions:**
- Document **system boundaries / non-goals** in ARCHITECTURE: no autonomous merge, no learning from the open web, no self-set instrumental goals, no unbounded agentic loops.
- When adding agentic or Claw-style layers, keep merge authority human-only; orchestration may suggest, but only the companion approves Record changes.

**Status:** Documented in ARCHITECTURE § System boundaries and harness.

---

## 4. Config via skills that modify code (not config soup)

**Source:** Karpathy on NanoClaw — e.g. `/add-telegram` instructs the agent to modify code to integrate Telegram; "config via skills" avoids if-then-else config monsters.

**Insight:** Adding a capability (e.g. a new channel) should be a **skill**: a doc + template or small code pattern that an agent or human can apply, rather than another branch in a giant config.

**Implementable actions:**
- **Adding a channel:** Follow the pattern in [ADDING-A-CHANNEL](adding-a-channel.md): replicate Telegram/WeChat structure (entrypoint, core call, env), add one place in config/router. No "if channel X then …" sprawl.
- New integrations: prefer "skill doc + code template" over expanding a single config schema.

**Status:** adding-a-channel.md created; pattern applied to existing Telegram/WeChat.

---

## 5. Small, auditable surface

**Source:** Karpathy — NanoClaw ~4K lines, "fits in head and in AI context"; OpenClaw 400K lines and security concerns.

**Insight:** Keep core bot and pipeline small and readable so they remain auditable and forkable.

**Implementable actions:**
- Prefer adding a **documented skill or script** over expanding `bot/` or pipeline logic without bounds.
- When refactoring, preserve or reduce line count in `bot/core.py`, `bot/prompt.py`, and pipeline scripts; extract only when it improves clarity.
- Run `scripts/check_harness_invariants.py` before major model or harness changes (runs governance_checker + optional line-count warn). CI runs `scripts/governance_checker.py` on every push/PR (`.github/workflows/governance.yml`).

**Status:** Implemented — check_harness_invariants.py, governance.yml; line limits in script are advisory (warn only).

---

## 6. Maximally forkable + skills that fork

**Source:** Karpathy — "maximally forkable repo + skills that fork it into any desired configuration."

**Insight:** Clone → add user dir → run pipeline = base fork. Optional "skills" (docs + scripts) add capabilities (channels, exports, probes) without baking them into core.

**Implementable actions:**
- Document fork path in README or [PORTABILITY](portability.md): clone, create `users/[id]`, run pipeline; optional skills = listed in docs.
- New features that are optional (e.g. a new export, a new channel) should be addable via a skill doc + minimal code, not mandatory core.

**Status:** PORTABILITY and repo layout support this; ADDING-A-CHANNEL is one skill template.

---

## 7. What to do with "AGI" claims (operational, not philosophical)

**Source:** LW thread — disagreement on whether "AGI is here" helps or harms; need for actionable response.

**Insight:** Grace-Mar doesn't need to take a stance on AGI. It does need to stay **sovereign and evidence-linked** regardless of model capability: companion-owned Record, human-only merge, clear knowledge boundary.

**Implementable actions:**
- When upgrading models or adding agentic layers: (1) keep Sovereign Merge Rule and staging; (2) keep knowledge boundary and abstention; (3) document any new "goal" the system can pursue and ensure it is bounded (e.g. "suggest next question" not "maximize engagement").

**Status:** Invariants already in agents.md and GRACE-MAR-CORE; re-assert on any major capability upgrade.

---

## Summary table

| # | Insight | Where implemented / documented |
|---|--------|--------------------------------|
| 1 | Voice = model + harness | ARCHITECTURE § System boundaries and harness |
| 2 | Continual learning = human-gated writes | IDENTITY-FORK-PROTOCOL, agents.md |
| 3 | Explicit non-goals / no autonomous optimizer | ARCHITECTURE § System boundaries and harness |
| 4 | Config via skills (add channel = skill) | adding-a-channel.md |
| 5 | Small auditable surface | Design principle; DEVELOPMENT-HANDOFF |
| 6 | Forkable + optional skills | PORTABILITY, ADDING-A-CHANNEL |
| 7 | Sovereign Record regardless of model | agents.md, GRACE-MAR-CORE; re-assert on upgrades |

**Related:** [NOTES-CMC-SUBSTANCE](notes-cmc-substance.md) — intellectual substance from CMC CHINA files. [IMPLEMENTABLE-OPTIMIZATIONS-FROM-CMC](implementable-optimizations-from-cmc.md) — proposed code/prompt optimizations from that substance.
