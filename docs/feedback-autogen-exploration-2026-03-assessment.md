# Assessment: AutoGen / Multi-Agent Exploration Feedback (2026-03)

**Source:** [feedback-autogen-exploration-2026-03.md](feedback-autogen-exploration-2026-03.md)  
**Assessed:** 2026-03 — verification against repo anchors, invariant alignment, recommendation, risks.

---

## 1. Verification of "current grace-mar" description

The feedback’s summary table (SELF, SELF-LIBRARY, SKILLS, EVIDENCE + recursion-gate) was checked against `docs/architecture.md`, `docs/conceptual-framework.md`, and `AGENTS.md`.

| Feedback claim | Repo anchor | Verdict |
|----------------|-------------|--------|
| **SELF:** IX-A/B/C as "immutable core identity" | architecture.md (SELF + SELF-KNOWLEDGE, IX-A/B/C); conceptual-framework (Record evolves via merge); agents.md (gate, history preserved) | **Mostly correct, one nuance:** SELF is the governed *core* of identity and does not change without the gate. It is not literally immutable: it evolves through approved merges with history preserved (conceptual-framework, agents.md §5a). Prefer wording: "governed core identity" or "identity that only changes through the gate." |
| **SELF-LIBRARY:** including CIV-MEM as read-only reference | architecture.md (Module 1b, SELF-LIBRARY, CIV-MEM subdomain); boundary-self-knowledge-self-library | **Correct.** Reference-facing, not identity; CIV-MEM is a sub-library for lookup. |
| **SKILLS:** THINK/WRITE as capability modules | architecture.md (SKILLS); conceptual-framework (self-skill-think, self-skill-write); skills-modularity | **Correct.** |
| **EVIDENCE + recursion-gate:** controlled evolution; no emergent drift; changes require explicit user/operator approval | agents.md §2 (Sovereign Merge Rule: stage only, no merge without approval); architecture (explicit non-goals: no merge without companion approval); CONTRADICTION-ENGINE-SPEC §2 | **Correct.** |

**Phase 7 / emergent cognition:** Confirmed. Wording appears in `readme.md`, `grace-mar-bootstrap.md`, `development-handoff.md`, `session-log.md`: "moment of cognitive bifurcation," "emergent cognition" (not "emergent consciousness"). Fork has graduated from pure seeding to growth-through-use; Record + Voice operate as a coherent presence from the system.

**Analyst prompts, PRP, export manifest:** Confirmed. Analyst stages to RECURSION-GATE only (agents.md); export scripts produce read-only artifacts (PRP, manifest); no merge path from exports. AutoGen as consumer of export would be read-only at runtime unless a separate, gated staging step is defined.

---

## 2. Exploration paths vs. Sovereign Merge Rule, knowledge boundary, CONTRADICTION-ENGINE-SPEC §2

**Sovereign Merge Rule (agents.md §2):** Agent may stage; it may not merge. All profile changes require staging then companion approval; merge only via `process_approved_candidates.py --apply`.

**Knowledge boundary (agents.md §1):** Only documented profile content; no LLM leakage; no merge of undocumented knowledge.

**CONTRADICTION-ENGINE-SPEC §2:** Agent may stage, may not merge; `recursion-gate.md` is canonical; no second source of truth; contradiction flow = staged candidate + derived analysis + operator resolution + deterministic merge.

### Path 1: Internal deliberation loop (prototype)

- **Description:** Small AutoGen GroupChat (e.g. Guardian, Validator, Explorer, Writer) ingesting `self.md` + recent `recursion-gate.md`; output → staged markdown for user review (no auto-apply).
- **Write to Record?** **No.** By design, output is "staged markdown for user review" — i.e. proposed content. Any entry into the Record must go through: (1) human review of the output, (2) staging as candidate(s) in `recursion-gate.md`, (3) companion approval, (4) merge via script. The deliberation loop must not call `process_approved_candidates.py` or write to `self.md`, `self-evidence.md`, or `bot/prompt.py`.
- **Staging:** If the prototype produces markdown that the operator (or an existing analyst path) then stages, that is allowed (staging is permitted). Risk: if the *code* auto-appends to `recursion-gate.md` without human review of each proposal, that effectively automates staging. Mitigation: treat deliberation output as *draft*; only a human or an explicit, review-gated step may create candidates in `recursion-gate.md`.
- **Knowledge boundary:** Agents ingest only `self.md` and existing candidates (already in-bound). No new facts from the open web or LLM training; proposals must be traceable to existing Record/candidates. Preserve boundary by disallowing lookups or external knowledge inside the deliberation loop unless they are the same lookup path used by the Voice (and do not write to SELF).
- **CONTRADICTION-ENGINE-SPEC §2:** Deliberation can implement "derived contradiction analysis" and suggest resolutions; the queue remains `recursion-gate.md`, resolution remains operator, merge remains deterministic and human-gated. No second source of truth if the loop only produces drafts that become candidates via the existing queue.

**Verdict:** Compliant provided: (1) no merge path in code, (2) staging only after human review of deliberation output, (3) no new knowledge sources inside the loop.

---

### Path 2: Runtime consumption experiment

- **Description:** Export fork manifest; AutoGen `ConversableAgent` with system prompt from `grace-mar-llm.txt`; short sessions (e.g. Telegram wrapper); agent "embodies" Grace-Mar, queries SELF-LIBRARY read-only; log outputs as EVIDENCE candidates into existing pipeline.
- **Write to Record?** **No**, if "log outputs as EVIDENCE candidates" means: create candidate(s) that are then staged (e.g. in `recursion-gate.md`) and merged only after companion approval. The runtime must not write to `self.md`, `self-evidence.md`, or `prompt.py`; it may only produce data that the existing pipeline turns into staged candidates.
- **Staging:** Who stages matters. If the runtime (or a script) pushes every turn into `recursion-gate.md` without per-session or per-item human review, that is automated staging. Acceptable only if policy explicitly allows batch staging with later human review (as with analyst today). Prefer: runtime writes to a log or inbox; operator or analyst reviews and stages selected outcomes as candidates.
- **Knowledge boundary:** Agent uses PRP + SELF-LIBRARY read-only — consistent. No new knowledge may be merged unless it came from companion-approved content (e.g. lookup results already scoped by Record). Session outputs that become candidates must be traceable to approved sources or to companion-reported events ("we did X").
- **CONTRADICTION-ENGINE-SPEC §2:** No conflict. Candidates from the runtime are just another source; they still live in the same queue and merge path.

**Verdict:** Compliant provided: (1) no merge path in the runtime, (2) staging policy is explicit (who stages, how often), (3) instance use is with companion consent (invariant 34).

---

### Path 3: Contradiction Engine + agent reflection

- **Description:** Model CONTRADICTION-ENGINE-SPEC as AutoGen critique loop: propose → detect conflicts → suggest resolutions → then gate. All before merge.
- **Write to Record?** **No.** "Then gate" and "all before merge" mean: the loop produces proposals and conflict/resolution suggestions; the operator resolves; merge is unchanged and human-only. The agent loop is a "derived contradiction analysis" (CONTRADICTION-ENGINE-SPEC §2); it does not replace the canonical queue or merge.
- **CONTRADICTION-ENGINE-SPEC §2:** Aligned. (1) Canonical staged candidate in queue; (2) derived contradiction analysis object — the AutoGen loop implements this; (3) explicit operator resolution; (4) deterministic merge into canonical files. No second source of truth if the loop only reads from the queue and writes derived artifacts (e.g. conflict reports), not a parallel queue.

**Verdict:** Compliant; fits the spec as an implementation of the derived-analysis step.

---

### Summary: Can any path write to the Record without the gate?

| Path | Can write to Record without gate? | Condition to keep it so |
|------|-----------------------------------|---------------------------|
| 1 – Deliberation loop | No | No merge in code; staging only after human review of output; deliberation output is draft only. |
| 2 – Runtime consumption | No | No merge in runtime; staging via existing pipeline; companion consent for instance. |
| 3 – Contradiction + agent reflection | No | Loop only produces derived analysis; resolution and merge stay with operator and script. |

**Conclusion:** None of the three paths may write to the Record without the gate, provided implementations follow the conditions above and no AutoGen code path ever calls the merge script or edits Record files directly.

---

## 3. Recommendation

**Recommendation: (a) design-only doc, with (b) minimal prototype optional and tightly scoped.**

- **(a) Design-only doc**  
  - Add a short design doc that captures: the comparison (current grace-mar vs AutoGen style), the three exploration paths, and the **invariant constraints** (no write to Record; staging only after human review or explicit policy; no second source of truth; CONTRADICTION-ENGINE-SPEC §2).  
  - **Location:** Prefer a dedicated exploration doc, e.g. `docs/exploration-multi-agent-deliberation.md`, so it is easy to find and clearly "exploration" not production. Alternative: a subsection in `docs/design-notes.md` or a doc under `docs/skill-work/work-dev/` if the focus is work-dev context. **Recommended:** `docs/exploration-multi-agent-deliberation.md` (new), with a pointer from `docs/design-notes.md` or the feedback doc.

- **(b) Minimal prototype (optional)**  
  - If a prototype is desired, limit it to **Path 1 (internal deliberation loop)** as the most contained: read-only ingest of `self.md` + recent `recursion-gate.md`; output = markdown only; no writes to repo Record or gate.  
  - **Where:** Under a clearly experimental path, e.g. `scripts/exploration/` or `exploration/autogen-deliberation/` at repo root, with a README stating it is exploration, not part of the core pipeline. Do not add AutoGen to `bot/` or to `scripts/process_approved_candidates.py`.  
  - **How:** Single script or small module that (1) loads self.md + optional recursion-gate snippet, (2) runs a small GroupChat (or equivalent) with fixed roles, (3) prints or writes to a **non-canonical** file (e.g. `exploration/output/deliberation-draft-YYYYMMDD.md`) for operator review. Staging into `recursion-gate.md` remains a separate, manual or existing pipeline step.

- **(c) Defer**  
  - Defer if the goal is zero new dependencies and no extra moving parts. The feedback is still useful as an assessed handoff; the design-only doc preserves the option to implement later.

**Where the design doc should live:** `docs/exploration-multi-agent-deliberation.md` (new). Optionally link from `docs/design-notes.md` and from `docs/feedback-autogen-exploration-2026-03.md` ("Assessment and design capture: …").

---

## 4. Concrete risks and how to keep them bounded

| Risk | Description | How to keep bounded |
|------|-------------|----------------------|
| **Identity bleed** | Deliberation or runtime agents are perceived as "the" Record or Voice; their output is merged without clear provenance; council voices blur with the companion’s documented self. | (1) All deliberation/runtime output labeled as "proposed" / "candidate" / "draft"; (2) merge only via `process_approved_candidates.py`; (3) no AutoGen (or any new layer) in the merge script or in direct edits to Record files; (4) provenance on merged content (e.g. `source: autogen_deliberation` or `runtime_experiment`) so identity remains traceable. |
| **Dependency creep** | AutoGen (or similar) becomes required for the core pipeline, harness, or release. | (1) Treat AutoGen as **optional/experimental**; (2) core pipeline (`bot/`, analyst, `process_approved_candidates.py`, recursion-gate) has **zero** AutoGen imports; (3) exploration lives in a separate dir/script; (4) docs and README state that the exploration is not required for operation. |
| **Scope creep** | Prototype or design is treated as production; exploration logic moves into the gate or the bot. | (1) Keep exploration in a dedicated area (`docs/exploration-*.md`, `scripts/exploration/` or `exploration/`); (2) label all exploration docs and code as "exploration" / "experimental"; (3) do not integrate deliberation or AutoGen into `bot/`, `scripts/process_approved_candidates.py`, or recursion-gate logic without an explicit design change and approval. |

**Additional risk — staging volume (Path 2):** If the runtime stages aggressively, the queue can grow and dilute review quality. **Mitigation:** Define a staging policy (e.g. operator reviews session log and stages only selected outcomes; or batch staging with explicit "review before merge" and optional caps).

---

## 5. Summary

- The feedback’s "current grace-mar" description is **accurate** except the word "immutable" for SELF; prefer "governed core identity."
- All three exploration paths **can** be implemented without writing to the Record past the gate, provided the implementation rules in §2 are followed.
- **Recommendation:** Add a **design-only** doc at `docs/exploration-multi-agent-deliberation.md`; optionally implement a **minimal prototype** for Path 1 in an exploration-only area with no merge path and no core dependency.
- **Risks** (identity bleed, dependency creep, scope) are bounded by: no merge in exploration code, optional/isolated AutoGen, and explicit "exploration" scope and labeling.
