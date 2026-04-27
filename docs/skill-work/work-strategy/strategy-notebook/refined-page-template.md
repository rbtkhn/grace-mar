# Refined page template (all experts)

<!-- word_count: template ~3k target; see § Length -->

WORK only; not Record.

**Publication vocabulary (formal pin):** **Machine** — use YAML / cold-line tag **`pub_date:YYYY-MM-DD`** (and [`raw-input/`](../raw-input/README.md) folder rules). **Human** — preamble line **`Published:`** (date). **Do not** use an “aired” block or **`aired:`** as the norm; full spec: [raw-input README — Publication vocabulary](../raw-input/README.md#publication-vocabulary-formal-pin), [STRATEGY-NOTEBOOK-ARCHITECTURE.md — publication vocabulary](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#publication-vocabulary-formal-pin).

**SSOT hierarchy (two layers):**

1. **[`raw-input/`](../raw-input/README.md)** is the **SSOT for literal capture** — the archived words (and capture metadata) of the source. The refined page’s **`### Verbatim`** is **always** excerpted *from* that file (or a defined lane of it) and may be **condensed for the page word budget** (see **§ Length**); the raw file remains the **unabridged** reference. If an on-page quote disagrees with the raw on **wording**, **fix the page** (or the raw); do not invent counterfactual lines.
2. **This file shape** (`experts/…/ *-page-*.md`) is the **SSOT for notebook work** — the object you cite when composing **`strategy-page`** blocks, expert **`thread.md`**, and **`chapters/…/days.md`**: **lane**, **sibling links**, **Reflection** / **Foresight** judgment, and the readable **`### Verbatim`** copy. Downstream analysis should **default to refined pages** as the handle for “this capture / this expert-lane,” not re-derive structure by re-ingesting raw unless you are **auditing the literal** or **editing capture**.

**Purpose:** Standalone **refined page** for expert **`{expert_id}`** (replace token everywhere below when pasting scaffolds). **`### Verbatim`** carries **expert (or host/guest lane) text from** linked [`raw-input/`](../raw-input/README.md)—**lightly cleaned and formatted**, and **sized to the page budget** in **§ Length** when the transcript is long; **`### Reflection`** and **`### Foresight`** are **operator analysis** (**may be stubbed** on ingest, completed in a later pass). **Naming:** **`### Chronicle`** remains the verbatim-first heading inside **thread-embedded** **`strategy-page`** fences ([strategy-page-template.md](strategy-page-template.md)); **`### Verbatim`** is the refined-page heading so **Chronicle** names the **thread / `days.md` day-block** weave, not this standalone file. Distinct from a **`strategy-page`** HTML fence in **`thread.md`** (or **`*-thread-YYYY-MM.md`**) unless you duplicate judgment there during EOD compose.

**Thread-embedded pages:** For `<!-- strategy-page:start … -->` blocks in monthly or legacy thread files, use [`strategy-page-template.md`](strategy-page-template.md) instead of this file.

**Filename:** Default **`{expert_id}-page-YYYY-MM-DD.md`** (publication / **`pub_date`** anchor). **Multiple refined pages for the same publication date are allowed:** **`{expert_id}-page-YYYY-MM-DD-<slug>.md`** with **`<slug>`** from the primary `raw-input` stem so filenames stay unique. **Alternatively,** consolidate same-day captures into **one** refined file with **A / B / C** Verbatim blocks when this template’s same-day pattern applies. If the `raw-input/` folder date differs (ingest batching), note it in **`### Appendix`**. Under **`experts/{expert_id}/transcript.md`** when used, add one **`Refined page:`** line per refined file for that date.

**Length (target budget):** **~3000 words** per refined page (soft target, not a hard cap). **~70–80%** of those words should live under **`### Verbatim`** (verbatim transcript text for this expert or lane). **~20–30%** = preamble, **`### Reflection`**, **`### Foresight`**, and **`### Appendix`**. When a lane’s transcript **exceeds** the verbatim share at ~3000 total words, **condense** the on-page **`### Verbatim`** by pruning (e.g. head+tail of the lane with a short omission line; never paraphrase into “Verbatim” — use **operator analysis** only in Reflection/Foresight). **Automation:** from repo root, `python3 scripts/strategy/refined_page_word_budget.py check <*page*>.md` and `python3 scripts/strategy/refined_page_word_budget.py condense <raw.md> --lane <key>`; composition passes that build **strategy expert** / refined pages (including EOD and assistants) should run **check** after large ingests. **Unabridged** text always remains in **`raw-input/`**; note omissions in **Appendix** (see bullet order). No path dumps or `verify:` in body sections—**`### Appendix`** only (unless grammatical prose in Reflection explicitly cites a tier).

### Prose emphasis (Verbatim / Reflection / Foresight)

Do not scatter `**inline bold**` through running paragraphs for rhetorical stress, “beat” words, or decoration. Use normal weight for body copy. Bold is allowed for:

- Line-leading labels in the preamble (e.g. **Expert:**, **Published:**) and for the required appendix bullet titles (see Appendix bullet order below).
- Optional bold for the short title of a bullet inside **Foresight** when the bullet is a labeled stub (title only—not the whole sentence).

Section titles use `###` headings, not bold.

---

## Preamble modes — core (default)

Pick **one** unless your ingest pipeline documents a second same-day block (A/B/C Verbatim in one file).

### Mode A — Primary dated capture

Use when **Verbatim** carries the full capture text for this expert’s main artifact for that calendar day (broadcast, interview, essay, or long transcript) with a canonical **publication** date (same anchor as **`pub_date`**).

```markdown
**Expert:** `{expert_id}` · **Published:** YYYY-MM-DD · **Artifact:** refined page (standalone file under `experts/{expert_id}/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode B — Notebook stub

Use when **`transcript.md`** (in **`experts/{expert_id}/`**) holds only a `notebook |` row or thin registry lines for that date (no long verbatim). Point to the chapter seam when the lens hangs off a woven day.

```markdown
**Expert:** `{expert_id}` · **Ingest:** YYYY-MM-DD · **Artifact:** refined page (standalone file under `experts/{expert_id}/`). **Note:** This date may be a `notebook |` lens row only—not a full capture verbatim. [Optional: tri-mind / chapter pointer — e.g. `days.md` § anchor.]
```

---

## Preamble modes — extended (ritter-shaped ingest; optional elsewhere)

Use these when **`{expert_id}`** is **`ritter`** or when another expert’s ingest matches the same capture shapes (adapt **Expert** / paths).

### Mode C — Substack essay

Long-form essay with **published** date; pin `source_url` in raw-input frontmatter.

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode C — Substack · **Artifact:** refined page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode D — Judging Freedom (or third-party interview)

Host-dated conversation; use **Published:** or **host date** per inbox / raw-input convention (same calendar anchor as **`pub_date`**).

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode D — Judging Freedom / interview (see raw-input `series`) · **Artifact:** refined page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode E — YouTube / standalone video

Monologue or guest spot with canonical `watch?v=` when pinned.

```markdown
**Expert:** `ritter` · **Published:** YYYY-MM-DD · **Capture:** Mode E — YouTube (see raw-input `source_url`) · **Artifact:** refined page (standalone file under `experts/ritter/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.
```

### Mode F — Notebook / X stub

**`transcript.md`** (under **`experts/ritter/`**) holds mostly **`X | cold`** or registry lines without a long verbatim block for that date.

```markdown
**Expert:** `ritter` · **Ingest:** YYYY-MM-DD · **Capture:** Mode F — notebook / X stub · **Artifact:** refined page (standalone file under `experts/ritter/`). **Note:** May lack a single long capture—point to `days.md` / chapter seam when the lens hangs off a woven day.
```

---

## Body scaffold

1. Horizontal rule `---` after the preamble.
2. `### Verbatim` — **Transcript text** from the linked `raw-input` capture (after YAML frontmatter when present), for this **expert or lane** only: **lightly cleaned and formatted**—paragraphing, spacing, obvious ingest artifacts, optional speaker labels; **do not** replace the expert’s words with summary or paraphrase. If the lane is **longer than the § Length verbatim budget** allows, **prune/condense** (machine or operator) while keeping all remaining text **quote-faithful**; mark omissions (inline italic one-liner and/or **Appendix**). The file under `raw-input/` is always the **full** capture; on-page may be a **subset**. **Notebook stub modes** (core Mode B, or extended Mode F for `ritter`): brief stub or pointer only.
3. `### Reflection` — **Operator analysis:** `{expert_id}`-lane arc; keep verification discipline explicit where load-bearing claims sit in commentator tier. _(When `{expert_id}` is `ritter`, add IHL / coercion / Hormuz or Russia–U.S. seams in prose when material.)_ **May be stubbed** until a later operator pass.
4. `### Foresight` — **Operator analysis:** falsifiers, resume lines, tier tags (bullets allowed). **May be stubbed** until a later operator pass.
5. Horizontal rule `---` before appendix.
6. `### Appendix` — machinery only (paths, inbox grep, `thread:{expert_id}`, canonical URL).

**Appendix bullet order (required):**

1. **Full verbatim (capture):** link to the capture under `raw-input/<YYYY-MM-DD>/` (slug varies by ingest pipeline) — always the **unabridged** file, even if **`### Verbatim`** is condensed.
2. **Omissions (if any):** when on-page `### Verbatim` is a **pruned** subset, one line: approximate **words omitted** and that the **full** text is the **Full verbatim (capture)** link. Omit this bullet if the page includes the full lane text.
3. **Inbox / triage:** link to [`daily-strategy-inbox.md`](daily-strategy-inbox.md) with grep hints (`thread:{expert_id}`, date, and for stub modes the `notebook |` / `verify:` / capture tails as used in inbox).
4. **`thread:{expert_id}`** · **verify:** one line consolidating verify tier for this page (include **`pub_date:YYYY-MM-DD`** grep hint where load-bearing).
5. **Canonical primary:** pin `source_url`, video ID, article URL, or X permalink when known; for pure stub modes use **Not applicable** unless one URL is pinned.

---

## Raw-input naming

Verbatim lives under `raw-input/<date>/`. Refined pages live only under **`experts/{expert_id}/`**.

**Multi-expert lane split:** `### Verbatim` on each refined page = **that speaker’s lines** from the shared raw file (concatenate turns), not a paraphrase; then **apply the § Length budget** (often **~70–80%** of **~3000** words in Verbatim — use [`refined_page_word_budget.py`](../../../scripts/strategy/refined_page_word_budget.py) **condense** if needed). Extract: [`scripts/strategy/extract_transcript_speaker_lanes.py`](../../../scripts/strategy/extract_transcript_speaker_lanes.py). See [`.cursor/skills/strategy-notebook-lane-split/SKILL.md`](../../../.cursor/skills/strategy-notebook-lane-split/SKILL.md).

---

## MEM / topic-trace boundary (optional)

When **`### Reflection`** or **`### Foresight`** draws on **CIV-MEM** routing, **MEM CONNECTIONS**, or **structural analogy** from the read-only upstream corpus, keep that work in the **WORK · DERIVED** lane: do not treat graph patterns as **Record** truth or as **civilization_memory** canon edits. Governing contract: [topic-trace-contract.md](../../work-civ-mem/topic-trace-contract.md). For a **standalone** bounded trace file (separate from this **refined page**), use [topic-trace-template.md](../../work-civ-mem/topic-trace-template.md). **`### Verbatim`** remains **verbatim expert capture** only—do not merge MEM synthesis into Verbatim as if it were the expert’s words.

---

## Ritter lane (optional machine index and validators)

Applies when **`{expert_id}`** is **`ritter`** (paths relative to **`experts/ritter/`**; adjust if you move manifests).

- Optional machine index: [`experts/ritter/ritter-pages-manifest.yaml`](experts/ritter/ritter-pages-manifest.yaml).
- Legacy tooling: [`scripts/strategy/assemble_ritter_pages_verbatim.py`](../../../scripts/strategy/assemble_ritter_pages_verbatim.py), [`scripts/strategy/build_ritter_refined_pages.py`](../../../scripts/strategy/build_ritter_refined_pages.py).

### Machine checks (`verify_ritter_refined_pages.py`)

[`scripts/strategy/verify_ritter_refined_pages.py`](../../../scripts/strategy/verify_ritter_refined_pages.py) (repo root): manifest rows, `raw-input` on disk, `transcript.md` backlinks, and page spine **`### Verbatim`**, **`### Reflection`**, **`### Foresight`**, **`### Appendix`** (legacy **`### Chronicle`** on older refined files; legacy `### Signal` / `### Judgment` / `### Open` / `### Technical appendix` still accepted until regenerated). **`**Words:** N`** is **optional** (Ritter): when present it must match full-file word count with that line stripped (±5 tokens); when omitted, that bookkeeping is skipped. **General** refined-page **target** is still **~3000 words** / **70–80% verbatim** per **§ Length**; use [`refined_page_word_budget.py`](../../../scripts/strategy/refined_page_word_budget.py) for all experts. An optional Reflection+Foresight **share** advisory in the Ritter script runs only when **`**Words:**`** is present. Use `--no-page-shape` for manifest/transcript-only checks. Other experts may gain full parity with the Ritter script later. Apply **`ritter` manifest** section only to **`ritter`**.

---

## Transcript wiring

Under the matching `## YYYY-MM-DD` in **`experts/{expert_id}/transcript.md`**, add (when not already present):

- **`Verbatim:`** → relative link to the `raw-input` capture.
- **`Refined page:`** → `{expert_id}-page-YYYY-MM-DD.md` or `{expert_id}-page-YYYY-MM-DD-<slug>.md` (one line per refined file).
- **`Template:`** → optional pointer to the canonical [**`refined-page-template.md`**](refined-page-template.md) **or** to the thin **`{expert_id}-page-template.md`** stub in the same folder. Old bookmarks may still use the redirect [**`refined-page-template.md`**](refined-page-template.md).

---

## Paste scaffold (replace `{expert_id}` and placeholders)

**Core Mode A example:**

```markdown
# {ExpertTitle} refined page — YYYY-MM-DD

WORK only; not Record.

**Expert:** `{expert_id}` · **Published:** YYYY-MM-DD · **Artifact:** refined page (standalone file under `experts/{expert_id}/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate the same judgment there during EOD compose.

---

### Verbatim



### Reflection



### Foresight



---

### Appendix

- **Full verbatim (capture):** [raw-input/YYYY-MM-DD/…](../../raw-input/YYYY-MM-DD/….md)
- **Omissions (if any):** — *omit bullet if `### Verbatim` is full lane text*
- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:{expert_id}`, YYYY-MM-DD)
- **`thread:{expert_id}`** · **verify:** full-text + raw-input + pub_date:YYYY-MM-DD
- **Canonical primary:** pin when known (see raw-input frontmatter / cold line)
```

Use **`# {ExpertTitle}`** as a human-facing title case of the expert display name (operator choice); filename stays **`{expert_id}-page-…`**.

---

## Compliance checklist (retrofit / review)

1. Title: `# … refined page — YYYY-MM-DD` (optional short parenthetical when multiple files share the publication date); filename uses `-<slug>` when split.
2. `WORK only; not Record.` on its own line after the title.
3. Preamble matches one chosen mode; **Artifact:** line uses “refined page (standalone file under `experts/{expert_id}/`)” verbatim.
4. `---` before `### Verbatim`.
5. `### Verbatim`, `### Reflection`, `### Foresight` present; **Verbatim** = transcript text (lightly cleaned, optionally condensed for **§ Length**; never paraphrase as Verbatim)—no `verify:` / path machinery there; **Reflection** / **Foresight** = operator analysis (stubs OK). No decorative bold except lane rules (see Prose emphasis). Prefer **~3000** total words, **~70–80%** in Verbatim (`refined_page_word_budget.py check`).
6. `---` before `### Appendix`.
7. Appendix bullets in order: Full verbatim (capture) → Omissions (if pruned) → Inbox / triage → `thread:{expert_id}` · verify → Canonical primary.
8. Relative links resolve from **`experts/{expert_id}/`** (typically `../../raw-input/…`, `../../daily-strategy-inbox.md`, `../../chapters/…` when citing `days.md`).

---

## Compat stubs

Each expert keeps **`experts/<expert_id>/<expert_id>-page-template.md`** as a **short stub** linking here so existing `Template:` lines and bookmarks stay valid. Edit policy: **change this file**; change per-expert stubs only when the compat paragraph itself needs revision. Legacy on-disk name [refined-day-page-template.md](refined-day-page-template.md) remains a one-hop redirect to this file.
