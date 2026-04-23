# Greenwald refined day page — template

WORK only; not Record.

**Purpose:** Standalone refined day page for the `greenwald` expert. **`### Chronicle`** carries the **full verbatim** from linked [`raw-input/`](../../raw-input/README.md)—**lightly cleaned and formatted**; **`### Reflection`** and **`### Foresight`** are **operator analysis** (**may be stubbed** on ingest, completed in a later pass). Distinct from a `strategy-page` HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](../../strategy-page-template.md) instead of this file.

**Length:** No enforced word limit. **Chronicle** is often long (full verbatim). **Reflection** / **Foresight** start as stubs or short notes until operator analysis—still no `verify:` machinery in those sections except as grammatical prose (path dumps belong in **`### Appendix`**). Mode B without a capture may be mostly appendix + stubs.

### Prose emphasis (Chronicle / Reflection / Foresight)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Aired:**) and for the required appendix bullet titles (see Appendix bullet order below).
- Optional bold for the short title of a bullet inside Foresight when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes (pick one)

### Mode A — Primary dated capture

Use when **Chronicle** carries the full verbatim for this expert’s main artifact for that calendar day (broadcast, interview, essay, or long transcript) with a canonical **aired** or **published** date.

```markdown
**Expert:** `greenwald` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/greenwald/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Notebook stub

Use when [`transcript.md`](transcript.md) holds only a `notebook |` row or thin registry lines for that date (no long verbatim). Point to the chapter seam when the lens hangs off a woven day.

```markdown
**Expert:** `greenwald` · **Ingest:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/greenwald/`). **Note:** This date may be a `notebook |` lens row only—not a full capture verbatim. [Optional: tri-mind / chapter pointer — e.g. `days.md` § anchor.]
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Chronicle` — **Full verbatim** from the linked `raw-input` capture (after YAML frontmatter when present): **lightly cleaned and formatted** only—paragraphing, spacing, obvious ingest artifacts, optional speaker labels; **do not** replace the expert’s words with summary or paraphrase. The file under `raw-input/` remains the archived capture; **Chronicle** is the readable full text on this page. **Mode B** (no long capture): brief stub or pointer only.
3. `### Reflection` — **Operator analysis:** Greenwald-lane arc; keep verification discipline explicit where load-bearing claims sit in commentator tier. **May be stubbed** until a later operator pass.
4. `### Foresight` — **Operator analysis:** falsifiers, resume lines, tier tags (bullets allowed). **May be stubbed** until a later operator pass.
5. Horizontal rule `---` before appendix.
6. `### Appendix` — machinery only (paths, inbox grep, `thread:greenwald`, canonical URL).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link to the capture under `raw-input/<YYYY-MM-DD>/` (slug varies by ingest pipeline).
2. **Inbox / triage:** link to [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) with grep hints (`thread:greenwald`, date, and for Mode B the `notebook |` / `verify:` tail).
3. **`thread:greenwald`** · **verify:** one line consolidating verify tier for this page.
4. **Canonical primary:** pin `source_url`, video ID, article URL, or X permalink when known; for Mode B use **Not applicable** unless a clip or permalink is explicitly tied.

---

## Raw-input naming (Greenwald)

Verbatim lives under `raw-input/<date>/`. Refined pages live only under `experts/greenwald/`.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add (when not already present):

- `Verbatim:` → relative link to the `raw-input` capture.
- `Refined day page:` → `greenwald-page-YYYY-MM-DD.md`.
- `Template:` → [`greenwald-page-template.md`](greenwald-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

**Mode A example:**

```markdown
# Greenwald day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `greenwald` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/greenwald/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Chronicle



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:greenwald`, YYYY-MM-DD)
- **`thread:greenwald`** · **verify:** full-text + raw-input + aired:YYYY-MM-DD
- **Canonical primary:** pin when known (see raw-input frontmatter / cold line)
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Greenwald day page — YYYY-MM-DD`.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches Mode A or Mode B; **Artifact:** uses “refined day page (standalone file under `experts/greenwald/`)” verbatim.
4. `---` before `### Chronicle`.
5. `### Chronicle`, `### Reflection`, `### Foresight` present; **Chronicle** = full verbatim (lightly cleaned)—no `verify:` / path machinery there; **Reflection** / **Foresight** = operator analysis (stubs OK). No decorative bold except lane rules (see Prose emphasis).
6. `---` before `### Appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Inbox / triage → `thread:greenwald` · verify → Canonical primary.
8. Relative links resolve from `experts/greenwald/` (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).
