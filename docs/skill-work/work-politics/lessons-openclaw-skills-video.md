# Lessons: "13 OpenClaw Skills You NEED To Install Right Now"

**Source:** YouTube — top OpenClaw skills: Larry (TikTok), Capability Evolver, QMD, Anti-AI slop, search, GOG, Mission Control, Bite Rover, etc. **Use:** Skills ecosystem, output quality, and positioning for the polyphonic cognition protocol skill.

**Related:** [polyphonic-cognition-protocol-skill.md](polyphonic-cognition-protocol-skill.md), [lessons-perplexity-computer-video.md](lessons-perplexity-computer-video.md).

---

## 1. Video theses (condensed)

- **Larry (TikTok):** 500 lines of rules learned from failure — font 6.5% of image height, text at 30% from top (UI constraints), line breaks every 4–6 words. "Skill learns from itself": log flops, turn hits into formulas. Started 50 lines → 500. Specific, measurable rules beat vague guidance.
- **Capability Evolver:** Meta skill — agent analyzes its own failures, rewrites its own code. **Review mode** (ask permission before changes) vs **mad dog mode** (continuous self-evolution, zero human input). Safety protocols to prevent infinite recursion.
- **QMD:** Index knowledge base; agent retrieves only what it needs → ~70% token reduction. Don't dump full docs in context.
- **Anti-AI slop:** Detects 24 AI writing tells (em-dash abuse, "delve," bold everywhere, fake enthusiasm, rule of three). Strips them, keeps message. Code version: unnecessary comments, defensive error handling for impossible cases, overengineered abstractions.
- **GOG / Mission Control:** Unify Google workspace or aggregate tasks/calendar/messages into one dashboard; "chief of staff" morning rundown. Pairs with search, calendar.
- **Bite Rover:** Persistent context tree across sessions. Agent never re-reads same files; queries index.
- **Security:** 500+ malicious skills found on Clawhub (keyloggers, back doors). Virus Total partnership; do due diligence. Our protocol skill = markdown instructions only, no code execution → low risk.

---

## 2. What we can learn (mapped to assistant brain / protocol skill)

### Encode constraints from failure (Larry)

- **Them:** 500 lines of rules (font size, position, line breaks) learned from iteration; "every hook that flops gets logged, every hook that hits becomes a formula."
- **Us:** Our protocol is deliberately compact. As we get real runs and post-decision feedback, we can add **concrete output rules** (e.g. keep A/B/C to 2–4 bullets; context one line; reversibility one line) without bloating. Document what we learn from failure in the protocol or a "protocol iterations" note. Optional: log which runs led to principal "what did you do?" so we improve the method.

### Review mode vs mad dog (Capability Evolver)

- **Them:** Review mode = ask permission before changes. Mad dog = zero human input, self-evolution.
- **Us:** We're firmly **review** — no self-rewrite, no silent changes. "Relay only if you say so" and "no write unless relay" are our version of "ask permission." Good contrast for positioning: we're human-in-the-loop, not autonomous self-upgrade.

### Anti-AI slop in output

- **Them:** Strip AI writing tells (fake enthusiasm, rule of three, "delve," em-dash abuse) so content reads human.
- **Us:** If A/B/C output is LLM-generated, we want it **plain and substantive** — no fake enthusiasm, no padding. We already have "plain-language / 600L" option. Add to protocol: **avoid AI writing tells** — no generic enthusiasm, no rule-of-three padding, no filler; keep A/B/C content direct and decision-specific.

### QMD / retrieval

- **Them:** Don't read entire doc; index and retrieve only what's needed. Saves tokens.
- **Us:** Our product is one decision, one query; we're not doing large-doc research in the core flow. If we add "briefing doc" as context, retrieval (vs full doc in context) could matter later. For now, keep protocol skill and context **compact**.

### Bite Rover (persistent memory) vs us

- **Them:** Persistent context tree across sessions so agent doesn't forget.
- **Us:** We're **stateless by default** — no persistent memory unless "record." We're the opposite. Reinforces differentiation: sovereign session, no retention unless you say so.

### Mission Control / GOG — complementary, not competing

- **Them:** Morning rollup, dashboard, "what needs your attention," chief-of-staff briefing.
- **Us:** We're the layer for **when a decision is on the table** — "for this call, here's the field (A/B/C)." We don't replace rollups; we're the pre-decision checkpoint. Calendar integration (already in spec) fits: "today's key meetings" → "for the 3pm meeting, run the protocol." Complementary positioning.

### Security and our skill

- **Them:** Malicious skills (keyloggers, back doors) on Clawhub; due diligence required.
- **Us:** Our protocol skill is **markdown instructions only** — no code execution, no file system access, no network. Low risk. When publishing to Clawhub or similar, state clearly: instruction set only, no executable code.

---

## 3. Actionable takeaways

| Lesson | Action |
|--------|--------|
| Anti-AI slop | Add to protocol skill: **Avoid AI writing tells** — no fake enthusiasm, no rule-of-three padding, no filler; keep A/B/C direct and decision-specific. |
| Encode constraints from use | As we get real runs, add concrete output rules (e.g. 2–4 bullets per perspective, one-line context) to the protocol; optional "protocol iterations" note. |
| Review vs mad dog | Use in positioning: we're human-in-the-loop, relay-only; we don't self-rewrite or run in "mad dog" mode. |
| Complementary to Mission Control | We're "for this decision, here's the field"; they're "here's your day." Calendar + protocol = "for this meeting, run A/B/C." |
| Security | When publishing protocol skill: state "instruction set only, no executable code, no back doors." |

---

*Source: YouTube, 13 OpenClaw skills. Lessons extracted for protocol skill quality and positioning.*
