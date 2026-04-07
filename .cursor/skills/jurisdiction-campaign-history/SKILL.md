---
name: jurisdiction-campaign-history
preferred_activation: jurisdiction history
description: 'WORK-politics: derive campaign framing from jurisdictional history (House district, U.S. Senate, governor) using repo chronology markdown; modes house | senate | governor | stack; optional handoff to politics-massie (draft X only). Triggers: jurisdiction history, district history pass, senate history pass, governor history pass, political stack brief.'
portable: true
version: 1.0.0
tags:
- operator
- work-politics
portable_source: skills-portable/jurisdiction-campaign-history/SKILL.md
synced_by: sync_portable_skills.py
---
# Jurisdiction campaign history — framing pass

**Preferred activation (operator):** say **`jurisdiction history`** (optionally with **`house`**, **`senate`**, **`governor`**, or **`stack`**).

Use this skill to turn **documented** chronologies (House CD, U.S. Senate, or governor roster) into **campaign-usable** insights: disproportion, narrative hooks, and explicit boundaries. **WORK territory only** — not Record, not Voice knowledge, not autonomous posting.

## Canonical inputs (configure in your instance)

Map paths in the **Cursor appendix** for this repository (default Kentucky work-politics chronologies when present).

| Input | Meaning |
|-------|---------|
| **office** | Required: `house` \| `senate` \| `governor` \| `stack` |
| **Chronology path(s)** | Markdown file(s) the agent reads as source (operator may override paths) |
| **Cycle context** | 2–5 bullets: office sought, year, audience, principal pillars, what decision the brief supports |

## Hard guardrails

| Rule | Detail |
|------|--------|
| **No invented facts** | Claims must trace to the chronology doc or be labeled **VERIFY** with a named authority (e.g. Bioguide, Senate roster, NGA). |
| **Jurisdiction hygiene** | Never blur **House CD**, **statewide Senate**, and **governor** without naming the office. In `stack` mode, every insight row must include a **Jurisdiction** column. |
| **Redistricting (House)** | Same district number is not the same geography across decades; one explicit line per House run. |
| **Senate classes** | When relevant, note **Class 2 vs Class 3** and that terms are staggered; appointments/specials matter. |
| **Governor parties** | Old party labels (Whig, Jeffersonian-Republican) are not modern D/R; say so when analogizing. |
| **Public copy** | Output may include suggested lines for social — mark **`DRAFT — NOT POSTED`** if any line could be published. Operator approves before publish. |
| **politics-massie handoff** | If the operator wants X threads for @usa_first_ky analysis lane, invoke **`massie x`** / **politics-massie** after this pass; that skill owns web search and cite discipline for posts. |

## Mode checklist (run before writing insights)

| Mode | Extra checks |
|------|----------------|
| **house** | Redistricting + at-large years if noted in source; special-election swear dates if in doc. |
| **senate** | Class 2 vs 3; appointment chains; same person non-consecutive stints. |
| **governor** | Term-limit era vs pre-1992; resignations for Senate; Confederate shadow gov’t is **not** the main roster. |
| **stack** | Read **all** configured paths; single brief with **Jurisdiction** on every insight; one paragraph **integration** (how House / Senate / executive stories differ for this cycle). |

## Procedure

1. **Parse** operator `office` and paths (defaults from appendix if omitted).
2. **Read** chronology file(s); note sections used (roster, footnotes, sources).
3. **Disproportion** — Short table or bullets: what the history **overweights** vs what is **thin** (e.g. long tenures vs competitive eras).
4. **Campaign insights** — **5–7 bullets**. Each: *claim* · *use* · *risk* · *source (doc section or VERIFY)*.
5. **Hooks** — Three lines labeled **Positive**, **Contrast**, **Caution** (topic-first if any may become public).
6. **Boundaries** — `Do not say` list (false geographic continuity, unsourced scandal, implying voters “own” distant history).
7. **Verify next** — Only if needed: Bioguide, Senate KY roster, NGA, maps.
8. **Optional:** One block **Handoff to politics-massie** — paste hooks + 2–3 insights; remind **draft-only** and cite rules there.

## Output template (use verbatim headings)

```markdown
## District / jurisdiction snapshot (from source)
## Disproportion
## Campaign insights
## Hooks (Positive / Contrast / Caution)
## Boundaries
## Verify next (if any)
## Optional — Handoff notes for politics-massie
```

## Related portable skills

- **politics-massie** — Real-time web search + draft X for @usa_first_ky; use **after** this pass when the operator wants posts.


## Cursor / grace-mar instance

Use these paths **in this repository** when applying the portable skill. Override when working another state or district.

## Default geography

- **State:** Kentucky
- **House example district:** KY-4 (adjust path if you maintain another CD doc)

## Default chronology paths

| Office | Path |
|--------|------|
| House (KY-4) | [ky-4-district-history-report.md](../../../docs/skill-work/work-politics/ky-4-district-history-report.md) |
| U.S. Senate (KY) | [ky-us-senate-chronology.md](../../../docs/skill-work/work-politics/ky-us-senate-chronology.md) |
| Governor (KY) | [ky-governors-chronology.md](../../../docs/skill-work/work-politics/ky-governors-chronology.md) |

## Stack mode

Use **all three** paths above unless the operator substitutes another markdown chronology for the same office type.

## politics-massie handoff

Cursor assembled skill: [.cursor/skills/politics-massie/SKILL.md](../politics-massie/SKILL.md). Instance context table: [account-x.md](../../../docs/skill-work/work-politics/account-x.md) and related rows in politics-massie appendix.
