# Feedback: AutoGen / Multi-Agent Exploration (for assessment)

**Purpose:** Handoff for a new agent session to **assess** this feedback. The feedback compares grace-mar’s cognitive-fork design to multi-agent patterns (AutoGen/AG2) and suggests hybrid exploration paths. No commitment to implement; assess alignment, risks, and where this would live.

**Date captured:** 2026-03  
**Assessed:** See [feedback-autogen-exploration-2026-03-assessment.md](feedback-autogen-exploration-2026-03-assessment.md). Design and minimal prototype: [exploration-multi-agent-deliberation.md](exploration-multi-agent-deliberation.md); prototype under `exploration/autogen-deliberation/`.

---

## 1. Summary of feedback

The feedback assumes a prior discussion of **cognitive architectures like AutoGen** and interprets “exploring” as probing ways to evolve or compare the **cognitive fork** toward more **agentic/multi-module** behavior, given:

- Runtime integration (OpenClaw, export manifests)
- Contradiction handling and reflection gates
- External harness portability

It contrasts grace-mar (singleton-centric, governed, evidential) with **AutoGen/AG2** (conversational multi-agent, emergent collaboration) and proposes **low-risk exploration paths** that keep the companion gate intact.

---

## 2. Feedback’s view of current grace-mar

| Layer | Description (as stated in feedback) |
|-------|-------------------------------------|
| **SELF** | IX-A knowledge, IX-B curiosity, IX-C personality as immutable core identity |
| **SELF-LIBRARY** | Including CIV-MEM as read-only reference layer |
| **SKILLS** | THINK/WRITE as capability modules |
| **EVIDENCE + recursion-gate** | Controlled evolution; no emergent drift; changes require explicit user/operator approval |

**Repo anchors to verify:**  
`docs/conceptual-framework.md`, `docs/architecture.md`, `docs/self-template.md`, `agents.md` (Sovereign Merge Rule, knowledge boundary), `docs/boundary-self-knowledge-self-library.md`.

---

## 3. Comparison table (from feedback)

| Aspect | grace-mar (current) | AutoGen / multi-agent style | Suggested hybrid idea |
|--------|---------------------|-----------------------------|------------------------|
| **Core entity** | Single governed fork | Swarm of ConversableAgents | Internal “council” agents that deliberate *inside* the recursion-gate before proposing changes to SELF |
| **Coordination** | Gated pipeline + user review | GroupChat / message-passing / negotiation | Lightweight GroupChat simulator (AutoGen patterns): “Identity Guardian”, “Evidence Validator”, “Curiosity Explorer” → output staged for user review |
| **Memory / state** | Canonical Markdown + EVIDENCE log | Short-term chat + long-term vector stores | Export Record as shared memory object; AutoGen agents read-only at runtime |
| **Reflection** | Contradiction Engine spec + session briefs | Built-in critique/refine loops | Formalize reflection as agent loop: propose → critique (vs SELF boundaries) → refine → gate |
| **Determinism / control** | Very high (gates, validation) | Medium (emergent, tunable) | Keep final integration gated/user-approved; use AutoGen only for **pre-proposal ideation** |
| **Runtime integration** | OpenClaw hook, Telegram bot, export manifests | Native async, tool-calling, code exec | Use `export_manifest.json` + `llms.txt` to bootstrap AutoGen agents that treat the fork as persona / long-term memory |

**Repo anchors:**  
`docs/CONTRADICTION-ENGINE-SPEC.md`, `docs/openclaw-integration.md`, `docs/contradiction-timeline.md`, `docs/pipeline-events-schema.md`, export scripts and manifest shape.

---

## 4. Why explore now (feedback’s rationale)

- **Phase 7 (emergent cognition)** is live → fork is beyond pure seeding; multi-agent deliberation could simulate “emergence” without identity bleed.
- Recent work: runtime consumer, approval inbox, OpenClaw integration → bridges to external harnesses already exist; AutoGen could test **multi-module coordination inside the fork** (e.g. IX-B “debating” with IX-A on new proposals).
- No AutoGen in repo yet; analyst prompts, PRP, agent manifest exports are cited as compatible. **agents.md** guardrails (no leakage, no unapproved changes) align with wrapping AutoGen in a **sandboxed, read-only** mode around the Record.

---

## 5. Concrete exploration paths (from feedback)

1. **Internal deliberation loop (prototype)**  
   - Small AutoGen GroupChat (3–5 agents) ingesting `self.md` + recent `recursion-gate.md` candidates.  
   - Roles: Guardian (SELF vs SELF-LIBRARY), Validator (EVIDENCE/CIV-MEM), Explorer (IX-B), Writer (drafts).  
   - Output → staged markdown for user review (no auto-apply).  
   - Goal: reasoning depth before the gate without losing control.

2. **Runtime consumption experiment**  
   - Export fork manifest; initialize AutoGen `ConversableAgent` with system prompt from `grace-mar-llm.txt`.  
   - Short sessions (e.g. via Telegram wrapper); agent “embodies” Grace-Mar, queries SELF-LIBRARY read-only.  
   - Log outputs as EVIDENCE candidates → into existing pipeline.

3. **Contradiction Engine + agent reflection**  
   - Model CONTRADICTION-ENGINE-SPEC as AutoGen critique loop: propose → detect conflicts → suggest resolutions → then gate.  
   - All before merge.

---

## 6. Assessment tasks for next session

When assessing this feedback, the next agent should:

1. **Verify claims**  
   - Confirm the “current grace-mar” summary (SELF, SELF-LIBRARY, SKILLS, EVIDENCE, gate) against `docs/architecture.md`, `docs/conceptual-framework.md`, and `agents.md`.  
   - Confirm Phase 7 and “emergent cognition” wording and intent.  
   - Confirm that analyst prompts, PRP, and export manifest are as described (read-only consumption, no merge from AutoGen).

2. **Invariant alignment**  
   - Check each exploration path against: Sovereign Merge Rule, knowledge boundary, no unapproved merge, stage-only automation, CONTRADICTION-ENGINE-SPEC §2 (architectural constraints).  
   - Explicitly note: where could an AutoGen layer write? Only to staging/candidates, never to SELF or EVIDENCE without gate.

3. **Recommendation**  
   - Should any path be adopted? Options: (a) design-only (doc in work-dev or new design note), (b) minimal prototype (e.g. internal deliberation loop as experiment), (c) defer.  
   - If adopt: where does it live? (e.g. `docs/skill-work/work-dev/` design doc, `docs/design-notes.md` section, or new `docs/exploration-multi-agent-deliberation.md`.)

4. **Risks and boundaries**  
   - Identity bleed: can “council” or AutoGen agents ever write to Record? (Answer must remain no.)  
   - Dependency: add AutoGen as optional/experimental only; do not make core pipeline depend on it.  
   - Scope: keep any prototype clearly labeled as exploration, not production gate path.

---

## 7. Repo anchors (quick ref for assessor)

| Topic | Location |
|-------|----------|
| Governance, merge rule, knowledge boundary | `agents.md` |
| Architecture, harness, non-goals | `docs/architecture.md` |
| Tricameral mind, Record, companion | `docs/conceptual-framework.md` |
| Contradiction engine constraints | `docs/CONTRADICTION-ENGINE-SPEC.md` §2 |
| OpenClaw, export, handback | `docs/openclaw-integration.md`, `docs/skill-work/work-dev/README.md` |
| Pipeline events, staging | `docs/pipeline-events-schema.md`, `bot/core.py` (emit_pipeline_event, _stage_candidate) |
| Phase 7 / emergent cognition | `users/grace-mar/self.md` or evidence; bootstrap or handoff |
| Export manifest, PRP | `scripts/export_*.py`, manifest/PRP outputs |
| Design non-goals (agentic) | `docs/architecture.md` (“Any future agentic or orchestration layer … must keep merge authority human-only”) |

---

## 8. Suggested re-entry prompt for next session

Copy-paste this to start the assessment:

```
Assess the feedback in docs/feedback-autogen-exploration-2026-03.md:

1. Verify the "current grace-mar" description against architecture.md, conceptual-framework.md, and agents.md.
2. Check each of the three exploration paths against the Sovereign Merge Rule, knowledge boundary, and CONTRADICTION-ENGINE-SPEC §2. Can any path write to the Record without the gate? (It must not.)
3. Recommend: (a) design-only doc, (b) minimal prototype (where and how), or (c) defer. If (a) or (b), say where in the repo it should live (work-dev, design-notes, or new exploration doc).
4. List concrete risks (identity bleed, dependency creep, scope) and how to keep them bounded.
```
