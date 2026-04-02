# Prep — Interviews #12: Jay Shapiro × Jiang (truth, myth, personal path)

**Operator lane — work-jiang.** Not Record. Full ASR text was supplied in the **2026-04-02** operator session (Cursor); keep a local copy until the curated lecture is filled.

## Canonical YouTube metadata (fill before registry is “green”)

| Field | Value |
|--------|--------|
| **Title (platform)** | Professor Jiang on His Painful Personal Path \| Truth and Myth \| A Search for Reality \| Internet Fame |
| **Host** | Jay Shapiro (intro references “Lummi Podcast” / long-form monologue + dialogue) |
| **Guest** | Jiang Xueqin (“Professor Xiang” online) |
| **`video_id` (11 chars)** | `oErKnj_uyPA` |
| **Upload date (YYYY-MM-DD)** | `2026-04-01` (yt-dlp `upload_date` 20260401) |
| **Canonical URL** | [https://www.youtube.com/watch?v=oErKnj_uyPA](https://www.youtube.com/watch?v=oErKnj_uyPA) |

## Content / governance notes (for curation)

- **Sensitive threads:** Holocaust historiography and rhetoric (including clips-host framing), Middle East / Israel–Palestine, eschatology, secret-society and “transnational elite” speculation, 9/11 skepticism, Epstein, Kabbalah, Masada / Dead Sea Scrolls (host afterword).
- **Divergence / mainstream:** Several historical and archaeological claims are contested; Volume VI default is **divergence box** per `CHAPTER-DIVERGENCE-BOX.md` — flag claims, name **whose** mainstream, avoid presenting speculation as settled fact.
- **Naming:** Keep **Jiang Xueqin** as speaker name in curated dialogue; “Professor Xiang” is online moniker (explained in interview).

## Ingest checklist (aligned with `WORKFLOW-transcripts.md`)

1. ~~Confirm **`video_id`** and **upload date**~~ — done: `oErKnj_uyPA`, `2026-04-01` (see lecture header + `sources.yaml`).
2. **Captions pulled:** bucket `research/external/youtube-channels/vi-12-j-shapiro/`. Verbatim → heuristic speaker-labeled `## Full transcript` via `scripts/work_jiang/emit_interview_dialogue_from_verbatim.py` (verify labels vs audio). Diff recipe: [intake/DIFF-vi-12-caption-vs-paste.md](DIFF-vi-12-caption-vs-paste.md).
3. Run `python3 scripts/work_jiang/build_source_registry.py` (refreshes `vi-12` row).
4. When memo is substantive, run `python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write` on the analysis file (after front matter exists).
5. ~~Rename analysis memo~~ — done: `analysis/oErKnj_uyPA-interviews-12-analysis.md`.
6. `python3 scripts/work_jiang/validate_work_jiang.py` (and evidence-pack / render scripts if you extend packs to `vi-ch12`).

## Topic spine (for “At a glance” / analysis — not a transcript)

- Biography: village birth 1976, immigration Canada, bullying / stutter, Yale BA English, disillusionment, China since ~1999, education reform, pivot to geopolitics videos / Asimov–Foundation frame.
- “Professor” label: high school great-books teacher; internet moniker.
- Prediction self-assessment: strong on broad contours, weak on timelines / VP pick etc.
- Secret societies / eschatology: Freemasonry (e.g. Pike, *Morals and Dogma*), Jacob Frank, Newton–alchemy–prophecy thread; framed as thought experiment vs. academic paper.
- Holocaust discussion: Jiang’s “no direct evidence I could find” phrasing vs. host’s pushback (records, camps, survivors); mythology vs. truth; Masada narrative and national myth (host); Dead Sea Scrolls convenience narrative (host afterword).
- Truth / consequences: UN Afghanistan anecdote (avian flu reporting), personal ethics, marriage; host on mythmakers, polarization, “question everything.”
- Closing: bureaucracy, speech law (Canada), hope / “spiritual awakening.”
