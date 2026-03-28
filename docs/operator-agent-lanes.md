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

**Ambiguous one-liners** (e.g. a vague question with no prefix) still default to **PLAN**. For implementation, commits, or push, the operator should use **`EXECUTE`** (or **`DOCSYNC`** / **`EXECUTE_LOCAL`** as appropriate) or explicit verbs such as “implement,” “commit,” or “commit and push.”

---

## Git workflow — grace-mar

Scope rules for this repo (instance + operator lanes), complementary to [AGENTS.md](../AGENTS.md) merge authority.

- **Feature branch per theme** — For non-trivial or multi-file work, use a dedicated branch so `main` stays easy to fast-forward and PRs stay reviewable. Trivial one-file fixes on `main` remain fine when the operator prefers.
- **Scoped staging** — When the task is narrow, stage by path or `git add -p`. Mixing `users/grace-mar/*`, `research/external/work-jiang/*`, `bot/`, and broad `docs/*` in one commit without operator intent is a **review hazard**; split or call it out in the commit message.
- **Before push (collaborative remotes)** — If others may have pushed, run `git fetch` and reconcile (`git pull --rebase` or merge) before `git push` to avoid a surprise “fetch first” rejection.
- **After `git push` of a branch other than `main`** — Emit a **GitHub compare URL** so the operator can open a PR without the `gh` CLI:
  - `https://github.com/<owner>/<repo>/compare/<base>...<head>`
  - Derive `<owner>` and `<repo>` from `git remote get-url origin` (HTTPS or `git@github.com:owner/repo.git`).
  - Typical bases: `main` or the branch the operator named.
  - Add a **suggested PR title** and a **short body** (three to five lines: scope, risk, how to verify).
- **Optional helper:** `python3 scripts/github_compare_url.py` prints the compare URL for the current branch against `main` (see `--help`).

### Source of “done” (plan vs execution)

Cursor **plan files** may be frozen or read-only by policy; **Cursor todos** are ephemeral. **Canonical shipped work** is **git history** on the intended remote (plus companion-approved gate merges into the Record when applicable). Do not treat the plan markdown as the only ledger for what is finished.

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
- [Bootstrap — Working trees and authority](../bootstrap/grace-mar-bootstrap.md#working-trees-and-authority)
