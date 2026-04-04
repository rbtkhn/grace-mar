# Tucker Carlson — curated transcript book (operator)

**Purpose:** **Highly curated** index of Tucker Carlson monologues / episodes that feed **work-strategy** and **work-politics** analysis. **Not** a comprehensive channel mirror (contrast [predictive-history](../predictive-history/README.md)).

**Assembled volume:** Committed snapshot copies of selected transcripts live in **[tucker-carlson-book](../tucker-carlson-book/README.md)** (table of contents: [INDEX.md](../tucker-carlson-book/INDEX.md)).

**Not** companion Record or Voice knowledge until anything is merged through **RECURSION-GATE** per [AGENTS.md](../../../../AGENTS.md).

---

## Layout

| Artifact | Role |
|----------|------|
| [CURATED-INDEX.md](CURATED-INDEX.md) | **Working spine** of the book — one row per **selected** video: id, title, URL, why it matters, link to **processed** transcript. |
| `transcripts/` (optional) | **Raw** `.txt` from ASR / yt-dlp — **gitignored**; local audit only. Curated bodies live under [work-strategy/transcripts](../../work-strategy/transcripts/). |

---

## Pipeline

1. **Select** — Add or update a row in **CURATED-INDEX.md** (editorial line: why this episode is in the book).
2. **Process** — Create **`research/external/work-strategy/transcripts/<slug>.md`** per [work-strategy transcripts README](../../work-strategy/transcripts/README.md): header, Perceiver ≤200 words, optional strategy hooks, cleaned body.
3. **Link** — Point the index row at that `*.md` path.
4. **Git** — Commit index + processed transcript per [Commit policy (ingest → git)](../../work-strategy/transcripts/README.md#commit-policy-ingest--git).

Optional bulk caption pull for **one** video: reuse `scripts/fetch_youtube_channel_transcripts.py` with `--input` listing a single watch URL and `--output-dir` here if you want raw `.txt` under `transcripts/` (still gitignored).

---

## Guardrails

- Opinion + narrative; triangulate claims with **primary** or **cited news** before ship-facing copy — see [external-tech-scan.md](../../../../docs/skill-work/work-strategy/external-tech-scan.md).
- **work-politics** drafts still need sources and gate policy.

---

## See also

- [tucker-carlson-book/](../tucker-carlson-book/) — **operator book** (curated transcripts next to predictive-history).
- [work-strategy/transcripts/](../../work-strategy/transcripts/) — canonical **processed** transcript location.
- [analyst-corpus INDEX](../../work-strategy/analyst-corpus/INDEX.md) — optional registry row if Carlson is tracked as an analyst source.
