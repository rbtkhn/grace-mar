# Trust layers — reliability vs adversarial surfaces

**Purpose:** Complement the **knowledge boundary** ([knowledge-boundary-framework.md](knowledge-boundary-framework.md)) with a **tooling and environment** lens. The boundary defines what the Voice may treat as Record knowledge. This doc defines two **different** failure modes when operators or harnesses interact with **external** systems.

**Authority:** Subordinate to [AGENTS.md](../AGENTS.md) and the knowledge-boundary framework. This is **operational nuance**, not a second constitution.

---

## Two layers

| Layer | Question it answers | Examples |
|-------|---------------------|----------|
| **Reliability** | Did the integration **work this time**? Timeouts, flaky networks, service workers, MCP hiccups, rate limits, `page.evaluate` races. | Retry, fallback, “tell the user writes failed,” degraded read-only paths. |
| **Trust / adversarial** | Is the **surface honest**? Untrusted web pages, spoofed globals (`window` APIs), misleading DOM, hostile or confused peers on a federated bus. | “Presence of a function” is **not** authentication. Combine **origin policy**, **verified extension/profile**, and **threat model** for the workflow—not vibes. |

Confusing the two produces **false confidence**: a reliable call to a **fake** API is still wrong; an unreliable call to a **real** API is a reliability problem, not proof of malice.

---

## Relation to Grace-Mar

- **Record vs LLM exterior** (AGENTS, knowledge boundary) governs **what becomes knowledge** in the fork.
- **Reliability vs adversarial** governs **how operators and tools interpret signals** from browsers, MCP servers, external repos, and chat surfaces **before** those signals become staging input.

OB1 / mixed-trust bridges: see [integrations/ob1/architecture.md](integrations/ob1/architecture.md) and [work-cici LEAKAGE-CHECKLIST](skill-work/work-cici/LEAKAGE-CHECKLIST.md) — runtime and tooling are **not** the canonical Record.

---

## See also

- [knowledge-boundary-framework.md](knowledge-boundary-framework.md) — interior / exterior / lookup path  
- [architecture.md](architecture.md) — Voice = model + harness; state governance  
- [AGENTS.md](../AGENTS.md) — sovereign merge, calibrated abstention
