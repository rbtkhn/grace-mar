# Predictive History — Volume II (Civilization) systematic audit

**Operator WORK** — not Record. **Date:** 2026-04-02 (assistant run). **Scope:** `volume_2_civilization` in `metadata/book-architecture.yaml`, `civ-ch01`–`civ-ch60`, evidence packs, registries, `sources.yaml` `civ-*`.

**Method:** Same three-audit frame as Volume I Geo-Strategy review: (1) thesis–claim graph, (2) evidence pack ↔ chapter queue alignment, (3) cross-lecture contradiction / drift. Automated checks + repo reads; **no** full transcript pairwise comparison (would need a dedicated long-context pass).

---

## Executive summary

- **Audit 1 (thesis–claim):** **Major gap.** `thesis-map.yaml` has **no** `civ-ch*` references; `claims.jsonl` has **zero** rows with `chapter_candidates` including any `civ-chNN`. Volume II is **not** on the integrated thesis/claims spine yet.
- **Audit 2 (packs ↔ queue):** **Pass** on structure — **60/60** chapters in YAML, **60/60** `source-map.yaml` entries match `source_ids`, **60/60** evidence packs on disk (`evidence-packs/civ-chNN.md`). Packs are **scaffold** quality: analysis sections empty, no linked divergences/predictions in registry metadata for `civ-*`.
- **Audit 3 (cross-lecture drift):** **Blocked / deferred.** Without analysis memos (almost all `civ-*` still `analysis: missing`), a **contradiction matrix** cannot be built from the argument layer. **Thematic** arc spans agriculture origins → American empire (lecture 60); expect **tone and frame shifts** — flag for **human or long-context** read when analyses exist.

---

## Scope

| Read | Coverage |
|------|----------|
| `metadata/book-architecture.yaml` | `volume_2_civilization` |
| `metadata/source-map.yaml` | `civ-ch01`–`civ-ch60` |
| `evidence-packs/civ-ch*.md` | existence + spot-check `civ-ch01`, `civ-ch60` |
| `metadata/thesis-map.yaml` | grep `civ-ch` / `civ-` linkage |
| `claims/registry/claims.jsonl` | `chapter_candidates` ∩ `civ-ch*` |
| `metadata/concepts.yaml` | `chapter_ids` / `source_ids` for Volume II |
| `metadata/prediction-links.yaml`, `divergence-links.yaml` | `civ-*` |
| `metadata/sources.yaml` | `civ-*` analysis status |

**Truncated:** Full lecture text (60 files) not diffed for contradictions in this pass.

---

## Findings table

| id | Audit | Layer | Severity | Location | Issue | Suggested fix (optional) |
|----|-------|--------|----------|----------|--------|--------------------------|
| V2-001 | 1 | thesis / claims | **major** | `metadata/thesis-map.yaml` | No thesis subclaims or pointers reference `civ-chNN` or Civilization arc. | When Volume II thesis is drafted, add subclaims + `linked_claim_ids`; wire claims with `chapter_candidates: [civ-chNN]`. |
| V2-002 | 1 | claims registry | **major** | `claims/registry/claims.jsonl` | No claims tag `civ-ch*` in `chapter_candidates`. | Extract claims from future `analysis/*.md` for `civ-*`; run claim-linking workflow. |
| V2-003 | 1 | concepts | **minor** | `metadata/concepts.yaml` | No `civ-ch` in concept `chapter_ids` (spot-check / grep). | Tag concepts as Civilization memos and packs mature. |
| V2-004 | 2 | evidence pack | **observation** | `evidence-packs/civ-ch*.md` | All packs list core source + excerpt; **Core analysis** empty; blockers note missing analysis memo. | Expected for `outline_pending` — complete analysis per source, regenerate packs. |
| V2-005 | 2 | registries | **major** | `prediction-links.yaml`, `divergence-links.yaml` | No `civ-*` entries found (Volume II uses **divergence** Part II, not predictions). | Add `divergence_links` rows for `civ-*` as Part I divergence boxes are curated. |
| V2-006 | 3 | lecture / analysis | **major** | `metadata/sources.yaml` `civ-*` | **59** of **60** sources still `analysis: missing` (1 may be complete — re-run registry if needed). | Prioritize analysis backlog for `civ-01` onward; then re-run audit 3 on memos + lectures. |
| V2-007 | 3 | narrative arc | **observation** | Lectures #1 vs #60 titles | Arc moves from **origins of agriculture** to **decline of American empire** — large scope; risk of **implicit frame drift** across Parts. | In book outline, add explicit bridge sections (Part I mid-point recap / through-lines). |

---

## Cross-cutting themes

1. **Volume II is structurally wired but argument-light** — YAML, maps, and packs align; **thesis, claims, divergences, and concepts** still Geo-centric.
2. **Part II contract is divergence, not predictions** — empty prediction links for `civ-*` is **consistent**; absence of **divergence** links is the real gap for end-of-chapter boxes.
3. **Analysis is the bottleneck** — until `civ-*` memos exist, audits 1 and 3 cannot reach “book-ready” depth.

---

## Status (pilot `civ-01` / `civ-ch01`, 2026-04-02)

| Audit id | Prior severity | After pilot |
|----------|----------------|-------------|
| **V2-001** | major | **Partially addressed** for `civ-ch01` only — thesis subclaim `t04` links `clm-0031`–`clm-0034`; other `civ-ch*` chapters still off-spine. |
| **V2-002** | major | **Partially addressed** — four claims with `chapter_candidates: [civ-ch01]`; remaining 59 chapters have no claims yet. |
| **V2-003** | minor | **Partially addressed** — selected concepts tagged with `civ-01` / `civ-ch01`; bulk retagging deferred. |
| **V2-004** | observation | **Partially addressed** for `civ-ch01` — Core analysis path populated; other packs unchanged. |
| **V2-005** | major | **Partially addressed** — `div-CIV01-001` linked via generated `divergence-links.yaml`; `civ-02+` still open. |
| **V2-006** | major | **Partially addressed** — `civ-01` analysis complete; **59** sources still `analysis: missing`. |
| **V2-007** | observation | **Open** for full arc execution — operator doc added (`chapters-volume-ii/VOLUME-II-ARC-THROUGH-LINES.md`); not yet reflected in drafted chapter prose. |

All other Volume II scope items from the pre-pilot executive summary remain **open** until repeated for additional sources.

---

## Recommended next audit

After **≥10** Civilization analysis memos exist with claim extraction: re-run **audit 1** (thesis–claim linkage) and **audit 3** (memo-level contradiction matrix for overlapping claims on agriculture, religion, empire, modernity).

---

*Generated for operator continuity. Re-run or extend with `python3` checks + manual thesis edits as Volume II matures.*
