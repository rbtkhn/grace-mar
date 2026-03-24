# ASR / transcript verification rubric (work-jiang)

**Purpose:** Decide when summarized or curated text is “good enough” vs when you need **verbatim** evidence from captions or listening.

This lane is operator research, not companion Record truth. Use the rubric to avoid silently treating a paraphrase or bad ASR line as a direct quotation.

---

## Three epistemic levels

1. **Summary (non-verbatim)**  
   - Intake bullets, “at a glance,” or compressed lecture arc.  
   - **Safe for:** internal argument maps, backlog priorities, “what the lecture is about.”  
   - **Not safe for:** book pull-quotes, footnotes, or “Professor Jiang said X” without a check.

2. **Curated lecture body**  
   - Edited markdown in `lectures/*.md` (may include long transcript-like text or ASR-normalized blocks).  
   - **Safe for:** drafting and quote **candidates** (`metadata/quote-candidates*.yaml`).  
   - Treat as **ASR-uncertain** until you run a targeted check (below).

3. **Verified line**  
   - Matched to **raw caption file** under `research/external/youtube-channels/predictive-history/transcripts/` **or** to the recording at a **timestamp**.  
   - Optional markers in text: `[verify: MM:SS]`, `[unclear]`, or a short note `verified_against: transcript YYYY-MM-DD`.  
   - **Safe for:** promoting a line into `metadata/quotes.yaml` with `verification` / `status` fields documented in that file.

`scripts/work_jiang/bootstrap_quotes_from_candidates.py` already notes: auto rows are ASR; verify before scholarly citation.

---

## Targeted verification (high yield)

Do **not** proofread two hours of captions end-to-end unless the chapter depends on it. **Do** verify when any of these apply:

| Signal | Why |
|--------|-----|
| Proper names, non-English terms, book titles | ASR corruption is common |
| Numbers, dates, vote counts, “X trillion” | High error + high liability |
| Direct attribution (“X said…”) | Needs exact wording |
| Pull-quote / epigram for book or public copy | Must match audio or caption |
| Legally or interpersonally sensitive line | Verbatim trail required |

**Method:** Open the raw `transcripts/<video_id>_*.txt` for that episode (after fetch) or the video at the segment; fix the curated file or the quote row, and record how you verified.

---

## Operational habits

- **Paste workflow:** If the operator pastes a transcript in chat, keep a **local copy** (or re-fetch captions) so two witnesses exist: paste vs YouTube.  
- **Compact intake path:** Intake is **lossy** by design. For episodes where wording matters, either fetch raw transcripts or add a [verbatim appendix](templates/verbatim-appendix-snippet.md) to the curated lecture.  
- **Quote pipeline:** `extract_quote_candidates.py` emits **machine candidates** only. Curators promote to `quotes.yaml` after verification as needed.

---

## Related docs

- [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) — three layers (raw / curated / analysis).  
- [../youtube-channels/predictive-history/README.md](../youtube-channels/predictive-history/README.md) — fetch CLI.  
- [../youtube-channels/predictive-history/transcripts/README.md](../youtube-channels/predictive-history/transcripts/README.md) — gitignored raw cache.
