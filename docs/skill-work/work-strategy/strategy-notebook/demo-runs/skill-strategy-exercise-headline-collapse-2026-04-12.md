# Exercise 1 — headline collapse (clean-room example)

**Series:** skill-strategy exercise · **Date:** 2026-04-12  
**Purpose:** Validate tagged rewrite vs synthetic wire mashup (no real attributions in the **input** paragraph).

---

## Synthetic input (adversarial mashup — **do not** treat as reporting)

The Vatican called for an immediate de-escalation across all theaters while the White House said the framework was holding and Tehran would soon accept inspections; the Kremlin warned any blockade would destabilize energy markets and Beijing urged restraint through existing UN channels, adding that unilateral steps complicated dialogue, and Iran’s foreign ministry said foreign warships had no place in regional waters and that prior understandings remained the baseline for talks.

---

## Tagged bullets (example completion — **Exercise 1** output)

| Thread | Paraphrase | Verify needed |
|--------|------------|---------------|
| **ROME** | Holy See line: de-escalation across theaters (moral–diplomatic register). | Yes — **vatican.va** / Bollettino primary for exact text; not merged with WH/Kremlin facts. |
| **VP / WH** | U.S. executive frame: “framework holding”; Iran inspections timeline (as summarized). | Yes — **WH readout** / full quote; “soon” is a claim class. |
| **Kremlin** | Russia warns blockade → energy market instability. | Yes — **Kremlin.ru** or dated transcript for “blockade” wording. |
| **PRC / MFA** | China urges restraint via UN; unilateral steps complicate dialogue. | Yes — **MFA** English page or dated briefing. |
| **IRI / MFA** | Iran: foreign warships out of regional waters; prior understandings = baseline for talks. | Yes — **MFA / IRNA / Tasnim** primary; **not** conflated with Islamabad scaffold text. |

**Headline-stack check:** Input merges planes in one paragraph; output **does not** merge — bullets separate channels (**HS** pass for this artifact).

**Optional Thesis A / B:** *Thesis A — Diplomatic hold:* frameworks and talks continue under coercive backdrop. *Thesis B — Maritime / scope fight:* “regional waters” vs “blockade” definitions may be the real fault line — keep **separate** until primaries align.

---

## Links (exercise artifact)

- [`EXERCISE-PROMPTS.md`](EXERCISE-PROMPTS.md) — Exercise 1 definition  
- [`skill-strategy-exercise-rubric-reference.md`](skill-strategy-exercise-rubric-reference.md) — **FT**, **HS**  
- [`../../daily-brief-native-international-pass.md`](../../daily-brief-native-international-pass.md) — native-language triangulation
