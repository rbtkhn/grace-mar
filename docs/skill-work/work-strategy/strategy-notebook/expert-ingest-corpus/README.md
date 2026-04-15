# Deprecated folder — `expert-ingest-corpus/`

Per-expert rolling ingests now live in the parent directory as **`strategy-expert-<expert_id>.md`** (same level as [strategy-commentator-threads.md](../strategy-commentator-threads.md)).

- **Rebuild:** `python3 scripts/strategy_expert_corpus.py` (writes only the marked **Rolling ingest** block; **Seed** sections are preserved).
- **Index:** [strategy-commentator-threads.md](../strategy-commentator-threads.md) — overview in [README.md](../README.md).

**Lectures and essays (Predictive History):** For **LIB-0149** primary artifacts, **video lectures** (`lectures/*.md` and related rows in `metadata/sources.yaml`) and **Substack essays** (`substack/essays/*.md`, `series: essays`) are **the same class of source** for strategy-layer indexing: both use `lecture_path` in the registry, both count as Jiang-authored PH text once ingested and curated per work-jiang status. Do **not** treat essays as a second-tier ingest for expert-thread or stub automation. Canonical policy: [work-jiang README](../../../../../research/external/work-jiang/README.md#lectures-and-essays-equal-ph-primary-artifacts).

**Not** canonical Record truth; **WORK** notebook hygiene only.
