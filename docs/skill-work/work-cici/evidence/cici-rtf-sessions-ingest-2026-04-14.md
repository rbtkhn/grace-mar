# Cici — RTF session exports + GitHub verification (WORK)

**Captured:** 2026-04-14  
**Territory:** work-cici **evidence** — not Xavier’s Record; not a gate merge.

| Source (Downloads) | Stored in-repo |
|--------------------|----------------|
| `grace-mar patterns (2).rtf` | [cici-brewmind-companion-contract-session-2026-04-14.rtf](cici-brewmind-companion-contract-session-2026-04-14.rtf) |
| `plan for cici (1).rtf` | [cici-claude-best-practices-plan-session-2026-04-14.rtf](cici-claude-best-practices-plan-session-2026-04-14.rtf) |

Text extracted with `textutil -convert txt` on macOS for summary; RTF binaries preserved for audit.

---

## Session A — “grace-mar patterns” / BrewMind companion contract (RTF 1)

**Content:** Full **Claude Code prompt** implementing grace-mar-style patterns (abstention, tiers, proposal echo, lanes, humane purpose, open loops), then **Phase 0** orientation bullets and **execution** on branch `claude/brewmind-companion-contract-xA3Vn`, merged to **`main`**.

**Stated deliverables (transcript):**

- `docs/companion-agent/brewmind-companion-contract.md` — eight-section behavioral contract.  
- `docs/companion-agent/brewmind-open-loops.md` — Partners / Site / Content / Budget / Blockers.  
- `CLAUDE.md` — **BrewMind companion defaults** (8 bullets + link).  
- `proposals/queue/prop-20260414-001-brewmind-companion-contract.json` — **proposed**, workflows surface.

**GitHub verification:** Commit **[`fcfe437`](https://github.com/Xavier-x01/Cici/commit/fcfe4375599c7835b645c2977afc3df0d96b1214)** on **`main`** (2026-04-14T01:44:44Z), **parent [`5337b1c`](https://github.com/Xavier-x01/Cici/commit/5337b1ce2c58edd9fb02d6feb0b6461e1c1fb711)** — matches “merge companion work after session behavior commit.”

---

## Session B — `shanraisshan/claude-code-best-practice` absorption (RTF 2)

**Content:** **PLAN** to add **`.claude/`** native layer (settings, slash commands, agents, hooks, `CLAUDE.local.md` stub, `.gitignore`), then **EXECUTE** on `claude/cici-best-practices-plan-ywd4E`, merged to **`main`**.

**Stated deliverables (transcript):**

- `.claude/settings.json` — plan mode, permissions, SessionStart hook.  
- `.claude/hooks/session-start.sh` — surfaces proposals + open loops.  
- `.claude/commands/*.md` — `/session-start`, `/draft-proposal`, `/review-governed-change`, `/promote-to-governed-state`, `/stage-evidence`, `/memory-audit`.  
- `.claude/agents/*.md` — proposal-reviewer, evidence-stager, memory-auditor.  
- `CLAUDE.md` — Plan-mode-first, command table, agents table, **Common Errors** log.  
- `CLAUDE.local.md` — gitignored stub; operator fills personally.

**Upstream inspiration (external):** [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) — patterns absorbed per session; not vendored wholesale.

**GitHub verification:** Commit **[`901012d`](https://github.com/Xavier-x01/Cici/commit/901012d0da2be14b5b42acab1ce981ec30fe9a07)** on **`main`** (2026-04-14T02:19:38Z), **parent [`fcfe437`](https://github.com/Xavier-x01/Cici/commit/fcfe4375599c7835b645c2977afc3df0d96b1214)** — **fast-forward** chain: session A → session B.

---

## Repo state snapshot (`main` tip)

| Field | Value |
|--------|--------|
| **`main` HEAD** | [`901012d`](https://github.com/Xavier-x01/Cici/commit/901012d0da2be14b5b42acab1ce981ec30fe9a07) |
| **Parent chain (3)** | `901012d` → `fcfe437` → `5337b1c` |
| **Match to RTFs** | **Yes** — both described merges appear on **public `main`** with correct parent order. |

**Operator follow-ups (from transcripts, still valid):**

- **`CLAUDE.local.md`** — gitignored; Xavier maintains locally.  
- **Proposals** `prop-20260413-001`, `prop-20260414-001` — **review / approve** when ready; governed apply only after owner decision.  
- **Validator warnings** — session notes: full-path `target_surface` vs short IDs in validator (known pattern).

---

## Files in this folder

| File | Role |
|------|------|
| [cici-brewmind-companion-contract-session-2026-04-14.rtf](cici-brewmind-companion-contract-session-2026-04-14.rtf) | RTF export — companion contract session. |
| [cici-claude-best-practices-plan-session-2026-04-14.rtf](cici-claude-best-practices-plan-session-2026-04-14.rtf) | RTF export — best-practices `.claude/` session. |
| This file | Summary + API verification. |
