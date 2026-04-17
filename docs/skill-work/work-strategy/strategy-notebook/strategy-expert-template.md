# Strategy expert — templates (WORK only)

**Single source** for the **four** on-disk files each commentator uses (profile, thread, transcript, **mind**). When adding someone new, either copy **each** section below into its own file (name on the section heading) or run `python3 scripts/expand_strategy_expert_template.py --expert-id <slug> [--full-name "..."]` from the repo root (`--dry-run` to preview). `validate_expert_profiles.py` validates real `strategy-expert-<id>.md` profiles only (this bundle file is skipped; `-mind.md` companions are skipped too). `validate_strategy_expert_threads.py` checks on-disk `strategy-expert-<id>-thread.md` **journal-layer** month blocks (prose vs list-only hints, and **≥500 prose words** per `## YYYY-MM` unless opted out). Use `--month MM` (`01`–`12`) to scope checks to one calendar month across all expert-thread files; omit for a full audit.

**Voice tier policy (defaults):** Tier **B** — compact **voice fingerprint** in profile — is the default once **`thread:`** ingests support it (typically ≥2 month blocks with ingest lines). Tier **C** — roster index + minimal profile — applies to **sparse** lanes until promoted. Tier **A** — long-form fingerprint in **`strategy-expert-<id>-mind.md`** (and/or legacy **`minds/CIV-MIND-*** for Tri-Frame). Numeric promotion defaults and **last reviewed** discipline live under [Profile → **Voice fingerprint (compact)**](#voice-fingerprint-compact).

Jump: [Profile](#profile-template) · [Thread](#thread-template) · [Transcript](#transcript-template) · [Mind](#mind-template)

**Weave skeleton (primary expert):** When a **`weave`** names this **`thread:`** as **primary**, default **Signal / Judgment / Links / Open** pressure for the knot (and compressed `days.md` when woven there) follows [NOTEBOOK-PREFERENCES.md § Weave skeletons (S1–S5)](NOTEBOOK-PREFERENCES.md#weave-skeletons-s1-s5) — see the **primary → skeleton** table and **failure modes**; orthogonal to the **knot-shape** menu ([STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave command — knot-shape menu*).

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

## Published sources (operator web index)

1. <url>
2. <url>
3. <url>

## Seed

<operator standing notes>

---

**Companion files:** [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day rolling verbatim), [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled analytical thread), and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form voice / linguistic fingerprint).

---

<a id="thread-template"></a>

## Thread → `strategy-expert-<expert_id>-thread.md`

# Expert thread — `<expert_id>`

WORK only; not Record.

**Source:** Human **narrative journal** (below) + [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (verbatim ingests) + relevant **knot** files (where this expert’s material was used).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile), [`strategy-expert-<expert_id>-transcript.md`](strategy-expert-template.md#transcript-template) (7-day verbatim), and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form mind).

---

## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **knots**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-<expert_id>-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that “Segment 2” in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.
- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id <expert_id> --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`<expert_id>-<start>-to-<end>.md`) plus **per-month** files (`<expert_id>/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.
- **`<!-- backfill:<expert_id>:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.
- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
- **Lens vs lane (Tri-Frame / `CIV-MIND-*` only):** Optional journal subsection **above** `<!-- strategy-expert-thread:start -->` when this expert has a **CIV-MIND-*** file: link `minds/CIV-MIND-….md`, state **lens ≠ transcript**, and when to use **`verify:lens-fold+CIV-MIND-…`** vs a **primary URL**. Filled example: [`strategy-expert-alexander-mercouris-thread.md`](strategy-expert-alexander-mercouris-thread.md) (**CIV-MIND-MERCOURIS**).

---

<!-- strategy-expert-thread:start -->

## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + knot index. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

_(Populated by `strategy_expert_corpus.py` / `strategy_thread.py` when transcript lines exist.)_

### Knot references

_(Populated when knot index references this expert.)_

_(No transcript or knot material for extraction.)_

<!-- strategy-expert-thread:end -->

<!-- Optional: stable machine-readable ledger (YAML/JSON). Not overwritten by default extraction. Uncomment and edit if tooling needs it.

```thread-ledger
expert_id: <expert_id>
last_thread_run: null
knot_paths: []
```

-->

---

<a id="transcript-template"></a>

## Transcript → `strategy-expert-<expert_id>-transcript.md`

# Expert transcript — `<expert_id>`

WORK only; not Record.

**Source:** Verbatim **blocks** from [`daily-strategy-inbox.md`](daily-strategy-inbox.md) whose **first line** includes `thread:<expert_id>` (optional **continuation paragraphs** on following lines until the next top-level `- ` bullet or `##` heading), routed on ingest by `strategy_expert_transcript.py`.
**Length:** Target **≤ 2000 words** per ingest block; with **7-day** pruning, the whole file should stay near a **≤ ~20,000 word** soft ceiling (triage warns if exceeded).
**Retention:** 7-day rolling window; date sections older than 7 days are pruned automatically.
**Editing:** Operator may lightly edit for clarity after triage. Edits are preserved across triage runs (append-only, not overwrite).
**Companion files:** [`strategy-expert-<expert_id>.md`](strategy-expert-template.md#profile-template) (profile), [`strategy-expert-<expert_id>-thread.md`](strategy-expert-template.md#thread-template) (distilled thread), and [`strategy-expert-<expert_id>-mind.md`](strategy-expert-template.md#mind-template) (optional long-form mind).

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

**Provenance (when migrating from `minds/`):** If a [`minds/CIV-MIND-*.md`](minds/) file exists for this lane, populate this file by **mapping** that source into the section spine below (reformat; avoid one undifferentiated paste). Add an explicit line: *Derived from / aligned with `minds/CIV-MIND-….md`.* Until **tri-mind** / **minds-authentic-voice** paths are updated, skills may still cite `minds/CIV-MIND-*`; this **`-mind.md`** copy is the **strategy-notebook bundle-local** long read.

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

_Stubs ship with the above headings only; Tri-Frame lanes may replace the body with mapped content from `minds/CIV-MIND-*.md`._
