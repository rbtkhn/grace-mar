# Grace-Mar Development Handoff

Use this file to resume development quickly in a new agent conversation.

Last updated: 2026-02-24

---

## Current Baseline

- Branch: `main`
- Latest pushed commit: `f3b27f2` (intent-governance + OpenClaw + curiosity merge batch)
- Core invariants active: Sovereign Merge Rule, knowledge boundary, evidence linkage, **companion** merge authority (see Terminology below).

---

## Conceptual & Terminology Changes (This Session)

**Read this first** when resuming — the following are now canonical in docs and prompts.

### Tricameral mind (bicameral deprecated)
- **Tricameral mind** = **MIND** (human / companion), **RECORD** (Grace-Mar), **VOICE** (Grace-Mar).
- The earlier "bicameral dyad" framing is deprecated. Use "tricameral mind" only.
- CONCEPTUAL-FRAMEWORK §8 is the source; agents.md and grace-mar-bootstrap reference it.

### Companion (not "user" in conceptual prose)
- **Companion** = the person whose Record it is (the human in the tricameral mind). Preferred term in conceptual docs and prompts; affectionate and relatable.
- **Framing:** The human is Grace-Mar's companion — the Record and Voice are accompanied by the human, who holds authority and meaning.
- Technical identifiers unchanged: `users/[id]`, `--user`, `user_id` in code and paths stay as-is.

### Age-neutral language
- System is age-neutral. "Operator" or "facilitator" (not "parent") for whoever runs the gate when the companion is a minor or needs support.
- **operator-brief.md** and **letter-to-user.md** are the age-neutral entry points; PARENT-BRIEF and LETTER-TO-STUDENT remain as variants.
- WISDOM-QUESTIONS is "Reflective Tier"; SELF/SKILLS templates use "user" or "companion" in prose, not "child."

### Intent engineering as design lens
- **DESIGN-NOTES §11.7** — Intent engineering: "Context tells agents what to know; intent tells agents what to want." Grace-Mar's INTENT layer + companion gate = intent infrastructure at companion scale.
- Source: "Prompt Engineering Is Dead. Context Engineering Is Dying. What Comes Next Changes Everything." (YouTube transcript, 2026).
- intent-template.md has a design-lens block pointing to §11.7.

### X.com (Twitter) integration — design only
- **docs/x-integration.md** — Design-stage options for X API: feed consumer (read → match → stage) recommended first; Voice-on-X deferred. Tricameral alignment and technical placement documented. No implementation yet.

### Implementable insights (design + skills)
- **docs/implementable-insights.md** — Concrete takeaways from Claws/AGI discourse: harness vs model, continual learning = human-gated writes, system boundaries, config-via-skills, small auditable surface, forkable + skills. Linked from ARCHITECTURE § System boundaries and harness.
- **docs/adding-a-channel.md** — Skill pattern for new channels: one entrypoint per channel, shared core, env config, no channel logic in core.

---

## Recently Completed (High Level)

### This session (recommended order)
- **Engagement export** — `scripts/export_engagement_profile.py`: JSON/markdown of interests, IX-B curiosity, IX-C personality, talent_stack for tutors/platforms. DESIGN-ROADMAP §9 and OPERATOR-BRIEF updated.
- **Session continuity** — OPERATOR-BRIEF section "Session continuity & PENDING-REVIEW": before/after checklist, link to OPERATOR-WEEKLY-REVIEW.
- **/debates** — Operator command lists unresolved debate packets; `list_unresolved_debate_packets()` in core.py.
- **Companion terminology** — Pass over IDENTITY-FORK-PROTOCOL, OPENCLAW-INTEGRATION, PORTABILITY, ARCHITECTURE, PIPELINE-MAP, ADAPTIVE-CURRICULUM-INTEGRATION; DEVELOPMENT-HANDOFF task 1 and 4 updated.
- **docs/README** — Row for USING-GRACE-MAR-WITHOUT-A-SCHOOL; operator row uses "companion" not "user".

### Intent governance upgrades
- Added machine-readable intent export (`scripts/export_intent_snapshot.py`).
- Added cross-agent advisory conflict checks in merge flow.
- Added operator commands:
  - `/intent_audit`
  - `/intent_review`
  - `/intent_debate`
  - `/resolve_debate`
  - `/debates` — list unresolved debate packets
- Added debate packet stage/resolve workflow in pipeline tooling.

### OpenClaw integration upgrades
- Outbound export includes `intent_snapshot.json`.
- `user.md` export gets constitution context prefix when intent is available.
- Inbound OpenClaw staging performs advisory constitutional check and emits events.

### Record updates
- Curiosity probe responses were staged and merged into `IX-B` via approved candidates.
- Receipt-based merge flow executed and merge receipts persisted.

---

## Current Uncommitted Work (At Time of This Handoff)

Likely includes (run `git status` to confirm):

- Conceptual/terminology edits: agents.md, grace-mar-core.md, conceptual-framework.md, grace-mar-bootstrap.md, identity-fork-protocol.md, design-roadmap.md, operator-brief.md, parent-brief.md, letter-to-user.md, letter-to-student.md, wisdom-questions.md, simple-user-interface.md, chat-first-design.md, white-paper.md, design-notes.md (§11.7 intent engineering + companion wording), self-template.md, skills-template.md, architecture.md, docs/readme.md, and others.
- Bot: `bot/prompt.py`, `bot/core.py` (companion/operator wording).
- New: `docs/operator-brief.md`, `docs/letter-to-user.md`, `docs/x-integration.md`.
- intent-template.md (design-lens block, companion gate wording).

If the companion/operator asks to commit, include all modified and new files from this session.

---

## Recommended Next Tasks

1. **Companion terminology consistency** — Applied in IDENTITY-FORK-PROTOCOL, OPENCLAW-INTEGRATION, PORTABILITY, ARCHITECTURE, PIPELINE-MAP, ADAPTIVE-CURRICULUM-INTEGRATION. Optional further pass: WHITE-PAPER, remaining docs.
2. Align business docs for zero drift:
   - add explicit cross-links between `business-plan.md`, `business-prospectus.md`, `white-paper.md`.
3. Formalize READ multimodality wording:
   - update `skills-template.md` and architecture references so READ explicitly includes text/video/music/images.
4. Operator UX for debate workflow:
   - `/debates` listing command for unresolved debate packets (implemented).
5. Add small glossary section to business-facing docs for non-technical readers.

---

## External signal (2026-02-24)

Briefing items relevant to Grace-Mar / IFP positioning and design:

- **Persona selection** — Anthropic: LLMs simulate diverse characters in pre-training; post-training elicits a specific "Assistant" persona via a Persona Selection Model; "your AI is best understood as a character that learned to play itself." **Relevance:** Grace-Mar inverts default persona: the companion gates which character gets elicited. The Record is the selected character; the Voice speaks it. Design reinforces "character that learned to play itself" but with companion-owned selection, not vendor default.
- **Identity in the agent economy** — Anthropic vs DeepSeek/Moonshot/MiniMax (distillation/fraud); Frontier Alliances (BCG, McKinsey, Accenture) deploying AI at scale; IBM repriced on COBOL modernization. **Relevance:** IFP/companion-owned identity is the primitive that prevents lock-in and unauthorized distillation. Who owns the identity layer matters more as models and enterprises scale.
- **Homogenization of expressed identity** — Employers report AI-assisted job applications all sound the same; candidates who optimized hardest are deprioritized. **Relevance:** The Record is a counter-move: structured, evidence-linked, companion-owned identity that does not collapse into the same prompt-dust as everyone else. Differentiation through documented self, not through optimized generic persona.

See DESIGN-NOTES §11.8 for slightly expanded commentary.

---

## Quick Resume Commands

```bash
git status
python3 scripts/metrics.py
python3 scripts/session_brief.py --user grace-mar
python3 scripts/validate-integrity.py --user grace-mar --json
python3 scripts/governance_checker.py
```

If profile or prompt changed:

```bash
python3 scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt
```

---

## Reminder on Merge Authority

No direct merges into canonical Record files without explicit **companion** approval.
Staging and advisory analysis are allowed; integration remains companion-gated.

---

END OF FILE — DEVELOPMENT HANDOFF
