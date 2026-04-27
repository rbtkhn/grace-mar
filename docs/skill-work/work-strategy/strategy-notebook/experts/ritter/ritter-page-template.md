# Ritter refined day page — template
<!-- word_count: 902 -->

WORK only; not Record.

**Purpose:** Standalone refined day page for the `ritter` expert. **`### Chronicle`** carries the **full verbatim** from linked [`raw-input/`](../../raw-input/README.md)—**lightly cleaned and formatted**; **`### Reflection`** and **`### Foresight`** are **operator analysis** (**may be stubbed** on ingest, completed in a later pass). Distinct from a **`strategy-page`** HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](../../strategy-page-template.md) instead of this file.

**Filename:** Default **`ritter-page-YYYY-MM-DD.md`** (voice / publication date). **Multiple refined pages for the same publication date are allowed:** use **`ritter-page-YYYY-MM-DD-<slug>.md`** with **`<slug>`** from the raw-input stem so filenames stay unique. **Alternatively,** consolidate same-day captures into **one** refined file with **A / B / C** Chronicle blocks when this template provides a same-day section. If the `raw-input/` folder date differs (ingest batching), note it in **`### Appendix`**. Under [`transcript.md`](transcript.md) when used, add one **`Refined day page:`** line per refined file for that date.

**Length:** No enforced word limit. **Chronicle** is typically long (full verbatim) for Mode A–C; **Reflection** / **Foresight** may be stubbed until operator analysis. Mode D may be short. No path dumps or `verify:` in body sections—**`### Appendix`** only.

### Prose emphasis (Chronicle / Reflection / Foresight)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Published:**) and for the required appendix bullet titles (see Appendix bullet order below).
- Optional bold for the short title of a bullet inside **Foresight** when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes (pick one)

### Mode A — Substack essay

Long-form essay with **published** date; pin `source_url` in raw-input frontmatter.

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** refined day page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Judging Freedom (or third-party interview)

Host-dated conversation; use **aired** or **host date** per inbox / raw-input convention.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode B — Judging Freedom / interview (see raw-input `series`) · **Artifact:** refined day page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode C — YouTube / standalone video

Ritter monologue or guest spot with canonical `watch?v=` when pinned.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode C — YouTube (see raw-input `source_url`) · **Artifact:** refined day page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode D — Notebook / X stub

[`transcript.md`](transcript.md) holds mostly **`X | cold`** or registry lines without a long verbatim block for that date.

```markdown
**Expert:** `ritter` · **Ingest:** YYYY-MM-DD · **Capture:** Mode D — notebook / X stub · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Note:** May lack a single long capture—point to `days.md` / chapter seam when the lens hangs off a woven day.
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Chronicle` — **Full verbatim** from the linked `raw-input` capture (after YAML frontmatter when present): **lightly cleaned and formatted** only—paragraphing, spacing, obvious ingest artifacts, optional speaker labels; **do not** replace the expert’s words with summary or paraphrase. The file under `raw-input/` remains the archived capture; **Chronicle** is the readable full text on this page. **Mode B** (no long capture): brief stub or pointer only.
3. `### Reflection` — **Operator analysis:** Ritter-lane arc; IHL / coercion reads, Hormuz or Russia–U.S. seams; **commentator vs wire** tier discipline on load-bearing claims. **May be stubbed** until a later operator pass.
4. `### Foresight` — **Operator analysis:** falsifiers, resume lines, tier tags (bullets allowed). **May be stubbed** until a later operator pass.
5. Horizontal rule `---` before appendix.
6. `### Appendix` — machinery only (paths, inbox grep, `thread:ritter`, canonical primary).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link under `raw-input/<YYYY-MM-DD>/` (slug examples: `substack-ritter-…`, `judging-freedom-…`, `ritter-rant-…`, etc.).
2. **Inbox / triage:** link to [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) with grep hints (`thread:ritter`, date, and capture-specific `verify:` / `SS |` / `JF |` / `YT |` tails).
3. **`thread:ritter`** · **verify:** one line consolidating verify tier for this page.
4. **Canonical primary:** Substack URL, `watch?v=`, **Judging Freedom** link, or **X** permalink as applicable; **Not applicable** for pure Mode D stubs unless one URL is pinned.

---

## Raw-input naming (Ritter)

Verbatim lives under `raw-input/<date>/`. Refined pages live only under `experts/ritter/`. Optional machine index (capture → page file, modes, URLs): [`ritter-pages-manifest.yaml`](ritter-pages-manifest.yaml). Legacy tooling (verbatim-heavy page bodies): [`scripts/strategy/assemble_ritter_pages_verbatim.py`](../../../../scripts/strategy/assemble_ritter_pages_verbatim.py), [`scripts/strategy/build_ritter_refined_pages.py`](../../../../scripts/strategy/build_ritter_refined_pages.py).

## Machine checks (`verify_ritter_refined_pages.py`)

[`scripts/strategy/verify_ritter_refined_pages.py`](../../../../scripts/strategy/verify_ritter_refined_pages.py) (repo root): manifest rows, `raw-input` on disk, `transcript.md` backlinks, and page spine **`### Chronicle`**, **`### Reflection`**, **`### Foresight`**, **`### Appendix`** (legacy `### Signal` / `### Judgment` / `### Open` / `### Technical appendix` still accepted until regenerated). **`**Words:** N`** is **optional**: when present it must match full-file word count with that line stripped (±5 tokens); when omitted, **`**Words:**`** bookkeeping is skipped (Chronicle may still be full verbatim). An optional Reflection+Foresight **share** advisory runs only when **`**Words:**`** is present (legacy verbatim-leaning pages). **No** word-count ceiling. Use `--no-page-shape` for manifest/transcript-only checks.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add (when not already present):

- **`Verbatim:`** → relative link to the `raw-input` capture.
- **`Refined day page:`** → `ritter-page-YYYY-MM-DD.md` or `ritter-page-YYYY-MM-DD-<slug>.md`.
- **`Template:`** → [`ritter-page-template.md`](ritter-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

**Mode A example:**

```markdown
# Ritter day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** refined day page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Chronicle



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:ritter`, YYYY-MM-DD)
- **`thread:ritter`** · **verify:** full-text + raw-input + published:YYYY-MM-DD
- **Canonical primary:** pin when known (see raw-input frontmatter / cold line)
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Ritter day page — YYYY-MM-DD` (or include a short parenthetical title when helpful); filename `ritter-page-YYYY-MM-DD.md` or with `-<slug>` when needed.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches Mode A–D; **Artifact:** uses “refined day page (standalone file under `experts/ritter/`)” verbatim.
4. `---` before `### Chronicle`.
5. `### Chronicle`, `### Reflection`, `### Foresight` present; **Chronicle** = full verbatim (lightly cleaned)—no `verify:` / path machinery there; **Reflection** / **Foresight** = operator analysis (stubs OK). No decorative bold except lane rules.
6. `---` before `### Appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Inbox / triage → `thread:ritter` · verify → Canonical primary.
8. Relative links resolve from `experts/ritter/` (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).
