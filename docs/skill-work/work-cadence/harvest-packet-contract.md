# Session Harvest Packet — contract

**Purpose:** Canonical section headings and rules for the **Session Harvest Packet** produced by the **`harvest`** skill (`.cursor/skills/harvest/SKILL.md`). **Not** a bridge packet; **not** a cold-session initializer.

**vs bridge:** [Bridge](bridge-packet-contract.md) ends with reorientation (`coffee`) for a **fresh** thread. **Harvest must not** end with `coffee`. Harvest is for **midstream import** into an agent session that **already has momentum**. See also [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md).

---

## Required closing line (not `coffee`)

The packet must end with **exactly** this final line (plain text, not inside a code fence):

```text
Paste this into the target agent session as context for analysis; do not treat it as a fresh-session initializer.
```

---

## Section contract

Use this heading order unless a section is empty (omit empty sections; do not print “N/A” walls). **`## Thread coverage`** sits **after** **`## Current session purpose`** when present.

| Section | Layer | Content |
|---------|-------|--------|
| `# Session Harvest Packet — [YYYY-MM-DD]` | — | Date = packet generation day (UTC or local; state which). |
| `## Use this packet for` | — | One sentence: what the **receiving** agent should do (analyze, critique, extend, plan). |
| | | **Episodic cluster** — *what happened* |
| `## Current session purpose` | episodic | 1–3 sentences. May include **one** trailing caveat sentence when thread context is truncated (or leave caveat to **Thread coverage**). |
| `## Thread coverage` | episodic | **Optional.** Include when early chat is missing from context, when only a **transcript tail** was read, or when **deep** harvest used a capped read. **Max 2 short bullets** — e.g. basis (visible thread / transcript tail 200 / full transcript), truncation note. Omit when the default visible arc is clearly sufficient. |
| `## Important developments` | episodic | Prefer **before → after** lines. |
| | | **Semantic cluster** — *what was figured out* |
| `## Main outcomes` | semantic | Bullets; tag fragile lines `{fact}` / `{proposal}` / `{uncertain}` / `{warrant}` where useful. Use `{warrant}` for outcomes whose validity depends on a stated assumption. |
| `## Strongest insights` | semantic | Bullets; compress. |
| `## Decisions / directions chosen` | semantic | What was **chosen** vs merely discussed. Include warrant (invalidation condition) when a decision depends on an assumption that could change. |
| `## Artifacts / files / modules / products` | semantic | `` `path` — role — existing/proposed/modified `` |
| | | **Assessment** |
| `## Risks / tensions / critiques` | — | Named disagreements, failure modes. |
| `## Open questions` | — | Real questions, not filler. |
| `## Recommended next steps` | — | Numbered 1…n, actionable. |
| `## Suggested asks for the receiving agent` | — | Imperatives: Analyze…, Critique…, Compare… |
| `## Executive compression` | — | 8–15 dense bullets. |
| `## Agent surface` | — | **Always include** (Cursor). One line: **Cursor model:** plus the **model name from the Cursor chat UI** (model picker). Not Record. Use `unknown` only if unavailable. |
| *(final line)* | — | See **Required closing line** above (must be last). |

**Episodic / semantic rationale:** The episodic cluster captures *what happened* (timeline, purpose, developments); the semantic cluster captures *what was figured out* (outcomes, insights, decisions, artifacts). This mirrors Tulving's (1972) episodic–semantic memory distinction and LoreSpec's session-level extraction layers. The separation helps receiving agents distinguish chronological context from reusable knowledge.

---

## Forbidden in harvest packets

- A trailing **`coffee`** line (that is **bridge-only**).
- **`# Session Bridge`** title or bridge-specific sections (Arc, Carry-forward from last dream as the **primary** frame, etc.) unless you are **explicitly** comparing packets in prose.
- Implication that the packet **replaces** reading the gate or **authorizes** merges.

---

## Optional persistence

Default: packet exists **only in chat**. If the operator asks to save: e.g. `docs/skill-work/work-cadence/harvest-packets/YYYY-MM-DD-harvest.md` (operator-owned; not Record).

---

## Improving harvest over time (operator habit)

No scripts required. After pasting the packet into the target session, note **Load**, **Accuracy**, **Action** (see [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) § *After the paste*). If the same gap appears twice, update the skill or this contract.

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-05 | Initial contract in template (harvest as bridge sibling). |
| 2026-04-06 | Pointer to doc-only post-paste review loop (skill § After the paste). |
| 2026-04-07 | **Agent surface** (Cursor UI model). Optional **`## Thread coverage`** — truncation / transcript-basis honesty; **Current session purpose** may carry one caveat line. |
| 2026-04-07 | Episodic/semantic layer grouping; `{warrant}` tag; design rationale — LoreSpec-derived. |
