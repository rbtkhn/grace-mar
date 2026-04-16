# History Notebook

**Discoverability:** Linked from **`users/grace-mar/SELF-LIBRARY/history-notebook`** (repo-relative symlink when created). **LIB:** [LIB-0156](../../../../users/grace-mar/self-library.md#operator-analytical-books) in [`self-library.md`](../../../../users/grace-mar/self-library.md) (Operator analytical books).

**Operator-authored compressed chapters** distilling civilizational patterns into strategy-ready reference. Five temporal volumes; **target 20 chapters per volume (100 main-era chapters)**; each chapter ~500–1000 words. Not a mirror of CIV-MEM — an independent analytical layer the operator writes and the agent reads.

### Three layers (draft scaffolding)

Book identity and chapter IDs remain **SSOT** in [book-architecture.yaml](book-architecture.yaml) and PH wiring in [cross-book-map.yaml](cross-book-map.yaml). These folders are **additive** working layers fed by `civilization_memory` **as a reservoir** (read and distill; do not copy upstream trees):

| Layer | Location | Role |
|-------|----------|------|
| **Civilization threads** | [threads/](threads/) — `history-civ-*.md` | Longitudinal scratchpads: continuity, mechanism candidates, links to knots/chapters, open questions |
| **History knots** | [knots/](knots/) — `hn-knot-*.md` | Atomic mechanism units (many mem inputs → one knot; many knots → one chapter). **Not** strategy-notebook daily knots (LIB-0153) |
| **Chapters** | [chapters/](chapters/) + YAML ids | Finished comparative chapters (~500–1000w); cite **chapter ids** (`hn-i-v1-04`, …) from strategy-notebook **`### History resonance`** |

Flow: **CIV-MEM (reservoir) → threads → knots → chapters →** short resonance lines in [strategy-notebook](../strategy-notebook/README.md). Index: [knots/README.md](knots/README.md) (knot → chapter map).

- **Chapter format:** See [STYLE-GUIDE.md](STYLE-GUIDE.md)
- **Polyphonic drafting (operator):** [POLYPHONY-WORKFLOW.md](POLYPHONY-WORKFLOW.md) — CIV-MIND passes on a neutral spine, then public translation (no mind names in chapter prose)
- **Architecture SSOT:** [book-architecture.yaml](book-architecture.yaml) — all chapters, volumes, sub-groups, arcs
- **PH wiring SSOT:** [cross-book-map.yaml](cross-book-map.yaml) — sole source of truth for Predictive History ↔ History Notebook links
- **Growth model:** One volume at a time — design → write → validate
- **Strategy notebook (fast judgment):** [../strategy-notebook/README.md](../strategy-notebook/README.md) — daily **`### History resonance`** cites HN **chapter ids** and mechanism lines; see [STRATEGY-NOTEBOOK-ARCHITECTURE § Parallel to History notebook](../strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#parallel-to-history-notebook-lib-0156). Do not duplicate full chapters in `days.md`.

---

## Volume structure

| Volume | Era | Chapters |
|--------|-----|----------|
| **I — Ancient Empires** (to 476 CE) | Twenty **problem-led** chapters (comparative ancient evidence); see [research/VOL-I-PROBLEM-CHAPTERS.md](research/VOL-I-PROBLEM-CHAPTERS.md) | `hn-i-v1-01` … `hn-i-v1-20` (legacy civ draft: [chapters/vol-i/persia.md](chapters/vol-i/persia.md)) |
| **II — Medieval** (476–1453) | Post-Roman reconfigurations: Islam, Byzantium, Mongol disruption | islam, rome-byzantine, persia-islamic, mongol, china-medieval |
| **III — Early Modern** (1453–1789) | Ottoman peak, maritime expansion, continental consolidation | ottoman, anglia, france, russia |
| **IV — Industrial & Imperial** (1789–1945) | Revolution, total war, imperial collapse | america, germany, russia-imperial, anglia-imperial |
| **V — Contemporary** (1945–present) | Cold War, unipolarity, current crisis landscape | america-hegemonic, china-modern, russia-modern, persia-modern |
| **Appendix** | Methodology | method |

---

## Civilization arcs

Civilizations that span multiple volumes. The arc registry lives in `book-architecture.yaml`; chapters in each arc connect with cross-volume bridge prose (see [STYLE-GUIDE.md](STYLE-GUIDE.md#cross-volume-bridges-style-convention)).

| Arc | Chapters | Thread |
|-----|----------|--------|
| **Persian** | Vol I (`hn-i-v1-19`) → II → V | Tolerance → compression → siege governance. Vol I entry is the parity-buffer problem chapter. |
| **Roman** | Vol I (`hn-i-v1-04`, `hn-i-v1-05`) → II | Administration and expansion → persistence after territorial loss. |
| **Russian** | III → IV → V | Marginal resilience → rupture-regeneration → temporal compression. |
| **American** | IV → V | Constitutional republic → industrial hegemon → overextension. |
| **English** | III → IV | Maritime hegemony → managed decline. |
| **Chinese** | Vol I (`hn-i-v1-16` … `hn-i-v1-18`) → II → V | Cyclical reunification → bureaucratic maturity → patience as strategy. |

---

## PH wiring — "addresses all of Jiang's theories"

`cross-book-map.yaml` maps all 8 PH theses and 20 concepts to HN chapters. Validate coverage with:

```bash
python3 scripts/validate_cross_book.py
```

### Volume wiring checklist

When starting a new volume:

1. **Pre-map** — Open `cross-book-map.yaml` and assign the volume's chapters to the theses and concepts they will address. Set `coverage: partial` (or leave `stub` for concepts the volume doesn't touch).
2. **Write** — Draft chapters per [STYLE-GUIDE.md](STYLE-GUIDE.md). Formation dimensions are natural anchors for PH concepts: education-narrative → education, religious-legitimacy → religion, financialization-empire → economics.
3. **Validate** — Run `validate_cross_book.py`. Review coverage gaps and orphan chapters.
4. **Update** — Promote coverage values in `cross-book-map.yaml` as chapters are completed. Update chapter `status` in `book-architecture.yaml`.

One file to edit for wiring: `cross-book-map.yaml`. No changes to PH metadata; no operator-facing fields in chapter prose.

---

## Current chapters

| ID | Volume | Title | Status |
|----|--------|-------|--------|
| `hn-i-v1-01` | I | Legitimacy After Conquest | planned |
| `hn-i-v1-02` | I | Civilizational Endurance Under Defeat | planned |
| `hn-i-v1-03` | I | When Power Changes Shape | planned |
| `hn-i-v1-04` | I | Administration, Law, and the Long Run | planned |
| `hn-i-v1-05` | I | Expansion Ceilings, Glory, and Consolidation | planned |
| `hn-i-v1-06` | I | Sea Roads and Circulation Empires | planned |
| `hn-i-v1-07` | I | Inclusion, Occupation, Annihilation | planned |
| `hn-i-v1-08` | I | Institutions Against Genius | planned |
| `hn-i-v1-09` | I | Copying, Standardization, Selective Absorption | planned |
| `hn-i-v1-10` | I | From Subjects to Stakeholders | planned |
| `hn-i-v1-11` | I | Territorial Maximum, Strategic Maximum, Overreach | planned |
| `hn-i-v1-12` | I | Geography of Origin and Permanence | planned |
| `hn-i-v1-13` | I | Mechanism Failure at the Frontier | planned |
| `hn-i-v1-14` | I | Elite Defection and the Shape of Defeat | planned |
| `hn-i-v1-15` | I | Deflection and Ambivalence Toward Outside Orders | planned |
| `hn-i-v1-16` | I | Non-Native Rule, Hybridity, Peak, Exhaustion | planned |
| `hn-i-v1-17` | I | Fragmentation and Monopoly of Authority | planned |
| `hn-i-v1-18` | I | Corridors, Exchange, Legibility, Aftermath of Conquest | planned |
| `hn-i-v1-19` | I | Parity, Buffers, Exhaustion, Third Shock | planned |
| `hn-i-v1-20` | I | Collapse, Vacancy, Succession | planned |
| `hn-ii-islam` | II | Islam — Rashidun to Abbasid Caliphate | planned |
| `hn-ii-rome-byzantine` | II | Byzantium — Eastern Roman Survival | planned |
| `hn-ii-persia-islamic` | II | Persia — Post-Conquest to Timurid | planned |
| `hn-ii-mongol` | II | Mongol — Steppe Cycle and Disruption | planned |
| `hn-ii-china-medieval` | II | China — Tang to Ming | planned |
| `hn-iii-ottoman` | III | Ottoman — Rise to Stagnation | planned |
| `hn-iii-anglia` | III | England — Tudor to Colonial Order | planned |
| `hn-iii-france` | III | France — Bourbon to Revolution | planned |
| `hn-iii-russia` | III | Russia — Muscovy to Catherine | planned |
| `hn-iv-america` | IV | America — Republic to Global Hegemony | planned |
| `hn-iv-germany` | IV | Germany — Unification to Catastrophe | planned |
| `hn-iv-russia-imperial` | IV | Russia — Napoleonic Wars to Soviet | planned |
| `hn-iv-anglia-imperial` | IV | England — Pax Britannica to World Wars | planned |
| `hn-v-america-hegemonic` | V | America — Cold War to Overreach | planned |
| `hn-v-russia-modern` | V | Russia — Soviet Collapse to Putin | planned |
| `hn-v-persia-modern` | V | Persia — Islamic Republic to War Phase | planned |
| `hn-v-china-modern` | V | China — PRC to Belt and Road | planned |
| `hn-app-method` | Appendix | How Jiang Thinks — Methodology | planned |

---

## Conventions

- **Operator-authored**, not auto-generated — the value is in the compression and judgment
- **Independent growth** — adding a chapter does not require updating CIV-MEM; CIV-MEM growth does not require updating chapters (though it may prompt revision)
- **Inline pattern tags** (`[pattern:X]`) enable future script extraction of an axiom deck without building one now
- **WORK only** — not Record, not Voice knowledge unless gated
- **Public / operator boundary** — chapter prose is public; metadata lives in YAML only (see [STYLE-GUIDE.md](STYLE-GUIDE.md))
