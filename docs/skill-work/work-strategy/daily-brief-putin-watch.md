# Putin — last 48 hours (good morning / daily brief)

**Purpose:** Standing **operator WORK** slice for the daily brief: **Vladimir Putin’s public statements and visible activity** in a **rolling 48-hour** window (not Record truth, not Voice knowledge).

**When:** Each **good morning** pass that runs the [daily-warmup skill](../../../.cursor/skills/daily-warmup/SKILL.md) should include a **compact block** (bullets + URLs) in the operator reply. After `generate_work_politics_daily_brief.py`, **§1d** in the generated file is the canonical paste target (see generator output).

---

## What to cover

- **Scheduled appearances** (Kremlin events, forums, phone calls) with **date/time (UTC if possible)**.
- **Quoted lines** that move policy or negotiation framing — attribute to **wire or official transcript**, not paraphrase-only.
- **Domestic security / military** remarks if they are new in the window.
- If **nothing material** in 48h: one line — *“No major new Putin statements located in window; see Kremlin feed for minor events.”*

## Canonical surfaces (bookmark)

| Surface | URL | Notes |
|--------|-----|--------|
| Kremlin — events / transcripts | [kremlin.ru/events/president](http://kremlin.ru/events/president) | Primary for official wording |
| Reuters — Russia / Ukraine | [reuters.com/world](https://www.reuters.com/world/) | Cross-check time and phrasing |
| BBC — Russia / Ukraine | [bbc.com/news/world](https://www.bbc.com/news/world) | |
| TASS (English) | [tass.com](https://tass.com/) | State wire; label as such |
| RIA Novosti | [ria.ru](https://ria.ru/) | Russian-language; use with attribution |

## Guardrails

- **Cite URLs** for each bullet used in client-facing or posted material.
- **Do not** merge into SELF, EVIDENCE, or `bot/prompt.py` without the gated pipeline.
- **RSS §2** of the daily brief may surface Putin-adjacent headlines; it **does not** replace this pass (timing, full quotes, Kremlin schedule).

---

**Last procedure refresh:** 2026-03-28
