# Work-jiang — systematic transcript intake & analysis

Operator research for the Jiang book/site lane. **Not** Record truth until merged through the gate. See [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md) for project purpose.

---

## 1. What this workflow produces

For each video you care about, you want **three layers** on disk (names are conventions, not law):

| Layer | Purpose | Typical location |
|-------|---------|------------------|
| **Raw caption pull** | Machine transcript + provenance header | `research/external/youtube-channels/predictive-history/transcripts/` (often **gitignored**; see channel README) |
| **Curated lecture file** | Human-readable archive: metadata, “at a glance,” optional full ASR, **canonical YouTube URL** | `research/external/work-jiang/lectures/<slug>.md` |
| **Analysis memo** | Structured read: claims, tags, lattice crosswalk, tensions, dependencies | `research/external/work-jiang/analysis/<video_id>-<short-slug>.md` (or append sections in one rolling doc — pick one pattern and keep it) |

Keeping **raw** and **curated** separate avoids mixing YouTube caption noise with your editorial summary.

**Longitudinal influence (optional):** To track how **public engagement** with Jiang material changes over time (views, likes, comment counts, channel subscribers), use [influence-tracking/README.md](influence-tracking/README.md) and `scripts/snapshot_youtube_video_metrics.py` → append-only `influence-tracking/snapshots/video-metrics.jsonl`. This measures **attention proxies**, not “impact” in a causal sense.

**Prediction accuracy (optional):** Log falsifiable claims in [prediction-tracking/registry/predictions.jsonl](prediction-tracking/registry/predictions.jsonl) with evaluation windows and evidence URLs; see [prediction-tracking/README.md](prediction-tracking/README.md). **Separate** from views/likes — a viral video can host a wrong forecast.

**Mainstream divergence (optional):** When a lecture asserts something **contested** vs a named consensus (historiography, IR, theology), add a row to [divergence-tracking/registry/divergences.jsonl](divergence-tracking/registry/divergences.jsonl); see [divergence-tracking/README.md](divergence-tracking/README.md). Always name **whose** mainstream.

---

## 2. Phase A — Acquire & register

1. **Refresh channel index (optional but recommended)**  
   From repo root (deps: `pip install -e ".[youtube-research]"` or `yt-dlp` + `youtube-transcript-api`):

   ```bash
   python3 scripts/fetch_youtube_channel_transcripts.py \
     --channel "https://www.youtube.com/@PredictiveHistory/videos" \
     --output-dir research/external/youtube-channels/predictive-history \
     --resume --sleep 0.5
   ```

   - **`--dry-run --limit 200`** — list IDs/titles without downloading (queue planning).  
   - **`--resume`** — skip videos that already have a non-trivial `.txt`.  
   - Output: `transcripts/*.txt` with header (`video_id`, `title`, `url`, `language`, `fetched_at_utc`) + `index.json` manifest.

2. **Register intent** — note in your tracker or `work-jiang.md` **WORK GOALS** / `near_term` which series or episode IDs you are processing this week (operator choice).

---

## 3. Phase B — Normalize & link

For each target video:

1. **Stable key** — use **`video_id`** (11 chars) as the join key between `index.json`, raw `.txt`, curated lecture, and analysis memo.

2. **Canonical URL** — `https://www.youtube.com/watch?v=<video_id>` unless you have a playlist-specific URL; prefer **`@PredictiveHistory`** uploads when that is the source of truth (verify title/series match; avoid unrelated fan edits).

3. **Slug** — filesystem-safe stem, e.g. `geo-strategy-01-iran-strategy-matrix-2024-04-24` or `xEEpOxqdU5E-geo-strategy-01`; include **video_id** in analysis filename if you want grep-friendly linkage.

4. **Curated lecture file (when needed)** — If captions alone are insufficient (e.g. classroom Q&A, longer ASR), add or update `lectures/<slug>.md` with:
   - Speaker, audience, date (if stated), topic, **canonical Source** line  
   - Short **At a glance** before dumping full transcript  
   - **Tags** line for retrieval

---

## 4. Phase C — First pass (close read)

Read the raw pull (or curated transcript) once **without** structuring:

- **Genre** — e.g. Geo-Strategy, Game Theory, Civilization strand.  
- **Audience** — who is being addressed (affects rhetoric).  
- **Moves** — what the lecture *does* (define terms, historical analogy, prediction, normative claim).

Note **exposition** (what the philosophy asserts or teaches) vs **analysis** (predictions, comparisons, stress tests) — work-jiang keeps these separable for the eventual book/site.

---

## 5. Phase D — Structured extraction

Fill the **analysis memo** (see appendix template) with:

- **Thesis / aim** — one paragraph.  
- **Defined terms** — glossary bullets.  
- **Claims** — numbered; tag each as observation / interpretation / forecast where helpful.  
- **References** — events, books, wars, other lectures (internal cross-links by slug or video_id).  
- **Open questions** — what is left ambiguous or deferred to “future class.”

---

## 6. Phase E — Analytic passes (repeatable)

Run any subset per video; order is flexible.

1. **Internal consistency** — Do definitions stay stable? Do later claims depend on earlier ones?  
2. **CIV-MEM lattice** — Follow [CIV-MEM-LENS.md](CIV-MEM-LENS.md): **conditions**, **institutions**, **seams**, **continuity/memory**, **time structure**, **decline/stress**, then **multi-perspective**. [work-civ-mem](../../../docs/skill-work/work-civ-mem/README.md) / [`docs/civilization-memory/`](../../../docs/civilization-memory/README.md) are **retrieval surfaces** for analogy and vocabulary — not automatic truth; tag `{CMC: path}` if corpus text enters a shippable draft ([civ-mem-draft-protocol](../../../docs/skill-work/work-politics/civ-mem-draft-protocol.md)).  
3. **Current-events grounding (optional)** — One short paragraph: where abstract claims meet a concrete episode; flag **ship** vs **draft** if anything could become public copy.  
4. **Book/site placement** — Outline hook: which chapter or site section this feeds; duplicates or contradictions vs other memos.

---

## 7. Phase F — Quality & provenance checks

Before treating a memo as “done for this sprint”:

- [ ] `video_id` and **canonical URL** match `index.json` / YouTube.  
- [ ] Raw pull path or fetch date noted if someone must reproduce.  
- [ ] Exposition vs analysis clearly separated where mixed.  
- [ ] No companion Record merge — operator lane only unless you run the gated pipeline.

---

## 8. Phase G — Queue discipline

- **Priority** — e.g. by series (Geo-Strategy first), or by dependency (earlier numbered lectures before updates).  
- **Batch size** — e.g. one analysis memo per session, or one *series* per week; avoid an unbounded backlog without a numbered queue.  
- **Stale pulls** — Re-run fetch with `--resume` after long gaps; captions can change.

---

## Appendix A — Analysis memo template (copy into `analysis/<video_id>-<slug>.md`)

```markdown
# Analysis — [short title]

- **video_id:**  
- **canonical_url:**  
- **series / episode:**  
- **raw_transcript:** path or `index.json` reference  
- **analyzed_at:** YYYY-MM-DD (operator)

## Thesis / aim

## Defined terms

## Claims (numbered)

1. …

## Internal tensions (if any)

## CIV-MEM lattice (full)

| Slot | Notes |
|------|--------|
| Conditions | |
| Institutions | |
| Seams / friction | |
| Continuity / memory | |
| Time structure | |
| Decline / stress | |
| Multi-perspective | |

## Cross-refs (other lectures / memos)

## Current-events tie-in (optional draft)

## Book/site outline hook

## Follow-ups
```

---

## Appendix B — Command quick reference

| Goal | Command |
|------|---------|
| List channel videos | `python3 scripts/fetch_youtube_channel_transcripts.py --dry-run --limit 200` |
| Pull transcripts | `python3 scripts/fetch_youtube_channel_transcripts.py --resume --output-dir research/external/youtube-channels/predictive-history` |
| Manifest | `research/external/youtube-channels/predictive-history/index.json` |

---

## Appendix C — Related docs

- [work-jiang README](README.md) — research tree  
- [Predictive History channel README](../youtube-channels/predictive-history/README.md) — fetch details, gitignore behavior  
- [work-civ-mem README](../../../docs/skill-work/work-civ-mem/README.md) — lattice as external reference, not automatic Record  
