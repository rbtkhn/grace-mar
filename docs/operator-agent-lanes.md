# Operator–agent message lanes

**Purpose:** Use one explicit **lane prefix** at the start of a message (or in the first line) so **plan-only** work, **full ship** (through push), **docs-only** sync, or **local commit without push** is unambiguous for the agent—especially when Cursor **plan mode** is active.

These lanes govern **tooling and git scope** for the turn, not Abby’s persona or Record pipeline law.

---

## Lanes

### `PLAN`

- Design, tradeoffs, questions, or written plan content.
- **No** repo file edits, **no** git, **no** push—unless the same message explicitly allows editing a specific plan file or doc.

### `EXECUTE`

- Implement the agreed scope; run checks the operator asked for (tests, linters, `validate-template`, etc.).
- **`git commit`** when there are changes; **`git push`** when the message includes shipping to remote (name the branch or say “push”).
- **Tags** (e.g. `template-v0.x.x`) only if the operator states them in the message.

### `DOCSYNC`

- **Documentation only:** merge logs, mirrors, README, operator docs, cross-links.
- Keep the diff narrow to docs (and explicitly named files).
- **Push** only if the operator says to push in the same message.

### `EXECUTE_LOCAL`

- Same as **EXECUTE** for implementation and **commit**, but **do not push** unless the operator upgrades the lane in-message (e.g. “now push”).

---

## Default

If there is **no** prefix and intent is **unclear**, the agent should default to **PLAN** (safest: prose and proposals only)—unless the message clearly **continues** an already-approved **EXECUTE** thread (same task, same scope).

---

## Examples

- `PLAN — Should we add CI for validate-change-review before or after template tag?`
- `EXECUTE — Add docs/operator-agent-lanes.md; commit grace-mar; push origin main.`
- `DOCSYNC — Update merging-from-companion-self §3 with pin abc1234; push grace-mar.`
- `EXECUTE_LOCAL — Patch server.js; commit companion-self; do not push yet.`

---

## Relation to Think / Ship

[operator-creative-process](../.cursor/rules/operator-creative-process.mdc) **Think** vs **Ship** is **cognitive cadence** (explore vs gated merge / client-facing ship).

**PLAN / EXECUTE / DOCSYNC / EXECUTE_LOCAL** are **per-message scope** for the coding agent: whether this turn may touch files, git, and remotes.

They **stack**: you can be in **Think** cognitively and still send **`PLAN`** so the agent does not edit; or be in **Ship** and send **`EXECUTE`** so the agent runs through push when you say so.

---

## See also

- [Operator style](../.cursor/rules/operator-style.mdc) (always-on; links here)
- [Operator cognition — North star](lanes/operator-cognition.md)
