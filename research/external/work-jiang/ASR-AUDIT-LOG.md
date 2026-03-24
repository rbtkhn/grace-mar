# ASR audit log — work-jiang / Predictive History

**Purpose:** Cross-session traceability for **targeted** transcript verification (not full linear proofreading). Canonical rules: [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md). Operator research only; not companion Record.

---

## 1. Scope (kickoff — edit when you start a pass)

| Field | Your choice |
|-------|-------------|
| **Series** | `geo-strategy` / `civilization` / `secret-history` / `mixed` |
| **Depth** | **A** — spot-check high-signal episodes only · **B** — all in-scope episodes, **targeted signals only** (rubric table) · **C** — full read (exceptional) |
| **Session / date** | |

**Suggested first pass:** Geo-Strategy, depth **B**, after raw captions exist for those `video_id`s.

---

## 2. Preconditions (check before auditing)

- [ ] **Raw captions:** `research/external/youtube-channels/predictive-history/transcripts/{video_id}_*.txt` for episodes in scope. Fetch: [predictive-history README](../youtube-channels/predictive-history/README.md) — `scripts/fetch_youtube_channel_transcripts.py`.
- [ ] **Coverage report (optional):** from repo root, `python3 scripts/work_jiang/check_asr_audit_preconditions.py` (add `--strict` to fail CI if any in-scope lecture lacks raw).
- [ ] **Tooling sanity:** `pytest tests/test_normalize_lecture_transcript_asr.py -q`
- [ ] **Verbatim diff layer (optional):** `python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run --only-glob '<pattern>'` then `--write` — see [verbatim-transcripts/README.md](verbatim-transcripts/README.md).

---

## 3. Targeted verification (what to actually check)

Do **not** proofread entire transcripts unless depth **C** or a chapter requires it. **Do** verify when any of these apply ([ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md) § Targeted verification):

| Signal | Checked? (episode list or “all in scope”) |
|--------|-------------------------------------------|
| Proper names, non-English, book titles | |
| Numbers, dates, counts | |
| Direct attribution / pull-quotes | |
| Sensitive or high-liability lines | |

**Compare:** raw `.txt` ↔ `verbatim-transcripts/<slug>.md` (if generated) ↔ `lectures/<slug>.md` (`## Full transcript` if present) ↔ quote candidates you intend to promote to `metadata/quotes.yaml`.

**Geo-Strategy invariant:** never treat civilization-only ASR fixes as automatic for geo (e.g. “thieves” vs Thebes) — see tests and `asr_light_clean.py`.

---

## 4. Findings log (append rows)

| Date | Lecture file | Signal type | Before (short) | After / fix | Verified how (raw file, timestamp, ear) |
|------|--------------|-------------|------------------|-------------|----------------------------------------|
| | | | | | |

---

## 5. Commands reference

```bash
# Tests
pytest tests/test_normalize_lecture_transcript_asr.py -q

# Coverage (lectures with YouTube URL vs raw .txt)
python3 scripts/work_jiang/check_asr_audit_preconditions.py
python3 scripts/work_jiang/check_asr_audit_preconditions.py --only-glob 'geo-strategy-*'
python3 scripts/work_jiang/check_asr_audit_preconditions.py --strict   # exit 1 if gaps

# Verbatim layer (example: Geo-Strategy)
python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run --only-glob 'geo-strategy-*'
python3 scripts/work_jiang/sync_verbatim_transcripts.py --write --only-glob 'geo-strategy-*'
```

---

## Related

- [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) — layers and Phase B verbatim step  
- [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md) — epistemic levels and when timestamps/captions are required  
