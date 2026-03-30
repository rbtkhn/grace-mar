# work-strategy — transcript ingest (operator)

**Purpose:** Hold **raw or lightly curated transcripts** that feed the **work-strategy** pipeline ([current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md) step 1 **Perceiver**, [persuasive-content-pipeline.md](../../../../docs/skill-work/work-strategy/persuasive-content-pipeline.md), [LEARN_MODE_RULES.md](../../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md)), **separate from** the companion **Record** and **separate from** [work-jiang](../../../work-jiang/README.md) lecture corpora.

**Not Voice knowledge** until anything is merged through **RECURSION-GATE** per [AGENTS.md](../../../../AGENTS.md).

---

## Layout

| Pattern | Use |
|---------|-----|
| **Curated digest** | `*.md` in this folder — YAML or front matter optional; body = transcript excerpt + **source URL**, **date**, **operator summary** (see [work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md](../../work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md) for shape). **Commit** when the digest is the durable artifact. |
| **Raw captions** | `*.txt` from YouTube/podcast ASR — may stay **local-only** (gitignore) if large; prefer provenance header (`# url: …`, `# fetched_at_utc: …`). |

---

## How to ingest

1. **Manual paste** — Drop text into a new `.md` or `.txt`; add source line at top.
2. **YouTube (same tooling as other lanes)** — For **Predictive History** channel videos, use [youtube-channels/predictive-history/README.md](../../youtube-channels/predictive-history/README.md) and `scripts/fetch_youtube_channel_transcripts.py` (raw usually under `youtube-channels/predictive-history/transcripts/`, often gitignored). For **work-strategy-only** sources (e.g. GTC panels, strategy podcasts), either copy the fetched `.txt` here with a note **or** add a channel folder under `research/external/youtube-channels/` following that README’s pattern.
3. **Downstream** — Run **Perceiver** (neutral fact summary ≤200 words) from the file; then [current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md) (energy hook if relevant → lenses → synthesis). Log outcomes in **STRATEGY.md** §III / §IV **WS–MEM** when you want execution memory.

---

## Guardrails

- Treat long-form media as **narrative + opinion** unless triangulated with **primary** or **cited news** — see [external-tech-scan.md](../../../../docs/skill-work/work-strategy/external-tech-scan.md).
- **work-politics** ship copy still needs **sources** and gate policy; transcripts here are **upstream** research.

---

## See also

- [common-inputs.md](../../../../docs/skill-work/work-strategy/common-inputs.md) — shared inputs with work-politics.
- [work-strategy README](../../../../docs/skill-work/work-strategy/README.md) — territory index.
