# Instance Doctrine — grace-mar

> Instance-specific operating rules for the grace-mar companion fork. This file is **Layer 2** in the [four-layer instruction architecture](../../docs/layer-architecture.md). Core doctrine lives in [AGENTS.md](../../AGENTS.md); this file may narrow but never contradict it.

---

## Operating Modes

Distinct modes govern what the agent may do. Avoid mixing them.

| Mode | Purpose | Agent behavior |
|------|---------|----------------|
| **Session** | Interactive conversation with companion | Respond as Voice; propose activities. Do not merge. Do not stage unless "we [did X]" triggers pipeline. |
| **Pipeline** | Process staged candidates | Detect signals, stage to RECURSION-GATE, or on approval instruct operator to run `process_approved_candidates.py --apply` (do not edit SELF/EVIDENCE/prompt directly). See [OPERATOR-WEEKLY-REVIEW](../../docs/operator-weekly-review.md) for recommended rhythm. |
| **Query** | Browse or answer questions about the Record | Read-only. Report what is documented. Do not edit. |
| **Maintenance** | End-of-day consolidation (`dream`) | Run `scripts/auto_dream.py` — normalize self-memory, check integrity and governance, refresh contradiction digest, emit pipeline event. Read-only with respect to the Record; may write to self-memory and derived artifacts. No merge authority. See `.cursor/skills/dream/SKILL.md`. |

When in doubt, default to Session (conversational, no merges).

**Implementation preference:** The operator prefers to see a short proposal (scope, approach, files to touch) before the agent implements. Propose first; implement after approval.

**Proposal format:** One paragraph with: (1) Scope — what's in, what's out; (2) Approach — high-level steps or method; (3) Files — paths to create or modify. Trivial fixes (typos, obvious corrections) may skip proposal.

**Edit restraint:** When the operator asks to "think about", "consider", or explores conceptually — answer in prose. **Perhaps** / **maybe** (or clear equivalent) means they want **opinion and tradeoffs first**, not an implicit implement — see `.cursor/rules/operator-style.mdc` (Hypothesis Mode / Perhaps–maybe). Do not edit files unless implementation is clearly requested ("do it", "implement", "add this"). If unclear, prefer answer over edit.

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
| **Continuity fidelity** | Bridge round-trip >= 80% | `python scripts/test_bridge_continuity.py` or `pytest tests/test_bridge_continuity.py` — no LLM needed; run before bridge format changes |
| **Performance suite** | Local micro-benchmarks + optional I/O/LLM/HTTP tiers | `python scripts/run_perf_local.py` or `pytest tests/test_perf_local.py` (tier 1 in CI); full: `python scripts/run_perf_suite.py --tier 1 2 3`; see [perf-budgets.md](../../docs/perf-budgets.md) |
| **Judgment probes** | Voice makes value-aligned choices under ambiguity, reflects IX-C tensions | `python scripts/run_judgment_probes.py` — 8 probes targeting documented personality tensions; committed/trait_aligned/tension_preserved/age_appropriate scoring; use `-o results.json` for trending |
| **Identity delta** | Profile changes do not degrade Voice quality | `python scripts/eval_identity_delta.py -u grace-mar` — runs judgment + voice benchmarks, computes deltas against saved baseline; run after gate merges |

---

## File Update Protocol

When pipeline candidates are approved, **merge** into all of these together. **Merge only via script:** The agent must **not** edit `self.md`, `self-archive.md`, `recursion-gate.md`, `session-log.md`, or `bot/prompt.py` directly. It must instruct the operator to run `python scripts/process_approved_candidates.py --apply` (or the receipt flow: `--generate-receipt` then `--apply --receipt`). This prevents five-file drift and preserves the audit trail. Only the script performs the atomic update across all files.

**Optional orchestration:** `scripts/atomic_integrate.py` runs the same merge (`--quick` / receipt-based semantics) with extra disk backups and a JSON receipt; it does not replace `process_approved_candidates.py`.

**Derived exports before merge:** `process_approved_candidates.py` runs `scripts/refresh_derived_exports.py` for the target user immediately before integrity preflight, so a stale `manifest.json` / PRP / runtime bundle cannot block merges after prior Record or prompt edits (operators need not run refresh by hand first).

| File | What to update |
|------|---------------|
| `users/grace-mar/self.md` | New entries merged into IX-A (Knowledge), IX-B (Curiosity), and/or IX-C (Personality) |
| `users/grace-mar/self-archive.md` | Canonical **EVIDENCE**: new activity log entry (ACT-XXXX) **and** append **§ VIII. GATED APPROVED LOG** per merged candidate (gated; only `scripts/process_approved_candidates.py` writes § VIII) |
| `users/grace-mar/recursion-gate.md` | Move candidates from Candidates to Processed |
| `users/grace-mar/session-log.md` | New session record; pipeline merges append lines under `## Pipeline merge (automated)` |
| `bot/prompt.py` | Update relevant prompt sections + analyst dedup list |
| `users/grace-mar/pipeline-events.jsonl` | Append `applied` event per candidate: `python scripts/emit_pipeline_event.py applied CANDIDATE-XXXX evidence_id=ACT-YYYY` |
| **PRP** | Regenerate: `python scripts/export_prp.py -u grace-mar -o grace-mar-llm.txt` (or repo default). Commit if changed. Keeps anchor in sync with Record. |

**Real-time log vs gated approved log:** The bot and Mini App append to `users/grace-mar/session-transcript.md` (raw conversation log for operator continuity). The **gated approved log** is **not** written in real time; it is appended only when candidates are merged — as **`self-archive.md` § VIII** (same gate as SELF/EVIDENCE). It holds voice-related approved summaries and other merge-line activity. Optional **`self-evidence.md`** is a **compatibility pointer** only; see [canonical-paths.md](../../docs/canonical-paths.md).

The bot emits `staged` events automatically. Emit `applied` (or `rejected`) when processing the queue.

**Post-merge PRP refresh:** After merging into SELF, EVIDENCE, or prompt, run the export script. If the output differs from the committed PRP file, commit the update.

**Gated commit hook (optional):** If pre-commit is installed with `pre-commit install --hook-type commit-msg`, commits that stage `users/*/self.md`, `self-skills.md`, `skills.md`, `self-evidence.md`, `self-archive.md`, `merge-receipts.jsonl`, `bot/prompt.py`, or PRP `*-llm.txt` must include **`[gated-merge]`** in the commit message (or mention `process_approved_candidates`). Emergency bypass: `ALLOW_GATED_RECORD_EDIT=1`. See `scripts/check_gated_record_commit_msg.py`.

**Provenance on IX entries:** When merging new entries into IX-A, IX-B, or IX-C, include `provenance: human_approved` (content passed the gated pipeline). Existing entries may use `curated_by: companion` as equivalent. Optionally record `source:` (e.g. `bot lookup`, `bot conversation`, `operator`) to indicate origin. Optionally add `scope:` or `constraint:` when the candidate implies a boundary. Optionally add `warrant:` — the unstated assumption that, if changed, would mean this entry should be revisited (e.g. "holds while limited self-regulation strategies are in use"). Omit for straightforward facts or stable preferences with no expiration condition. Do not backfill old entries unless the companion requests it.

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

## Repository Structure

**Canonical user paths** (lowercase filenames): [docs/canonical-paths.md](../../docs/canonical-paths.md). **Dated filenames and CLI dates:** [docs/date-time-conventions.md](../../docs/date-time-conventions.md).

```
grace-mar/
├── AGENTS.md                    # Core doctrine (Layer 1)
├── README.md                    # Project overview
├── bootstrap/grace-mar-bootstrap.md  # Session bootstrap for Cursor
├── .cursor/rules/grace-mar.mdc  # Cursor-specific governance rule
├── docs/
│   ├── grace-mar-core.md       # Canonical governance (v2.0)
│   ├── conceptual-framework.md # Fork vs. twin, emulation, terminology (AI parsing)
│   ├── architecture.md         # Full system architecture
│   ├── layer-architecture.md   # Four-layer instruction model
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
        ├── instance-doctrine.md  # Instance-specific operating rules (Layer 2)
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
        ├── self-history.md     # Derived dual log: WORK aggregate + gate-approved companion thread (optional; not Record)
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

## Instance-specific terminology

- **Do not** use legacy on-disk names (`SELF.md`, `EVIDENCE.md`, `PENDING-REVIEW.md`, …) — canonical paths are **`self.md`**, **`self-skills.md`** (capability index; legacy `skills.md` until migrated), **`self-archive.md`** (EVIDENCE), **`recursion-gate.md`** ([canonical-paths.md](../../docs/canonical-paths.md))
