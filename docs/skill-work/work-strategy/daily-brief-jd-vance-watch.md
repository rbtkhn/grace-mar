# JD Vance — last 48 hours (coffee menu C — Strategy (daily brief) / daily brief)

**Purpose:** Standing **operator WORK** slice for the daily brief: **J.D. Vance’s public statements and visible activity** (Vice President; prior Senate role when historically relevant) in a **rolling 48-hour** window (not Record truth, not Voice knowledge).

**When:** When the operator chooses **coffee menu C — Strategy (daily brief)** in the [coffee skill](../../../.cursor/skills/coffee/SKILL.md) (legacy **hey** still works): run the **web scan**, then write the **compact block** (bullets + URLs) into **§1e** (`## 1e. JD Vance — last 48 hours`) **in the daily brief file** after `generate_work_politics_daily_brief.py` (or when refreshing an existing today’s file). Step 1 **coffee** does **not** run this scan — it is part of **C** only.

---

## What to cover

- **Official VP / White House** readouts, joint appearances with the President, foreign travel, and **quoted lines** that move policy or coalition framing.
- **Congress-era** material only when it is **new in the window** or directly ties to a live national story (otherwise deprioritize).
- **KY-4 / principal adjacency:** when Vance’s lines intersect **Massie**, **war powers**, **spending**, or **MAGA coalition** dynamics the campaign tracks, note that tie in one bullet.
- If **nothing material** in 48h: one line — *“No major new Vance statements located in window; see White House / major wires for minor items.”*

## Canonical surfaces (bookmark)

| Surface | URL | Notes |
|--------|-----|-------|
| White House — briefings / remarks | [whitehouse.gov](https://www.whitehouse.gov/) | Official schedule and transcripts when posted |
| U.S. Senate — historical record | [senate.gov](https://www.senate.gov/) | Prior role; use when window-relevant |
| Reuters — U.S. politics | [reuters.com/world/us](https://www.reuters.com/world/us/) | Cross-check time and phrasing |
| Roll Call / The Hill | feeds in [daily-brief-config.json](daily-brief-config.json) | Congressional + VP-adjacent |

**Native-language triangulation:** When Iran (or other foreign capitals) is load-bearing for U.S.–Iran or VP travel threads, add **at least one Persian-language outlet bullet** (IRNA / Tasnim / Fars, etc.) with URL and **state vs independent** note — see [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md).

## Guardrails

- **Cite URLs** for each bullet used in client-facing or posted material.
- **Do not** merge into SELF, EVIDENCE, or `bot/prompt.py` without the gated pipeline.
- **RSS §2** of the daily brief may surface Vance-adjacent headlines; it **does not** replace this pass (timing, full quotes, official wording).

---

**Last procedure refresh:** 2026-04-12
