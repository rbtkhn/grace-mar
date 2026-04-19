---
name: primary-overhearing-analysis
preferred_activation: primary overhearing
description: Analyzes high-symbolism speeches, visits, and rituals using primary vs overhearing audiences, speech-act function, and second-order spillover (soft power, who gains moral authority vs rivals who claim to solve the problem). Use when the operator asks for audience optics, primary/overhearing frame, papal or diplomatic visits, interfaith stops, migration messaging, or narrative competition over the solver role.
portable: true
version: 1.0.0
tags:
- operator
- analysis
- strategy
portable_source: skills-portable/primary-overhearing-analysis/SKILL.md
synced_by: sync_portable_skills.py
---
# Primary vs overhearing audience analysis

**Preferred activation (operator):** **`primary overhearing`** (or **`audience optics`**).

Use for **public symbolic events**: papal or other religious leaders’ trips, major diplomatic speeches, migration or humanitarian addresses, mosque/church/synagogue visits, UN-style moral framing—not for private negotiation text unless the operator asks.

**Default lane:** **Think** / **WORK** analysis; **not** Record truth, not autonomous outbound copy unless the operator routes to a draft skill.

## Core constructs

| Construct | Meaning |
|-----------|--------|
| **Primary audience** | The **grammatical addressee** and **hosts**: who the ritual is staged to satisfy (e.g. state hosts, local religious leadership, affected community on site). |
| **Overhearing audience(s)** | Everyone **not** the direct addressee but **meant to see or hear** the performance: global media, diaspora, domestic factions, rival capitals, religious subgroups (reassurance vs alarm). Often **multiple** with conflicting reads. |
| **Speech act / ritual function** | What the event **does** (honour, repair, warn, invite, boundary-set), not only what words say. |
| **Second-order spillover** | **Favourability**, **attention**, **legitimacy** shifts: who gains **soft power** or **moral authority**; who loses **relative** ground as the **sole solver** of a felt problem (enforcement, order, realism) when the frame is mercy, dialogue, or bridge-building. |
| **Narrative competition** | Different overhearers slot the same images into **different** stories (bridge vs elite cosmopolitanism; continuity vs betrayal of base). |

## Procedure

1. **Event** — One line: actor, place, date if known; flag **VERIFY** if facts are uncertain.
2. **Primary audience** — Who is **directly** addressed and **whose** legitimacy or feelings the staging serves.
3. **Overhearing audiences** — List **2–4** distinct groups; note **tension** (who applauds vs who resents the same clip).
4. **Speech act** — Short: what the visit or speech **performs** in one paragraph.
5. **Second-order effects** — Bullets: soft power, **relative** positioning vs named political or cultural rivals **only when** the operator or evidence ties the event to that contest; otherwise keep generic (“restrictionist vs bridge-builder frame”).
6. **Limits** — One short paragraph: what this analysis **does not** imply (e.g. no automatic polling swing; domain of spillover may be interfaith not border policy unless linked).

## Output template (use verbatim headings)

```markdown
## Event (fact spine)
## Primary audience
## Overhearing audiences
## Speech act / ritual function
## Second-order spillover and narrative competition
## Limits and abstentions
```

## Guardrails

- **No invented facts** — Dates, names, quotes, attendance: **VERIFY** with a source or stay at framework level.
- **No fake precision** — Avoid “this hurts Trump by X points” unless citing polls or studies.
- **Scope honesty** — If spillover to domestic politics is **optional framing by media**, say so; distinguish **primary** diplomatic/interfaith effects from **grafted** US or EU culture-war reads.

## Agent behavior norms

- **Brevity** — Default to the template; expand only if the operator asks for depth.
- **Abstention** — When the event is unfamiliar, run the **frame** without filling in false specifics.

## Related (optional handoffs)

- **fact-check** — When claims about what was said or signed need web verification.
- **skill-strategy** — When the operator wants the same insight folded into strategy-notebook judgment with civ-mem grounding.


## Cursor / grace-mar instance

Grace-mar paths (from `.cursor/skills/primary-overhearing-analysis/`).

| Topic | Path |
|--------|------|
| Portable core | [skills-portable/primary-overhearing-analysis/SKILL.md](../../../skills-portable/primary-overhearing-analysis/SKILL.md) |
| Manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |
| Strategy notebook (optional weave) | [docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) |

**Instance note:** Vatican or state **primary** sources (e.g. press.vatican.va) beat unattributed recap for quotes and dates when the operator wants verification.
