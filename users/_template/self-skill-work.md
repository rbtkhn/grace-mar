# self-skill-work (Template)

**Template only. No real data.** Copy to `users/<new_id>/self-skill-work.md` in an instance. Schema tag: **WORK**. Making and doing; populated from activity.

**Objectives and intentions** for the user and companion are encoded in skill-work (this file and linked evidence). Evidence-linked; planning, execution, collaboration, originality per instance schema.

**Module intent:** WORK serves as tutor for the companion in making, planning, execution, and creation — proposing activities at the container edge, answering questions, scaffolding next steps, aligned with work goals and life mission. Captures capability from evidence; human-gated.

---

## Objectives and intentions

**Default objectives for new users** (standard set). Replace or extend per instance or after seed. Format: **label** — **description**.

- **Learn and grow** — Steady intake (THINK) at the right level; build knowledge and curiosity.
- **Express and create** — Regular WRITE: journal, stories, explanations; develop voice.
- **Build and ship** — Do projects and creations (WORK); finish and record what was made.
- **Make progress visible** — Use "we did X" and the gate so the Record and edge stay current.
- **Stay within the design** — Aim for up to 2 hours of screen-based learning per day when applicable.
- **Recursively improve** — Improve the ability of companion-self and the human companion over time; this objective can evolve as technology and practice advance. See [Evolving practice and recursive improvement](../../docs/evolving-practice-recursive-improvement.md) for a framework (context, intent, specification engineering) that supports this.

---

## How WORK uses self-personality (IX-C)

WORK utilizes **self-personality** (voice, preferences, values, narrative) so making and doing stay aligned with who the companion is. Instance and integrations should read IX-C (self-personality.md) when proposing work, structuring tasks, phrasing the edge, and prompting "we did X." Canonical pattern: [CONCEPT](../../docs/concept.md) §4 "How WORK utilizes self-personality (IX-C)."

| Use | How IX-C is used |
|-----|------------------|
| **What to build and why** | Values and narrative → which projects and kinds of work are proposed. |
| **How they work** | Preferences → chunk size, pacing, structure, solo vs. collaborative framing. |
| **Voice in work outputs** | Tone and style of WORK-produced text (descriptions, posts) follow self-personality. |
| **Resilience and difficulty** | Narrative/values → difficulty of suggestions and how setbacks / "next try" are framed. |
| **Ritual and "we did X"** | Reflection preferences → how WORK prompts for capture and how progress is summarized. |
| **Edge phrasing** | "What's next" for WORK phrased in companion's voice and values. |

---

## Channels / interfaces (overlap with WRITE)

Same channels that can carry WRITE (Voice, expression) can also be **work interfaces**: the companion (including an autonomous agent or non-human economic actor, e.g. a business) may *do* work through them—transact, respond, publish, operate. Instance fills in which are in use; no secrets here—reference only.

- • **Telegram bot** — (e.g. bot handle; for messaging, automation, or economic activity)
- • **WeChat bot / official channel** — (e.g. channel; for outreach, support, or commerce)
- • **HTML page** — (e.g. site or app URL; for presence, offers, or self-service)
- • **Email account** — (e.g. address; for correspondence, contracts, or notifications)
- • **X.com API** — (e.g. account or app; for posting, listening, or API-driven work)

(Add or remove per instance. Evidence of WORK may link to these interfaces. Overlap with self-skill-write is intentional: one identity can both *express* (WRITE) and *act* (WORK) through the same channels.)

---

## WORK goals

Companion's own objectives for making, planning, execution, creation. Gated; evidence-linked when captured. Standard: **near_term** (list), **horizon** (list), **source** (optional evidence id).

- **near_term** — (e.g. "finish X", "learn Y"; instance fills or leaves empty)
- **horizon** — (e.g. longer-term goals; instance fills or leaves empty)
- **source** — (evidence id when goals were captured; optional)

Template note: instances may initialize WORK lane docs in `docs/skill-work/work-business/` and `docs/skill-work/work-dev/` from seed survey outputs, then use them during daily good-morning planning.

---

## Life mission ref

Life mission lives in SELF (identity, values). WORK goals align with it. Instance keeps the canonical life mission in `self.md` (e.g. § VALUES or equivalent); this file and WORK flows reference it.

---

## Tasks (planning / execution)

Concrete work items. Per [schema-record-api](../../docs/schema-record-api.md): each task has **summary**, **status** (pending | in_progress | done), optional **id**, **evidence_id**, **updated**.

| id | summary | status | evidence_id |
|----|---------|--------|-------------|
| — | (instance adds tasks; link to evidence when done) | — | — |
