# Self-memory audit (multi-dimension)

**Canonical template:** [memory-template.md](memory-template.md) · **Path:** `users/[id]/self-memory.md` · **Authority:** [AGENTS.md](../AGENTS.md) (MEMORY is not the Record).

Use **one row per dimension** in the summary table. Each dimension is a separate lens so a clean score on one axis does not hide failure on another.

**Governance:** This audit does **not** merge into SELF or EVIDENCE. Findings that are durable knowledge or identity → **RECURSION-GATE** candidate only, after companion approval.

---

## Dimension 1 — Governance and hierarchy (authority)

**Question:** Does anything in MEMORY **claim** or **imply** authority over SELF, EVIDENCE, or the gate?

**Checks**

- Lines that read like **durable facts**, **identity**, or **IX-style knowledge** not reflected in `self.md`, or that **contradict** SELF.
- **Pipeline smuggling:** content that behaves like a gate candidate (LEARN / CUR / PER) but exists only in MEMORY.
- **Provenance:** verbatim companion quotes presented as canonical truth without a gate path.

**Pass signal:** File reads as continuity and meta; in-character truth lives in SELF / EVIDENCE or is explicitly deferred.

---

## Dimension 2 — Horizon architecture and lifespan (structure + decay)

**Question:** Are the three horizons used as intended, and does decay policy match reality?

**Checks**

- Headers: prefer exact `## Short-term`, `## Medium-term`, `## Long-term` (memory-template §VI). Legacy shapes note **loss of bucketing** for Voice and pruning.
- **Placement:** short = session/day; medium = open loops / labeled hypotheses; long = **meta only** (pointers, rotation habits), not stable facts.
- **Lifespan** (memory-template §IV): short hours–2 days; medium days–few weeks; long until revised (quarterly review). Compare `Last rotated:` and entry dates to staleness.
- **Promotion rule** (§II): content that survived weeks and sounds like Record → should be **gated**, not parked in long-term MEMORY.

**Pass signal:** Density matches horizon roles; stale short/medium is trimmed or promoted intentionally.

---

## Dimension 3 — Content boundary (Record leakage vs allowed scope)

**Question:** Does any line violate the allowed / avoid matrix (memory-template §III)?

**Checks**

- Short-term: tone, thread, calibrations, resistance — not IX-A facts or IX-B interests as if permanent.
- Medium-term: open loops, coordination — not a copy of SELF.
- Long-term: process/pointers — not knowledge or personality claims.

**Technique:** Tag paragraphs as **continuity**, **hypothesis**, **meta-pointer**, or **Record-shaped**. **Record-shaped** lines in MEMORY are findings (stage or delete).

**Pass signal:** Forbidden categories are empty or explicitly labeled as hypotheses pending gate.

---

## Dimension 4 — Mechanical and template health (parseability + hygiene)

**Question:** Will tooling and humans reliably read and maintain this file?

**Checks**

- **Dream normalization:** `python3 scripts/auto_dream.py -u <id> --dry-run` — note `self_memory.changed` vs `blank_lines_collapsed` (see *Telemetry note* below).
- **Markdown hygiene:** broken fences, orphan bullets, duplicate top-level `##` headers, huge pasted blocks.
- **Voice caps:** [bot/core.py](../bot/core.py) loads horizons with per-section line caps (`_MEMORY_MAX_LINES`: short 45, medium 28, long 18 after filtering). Count filtered lines per bucket if the file grows.

**Pass signal:** Structure matches loader expectations; substantive lines stay under caps.

### Telemetry note (dream / normalize)

`normalize_self_memory_content` may report `blank_lines_collapsed > 0` while `changed` is **False** for the on-disk file: the rebuild + collapse path can round-trip to **byte-identical** text. Treat **non-zero collapsed** with **changed False** as “normalizer ran; no write needed,” not as a pending edit.

---

## Optional fifth dimensions

- **Cross-surface duplication:** same fact or loop in MEMORY and `session-transcript.md` or operator notes — pick a single ephemeral source of truth.
- **Operational alignment:** medium-term open loops match coffee / handoff / work-history; else MEMORY may be decorative.
- **Integrity:** `python3 scripts/validate-integrity.py --user <id> --json` for path / manifest drift affecting the user dir.

---

## Audit summary table (copy per run)

| Dimension | Pass / watch / fail | Notes (section or line) |
|-----------|---------------------|-------------------------|
| 1 Hierarchy | | |
| 2 Horizons + lifespan | | |
| 3 Content boundary | | |
| 4 Mechanical | | |

---

## Completed run: `grace-mar` (2026-04-05)

**Target file:** [users/grace-mar/self-memory.md](../users/grace-mar/self-memory.md)  
**Cross-checks:** Overlap spot-check vs [users/grace-mar/self.md](../users/grace-mar/self.md) and EVIDENCE for **Bach Goldberg Variations** / **Tchaikovsky Andante cantabile** (merged LEARN/CUR; ACT-0038/0039).  
**Voice load (filtered lines):** short 7 / cap 45, medium 1 / cap 28, long 2 / cap 18 — all **under cap** (`bot/core.py` semantics).  
**Dream dry-run:** `integrity ok`, `governance ok`; `self-memory changed: False`, `blank_lines_collapsed: 3`, `deduped lines: 0` (idempotent normalize; see Telemetry note).

| Dimension | Result | Notes |
|-----------|--------|--------|
| 1 Hierarchy | **Pass** | Header states non-Record; long-term points to `self.md`, `self-archive.md`, gate path. Recent Topics bullet **does not contradict** SELF — music listening is already in IX / EVIDENCE from 2026-02-24 merges. No pipeline-only smuggling observed. |
| 2 Horizons + lifespan | **Watch** | Correct `## Short-term` / `## Medium-term` / `## Long-term`. `Last rotated: 2026-04-05` is current. **Short-term** still carries a **2026-02-24** listening note — older than template short horizon (hours–2 days); recommend **clear or refresh** now that Record carries the same facts (continuity-only redundancy). Medium-term is placeholder-only (acceptable). |
| 3 Content boundary | **Pass** | Recent Topics line is **explicitly framed** as thread continuity with pointer to EVIDENCE + SELF; not smuggling IX as MEMORY-only truth. Long-term stays meta (rotation + pointers). |
| 4 Mechanical | **Pass** | Valid horizon headers (`scripts/record_index.py` index). Subsections under Short-term (`### Tone`, etc.) parse under short bucket. No broken markdown. Dream dry-run clean aside from collapsed-line metric quirk above. |

**Optional — duplication:** No matching string in `session-transcript.md` for that music line (low cross-surface dup risk).

**Suggested follow-up (operator, not gated unless new facts):** Trim or replace the stale Short-term bullet with a lighter pointer (or empty Recent Topics) to reduce redundancy with the Record.
