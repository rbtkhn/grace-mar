# Strategy page template (`strategy-page`)

WORK only; not Record.

**Contract:** A **strategy-page** is any notebook page that uses the **same scaffold** below: **`### Chronicle`**, **`### Reflection`**, **`### Foresight`**, optional **`### Appendix`**, and the **length / cadence** rules. By default **`### Chronicle`** carries the **full verbatim** capture (lightly cleaned and formatted); **`### Reflection`** and **`### Foresight`** are **operator analysis** and **may be stubbed** on first write. Experts implement that contract in one or both **surfaces**:

1. **Thread fence (HTML comments):** `<!-- strategy-page:start … -->` … `<!-- strategy-page:end -->` in the expert’s **`thread.md`** (or monthly **`*-thread-YYYY-MM.md`**) under the correct **`## YYYY-MM`**. This is what [`validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) parses.
2. **Expert file (standalone):** **`experts/<expert_id>/<expert_id>-page-*.md`** — e.g. [`ritter-page-template.md`](experts/ritter/ritter-page-template.md), `mercouris-page-*.md`. Same strategy-page contract; file usually sits beside **`raw-input/`** with capture preamble and appendix links. **Not** checked by `validate_strategy_pages.py` unless you **duplicate** the same logical page into a thread fence (e.g. cross-expert **`id` / `date` / `watch`**).

**Where (thread fence):** Add a `<!-- strategy-page:start … -->` … `<!-- strategy-page:end -->` block under the correct **`## YYYY-MM`** in the expert’s **thread file for that month** — **`experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`** when using monthly thread files, or **`experts/<expert_id>/thread.md`** under the matching month heading when using a single legacy file. The page’s **`date="YYYY-MM-DD"`** must fall in that **`YYYY-MM`**. For the same logical analysis across experts, **duplicate** the block into each expert’s file with the same **`id=`** and **`date=`** (see [watches/README.md](watches/README.md)). Thread layout details: [strategy-expert-template.md § Thread](strategy-expert-template.md#thread-template).

**Required sections:** **`### Chronicle`**, **`### Reflection`**, and **`### Foresight`**. **`### Chronicle`** is normally the **full verbatim** body (expert speech / essay text), lightly cleaned—**not** a paraphrase digest. Markdown **`>`** blockquotes **inside Chronicle** are optional **lift markers**: lines you may **re-elevate** into the expert **thread** month journal (lede/closer) when composing that month; they do not change `validate_strategy_pages.py` behavior. Pre-elevation to month bookends is **operator-picked** per the **verbatim quote selection** rubric in [strategy-expert-template.md](strategy-expert-template.md#thread-template) (Thread). **`### Reflection`** / **`### Foresight`** are **operator analysis** (judgment, falsifiers, resume lines—grammatical prose when filled in); **stubs are OK** until a later pass. List dumps and machinery belong in **`### Appendix`** when used, or overflow — see below.

**Optional `### Appendix`:** Omit when the page is short and has **no** paste-ready machinery (URLs, `thread:`, `verify:`, `batch-analysis` tails, bare paths). When you **do** need that material, add **`### Appendix`** and keep **machinery only** there — see **Rules** and **Machine checks** below. **Do not** rename this heading: [`validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) splits prose vs appendix on the exact string **`### Appendix`** (match is case-insensitive in the script). “Optional” means **omit the section entirely**, not use a different title.

**Length:** **No** enforced word limit on a single page; very long one-file captures are uncommon in practice. Words in **`### Appendix`** (when present) are **outside** readable “body” weighting for compose discipline. If a thread-fence page grows unwieldy, split logically → `days.md`, a second page **`id`**, or **References** in the notebook sense.

**Cadence:** Prefer **one end-of-day page session** per day—do not create or extend `strategy-page` blocks continuously during the day; daytime capture stays in [daily-strategy-inbox.md](daily-strategy-inbox.md).

**strategy-state-iran (institutional lane — not commentator-shaped):** **Primary** new work uses [**channels/**](strategy-state-iran/channels/README.md) (institutional routing) + [**weave/**](strategy-state-iran/weave/) (`YYYY-MM-institutional-ledger` + `institutional-weave`) with [**signal class**](strategy-state-iran/templates/INSTITUTIONAL-LEDGER-SIGNAL-CLASSES.md) headings, **not** person-primary top organization. Templates: [announced vs material](strategy-state-iran/templates/ANNOUNCED-VS-MATERIAL-BLOCK.md), [institutional scorecard](strategy-state-iran/templates/INSTITUTIONAL-SCORECARD.md). [**Clusters**](strategy-state-iran/clusters/) hold multi-day objects; [translation-provenance](strategy-state-iran/translation-provenance/) for republication chains. **Legacy:** [`strategy-state-iran/voices/iri-institutional/thread.md`](strategy-state-iran/voices/iri-institutional/thread.md) retains **tri-voice** **`### Voice — …`** + **`strategy-page`** for **history** and **inbound** links; see migration note at top of that file. Per-day consolidation: [`strategy-state-iran/chapters/YYYY-MM/daily/`](strategy-state-iran/chapters/2026-04/daily/). Full [strategy-state-iran/README.md](strategy-state-iran/README.md).

---

## Shared logical page across experts

When the same analysis is **duplicated** into multiple expert **thread** files (same **`<expert_id>-thread-YYYY-MM.md`** per expert when using monthly thread files), keep **`id=`**, **`date=`**, and **`watch=`** **identical**. Set **`Also in:`** to the peer **`expert_id`**s. **Chronicle** may duplicate shared verbatim where intended; **Reflection** should reflect **that file’s voice** — same thesis object, **different operator read**, not copy-pasted identical analysis across experts unless you intend reuse.

---

## Machine checks (`validate_strategy_pages.py`)

[`scripts/validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) enforces the following (mirror of the script; extend the script first if you want new rules):

1. **Fences:** Every `<!-- strategy-page:start … -->` has a matching `<!-- strategy-page:end -->` in the **human layer** of the expert **thread** file (above `<!-- strategy-expert-thread:start -->`).
2. **Start tag shape:** The opener must carry **`id="…"`**, **`date="…"`**, **`watch="…"`** (empty **`watch=""`** is valid). Parsed by [`strategy_page_reader.py`](../../../../scripts/strategy_page_reader.py).
3. **Prose vs appendix (optional `--strict-prose`):** With **`--strict-prose`**, words **before** the first **`### Appendix`** heading must be **≥ `--min-prose-ratio`** (default **0.90**) of **all** words in the page inner. If there is **no** appendix heading, the **entire** block counts as prose for that ratio. So: put machinery in the appendix when you use one; otherwise keep the page lean so the ratio stays meaningful if you run strict mode.
4. **No other structural checks** in this script (no regex for mandatory `### Chronicle` — the **required scaffold** is policy in **this** template and weave discipline).

**Commands (repo root):**

```bash
python3 scripts/validate_strategy_pages.py
python3 scripts/validate_strategy_pages.py --strict-prose
python3 scripts/validate_strategy_pages.py --strict-prose --min-prose-ratio 0.90
```

---

## Scaffold (paste and replace placeholders)

```markdown
<!-- strategy-page:start id="<kebab-id>" date="YYYY-MM-DD" watch="<optional-watch-slug>" -->
### Page: <human title>

**Date:** YYYY-MM-DD
**Watch:** <optional>
**Also in:** <expert_id, expert_id>   <!-- peers with the same logical page; omit if single expert -->

### Chronicle

<!-- Full verbatim capture (lightly cleaned / formatted). Not a summary. -->

### Reflection

<!-- Operator analysis — may be stubbed until later. Grammatical prose when filled in. -->

### Foresight

<!-- Operator analysis — falsifiers, resume lines, honest doubt; stubs OK initially. -->

---

### Appendix

<!-- Optional. Paste-ready one-liners, thread: / verify: / batch-analysis tails, bare URLs, repo paths. Omit this whole section when there is no machinery. -->
<!-- strategy-page:end -->
```

**Rules:** When **`### Appendix`** is present, keep **machinery** (URLs, `thread:`, `verify:`, path dumps) **in that section only** — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *EOD compose — page-shape menu* and § *Same-day iteration* under *Compose choice and section weighting*.

**Legacy:** Standalone files under `chapters/…/knots/` were retired; old content lives in git history. Deprecated mirror: [strategy-notebook-knot-template.md](strategy-notebook-knot-template.md).
