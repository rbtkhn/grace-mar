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
- **Ephemeral / session:** `memory.md`, chat — **not** Record truth until merged through the gate.

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

## Checklist artifact (machine-readable)

- **[agent-surface-template.yaml](agent-surface-template.yaml)** — three axes (runtime, orchestration, interface) plus **Grace-Mar** trust fields (Record authority, staging, gate, continuity).
- **CLI:** `python scripts/work_dev/agent_surface_checklist.py` prints the template; `--validate path.yaml` checks required keys.

---

## Cross-references

- [session-continuity-contract.md](session-continuity-contract.md) — continuity is explicit, not “the agent remembers.”
- [workspace.md](workspace.md) — operator entrypoint and file map.
- [three-compounding-loops.md](three-compounding-loops.md) — Record vs WORK vs CI; drafts must not become canon.
- [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md) — one-loop export → stage → merge.
- [openclaw-integration.md](../../openclaw-integration.md) — full integration guide.
- [runtime/observability/README.md](../../../runtime/observability/README.md) — JSONL feeds and producers.

---

*Informed by industry discourse on enterprise agent adoption: environments and engineering basics compound; hype without structure does not.*
