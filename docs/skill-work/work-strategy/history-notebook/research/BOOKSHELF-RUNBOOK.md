# Bookshelf runbook (History Notebook)

**WORK only;** not Record. This runbook describes **Bookshelf** — the **title-level seed catalog** (`bookshelf-catalog.yaml`) for building a personal reference shelf (target ~500 works) that **informs** [History Notebook](../README.md) chapter drafting. **Human overview (Bookshelf vs operator books):** [BOOKSHELF.md](BOOKSHELF.md). **Self-library container:** [LIB-0158 — Bookshelf](../../../../users/grace-mar/self-library.md#bookshelf) (owned print catalog — separate from [LIB-0156](../../../../users/grace-mar/self-library.md#operator-analytical-books) operator-authored chapters). It does **not** replace:

- [`book-architecture.yaml`](../book-architecture.yaml) — chapter SSOT  
- [`cross-book-map.yaml`](../cross-book-map.yaml) — Predictive History ↔ HN coverage truth  
- [`STATUS.md`](../STATUS.md) — **distillation queue** for the **next `hn-*` chapters to draft**

## What the Bookshelf files are

| Artifact | Role |
|----------|------|
| [`bookshelf-catalog.yaml`](bookshelf-catalog.yaml) | Bibliographic rows (`HNSRC-*`), **era** (+ optional **eras**), optional hints to `hn-*` and PH — **planning shelf** |
| [VOL-I-LIBRARY-SCAFFOLD.md](VOL-I-LIBRARY-SCAFFOLD.md) | Vol I only: **chapter × shelf** matrix + gap notes (drafting aid; not chapter SSOT) |
| **HN chapters** (`chapters/`, `hn-*`) | Operator-distilled ~500–1000w prose — **deliverable** |
| **STATUS.md** | Single queue for **which chapter to write next**; link from strategy-notebook `meta.md` |

**Rule:** Catalog rows **do not** automatically update `cross-book-map.yaml`. When a thesis/concept row moves toward `partial` / `full`, follow [STATUS.md § Coverage coupling](../STATUS.md) and the [README PH wiring checklist](../README.md#ph-wiring--addresses-all-of-jiangs-theories).

## Era upload order

Process the shelf in this **fixed sequence** (batches of **five titles** within each era):

1. **ancient**
2. **medieval**
3. **colonial** (operator label; maps mainly to early modern / maritime–colonial themes in Vol III)
4. **industrial**
5. **modern**

| `era` value | Typical HN volume hint (`hn_volume`) |
|-------------|--------------------------------------|
| `ancient` | `vol-i` |
| `medieval` | `vol-ii` |
| `colonial` | `vol-iii` (note cross-straddle to `vol-iv` in `notes` when needed) |
| `industrial` | `vol-iv` |
| `modern` | `vol-v` |

**Multiple temporal categories:** When a work **logically belongs** in more than one bucket (e.g. Gibbon’s narrative spans late antiquity and medieval Europe), set **`eras`** to the full list and keep **`era`** as the **primary** bucket (upload order, default shelf file). Example: `era: medieval` + `eras: [ancient, medieval]`. Omit **`eras`** when a single category is enough.

### Era boundaries (Bookshelf rule)

**Year labels:** use **BC** and **AD** (traditional system), not BCE or CE — see [STYLE-GUIDE § Dating](../STYLE-GUIDE.md#dating-years).

**`ancient` ends with the fall of the Roman Empire in the West** (traditional **~476 AD**). Works whose main subject is **late Roman decline, the fall itself, or the last generations of the Western imperial order** stay **`era: ancient`** — they close the ancient arc; they are not “misplaced” medieval.

**`medieval`** begins with the **post-476 AD** formations and parallel stories you shelve next (e.g. Ostrogothic Italy, Byzantine empire as medieval frame, Islamic expansion, medieval church and states — aligned to History Notebook Vol II and your upload order).

**`medieval` ends with the fall of Constantinople** (traditional **1453 AD**), matching [History Notebook Vol II](../README.md) (476 AD–1453 AD). Works centered on **late Byzantine** or the **1453** transition may use **`eras: [medieval, colonial]`** (or **`notes`**) when the narrative runs into early modern **Ottoman** or maritime Europe — pick primary **`era`** for shelf sort.

**`colonial`** (operator label → Vol III) picks up **post-1453** early modern / maritime–colonial themes for this book; use **`notes`** when a title straddles 1453.

**`colonial` ends with the French Revolution** (traditional **1789 AD**), matching [History Notebook Vol III](../README.md) (1453 AD–1789 AD). Works whose narrative crosses into **industrial** war or state formation (e.g. long 18th–19th-century arcs) may use **`eras: [colonial, industrial]`** (or **`notes`**) — pick primary **`era`** for shelf sort.

**`industrial`** (Vol IV) picks up **post-1789** themes for this book; use **`notes`** when a title straddles 1789.

**`industrial` ends with the end of the Second World War** (traditional **1945 AD**), matching [History Notebook Vol IV](../README.md) (1789 AD–1945 AD). Works whose narrative crosses into the **contemporary** order (Cold War, decolonization, post-1945 institutions) may use **`eras: [industrial, modern]`** (or **`notes`**) — pick primary **`era`** for shelf sort.

**`modern`** (Vol V) picks up **post-1945** themes for this book; use **`notes`** when a title straddles 1945.

If a title straddles (e.g. one volume covers 400–600 AD, or 1400–1500 AD across 1453, or 1750–1850 AD across 1789, or 1930–1960 AD across 1945), set **`eras`** when multiple buckets apply; use **`notes`** for nuance; pick one **`era`** as primary for batch/sort, or split editions later.

## Per-batch workflow (five titles)

1. Confirm the **active era** (next in the sequence above).
2. Add five new `items` in `bookshelf-catalog.yaml` (or paste a block for the agent to merge):
   - Next sequential `id`: `HNSRC-NNNN`.
   - Required: `title`, `author`, **`era`**.
   - Optional: `eras`, `year`, `isbn`, `added_batch`, `tags`, `hn_volume`, `primary_arc`, `candidate_hn_chapters`, `ph_thesis_hints`, `ph_concept_hints`, `notes`.
3. Run validation: `python3 scripts/validate_bookshelf_catalog.py` (use `--strict` in CI if wired).
4. **Within-era pass:** dedupe, cluster tags, adjust `candidate_hn_chapters` only as **planning** hints.
5. **When an era slice feels complete:** optional short summary in this file (dated bullet) or in git commit message — not required for v1.

## Relation to SELF-LIBRARY (`LIB-*`)

Promoting a work to the global companion library ([`docs/library-schema.md`](../../../../library-schema.md)) is **optional**. If you add a `lib_id` on a catalog row, keep `self-library.md` as SSOT for the `LIB-*` entry; the catalog row is a **History-Notebook–scoped** mirror for drafting.

## Phase 2 — full text (not implemented yet)

When you upload **whole book text** (PDF, EPUB, or extracted markdown):

- Store binaries or large extracts **outside git** or under a **gitignored** tree; do not commit copyrighted full text without rights.
- Extend each catalog row with optional fields (convention only until you implement tooling):

| Field | Purpose |
|-------|---------|
| `content_path` | Absolute path or repo-relative path to gitignored file |
| `content_kind` | e.g. `pdf`, `epub`, `md_extract` |
| `indexed_at` | ISO date when search/RAG index last built |

- **RAG / embeddings:** separate decision (local vector store vs external); wire in a later lane after `content_path` is stable.

## Example: minimal new row

```yaml
  - id: HNSRC-0006
    title: "Example Work"
    author: "Author Name"
    year: 1920
    era: ancient
    added_batch: "2026-04-18-ancient-b"
    tags: [example]
    notes: "Replace with a real title from your shelf."
```

## Validation

```bash
python3 scripts/validate_bookshelf_catalog.py
python3 scripts/validate_bookshelf_catalog.py --strict
```

Checks: unique `HNSRC-*` ids, required `era`, `candidate_hn_chapters` ⊆ `book-architecture.yaml`, duplicate `(title, author)` warnings.
