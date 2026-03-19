# Exploration: Multi-Agent Deliberation (AutoGen-style)

**Status:** Exploration — design and optional prototype. Not part of the core pipeline.  
**Purpose:** Capture a possible evolution of the cognitive fork toward internal multi-agent deliberation while preserving the Sovereign Merge Rule and knowledge boundary.  
**Source:** [feedback-autogen-exploration-2026-03.md](feedback-autogen-exploration-2026-03.md); assessment: [feedback-autogen-exploration-2026-03-assessment.md](feedback-autogen-exploration-2026-03-assessment.md).

---

## 1. Current grace-mar vs AutoGen-style

| Aspect | grace-mar (current) | AutoGen / multi-agent style | Hybrid idea (this exploration) |
|--------|---------------------|-----------------------------|---------------------------------|
| **Core entity** | Single governed fork (Record + Voice) | Swarm of ConversableAgents | Internal “council” agents deliberate *before* the gate; output is draft only |
| **Coordination** | Gated pipeline + companion review | GroupChat / message-passing | Lightweight deliberation → staged markdown for user review (no auto-apply) |
| **Memory / state** | Canonical Markdown + EVIDENCE | Short-term chat + vector stores | Record exported as read-only context; agents do not write to Record |
| **Reflection** | Contradiction Engine spec + session briefs | Critique/refine loops | Propose → critique (vs SELF boundaries) → refine → **then gate** |
| **Determinism** | Very high (gates, validation) | Medium (emergent) | Final integration remains gated; AutoGen used only for pre-proposal ideation |
| **Runtime** | OpenClaw, Telegram, export manifests | Async, tool-calling, code exec | Export manifest + PRP bootstrap agents that read Record only |

**Invariant:** Any future agentic or orchestration layer must keep merge authority human-only (architecture.md; agents.md §2). This exploration respects that: deliberation may suggest; only the companion may approve and merge.

---

## 2. Invariant constraints (MUST preserve)

All exploration paths must preserve:

- **Sovereign Merge Rule (agents.md §2):** Agent may stage; it may not merge. Merge only via `process_approved_candidates.py --apply` after companion approval.
- **Knowledge boundary (agents.md §1):** No LLM knowledge leakage; only documented profile content; no merge of undocumented facts.
- **CONTRADICTION-ENGINE-SPEC §2:** `recursion-gate.md` remains the canonical queue; no second source of truth; contradiction flow = staged candidate + derived analysis + operator resolution + deterministic merge.
- **No write to Record from exploration:** No AutoGen (or any deliberation) code path may write to `self.md`, `self-evidence.md`, `bot/prompt.py`, or call the merge script. Output is **draft**; staging into `recursion-gate.md` is a separate, human-reviewed step.

---

## 3. Three exploration paths

### Path 1: Internal deliberation loop (prototype)

- **Idea:** Small GroupChat-style loop (e.g. Guardian, Validator, Explorer, Writer) with read-only ingest of `self.md` + recent `recursion-gate.md` candidates.
- **Output:** Staged markdown for user review (no auto-apply). Draft written to a non-canonical file (e.g. `exploration/autogen-deliberation/output/deliberation-draft-*.md`).
- **Goal:** Reasoning depth before the gate without losing control.
- **Implementation:** Minimal prototype under `exploration/autogen-deliberation/`; optional dependency on AutoGen; no merge path in code.

### Path 2: Runtime consumption experiment

- **Idea:** Export fork manifest; initialize a ConversableAgent with system prompt from PRP (`grace-mar-llm.txt`); short sessions (e.g. Telegram wrapper); agent queries SELF-LIBRARY read-only.
- **Output:** Session outputs logged as EVIDENCE candidates → fed into **existing** pipeline (operator or analyst stages; companion approves).
- **Constraint:** Runtime must not merge; staging policy (who stages, how often) must be explicit.

### Path 3: Contradiction Engine + agent reflection

- **Idea:** Model CONTRADICTION-ENGINE-SPEC as an AutoGen critique loop: propose → detect conflicts → suggest resolutions → then gate. All before merge.
- **Constraint:** Loop produces derived analysis only; resolution and merge remain with operator and `process_approved_candidates.py`.

---

## 4. Risks and boundaries

| Risk | Mitigation |
|------|------------|
| **Identity bleed** | Label all deliberation output as "proposed" / "draft"; merge only via script; no exploration code in merge path; provenance (e.g. `source: autogen_deliberation`) on any staged content. |
| **Dependency creep** | AutoGen optional; core pipeline has zero AutoGen imports; exploration lives in `exploration/` and is not required for operation. |
| **Scope creep** | Exploration clearly labeled; no integration into `bot/` or `process_approved_candidates.py` without explicit design change and approval. |

---

## 5. Where this lives

- **Design:** This doc (`docs/exploration-multi-agent-deliberation.md`).
- **Prototype (Path 1):** `exploration/autogen-deliberation/` — README + script; output to `exploration/autogen-deliberation/output/`; no writes to Record or gate.
- **Assessment and rationale:** [feedback-autogen-exploration-2026-03-assessment.md](feedback-autogen-exploration-2026-03-assessment.md).
