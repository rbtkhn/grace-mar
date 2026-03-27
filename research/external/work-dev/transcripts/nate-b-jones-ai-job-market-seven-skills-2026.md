# Nate B. Jones — AI labor market (K-shape) and seven production skills (digest)

**Source:** YouTube, channel [AI News & Strategy Daily (Nate B Jones)](https://www.youtube.com/@NateBJones). Approximate title: *The AI Job Market Split in Two / $400K roles and hiring friction* (2026). **Transcript:** supplied by operator (Cursor session); cite exact URL when pinned.

**Scope:** External research for [work-dev](../../../../docs/skill-work/work-dev/README.md). Not Record truth until merged through the pipeline.

---

## Thesis (labor market)

- **K-shaped split:** Traditional knowledge-work openings (generalist PM, conventional SWE, standard analysts) **flat or falling**; roles that **design, build, operate, and manage AI/agentic systems** are **extremely tight** on qualified people.
- **Perception gap:** Employers report “cannot fill”; many applicants report “cannot get hired” — **mismatch**, some **exploitative hiring** (using candidates to learn AI), and candidates **overselling** or lacking production skills.
- **Speaker-cited stats (verify independently):** e.g. ~**3.2** open AI roles per qualified candidate; Manpower-style figures (~1.6M jobs vs ~0.5M qualified); **~142 days** time-to-fill. Treat as **directional** until sourced.

**Work-dev lens:** Buyer and operator vocabulary — **reliable governance of agentic systems** (not “chat skills”) is the scarce capability; aligns with **silent failure**, **stage-only**, **companion gate**, and **portable Record**.

---

## Seven skills (from job postings, per speaker)

| # | Skill | One-line | Adjacent professions |
|---|--------|----------|----------------------|
| 1 | **Specification precision / clarity of intent** | Instructions literal enough that agents reproduce intent without drifting | Technical writing, law, QA |
| 2 | **Evaluation and quality judgment** | Automated evals, simulations, edge cases; resist fluent-wrong output; “taste” as repeatable error detection | Editing, auditing |
| 3 | **Task decomposition and multi-agent delegation** | Planner + sub-agents; **size work to the harness**; guardrails, not vague PM handoffs | PM (adapted) |
| 4 | **Failure pattern recognition** | Diagnose root causes and fix | SRE, risk, ops |
| 5 | **Trust and security design** | Human vs agent boundaries, blast radius, reversibility, frequency, **functional vs semantic** correctness | Risk, security |
| 6 | **Context architecture** | Persistent vs session context; clean retrieval; avoid polluting context; “library for agents” | Librarians, tech writers |
| 7 | **Cost and token economics** | Blended model mix, ROI, $/MTok, planning before burning tokens | Applied math / finance |

---

## Six failure types (speaker)

1. **Context degradation** — quality drops as context window fills.
2. **Specification drift** — long runs lose original spec unless harness re-anchors.
3. **Sycophantic confirmation** — agent agrees with bad input and builds on it.
4. **Tool selection errors** — wrong tool, often from bad tool framing or overload.
5. **Cascading failure** — one agent error propagates without correction loops.
6. **Silent failure** — output **plausible** but **wrong in production** (hardest).

---

## Trust design dimensions (speaker)

- **Cost of error / blast radius**
- **Reversibility** (draft vs committed action)
- **Frequency** (volume of exposure)
- **Verifiability** — insist on **functional** correctness, not only plausible text

---

## Work-dev / Grace-Mar mapping (operator)

| Transcript idea | Repo anchor |
|-----------------|-------------|
| Spec precision | [templates/specification-precision.md](../../../../docs/skill-work/work-dev/templates/specification-precision.md), OpenClaw skills, handback specs |
| Eval / quality | [quality-gates-narrative.md](../../../../docs/skill-work/work-dev/quality-gates-narrative.md), [variation-types.md](../../../../docs/skill-work/work-dev/variation-types.md), `validate-change-review.py` (template) |
| Multi-agent / harness | [PARALLEL-MACRO-ACTIONS.md](../../../../docs/skill-work/work-dev/PARALLEL-MACRO-ACTIONS.md), [agentic-environment-principles.md](../../../../docs/skill-work/work-dev/agentic-environment-principles.md) |
| Failure modes | [agent-reliability-playbook.md](../../../../docs/skill-work/work-dev/agent-reliability-playbook.md), [failure-pattern-checklist.md](../../../../users/grace-mar/recursion-gate-staging/failure-pattern-checklist.md) |
| Trust / guardrails | [AGENTS.md](../../../../AGENTS.md) stage-only merge, [safety-story-ux.md](../../../../docs/skill-work/work-dev/safety-story-ux.md) |
| Context architecture | Canonical paths, export bundles, SESSION-LOG / RECURSION-GATE read order ([session-continuity-contract.md](../../../../docs/skill-work/work-dev/session-continuity-contract.md)) |
| Token economics | [economic-benchmarks.md](../../../../docs/skill-work/work-dev/economic-benchmarks.md), `scripts/token_economics.py`, [emit_compute_ledger.py](../../../../scripts/emit_compute_ledger.py) |

---

## Operational artifacts (this repo)

- Digest (this file).
- Template: [specification-precision.md](../../../../docs/skill-work/work-dev/templates/specification-precision.md).
- Checklist: [failure-pattern-checklist.md](../../../../users/grace-mar/recursion-gate-staging/failure-pattern-checklist.md).
- Estimator CLI: [token_economics.py](../../../../scripts/token_economics.py).
