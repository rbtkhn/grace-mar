# Agentic environment principles (work-dev)

**Purpose:** A short, in-repo framing for operators: **identity continuity and safe agent use come from the repo and policy surface**, not from a “smarter” model. Use this when debugging integrations, handback, or OpenClaw-adjacent work.

---

## 1. Reframe the sell

- **Not:** “We need a better agent / prompt.”
- **Yes:** **Data + policy + measurement** for **identity continuity**: canonical files, lanes, gate, continuity receipts, observability feeds.

The integration is **environment engineering** first. Models sit on top of that.

---

## 2. Default debug order (environment before prompt)

When something feels wrong in production or staging:

1. **Continuity** — receipt present? TTL? `continuity_read_log` / handback 428 path?
2. **Lane** — changed paths owned by the declared PR lane? (`lanes.yaml`, `check_lane_scope.py`)
3. **Gate** — candidates staged correctly? Provenance fields in YAML blocks?
4. **Observability** — `runtime/observability/*.jsonl`, dashboard counts, harness events?

Only then treat it as **prompt / model** behavior.

---

## 3. “Data dominates” (canonical truth first)

Rob Pike’s rule applies here as: **structure the repo so algorithms (and agents) stay obvious.**

- **Authoritative:** `users/[id]/self.md`, `recursion-gate.md`, `self-evidence.md` (per [AGENTS](../../../AGENTS.md) and the gated pipeline).
- **Non-Record continuity:** `self-memory.md` (short/medium/long horizons; rotatable; legacy `memory.md`), chat — **not** Record truth until merged through the gate.

Clever retrieval does not replace **clean canonical files** and **explicit staging**.

---

## 4. Resist “agent mesh” envy

Highest-leverage moves in this territory stay **boring**:

- Gate hygiene and merge discipline  
- Continuity contract and handback provenance  
- Lane scope and CI  
- Dashboard and observability feeds  

Complex multi-agent topologies are optional; **companion sovereignty + audit trail** are not.

---

## 5. Local-private stacks: three operator rules (a, b, c)

Products that advertise **100% local** models, **Docker** sandboxes, or **chat vs utility vs embedding** splits are still **vendor runtimes**. Grace-Mar stays **repo + gate**. These rules align the two without confusing them.

### (a) Explicit data residency and role split

- **Data residency:** Decide per workload: **repo-only / export bundle** vs **cloud chat**. Sensitive or identity-adjacent work belongs in **files and bounded flows**, not pasted into arbitrary UIs. Use **[agent-surface-template.yaml](agent-surface-template.yaml)** — `runtime.placement` and related fields — when evaluating a new tool.
- **Role split:** Do not collapse **reasoning**, **cheap background work**, and **retrieval** into one undifferentiated “the AI.” In this repo, the bot already separates concerns ([`bot/prompt.py`](../../../bot/prompt.py) — SYSTEM vs ANALYST vs LOOKUP / rephrase). External stacks that expose **chat / utility / embedding** models are the same *idea*: match surface to job so you can **measure** and **audit** each path.

### (b) Bounded execution for anything that can touch the repo or staging

- Prefer **narrow surfaces**: authenticated **handback**, **stage-only** scripts, **lanes** — not “full disk from chat.”
- **Sandboxing** (e.g. containers) for agentic execution is the right *metaphor*: **limit blast radius** if a tool runs code or writes files.
- **work-dev posture:** continuity checks, **428** when receipts are missing, **observability** feeds — **your** operational security story, not the model vendor’s.

### (c) Pipeline discipline — local “memory” is not the Record

- **Vector stores, markdown scratchpads, or long-session agent memory** (local or cloud) are **not** **`self.md`** and **not** evidence until they pass **[AGENTS](../../../AGENTS.md)** pipeline.
- **Nothing** becomes durable identity because an agent “remembered” it offline. **Companion-approved merge** through RECURSION-GATE (and `process_approved_candidates.py`) is the only path into the Record.
- **self-memory** (`self-memory.md`) remains **outside the gated Record** (prunable continuity); **SELF** remains authoritative after merge.

---

## Checklist artifact (machine-readable)

- **[agent-surface-template.yaml](agent-surface-template.yaml)** — three axes (runtime, orchestration, interface) plus **Grace-Mar** trust fields (Record authority, staging, gate, continuity). Optional **`agent_species`**: `coding_harness` | `dark_factory` | `auto_research` | `workflow_orchestration` (do not mix species with the wrong workload).
- **CLI:** `python scripts/work_dev/agent_surface_checklist.py` prints the template; `--validate path.yaml` checks required keys and validates `agent_species` when set.

---

## Cross-references

- [session-continuity-contract.md](session-continuity-contract.md) — continuity is explicit, not “the agent remembers.”
- [workbench/README.md](workbench/README.md) — **artifact execution inspection** for generated UIs, CLIs, and visual outputs (run → inspect → workbench receipt); not Record truth, not a merge path—use before treating generated output as shippable.
- [workspace.md](workspace.md) — operator entrypoint and file map.
- [three-compounding-loops.md](three-compounding-loops.md) — Record vs WORK vs CI; drafts must not become canon.
- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) — one-loop export → stage → merge.
- [openclaw-integration.md](../../openclaw-integration.md) — full integration guide.
- [runtime/observability/README.md](../../../runtime/observability/README.md) — JSONL feeds and producers.
- [managed-agent-design.md](managed-agent-design.md) — persistent-agent lifecycle, operator runbook, steward boundary review.

---

*Informed by industry discourse on enterprise agent adoption: environments and engineering basics compound; hype without structure does not.*
