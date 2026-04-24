---
name: brewmind-governed-steward
preferred_activation: brewmind governed steward
description: "BrewMind × Cici: route business facts through evidence → prepared context → proposals → governed state (owner-approved). Triggers: brewmind steward, governed state steward, BrewMind gate, Cici proposal, promote BrewMind fact."
---

# brewmind-governed-steward — BrewMind business × Cici Git truth

**Primary triggers:** **`brewmind governed steward`**, **`BrewMind steward`**, **`governed state steward`**, **`Cici proposal`**, **`promote BrewMind fact`**.

**Purpose:** Make **[Cici](https://github.com/Xavier-x01/Cici)** actually **manage** BrewMind **business** — not only chat or Supabase recall — by **closing the loop** from messy reality to **reviewable, durable files** Xavier owns.

**Territory:** **WORK** (advisor + Xavier operator). **Not** grace-mar **Record** or **RECURSION-GATE** merges. **Canonical instance:** Xavier’s repo [Cici](https://github.com/Xavier-x01/Cici) — see [README](https://github.com/Xavier-x01/Cici#readme), [`docs/governed-state-doctrine.md`](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md), `config/authority-map.json`.

**Pairs with:** [skill-cici](../skill-cici/SKILL.md) (daily rhythm / journal) · [work-cici](../../../docs/skill-work/work-cici/README.md) · optional Cici slash commands (`/draft-proposal`, `/review-governed-change`, `/promote-to-governed-state`, `/session-start`).

---

## The one skill (in one sentence)

**Know which BrewMind facts belong in which layer — and move them with a proposal before they become “official.”**

---

## Layer routing (do this first)

| Kind of input | Default landing | Next step toward truth |
|---------------|-----------------|-------------------------|
| Raw note, screenshot, call log, “someone said …” | `evidence/` | Summarize in `prepared-context/` when decision-ready |
| Pricing, hours, partner terms, public promise, membership rules | **Never** only chat | **`proposals/queue/`** JSON + schema — owner reviews |
| Approved durable business fact | `users/cici/governed-state/` (per authority map) | Only **after** explicit approve + validate |

**Supabase / MCP “thoughts”** = **operational memory**. **Git governed state** = **durable, reviewable business record** in-repo. Promote on purpose; do not duplicate blindly.

---

## Steps (operator or Xavier with Claude Code)

1. **Name the fact** — One sentence: what would change if this were wrong?
2. **Pick the surface** — Evidence only vs needs proposal vs already in governed state (read `config/authority-map.json`).
3. **Draft or update** — Use `/draft-proposal` or hand-edit `proposals/queue/` per repo schema; link supporting evidence paths.
4. **Review** — Self-review + `/review-governed-change` (or human checklist): authority, scope, no secrets in-repo.
5. **Approve** — Owner (Xavier) decides; rejected/deferred go to `proposals/rejected/` with reason if your workflow uses it.
6. **Apply** — Promote to governed state per doctrine; run `scripts/validate-governed-state.py` / CI before push.
7. **Push** — Same day when possible so advisor sees a **commit spine** aligned with BrewMind reality.

---

## Anti-patterns

- **Chat as system of record** — Business truth only in Claude thread → **invisible** to git history and advisor review.
- **Skipping proposals for “small” changes** — Small public-facing facts (price, hours) are **high leverage**; route them.
- **Writing governed state directly** to “save time” — Bypasses review and breaks the model Cici was built for.
- **Flattening Supabase into Git** without a decision — Capture **what happened** in evidence; **what is policy** goes through gate.
- **Huge weekly dumps** — Prefer **small daily ships** (evidence note or one proposal) over rare big merges.

---

## Success signal

One week where **at least two** BrewMind-tagged facts moved **evidence → proposal → (approved) governed** or **explicit defer** with a dated note — and **`main`** on GitHub shows it.

---

## Related (grace-mar advisor)

- [brewmind-philippines-onboarding-guide.md](../../../docs/skill-work/work-cici/brewmind-philippines-onboarding-guide.md) — business bundle
- [xavier-work-profile.md](../../../docs/skill-work/work-cici/xavier-work-profile.md) — Cici matrix row
- [evidence/cici-rtf-sessions-ingest-2026-04-14.md](../../../docs/skill-work/work-cici/evidence/cici-rtf-sessions-ingest-2026-04-14.md) — `.claude/` + companion contract context
