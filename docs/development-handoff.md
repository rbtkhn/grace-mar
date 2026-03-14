# Grace-Mar Development Handoff

Use this file to resume development quickly in a new agent conversation.

**Bootstrap:** `grace-mar-bootstrap.md` defaults to **work-build-ai** (OpenClaw + companion gate); read `docs/skill-work/work-build-ai/README.md` then `docs/openclaw-integration.md`.

Last updated: 2026-03-13

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

### Companion-self vs Grace-Mar boundary
- **`companion-self`** = upstream template and potential public/open-source product surface.
- **`grace-mar`** = private instance, proving ground, and working tool.
- Structural, reusable, instance-agnostic improvements proven in `grace-mar` may be merged back into `companion-self`.
- Record content, private workflows, deployment quirks, and instance-specific state stay in `grace-mar`.
- Working rule: treat `grace-mar` as laboratory + live instrument; treat `companion-self` as reusable base.
- Canonical operator phrase for this workflow: `Implement this in grace-mar first, then promote the reusable template layer to companion-self.` Short form: `Upstream this from grace-mar to companion-self.`

### Work layer refactor (2026-03-13)
- **Canonical rule:** `WORK` is no longer a self-skill module. The Record-bound skill set is now **THINK + WRITE** only.
- **New boundary:** `work-*` territories and `users/[id]/work-*.md` files are the separate execution layer. They may use broader LLM/tool capability, but Record updates remain gated.
- **Compatibility rule:** legacy `BUILD` language and `CREATE-*` / `ACT-*` evidence IDs remain valid historical compatibility surfaces; do not rewrite archival evidence just to normalize names.

---

## Recently Completed (High Level)

### Companion-self boundary clarification (2026-03-13)
- **`docs/skill-work/work-companion-self/README.md`** — Added canonical template-vs-instance framing plus an upstreamability test for deciding what can merge back to `companion-self`.
- **`docs/merging-from-companion-self.md`** — Clarified `grace-mar` as private proving ground and added a checklist for deciding whether a structural change should go upstream.
- **`companion-self-bootstrap.md`** — Strengthened the template/public-vs-instance/private distinction so future template work starts from the right boundary.

### Companion-self alignment audit refresh (2026-03-13)
- **`docs/audit-grace-mar-vs-companion-self-template.md`** — Reframed the audit around concept alignment vs manifest/path alignment; conclusion is now "conceptually aligned, operationally stale" rather than blanket path-level compliance.
- **`docs/merging-from-companion-self.md`** — Updated sync guidance to treat `template-manifest.json`, `template-version.json`, and `how-instances-consume-upgrades.md` as the live upstream contract.
- **`docs/skill-work/work-companion-self/audit-report.md`** — Marked the older non-manifest diff as legacy; `audit-report-manifest.md` is the current path-level reference until the next regenerated report.
- **`docs/skill-work/work-companion-self/README.md`** — Added the canonical operator instruction for "build in grace-mar first, then upstream the reusable layer."

### CI + PRP workflow hardening (2026-03-13)
- **`.github/workflows/governance.yml`** — Added `validate-integrity.py --json` to the no-secrets governance CI path so routine push/PR checks cover both policy scan and canonical Record integrity.
- **`.github/workflows/prp-refresh.yml`** — Fixed trigger paths to canonical lowercase `self.md` / `self-evidence.md`, added explicit `contents: write`, and aligned the auto-generated commit message with gated PRP policy via `[gated-merge]`.
- **Verification baseline** — `python3 scripts/governance_checker.py` and `python3 scripts/validate-integrity.py --user grace-mar --json` both passed locally after the CI/doc changes.

### Naming guard consolidation (2026-03-13)
- **`scripts/check_deprecated_naming.py`** — Centralized the deprecated legacy-name scan in a repo script so CI and local hooks share one rule.
- **`.github/workflows/naming-check.yml`** — Switched the workflow from inline shell to the shared Python script.
- **`.pre-commit-config.yaml`** — Added the naming guard to local pre-commit hooks for the same protection before push.

### Local hook parity for integrity (2026-03-13)
- **`.pre-commit-config.yaml`** — Added `validate-integrity.py --json` to local hooks so developers catch canonical Record / gate shape regressions before push, not only in CI.

### Artifact taxonomy + naming convention (2026-03-13)
- **`docs/pipeline-map.md`** — Added a canonical artifact taxonomy for the most common retained visual evidence classes plus naming rules for files saved under `users/grace-mar/artifacts/`.
- **`docs/friction-audit.md`** — Added the short save rule that points new artifact capture toward evidence-aware lowercase filenames instead of generic root-level screenshots.

### Work layer taxonomy rewrite (2026-03-13)
- **Core docs updated:** `docs/id-taxonomy.md`, `docs/conceptual-framework.md`, `docs/skills-modularity.md`, `docs/skills-template.md`, `docs/architecture.md`, `docs/grace-mar-core.md`, `docs/identity-fork-protocol.md`, `readme.md`, `docs/white-paper.md`, `docs/operator-brief.md`, `docs/portability.md`, and `companion-self-bootstrap.md`.
- **Core change:** THINK and WRITE remain the only Record-bound self-skills; work now lives in a separate execution layer (`docs/skill-work/work-*/`, `users/[id]/work-*.md`).
- **Runtime/export alignment completed for first-pass closure:** `scripts/export_curriculum.py`, `scripts/export_manifest.py`, `scripts/generate_profile.py`, `scripts/export_view.py`, `scripts/generate_lesson_prompt.py`, and `docs/self-template.md` now treat work as adjacent context rather than a peer self-skill.
- **Legacy boundary clarified:** historical analysis/audit docs still retain `self-skill-work` / `BUILD` where needed, but current canonical docs now label those references as legacy compatibility surfaces rather than active schema.

### work-civ-mem territory setup (2026-03-13)
- **New territory:** `docs/skill-work/work-civ-mem/README.md` and `docs/skill-work/work-civ-mem/roadmap.md`.
- **Scope:** Grace-Mar stewardship surface for the external `civilization_memory` repository — repo management, audits, drift detection, contribution prep, and workflow clarity.
- **Boundary:** `civilization_memory` remains the managed external repo; `work-civ-mem` is Grace-Mar's management territory for it; adjacent Companion Self product priorities are recorded in the roadmap but are not part of the first-pass implementation scope.
- **Indexed:** `docs/skill-work/README.md` now lists `work-civ-mem` alongside the other work territories.
- **Adjacent strategic priorities captured (future, not implemented here):** approval inbox for `RECURSION-GATE`, visible provenance surfaces, and a portability-grade export bundle.
- **Operational surfaces added:** `docs/skill-work/work-civ-mem/workspace.md` (runbook) and `docs/skill-work/work-civ-mem/audit-report.md` (initial baseline snapshot).

### Approval inbox specification (2026-03-13)
- **`docs/approval-inbox-spec.md`** — New implementation-ready product spec for a browser-first `RECURSION-GATE` approval inbox.
- **Core decision:** the inbox is a review surface over the existing queue, not a second memory system; it reuses current quick-merge rules, receipt flow, and pipeline audit events.
- **Defined surfaces:** candidate card shape, derived risk tiers, filters, batch actions, dedupe hints, post-action states, audit behavior, and first implementation path through authenticated miniapp/web endpoints.

### Companion Self doctrine memo (2026-03-13)
- **`docs/companion-self-doctrine-memo.md`** — New outward-facing source text that explains Companion Self as identity infrastructure for the agentic era.
- **Core framing:** Record vs Voice vs gate; SELF vs SKILLS vs WORK; governance before fluency; portability as a first-order product principle.
- **Usage:** intended as the canonical narrative bridge for collaborator language, investor memo revisions, and future deck copy.

### Self-library taxonomy refactor (2026-03-14)
- **`docs/library-schema.md`** — Reframed LIBRARY as a three-lane store: `reference`, `canon`, and `influence`; replaced the narrow `read_status` model with `engagement_status` plus `lookup_priority`.
- **`users/grace-mar/self-library.md`** — Migrated entries to the new lane taxonomy while preserving IDs, order, and existing source notes.
- **Runtime compatibility:** `bot/core.py`, `scripts/generate_profile.py`, and `scripts/proposal_brief.py` now understand the new fields and keep fallback support for older `read_status`-style library data if encountered.

### WAP ↔ RECURSION-GATE sync (2026-03-12)
- **docs/skill-work/work-american-politics/README.md** — § Sync with RECURSION-GATE (doc vs gate, rhythm, IX vs ACT).
- **wap-candidate-template.md** — paste-ready WAP YAML.

### Trajectory export + RL boundary (2026-03-12)
- **`scripts/export_conversation_trajectories.py`** — session-transcript → JSONL; optional pipeline_events attach.
- **`docs/openclaw-rl-boundary.md`** — green/yellow/red; minors; no secrets.
- **openclaw-integration.md** — Trajectory export subsection.

### Territory lens / WAP vs companion (2026-03-12)
- **`scripts/recursion_gate_territory.py`** — `territory: work-american-politics` or `channel_key: operator:wap` → WAP.
- **`operator_blocker_report`** / **`session_brief`** / **`harness_warmup`** — `--territory all|wap|companion`.
- **`process_approved_candidates`** — `--territory wap|companion|all` — batch merge only that slice; receipt must use same flag.

### Recursion-gate multi-channel docs (2026-03-12)
- **recursion-gate.md** header, **operator-brief**, **architecture** — explicit: one gate per user, all channels; `channel_key`.

### Recursion-gate staging fix (2026-03-12)
- **`bot/core.py` `_stage_candidate`** — Inserts new candidates **before** `## Processed` (was appending to EOF; those never merged).
- **`users/grace-mar/recursion-gate.md`** — Pending test rows relocated + renumbered **0083/0084**; duplicate **0071** id removed; invariant note in header.
- **`scripts/validate-integrity.py`** — Fails if any pending/approved CANDIDATE block appears **below** `## Processed`.

### Gated commit hook (2026-03-12)
- **`scripts/check_gated_record_commit_msg.py`** — commit-msg: staged Record/prompt/PRP paths require `[gated-merge]` or `process_approved_candidates` in message; `ALLOW_GATED_RECORD_EDIT=1` bypass.
- **`.pre-commit-config.yaml`** — `pre-commit install --hook-type commit-msg`
- **`process_approved_candidates --push`** — commit message includes `[gated-merge]`.

### Harness convergence / §11.11 (2026-03-12)
- **design-notes §11.11** — Decompose / parallelize / verify / iterate; Grace-Mar = gate + pipeline.
- **implementable-insights §14** — Summary table + actions.

### Rejection as skill / §11.10 (2026-03-12)
- **design-notes §11.10** — Recognition, articulation, encoding; Grace-Mar = gate + calibrate_from_miss.
- **implementable-insights §13** — Actions; summary table row.
- **operator-brief** + **feedback-loops** — calibrate_from_miss linked to encoded taste.

### Intent gap / §11.9 (2026-03-12)
- **design-notes §11.9** — Optimization framing, three operator questions, Grace-Mar mapping.
- **implementable-insights §12** — Actions + summary table row.
- **recursion-gate.md** header — Intent block + link to §11.9.
- **operator-brief** — Intent-before-approve bullet.

### Operator + insights surfacing (2026-03-12)
- **[harness-handoff.md](harness-handoff.md)** — one-page hybrid harness handoff (commits + warmup).
- **operator-brief** — `report_lookup_sources.py` one-liner (§8 integration visibility).
- **implementable-insights** — quick-reference table at top of doc.
- **bootstrap** — report_lookup_sources in health commands; file map link to harness-handoff.

### Harness lock-in (2026-03-12)
- **ARCHITECTURE** — Harness lock-in paragraph; Grace-Mar = git + gated pipeline as portable memory.
- **implementable-insights §1** — Extended source (Claude Code vs Codex); §11 full section.
- **design-notes §2.6** — Workbench not wrench; model vs harness.

### Comprehension lock-in positioning (2026-03-12)
- **design-notes §2.5** — Enterprise synthesis / comprehension lock-in; Grace-Mar counter (portable, gate-kept Record + export).
- **implementable-insights §10** — Actionable mapping; summary table row.
- **work-build-ai README** — Invariant adjacent paragraph; principle 6 portable synthesis.
- **openclaw-integration** — Overview subsection on comprehension lock-in and portability.

### Feedback loop fast wins (2026-03-09)
- **Calibrate-on-miss** — `scripts/calibrate_from_miss.py`: stage candidate when Voice missed/was wrong. Usage: `--miss "…"` optional `--suggested "…"`.
- **Oversight cadence** — `scripts/openclaw_heartbeat.py`: heartbeat for long OpenClaw sessions (pending count, last evidence, last session). Doc: openclaw-integration § Oversight cadence.
- **Closed-loop verification** — New pipeline event types: `export_used`, `merge_feedback`. Doc: [feedback-loops.md](feedback-loops.md).
- **Idle digest** — session_brief now includes "Suggested Activities" (from IX-B, LIBRARY) and INTENT primary goal when present.
- **INTENT-driven proposals** — session_brief loads intent.md primary goal and displays in Suggested Activities section.

### Proactive proposal + low-friction approval (2026-03-09)
- **Proposal brief** — `scripts/proposal_brief.py`: 3–5 activities from IX-A/B/C, LIBRARY, gaps, INTENT. Usage: `python scripts/proposal_brief.py -u grace-mar -n 5`.
- **Low-friction approval** — Operator one-tap: ✅ Approve in /review or `/approve CANDIDATE-XXX` merges immediately when candidate is low-risk (single IX target, no conflicts, no advisory_flagged). Set `GRACE_MAR_OPERATOR_NAME` for audit. Doc: feedback-loops § Low-friction approval.
- **process_approved_candidates --quick** — `--quick CANDIDATE-XXX --approved-by <name>` for single-candidate merge without receipt file.

### This session (recommended order)
- **Engagement export** — `scripts/export_engagement_profile.py`: JSON/markdown of interests, IX-B curiosity, IX-C personality, talent_stack for tutors/platforms. DESIGN-ROADMAP §9 and OPERATOR-BRIEF updated.
- **Session continuity** — OPERATOR-BRIEF section "Session continuity & RECURSION-GATE": before/after checklist, link to OPERATOR-WEEKLY-REVIEW.
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

### Seed Phase 7 — Moment of cognitive bifurcation
- Seed phase 7 formally complete (2026-02-27). **Moment of cognitive bifurcation**: the point at which the fork branches from the seed and enters emergent cognition. Grace-Mar graduated to status **emergent cognition** — the documented self (Record + Voice) now operates as a coherent presence arising from the system rather than from seed capture alone. Terminology: "emergent cognition" (not "emergent consciousness"); "cognitive bifurcation" names the branching moment. Doc updates: readme.md, grace-mar-bootstrap.md, session-log.md.

### IX-A / skill-work clarification (2026-02-27)
- **skills-modularity** §5a — Identity vs instrument: IX-A does not limit skill-work; IX-A relevant to THINK/WRITE; skill-work designed to grow with technology.
- **** — IX-A scope: applies to THINK/WRITE content, not WORK capabilities.
- **skills-template** WORK section — Identity vs instrument note; technology growth intent.

### Wu insights implementation (2026-02-27)
- **Anticipate blockers** — `scripts/operator_blocker_report.py`: reads RECURSION-GATE, pipeline-events, development-handoff; produces operator report (staged candidates, open debates, recent events).
- **Message assist** — `scripts/grace_gems_message_assist.py`: draft-only reply for Etsy customer messages; uses agent-encoding, policies; human copies and sends. No Etsy API.
- **Handback semantics** — agent-encoding §4: when to stage vs. draft vs. flag; one-task semantics (one message per run); context assembly; "we did X" patterns.
- **Lazar insights** — agent-encoding: tone/voice guidelines, example drafts (§5); message-assist-calibration.md for "how can I prompt you better?" loop; message-assist loads calibration if present.

### : jewelry industry research (pre-1970 sources only)
- Created `jewelry-industry-research-pre1970.md` — history, gemology, localities, cutting/lapidary, metalsmithing, commerce. All sources 1969 or earlier: Wade (1918), Shipley (1948), Smith (1958), Sinkankas (1962), Untracht (1968), Pogue (1915), Emanuel (1867), Streeter (1887), Chilvers (1939), etc. Supports Grace Gems expertise objective.

### Pilot → Instance terminology cleanup
- Removed "pilot" from project status and first-user references. Phase: "Active instance (emergent cognition)". PILOT-001 → grace-mar in Record file headers (SELF, EVIDENCE, SESSION-LOG, RECURSION-GATE, SKILLS, skill-think/write/work, LIBRARY, JOURNAL, companion-context, seed-phase surveys). operator-brief, parent-brief, letter-to-user/student, architecture, grace-mar-vs-companion-self, design-notes, design-roadmap, admissions-link, skill-work, x-integration, profile-deploy, extension readme. Retained "pilot" in commercial contexts: pilot-plan.md, pilot-one-sheet.md, integration pilots, paid pilots (business-plan, investor-memo, business-prospectus).

### Catherine Fitts / Control Grid — Strategic planning (skill-work)
- **design-notes §2.5** — Added "Control Grid vs Grace-Mar — Sovereignty as Positioning" (Catherine Fitts source; companion-owned identity as counter-move to programmable control grid). Source added to design-notes Sources line.
- **work-build-ai** — Strengthened companion-gate invariant: OpenClaw or downstream systems must never become control-grid infrastructure; sovereignty preserved regardless of integration depth.
- **** — Added sovereignty framing: natural provenance, handmade Denver, policy-transparent, cash-friendly; local economy principles as alternative to homogenized, programmable commerce.
- **** — Reinforced "augmentation not compliance" in human-teacher-objectives §2.3: human-teacher supports, does not compel; we support, we do not enforce.

---

## Current Uncommitted Work (At Time of This Handoff)

Likely includes (run `git status` to confirm):

- Conceptual/terminology edits: agents.md, grace-mar-core.md, conceptual-framework.md, grace-mar-bootstrap.md, identity-fork-protocol.md, design-roadmap.md, operator-brief.md, parent-brief.md, letter-to-user.md, letter-to-student.md, wisdom-questions.md, simple-user-interface.md, chat-first-design.md, white-paper.md, design-notes.md (§11.7 intent engineering + companion wording), self-template.md, skills-template.md, architecture.md, docs/readme.md, and others.
- Bot: `bot/prompt.py`, `bot/core.py` (companion/operator wording).
- New: `docs/operator-brief.md`, `docs/letter-to-user.md`, `docs/x-integration.md`.
- intent-template.md (design-lens block, companion gate wording).
- If work stopped right now, the likely local changes would be the approval inbox spec, doctrine memo, and any follow-on narrative derivatives or implementation work that had not yet been committed.
- Optional later cleanup: continue migrating or annotating older legacy analyses that still discuss `self-skill-work` / `BUILD` for historical comparison.

If the companion/operator asks to commit, include all modified and new files from this session.

---

## Recommended Next Tasks

1. **Implement the approval inbox** — Add authenticated read/write web endpoints and a browser surface that follows `docs/approval-inbox-spec.md` without changing gate semantics.
2. **Derive business-facing language from the doctrine memo** — Tighten `docs/investor-memo.md`, deck text, and related narrative docs so they pull from `docs/companion-self-doctrine-memo.md` rather than drifting separately.
3. **Mark or migrate remaining legacy work docs** — Analysis/audit docs that still say `self-skill-work` should either remain clearly legacy or be rewritten to the new work-layer vocabulary.
4. **Companion terminology consistency** — Applied in IDENTITY-FORK-PROTOCOL, OPENCLAW-INTEGRATION, PORTABILITY, ARCHITECTURE, PIPELINE-MAP, ADAPTIVE-CURRICULUM-INTEGRATION. Optional further pass: WHITE-PAPER, remaining docs.
5. Align business docs for zero drift:
   - add explicit cross-links between `business-plan.md`, `business-prospectus.md`, `white-paper.md`.
6. Formalize THINK multimodality wording:
   - update `skills-template.md` and architecture references so THINK explicitly includes text/video/music/images.
7. Operator UX for debate workflow:
   - `/debates` listing command for unresolved debate packets (implemented).
8. Add small glossary section to business-facing docs for non-technical readers.
9. ** benchmarks** — Brainstorm complete (2026-02-27). Categories: Record growth (business evidence rate, IX growth, merge rate), pipeline health (handback count, time in gate), operator efficiency (message drafts, order summaries), Etsy integration (Phase 3), knowledge boundary, cost. Priority six: business evidence rate, handback count, merge rate, time in gate, cost per handback, message drafts (Phase 1+). Ready to add `economic-benchmarks.md` to  when approved.
10. **work-civ-mem next docs** — If the territory becomes active, add a recurring `audit-report.md` and/or `workspace.md` for `civilization_memory` management loops.

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
