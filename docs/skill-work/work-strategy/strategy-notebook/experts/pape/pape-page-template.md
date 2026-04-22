# Pape refined day page — template

WORK only; not Record.

**Purpose:** Standalone **Signal / Judgment / Open** artifact for the `pape` expert. **Not** a substitute for full **verbatim** in [`raw-input/`](../../raw-input/README.md). Distinct from a **`strategy-page`** HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** Use [`strategy-page-template.md`](../../strategy-page-template.md) for `<!-- strategy-page:start … -->` blocks in thread files.

**Filename date:** Always use **`aired_date`** for `pape-page-YYYY-MM-DD.md`. If `ingest_date` or the `raw-input/` folder date differs, note it only in the **Technical appendix** (capture path still reflects on-disk location).

**Prose budget:** Target ~500–1000 words combined across **Signal**, **Judgment**, and **Open** for **Mode A** and **Mode B**. **Mode C** (X / social) is often much shorter. Grammatical prose only in those sections—no path dumps or `verify:` machinery there.

---

## Preamble modes (pick one)

### Mode A — Studio / long transcript

Long-form interview or multi-segment studio capture (e.g. Cyrus Janssen + embedded cold rows in `transcript-pape.md`).

```markdown
**Expert:** `pape` · **Aired:** YYYY-MM-DD · **Capture:** Mode A — studio / long transcript · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Third-party show interview

Guest spot with **pinned** canonical URL in raw-input frontmatter (`source_url`, `series`, `episode_title`).

```markdown
**Expert:** `pape` · **Aired:** YYYY-MM-DD · **Capture:** Mode B — third-party show (**Series** in raw-input) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode C — X / social thread or short ingest

`kind: x-post-text`, single post, or thin `transcript-pape.md` dominated by **X | cold** rows.

```markdown
**Expert:** `pape` · **Aired:** YYYY-MM-DD · **Capture:** Mode C — X / social (see raw-input `kind:`) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Signal` — fact framing and capture content.
3. `### Judgment` — Pape-lane arc (escalation trap, blockade stages, zero-sum binaries, domestic pocketbook, etc.); keep **homophone** and **tier** discipline (e.g. Janssen **“fourth center”** negotiation fork ≠ NYT **“4th power”** card—do not merge in Judgment).
4. `### Open` — falsifiers, resume lines, tier tags.
5. Horizontal rule `---` before appendix.
6. `### Technical appendix` — **machinery only**.

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link under `raw-input/…` (path uses **on-disk** folder date; may differ from `aired_date`—call out if so).
2. **Inbox / triage:** [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) — `search thread:pape`, aired date, and capture-specific grep hints.
3. **`thread:pape`** · **verify:** one consolidated verify line.
4. **Canonical video:** pinned `source_url` / watch ID when applicable; for **Mode C** pure X threads use **X profile / per-status permalinks** (pin when known) or **Not applicable** if only text paste.

---

## Transcript wiring

Under **`## YYYY-MM-DD`** in [`transcript.md`](transcript.md) (aired date), add when missing:

- **`Verbatim:`** → link to primary `raw-input` file (same label for all modes; X captures are still “verbatim” text on disk).
- **`Refined day page:`** → `pape-page-YYYY-MM-DD.md`.

Add **Template:** [`pape-page-template.md`](pape-page-template.md) in the transcript header metadata (see [`experts/mercouris/transcript.md`](../mercouris/transcript.md) pattern).

---

## Paste scaffolds

**Mode A / B (long or show)** — adjust preamble Mode line.

```markdown
# Pape day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `pape` · **Aired:** YYYY-MM-DD · **Capture:** Mode A — studio / long transcript · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Signal



### Judgment



### Open



---

### Technical appendix

- **Full verbatim (capture):** [raw-input/…](../../raw-input/….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:pape`, YYYY-MM-DD)
- **`thread:pape`** · **verify:** …
- **Canonical video:** …
```

**Mode C** — shorter body; fourth bullet may reference X permalinks or N/A.

---

## Compliance checklist

1. Title `# Pape day page — YYYY-MM-DD` matches **`aired_date`**.
2. `WORK only; not Record.`
3. Preamble identifies **Mode A, B, or C** and uses **standalone file under `experts/pape/`**.
4. `---` before `### Signal`; prose-only in Signal/Judgment/Open.
5. `---` before `### Technical appendix`.
6. Appendix bullets in order: capture → inbox → `thread:pape` verify → canonical / X.
7. Relative links from `experts/pape/` (`../../raw-input/…`, `../../daily-strategy-inbox.md`).
