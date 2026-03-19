# Claude Code / WAT ↔ work-dev crosswalk

**Purpose:** Map common **agentic IDE** practice (workflows + agent + tools, plan-then-build, deploy vs in-session) to **work-dev** delivery, reliability, and Grace-Mar boundaries—so operators and clients share vocabulary.

**Audience:** Operators scoping OpenClaw-adjacent builds, client SOWs, and internal alignment. Not a Claude Code tutorial.

---

## WAT in one table

| Layer | Typical form | Role |
|-------|--------------|------|
| **Workflows** | Markdown SOPs: goal, inputs, which tools, outputs, edge cases | Repeatable process spec |
| **Agent** | Model + session: plans, asks, routes to workflows/tools | Judgment and recovery **while building or when supervised** |
| **Tools** | Scripts, APIs, MCP-backed actions; secrets in `.env` | **Deterministic** steps the agent invokes |

**work-dev read:** Same separation as **reasoning vs execution** in [agent-reliability-playbook.md](agent-reliability-playbook.md). Tools and deployed paths should be auditable; agent “thinking” is not the audit trail.

---

## In-session agent vs deployed automation

| Mode | What runs | Self-heal / adapt | Reliability expectation |
|------|-----------|-------------------|-------------------------|
| **You + agent in IDE** | Full agent | High—research, patch tools, iterate | Good for **discovery** and **hardening** |
| **Cron / webhook / hosted job** | **Code** (workflows as orchestration + tool scripts) | Low—fails like traditional automation unless you built retries and tests | Must be **battle-tested**; tail cases need explicit handling |

**work-dev read:** Phase 1–3 can be agent-heavy; Phase 4 must assume **production = mostly deterministic**. Aligns with **inverted-U** and **progressive autonomy** in the reliability playbook.

---

## Planning, “done,” and scope

| Practice | work-dev mapping |
|----------|----------------------|
| **Plan before full autonomy** | Phase 2 architecture + acceptance criteria before large builds |
| **Clarifying questions until aligned** | Diagnostic memo + explicit **definition of done** (rows, fields, stop condition) |
| **Vague goals → bad output** | [delivery-playbook.md](delivery-playbook.md) Phase 1: name **tail** and **high-stakes** workflows, not only happy path |

---

## Context, skills, MCP

| Idea | work-dev mapping |
|------|----------------------|
| **Lean router doc** (pointers, not megaprompt) | Handback payloads: facts vs opinion; thin gate, fat references |
| **Context rot / compact** | Long OpenClaw threads: summarize into SESSION-LOG-shaped handoffs; avoid merging noise into Record |
| **MCP token cost** | Prefer **narrow API surface** + cheat sheet when one integration dominates |

---

## Security and handover (client builds)

| Idea | work-dev / Grace-Mar mapping |
|------|-----------------------------------|
| **Client-owned API keys and billing** | Clear **who pays runtime**; avoids operator as opaque middleman |
| **Secrets in `.env`, not chat** | Same spirit as **no secrets in repo**; operator vaults for production |
| **Webhooks hardened** | Auth, signing, rate limits—parallel to **staging** surfaces that must not be spammed |
| **Their repo / their host** | **Provenance** and exit: they can run without you as sole keyholder |

**Grace-Mar note:** Companion **gate** and **stage-only** OpenClaw mirror “human review before irreversible action”—not the same as webhook auth, same **membrane** idea.

---

## QA and evals

| Practice | work-dev mapping |
|----------|----------------------|
| Screenshot / browser loops for UI | Phase 4 **sample passed runs** + visual checks where UI matters |
| **Black-box** many inputs → log I/O | Factorial + **variation-types.md**; deterministic diff on outputs |
| Skill **evals** / regression | **Eval flywheel** in agent-reliability-playbook |

---

## Commercial vocabulary (outcomes, not stack)

| Course frame | work-dev doc |
|--------------|-------------------|
| Diagnose constraint → prescribe | [engagement-model.md](engagement-model.md), [offers.md](offers.md) |
| Value / outcome pricing | [engagement-model.md](engagement-model.md), economic-benchmarks |
| Partner / borrowed authority | [partner-channel.md](partner-channel.md) |

---

## Related docs

| Doc | Why |
|-----|-----|
| [agent-reliability-playbook.md](agent-reliability-playbook.md) | Tails, reasoning vs action, anchoring, four layers |
| [delivery-playbook.md](delivery-playbook.md) | Phases 1–5 |
| [variation-types.md](variation-types.md) | Factorial stressors |
| [openclaw-integration.md](../../openclaw-integration.md) | Handback shape, stage-only, gate |
| [provenance-checklist.md](provenance-checklist.md) | Audit path |

---

*Document version: 1.0 — crosswalk for work-dev; course concepts are illustrative, not vendor-specific requirements.*
