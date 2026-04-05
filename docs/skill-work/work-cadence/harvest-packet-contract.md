# Session Harvest Packet — contract

**Purpose:** Canonical section headings and rules for the **Session Harvest Packet** produced by the **`harvest`** skill (`.cursor/skills/harvest/SKILL.md`). **Not** a bridge packet; **not** a cold-session initializer.

**vs bridge:** [bridge](../../../.cursor/skills/bridge/SKILL.md) ends with a lone line `coffee` so the **next** session runs work-start coffee on a **fresh** thread. **Harvest must not** end with `coffee`. Harvest is for **midstream import** into an agent session that **already has momentum**.

---

## Required closing line (not `coffee`)

The packet must end with **exactly** this final line (plain text, not inside a code fence):

```text
Paste this into the target agent session as context for analysis; do not treat it as a fresh-session initializer.
```

---

## Section contract

Use this heading order unless a section is empty (omit empty sections; do not print “N/A” walls).

| Section | Content |
|---------|--------|
| `# Session Harvest Packet — [YYYY-MM-DD]` | Date = packet generation day (UTC or local; state which). |
| `## Use this packet for` | One sentence: what the **receiving** agent should do (analyze, critique, extend, plan). |
| `## Current session purpose` | 1–3 sentences. |
| `## Main outcomes` | Bullets; tag fragile lines `{fact}` / `{proposal}` / `{uncertain}` where useful. |
| `## Strongest insights` | Bullets; compress. |
| `## Decisions / directions chosen` | What was **chosen** vs merely discussed. |
| `## Important developments` | Prefer **before → after** lines. |
| `## Artifacts / files / modules / products` | `` `path` — role — existing/proposed/modified `` |
| `## Risks / tensions / critiques` | Named disagreements, failure modes. |
| `## Open questions` | Real questions, not filler. |
| `## Recommended next steps` | Numbered 1…n, actionable. |
| `## Suggested asks for the receiving agent` | Imperatives: Analyze…, Critique…, Compare… |
| `## Executive compression` | 8–15 dense bullets. |
| *(final line)* | See **Required closing line** above. |

---

## Forbidden in harvest packets

- A trailing **`coffee`** line (that is **bridge-only**).
- **`# Session Bridge`** title or bridge-specific sections (Arc, Carry-forward from last dream as the **primary** frame, etc.) unless you are **explicitly** comparing packets in prose.
- Implication that the packet **replaces** reading `recursion-gate.md` or **authorizes** merges.

---

## Optional persistence

Default: packet exists **only in chat**. If the operator asks to save: e.g. `docs/skill-work/work-cadence/harvest-packets/YYYY-MM-DD-harvest.md` (operator-owned; not Record).

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-04 | Initial contract (harvest as bridge sibling). |
