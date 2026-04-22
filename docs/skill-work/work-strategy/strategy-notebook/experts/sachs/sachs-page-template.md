# Sachs refined day page — template

WORK only; not Record.

**Purpose:** Standalone Signal / Judgment / Open artifact for the `sachs` expert. Not a substitute for full verbatim in [`raw-input/`](../../raw-input/README.md). Distinct from a `strategy-page` HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](../../strategy-page-template.md) instead of this file.

**Prose budget:** Target ~500–1000 words combined across Signal, Judgment, and Open for Mode A (primary long-form capture for this expert). Mode B (`notebook |` stub or short social ingest) may be much shorter. Grammatical prose only in those sections—no path dumps or `verify:` machinery there.

### Prose emphasis (Signal / Judgment / Open)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Aired:**) and for the required appendix bullet titles (see Technical appendix pattern below).
- Optional bold for the short title of a bullet inside Open when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes (pick one)

### Mode A — Primary dated capture

Use when the page summarizes this expert’s main artifact for that calendar day (broadcast, interview, essay, or long transcript) with a canonical **aired** or **published** date.

```markdown
**Expert:** `sachs` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/sachs/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Notebook stub

Use when [`transcript.md`](transcript.md) holds only a `notebook |` row or thin registry lines for that date (no long verbatim). Point to the chapter seam when the lens hangs off a woven day.

```markdown
**Expert:** `sachs` · **Ingest:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/sachs/`). **Note:** This date may be a `notebook |` lens row only—not a full capture verbatim. [Optional: tri-mind / chapter pointer — e.g. `days.md` § anchor.]
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Signal` — fact framing and episode (or stub) content.
3. `### Judgment` — Sachs-lane arc; keep verification discipline explicit where load-bearing claims sit in commentator tier.
4. `### Open` — falsifiers, resume lines, tier tags (bullets allowed).
5. Horizontal rule `---` before appendix.
6. `### Technical appendix` — machinery only (paths, inbox grep, `thread:sachs`, canonical URL).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link to the capture under `raw-input/<YYYY-MM-DD>/` (slug varies by ingest pipeline).
2. **Inbox / triage:** link to [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) with grep hints (`thread:sachs`, date, and for Mode B the `notebook |` / `verify:` tail).
3. **`thread:sachs`** · **verify:** one line consolidating verify tier for this page.
4. **Canonical primary:** pin `source_url`, video ID, article URL, or X permalink when known; for Mode B use **Not applicable** unless a clip or permalink is explicitly tied.

---

## Raw-input naming (Sachs)

Verbatim lives under `raw-input/<date>/`. Refined pages live only under `experts/sachs/`.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add (when not already present):

- `Verbatim:` → relative link to the `raw-input` capture.
- `Refined day page:` → `sachs-page-YYYY-MM-DD.md`.
- `Template:` → [`sachs-page-template.md`](sachs-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

**Mode A example:**

```markdown
# Sachs day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `sachs` · **Aired / published:** YYYY-MM-DD · **Artifact:** refined day page (standalone file under `experts/sachs/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Signal



### Judgment



### Open



---

### Technical appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:sachs`, YYYY-MM-DD)
- **`thread:sachs`** · **verify:** full-text + raw-input + aired:YYYY-MM-DD
- **Canonical primary:** pin when known (see raw-input frontmatter / cold line)
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Sachs day page — YYYY-MM-DD`.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches Mode A or Mode B; **Artifact:** uses “refined day page (standalone file under `experts/sachs/`)” verbatim.
4. `---` before `### Signal`.
5. `### Signal`, `### Judgment`, `### Open` present; prose-only (no machinery in those sections); no decorative bold in body paragraphs (see Prose emphasis above).
6. `---` before `### Technical appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Inbox / triage → `thread:sachs` · verify → Canonical primary.
8. Relative links resolve from `experts/sachs/` (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).
