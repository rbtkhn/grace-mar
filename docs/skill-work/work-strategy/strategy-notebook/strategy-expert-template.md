# Strategy expert — templates (WORK only)
<!-- word_count: 2557 -->

**Single source** for the **four** on-disk files each commentator uses (profile, thread, transcript, **mind**). When adding someone new, either copy **each** section below into its own file (name on the section heading) or run `python3 scripts/expand_strategy_expert_template.py --expert-id <slug> [--full-name "..."]` from the repo root (`--dry-run` to preview). `validate_expert_profiles.py` validates real `strategy-expert-<id>.md` profiles only (this bundle file is skipped; `-mind.md` companions are skipped too). `validate_strategy_expert_threads.py` checks on-disk **`experts/<id>/thread.md`**, **`experts/<id>/<id>-thread-YYYY-MM.md`** (and flat `strategy-expert-<id>-thread.md` / `…-thread-YYYY-MM.md`) **journal-layer** month blocks (prose vs list-only hints, and **≥500 words** of **prose + blockquotes** per `## YYYY-MM` unless opted out — **verbatim-forward** policy). During a **phased** monthly split, **both** a monthly file and **`thread.md`** may exist; `discover_all_pages` uses **union** + **dedupe** (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread*). Use `--month MM` (`01`–`12`) to scope checks to one calendar month across all expert-thread files; omit for a full audit.

**Voice tier policy (defaults):** Tier **B** — compact **voice fingerprint** in profile — is the default once **`thread:`** ingests support it (typically ≥2 month blocks with ingest lines). Tier **C** — roster index + minimal profile — applies to **sparse** lanes until promoted. Tier **A** — long-form fingerprint in **`strategy-expert-<id>-mind.md`** (and/or legacy **`minds/CIV-MIND-*** for Tri-Frame). Numeric promotion defaults and **last reviewed** discipline live under [Profile → **Voice fingerprint (compact)**](#voice-fingerprint-compact).

Jump: [Profile](#profile-template) · [Thread](#thread-template) · [Transcript](#transcript-template) · [Mind](#mind-template)

**Compose skeleton (primary expert):** When the **EOD session** names this **`thread:`** as **primary**, default **Chronicle / Reflection / References / Foresight** pressure (and compressed `days.md` when composed there) follows [NOTEBOOK-PREFERENCES.md § Weave skeletons (S1–S5)](NOTEBOOK-PREFERENCES.md#weave-skeletons-s1-s5) — see the **primary → skeleton** table and **failure modes**; orthogonal to the **page-shape** menu ([STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *EOD compose — page-shape menu*).

---

<a id="profile-template"></a>

## Profile → `strategy-expert-<expert_id>.md`

# Strategy expert — <Full name> (`<expert_id>`)

WORK only; not Record.

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) — **`<expert_id>`** lane.

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | <full name> |
| **expert_id** | `<expert_id>` |
| **Role** | <one-line lane description> |
| **Default grep tags** | <tags in cold> |
| **Typical pairings** | <batch-analysis partners> |
| **Notebook-use tags** | <comma-separated from `orient`, `negotiate`, `validate`, `authorize`, `stress-test`, `narrate`, `historicize`> |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — Tier B

_Omit or leave “roster-only (Tier C)” until **`thread:`** density supports a card._

| Field | Value |
|-------|-------|
| **Voice tier** | `B` (compact) · `C` (roster-only until promoted) |
| **Voice fingerprint — last reviewed** | `YYYY-MM` — re-pass when **≥4** new `## YYYY-MM` sections since this date, **≥12** months wall time, or a **major crisis fork** (operator judgment). |

**Promotion defaults (all tunable)**

| Step | Heuristic |
|------|-----------|
| **C → B** | ≥**2** distinct calendar months each with ≥**1** `thread:` line, **or** ≥**1** thread block citing a named digest/transcript episode with Judgment — and cadence / failure modes / verify tier are stateable without pure guesswork. |
| **B → B+** | Append when ≥**2** new month blocks add a **novel** mechanism vs prior review, or log **Fingerprint changelog** in the thread. |
| **B → A** (long-form **`strategy-expert-<expert_id>-mind.md`** and/or `minds/`) | ≥**3** month blocks with `thread:` in a rolling **12-month** window **or** ≥**6** lifetime thread-months **and** (card would exceed ~**40–50** lines **or** long authentic-voice tables needed) **and** operator maintains the mind file — **override:** explicit decision anytime. |

**Governance:** LLM “sounds like” lines are **candidates** until merged into profile or **`strategy-expert-<expert_id>-mind.md`** / `minds/`.

## Convergence fingerprint

### Recurrent convergences

- `<expert_id>` + `<partner_id>` — <shared mechanism / shared claim>

### Convergence conditions

- This expert usually converges when:
  - <condition>

## Tension fingerprint

### Recurrent tensions

- `<expert_id>` x `<partner_id>` — <recurring disagreement>

### Tension conditions

- This expert usually tensions when:
  - <condition>

## Signature mechanisms

- <mechanism this expert returns to repeatedly>

## Recurrent claims

- <claim this expert makes across episodes>

## Failure modes / overreads

- <where this expert overstates / flattens / misses>

## Predictive drift / accuracy notes

- <what changed over time>
- <where prior calls held / failed>

## Active weave cues

- Pull this expert into weave when:
  - <condition>

## Knot-use guidance

- Best used for: <page types / question shapes>
- Usually insufficient alone for: <what needs pairing>

## History resonance defaults

- Typical HN chapter families: <history-notebook chapter ids>
- Typical mechanism hooks: <mechanism pointers>
- **One-way boundary:** Cite HN (and optional `MC-*` when the civilization thread is SSOT) from this expert surface — do not treat daily or thread text as a driver of HN edits; that path is **operator-originated** in `history-notebook/`. See [STRATEGY-NOTEBOOK-ARCHITECTURE — HN and strategy notebook: one-way citations](STRATEGY-NOTEBOOK-ARCHITECTURE.md#hn-and-strategy-notebook-one-way-citations).

## Published sources (operator web index)

1. <url>
2. <url>
3. <url>

## Seed

<operator standing notes>

---

**Companion files:** [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day rolling verbatim), thread file(s) — **canonical:** **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`** (one per month; see [Thread](#thread-template)), **legacy:** [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) / **`experts/<expert_id>/thread.md`**, and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form voice / linguistic fingerprint).

---

<a id="thread-template"></a>

## Thread → `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md` (one file per month; legacy `thread.md` optional)

# Expert thread — `<expert_id>`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + **[`raw-input/`](raw-input/README.md)** (durable bulk verbatim when used) + [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day triage / optional clips) + relevant **`strategy-page`** work (where this expert’s material was used).
**SSOT (month journal):** **Thread-embedded** **`strategy-page`** fences under the correct **`## YYYY-MM`** are the default **spine** for each month’s readable journal. Standalone **`experts/<expert_id>/*-page-*.md`** day files are **optional** overflow; mention or mirror them in a month only when **load-bearing** (or after duplicating the same logical page into a thread fence), not as the default month composition path.
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript (optional body) + **inbox links to `raw-input/`** for the same `thread:` lane, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile), [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day verbatim), and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form mind).

---

## Journal layer — Narrative (operator)

**Compose each `## YYYY-MM` from that month’s thread `strategy-page` set** (each fence’s `date=` falls in the month), not as a free-standing parallel essay and not as a long paraphrase of **`transcript.md`**. Dated week arcs are still welcome. Cover: how this voice **moves across the pages** you closed that month, convergence/tension with other **`thread:`** experts, and **Open** / **verify** pins. The **journal layer** is **not** overwritten by the **`thread`** script.

**Month shape (70 / 30 norm):** about **70%** **expert-anchored** material ( **`### Chronicle`** and markdown **`>`** lines inside thread **`strategy-page`** blocks for that month), about **30%** **connective** prose in the **skill-write** register (topic-led glue, **lede**/**closer**, paste-ready lines where useful) — the glue is **not** a second full analysis *parallel* to the pages. *Norm only; not a validator threshold.*

**Bookends (under each `## YYYY-MM`, above the machine layer):**

- **Lede** — a short **chapter open** right after the month heading, **before** the first `<!-- strategy-page:start` …` fence: what **carries in**, the **dominant watch** (if one), and how you are reading the month. *(Placeholder: one paragraph, topic-led.)*
- **Closer** — after the **last** `strategy-page` **end** fence for that month: what **stays open**, **verify** hooks, and one-line **arc** (what moved vs what repeated). *(Placeholder: one paragraph; may compress **Open** pins.)*

**List pages in a calendar month (read-only):** from repo root:

- `python3 scripts/list_strategy_pages_by_month.py --year-month YYYY-MM` — TSV (`expert_id`, `id`, `date`, `watch`, path); add `--expert-id <id>` for one lane.
- `python3 scripts/list_strategy_pages_by_month.py --year-month YYYY-MM --chronicle-snippets` — same TSV, then **advisory** first-paragraph + `>` line candidates per page (dumb `### Chronicle` parse; **never** auto-inserts; rubric still governs operator picks).
- `python3 scripts/list_strategy_pages_by_month.py --year-month YYYY-MM --json` — JSON array; add `--chronicle-snippets` to include a `snippets` object per row.

**Layout:** **Canonical:** **one thread file per calendar month** — **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`** (optional flat **`strategy-expert-<expert_id>-thread-YYYY-MM.md`**). Each file is **temporally bounded** to that month: journal + **`strategy-page`** fences + machine layer for **`YYYY-MM`** only; an optional **`## YYYY-MM`** heading matching the filename keeps grep / validator continuity. **Legacy:** one **`experts/<expert_id>/thread.md`** (or flat `strategy-expert-<expert_id>-thread.md`) with **multiple** **`## YYYY-MM`** segments until you run **`migrate_thread_md_to_monthly.py`**. For **2026** in a **single** legacy file: **Segment 1** = January (`## 2026-01`), **Segment 2** = February, **Segment 3** = March, **Segment 4** = April (ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that “Segment 2” in the month sense.

**Continuity (month open) —** optional at the start of a **new** month file: one short paragraph (what **carried** from the prior month, what is still **open**, which **pages** or **verify** pins matter) so a monthly file reads as a **chapter**, not a reset. Use especially when the expert’s lane spans several months of capture.

**Partial split (monthly + legacy):** while adding monthly files one at a time, you may still keep **`## YYYY-MM`** content in **both** a **`...-thread-YYYY-MM.md`** and **`thread.md`**. The **monthly** file is the **canonical** chapter for that month; when **both** are on disk, page discovery (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Thread* — *Partial monthly layout and union discovery*) **scans** both and **dedupes** ``strategy-page`` by ``id=``, preferring the **monthly** copy.

Add narrative **above** the `<!-- strategy-expert-thread:start -->` marker, **not** inside the machine block.

### Verbatim quote selection (for month lede, closer, and in-month lifts)

**Source order (strict):** (1) **`strategy-page`** in the **thread** for that `YYYY-MM` — primary pool **`### Chronicle`**; secondary: **`>`** lines **inside** that page (treat as *pre-elevated* month candidates; see [strategy-page-template.md](strategy-page-template.md) `### Chronicle`). (2) **Not default:** **`transcript.md`** for month bookend quotes (duplicates bulk SSOT); use only if **Chronicle** is empty/stub and you **name** the ingest day in the bookend.

| Priority | Signal | Rationale |
|----------|--------|------------|
| P1 | **Thesis / mechanism** (1–3 sentences, causal) | Analytical spine for the month. |
| P2 | **Watch-resonant** | Prefer pages whose `watch=` matches the month’s active **watches** in **`days.md` / [STATUS](STATUS.md)**. |
| P3 | **Repetition** | Same claim appears on multiple days → **one** crisp excerpt, not every repeat. |
| P4 | **Falsifier-linked** | If **Reflection** states a falsifier, prefer the **Chronicle** line the falsifier would test. |
| P5 | **Week coverage** | In dense months, ~**one** strong excerpt per calendar week **cluster** (avoid quote spam). |
| P6 | **Attribution** | Long lifts stay as blockquotes; short inline clips point to the same page (`date=` on the fence). |

**Exclusions:** throat-clearing, redundant everyone-had-it wire, duplicating the machine **### Page references** block as prose.

### Thread-embedded `strategy-page` blocks (journal layer)

Woven pages use the scaffold in [strategy-page-template.md](strategy-page-template.md): marker-fenced **`<!-- strategy-page:start` … `end` →`** under the correct **`## YYYY-MM`** in the **thread file for that month** — e.g. **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`** (or legacy **`thread.md`** when still on a single file). After edits, run **`python3 scripts/validate_strategy_pages.py`** from repo root (optional **`--strict-prose`** per that template’s **Machine checks**). Full section rules, optional **`### Appendix`**, and shared-`id` peer guidance live in **strategy-page-template.md** — not duplicated here.

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **Migrating from one `thread.md` to monthly files** — `python3 scripts/migrate_thread_md_to_monthly.py --apply` (repo root) splits journal **`## YYYY-MM`** blocks into **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`**; then run **`python3 scripts/strategy_thread.py`** so machine layers repopulate. See [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § Thread.

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (**one segment per file** when using **`<expert_id>-thread-YYYY-MM.md`** monthly files; multiple segments per file only in legacy **`thread.md`**). **Default:** **at least ~500 words** of substantive text per month-segment — **running prose** and/or **markdown blockquotes** (`>`) of the expert (verbatim-forward); see `validate_strategy_expert_threads.py`. List lines do not count. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the minimum and are **not** an equally canonical substitute unless the operator opts into ledger-only months (see HTML comment below). To scaffold, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root. Whole-file opt-out for alternate journal discipline: `<!-- strategy-expert-thread:verbatim-forward-journal-ok -->`.
- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id <expert_id> --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`<expert_id>-<start>-to-<end>.md`) plus **per-month** files (`<expert_id>/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.
- **`<!-- backfill:<expert_id>:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.
- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
- **Lens vs lane (Tri-Frame / `CIV-MIND-*` only):** Optional journal subsection **above** `<!-- strategy-expert-thread:start -->` when this expert has a **CIV-MIND-*** file: link `minds/CIV-MIND-….md`, state **lens ≠ transcript**, and when to use **`verify:lens-fold+<expert_id>`** (same **`<expert_id>`** as `thread:<expert_id>` and `strategy-expert-<expert_id>-*.md`) vs a **primary URL**. Fingerprint text still lives in **`strategy-expert-<expert_id>-mind.md`**; `minds/CIV-MIND-….md` remains the stable redirect path for bookmarks. Filled example: [`strategy-expert-mercouris-thread.md`](strategy-expert-mercouris-thread.md) (`verify:lens-fold+mercouris`).

---

<!-- strategy-expert-thread:start -->

## Machine layer — Extraction (script-maintained)

_Auto-generated from `transcript.md` + **on-disk and inbox** `raw-input/…` (de-duped **Recent raw-input (lane)**) + `strategy-page` blocks (+ optional empty legacy on-disk index). **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

_(Populated by `strategy_expert_corpus.py` / `strategy_thread.py` when `transcript.md` body lines exist.)_

### Recent raw-input (lane)

_(**Union** of on-disk `raw-input/**.md` with this expert’s `thread:` and inbox lines that point at `raw-input/…`—paths de-duped, disk first.)_

### Page references

_(Populated from `strategy-page` blocks; optional legacy index rows if present on disk.)_

_(No transcript, raw-input lane, or page material for extraction.)_

<!-- strategy-expert-thread:end -->

<!-- Optional: stable machine-readable ledger (YAML/JSON). Not overwritten by default extraction. Uncomment and edit if tooling needs it.

```thread-ledger
expert_id: <expert_id>
last_thread_run: null
legacy_index_paths: []
```

-->

---

<a id="transcript-template"></a>

## Transcript → `experts/<expert_id>/transcript.md`

# Expert transcript — `<expert_id>`

WORK only; not Record.

**Read path (operator):** **Durable dated bulk verbatim** for analysis and **Chronicle** lives in **[`raw-input/`](raw-input/README.md)** and in **thread-embedded** **`strategy-page`** (and optional standalone `*-page-*.md`). **Do not treat** this **7-day rolling** file as a **second SSOT** you must open to “get” the expert’s text. It is **pipeline plumbing**: an **inbox triage sink** plus what **`thread`** copies into the **machine layer**; it may hold **pointers** to `raw-input/`, one-line `thread:` **registry** rows, and **optional** short clips. **Empty or pointer-only** transcript is **valid** when full text lives under `raw-input/`.

**Source:** Verbatim **blocks** from [`daily-strategy-inbox.md`](daily-strategy-inbox.md) whose **first line** includes `thread:<expert_id>` (optional **continuation paragraphs** on following lines until the next top-level `- ` bullet or `##` heading), routed on ingest by `strategy_expert_transcript.py`.
**Length:** Target **≤ 2000 words** per ingest block; with **7-day** pruning, the whole file should stay near a **≤ ~20,000 word** soft ceiling (triage warns if exceeded).
**Retention:** 7-day rolling window; date sections older than 7 days are pruned automatically.
**Editing:** Operator may lightly edit for clarity after triage. Edits are preserved across triage runs (append-only, not overwrite).
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile), [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled thread), and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form mind).

**Optional refined page (same folder):** `experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md` (e.g. Mercouris: `mercouris-page-2026-04-21.md`; Pape: `pape-page-2026-04-20.md`). **Multiple refined pages for the same publication date are allowed:** `experts/<expert_id>/<expert_id>-page-YYYY-MM-DD-<slug>.md` (slug from the primary `raw-input` stem), **or** one consolidated file with **A / B / C** Chronicle blocks per [refined-page-template.md](refined-page-template.md). Chronicle / Reflection / Foresight artifact; **not** a substitute for full **verbatim** in [`raw-input/`](raw-input/README.md). Distinct from **`strategy-page`** fences in the expert **thread file(s)** unless you mirror judgment during EOD compose. **SSOT:** [refined-page-template.md](refined-page-template.md) (parameter **`{expert_id}`**). Each expert keeps a colocated **`experts/<expert_id>/<expert_id>-page-template.md`** **compat stub** linking the canonical file (e.g. [`experts/mercouris/mercouris-page-template.md`](experts/mercouris/mercouris-page-template.md), [`experts/pape/pape-page-template.md`](experts/pape/pape-page-template.md)). Introducing refined pages implies **bringing existing `*-page-*.md` files into compliance** with the canonical template for that expert. Do **not** add empty `*-page-template.md` files until the expert has at least one day page or a settled capture contract.

<a id="thesis-scaffold-pattern"></a>

### Thesis-first verbatim scaffold (canonical shape — use this, not ad hoc sidecar files)

**Do not** create separate `*-thesis-scaffold-FULL.md` files under `strategy-notebook/` for each episode. The **structure and convention** live **here** (template) and in [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md#verbatim-thesis-scaffold) + [THESIS-SCAFFOLD-CHECKLIST.md](THESIS-SCAFFOLD-CHECKLIST.md).

For a dated ingest where you want **bold theses**, **clear separation**, and **verbatim sentences** under each thesis:

1. Under **`## YYYY-MM-DD`**, keep the show/source line (e.g. **The Duran** · expert · air date).
2. **Above** the `~~~text` fence, add **markdown** blocks for human / GitHub preview:
   - **`**Short operator label**`** as the only heading for each block — one concise **bold** line (your words, not the expert’s). **Do not** number blocks (no “Thesis 1”, “Thesis 2”, etc.).
   - Then **one expert sentence per paragraph** (blank line between sentences). **Only** the expert’s words in those paragraphs — whole sentences, no paraphrase.
   - Between blocks, a horizontal rule **`---`** on its own line.
3. **`~~~text` … `~~~`:** Put the **same** verbatim body you want **`thread`** / corpus extraction to see — typically the **≤ ~2000 word** copy (may match the markdown block text or be a single continuous paste). `strategy_expert_corpus.py` reads the transcript file as text; it does not render markdown, but the **fence** carries the operational verbatim.

**Word budget:** Target **≤ ~2000 words** in the fence per ingest; use the checklist to drop whole sentences by thesis, or optional `python3 scripts/abridge_verbatim_transcript.py` for sentence-only boilerplate/length trim (does not assign theses). See architecture for **archive** if the fence is trimmed and you need the long episode elsewhere (git history, optional **full linear** file, or out-of-repo — not a second “scaffold FULL” naming pattern).

---

<!-- Triage appends new date sections below. Do not add content above this line. -->

---

<a id="mind-template"></a>

## Mind → `strategy-expert-<expert_id>-mind.md`

# Expert mind — <Full name> (`<expert_id>`)

WORK only; not Record.

**Epistemic fence:** This file is an **analytical voice / style fingerprint** for WORK (tri-mind, strategy passes). It is **not** biographical truth about a real person, **not** the Record, and **not** a substitute for **transcript-grounded** Judgment when a claim must be anchored to a primary line.

**Provenance:** **Grace-Mar SSOT** for Tri-Frame lanes is this **`-mind.md`** file (mapped corpus below). [`minds/CIV-MIND-*.md`](minds/) is a **stable redirect** path to this file for skills and upstream template naming. When **bootstrapping** a new expert from civ-mem, you may first map from `research/repos/civilization_memory/docs/templates/CIV–MIND–….md` into this spine — then keep `minds/CIV-MIND-*.md` as a redirect to this file (no duplicate body).

**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile), [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled thread), [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (verbatim ingests).

| Field | Value |
|-------|-------|
| **Status** | `stub` · `active` |
| **Mind — last reviewed** | `YYYY-MM` |

---

### I. Purpose and role

- What this voice **is** in the notebook (sharpening tool, interpretive lens, style constraint).
- What it is **not** (replacement for primary quotes, autonomous agent, etc.).

### II. Lane identity

- Short **register** summary: discipline, tempo, posture (operator-curated).

### III. Contrast and pairings (optional)

- Table or bullets: how this lane **differs** from adjacent **`thread:`** experts when both appear in a batch pass.

### IV. Linguistic fingerprint

- **Openers**, **transitions**, **hedging**, **argument markers** — transcript- or corpus-derived where possible.
- Subsections as needed (IV.A, IV.B, …).

### V. Domain relevance and register failure modes

- Where this voice is **load-bearing** in the notebook; where it tends to **overread** or flatten.

---

_Stubs ship with the above headings only; Tri-Frame lanes replace the body with mapped content here (SSOT); `minds/CIV-MIND-*.md` stays a redirect to this file for stable links._
