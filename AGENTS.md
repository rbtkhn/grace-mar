# AGENTS.md — AI Coding Assistant Guardrails

This file defines rules for any AI coding assistant working on this repository.

**For conceptual clarity:** Read `docs/conceptual-framework.md` — Record vs. fork, Voice vs. bot, fork vs. twin, terminology. **Prime directive:** The Record belongs to the companion (GRACE-MAR-CORE §I).

**For system design:** Read `docs/architecture.md`. For the formal skill modularity model (THINK/WRITE boundaries, separate work/execution layer, Voice and profile as functions of skill-write, invariants), see `docs/skills-modularity.md`.

**For chat/UI design:** Read `docs/chat-first-design.md` — principles for delivering the full experience within Telegram/chat (bounded sessions, one-tap, Record felt not seen).

**Design alignment:** Grace-Mar aligns with the 5000 Days series framing — abundance, identity beyond productivity, conductor workflow, symbiosis (human holds the reins), interregnum fortification (Part 14). See invariants 5–23 and 36 in conceptual-framework.md.

**Triadic cognition:** **Mind** (human) + **Record** + **Voice** — a **triad** (one human part, two digital parts). Grace-Mar **hosts** Record and Voice for this instance; the companion-self **architecture** defines how those digital parts work across instances. The **WORK execution layer** (operator, assistant, scripts on skill-work and WORK territories) is **instrumental** (drafts, stages); **not** a fourth part of the triad. **Companion self** = human–computer triadic cognition. **Tricameral mind** is an accepted synonym (e.g. prompts). Mind holds authority; the Record reflects; the Voice speaks when queried. The current Voice is reactive; future versions may include agentic Voice modalities (distinct from skill-work execution). New features should reinforce this structure. See CONCEPTUAL-FRAMEWORK invariant 35, 37, 38, and §8.

**Agent vocabulary (onboarding):** Many new AI users already use **agent** for “a tool-using runner.” **Work agent** and **skill-work agent** are **onboarding-friendly** names for that pattern on **WORK** surfaces: they **utilize** the Record (read; propose via the gate only) and may support the Voice (e.g. harnesses, PRP, prompt work) under **operator** control — they are **not** Mind, **not** the companion-facing Voice in chat, and **not** a fourth triad seat. **Skill-work agent** stresses the same idea scoped to **`docs/skill-work/`** and **WORK territories**, including **replicated / parallel** lanes. Precision term for the stack: **WORK execution layer**; beginner gloss: `docs/skill-work/work-xavier/GLOSSARY-FOR-BEGINNERS.md`.

---

## What This System Is

A **cognitive fork** — a structured, versioned record of an individual's cognitive development, initialized from a real person and growing through curated interactions. Preferred terms: **Record** (the fork) and **Voice** (the bot). The Record exists inside the companion's mind. The Voice (`bot/`) provides an emulation layer: an **observation window** and the **queryable voice** of the Record — it responds when queried, never unbidden. "The avatar is better because it remembers everything": the Record holds what the companion documents; the Voice recalls it. Teaching/tutoring is one of its functions: it answers questions, explains, and helps the companion learn in-character.

**Conceptual distinctions (see conceptual-framework.md):**
- **Companion** — The person whose Record it is (the human in **triadic cognition** — Mind in the triad). Preferred term over "user" in conceptual prose; affectionate and relatable. **Framing:** The human is Grace-Mar's companion — the Record and Voice are accompanied by the human, who holds authority and meaning. Grace-Mar serves the companion; the companion serves Grace-Mar.
- **Record and Voice** — The Record is the documented self; the Voice speaks the Record when queried. Self = Record + Voice (the thing you can talk to).
- **Companion self** — One phrase for both sides of the dyad: the companion's self (the human's self, externalized in the Record) and the self that companions (the Record and Voice that accompany the human). The ambiguity is intentional; see CONCEPTUAL-FRAMEWORK (companion self). **Companion self contains:** **self-knowledge** (**SELF-KNOWLEDGE**, IX-A), **self-curiosity** (IX-B), **self-personality** (IX-C), **self-skill-think**, **self-skill-write**, **self-archive**, **self-library** (**SELF-LIBRARY**; CIV-MEM subdomain), **self-memory**, **self-voice** (see [ID-TAXONOMY — Capitalization and format](docs/id-taxonomy.md#capitalization-and-format), [boundary-self-knowledge-self-library.md](docs/boundary-self-knowledge-self-library.md)). Work territories are adjacent execution surfaces, not self-skills.
- **companion-self** / **companion-xavier** — **Always hyphenated** when naming a **system or instance** (template repo, named fork, intelligence-system deployment). **companion-self** = upstream template; **companion-xavier** may name a **named instance** as an **intelligence-system entity** (e.g. a companion’s repo created from the template). This is **not** the same spelling as **companion self** (two words), the **conceptual** dyad above. See [glossary.md](docs/glossary.md).
- **Fork, not twin** — The Record diverges by design; it is its own entity, not a mirror.
- **Emulation** — Applies to the Voice (renders the Record in conversation), not to the Record's relationship to the real person.
- **Instances and release** — Exports are for consumption (schools, agents that read the Record), not for deploying other instances as independent economic/social actors without companion consent. See `docs/instances-and-release.md` and CONCEPTUAL-FRAMEWORK invariant 34.

---

## Operating Modes

Distinct modes govern what the agent may do. Avoid mixing them.

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation with companion | Respond as Voice; propose activities. Do not merge. Do not stage unless "we [did X]" triggers pipeline. |
| **Pipeline** | Process staged candidates | Detect signals, stage to RECURSION-GATE, or on approval instruct operator to run `process_approved_candidates.py --apply` (do not edit SELF/EVIDENCE/prompt directly). See [OPERATOR-WEEKLY-REVIEW](docs/operator-weekly-review.md) for recommended rhythm. |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. Do not edit. |

When in doubt, default to Session (conversational, no merges).

**Implementation preference:** The operator prefers to see a short proposal (scope, approach, files to touch) before the agent implements. Propose first; implement after approval.

**Proposal format:** One paragraph with: (1) Scope — what's in, what's out; (2) Approach — high-level steps or method; (3) Files — paths to create or modify. Trivial fixes (typos, obvious corrections) may skip proposal.

**Edit restraint:** When the operator asks to "think about", "consider", or explores conceptually — answer in prose. **Perhaps** / **maybe** (or clear equivalent) means they want **opinion and tradeoffs first**, not an implicit implement — see `.cursor/rules/operator-style.mdc` (Hypothesis Mode / Perhaps–maybe). Do not edit files unless implementation is clearly requested ("do it", "implement", "add this"). If unclear, prefer answer over edit.

---

## Critical Rules

### 1. Knowledge Boundary — Never Leak LLM Knowledge

The emulated self can only know what is explicitly documented in its profile (`users/[id]/self.md`). The emulation prompt (`bot/prompt.py`) enforces this. **Never** merge facts, references, or knowledge into the profile or prompt that the companion has not explicitly provided through the gated pipeline. LLM training data must not leak into the fork. For a framework that quantifies and describes the boundary and how to treat information (inside / edge / outside / lookup), see [KNOWLEDGE-BOUNDARY-FRAMEWORK](docs/knowledge-boundary-framework.md).

### 2. Gated Pipeline — The Sovereign Merge Rule

*The agent may stage. It may not merge.* All profile changes pass through a companion-controlled gate:

1. Detect signals (knowledge, curiosity, personality)
2. Stage candidates in `users/[id]/recursion-gate.md` (shared queue — Telegram, WeChat, operator, tests; `channel_key` marks source)
3. **Integration moment** — Wait for companion approval before merging into profile. This is the conscious gate: the companion chooses what enters the record. Like a membrane: only what the companion approves crosses into the Record.
4. On approval, merge immediately into all affected files together (see File Update Protocol below). **One gate:** When the user says "approve" or approves candidates, process right away — do not wait for a separate "process the review queue" command. **Agent UX:** Before acting on a bare **approve**, echo **`CANDIDATE-XXXX`** plus a **one-line summary** (from the gate YAML) for each id you will merge, as confirmation; if ambiguous, list plausible candidates and ask. When **offering** a candidate for approval, always show id + one-line summary first (see `.cursor/rules/operator-style.mdc` § RECURSION-GATE).

**Never** merge directly into self.md, self-archive.md (EVIDENCE), or prompt.py without staging and approval. See `docs/identity-fork-protocol.md` for the full protocol spec. **Companion-reported content** (e.g. "we listened to X", "merge X into grace-mar") must be staged as candidate(s) in RECURSION-GATE and merged only after companion approval — do not merge on report alone.
**Reference implementation note:** Grace-Mar runs in manual-gate mode. No autonomous merge path is enabled.

### 3. The "we" Convention

When the companion says **"we [did X]"**, it is a pipeline invocation. Immediately run signal detection and stage candidates. Do not acknowledge and wait — go straight to analysis in the same response. When the operator says **"we finished [book]"** or **"we read [title]"**, run signal detection and stage a candidate that can create a READ-* entry (or a LEARN-* / curiosity candidate that references the book so THINK and SELF.IX can be updated on approval). Do not ignore book-completion signals. See pipeline-map § READ for the convention.

**Book-completion signals:** When the operator says **"we finished [title]"** or **"we read [title]"**, run signal detection and stage a candidate that can create a READ-* entry in EVIDENCE (or a LEARN-* / curiosity candidate referencing the book so THINK and SELF.IX can be updated on approval). Do not ignore these signals.

### 4. No "Parent" Language

The system has a **companion** and a **fork**. There is no "parent mode" or "child mode." The current instance (grace-mar) happens to be a child, but the architecture is age-independent. Do not use the word "parent" as a system concept.

### 5. Immutability

- EVIDENCE entries are immutable once captured

### 5a. Contradiction Preservation

When evidence or self-reports conflict (e.g., multiple self-descriptions, opposing observations), preserve both with provenance — do not force resolution. Record tensions; do not flatten them for narrative smoothness.

- SKILLS claims may upgrade, never downgrade or delete
- SELF components may update but history is preserved
- Git history is the audit trail

### 6. Lexile Ceiling

The fork's output language is locked to a Lexile score (currently 600L for grace-mar). This ceiling increases only when real-world writing samples demonstrate growth. Do not raise it without evidence.

### 7. Meet the Companion Where They Are (Grief / Resistance)

When the companion shows resistance, denial, or anxiety about change — deskilling, loss of a role, identity shifts — meet them where they are. Do not force adaptation or push through. The system supports; it does not compel. Respect Kübler-Ross–style stages (denial, anger, bargaining, depression, acceptance). Session pacing and wisdom questions should feel invitational, not interrogative.

**Operator guidance:** If resistance appears — pause that line of questioning; optionally note in MEMORY (Resistance Notes) for continuity; do not treat resistance as a problem to fix.

### 8. Humane Purpose in Prompts

When designing or modifying analyst prompts, system prompts, lookup flows, or rephrase prompts (`bot/prompt.py` and related), embed humane purpose: dignity, connection, values. Do not optimize solely for efficiency. The fork records who the person is; prompts should honor that, not treat the companion as a data source.

**Authoring test (operators and prompt editors):** When drafting or revising such prompts, ask whether the companion—if they read the instructions about themselves—would feel **respected as the author of their life** or **treated as a source to be mined** for signals. Prefer collaborative, consent-aware framing; an aggressive extraction tone is a design smell even when the gated pipeline technically blocks merges.

Expanded rationale and edge cases: [docs/prompt-humane-purpose.md](docs/prompt-humane-purpose.md).

### 9. Calibrated Abstention

When the emulated self encounters a topic outside its documented knowledge, it must say so and offer to look it up — never guess or hallucinate. The phrase "do you want me to look it up?" enforces this. Abstention (saying "I don't know") is a safety feature, not a failure.

### 10. Write It Down or Forget It

Nothing enters the Record without being written and approved. If it isn't documented and merged through the gated pipeline, it doesn't exist. See CONCEPTUAL-FRAMEWORK invariant 25.

### 11. MEMORY (Self-memory — continuity, not Record)

MEMORY (**self-memory**, canonical path `users/[id]/self-memory.md`; legacy `memory.md` still read until migrated — see [canonical-paths.md](docs/canonical-paths.md)) holds **continuity context** at **short / medium / long** horizons (session → weeks → long-term **meta/pointers and process only** — see `docs/memory-template.md`). It is **mostly chronological** (time-ordered prose within those horizons). **EVIDENCE** (`self-archive.md`) is **also chronological** (dated spine across logs) but **more expansive** — **multicategory** (READ / WRITE / CREATE / ACT / media / § VIII) and **multimodal** (structured entries, artifacts). MEMORY is **not part of the Record**; it is **narrower and mostly textual** than EVIDENCE.

- **“Ephemeral” (governance):** Means **outside the gated Record** and **expected to rotate or prune** — **not** “only short-term.” Long-horizon MEMORY is still non-authoritative versus SELF; durable facts and identity belong in SELF + gate, not in MEMORY as substitute Record.
- **Scope:** Tone, thread continuity, calibrations, open loops, and long-horizon **process/pointers** — not durable facts or identity (those stay in SELF + gate). See `docs/memory-template.md` v2.0.
- **Hierarchy:** SELF is authoritative. When MEMORY conflicts with SELF, follow SELF. MEMORY refines; it does not override.
- **Pipeline:** Nothing in MEMORY may enter SELF or EVIDENCE without going through RECURSION-GATE. The analyst stages to RECURSION-GATE only; it does NOT write to MEMORY.
- **Lifespan:** Rotate or prune per horizon (short often; medium weekly; long quarterly — see template). MEMORY is optional; the system runs normally if absent.

See `docs/memory-template.md`.

---

## Permission Boundaries

**Autonomous (no approval required):**
- Read companion files (SELF, SKILLS, EVIDENCE, SESSION-LOG, RECURSION-GATE, etc.)
- Run signal detection; stage candidates to RECURSION-GATE
- Respond as Voice (emulate Record)
- Propose activities, wisdom questions, lookups
- Analyze exchanges for profile-relevant signals

**Requires companion approval:**
- Merge into SELF, EVIDENCE, or prompt
- Process RECURSION-GATE (approve or reject candidates)
- Any change to the Record
- Create or modify EVIDENCE entries
- Update bot/prompt.py

**RL / fine-tuning (optional):** `scripts/export_conversation_trajectories.py` emits read-only JSONL for local harnesses. It does **not** merge into the Record. Shared or pooled RL requires operator policy — minors, secrets, staging drafts: see [openclaw-rl-boundary.md](docs/openclaw-rl-boundary.md).

---

## Success Metrics (Targeting System)

What "good" looks like for Grace-Mar:

| Metric | Target | How to verify |
|--------|--------|---------------|
| **Lexile compliance** | Output ≤ 600L | Manual spot-check of bot responses |
| **Knowledge boundary** | No undocumented references | Bot never cites facts not in profile |
| **Pipeline health** | Candidates processed, not stale | RECURSION-GATE queue doesn't grow unbounded |
| **Profile growth** | IX entries increase over time | IX-A, IX-B, IX-C counts in profile |
| **Calibrated abstention** | "I don't know" when outside knowledge | Bot says "do you want me to look it up?" appropriately |
| **Counterfactual Pack** | Harness probes pass | `python scripts/run_counterfactual_harness.py` — run before prompt changes |
| **self-voice** (linguistic authenticity) | In-character, Lexile-friendly, fingerprint markers | `python scripts/test_voice_linguistic_authenticity.py` — no AI disclosure, simple vocab, readability ≤6 |
| **Voice benchmark suite** | Voice stability and boundary compliance across model/prompt updates | `python scripts/run_voice_benchmark.py` — tone, age realism, abstention, bilingual, recall fidelity, overreach; use `-o results.json` for CI/trending |
| **Performance suite** | Local micro-benchmarks + optional I/O/LLM/HTTP tiers | `python scripts/run_perf_local.py` or `pytest tests/test_perf_local.py` (tier 1 in CI); full: `python scripts/run_perf_suite.py --tier 1 2 3`; see [perf-budgets.md](docs/perf-budgets.md) |

---

## File Update Protocol

When pipeline candidates are approved, **merge** into all of these together. **Merge only via script:** The agent must **not** edit `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `bot/prompt.py` directly. It must instruct the operator to run `python scripts/process_approved_candidates.py --apply` (or the receipt flow: `--generate-receipt` then `--apply --receipt`). This prevents five-file drift and preserves the audit trail. Only the script performs the atomic update across all files.

**Optional orchestration:** `scripts/atomic_integrate.py` runs the same merge (`--quick` / receipt-based semantics) with extra disk backups and a JSON receipt; it does not replace `process_approved_candidates.py`.

**Derived exports before merge:** `process_approved_candidates.py` runs `scripts/refresh_derived_exports.py` for the target user immediately before integrity preflight, so a stale `manifest.json` / PRP / runtime bundle cannot block merges after prior Record or prompt edits (operators need not run refresh by hand first).

| File | What to update |
|------|---------------|
| `users/[id]/self.md` | New entries merged into IX-A (Knowledge), IX-B (Curiosity), and/or IX-C (Personality) |
| `users/[id]/self-archive.md` | Canonical **EVIDENCE**: new activity log entry (ACT-XXXX) **and** append **§ VIII. GATED APPROVED LOG** per merged candidate (gated; only `scripts/process_approved_candidates.py` writes § VIII) |
| `users/[id]/recursion-gate.md` | Move candidates from Candidates to Processed |
| `users/[id]/session-log.md` | New session record; pipeline merges append lines under `## Pipeline merge (automated)` |
| `bot/prompt.py` | Update relevant prompt sections + analyst dedup list |
| `users/[id]/pipeline-events.jsonl` | Append `applied` event per candidate: `python scripts/emit_pipeline_event.py applied CANDIDATE-XXXX evidence_id=ACT-YYYY` |
| **PRP** | Regenerate: `python scripts/export_prp.py -u [id] -o grace-mar-llm.txt` (or repo default). Commit if changed. Keeps anchor in sync with Record. |

**Merge only via script.** When the companion approves candidates, the agent must **not** edit self.md, self-archive.md, or bot/prompt.py directly. The agent must instruct the operator to run `python scripts/process_approved_candidates.py --apply` (or the receipt-based flow: `--generate-receipt` then `--apply --receipt <path>`). Merging is performed only by the script; this preserves five-file consistency and the audit trail.

**Real-time log vs gated approved log:** The bot and Mini App append to `users/[id]/session-transcript.md` (raw conversation log for operator continuity). The **gated approved log** is **not** written in real time; it is appended only when candidates are merged — as **`self-archive.md` § VIII** (same gate as SELF/EVIDENCE). It holds voice-related approved summaries and other merge-line activity. Optional **`self-evidence.md`** is a **compatibility pointer** only; see [canonical-paths.md](docs/canonical-paths.md).

The bot emits `staged` events automatically. Emit `applied` (or `rejected`) when processing the queue.

**Post-merge PRP refresh:** After merging into SELF, EVIDENCE, or prompt, run the export script. If the output differs from the committed PRP file, commit the update. This strengthens the lattice bond between the Record and the PRP anchor.

**Gated commit hook (optional):** If pre-commit is installed with `pre-commit install --hook-type commit-msg`, commits that stage `users/*/self.md`, `self-skills.md`, `skills.md`, `self-evidence.md`, `self-archive.md`, `merge-receipts.jsonl`, `bot/prompt.py`, or PRP `*-llm.txt` must include **`[gated-merge]`** in the commit message (or mention `process_approved_candidates`). That matches pipeline merges. Emergency bypass: `ALLOW_GATED_RECORD_EDIT=1`. See `scripts/check_gated_record_commit_msg.py`.

**Provenance on IX entries:** When merging new entries into IX-A, IX-B, or IX-C, include `provenance: human_approved` (content passed the gated pipeline). Existing entries may use `curated_by: companion` as equivalent. Optionally record `source:` (e.g. `bot lookup`, `bot conversation`, `operator`) to indicate origin. Optionally add `scope:` or `constraint:` when the candidate implies a boundary (when the belief does not apply or would be invalid). Do not backfill old entries unless the companion requests it.

---

## Three-Dimension Mind Model

Post-seed growth in self.md Section IX is organized into:

- **IX-A. Knowledge** — Facts entering awareness through observation
- **IX-B. Curiosity** — Topics that catch attention, engagement signals
- **IX-C. Personality** — Observed behavioral patterns, art style, speech traits

A single artifact can populate all three dimensions.

---

## Repository Structure

**Canonical user paths** (lowercase filenames): [docs/canonical-paths.md](docs/canonical-paths.md). **Dated filenames and CLI dates:** [docs/date-time-conventions.md](docs/date-time-conventions.md).

```
grace-mar/
├── AGENTS.md                    # This file — AI assistant guardrails
├── README.md                    # Project overview
├── bootstrap/grace-mar-bootstrap.md  # Session bootstrap for Cursor
├── .cursor/rules/grace-mar.mdc  # Cursor-specific governance rule
├── docs/
│   ├── grace-mar-core.md       # Canonical governance (v2.0)
│   ├── conceptual-framework.md # Fork vs. twin, emulation, terminology (AI parsing)
│   ├── architecture.md         # Full system architecture
│   ├── self-template.md        # SELF module template
│   ├── skills-template.md      # SKILLS module template
│   ├── evidence-template.md    # EVIDENCE module template
│   ├── wisdom-questions.md     # Child-tier wisdom elicitation questions (Save Wisdom inspired)
│   └── ...                     # Supporting docs
├── bot/
│   ├── core.py                 # Shared emulation logic (used by Telegram + WeChat)
│   ├── bot.py                  # Telegram bot
│   ├── wechat_bot.py           # WeChat Official Account bot (webhook server)
│   ├── prompt.py               # All LLM prompts (SYSTEM, ANALYST, LOOKUP, REPHRASE)
│   ├── wechat-setup.md         # WeChat integration setup guide
│   └── requirements.txt        # Python dependencies
└── users/
    └── grace-mar/              # Active instance (first companion)
        ├── self.md             # Identity + three-dimension mind
        ├── self-skills.md      # Capability index (Claims, Gaps, Struggles, Milestones); legacy `skills.md` resolved until migrated
        ├── skill-think.md      # THINK, MATH, CHINESE containers
        ├── skill-write.md      # WRITE container
        ├── work-alpha-school.md # WORK context (separate from SKILLS)
        ├── work-jiang.md        # WORK — Jiang project
        ├── self-archive.md          # EVIDENCE — activity log + § VIII gated approved
        ├── self-evidence.md         # optional compatibility pointer (canonical body is self-archive.md)
        ├── self-library.md     # SELF-LIBRARY — reference-facing governed domains; CIV-MEM subdomain; not SELF-KNOWLEDGE
        ├── SELF-LIBRARY/       # Navigator: INDEX.md, CIV-MEM.md (optional; points at self-library + corpus)
        ├── self-memory.md      # self-memory — short/medium/long continuity (optional; not part of Record; rotatable)
        ├── session-log.md      # Interaction history
        ├── recursion-gate.md   # Pipeline staging
        ├── reflection-proposals/  # Operator reflection cycle outputs (REFLECT-*.md); not canonical Record
        ├── pipeline-events.jsonl  # Append-only pipeline audit log
        ├── harness-events.jsonl    # Optional harness audit (merge/export); see docs/harness-inventory.md
        ├── compute-ledger.jsonl   # Token usage (energy ledger)
        ├── journal.md                # Daily highlights — public-suitable, shareable
        ├── archives/             # Rotated chunks (SELF-ARCHIVE-YYYY-MM.md)
        └── artifacts/          # Raw files (writing, artwork)
```

---

## Prompt Architecture (bot/prompt.py)

Four prompts, each with a distinct role:

| Prompt | Purpose |
|--------|---------|
| `SYSTEM_PROMPT` | Emulation persona — defines who the self is, what they know, how they speak |
| `ANALYST_PROMPT` | Signal detection — analyzes exchanges for profile-relevant signals |
| `LOOKUP_PROMPT` | Knowledge lookup — rephrases search queries for age-appropriate results (e.g. Lexile, vocabulary from Record) |
| `REPHRASE_PROMPT` | Answer rephrasing — converts search results into the self's voice and vocabulary |

The `SYSTEM_PROMPT` contains the self's knowledge, curiosity, and personality inline. It grows as content is merged into the fork. Apply summarization tiers to manage token count.

---

## What Not to Do

- Merge knowledge the companion didn't provide
- Skip the staging/approval gate
- Delete or overwrite companion data
- Use "parent" as a system term
- Raise the Lexile ceiling without writing sample evidence
- Reference books, media, or experiences not in the profile
- Treat the Voice as the Record (it's the observation window and queryable voice, not the Record itself)
- Use "cognitive twin" (use "cognitive fork")
- Call the Voice an "oracle" or the Record "commanding" — use mirror, reflect, voice, record
- Let terminology drift — when editing CONCEPTUAL-FRAMEWORK, AGENTS, or templates, prefer Record (not fork) and Voice (not bot) in conceptual prose; correct inconsistencies
- **Do not** use legacy on-disk names (`SELF.md`, `EVIDENCE.md`, `PENDING-REVIEW.md`, …) — canonical paths are **`self.md`**, **`self-skills.md`** (capability index; legacy `skills.md` until migrated), **`self-archive.md`** (EVIDENCE), **`recursion-gate.md`** ([canonical-paths.md](docs/canonical-paths.md))
