# Specification precision template v1 (work-dev / OpenClaw / gate)

**Purpose:** Machine-literal intent for agent runs, OpenClaw skills, handback bundles, or major operator proposals. Aligns with **stage-only** automation and **companion merge authority** ([work-dev README](../README.md)). Not a substitute for RECURSION-GATE approval.

**Provenance:** Operator pattern; informed by Nate B. Jones “specification precision” framing (see [work-dev digest](../../../../research/external/work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md)).

---

## Intent (one sentence, functional)

What **must be true** when this work is done — no vibes.

---

## Success criteria (measurable)

- **Functional correctness:** What must be true in outputs or repo state (files created, scripts pass, format valid).
- **Edge cases:** List explicitly (boundary inputs, empty states, permission errors).
- **Failure modes to avoid:** e.g. specification drift, sycophantic confirmation on bad source data, silent failure (looks right, wrong in production).

---

## Input context

| Kind | Paths / artifacts |
|------|-------------------|
| **Persistent (always-on)** | e.g. canonical `users/<id>/session-log.md`, `recursion-gate.md`, export bundle paths per [session-continuity-contract.md](../session-continuity-contract.md) |
| **Per-run (on demand)** | Specific files, tickets, or data objects for this task only |

**Rule:** Do not treat chat history or vendor UI as canonical; **git-tracked** sources win.

---

## Output format (strict)

Describe exact deliverables: file paths, JSON shape, or PR/commit expectations.

```json
{
  "example_required_fields": ["field1", "field2"]
}
```

---

## Guardrails and escalation

- **Never merge** into SELF, EVIDENCE, or `bot/prompt.py` without companion approval and `process_approved_candidates.py` ([AGENTS.md](../../../../AGENTS.md)).
- **Escalate to human** when: confidence below threshold, blast radius high, irreversible action, or policy ambiguity.
- **Log** decisions with **reason codes** where the harness supports it.

---

## Verification

- **Automated:** Which scripts or checks (`validate-integrity.py`, harness tests, schema validators).
- **Human spot-check:** What a reviewer must eyeball (functional vs semantic correctness).

---

## Sign-off (operator)

- [ ] Intent is specific enough that another operator would run the same task without guessing.
- [ ] Blast radius and reversibility noted.
- [ ] Staging vs merge path explicit.
