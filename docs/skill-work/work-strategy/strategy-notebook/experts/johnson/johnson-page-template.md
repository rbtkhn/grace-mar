# Johnson refined day page — template

WORK only; not Record.

**Purpose:** Standalone Chronicle / Reflection / Foresight artifact for the `johnson` expert. Not a substitute for full verbatim in [`raw-input/`](../../raw-input/README.md). Distinct from a `strategy-page` HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](../../strategy-page-template.md) instead of this file.

**Prose budget:** Target ~500–1000 words combined across Signal, Judgment, and Open for Mode A (primary long-form capture for this expert). Mode B (`notebook |` stub or short social ingest) may be much shorter. Grammatical prose only in those sections—no path dumps or `verify:` machinery there.

### Prose emphasis (Chronicle / Reflection / Foresight)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Aired:**) and for the required appendix bullet titles (see Technical appendix pattern below).
- Optional bold for the short title of a bullet inside Open when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes (pick one)

### Mode A — Primary dated capture

Use when the page summarizes this expert’s main artifact for that calendar day (broadcast, interview, essay, or long transcript) with a canonical **aired** or **published** date.

```markdown
**Expert:** `johnson` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/johnson/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Notebook stub

Use when [`transcript.md`](transcript.md) holds only a `notebook |` row or thin registry lines for that date (no long verbatim). Point to the chapter seam when the lens hangs off a woven day.

```markdown
**Expert:** `johnson` · **Ingest:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/johnson/`). **Note:** This date may be a `notebook |` lens row only—not a full capture verbatim. [Optional: tri-mind / chapter pointer — e.g. `days.md` § anchor.]
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Chronicle` — fact framing and episode (or stub) content.
3. `### Reflection` — Johnson-lane arc; keep verification discipline explicit where load-bearing claims sit in commentator tier.
4. `### Foresight` — falsifiers, resume lines, tier tags (bullets allowed).
5. Horizontal rule `---` before appendix.
6. `### Appendix` — machinery only (paths, inbox grep, `thread:johnson`, canonical URL).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link to the capture under `raw-input/<YYYY-MM-DD>/` (slug varies by ingest pipeline).
2. **Inbox / triage:** link to [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) with grep hints (`thread:johnson`, date, and for Mode B the `notebook |` / `verify:` tail).
3. **`thread:johnson`** · **verify:** one line consolidating verify tier for this page.
4. **Canonical primary:** pin `source_url`, video ID, article URL, or X permalink when known; for Mode B use **Not applicable** unless a clip or permalink is explicitly tied.

---

## Raw-input naming (Johnson)

Verbatim lives under `raw-input/<date>/`. Refined pages live only under `experts/johnson/`.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add (when not already present):

- `Verbatim:` → relative link to the `raw-input` capture.
- `Refined day page:` → `johnson-page-YYYY-MM-DD.md`.
- `Template:` → [`johnson-page-template.md`](johnson-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

**Mode A example:**

```markdown
# Johnson day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `johnson` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/johnson/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Chronicle



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:johnson`, YYYY-MM-DD)
- **`thread:johnson`** · **verify:** full-text + raw-input + aired:YYYY-MM-DD
- **Canonical primary:** pin when known (see raw-input frontmatter / cold line)
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Johnson day page — YYYY-MM-DD`.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches Mode A or Mode B; **Artifact:** uses “refined day page (standalone file under `experts/johnson/`)” verbatim.
4. `---` before `### Chronicle`.
5. `### Chronicle`, `### Reflection`, `### Foresight` present; prose-only (no machinery in those sections); no decorative bold in body paragraphs (see Prose emphasis above).
6. `---` before `### Appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Inbox / triage → `thread:johnson` · verify → Canonical primary.
8. Relative links resolve from `experts/johnson/` (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).
