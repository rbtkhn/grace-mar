# work-politics workspace

Canonical operator entrypoint for the territory.

Use this file when you want one place to understand:

- current campaign state
- what is stale
- what is queued for X / content
- what sources feed the weekly brief
- how outreach is being framed and tracked
- what should stage to `RECURSION-GATE`

---

## Dashboard schema

| Section | Purpose | Canonical source |
|---------|---------|------------------|
| **Campaign status** | Principal, phase, days until primary, next critical dates | `principal-profile.md`, `calendar-2026.md` |
| **Active clients** | Multi-client consulting view: who is active, jurisdiction, channel_key | [clients/](clients/) + per-client sheets |
| **Compliance blockers** | Per-jurisdiction open items before new paid work | [compliance-checklist.md](compliance-checklist.md) + client templates |
| **Territory blockers** | Stale docs, placeholder-heavy research surfaces, missing work-politics gate rhythm | Derived from `calendar-2026.md`, `opposition-brief.md`, `principal-profile.md`, `revenue-log.md`, `brief-source-registry.md`, `content-queue.md`, `users/grace-mar/recursion-gate.md` |
| **Pending work-politics gate items** | Work-politics-only `RECURSION-GATE` review | `users/grace-mar/recursion-gate.md` via territory filter |
| **Brief readiness** | What sources feed the weekly brief and what still needs checking | `brief-source-registry.md` |
| **Content queue** | X / content workflow state for `@usa_first_ky` | `content-queue.md` |
| **Revenue / offer state** | Revenue totals, BTC/SMM commitments, active commercial surfaces | `revenue-log.md`, `fiverr-microtask-100.md`, `account-x.md` |
| **Outreach learning** | Offer framing, proof, target segments, funnel, and objections | `outreach-workspace.md`, `offers.md`, `proof-ledger.md`, `target-registry.md`, `outreach-funnel.md`, `objection-log.md` |
| **Next actions** | Highest-leverage companion/operator actions now | Derived from the sections above |

---

## Canonical working files

| File | Role |
|------|------|
| `README.md` | Territory doctrine, scope, sync policy, and support menu |
| `consulting-charter.md` | Umbrella consulting mission + service lines (federal / state / local / intl) |
| `compliance-checklist.md` | Pre-engagement gates (FEC, state, FARA, intl) |
| `clients/` | Per-client index; [clients/massie-ky4.md](clients/massie-ky4.md) = primary client |
| `brief-source-registry.md` | Structured intake and freshness tracker for weekly brief inputs |
| `content-queue.md` | Structured X/content operations queue |
| `weekly-brief-template.md` | Output shape for the campaign brief |
| `civ-mem-draft-protocol.md` | Civ-mem → speech/policy; human-always-approves gates |
| `prep-before-call-abc.md` | A/B/C prep template (legitimacy, structure, liability) before high-stakes calls/decisions; fixed perspectives, tensions preserved |
| `polyphonic-cognition-protocol-skill.md` | Loadable protocol for agents/humans: fixed A/B/C/D, instinct-as-input, contradiction badge, no write unless relay |
| `clawhub-polyphonic-cognition/` | ClawHub publishable bundle: skill.yaml, SKILL.md, clawhub.json, README, SECURITY; instructions-only, no permissions |
| `scenario-polyphonic-cognition-skill.md` | Illustrated scenario: prep before a call, instinct-as-input, A/B/C + tension + reversibility, "we did X" |
| `cheat-sheet-polyphonic-cognition-protocol.md` | One-page staff training: when to query, read A/B/C, relay only if "record," "we did X" after |
| `one-pager-assistant-brain-cognitive-polyphony.md` | Reusable one-pager: assistant brain + polyphonic cognition; federal and "what is this system" |
| `capability-statement-assistant-brain.md` | Reusable capability statement (what we provide, why unique, who for, past performance); federal and general |
| `past-performance-assistant-brain.md` | Past performance evidence for assistant brain / polyphonic cognition; feeds capability statement and proposals; PP-001 (campaign) + placeholders for A/B/C prep, before/after, training |
| `competitor-research-assistant-brain-judgment-testing.md` | Competitor scan: multi-perspective / options / debate tools, government/civic, research; positioning vs us |
| `uare-ai-competitive-notes.md` | Uare.ai (Eternos): blog excerpts, LoCascio/Mayfield/Boldstart quotes; pitch comparison and differentiation |
| `lessons-solo-founder-ai-video.md` | Lessons from solo-founder/AI-talent video: taste vs conviction, speed of control, coordination proxy, blocked by overhead; mapped to assistant brain |
| `lessons-perplexity-computer-video.md` | Lessons from Perplexity Computer video: skills, sub-agents, Model Council vs us, memory, integrations, visual output; actionable takeaways |
| `lessons-deepseek-insider-self-improving-agents.md` | Lessons from DeepSeek Insider (John Wang): sovereign layer vs self-improving agents, memory/bounded session, input-grounded A/B/C, human learning; positioning |
| `lessons-openclaw-skills-video.md` | Lessons from OpenClaw skills video: Larry (constraints from failure), review vs mad dog, Anti-AI slop, Mission Control complementary, security; protocol output quality |
| `actionable-features-and-insights.md` | Actionable features (instinct-as-input, reversibility, contradiction badge, post-decision), copy snippets, process items; priority order |
| `civ-mem-test-run-*.md` | Dated test runs (DRAFT until signed) |
| `principal-profile.md` | Principal baseline |
| `opposition-brief.md` | Living opposition tracker |
| `calendar-2026.md` | Election and compliance calendar |
| `revenue-log.md` | Revenue and allocation continuity |
| `outreach-workspace.md` | Canonical outreach entrypoint and workflow rhythm |
| `offers.md` | Current offer framing and low-risk entry offers |
| `proof-ledger.md` | Reusable proof fragments for outreach |
| `target-registry.md` | Narrow target segments and lead-source logic |
| `outreach-funnel.md` | Outreach tracking by stage |
| `objection-log.md` | Structured learning from objections and replies |

---

## Operating rhythm

1. **"We did X" → stage** — After calls, readings, decisions, milestones, say "we did X" so the agent stages to RECURSION-GATE; the gate stays current. See [we-did-x-habit.md](../../we-did-x-habit.md).
2. Refresh `brief-source-registry.md` before the weekly brief.
3. Review `content-queue.md` before asking for post drafts.
4. Use the work-politics dashboard/operator surface for territory blockers and next actions.
5. Use `outreach-workspace.md` when the work block is about offer testing, proof, and buyer learning rather than campaign execution.
6. Stage work-politics milestones through `RECURSION-GATE` when something should become audited continuity or Record-adjacent knowledge.

---

## Guardrail

This workspace is a `WORK` surface. It does not create a second queue, and it does not change the gated merge rule.
