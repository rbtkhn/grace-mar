# Ritter strategy page — template (`ritter-page`)

WORK only; not Record.

**Purpose:** A **`ritter-page-*.md`** file **is** Ritter’s **strategy-page** — same contract as [`strategy-page-template.md`](../../strategy-page-template.md) (**Chronicle / Reflection / Foresight**, optional **`### Appendix`**). This is the **file surface** for Ritter; it is **not** a separate artifact *kind*. **`Chronicle` carries the expert’s text from the linked `raw-input` capture (target ~80% of on-page words).** **`Reflection` / `Foresight` are WORK analysis (~20%)**—tier discipline, seams, falsifiers—not a substitute for the archived verbatim file. Regenerate from manifest captures with [`scripts/strategy/assemble_ritter_pages_verbatim.py`](../../../../scripts/strategy/assemble_ritter_pages_verbatim.py). **Optional:** duplicate or compress the same logical page into a **`<!-- strategy-page:start … -->`** fence in [`thread.md`](thread.md) when you need cross-expert **`id` / `date` / `watch`** or [`validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) checks.

**Alternate surface (thread):** HTML-comment fences in `thread.md` per [`strategy-page-template.md`](../../strategy-page-template.md).

**Filename:** Every manifest-backed refined page uses **`ritter-page-YYYY-MM-DD-<slug>.md`**, where **`YYYY-MM-DD`** is the **voice / publication** date and **`<slug>`** comes from the raw-input stem (see **Same-day collision**). If the `raw-input/` folder date differs (ingest batching), note it only in the **`### Appendix`**.

**Same-day collision:** `<slug>` must be unique per capture. Derive it from the raw-input basename (drop the `substack-ritter-` prefix and trailing `-YYYY-MM-DD` if present, or use the whole stem for `judging-freedom-…` / `ritter-rant-…`). When more than one primary shares the same voice date (e.g. two essays or **Judging Freedom** plus **Ritter’s Rant**), distinct raw stems keep filenames distinct automatically. The generated H1 includes **`# Ritter strategy page — YYYY-MM-DD (*Essay or episode title*)`** when a display title is set. Under [`transcript.md`](transcript.md), add one **`Refined day page:`** line per `ritter-page` file for that date.

**Prose budget:** **Chronicle** embeds the full operator-ingested capture body (often thousands of words for Substack / long interviews). **Reflection** and **Foresight** stay comparatively short so the page stays roughly **~80% expert verbatim / ~20% WORK analysis** (short captures may skew slightly while boilerplate floors exist). **Mode D** (thin X / registry-only rows) may be much shorter if the capture is thin. No path dumps or `verify:` machinery in **Chronicle** body text—those belong in **`### Appendix`**.

---

## Preamble modes (pick one)

### Mode A — Substack essay

Long-form essay with **published** date; pin `source_url` in raw-input frontmatter.

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). Optional: echo in `thread.md` fence for watches / cross-expert duplication.
```

### Mode B — Judging Freedom (or third-party interview)

Host-dated conversation; use **aired** or **host date** per inbox / raw-input convention.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode B — Judging Freedom / interview (see raw-input `series`) · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). Optional: echo in `thread.md` fence for watches / cross-expert duplication.
```

### Mode C — YouTube / standalone video

Ritter monologue or guest spot with canonical `watch?v=` when pinned.

```markdown
**Expert:** `ritter` · **Aired:** YYYY-MM-DD · **Capture:** Mode C — YouTube (see raw-input `source_url`) · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). Optional: echo in `thread.md` fence for watches / cross-expert duplication.
```

### Mode D — Notebook / X stub

[`transcript.md`](transcript.md) holds mostly **`X | cold`** or registry lines without a long verbatim block for that date.

```markdown
**Expert:** `ritter` · **Ingest:** YYYY-MM-DD · **Capture:** Mode D — notebook / X stub · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). **Note:** May lack a single long capture—point to `days.md` / chapter seam when the lens hangs off a woven day.
```

---

### Prose emphasis (Chronicle / Reflection / Foresight)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Published:**) and for the required appendix bullet titles.
- Optional bold for the short title of a bullet inside **Foresight** when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Body scaffold

1. Preamble ends with **Expert:** … then **`**Words:** N (soft cap 3000)`** (full-file word count; over-cap suffix when needed). Regenerate via [`assemble_ritter_pages_verbatim.py`](../../../../scripts/strategy/assemble_ritter_pages_verbatim.py).
2. Horizontal rule `---` after the preamble block (before **Signal**).
3. `### Chronicle` — **expert verbatim**: full capture body from linked `raw-input` (after frontmatter), preserving Ritter’s wording; optional one-line label that this is operator-ingested text.
4. `### Reflection` — WORK-only notebook analysis (~20%): Ritter-lane arc, IHL/coercion reads, Hormuz or Russia–U.S. seams; **commentator vs wire** tier discipline on load-bearing claims.
5. `### Foresight` — falsifiers, resume lines, tier tags (bullets allowed).
6. Horizontal rule `---` before appendix.
7. `### Appendix` — machinery only.

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link under `raw-input/<YYYY-MM-DD>/` (slug examples: `substack-ritter-…`, `judging-freedom-…`, `ritter-rant-…`, etc.).
2. **Inbox / triage:** [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) — search `thread:ritter`, date, and capture-specific `verify:` / `SS |` / `JF |` / `YT |` hints.
3. **`thread:ritter`** · **verify:** one consolidated verify line.
4. **Canonical primary:** Substack URL, `watch?v=`, **Judging Freedom** link, or **X** permalink as applicable; **Not applicable** for pure Mode D stubs unless one URL is pinned.

---

## Raw-input naming (Ritter)

Verbatim lives under `raw-input/<date>/`. Ritter strategy-page files (`ritter-page-*.md`) live only under `experts/ritter/`. Machine-readable map (primary capture → `ritter-page-*.md`, modes, URLs): [`ritter-pages-manifest.yaml`](ritter-pages-manifest.yaml). Regenerate scaffolds with [`scripts/strategy/build_ritter_refined_pages.py`](../../../../scripts/strategy/build_ritter_refined_pages.py); CI check: [`scripts/strategy/verify_ritter_refined_pages.py`](../../../../scripts/strategy/verify_ritter_refined_pages.py).

## Machine checks (`verify_ritter_refined_pages.py`)

[`scripts/strategy/verify_ritter_refined_pages.py`](../../../../scripts/strategy/verify_ritter_refined_pages.py) (repo root):

- **Fail (exit 1):** each manifest row has `raw-input` on disk, matching `ritter-page-*.md`, and `transcript.md` contains that filename; each page has **`### Chronicle`**, **`### Reflection`**, **`### Foresight`**, **`### Appendix`** (legacy `### Signal` / `### Judgment` / `### Open` / `### Technical appendix` still accepted until regenerated); preamble has **`**Words:** N`** and **N** matches a full-file word count with the entire **`**Words:** …`** line removed (±5 tokens).
- **Warn (stderr, exit 0):** full-file count **> 3000** without **`Soft cap — pruning`** in **Reflection**; optional advisory if **Reflection + Foresight** share of (Chronicle + Reflection + Foresight) words exceeds **~35%**.
- **Soft cap:** **3000** is guidance only — full verbatim may stay on the page; re-running [`assemble_ritter_pages_verbatim.py`](../../../../scripts/strategy/assemble_ritter_pages_verbatim.py) overwrites page bodies from `raw-input`. Use `--no-page-shape` on the verifier for manifest/transcript-only checks.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in [`transcript.md`](transcript.md), add when missing:

- **`Verbatim:`** → relative link to the `raw-input` capture (or stub note if over triage budget).
- **`Refined day page:`** → `ritter-page-YYYY-MM-DD-<slug>.md` (from manifest / [`build_ritter_refined_pages.py`](../../../../scripts/strategy/build_ritter_refined_pages.py)). Transcript field label; the linked file **is** the strategy-page for that capture.
- **`Template:`** → [`ritter-page-template.md`](ritter-page-template.md) (optional header pointer).

---

## Paste scaffold (replace placeholders)

```markdown
# Ritter strategy page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode A — Substack · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). Optional: echo in `thread.md` fence for watches / cross-expert duplication.

---

### Chronicle



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:ritter`, YYYY-MM-DD)
- **`thread:ritter`** · **verify:** …
- **Canonical primary:** …
```

---

## Compliance checklist (retrofit / review)

1. Title: `# Ritter strategy page — YYYY-MM-DD (*…*)` (voice date + display title when present); filename is always `ritter-page-YYYY-MM-DD-<slug>.md`.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble identifies **Mode A–D**; **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`); **`**Words:**`** line (full file, soft cap 3000) before the first `---`.
4. `---` before `### Chronicle`; prose-only in Chronicle / Reflection / Foresight.
5. `---` before `### Appendix`.
6. Appendix bullets in order: capture → inbox → `thread:ritter` verify → canonical primary.
7. Relative links resolve from `experts/ritter/` (`../../raw-input/…`, `../../daily-strategy-inbox.md`).
