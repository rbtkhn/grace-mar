# MEMORY — Self-memory (short / medium / long)

> Not part of the Record. SELF is authoritative. "Ephemeral" = non-gated and rotatable, not "only short-term." See docs/memory-template.md v2.0 (three horizons).

Last rotated: 2026-04-28

## Short-term

### Tone

Analytical register confirmed as Voice persona. Companion prefers structural-first, compression-oriented responses. Match judgment style: structural analysis first (power, incentives, constraints), narrative second.

### Recent Topics

- Record population from WORK data completed 2026-04-17: direct-write sections II (Preferences) and VI (Philosophy); batch-gated 6 IX-C personality entries and 7 IX-B curiosity entries. IX-A knowledge entries deferred — operator will seed manually in a future session.
- Strategy notebook active — April weaves through 04-17 (Araghchi, Davis, dual-register, weave skeletons S1-S5).
- Portability Wave 4B (MCP read-only adapter) shipped.
- Companion migration completed 2026-04-14: Abby frozen to cold storage, Robert seeded.

### Calibrations

- Batch-gate discipline confirmed for IX entries. Direct-write for structural metadata (sections I-VII).
- Operator uses "approve all" for batch review — no per-candidate friction needed.
- High trust in elicitation files (`docs/skill-work/work-elicitation/`) as IX-C source material — no second-guessing needed when those files are the basis for personality candidates.

### Resistance Notes

- **IX-A (Knowledge):** Operator explicitly declined all 5 proposed knowledge candidates (tri-mind framework, war powers, multi-expert synthesis, wire discipline, Islamabad framework). Do not re-propose IX-A population until the operator initiates it.

## Medium-term

- **Record gaps:** Sections III (Family), IV (Education), V (Health) are empty. Operator will populate III manually. IV and V not discussed — do not push.
- **IX-A deferred:** Knowledge section is empty by operator choice. The 5 rejected candidates were well-formed but deferred. May revisit in a future session if the operator brings it up.
- **self.md Status field:** Currently reads `SEEDING`. Should be updated to `ACTIVE` or equivalent once the operator considers the initial population complete.
- **Dev-journal state (work-dev):** Latest entry is [Day 2 (2026-04-11)](../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/2026-04-11-day-02.md). Day 2 "tomorrow" item still open: run a real Tri-Frame overlay on a fresh daily brief end-to-end. Day 2 friction: CLI flag growth on `generate_wap_daily_brief.py` — consider splitting into `daily_brief_minds_*.py` if it grows again. Journal is ~6 days behind the active work window (last entry 04-11 vs current 04-17) — next dev-journal day file should fold any accumulated inbox or reflect recent portability / MCP / reseed work. Inbox is currently empty.

## Long-term

- **Rotation:** prefer weekly prune of Short/Medium; review Long-term quarterly for drift into "shadow Record."
- **Durable truth:** `users/grace-mar/self.md`; activity spine: `self-archive.md` (EVIDENCE); operator threads: `self-work.md`.
- **Companion identity:** Robert (reseeded 2026-04-14, populated 2026-04-17). Previous companion Abby frozen in cold storage (`archive/companion-freeze-abby-2026-04-14/`, git tag `companion-freeze/abby-2026-04-14`).
- **Voice register:** Analytical — structural, precise, framework-oriented. Set in `bot/prompt.py` HOW YOU SPEAK section.
- **Dev-journal pointer:** [`docs/skill-work/work-dev/dev-notebook/work-dev/journal/`](../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md) (LIB-0155) — canonical surface for work-dev reflection and learning; check latest day file and inbox for work-dev continuity on reentry. Inbox: [`daily-dev-journal-inbox.md`](../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/daily-dev-journal-inbox.md). Fold at dream.
- **Promotion flow:** Medium-term items that survive rotation and look like stable identity, knowledge, or personality claims should be staged as CANDIDATE blocks in `recursion-gate.md`, not left in memory as shadow Record. Memory observes; the gate governs; SELF is authoritative. Pipeline: `self-memory` (observe/accumulate) → `recursion-gate` (stage + companion review) → `self.md` IX-A/B/C (Record truth). See `docs/memory-template.md` v2.0 § II Promotion rule.
