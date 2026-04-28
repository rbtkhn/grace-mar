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
- **Dual worktree before push:** When pushing, also check **companion-self** if present (see [Git workflow — grace-mar + companion-self](#git-workflow--grace-mar--companion-self)); do not assume only the open workspace changed.
- **Tags** (e.g. `template-v0.x.x`) only if the operator states them in the message.
- **Skill discovery (optional):** After a **substantive** completed ship (not trivial one-line fixes), the agent may add **one** optional closing line inviting a pointer in [`skills-portable/skill-candidates.md`](../skills-portable/skill-candidates.md) or a draft under `skills-portable/_drafts/` — see [operator-style — Skill discovery](../.cursor/rules/operator-style.mdc). Skip when **coffee** menus apply — full **A–G** or the **steward** **Implement now / Later** fork (legacy **hey** still works) — or when the operator said **no menu** on a **non-coffee** WORK turn.

### `DOCSYNC`

- **Documentation only:** merge logs, mirrors, README, operator docs, cross-links.
- Keep the diff narrow to docs (and explicitly named files).
- **Push** only if the operator says to push in the same message.
- **Dual worktree before push:** When a **push** is in scope, same **companion-self** status check as **EXECUTE** — [Git workflow — grace-mar + companion-self](#git-workflow--grace-mar--companion-self).
- Same **optional skill-discovery** close as **EXECUTE** when the doc pass was substantive multi-file or clearly procedural (see **EXECUTE** bullet).

### `EXECUTE_LOCAL`

- Same as **EXECUTE** for implementation and **commit**, but **do not push** unless the operator upgrades the lane in-message (e.g. “now push”).
- Same **optional skill-discovery** close as **EXECUTE** when the ship is substantive (see above).

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

<a id="git-workflow--grace-mar--companion-self"></a>

### Git workflow — grace-mar + companion-self

Many sessions touch **two** git roots: **grace-mar** (this instance repo) and **companion-self** (template upstream clone — default path `./companion-self` under grace-mar or `GRACE_MAR_COMPANION_SELF`). [Bridge](../.cursor/skills/bridge/SKILL.md) is the full dual-repo seal ritual; **lane pushes** should still avoid leaving one repo dirty while the other ships.

When **`EXECUTE`** or **`DOCSYNC`** includes **push** / **ship to remote** (or you later upgrade **`EXECUTE_LOCAL`** to push in-message):

1. Run **`git status -sb`** in the grace-mar workspace (and `git fetch` / ahead-behind vs `@{u}` when a push is planned).
2. If **companion-self** exists at the conventional path, run **`git status -sb`** there too (and ahead-behind if `origin` is set).
3. **Surface both** in the reply before pushing: uncommitted files, unpushed commits, or “clean.”
4. If **either** repo has pending work, **do not** push only the other **silently**. **Commit/push** each repo that is in scope for this message; if the operator scoped **grace-mar only** (or companion-self only), say so and still **report** the sibling’s status in one line so nothing is forgotten.
5. If scope is **ambiguous** (both dirty but the message did not name both), **ask** once: push both, grace-mar only, or companion-self only.

For **session-close** or heavy handoff, prefer **`bridge`**, which formalizes the same assessment in Step 2–3.

### Anti-pattern: silent single-repo push

If **`EXECUTE`** / **`DOCSYNC`** pushed **one** repo while the **sibling** (e.g. companion-self) was **dirty or ahead**, that is a **scope miss** — not a secret optimization.

**Doc-only loop:** When this happens once, fix git state. When the **same** miss happens **twice**, add **one** caution bullet **here** or in [.cursor/skills/bridge/SKILL.md](../.cursor/skills/bridge/SKILL.md) Step 2 so the next agent surfaces **both** roots before push.

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

- [Conductor layer map](skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md) — five conductors as WORK stance / attention routing (not agents); links [conductor proposal lenses](skill-work/work-dev/conductor-proposal-lenses.md) for PR-shape prompts (Beethoven and Brahms tests); not Record authority.
- [WORK menu conventions](skill-work/work-menu-conventions.md) — evidence links, heuristic tags, choice logging (`session-transcript`), optional multi-agent note.
- [Operator style](../.cursor/rules/operator-style.mdc) (always-on; links here) — includes **WORK modules — multiple choice**: labeled next-step options on most turns when working in work-strategy / work-politics / work-jiang / work-dev unless the operator opts out or a fixed menu (e.g. `coffee`) already applies. **Rationale** (in-rule): lower operator cognitive load (selection vs path enumeration) and use assistant **parallel cognition** to prefetch plausible branches. **No faux “done”** in those menus — work **switches**, it does not end; options are pivots to other real work.
- [Operator cognition — North star](lanes/operator-cognition.md)
- [Bootstrap — Working trees and authority](../bootstrap/grace-mar-bootstrap.md#working-trees-and-authority)
