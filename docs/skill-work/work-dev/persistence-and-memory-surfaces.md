# Persistence and memory surfaces

**Status:** Operator WORK. **Not** Record truth. Template-portable companion-self guidance.

**Purpose:** Map **what persists where** so operators and template adopters do not confuse **vendor chat memory**, **session paste**, **self-memory**, **RECURSION-GATE**, and **merged SELF/EVIDENCE**. Aligns the “outcome agent trap” dimensions (persistent memory, inspectable surfaces, compounding context) with this architecture.

**Related:** [session-continuity-contract.md](session-continuity-contract.md), [three-compounding-loops.md](three-compounding-loops.md), [openclaw-integration.md](../../openclaw-integration.md), [identity-fork-protocol.md](../../identity-fork-protocol.md), [delegation-spec-external-agents.md](delegation-spec-external-agents.md).

---

## Surfaces at a glance

| Surface | What persists | Who writes | Inspectable (files / git)? | Compounds as Record? |
|--------|---------------|------------|----------------------------|----------------------|
| **Merged SELF, EVIDENCE (`self-archive.md`), `bot/prompt.py`** | Canonical identity, activity log, Voice prompt | **Only** via `scripts/process_approved_candidates.py` (or receipt flow) after companion approval | Yes — markdown + git history | **Yes** — Loop 1 |
| **`recursion-gate.md`** | Staged candidates (not yet Record) | Analyst, operators, `openclaw_stage`, integrations — **stage only** | Yes | **No** until approved and merged |
| **`self-memory.md`** | Short/medium/long **continuity** (tone, loops, pointers) | Operator/companion per [memory-template.md](../../memory-template.md); not pipeline output | Yes | **No** — MEMORY is explicitly non-authoritative vs SELF ([AGENTS.md](../../../AGENTS.md)) |
| **Session transcript / chat UI** | Raw conversation (instance-dependent) | Bot/Mini App append | Often yes as a file | **No** — not gated Record |
| **Harness / new thread paste** | Nothing unless saved — ephemeral model context | Human pastes warmup output | N/A | **No** |
| **External outcome agent** (Lindy, Opal, SaaS thread, etc.) | Vendor-controlled memory + artifacts **outside** repo until imported | Third-party product | Varies — often **partial** (final answer only) | **No** — hand back → stage → merge if it should touch Record |
| **WORK markdown** (`docs/skill-work/**`, `work-*.md`) | Drafts, briefs, logs | Operators, scripts that **only** write WORK paths | Yes | **No** — Loop 2 unless promoted through gate |
| **Repo / CI** | Tests, governance scripts | Engineers | Yes | **No** — Loop 3 (machinery), not companion identity |
| **Exports** (PRP, `USER.md`, runtime bundle) | **Read-only** snapshots of Record for tools | `export_prp.py`, `export_user_identity.py`, `export_runtime_bundle.py`, OpenClaw hooks | Yes | N/A — **derived**, refresh after merge |

**Canonical EVIDENCE body:** `users/[id]/self-archive.md` (see [canonical-paths.md](../../canonical-paths.md)). Some docs still mention `self-evidence.md` as a compatibility pointer.

---

## Read vs write for external agents

- **Trusted read sources for identity:** Approved exports + canonical Record files per [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) read order — not “whatever the product remembered last Tuesday.”
- **Trusted write path to Record:** **Stage** to `recursion-gate.md` (or equivalent) → companion **approve** → `process_approved_candidates.py --apply` only.
- **Do not treat vendor thread memory as Record compounding.** If the tool “learns” your preferences, that layer is **not** the Sovereign Merge Rule unless the same content is staged and approved in-repo.

---

## Efficiency note (assumption-labeled)

These are **hypotheses** for operator time saved — not measured defaults. Validate with a short time log if you want real numbers.

| Mechanism | What improves | How to quantify (assumption-labeled) |
|-----------|---------------|--------------------------------------|
| **Clear persistence map** | Less time re-explaining context; fewer mistakes from “the AI remembers” | *If* operators lose ~15–30 min/session to context re-wiring, reducing that **2–4 sessions/month** saves ~**30–120 min/month** (hypothesis). |
| **Binary gate checks** ([`users/_template/recursion-gate.md`](../../../users/_template/recursion-gate.md)) | Fewer bad merges and post-merge repair | *If* one bad merge/month costs ~45–90 min to unwind, cutting incidence **50%** saves ~**22–45 min/month** (hypothesis). |
| **Delegation spec + checkpoints** ([delegation-spec-external-agents.md](delegation-spec-external-agents.md)) | Less black-box delegation rework | *If* a high-stakes task **fully redoes** ~20% of the time at ~1–2 hr each, structured checkpoints target that tail — track **redo rate** before/after. |
| **Loop clarity** ([three-compounding-loops.md](three-compounding-loops.md)) | Less “WORK draft mistaken for Record” cleanup | Qualitative + **incident count** (drafts that reached SELF without gate). |

**Leading indicators (manual, 1–2 months):** time-to-approve typical candidates; “had to revert merge” (yes/no per month); minutes/week on external-agent handoff.
