# Ritter refined day page — template

WORK only; not Record.

**Purpose:** Standalone **Signal / Judgment / Open** artifact for the `ritter` expert. **Not** a substitute for full **verbatim** in [`raw-input/`](../../raw-input/README.md). Distinct from a **`strategy-page`** HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** Use [`strategy-page-template.md`](../../strategy-page-template.md) for `<!-- strategy-page:start … -->` blocks in thread files.

**Filename date:** Prefer the **voice / publication** date in the title (`ritter-page-YYYY-MM-DD.md`)—the date the capture attributes to the episode or essay. If the `raw-input/` folder date differs (ingest batching), note it only in the **Technical appendix**.

**Prose budget:** Target ~500–1000 words combined across **Signal**, **Judgment**, and **Open** for long-form captures (Substack, **Judging Freedom**, **YouTube** monologue). **Mode D** (thin X / registry-only rows) may be much shorter. Grammatical prose only in those sections—no path dumps or `verify:` machinery there.

---

## Preamble modes (pick one)

### Mode A — Substack essay

Long-form essay with **published** date; pin `source_url` in raw-input frontmatter.

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Judging Freedom (or third-party interview)

Host-dated conversation; use **aired** or **host date** per inbox / raw-input convention.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode B — Judging Freedom / interview (see raw-input `series`) · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode C — YouTube / standalone video

Ritter monologue or guest spot with canonical `watch?v=` when pinned.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode C — YouTube (see raw-input `source_url`) · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode D — Notebook / X stub

[`transcript.md`](transcript.md) holds mostly **`X | cold`** or registry lines without a long verbatim block for that date.

```markdown
**Expert:** `ritter` · **Ingest:** YYYY-MM-DD · **Capture:** Mode D — notebook / X stub · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Note:** May lack a single long capture—point to `days.md` / chapter seam when the lens hangs off a woven day.
```

---

### Prose emphasis (Signal / Judgment / Open)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Published:**) and for the required appendix bullet titles.
- Optional bold for the short title of a bullet inside **Open** when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Signal` — fact framing and capture content.
3. `### Judgment` — Ritter-lane arc (inspection / enforcement frame, IHL and coercion reads, Hormuz or Russia–U.S. seams as needed); keep **commentator vs wire** tier discipline on load-bearing claims.
4. `### Open` — falsifiers, resume lines, tier tags (bullets allowed).
5. Horizontal rule `---` before appendix.
6. `### Technical appendix` — machinery only.

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link under `raw-input/<YYYY-MM-DD>/` (slug examples: `substack-ritter-…`, `judging-freedom-…`, `ritter-rant-…`, etc.).
2. **Inbox / triage:** [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) — search `thread:ritter`, date, and capture-specific `verify:` / `SS |` / `JF |` / `YT |` hints.
3. **`thread:ritter`** · **verify:** one consolidated verify line.
4. **Canonical primary:** Substack URL, `watch?v=`, **Judging Freedom** link, or **X** permalink as applicable; **Not applicable** for pure Mode D stubs unless one URL is pinned.

---

## Raw-input naming (Ritter)

Verbatim lives under `raw-input/<date>/`. Refined pages live only under `experts/ritter/`.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add when missing:

- **`Verbatim:`** → relative link to the `raw-input` capture (or stub note if over triage budget).
- **`Refined day page:`** → `ritter-page-YYYY-MM-DD.md`.
- **`Template:`** → [`ritter-page-template.md`](ritter-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

```markdown
# Ritter day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** refined day page (standalone file under `experts/ritter/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Signal



### Judgment



### Open



---

### Technical appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:ritter`, YYYY-MM-DD)
- **`thread:ritter`** · **verify:** …
- **Canonical primary:** …
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Ritter day page — YYYY-MM-DD` (voice date).
2. `WORK only; not Record.` on its own line after the title.
3. Preamble identifies **Mode A–D**; **Artifact:** uses “refined day page (standalone file under `experts/ritter/`)”.
4. `---` before `### Signal`; prose-only in Signal / Judgment / Open.
5. `---` before `### Technical appendix`.
6. Appendix bullets in order: capture → inbox → `thread:ritter` verify → canonical primary.
7. Relative links resolve from `experts/ritter/` (`../../raw-input/…`, `../../daily-strategy-inbox.md`).
