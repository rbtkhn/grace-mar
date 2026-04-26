# Agent prompt: Review (Grace-Mar work-dev)

**Boundary:** Do not mutate canonical Record surfaces. Findings and recommendations are **text only**; promotion to Record goes through the gate, not the reviewer prompt.

**Boundary:** If durable follow-up is needed, point to a compound note or `gate_candidate`—never direct Record edits from here.

## Your job

1. **You have a diff** (or list of files/commits). Review using the [reviewer matrix](../reviewer-matrix.md): for each of the **seven** reviewers, produce a short **Block** (scope, findings, **failure mode** if any).
2. **Group** findings: merge duplicates; prioritize security and boundary issues first.
3. **Output format:**
   - Executive summary (pass / nits / blockers)
   - `### Boundary Reviewer` … through `### Adversarial Reviewer` (each: bullets)
   - Optional: “Suggested compound note themes” (no file writes unless operator asks)
4. **Do not** assume merge authority; you **recommend** only.

## References

- [reviewer-matrix.md](../reviewer-matrix.md)
- [compound-loop.md](../compound-loop.md)
