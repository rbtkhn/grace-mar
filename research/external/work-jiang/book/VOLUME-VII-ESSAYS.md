# Predictive History — Volume VII: Essays

**Book line:** Volume VII is a **full volume** of the **Predictive History** multivolume book: the **Essays** corpus — **written newsletter** posts (primary publication [Predictive History on Substack](https://predictivehistory.substack.com/)), distinct from **YouTube lectures** (Volumes I–V) and **long-form interviews** (Volume VI).

**Scope:** Volume VII includes **essays** Jiang publishes under the **Predictive History** brand — paid and free on Substack — as **operator-curated mirrors** in-repo for search, analysis, and crosswalk to lectures. Editorial discipline matches other volumes: Part I follows the corpus in **publication order**; Part II method TBD as the lane matures.

**Corpus:** `research/external/work-jiang/substack/essays/<slug>.md` — filename = Substack post slug (`/p/<slug>`). Each file has YAML front matter (`source_kind: substack_essay`, `publication_date`, `canonical_url`, …). See [substack/essays/README.md](../substack/essays/README.md).

**Registry (book-track):** `es-01` … `es-NN` in [`metadata/sources.yaml`](../metadata/sources.yaml) — publication order (front matter `publication_date`, tie-break slug), emitted by `scripts/work_jiang/build_source_registry.py` from `substack/essays/*.md` plus `analysis/essay-<slug>-analysis.md`. Chapters `es-chNN` live in [`metadata/book-architecture.yaml`](../metadata/book-architecture.yaml) (`volume_7_essays`); [`metadata/source-map.yaml`](../metadata/source-map.yaml) maps `es-chNN` → `[es-NN]`. Conventions: [volume-vii-book-track-conventions.md](../../../docs/skill-work/work-jiang/volume-vii-book-track-conventions.md). Crosswalk remains [substack/README.md](../substack/README.md).

**Analysis memos:** `research/external/work-jiang/analysis/essay-<slug>-analysis.md` — same memo sections as lecture analyses (`thesis`, `claims`, lattice, cross-refs). `normalize_analysis_frontmatter.py` does **not** auto-fill these (no YouTube id in filename).

**Chapter order:** Substack **`publication_date`**, earliest → latest (tie-break: slug). **Essay #N** is **ordinal in the ingested set** for a given operator snapshot — not an official episode number unless you add one in front matter.

## Corpus snapshot (on-disk)

| Pattern | Location |
|---------|----------|
| Essay text | `substack/essays/<slug>.md` |
| Theme ↔ lecture map | `substack/README.md` (one section per tracked post) |
| Analysis | `analysis/essay-<slug>-analysis.md` |

## Relation to other volumes

| Volume | Corpus | Notes |
|--------|--------|-------|
| VII | **Essays** (written) | Newsletter on Substack; `substack/essays/` — complements **VI** (dialogue on others’ channels) and **I–V** (classroom lectures) |

See [VOLUME-VI-INTERVIEWS.md](VOLUME-VI-INTERVIEWS.md) for Volume VI scope.
