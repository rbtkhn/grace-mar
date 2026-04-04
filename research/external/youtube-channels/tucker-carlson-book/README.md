# Tucker Carlson — operator book (curated transcripts)

**Purpose:** A **small, committed library** of **processed Tucker Carlson Network transcripts** the operator treats as one **volume**, stored **next to** [predictive-history](../predictive-history/README.md) under `research/external/youtube-channels/`.

**Not** companion Record or Voice knowledge until anything is merged through **RECURSION-GATE** per [AGENTS.md](../../../../AGENTS.md).

---

## Work-politics wiring

This book is indexed for **work-politics** as **long-form narrative ingest** (Iran, Hormuz, war powers, GOP / media framing) — not a substitute for cited news or FEC facts.

| Doc | Role |
|-----|------|
| [work-politics-sources.md](../../../../docs/skill-work/work-politics/work-politics-sources.md) | **§ Tucker Carlson Network** — when to use the book, guardrails, links to ROME-PASS exemplar and work-jiang |
| [brief-source-registry.md](../../../../docs/skill-work/work-politics/brief-source-registry.md) | Registry row points at [INDEX.md](INDEX.md) for brief refresh cadence |
| [workspace.md](../../../../docs/skill-work/work-politics/workspace.md) | Dashboard + canonical files mention **TCN** → this book |
| [iran-foreign-policy-brief.md](../../../../docs/skill-work/work-politics/iran-foreign-policy-brief.md) | Issue brief to align monologue / interview **frames** with principal-grounded messaging |

---

## Layout

| Artifact | Role |
|----------|------|
| [INDEX.md](INDEX.md) | **Table of contents** — video id, title, URL, file under `transcripts/`, notes. |
| [transcripts/](transcripts/) | **Committed copies** of each episode (plus YAML `canonical` pointer where a source-of-truth file exists elsewhere in the repo). |

---

## Relation to other paths

| Location | Role |
|----------|------|
| [tucker-carlson/](../tucker-carlson/README.md) | Curated **channel index** (working spine); link **processed** bodies. |
| [work-strategy/transcripts/](../../work-strategy/transcripts/) | Canonical **monologue digests** (e.g. `GyYy-QmxttU`). |
| [work-jiang/lectures/](../../work-jiang/lectures/) | **Interviews #11** (Tucker × Jiang) lives here as Predictive History lecture spine. |

When you **edit** a file that has a `canonical` path in its YAML front matter, consider **re-copying** into this book or editing the canonical file first, then refreshing the book copy — otherwise the two can drift.

---

## Pipeline

1. Add a row to **INDEX.md**.
2. Add or refresh **`transcripts/<video_id>-<slug>.md`** (work-strategy-style header + body where possible).
3. Optional: add a row to [tucker-carlson/CURATED-INDEX.md](../tucker-carlson/CURATED-INDEX.md) pointing at the book or canonical path.
4. Commit book + index together when the operator wants a durable snapshot.

---

## Guardrails

- Opinion, narrative, and theological claims; **verify** numbers and news lines against **primary** sources before ship-facing copy — see [external-tech-scan.md](../../../../docs/skill-work/work-strategy/external-tech-scan.md).
