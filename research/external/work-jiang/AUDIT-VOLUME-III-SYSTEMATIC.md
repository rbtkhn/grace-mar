# Predictive History — Volume III (Secret History) systematic audit

**Operator WORK** — not Record. **Date:** 2026-04-02 (assistant run). **Scope:** Secret History corpus (`sh-01`–`sh-28` in `metadata/sources.yaml`, `lectures/secret-history-*.md`), intended **Volume III** slot in the multivolume architecture, and parity with the Volume I–II audit frame.

**Method:** Same three-audit frame as Volume I / Volume II: (1) thesis–claim graph, (2) evidence pack ↔ chapter queue alignment, (3) cross-lecture contradiction / drift. Automated checks + repo reads; **no** full transcript pairwise comparison (would need a dedicated long-context pass).

---

## Executive summary

**Update (2026-04-02 — Volume III wired + `sh-01` pilot):** `volume_3_secret_history`, `source-map` `sh-ch01`–`sh-ch28`, validators, pack builder, and renders are **live**. Evidence packs **28/28** after regen. **Thesis** subclaim **`t05`** and **four** claims **`clm-0035`–`clm-0038`** anchor `sh-ch01`; **`div-SH01-001`** in divergences.

**Historical pre-implementation snapshot (for contrast):**

- **Structural:** Was **blocking** — no `volume_3_*` in YAML; validators skipped Secret History.
- **Audit 1:** Was **major gap** — no `sh-*` on thesis/claims spine.
- **Audit 2:** Was **fail** — no chapter rows, map entries, or packs.
- **Audit 3:** **Still largely deferred** — **27** of **28** sources remain `analysis: missing` / `chapter_mapping: not_started` after pilot (only **`sh-01`** complete).
- **Auxiliary:** `metadata/quote-candidates-secret-history.yaml` remains **outside** the core spine until explicitly linked in comparative workflow.

---

## Scope

| Read | Coverage |
|------|----------|
| `metadata/book-architecture.yaml` | **`volume_3_secret_history`** — `sh-ch01`…`sh-ch28` |
| `metadata/source-map.yaml` | **`sh-ch01`–`sh-ch28`** → `[sh-NN]` |
| `evidence-packs/sh-ch*.md` | **28/28** after `build_all_evidence_packs.py` |
| `metadata/thesis-map.yaml` | **`t05`** → `clm-0035`…`clm-0038` |
| `claims/registry/claims.jsonl` | **Four** rows for `sh-ch01` / `sh-01` (pilot) |
| `metadata/concepts.yaml` | **Three** concepts tagged `sh-01` / `sh-ch01` (pilot) |
| `metadata/divergence-links.yaml` | **`sh-01` / `sh-ch01`** via `div-SH01-001` (generated) |
| `metadata/sources.yaml` | **`sh-01`** analysis complete; **`sh-02`–`sh-28`** backlog |
| `book/VOLUME-III-SECRET-HISTORY.md` | Part II method **TBD**; corpus line updated to spine-wired |

**Truncated:** Full lecture text (28 files) not diffed for contradictions in this pass.

---

## Findings table

| id | Audit | Layer | Severity | Location | Issue | Suggested fix (optional) |
|----|-------|--------|----------|----------|--------|--------------------------|
| **V3-000** | 2 | book spine | **blocking** | `metadata/book-architecture.yaml`, `arch_chapters.py`, validators | Volume III not in nested volume list; no chapter IDs for Secret History. | Add `volume_3_secret_history` (name TBD) with `book.chapters` `sh-ch01`…`sh-ch28`; add `sh-chNN` → `[sh-NN]` to `source-map.yaml`; extend `VOLUME_BLOCK_KEYS` and `validate_argument_layer` / `validate_work_jiang` / `validate_comparative_layer` for `sh-ch*` + `` `sh-NN` `` pack pattern (mirror `civ-*`); add `emit_volume3_chapters_yaml.py` or generalize emitter. |
| **V3-001** | 1 | thesis / claims | **major** | `metadata/thesis-map.yaml` | No subclaims reference Secret History chapters or `sh-*` claims. | After pilot memo + claims exist, add subclaim(s) with non-empty `linked_claim_ids` (same constraint as Volume II). |
| **V3-002** | 1 | claims registry | **major** | `claims/registry/claims.jsonl` | No claims with `chapter_candidates` including `sh-chNN`. | Extract claims from future `analysis/*.md` for `sh-*`; follow Volume II pilot checklist in `volume-ii-book-track-conventions.md` (adapt naming to Volume III). |
| **V3-003** | 1 | concepts | **minor** | `metadata/concepts.yaml` | No `sh-ch` / `sh-` tags on concepts. | Tag 2–3 concepts per early lecture once memos exist; avoid bulk retagging prematurely. |
| **V3-004** | 2 | evidence pack | **major** | `evidence-packs/` | No `sh-ch*.md` files; nothing to regenerate from `build_evidence_pack.py` for Volume III. | Wire chapters + source-map, then scaffold packs (`build_evidence_pack` / `build_all_evidence_packs` once Volume III is in `all_chapters_flat`). |
| **V3-005** | 2 | registries | **major** | `prediction-links.yaml`, `divergences.jsonl` / `divergence-links.yaml` | No `sh-*` links. | **Decide Part II method** in `book/VOLUME-III-SECRET-HISTORY.md` (predictions vs divergence vs hybrid); then append registry rows consistent with that contract (Volume I-style predictions vs Volume II-style divergences). |
| **V3-006** | 3 | lecture / analysis | **major** | `metadata/sources.yaml` `sh-*` | **28** / **28** sources `analysis: missing`; **28** / **28** `chapter_mapping: not_started`. | Prioritize `sh-01` pilot memo + `analysis_path` + `status.analysis: complete`; set `chapter_mapping: complete` when `sh-ch01` is canonical. |
| **V3-007** | 3 | narrative arc | **observation** | Lectures #1 vs #28 titles | Arc moves from **how power works** / **collapse** through **evil, bureaucracy, imagination, ancient empires** to **Pax Judaica** — high interpretive load and controversy risk in Part II. | Add operator-facing **through-lines** doc (mirror `chapters-volume-ii/VOLUME-II-ARC-THROUGH-LINES.md`) after Part II method is chosen; mark checkpoint chapters (~10, ~20, ~28). |

---

## Cross-cutting themes

1. **Spine is live** — Repeat Volume II pilot pattern for **`sh-02+`** (`volume-iii-book-track-conventions.md`).
2. **Part II method unset** — Divergence boxes are **default** for Part I; Part II evaluation mode still **operator-locked** in `VOLUME-III-SECRET-HISTORY.md`.
3. **Analysis remains the scaling bottleneck** — **27** lectures still lack memos; contradiction matrix **deferred**.
4. **Quote bank** — `quote-candidates-secret-history.yaml` can be integrated when comparative rules need Secret History **high-priority** chapters (most `sh-ch*` are **exposition**).

---

## Status (pilot `sh-01` / `sh-ch01`, 2026-04-02)

| Audit id | Prior severity | After pilot + spine |
|----------|----------------|---------------------|
| **V3-000** | blocking | **Addressed** — `volume_3_secret_history`, `arch_chapters`, validators, emitter, renders. |
| **V3-001** | major | **Partially addressed** — `t05` links only `sh-01` claims; other chapters off-spine. |
| **V3-002** | major | **Partially addressed** — `clm-0035`–`0038`; **27** chapters have no claims yet. |
| **V3-003** | minor | **Partially addressed** — three concepts tagged for pilot; bulk retagging deferred. |
| **V3-004** | major | **Addressed** on structure — **28/28** packs; **`sh-ch01`** has Core analysis populated. |
| **V3-005** | major | **Partially addressed** — `div-SH01-001`; no prediction links for `sh-*` (consistent with default). |
| **V3-006** | major | **Partially addressed** — **`sh-01`** memo complete; **27** sources still `analysis: missing`. |
| **V3-007** | observation | **Partially addressed** — `chapters-volume-iii/VOLUME-III-ARC-THROUGH-LINES.md` added; drafted prose TBD. |

---

## Recommended next audit

1. **After spine wiring:** Re-run this checklist counts (expect **V3-000** / **V3-004** to move to **pass** on structure with scaffold packs).  
2. **After `sh-01` pilot** (memo, claims, thesis subclaim, registry row(s), regen pack): mirror Volume II **Status** table pattern for **V3-001**–**V3-006** partial credit.  
3. **After ≥10** Secret History analysis memos: re-run **audit 1** and **audit 3** (memo-level contradiction matrix for overlapping themes: power, evil, religion, empire).

---

## Related docs

- [`book/VOLUME-III-SECRET-HISTORY.md`](book/VOLUME-III-SECRET-HISTORY.md) — intent and setup checklist (update corpus line when promoting spine).  
- [`AUDIT-VOLUME-II-SYSTEMATIC.md`](AUDIT-VOLUME-II-SYSTEMATIC.md) — template audit; [`docs/skill-work/work-jiang/volume-ii-book-track-conventions.md`](../../docs/skill-work/work-jiang/volume-ii-book-track-conventions.md) — pilot checklist to generalize.  
- [`SERIES-NOTES.md`](SERIES-NOTES.md) — Volume III naming notes.

---

*Generated for operator continuity. Re-run or extend with `python3` checks + manual YAML edits as Volume III is promoted from corpus-only to book-track.*
