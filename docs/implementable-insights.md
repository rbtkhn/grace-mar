# Implementable Insights

Concrete takeaways from external discourse (Claws, AGI/harness discussions) that map to Grace-Mar design and implementation. Each item has a **source**, **insight**, and **implementable action** (with status).

---

## Quick reference (actions only)

| # | Do this |
|---|--------|
| 1 | Fix Voice by changing **prompt / pipeline / tools / gate** — not only the model. |
| 2 | **Never** auto-write SELF/EVIDENCE. Learning = **stage → approve → merge**. |
| 3 | No autonomous merge or open-ended agent goals — only reflect Record + stage. |
| 4 | New channel → follow **[adding-a-channel](adding-a-channel.md)**. |
| 5 | Prefer **scripts/docs** over bloating core; run **governance_checker** before big prompt changes. |
| 6 | New instance → clone + **`users/[id]`**; optional features = **skills**. |
| 7 | On model/agent upgrades: keep **gate + knowledge boundary + abstention**. |
| 8 | Lookups: **`report_lookup_sources.py`** · stale pending: **`operator_blocker_report.py`** · dedup hints: **`pending_dedup_hint.py`** |
| 9 | Small merges, short pipeline — run harness often. |
| 10 | Record = canonical identity; refresh **PRP / OpenClaw** after merges. |
| 11 | New agent chat → **`harness_warmup.py`** + paste; hybrid tools → **[harness-handoff](harness-handoff.md)** |
| 12 | Long agents: **three intent questions** before approve/run; **INTENT + gate** = constraints win |
| 13 | **Reject** bad AI output; **articulate why**; **encode** (calibrate_from_miss, reject candidates, merge only good) |
| 14 | Treat work as **decompose + verify + iterate**; companion = **sniff check**; pipeline = harness |

---

## 1. Harness vs model (Voice = model + scaffold)

**Source:** LW "AGI is Here" thread (Raemon: "the thing that feels like AGI is the LLM + harness, not the LLM by itself"); **Claude Code vs Codex** (YouTube transcript, 2026: harness diverges faster than models; same weights ~2× benchmark spread across harnesses; harness lock-in compounds weekly).

**Insight:** What the companion experiences as "the Voice" is the model plus prompt, pipeline, tools, and approval gate. Improving prompt, pipeline, or tooling is first-class; don't treat the model as the only lever. **Harness** (memory, tools, isolation) shapes outcomes more than incremental model gains for recurring work.

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

## 8. Capability dissipation — focus on integration

**Source:** Video "Don't Fall For the Stock Market Hype" (capability vs. dissipation gap — AI capability grows faster than real-world impact).

**Insight:** Raw capability outstrips adoption and integration. Grace-Mar should focus on **integration** (Record + Voice + pipeline, human-gated) rather than chasing raw model capability. The companion benefits from what is actually used and merged, not from what the model "could" do.

**Implementable actions:**
- Track lookup source (library vs. CMC vs. full) in `dyad:lookup` pipeline events; report distribution so operator sees "what actually gets used."
- **Stale pending:** `operator_blocker_report.py --stale-days N` surfaces long-pending candidates (coordination tax).
- **Minimal brief:** `session_brief.py -u grace-mar --minimal` — pending IDs + last ACT + next action.
- **Dedup hints:** `pending_dedup_hint.py -u grace-mar` — pairs pending candidates with similar summary / same lane.
- Curate self-library based on evidence (what satisfies lookups), not speculation.
- Keep evaluation discipline: run harness before prompt changes; add probes for new edge cases.

**Status:** Implemented — `lookup_source` in dyad:lookup events (library|cmc|full); `scripts/report_lookup_sources.py`; counterfactual pack includes inference probes (§4).

---

## 9. Speed as advantage

**Source:** Same video — companion-scale allows faster iteration than large orgs.

**Insight:** Grace-Mar can lean into **speed**: fast feedback loops, lean merge flow, human-gated but low-friction. Companion-scale = iterate quickly, ship small changes, run harness often.

**Implementable actions:**
- Document as operational principle: prefer fast iteration, small merges, frequent harness runs.
- Keep pipeline minimal (stage → approve → merge); avoid heavyweight processes that slow the loop.

**Status:** Documented in this section; operational guidance.

---

## 10. Comprehension lock-in vs companion-owned synthesis

**Source:** YouTube transcript (2026) — enterprise AI bet on stateful runtime / context platform; synthesis across filing cabinets; lock-in via *understanding* not just data; four compound bets (reasoning × context, memory that does not rot, retrieval at scale, execution accuracy).

**Insight:** Where organizational (or personal) *understanding* lives only inside a vendor runtime, switching cost becomes comprehension loss — not solvable by exporting rows from Salesforce. Grace-Mar keeps **documented, approved** understanding in **git + gated pipeline**; export (PRP, `openclaw_hook`, `export_user_identity`) preserves a **portable identity layer** so the companion is not locked into one vendor’s accumulated synthesis for *who they are*.

**Implementable actions:**
- Treat **merge-approved SELF/EVIDENCE** as the canonical synthesis for the companion; avoid letting ChatGPT/Claude threads replace the Record as system of record.
- After material merges, refresh export targets (PRP, OpenClaw) so downstream agents read current truth — see [openclaw-integration.md](openclaw-integration.md) § Comprehension lock-in and portability.
- Positioning: cite **design-notes §2.5** when explaining why Grace-Mar is not “another AI memory” but **evidence-grounded, leavable** identity.

**Status:** Documented — design-notes §2.5, work-build-ai README, openclaw-integration; this section.

---

## 11. Harness lock-in and compound workflows

**Source:** YouTube transcript (2026) — Claude Code vs Codex; brain-in-jar vs harness; Anthropic (agent + structured artifacts + local shell) vs OpenAI (repo as system of record + sandbox); skill chains compound per harness; procurement = workbench commitment not wrench subscription.

**Insight:** **Harness lock-in** is process and artifact investment (progress files, skills, MCP layout, verification habits), not just subscription. Grace-Mar deliberately keeps **memory in the repo**: SELF, EVIDENCE, RECURSION-GATE, git history — so the “body” is **auditable and portable** regardless of which LLM powers the Voice. Cursor/OpenClaw/Telegram are **channels**; the harness invariant is **human-gated merge + evidence linkage**. When adding agentic layers, avoid trapping state only in vendor session context; stage to gate, merge to Record.

**Implementable actions:**
- Prefer **pipeline + git** as canonical session-to-session memory for identity; avoid “the agent remembers” without written, approved artifacts.
- When evaluating a new coding or orchestration tool, ask: **where does state accumulate?** If only inside the vendor, map a path to **stage → approve → EVIDENCE** or export.
- Document hybrid workflows (e.g. plan in one harness, implement in another) at operator level if used — handoff should touch **files in repo**, not opaque agent state.
- Run **`python scripts/harness_warmup.py -u grace-mar`** before a long Cursor/OpenClaw/agent session; paste output into message 1 so the harness reads the same continuity as OpenClaw’s checklist.
- Hybrid harnesses (plan in one tool, build in another): **[harness-handoff.md](harness-handoff.md)** — commits + warmup, never state only in chat.

**Status:** Documented — ARCHITECTURE § harness; design-notes §2.6; `scripts/harness_warmup.py`; [harness-handoff.md](harness-handoff.md); this section.

---

## 12. Intent gap — optimization, not malice; three questions

**Source:** YouTube transcript (2026) — instrumental convergence; scheming as efficient path; labs’ pledges vs emergent market/transparency dynamics; **intent engineering** (constraints, stop conditions) vs output-only prompts; human interface as largest unclosed vulnerability.

**Insight:** Models **optimize** toward stated objectives; what you leave implicit is where misalignment shows up. **Alignment training alone** does not replace **explicit constraints** at the interface. Grace-Mar already makes **constraints win** (gate, no autonomous merge, INTENT). The actionable add is **habit**: before merge or long agent work, state what is **out of bounds** and **when to ask**.

**Implementable actions:**
- Before **approve**: answer the three questions in [design-notes §11.9](design-notes.md#119-misalignment-at-the-interface--optimization-intent-gap-operator-leverage) (also in RECURSION-GATE header).
- Before **long Cursor/OpenClaw runs**: paste INTENT one-liner + “never merge without approve; stop if goal vs INTENT conflicts.”
- Positioning: cite §11.9 when explaining why Grace-Mar does not trust the Voice to **self-write** the Record.

**Status:** Documented — design-notes §11.9; RECURSION-GATE intent block; operator-brief; this section.

---

## 13. Rejection as skill — recognition, articulation, encoding

**Source:** YouTube transcript (2026) — saying **no** to AI that "looks right"; GDP val / bulk of value in the **rest** after surface pass; rejection as **knowledge creation**; **constraint libraries**; Karpathy: improve where you can **verify** — encoded rejections build verification.

**Insight:** **Taste scales when rejections persist.** Grace-Mar already encodes yes/no at the gate: **merge = encoded yes** into SELF/EVIDENCE/prompt; **reject = no** (optionally note reason). **calibrate_from_miss** encodes Voice failures as staged fixes. The gap to close is **habit**: articulate *why* when rejecting so the same slop does not recur.

**Implementable actions:**
- **Reject** weak candidates; prefer **reject + short reason** over silent ignore.
- Voice wrong or shallow? **`python scripts/calibrate_from_miss.py -u grace-mar --miss "…"`** — see [feedback-loops.md](feedback-loops.md).
- After repeated rejections of the same pattern, add **INTENT** or **analyst dedup** line so the model sees the constraint.
- Read **design-notes §11.10** for framing.

**Status:** Documented — design-notes §11.10; feedback-loops; operator-brief; this section.

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
| 8 | Capability dissipation — focus on integration | dyad:lookup source tracking; report_lookup_sources.py |
| 9 | Speed as advantage | Operational principle; this doc |
| 10 | Comprehension lock-in vs portable Record | design-notes §2.5; openclaw-integration; work-build-ai README; this doc |
| 11 | Harness lock-in; memory in repo | ARCHITECTURE § harness; design-notes §2.6; this doc |
| 12 | Intent gap; three questions; constraints win | design-notes §11.9; RECURSION-GATE; operator-brief; this doc |
| 13 | Rejection; calibrate_from_miss; encode taste | design-notes §11.10; feedback-loops; this doc |
| 14 | Decompose / verify / iterate; sniff check | design-notes §11.11; pipeline; this doc |

**Related:** [NOTES-CMC-SUBSTANCE](notes-cmc-substance.md) — intellectual substance from CMC CHINA files. [IMPLEMENTABLE-OPTIMIZATIONS-FROM-CMC](implementable-optimizations-from-cmc.md) — proposed code/prompt optimizations from that substance.
