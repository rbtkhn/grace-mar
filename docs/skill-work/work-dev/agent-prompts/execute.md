# Agent prompt: Execute (Grace-Mar work-dev)

**Boundary:** Do not mutate canonical Record surfaces (SELF, SKILLS, EVIDENCE, Library, `users/*` identity files). If durable learning is needed, add a [compound note](../compound-note-template.md) or `gate_candidate` **recommendation** only.

## Your job

1. **Implement** the approved plan with **additive, minimal** changes. Match existing code style, naming, and paths.
2. **Touch only** the files the plan and operator agree on; no drive-by refactors.
3. **Run** relevant checks: e.g. `python3 -m py_compile` on new scripts, `pytest` on affected tests, or the narrow commands the plan names.
4. **Summarize** in the reply: bullet list of **exact files changed** and what each change does; any tests run and results.
5. **If** you learn something reusable, flag it for the **Compound** step—do not write to Record.

## Do not

- Edit `recursion-gate.md` or merge candidates unless the task explicitly authorizes a governed workflow.
- Add heavy dependencies; prefer stdlib or existing project deps.

## References

- [compound-loop.md](../compound-loop.md)
- [claim-proof-standard.md](../claim-proof-standard.md) (if claiming “done”)
