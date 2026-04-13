# UPLOAD-PREP — work-xavier bundle (forthcoming)

**Use when:** You are about to copy grace-mar **work-xavier**-related material to **[Cici](https://github.com/Xavier-x01/Cici)** (or another Xavier-controlled repo / zip share).

**Advisor module stays canonical in grace-mar** — her repo gets **what she needs to run**, not a full mirror of `docs/skill-work/work-xavier/`.

---

## 1) Choose upload scope

| Scope | What to copy | Typical destination |
|-------|----------------|---------------------|
| **Minimal (recommended default)** | Entire [`.cursor/skills/skill-xavier/`](../../../.cursor/skills/skill-xavier/) | `Cici/.cursor/skills/skill-xavier/` |
| **Skill + activation line** | After copy, one line in her `CLAUDE.md` (or repo onboarding doc): daily learning log → **skill-xavier** **Mode B** | Same repo |
| **Advisor docs** | Full `docs/skill-work/work-xavier/` | **Usually omit** — duplicates INDEX, runbooks, BrewMind pack; risks path confusion unless she explicitly maintains advisor docs in-tree |

**Link expectation:** `SKILL.md` links many paths under `docs/skill-work/work-xavier/` and `scripts/` — those resolve in **grace-mar**. On Cici, **Mode B** (journal template, guardrails, `validate-governed-state.py`) still works; deep links are for mentor context or grace-mar checkout. See [Porting](../../../.cursor/skills/skill-xavier/SKILL.md#porting-this-skill-to-cici) (trim **Mode A** if confusing).

---

## 2) Pre-flight (required)

- [ ] Read [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md) — no stray `users/grace-mar/` identity, no Record merges without her gate, RAG/MCP ≠ approval.
- [ ] Search files you will ship: no accidental `users/grace-mar/` path strings (except explicit policy cites).
- [ ] No API keys, tokens, or credentialed URLs in shipped markdown.
- [ ] If you paste **journal** samples, scrub secrets; journal is WORK, not her Record.

---

## 3) skill-xavier manifest (minimal upload)

Relative to grace-mar repo root:

```text
.cursor/skills/skill-xavier/
├── SKILL.md
└── (any other files in that directory — include whole folder)
```

Verify:

```bash
ls -la .cursor/skills/skill-xavier/
```

---

## 4) Optional: refresh grace-mar mirrors before / after the call

Upload to Cici does **not** require mirror files. If you are also aligning **advisor** materials in grace-mar, follow [SYNC-DAILY.md](SYNC-DAILY.md) and append [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md) / [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md) when you copy canonical cuts.

---

## 5) After upload lands

- [ ] Confirm she can follow **Mode B** steps (calendar day file, sections, governed-state validator when touching proposals/config).
- [ ] Log the event in the table below (and optionally one bullet under **Log** in [work-xavier-history.md](work-xavier-history.md)).

### Upload log (operator)

| Date | Scope | Destination | Notes |
|------|-------|-------------|-------|
| _(pending)_ | | | |
