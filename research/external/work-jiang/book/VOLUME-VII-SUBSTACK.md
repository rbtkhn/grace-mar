# Predictive History — Volume VII: Substack Essays

**Book line:** Volume VII is a **full volume** of the **Predictive History** multivolume book: the **written** newsletter / essay corpus on [Predictive History (Substack)](https://predictivehistory.substack.com/), distinct from **YouTube lectures** (Volumes I–V) and **long-form interviews** (Volume VI).

**Scope:** Volume VII includes **Substack posts** Jiang publishes under Predictive History — paid and free — as **operator-curated mirrors** in-repo for search, analysis, and crosswalk to lectures. Editorial discipline matches other volumes: Part I follows the corpus in **publication order**; Part II method TBD as the lane matures.

**Corpus:** `research/external/work-jiang/substack/essays/<slug>.md` — filename = Substack post slug (`/p/<slug>`). Each file has YAML front matter (`source_kind: substack_essay`, `publication_date`, `canonical_url`, …). See [substack/essays/README.md](../substack/essays/README.md).

**Registry:** **Not** wired into `metadata/sources.yaml` by default (unlike `vi-*` / `gt-*`). Volume VII is tracked by **on-disk essays + crosswalk** [substack/README.md](../substack/README.md). Add `sources.yaml` rows later if you want prediction-registry or chapter-map parity with lectures.

**Analysis memos:** `research/external/work-jiang/analysis/ss-<slug>-analysis.md` — same memo sections as lecture analyses (`thesis`, `claims`, lattice, cross-refs). `normalize_analysis_frontmatter.py` does **not** auto-fill these (no YouTube id in filename).

**Chapter order:** **Substack `publication_date`**, earliest → latest (tie-break: slug). **Substack #N** is **ordinal in the ingested essay set** for a given operator snapshot — not an official Substack episode number unless you add one in front matter.

## Corpus snapshot (on-disk)

| Pattern | Location |
|---------|----------|
| Essay text | `substack/essays/<slug>.md` |
| Theme ↔ lecture map | `substack/README.md` (one section per tracked post) |
| Analysis | `analysis/ss-<slug>-analysis.md` |

## Relation to other volumes

| Volume | Corpus | Notes |
|--------|--------|--------|
| VII | **Substack essays** | Written surface; complements **VI** (dialogue on others’ channels) and **I–V** (classroom lectures) |

See [VOLUME-VI-INTERVIEWS.md](VOLUME-VI-INTERVIEWS.md) for Volume VI scope.
