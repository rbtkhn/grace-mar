# Pape refined day page — template

WORK only; not Record.

**Purpose:** Standalone **Chronicle / Reflection / Foresight** artifact for the `pape` expert. **Not** a substitute for full **verbatim** in [`raw-input/`](../../raw-input/README.md). Distinct from a **`strategy-page`** HTML fence in [`thread.md`](thread.md) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** Use [`strategy-page-template.md`](../../strategy-page-template.md) for `<!-- strategy-page:start … -->` blocks in thread files.

**Filename date:** Always use **`published_date`** (Substack byline / operator publication stamp) for `pape-page-YYYY-MM-DD.md`. If `ingest_date` or the `raw-input/` folder date differs, note it only in the preamble (**Ingest** logged …) or appendix; capture paths still reflect on-disk location.

**Prose budget:** Target ~500–1000 words **equivalent** in **Chronicle** (often as **compressed beat lines**—see below)—plus proportionate **Reflection** / **Foresight**. **Mode C** (X / social) is often much shorter. Keep **`verify:`** tails, path dumps, and inbox machinery out of Chronicle / Reflection / Foresight body text—those belong in **`### Appendix`**.

### Prose emphasis (Pape Chronicle convention)

Pape refined pages typically use **heavy token-level bold** in **Chronicle** (and sometimes **Reflection**)—a `**word** **word**` beat pattern for compression, scan, and grep. That is **intentional** for this lane and **differs** from the Mercouris “normal weight body” rule. Do not “normalize” existing Pape pages to Mercouris prose style unless you are deliberately changing lane contract.

Section titles use `###` headings, not bold. Line-leading preamble labels (**Expert:**, **Published:**) stay bold per repo habit.

---

## Preamble modes (pick one)

Most current ingests are **Mode D** (Substack). Modes A–C remain for non-Substack captures.

### Mode A — Studio / long transcript

Long-form interview or multi-segment studio capture (cold rows in [`transcript.md`](transcript.md)).

```markdown
**Expert:** `pape` · **Published:** YYYY-MM-DD · **Capture:** Mode A — studio / long transcript · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Third-party show interview

Guest spot with **pinned** canonical URL in raw-input frontmatter (`source_url`, `series`, `episode_title`).

```markdown
**Expert:** `pape` · **Published:** YYYY-MM-DD · **Capture:** Mode B — third-party show (**Series** in raw-input) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode C — X / social thread or short ingest

`kind: x-post-text`, single post, or thin transcript dominated by **X | cold** rows.

```markdown
**Expert:** `pape` · **Published:** YYYY-MM-DD · **Capture:** Mode C — X / social (see raw-input `kind:`) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode D — Substack (*Escalation Trap*)

Essay or ledger post; pin **`source_url`** and **`published_date`** in raw-input frontmatter. Note **paid** vs public in preamble when it affects verify tier.

```markdown
**Expert:** `pape` · **Published:** YYYY-MM-DD · **Capture:** Substack — *Escalation Trap* (*Post Title*; operator paste; **paid** tier when applicable) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose. **Ingest** logged YYYY-MM-DD.
```

---

## Same-day multiple posts (one publish date)

When **more than one** primary Substack (or mixed) capture shares **`published_date`** (e.g. [pape-page-2026-03-05.md](pape-page-2026-03-05.md), [pape-page-2026-03-24.md](pape-page-2026-03-24.md)):

1. **Single** refined file: `pape-page-YYYY-MM-DD.md`.
2. **`### Chronicle`:** ordered blocks **`A —`** *Title* **(**[Substack](https://…)**):** … **`B —`** … **`C —`** … as needed. Each letter matches one verbatim file.
3. **`### Reflection` / `### Foresight`:** tag bullets with **(A)** / **(B)** / **(C)** when judgments differ by post.
4. **`### Appendix`:** **`Full verbatim (A):`** … **`Full verbatim (B):`** … ; mark **(**paid** **tier** **)** on the bullet where relevant. **`Canonical Substack URLs:`** — list all, with paid labels.
5. **[`transcript.md`](transcript.md):** one **`Verbatim:`** line per capture under the same **`## YYYY-MM-DD`**; note **(**paid** **tier** **)** on the paste line when useful. **One** **`Refined day page:`** line.
6. **[`daily-strategy-inbox.md`](../../daily-strategy-inbox.md):** one **SS | cold** row per post (same publish date), each pointing at the shared day page + its raw path.
7. **Raw-input:** cross-link via **`related_same_series`** between same-day captures.

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Chronicle` — compressed thesis / ledger / beats from the capture(s).
3. `### Reflection` — Pape-lane arc (escalation trap, Hormuz / blockade stages, Stage I–III, domestic pocketbook, etc.); **homophone** and **tier** discipline (e.g. negotiation fork vs press shorthand—do not merge distinct phrases in Judgment).
4. `### Foresight` — falsifiers, resume lines, tier tags (bullets allowed); **Cross-weave** bullets welcome.
5. Horizontal rule `---` before appendix.
6. `### Appendix` — **machinery only**.

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link under `raw-input/…` — for multi-post days use **(A)**, **(B)**, **(C)** sub-bullets (path uses **on-disk** folder date; may differ from `published_date`—call out if so).
2. **Adjacent arc:** neighbor day pages when helpful (`pape-page-…` · `pape-page-…`). Omit only when there is no natural seam.
3. **Inbox / triage:** [`daily-strategy-inbox.md`](../../daily-strategy-inbox.md) — `search thread:pape`, publish date, capture-specific grep hints.
4. **`thread:pape`** · **verify:** one consolidated verify line (include **paid-tier** / **DOD-tier** / **wire-tier** as appropriate).
5. **Canonical URL** or **Canonical Substack URLs:** pinned `source_url`(s); for **Mode C** use **X** permalinks or **Not applicable**. For multi-post days, list every canonical link here (match Appendix verbatims).

---

## Transcript wiring

Under **`## YYYY-MM-DD`** in [`transcript.md`](transcript.md) (publish date), add when missing:

- **`Verbatim:`** → link to each primary `raw-input` file (same label for all modes; multiple lines when same-day multi-post).
- **`Refined day page:`** → `pape-page-YYYY-MM-DD.md` (once per date).
- **`Template:`** → [`pape-page-template.md`](pape-page-template.md) (optional).

---

## Paste scaffolds

### Mode D (Substack) — single post

```markdown
# Pape day page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `pape` · **Published:** YYYY-MM-DD · **Capture:** Substack — *Escalation Trap* (*Title*; operator paste) · **Artifact:** refined day page (standalone file under `experts/pape/`). **Not** a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Chronicle



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Adjacent arc:** [pape-page-….md](pape-page-….md) · [pape-page-….md](pape-page-….md)
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:pape`, YYYY-MM-DD)
- **`thread:pape`** · **verify:** …
- **Canonical URL:** [Title](https://escalationtrap.substack.com/p/…)
```

### Same-day two posts (A / B)

Use two Chronicle blocks **A —** / **B —**, two verbatim appendix lines, two canonical URLs. Mirror **Foresight** with **(A)** / **(B)** if verify paths differ.

### Mode C — X / social

Same scaffold as Mode D but shorter body; fourth appendix bullet may be **X** permalinks or **Not applicable**.

---

## Compliance checklist

1. Title `# Pape day page — YYYY-MM-DD` matches **`published_date`** (one file per publish date, including multi-post days).
2. `WORK only; not Record.`
3. Preamble identifies capture mode (**Substack** / Mode A–C) and **Artifact:** **standalone file under `experts/pape/`**.
4. `---` before `### Chronicle`; Chronicle / Reflection / Foresight contain no `verify:` machinery or path dumps.
5. `---` before `### Appendix`.
6. Appendix bullets in order: **Full verbatim** (A/B/C if needed) → **Adjacent arc** (if any) → **Inbox** → **`thread:pape` verify** → **Canonical URL(s)**.
7. Relative links from `experts/pape/` (`../../raw-input/…`, `../../daily-strategy-inbox.md`).
8. Same-day multi-post: transcript has **multiple** `Verbatim:` lines; inbox has **multiple** rows; raw-input **`related_same_series`** cross-linked.
