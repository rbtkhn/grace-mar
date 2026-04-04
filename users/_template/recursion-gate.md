# recursion-gate — At the Gate (Template)

**Template only. No real data.** Copy this structure when creating a new user directory in an instance repo. The pipeline stages candidates **at the gate**; only the companion (or delegated human) may merge approved items into self, self-evidence, and the dimension files.

Governed by Identity Fork Protocol: agent may stage, may not merge. The gate is where the **recursive** loop turns—proposed changes wait here until the companion approves; then they enter the Record and the system improves. Hence *recursion-gate*.

---

## Candidates

(Placeholder: each candidate has mind_category, signal_type, summary, profile_target, suggested_entry — per instance schema. Companion approves, rejects, or edits; then merge runs.)

---

## Before approve — binary checks (optional)

Use these as a **fast test suite** before saying yes. Skip any row that does not apply to your instance. Adapt wording to your governance (Lexile, boundary rules, etc.).

- **Scope:** Does this candidate stay inside what the companion actually said or approved sources — no scope creep?
- **Contradiction:** Does anything here **flatly contradict** an existing SELF entry? If both should stand, is **provenance / tension** documented per instance policy?
- **Evidence:** Is there a plausible `evidence_id`, artifact, or `human_approved` path — not model invention?
- **Target surface:** Is `profile_target` (IX-A / IX-B / IX-C / EVIDENCE / prompt) correct for this content?
- **Voice / safety:** If prompt or Voice text changes: would the companion **stand behind** this text as canonical? Any boundary or abstention regression?
- **Operator echo:** For automated merges: does the operator echo **candidate id + one-line summary** before `--apply`, per instance procedure?

If any **must-pass** check fails, **reject or edit** the candidate; do not merge hoping to fix later.

---

*Do not use this file as a live staging area in the template. Copy to `users/<new_id>/recursion-gate.md` in an instance (or keep an equivalent name such as recursion-gate.json for the machine-readable queue).*
