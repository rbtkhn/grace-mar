# US–Iran kinetic likelihood — cross-author tracker
<!-- word_count: 321 -->

**Kind:** WORK-only strategy-notebook scaffold; **not** Record.  
**Governed by:** [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) § *US–Iran kinetic likelihood (cross-author track)* (`#us-iran-kinetic-track`).  
**Skill:** [`skill-strategy`](../../../../.cursor/skills/skill-strategy/SKILL.md) — apply when **`strategy`** passes touch U.S.–Iran escalation.

## Purpose

Hold a **single comparable object** across indexed authors: *conditional* **near-term** **likelihood** **of** **large-scale** **U.S.** **kinetic** **pressure** **on** **Iran** (major new strike wave, sustained strategic bombing campaign, or **explicit** author forecast of **imminent** **orders** **—** **not** **standing** **blockade** **rhetoric** **alone** **unless** **the** **author** **ties** **it** **to** **a** **new** **kinetic** **chapter*).

**Tier discipline:** Ingest lines remain **hypothesis-grade** until **wires** / **Pentagon-primary** / **named** **operational** **receipts**. This file **does not** **replace** **§1h** **IRI** **watch** **or** **Islamabad** **framework** **—** **it** **indexes** **commentator** **forecasts**.

## How to use

1. When a **`thread:<expert_id>`** **ingest** **states** **a** **directional** **view** **on** **this** **object**, **append** **one** **row** **to** **the** **rolling** **table** **below** **(or** **revise** **the** **same** **week** **if** **the** **same** **author** **updates** **stance)**.
2. If the author **does** **not** **address** **U.S.–Iran** **kinetic** **risk** **that** **week**, **no** **row** **—** **or** **explicit** **`N/A`** **in** **batch-analysis** **when** **you** **need** **a** **negative** **cell**.
3. **Optional** **`verify:`** **tail** **on** **inbox** **lines:** **`us-iran-kinetic:↑|↓|—|N/A`**.

## Rolling table (operator-maintained)

| Week / date | `expert_id` | Direction | Horizon (author) | Source (inbox / URL) | Notes |
|-------------|-------------|-----------|------------------|----------------------|-------|
| *— example —* | *`davis`* | *↑* | *near term* | *`daily-strategy-inbox.md` `thread:` row* | *Replace with real rows* |

_Add rows above the example or delete the example row when the first real row lands._

## Batch-analysis template

Use **after** the **last** **relevant** **`thread:`** **ingest** **in** **a** **multi-author** **bundle** **for** **the** **same** **calendar** **day** **(or** **same** **weave** **unit)**:

```text
batch-analysis | YYYY-MM-DD | US–Iran kinetic — author lattice | **Tension-first:** summarize **↑ / ↓ / — / N/A** **per** **named** **`thread:`** **(only** **where** **Iran** **kinetic** **load-bearing).** **Do** **not** **merge** **Hormuz** **rhetoric**, **Lebanon** **ceasefire**, **and** **hypothetical** **major** **strike** **into** **one** **Judgment** **without** **tier** **tags.** **Falsifiers:** **Pentagon** **readout**, **CENTCOM** **/** **named** **orders**, **wire** **strike** **reports** **—** **hypothesis-grade** **until** **receipts.** | crosses:us-iran-kinetic-lattice
```

**Note:** **`crosses:`** **here** **is** **a** **thematic** **label** **—** **not** **always** **two** **`expert_id`s** **(see** **[strategy-commentator-threads.md](strategy-commentator-threads.md)** **Crossing** **rules).** **Prefer** **explicit** **author** **list** **in** **the** **batch** **body** **text.**

## Related

- [strategy-commentator-threads.md](strategy-commentator-threads.md) — **Author threads: predictive accuracy and opinion drift**
- [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) — **§1h** state / MFA lane
- [islamabad-operator-index.md](../islamabad-operator-index.md) — bargaining framework (not substitute for kinetic ORBAT)
