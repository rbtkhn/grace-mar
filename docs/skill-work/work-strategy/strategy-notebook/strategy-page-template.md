# Strategy page template — thread-embedded (`strategy-page`)

WORK only; not Record.

**Where:** Add a `<!-- strategy-page:start … -->` … `<!-- strategy-page:end -->` block under the correct **`## YYYY-MM`** in **`experts/<expert_id>/thread.md`**. For the same logical analysis across experts, **duplicate** the block into each expert’s file with the same **`id=`** and **`date=`** (see [watches/README.md](watches/README.md)).

**Required prose scaffold:** **`### Signal`**, **`### Judgment`**, and **`### Open`** — **grammatical prose only** in each (facts framing, judgment, falsifiers / resume / doubt). This is the contract for a woven page; list dumps and machinery belong elsewhere (appendix when used, or overflow — see below).

**Optional `### Technical appendix`:** Omit when the page is short and has **no** paste-ready machinery (URLs, `thread:`, `verify:`, `batch-analysis` tails, bare paths). When you **do** need that material, add **`### Technical appendix`** and keep **machinery only** there — see **Rules** and **Machine checks** below. **Do not** rename this heading: [`validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) splits prose vs appendix on the exact string **`### Technical appendix`** (match is case-insensitive in the script). “Optional” means **omit the section entirely**, not use a different title.

**Length:** Target **500–1000 words** across **Signal + Judgment + Open** only. Words in **`### Technical appendix`** (when present) are **outside** that prose budget. Overflow → `days.md`, a second page **`id`**, or **Links** in the notebook sense.

**Cadence:** Prefer **one end-of-day page session** per day—do not create or extend `strategy-page` blocks continuously during the day; daytime capture stays in [daily-strategy-inbox.md](daily-strategy-inbox.md).

**strategy-state-iran (voices):** Under each **`## YYYY-MM`**, add **`### Month ledger (YYYY-MM)`** once per month (ingest span, seam targets, open hooks) — **month-gate** accumulation, not a daily ledger. See [strategy-state-iran/README.md](strategy-state-iran/README.md). Per-day consolidation lives in [`strategy-state-iran/chapters/YYYY-MM/daily/`](strategy-state-iran/chapters/2026-04/daily/).

---

## Shared logical page across experts

When the same analysis is **duplicated** into multiple **`experts/<expert_id>/thread.md`** files, keep **`id=`**, **`date=`**, and **`watch=`** **identical**. Set **`Also in:`** to the peer **`expert_id`**s. **Judgment** (and, where it helps, a line or two of **Signal** framing) should reflect **that file’s voice** — same thesis object, **different perspective**, not copy-pasted identical prose across experts unless you intend verbatim reuse.

---

## Machine checks (`validate_strategy_pages.py`)

[`scripts/validate_strategy_pages.py`](../../../../scripts/validate_strategy_pages.py) enforces the following (mirror of the script; extend the script first if you want new rules):

1. **Fences:** Every `<!-- strategy-page:start … -->` has a matching `<!-- strategy-page:end -->` in the **human layer** of `thread.md` (above `<!-- strategy-expert-thread:start -->`).
2. **Start tag shape:** The opener must carry **`id="…"`**, **`date="…"`**, **`watch="…"`** (empty **`watch=""`** is valid). Parsed by [`strategy_page_reader.py`](../../../../scripts/strategy_page_reader.py).
3. **Prose vs appendix (optional `--strict-prose`):** With **`--strict-prose`**, words **before** the first **`### Technical appendix`** heading must be **≥ `--min-prose-ratio`** (default **0.90**) of **all** words in the page inner. If there is **no** appendix heading, the **entire** block counts as prose for that ratio. So: put machinery in the appendix when you use one; otherwise keep the page lean so the ratio stays meaningful if you run strict mode.
4. **No other structural checks** in this script (no regex for mandatory `### Signal` — the **required scaffold** is policy in **this** template and weave discipline).

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

### Signal

<!-- Grammatical prose only. -->

### Judgment

<!-- Grammatical prose only. -->

### Open

<!-- Falsifiers, resume lines, honest doubt — still prose. -->

---

### Technical appendix

<!-- Optional. Paste-ready one-liners, thread: / verify: / batch-analysis tails, bare URLs, repo paths. Omit this whole section when there is no machinery. -->
<!-- strategy-page:end -->
```

**Rules:** When **`### Technical appendix`** is present, keep **machinery** (URLs, `thread:`, `verify:`, path dumps) **in that section only** — see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *EOD compose — page-shape menu* and § *Same-day iteration* under *Compose choice and section weighting*.

**Legacy:** Standalone files under `chapters/…/knots/` were retired; old content lives in git history. Deprecated mirror: [strategy-notebook-knot-template.md](strategy-notebook-knot-template.md).
