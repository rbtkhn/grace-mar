# Weekly brief template — work-politics

Use this structure when the companion requests a weekly brief. Fill each section with cited, documented content.

---

## Week of [DATE RANGE]

### 0. Recency slice (required each cycle)

- **Window:** last **7** or **30** days (circle one).
- **Rule:** At least **3** bullets in §1–§4 must be **only** from that window (with date or link proving recency).
- **Logged:** `Recency: 7d \| 30d · assembled [DATE]` — see [brief-source-registry § Recency pass](brief-source-registry.md#recency-pass-last-730-days).

---

### 1. Headlines (principal-relevant)

- 2–5 bullets: national or KY-4 news that affects the principal (votes, Iran, Epstein, Trump, Gallrein, district).
- **Source:** [link or publication].

---

### 1b. Geopolitical & military (live + analysis)

- Use the daily brief generator’s **§2a** (*G-ranked* defense / world / conflict headlines) as the **live** spine.
- Add **one paragraph of operator analysis**: what it implies for KY-4 messaging (e.g. war powers, restraint, spending, alliances) — tie to [principal-profile](principal-profile.md) and [analytical-lenses](analytical-lenses/manifest.md), not unsourced speculation.
- **Sources:** URLs from RSS rows; verify numbers and quotes before ship.

---

### 1c. Civ-mem depth (structural evidence — not breaking news)

- Run `python3 scripts/build_civmem_inrepo_index.py build` if needed; use **§2b** from the daily brief (*civ-mem depth hooks*) or query the index for overlaps with your §1 / §1b themes.
- Use MEM-style parallels to **strengthen logic** (long-horizon patterns, institutional mechanics). Tag provenance `{CMC: path}` per [civ-mem-draft-protocol](civ-mem-draft-protocol.md).
- **Does not** satisfy §0 recency requirements and **does not** replace dated news citations for campaign facts.

---

### 2. Principal (Massie)

- Votes or statements this week (with links).
- Media hits or social highlights.
- **Source:** Congress.gov, principal’s X, news.

---

### 3. Opposition

- Gallrein: events, ads, messaging, spend (if known).
- Trump / MAGA: visits, endorsements, attacks.
- **Source:** FEC, news, social.

---

### 4. Social / narrative

- What’s trending about the race or the principal (X, local FB, etc.); narrative to reinforce or push back on.
- **Source:** [where you looked].

---

### 5. Key dates this week

- From [calendar-2026.md](calendar-2026.md): registration, FEC, early vote, primary, or other.
- District or legislative events if relevant.

---

### 6. Suggested X / message angles (drafts on request)

- 1–3 angles the shadow account could use this week (e.g. “war powers vote,” “early vote reminder”).
- Companion requests draft tweets/threads as needed.

---

### 7. Triangulation — analytical lenses (mandatory for full briefs)

Run **after** §0–§6 drafts exist or in parallel on the same **neutral fact summary** (dated, sourced bullets shared across lenses).

1. **Structural (long horizon)** — [analytical-lenses/lens-structural-realism.md](analytical-lenses/lens-structural-realism.md)  
2. **Operational / diplomatic (near term)** — [analytical-lenses/lens-operational-diplomatic.md](analytical-lenses/lens-operational-diplomatic.md)  
3. **Institutional / domestic** — [analytical-lenses/lens-institutional-domestic.md](analytical-lenses/lens-institutional-domestic.md)

**Synthesis (operator / Grace-Mar core):**

- Highlight **convergence** (high-confidence shared implications).
- **Surface productive tensions** — where lenses disagree, say so explicitly (do not smooth over).
- Optional table format: Structural | Operational | Institutional | **Operator synthesis**
- Paste-ready block: [analytical-lenses/template-three-lenses.md](analytical-lenses/template-three-lenses.md)

**Governance:** Lenses are **WORK only**; see [analytical-lenses/manifest.md](analytical-lenses/manifest.md) (logging, no `self-evidence` trace dumps, human sign-off for ship).

---

### 8. High-stakes guardrail stress-test (when risk is elevated)

If §1–§7 (or the companion’s request) touches **war powers**, **congressional ethics / insider-trading**, **cartel-economy claims with legal bite**, or **border + civil liberties** in a volatile window — **before** final sign-off, complete a factorial stress-test brief:

- **Template:** [america-first-ky/stress-test-brief-template.md](america-first-ky/stress-test-brief-template.md)  
- **Method:** [america-first-ky/guardrail-stress-test.md](america-first-ky/guardrail-stress-test.md) (four failure modes, variation table, pass/fail)

**Scaffold (optional):** `python scripts/scaffold_stress_test_brief.py <issue-slug>` writes a dated copy under `america-first-ky/` (WORK only; does not touch the Record).

Low-stakes engagement posts can skip §8 unless the operator wants extra discipline.

---

*Agent fills this when you ask for “weekly brief for [date range].”*
