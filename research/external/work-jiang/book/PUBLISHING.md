# Predictive History — Publishing strategy

**Purpose:** Operator-facing defaults for how the **Predictive History** multivolume line ships to readers while the full corpus stays in **one repository**.

---

## One volume at a time

- **Release cadence:** Publish **one printed (or major digital) volume per release**, not an omnibus of the whole line. Total source material is large; serial publication keeps each book **finishable** for readers and **manageable** for editorial, design, and correction cycles.
- **Volumes I–VII** map to primary corpora as documented in [`WORKFLOW-transcripts.md`](../WORKFLOW-transcripts.md) and the per-volume specs: [VOLUME-II-CIVILIZATION.md](VOLUME-II-CIVILIZATION.md), [VOLUME-III-SECRET-HISTORY.md](VOLUME-III-SECRET-HISTORY.md), [VOLUME-IV-GAME-THEORY.md](VOLUME-IV-GAME-THEORY.md), [VOLUME-V-GREAT-BOOKS.md](VOLUME-V-GREAT-BOOKS.md), [VOLUME-VI-INTERVIEWS.md](VOLUME-VI-INTERVIEWS.md), [VOLUME-VII-ESSAYS.md](VOLUME-VII-ESSAYS.md). Volume I (Geo-Strategy) remains anchored in [`BOOK-ARCHITECTURE.md`](../BOOK-ARCHITECTURE.md) / `metadata/book-architecture.yaml`.

---

## Assume prior volumes (serial read)

- **Default reader:** Someone **may have read earlier volumes**; later volumes should **not** assume a cold start, but also need not **re-teach** the entire system.
- **Per-volume front matter:** Include a short **orientation** (what this volume’s corpus is, how it extends the arc) and a **suggested reading order** pointer (Volumes I → VII) for newcomers.
- **Lightweight refresh:** Where a concept first earned a careful definition in an earlier volume, later volumes may use **brief reminders**, **gloss pointers**, or **cross-refs** rather than full repetition. Canonical vocabulary work lives in [CONCEPT-DICTIONARY.md](../CONCEPT-DICTIONARY.md) / `metadata/concepts.yaml` as the long-lived index.

---

## Cross-volume references

- **Encouraged:** Footnotes, endnotes, or parenthetical **“see Predictive History, Volume _X_, …”** references when a claim, motif, or lecture depends on material published in another volume.
- **Goal:** Preserve honesty about dependencies **without** requiring the reader to own every volume for every sentence—references should identify **where** the fuller argument lives, not gate basic comprehension of the current volume’s core arc.
- **Editorial discipline:** Cross- refs should stay aligned with corpus boundaries and [BOOK-QUALITY-DOCTRINE.md](BOOK-QUALITY-DOCTRINE.md) (no scope expansion).

---

## Single repo for all corpora

- **Source of truth:** All lecture series, interviews, essays, registries, and tooling remain under **`research/external/work-jiang/`** in this repository regardless of which volume is **released** next.
- **Publishing** chooses what to **extract, edit, and typeset** for a given imprint; it does **not** split the research tree across separate repos unless there is a separate operational reason (mirrors and exports are fine).

---

## Related

- Editorial compression: [BOOK-QUALITY-DOCTRINE.md](BOOK-QUALITY-DOCTRINE.md)
- Transcript and layer discipline: [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md), [ASR-VERIFICATION-RUBRIC.md](../ASR-VERIFICATION-RUBRIC.md)
- Instance pointer: [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md)
