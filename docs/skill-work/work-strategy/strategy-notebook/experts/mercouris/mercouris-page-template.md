# Mercouris refined day page — template

WORK only; not Record.

**Purpose:** Standalone Signal / Judgment / Open artifact for the `mercouris` expert. Not a substitute for full verbatim in [`raw-input/`](../../raw-input/README.md). Distinct from a `strategy-page` HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](../../strategy-page-template.md) instead of this file.

**Prose budget:** Target ~500–1000 words combined across Signal, Judgment, and Open for Mode A (full The Duran episode). Mode B (`notebook |` stub) may be much shorter. Grammatical prose only in those sections—no path dumps or `verify:` machinery there.

### Prose emphasis (Signal / Judgment / Open)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Aired:**) and for the required appendix bullet titles (see Technical appendix pattern below).
- Optional bold for the short title of a bullet inside Open when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes (pick one)

### Mode A — Aired (The Duran)

Use when the page summarizes a broadcast with a canonical air date.

```markdown
**Expert:** `mercouris` · **Aired:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/mercouris/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Notebook stub

Use when [`transcript.md`](transcript.md) holds only a `notebook |` row for that date (no Duran verbatim). Point to the chapter seam when the lens hangs off a woven day.

```markdown
**Expert:** `mercouris` · **Ingest:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/mercouris/`). **Note:** This date is a `notebook |` lens row only—not a The Duran episode verbatim. [Optional: tri-mind / chapter pointer — e.g. `days.md` § anchor.]
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Signal` — fact framing and episode (or stub) content.
3. `### Judgment` — Mercouris-lane arc; keep verification discipline explicit where load-bearing claims sit in commentator tier.
4. `### Open` — falsifiers, resume lines, tier tags (bullets allowed).
5. Horizontal rule `---` before appendix.
6. `### Technical appendix` — machinery only (paths, inbox grep, `thread:mercouris`, canonical video).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link to the capture under `raw-input/<YYYY-MM-DD>/` (slug varies: `duran-mercouris-…-date.md`, `transcript-mercouris.md`, `YYYY-MM-DD-mercouris-verbatim.md`, etc.).
2. **Inbox / triage:** link to [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) with grep hints (`thread:mercouris`, date, and for Mode B the `notebook |` / `verify:` tail).
3. **`thread:mercouris`** · **verify:** one line consolidating verify tier for this page.
4. **Canonical video:** pin `source_url` / watch ID when known; for Mode B use Not applicable (no Duran episode) unless a clip is explicitly tied.

---

## Raw-input naming (Mercouris)

Verbatim lives under `raw-input/<date>/`, e.g. descriptive Duran slugs, `transcript-mercouris.md`, or RSS merge `YYYY-MM-DD-mercouris.md`. Refined pages live only under `experts/mercouris/`.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add (when not already present):

- `Verbatim:` → relative link to the `raw-input` capture.
- `Refined day page:` → `mercouris-page-YYYY-MM-DD.md`.
- `Template:` → [`mercouris-page-template.md`](mercouris-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

**Mode A example:**

```markdown
# Mercouris day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `mercouris` · **Aired:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/mercouris/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Signal



### Judgment



### Open



---

### Technical appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:mercouris`, YYYY-MM-DD)
- **`thread:mercouris`** · **verify:** full-text + raw-input + aired:YYYY-MM-DD
- **Canonical video:** pin when known (see raw-input frontmatter / cold line)
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Mercouris day page — YYYY-MM-DD`.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches Mode A or Mode B; **Artifact:** uses “refined day page (standalone file under `experts/mercouris/`)” verbatim.
4. `---` before `### Signal`.
5. `### Signal`, `### Judgment`, `### Open` present; prose-only (no machinery in those sections); no decorative bold in body paragraphs (see Prose emphasis above).
6. `---` before `### Technical appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Inbox / triage → `thread:mercouris` · verify → Canonical video.
8. Relative links resolve from `experts/mercouris/` (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).
