# Lessons: Perplexity Computer video (David Andre)

**Source:** YouTube — "Learn 80% of Perplexity Computer in 34 Minutes." Hosted AI agent: orchestrator, 19 models, skills, sub-agents, VM/proxy architecture, connectors, scheduling. **Use:** Architecture, UX, and positioning lessons for the assistant brain.

**Related:** [state-evolved-assistant-brain-heads-of-state.md](state-evolved-assistant-brain-heads-of-state.md), [actionable-features-and-insights.md](actionable-features-and-insights.md), [competitor-research-assistant-brain-judgment-testing.md](competitor-research-assistant-brain-judgment-testing.md).

---

## 1. Video theses (condensed)

- **Perplexity Computer:** Cloud-hosted AI agent; orchestrator routes to 19 models by task type (orchestration → Opus, research → Sonet, code → GPT, etc.). "Best model for the job" — not locked to one provider.
- **Blocking:** Most agents use data-center IPs and get blocked by sites. Perplexity uses VMs + proxies so cloud agent can browse/click like a human; Agent Zero runs locally → residential IP → not blocked.
- **Skills:** Agent loads **skills** (e.g. skill.md, PDF skill, research skill) when needed — detailed system prompt only when topic is relevant. Context engineering; user can add custom skills. Cream (payments) has official skill.md for any agent (Cursor, Codex, Agent Zero, OpenClaw).
- **Sub-agents:** Orchestrator spawns sub-agents; each has own context, shared workspace. Parallel execution (e.g. 10 at once); results aggregated (e.g. CSV) then synthesized.
- **Model Council:** Prompt to multiple top models; synthesizer resolves conflicts, gives one answer + where models agree/differ.
- **Memory:** Vector DB, memory persists across sessions, "clever at remembering key facts."
- **Scheduling:** Cron-style runs; each run gets fresh isolated VM, zero memory of past runs (reduces compounding hallucinations); can push notifications.
- **Integrations:** 400+ OAuth connectors (Slack, Gmail, calendar, Notion, GitHub, etc.); authenticate once.
- **Limitations (David's take):** Expensive ($200/mo, credits burn fast); multi-session file system confusion; GitHub auth issues; "still early." Prefers Agent Zero/OpenClaw for general, Claude Code for coding.
- **Interactive output:** Agent builds interactive web apps (e.g. oil/Strait of Hormuz viz) so user gets visual, not just text — "way easier to understand."

---

## 2. What we can learn (mapped to assistant brain)

### Model Council vs us

- **Them:** Multiple models → synthesizer → one answer + "where they agree/differ."
- **Us:** We **don't** synthesize. We preserve tensions; show A/B/C; no single answer. Model Council is a **competitor pattern** (converge + show disagreement). We differentiate: polyphonic cognition, no resolution. Reinforces "we never give you one answer."

### Skills as loadable instructions

- **Them:** Skills loaded when agent needs them (PDF, research, web building); reduces context bloat; third parties (e.g. Cream) publish skill.md for agents.
- **Us:** Our fixed A/B/C/D are like built-in "perspective skills." We could publish a **polyphonic-cognition-protocol skill** (skill.md or similar): one loadable instruction set so any agent or implementer can run the method — fixed perspectives, instinct-as-input optional, contradiction badge, no write unless relay. Spreads the method without building the full product.
- **Actionable:** Draft a **polyphonic-cognition-protocol.skill.md** (or skill block) for agent-skills ecosystems (OpenClaw, Cursor, etc.) and for human-run protocol.

### Sub-agents / parallel perspectives

- **Them:** Orchestrator spawns sub-agents in parallel; each has own context; shared workspace; aggregate results.
- **Us:** We could implement A, B, C (and D) as **parallel perspective sub-agents** — each produces its slot; orchestrator aggregates **without synthesis** (no "synthesizer"); output = A + B + C + tension labels. Same architecture idea, different rule: combine, don't resolve.
- **Actionable:** If we build a real implementation, consider "one orchestrator, N perspective agents in parallel, combine into one response with tension badges."

### Memory / persistence

- **Them:** Memory persists across sessions; vector DB; "clever at remembering."
- **Us:** We have **no write unless relay** — we don't remember unless the principal says "record." Deliberately opposite. Reinforces sovereign session and differentiation: "Your session. No silent logging. No retention unless you say so."

### Integrations

- **Them:** 400+ connectors; authenticate once; use in flow.
- **Us:** We're narrow: input = decision/question + optional context (meeting, briefing, calendar). Relevant integrations = **calendar**, **briefing/doc source**, maybe secure messaging. Not 400; a small set. List desired integrations in product spec (e.g. "Calendar connector: optional; Briefing source: optional").
- **Actionable:** Add to spec or roadmap: "Integrations (optional): calendar, briefing/doc source; authenticate once; no autonomous scraping."

### Interactive / visual output

- **Them:** Agent produces interactive web apps so user gets visual, not just text — "way easier to understand."
- **Us:** Our output is structured text (A/B/C + tensions). We could add **optional visual export**: e.g. one-page PDF, or simple diagram (three boxes A/B/C with tension arrows). Helps principals who prefer visual.
- **Actionable:** Feature: "Export run as one-pager PDF" or "Show as simple A/B/C diagram."

### Bounded scope avoids their bugs

- **Them:** Multi-session file system confusion; cross-chat can't find files; GitHub auth failures.
- **Us:** We're **one session, one decision, one output**. No cross-session workspace. Bounded scope reduces that class of failure. Reinforces "one principal, one decision."

### On-prem / local vs cloud

- **Them:** Running locally (Agent Zero) = residential IP = not blocked; Perplexity = cloud + VM/proxies.
- **Us:** For federal, **on-prem or air-gapped** is already a differentiator — data doesn't leave boundary; no blocking issue for us since we're not browsing the open web as the primary use. Keep "on-prem option" in capability statement.

### Pricing

- **Them:** Credit-based, $200/mo, 10k credits felt insufficient; "not economically viable" for heavy use.
- **Us:** We're not a general agent; we're a narrow product. **Fixed-fee pilot** or seat-based avoids credit anxiety. Already in our contract path.

---

## 3. Actionable takeaways

| Lesson | Action |
|--------|--------|
| Skills as loadable instructions | Draft **polyphonic-cognition-protocol.skill.md** (or skill block) for agent-skills ecosystems and for human-run protocol. |
| Parallel perspective agents | If building implementation: one orchestrator, A/B/C (and D) as parallel sub-agents; aggregate without synthesis; add tension labels. |
| No memory by design | Keep "no write unless relay" and "sovereign session" in copy; contrast with agents that "remember by default." |
| Integrations | Add to spec: optional integrations = calendar, briefing/doc source; list in roadmap or capability statement. |
| Visual export | Feature: optional "export run as one-pager PDF" or "A/B/C diagram" for principals who prefer visual. |
| Model routing | We lead with **structure over models**; we don't advertise which LLM. Perplexity advertises "best model per task" — we advertise "fixed perspectives, you decide." No change. |

---

*Source: YouTube, Perplexity Computer overview. Lessons extracted for assistant brain product and implementation.*
