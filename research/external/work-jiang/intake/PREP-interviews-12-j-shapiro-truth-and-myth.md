# Prep — Interviews #12: Jay Shapiro × Jiang (truth, myth, personal path)

**Operator lane — work-jiang.** Not Record. Full ASR text was supplied in the **2026-04-02** operator session (Cursor); keep a local copy until the curated lecture is filled.

## Canonical YouTube metadata (fill before registry is “green”)

| Field | Value |
|--------|--------|
| **Title (platform)** | Professor Jiang on His Painful Personal Path \| Truth and Myth \| A Search for Reality \| Internet Fame |
| **Host** | Jay Shapiro (intro references “Lummi Podcast” / long-form monologue + dialogue) |
| **Guest** | Jiang Xueqin (“Professor Xiang” online) |
| **`video_id` (11 chars)** | *TBD — paste from URL* |
| **Upload date (YYYY-MM-DD)** | *TBD — sets registry `publication_date` and Volume VI ordering* |
| **Canonical URL** | `https://www.youtube.com/watch?v=` + `video_id` |

## Content / governance notes (for curation)

- **Sensitive threads:** Holocaust historiography and rhetoric (including clips-host framing), Middle East / Israel–Palestine, eschatology, secret-society and “transnational elite” speculation, 9/11 skepticism, Epstein, Kabbalah, Masada / Dead Sea Scrolls (host afterword).
- **Divergence / mainstream:** Several historical and archaeological claims are contested; Volume VI default is **divergence box** per `CHAPTER-DIVERGENCE-BOX.md` — flag claims, name **whose** mainstream, avoid presenting speculation as settled fact.
- **Naming:** Keep **Jiang Xueqin** as speaker name in curated dialogue; “Professor Xiang” is online moniker (explained in interview).

## Ingest checklist (aligned with `WORKFLOW-transcripts.md`)

1. Confirm **`video_id`** and **upload date**; add to `lectures/interviews-12-j-shapiro-truth-myth-personal-path.md` using the line shape used in other interviews (contains `watch?v=` + 11-char id once only).
2. Optional: pull captions into `research/external/youtube-channels/` tree per channel README; or paste **cleaned** dialogue into `## Full transcript` in the lecture file.
3. Run `python3 scripts/work_jiang/build_source_registry.py` (refreshes `vi-12` row).
4. When memo is substantive, run `python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write` on the analysis file (after front matter exists).
5. Rename analysis memo to **`{video_id}-interviews-12-analysis.md`** if you want video-id-first naming like `vi-01`–`vi-11`; update registry by re-running `build_source_registry.py`.
6. `python3 scripts/work_jiang/validate_work_jiang.py` (and evidence-pack / render scripts if you extend packs to `vi-ch12`).

## Topic spine (for “At a glance” / analysis — not a transcript)

- Biography: village birth 1976, immigration Canada, bullying / stutter, Yale BA English, disillusionment, China since ~1999, education reform, pivot to geopolitics videos / Asimov–Foundation frame.
- “Professor” label: high school great-books teacher; internet moniker.
- Prediction self-assessment: strong on broad contours, weak on timelines / VP pick etc.
- Secret societies / eschatology: Freemasonry (e.g. Pike, *Morals and Dogma*), Jacob Frank, Newton–alchemy–prophecy thread; framed as thought experiment vs. academic paper.
- Holocaust discussion: Jiang’s “no direct evidence I could find” phrasing vs. host’s pushback (records, camps, survivors); mythology vs. truth; Masada narrative and national myth (host); Dead Sea Scrolls convenience narrative (host afterword).
- Truth / consequences: UN Afghanistan anecdote (avian flu reporting), personal ethics, marriage; host on mythmakers, polarization, “question everything.”
- Closing: bureaucracy, speech law (Canada), hope / “spiritual awakening.”
