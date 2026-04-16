# Cici handoff — BrewMind governed steward (operator)

**Do not copy this whole file into Cici.** Copy from the heading **`# BrewMind governed steward`** through the **end of the file** (everything after the first horizontal rule below). The lines above are operator-only.

**Target in [Xavier-x01/Cici](https://github.com/Xavier-x01/Cici):** create **`docs/skills/brewmind-governed-steward.md`** (add folder `docs/skills/` if it does not exist yet).

**Optional `CLAUDE.md` one-liner** (BrewMind or Skills section):

```text
BrewMind business facts: route through evidence → proposals → governed state per docs/skills/brewmind-governed-steward.md (owner approves before durable truth).
```

**Canonical Cursor skill (grace-mar):** [`.cursor/skills/brewmind-governed-steward/SKILL.md`](../../../.cursor/skills/brewmind-governed-steward/SKILL.md)

---

# BrewMind governed steward

**Say to Claude Code:** *BrewMind steward*, *governed state steward*, *Cici proposal*, or *promote BrewMind fact*.

**Purpose:** Run BrewMind **business** through this instance’s **Git-first** model — not only chat or Supabase — so facts become **reviewable** and **push** to GitHub as durable truth.

**See also:** [README.md](../../README.md) (repo layout), [Governed state doctrine](../governed-state-doctrine.md), `config/authority-map.json`. Optional Cici commands: `/draft-proposal`, `/review-governed-change`, `/promote-to-governed-state`, `/session-start`.

---

## The one skill (one sentence)

**Know which BrewMind facts belong in which layer — and move them with a proposal before they become official.**

---

## Layer routing (do this first)

| Kind of input | Default landing | Next step toward truth |
|---------------|-----------------|-------------------------|
| Raw note, screenshot, call log, “someone said …” | `evidence/` | Summarize in `prepared-context/` when decision-ready |
| Pricing, hours, partner terms, public promise, membership rules | **Never** only chat | **`proposals/queue/`** JSON + schema — you review |
| Approved durable business fact | `users/cici/governed-state/` (per authority map) | Only **after** explicit approve + validate |

**Supabase / MCP “thoughts”** = **operational memory**. **Git governed state** = **durable** in-repo record. Promote on purpose; do not duplicate blindly.

---

## Steps (with Claude Code)

1. **Name the fact** — One sentence: what would change if this were wrong?
2. **Pick the surface** — Evidence only vs needs proposal vs already in governed state (read `config/authority-map.json`).
3. **Draft or update** — Use `/draft-proposal` or hand-edit `proposals/queue/` per schema; link supporting evidence paths.
4. **Review** — Self-review + `/review-governed-change` (or checklist): authority, scope, **no secrets** in-repo.
5. **Approve** — You (owner) decide; rejected/deferred go to `proposals/rejected/` with a reason if your workflow uses it.
6. **Apply** — Promote to governed state per doctrine; run `scripts/validate-governed-state.py` / CI before push.
7. **Push** — Same day when possible so your advisor sees a **commit spine** aligned with BrewMind reality.

---

## Anti-patterns

- **Chat as system of record** — Business truth only in Claude → invisible in git history.
- **Skipping proposals for “small” changes** — Small public facts (price, hours) are high leverage; route them.
- **Writing governed state directly** to save time — Bypasses review and breaks this repo’s model.
- **Dumping Supabase into Git** without a decision — Capture **what happened** in evidence; **policy** goes through the gate.
- **Huge weekly dumps** — Prefer **small daily ships** (evidence note or one proposal) over rare big merges.

---

## Success signal

One week where **at least two** BrewMind-related facts moved **evidence → proposal → (approved) governed** or **explicit defer** with a dated note — and **`main`** on GitHub shows it.

---

## Related in this repo

- [brewmind.md](../brewmind.md) — BrewMind integration (if present)
- [governed-state-doctrine.md](../governed-state-doctrine.md)
- `docs/companion-agent/` — companion contract and open loops (filenames may vary by branch)
