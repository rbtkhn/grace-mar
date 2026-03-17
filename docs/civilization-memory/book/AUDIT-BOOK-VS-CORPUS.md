# Audit: Book vs civ-mem corpus

**Date:** 2026-03-14  
**Scope:** APPLIED-THEOLOGY.md and BOOK.md checked against the full `docs/civilization-memory/` corpus (essays, notes, minds).

---

## 1. Corpus inventory

### Essays (`essays/`)

| File | In BOOK.md | In APPLIED-THEOLOGY.md |
|------|------------|------------------------|
| THE-SIMPLE-CONDITION.md | ✓ Part 1 | ✓ Part 1 |
| ONE-SUBJECT-MANY-TONGUES.md | ✓ Part 2 | ✓ Part 2 |
| UNIVERSAL-LOVE-AND-MASTERY.md | ✓ Part 3 | ✓ Part 3 |
| THE-COORDINATION-HYPOTHESIS.md | ✓ Part 4 | ✓ Part 4 |
| THE-DELUSION-OF-SEPARATION.md | ✓ Part 5 | ✓ Part 5 |
| AI-ETHICS-FROM-THE-CONDITION.md | ✓ Part 6 | ✓ Part 6 |
| WRITING-THE-BOOK-AND-DEATH.md | ✓ Part 7 (Coda) | ✓ Part 7 (Coda) |
| PRESERVING-CONSCIOUSNESS-BIOLOGICAL-SYMBOLS.md | ✗ missing | ✓ Part 8 |

**Finding:** All 8 theology essays are in APPLIED-THEOLOGY. BOOK.md is missing Preserving Consciousness (still “seven parts” only).

---

### Notes (`notes/`)

| Note | Theology / applied? | In APPLIED-THEOLOGY |
|------|---------------------|----------------------|
| scripture-as-test-concept-and-literature.md | Yes | ✓ Part 9 (standalone) + **integrated in Part 2** (§ Scripture as test) |
| concept-god-non-zero-sum.md | Yes | ✓ Appendix + **integrated in Part 2** (§ One subject, many tongues) |
| face-category-blade.md | Yes (blade mechanism, see the face) | ✓ **Integrated in Part 1** (§ II blade/face; § IX children's question) |
| exercise-face-category-school-children.md | Yes (classroom exercise) | ✗ Not included |
| lens-gods-debris.md | Yes (Adams lens on Condition) | ✗ Not included |
| concept-cognitive-polyphony.md | Yes (STATE, one subject many tongues) | ✗ Not included |
| argument-purpose-of-history-unifies.md | Yes (purpose of history, reassembly) | ✗ Not included |
| trace-civmem-influence-writing-the-book-thesis.md | Meta / trace | ✗ Not included |
| literature-parallels-writing-purpose-death.md | Meta / literature | ✗ Not included |
| civ-mem-state-vs-scholar.md | Process (STATE vs SCHOLAR) | ✗ Not included |

**Finding:** Applied Theology now includes all three key theology notes (Scripture as Test, God is non-zero-sum, face-category-blade), with the latter three integrated in the body (Part 1 § II/IX, Part 2 § One subject, many tongues). Four other theology-related notes are not in the book: exercise (See the Face), lens God's Debris, polyphonic cognition. Two meta/argument notes (purpose of history, STATE/Scholar) and two trace/literature notes are out of scope for a single “Applied Theology” volume and reasonably excluded.

---

### Minds (`minds/`)

| File | Role |
|------|------|
| CIV–MIND–MERCOURIS.md | Polyphonic cognition profile; STATE reference |
| CIV–MIND–MEARSHEIMER.md | Polyphonic cognition profile; STATE reference |
| CIV–MIND–BARNES.md | Polyphonic cognition profile; STATE reference |

**Finding:** Minds are implementation/STATE profiles, not theology essays. Correctly excluded from the book. Referenced indirectly via polyphonic cognition in the corpus.

---

## 2. Content fidelity (book vs source)

### Essays

- **Spot-check (THE-SIMPLE-CONDITION):** Body text in APPLIED-THEOLOGY Part 1 matches the source essay (same paragraphs, section order). Source has YAML frontmatter; book correctly omits it.
- **Preserving Consciousness:** Book Part 8 matches the current essay (including “the good is in the living”). No frontmatter in book.
- **Assumption:** Parts 2–7 were copied from BOOK.md, which was built from the same essay sources; no systematic drift detected in the sample. **Recommendation:** Periodically re-run a diff of each part against its source file when sources are edited.

### Notes in the book

- **Scripture as Test (Part 9):** Book includes: The concept; Application to Hinduism and Buddhism; Tension with prophecy-fulfillment (Zionism); Link to Condition and One Subject Many Tongues. **Omitted from book:** Full “Literature search summary” (Levinas/Akedah, violent scripture hermeneutics, Satan’s use of scripture, Christian–Muslim dialogue, Jewish tradition, conclusion on originality). So the book has an **abridged** Scripture as Test; academic precedent and originality claim exist only in the note.
- **God is non-zero-sum (Appendix):** Book includes: Claim; Link to Condition and civ-mem; Be fruitful and multiply; Expand the light of consciousness. Matches the note in substance; “Expand the light” is slightly shortened (no full table, prose summary only).

---

## 3. Cross-references and links

- **In-book links:** APPLIED-THEOLOGY contains markdown links that point to **files** (e.g. `[THE-SIMPLE-CONDITION.md](THE-SIMPLE-CONDITION.md)`, `[concept-god-non-zero-sum.md](../notes/concept-god-non-zero-sum.md)`). In a single-document book these links do not resolve (no anchors to other files). **Finding:** Two such blocks:
  - After Universal Love and Mastery (Part 3): *See also: THE-SIMPLE-CONDITION.md, ONE-SUBJECT-MANY-TONGUES.md, concept-god-non-zero-sum.md.*
  - After AI Ethics (Part 6): *For the full theological treatment, see THE-SIMPLE-CONDITION.md and ONE-SUBJECT-MANY-TONGUES.md.*

**Recommendation:** For a single-file reading experience, either (a) replace with in-doc anchors (e.g. “See also Part 1 — The Simple Condition, Part 2 — One Subject Many Tongues”) or (b) leave as-is and treat the book as the canonical combined text, with links as references to the source paths for editors.

---

## 4. Index and README alignment

- **essays/README.md:** Still says “All **six** essays … are collected in BOOK.md” and lists only six items in the narrative arc (call → response → deepening → science → framework → use). It does not list Preserving Consciousness or the Coda as a seventh/eighth essay. BOOK.md actually has **seven** parts (Coda = Writing the Book and Death). So the README is **out of date** (count and list).
- **book/README.md:** Correctly describes BOOK.md (Parts 1–7) and APPLIED-THEOLOGY.md (Parts 1–10 including Preserving Consciousness, Scripture as Test, Appendix).

---

## 5. Summary of gaps and actions

| Issue | Severity | Suggested action |
|-------|----------|------------------|
| BOOK.md missing Preserving Consciousness | Medium | Add Part 8 to BOOK.md from essay source, or document that BOOK = arc only and APPLIED-THEOLOGY = full theology set. |
| Scripture as Test in book is abridged (no literature search) | Low | Optional: add “Literature search summary” and “Conclusion on originality” to Part 9, or add a short line in the book that the full note is in `notes/scripture-as-test-concept-and-literature.md`. |
| Theology notes not in book: face-category-blade, exercise, lens God's Debris, polyphonic cognition, argument-purpose-of-history | Low | Decide scope: either add these as short sections/appendix in Applied Theology, or state in book README that “theology notes” in the library include these and are not inlined. |
| Cross-references in APPLIED-THEOLOGY point to files | Low | Replace with “Part N — Title” or leave as source-path references. |
| essays/README.md says “six essays” and omits Preserving Consciousness | Low | Update to “eight essays” and add Preserving Consciousness to the list; correct BOOK.md description to “seven parts” (or eight if Preserving Consciousness is added). |

---

## 6. Recommendation

- **Canonical single volume:** Treat APPLIED-THEOLOGY.md as the single-document compilation of all theological materials in the library. BOOK.md remains the shorter narrative-arc edition (Condition → Coda) without Preserving Consciousness and without the notes.
- **Corpus as source of truth:** Essays and notes in `essays/` and `notes/` remain the edit-in-place sources. The book should be regenerated or patched when those sources change (or given a short “Last synced from corpus” note).
- **READMEs:** Update `essays/README.md` to list all eight essays and to describe BOOK.md and APPLIED-THEOLOGY.md accurately.
