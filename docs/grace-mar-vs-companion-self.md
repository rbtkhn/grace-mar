# Grace-Mar vs Companion-Self — Instance vs Template

Side-by-side comparison of the two repositories that form the companion-self vision: personalized, long-term cognitive profiles (companion selves) that grow through interaction, evidence, and self-directed learning.

| Repo | Role |
|------|------|
| [github.com/rbtkhn/grace-mar](https://github.com/rbtkhn/grace-mar) | **Instance / pilot** — live cognitive fork for one person |
| [github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self) | **Template / framework** — reusable blueprint for new instances |

---

## Core comparison

| Aspect | grace-mar (instance / pilot) | companion-self (template) |
|--------|------------------------------|----------------------------|
| **Purpose** | Live pilot for a specific user (Grace-Mar): real cognitive fork with seeded data, active pipeline, and emulation. | Reusable blueprint for creating new companion-self instances. No live user data. |
| **Description** | System for creating and maintaining versioned, evidence-grounded cognitive forks of an individual, growing via curated interactions over time. | Template repo for instantiating new companion selves after seed phase completion. |
| **Status** | Active pilot — seeded, pipeline running, bots live, real user data. | Reference/template — clone or fork to bootstrap new instances. |
| **Main reference** | Concrete example; linked from companion-self docs. | Points to grace-mar as the reference implementation ([grace-mar.com](https://grace-mar.com)). |
| **Primary focus** | Running system: profile generation, gated updates, bot emulation (Telegram/WeChat), export, metrics, integrity, profile/miniapp UI. | Education and self-improvement protocol, student app, upgrade mechanics, library structure, bootstrap process. |
| **Contains user data** | Yes — `users/grace-mar/` with self.md, skills, evidence logs, interaction history. | No — template only (`users/` is placeholder or _template). |
| **Tech** | Python-heavy (bot, scripts, Flask, export); HTML/JS for profile and miniapp. | JavaScript-heavy (student web app); HTML/shell/CSS; docs and scripts. |
| **Key directories** | `bot/`, `scripts/`, `docs/`, `users/grace-mar/`, `profile/`, `miniapp/` | `app/` (student interface), `library/`, `docs/`, `scripts/`, `users/_template/` |
| **Notable features** | Gated pipeline (signal → staging → recursion-gate → integration); Telegram/WeChat bots; growth dimensions (knowledge, curiosity, personality); export (JSON, PRP, PDF); integrity and uniqueness scoring. | Recursive self-learning objectives; 3-year roadmap and 6-week coding sprint; student app (e.g. localhost:3000); upgrade consumption (how instances pull improvements without losing records); bootstrap guide. |

---

## Relationship

- **companion-self** = upstream **template** — clean, reusable foundation.
- **grace-mar** = first **downstream instance** created from (or aligned with) that template.
- Shared protocol, UI patterns, library, and upgrade mechanics are developed in companion-self; instances like grace-mar **consume** those improvements without overwriting their Record or history. See [how-instances-consume-upgrades](https://github.com/rbtkhn/companion-self/blob/main/how-instances-consume-upgrades.md) (in companion-self) and [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md) (in grace-mar).

---

## One-sentence summary

- **grace-mar** = Living proof-of-concept cognitive fork for one person (Grace-Mar), with real data, bots, metrics, and export tools.
- **companion-self** = Open, reusable starter kit and educational framework you clone to create the next person’s lifelong companion self.

To create another instance (another person or persona), start from companion-self, follow its bootstrap and seed phase, and end up with a structure similar to grace-mar but with different user data.

---

## Related

- [MERGING-FROM-COMPANION-SELF](merging-from-companion-self.md) — How to pull template upgrades into grace-mar.
- [AUDIT-GRACE-MAR-VS-COMPANION-SELF-TEMPLATE](audit-grace-mar-vs-companion-self-template.md) — Compliance of this instance against the template.
