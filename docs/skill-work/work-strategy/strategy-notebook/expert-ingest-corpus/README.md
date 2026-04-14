# Expert ingest corpus (rolling window)

One Markdown file per indexed **`expert_id`** in [strategy-commentator-threads.md](../strategy-commentator-threads.md).

- **Contents:** Verbatim inbox lines that include **`thread:<expert_id>`** in a paste-ready bullet or backtick line, grouped by **`## YYYY-MM-DD`**. Dates are inferred from inbox markers (`Accumulator for`, `brief-handoff-bundle`, `Prior scratch`, `Folded`, `Prep`, `Retained reference`, etc.).
- **Retention:** Last **7** calendar days by default; each rebuild **drops** daily sections older than the window (yesterday’s oldest day falls off as new days append).
- **Rebuild:** From repo root:

  ```bash
  python3 scripts/strategy_expert_corpus.py
  ```

  Options: `--inbox PATH`, `--out DIR`, `--days N`, `--today YYYY-MM-DD` (tests), `--dry-run`.

**Purpose:** Richer **batch-analysis**, drift, and accuracy work without re-grepping the whole inbox — each voice’s recent **verbatim** capture lines sit in one place.

**Lectures and essays (Predictive History):** For **LIB-0149** primary artifacts, **video lectures** (`lectures/*.md` and related rows in `metadata/sources.yaml`) and **Substack essays** (`substack/essays/*.md`, `series: essays`) are **the same class of source** for strategy-layer indexing: both use `lecture_path` in the registry, both count as Jiang-authored PH text once ingested and curated per work-jiang status. Do **not** treat essays as a second-tier ingest for expert-thread or stub automation. Canonical policy in corpus: [work-jiang README](../../../../../research/external/work-jiang/README.md#lectures-and-essays-equal-ph-primary-artifacts).

**Not** canonical Record truth; **WORK** notebook hygiene only.
