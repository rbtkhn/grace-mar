# Pomodoro and timeboxing (operator playbook)

**Purpose:** Optional **WORK** guidance for structuring **focused intervals** inside the **~2-hour screen-based learning ceiling** described in [alpha-school-reference](../skill-work-alpha-school/alpha-school-reference.md) and [alpha-mastery-adaptation](../../alpha-mastery-adaptation.md). This doc is **operator doctrine**, not Record truth and not a product spec.

**Audience:** Operators using **work-dev**, deep coding blocks, or **Record-derived lesson** threads who want a simple, widely known time-management pattern.

**Disclaimer:** Interval lengths are **choices**, not medical or ergonomic advice. Adjust to your context, energy, and accessibility needs.

---

## What “Pomodoro” refers to

The **Pomodoro Technique** (popularized by Francesco Cirillo) names focused work intervals separated by short breaks—often using a kitchen timer (the Italian word *pomodoro* means “tomato,” from tomato-shaped timers). Companion-self does **not** ship a timer; this file only describes how the pattern can align with existing design language (2-hour block, mastery-at-edge, gate).

---

## Classic pattern

| Phase | Typical duration | Role |
|-------|------------------|------|
| Focused work | **25 minutes** | One task, one thread of attention |
| Short break | **5 minutes** | Reset (stretch, water, look away); avoid starting new work |
| Repeat | **4 cycles** | Then take a **longer break** (often **15–30 minutes**) |

**Interruptions:** Note the distraction briefly, return to the timer when possible; finishing the focus block before switching context is the usual discipline (adapt if your safety or duty context requires otherwise).

---

## Fitting roughly inside a 2-hour ceiling

The template’s **2 hours** is a **ceiling** for screen-based academic work, not a quota to fill. One way to map classic Pomodoros:

- **4 × 25 min** focused work ≈ **100 minutes**
- **3 × 5 min** short breaks (between those four blocks) ≈ **15 minutes**
- **1 × 15–25 min** longer break after the fourth block ≈ **15–25 minutes**

**Total ≈ 130–140 minutes**, i.e. in the same **order of magnitude** as a **2-hour design block** including breaks. Operators may use **fewer** Pomodoros, **shorter** breaks, or **shorter** focus intervals to stay **under** 120 minutes of clock time if that is the day’s goal.

---

## Variants (especially coding and deep work)

| Pattern | Work / break | When it can help |
|---------|--------------|------------------|
| **50 / 10** or **52 / 17** | Longer focus, short recovery | Debugging, algorithm work, deep reading |
| **40 / 10** | Balanced | Sustained coding with regular reset |
| **30 / 5–10** | Common adaptation | Programming flow with slightly longer focus than classic |

Tradeoff: longer focus blocks can raise **depth** but also **fatigue** and context cost. Pick explicitly; change the next day if the log shows drift or burnout.

---

## Record-derived lessons and one-line timeboxing

When pasting a lesson prompt built from the **minimal shape** in [schema-record-api.md](../../schema-record-api.md) (Record-derived lesson prompt), the operator may **append one optional sentence**, for example:

- “Treat **this activity** as one **25-minute** focus block; pause at the timer and summarize one line for logging.”
- “Today’s thread stays within a **2-hour** ceiling; pace **3–5** short activities with breaks between.”

That keeps **knowledge boundary** intact (still only Record-sourced facts in the body of the prompt) while making **pacing** explicit for the external LLM.

---

## CS50-style or course-style chunking (examples only)

External curricula (e.g. [CS50x weekly structure](https://cs50.harvard.edu/x/)) are **not** imported here—only **chunking discipline**:

- **One Pomodoro** might mean: “write and run one small function,” “read one spec section,” or “one failing test → green.”
- **Heavier weeks** (memory, data structures) may justify **50/10**-style blocks **within** the same daily ceiling, not **in addition** to unbounded screen time.

Link courses as **reference**; any structured pathway in-repo belongs in separate **WORK** docs or **governed** proposals, not in this playbook.

---

## Governance alignment

- **Reflection** after a block is optional operator habit; **durable claims** about the companion still go through **RECURSION-GATE** and companion approval ([AGENTS.md](../../../AGENTS.md)).
- This playbook does **not** auto-stage candidates, merge SELF, or change Voice behavior.

---

## Related docs

- [alpha-school-reference.md](../skill-work-alpha-school/alpha-school-reference.md) — 2-hour target, Record-driven prompts
- [alpha-mastery-adaptation.md](../../alpha-mastery-adaptation.md) — Pomodoro-style blocks in the Alpha analogy table
- [schema-record-api.md](../../schema-record-api.md) — minimal lesson prompt shape
- [work-lesson-generation-walkthrough.md](../work-lesson-generation-walkthrough.md) — how lesson prompts are built
- [delegation-spec-external-agents.md](delegation-spec-external-agents.md) — external agent delegation outline (separate concern)
