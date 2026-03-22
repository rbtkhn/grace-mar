# Jiang ideas — influence over time (operator tracking)

**Purpose:** Build a **repeatable, evidence-style trail** of how **public engagement** with Jiang’s material on a given surface (here: **@PredictiveHistory** videos) **changes over time**. This is **operator research** for the book/site lane — **not** Voice knowledge until merged through the gate.

**What we are *not* claiming:** “Influence” here means **observable proxies** (counts, growth rates), not proof of causal impact on policy or belief. Qualitative signals (press, citations, comment themes) can be added **manually** in `notes/`.

---

## Metrics (quantitative)

Each snapshot run records, per video (when available from `yt-dlp`):

| Field | Meaning |
|-------|---------|
| `view_count` | Reported play/views |
| `like_count` | Likes |
| `comment_count` | Comment thread size (not content) |
| `channel_follower_count` | Channel subscribers at snapshot time |
| `upload_date` | YouTube upload date (YYYYMMDD) |

**Cadence (suggested):** Monthly for a **priority list** of videos (e.g. Geo-Strategy series + Game Theory cluster); quarterly **channel spot-check**. Weekly only if you are actively watching a news-driven spike.

**Artifacts:**

- **`snapshots/video-metrics.jsonl`** — one JSON object per line per run; **append-only**; git tracks history.
- Optional: export charts from JSONL in a spreadsheet or notebook outside the repo.

---

## Metrics (qualitative, manual)

Use `notes/YYYY-MM-influence.md` (create when needed) for:

- Media mentions, interviews, reposts by identifiable accounts  
- Recurring **comment themes** (if you sample comments — do not paste large copyrighted text into the repo without a clear fair-use / research rationale)  
- Your own **hypotheses** about *why* a metric moved (election cycle, war news, algorithm, etc.) — label as **hypothesis**.

---

## How to record a snapshot

From repo root:

```bash
python3 scripts/snapshot_youtube_video_metrics.py \
  --video-id lkKrZq4YdqY \
  --jsonl research/external/work-jiang/influence-tracking/snapshots/video-metrics.jsonl
```

Multiple URLs or IDs:

```bash
python3 scripts/snapshot_youtube_video_metrics.py \
  --video-id lkKrZq4YdqY xEEpOxqdU5E \
  --jsonl research/external/work-jiang/influence-tracking/snapshots/video-metrics.jsonl
```

Requires **`yt-dlp`** on PATH (same stack as channel transcript tooling).

---

## Ethics & limits

- **YouTube ToS / rate limits:** Do not hammer the API; keep modest batch sizes and spacing.  
- **Privacy:** Snapshots are **aggregate**; do not store commenter PII in git.  
- **Interpretation:** Rising views after a geopolitical crisis reflects **attention**, not necessarily agreement with every claim in a lecture.

---

## CIV-MEM lens

Engagement metrics measure **attention**, not wisdom. Through the [CIV-MEM lattice](../CIV-MEM-LENS.md), ask whether spikes align with **condition** shifts (crisis, election) or **seam** visibility (alliance splits) — still descriptive, not proof of claim accuracy.

## Related

- [Prediction tracking](../prediction-tracking/README.md) — **forecast accuracy** (separate from attention metrics)  
- [Divergence tracking](../divergence-tracking/README.md) — **vs named mainstream** (orthogonal to views/likes)  
- [work-jiang.md](../../../users/grace-mar/work-jiang.md) — project purpose  
- [CHANNEL-VIDEO-INDEX.md](../../youtube-channels/predictive-history/CHANNEL-VIDEO-INDEX.md) — full video list for choosing IDs  
- [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md) — transcript + analysis workflow  
