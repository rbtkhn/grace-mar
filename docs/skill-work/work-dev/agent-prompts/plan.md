# Agent prompt: Plan (Grace-Mar work-dev)

Use inside this repo: **Grace-Mar** (`grace-mar`).

**Boundary:** Do not mutate canonical Record surfaces (SELF, SKILLS, EVIDENCE, Library, `users/*` identity files). If something should become durable, capture it as a [compound note](../compound-note-template.md) or `gate_candidate` **recommendation** only—no merge or self-approval.

## Your job

1. **Inspect** the relevant part of the repo: read files that the task implies; follow existing layout under `docs/skill-work/work-dev/`, `scripts/`, and territory boundaries in `AGENTS.md`.
2. **Propose the smallest safe plan**: ordered steps, files to create or touch, and what to avoid.
3. **Governance risks:** call out any path that could touch Record, gate, or authority language; suggest counterfactual or review where useful.
4. **Stop before coding** unless the operator explicitly says to execute—this prompt is plan-only by default.
5. **Output:** concise markdown: Summary → Steps → Files → Risks → Open questions.

## References

- [compound-loop.md](../compound-loop.md)
- [three-compounding-loops.md](../three-compounding-loops.md)
- [reviewer-matrix.md](../reviewer-matrix.md) (for risk shape only at plan time)
