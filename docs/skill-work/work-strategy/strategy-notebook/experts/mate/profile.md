# Strategy expert — `mate`
<!-- word_count: 407 -->

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) — **`mate`** lane.

## Identity

| Field | Value |
|-------|-------|
| **Name** | Aaron Maté (`@aaronjmate`) |
| **expert_id** | `mate` |
| **Role** | **Grayzone** / **investigative** lane: **media ownership**, **corporate skin**, and **propaganda** framing; **Israel/Palestine** vocabulary (**colonization** thesis); **CBS** / **billionaire** / outlet **lineage** claims — **tier verify** (filings, corporate docs) before **Links-grade** |
| **Default grep tags** | `Mate`, `Maté`, `Grayzone`, or `aaronjmate` in cold |
| **Typical pairings** | × `blumenthal`, × `parsi`, × `mercouris`, × `marandi` |
| **Notebook-use tags** | `narrate` |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) — Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint — last reviewed** | `2026-04` |

Promotion and refresh defaults: [strategy-expert-template.md § Voice fingerprint (compact)](strategy-expert-template.md#voice-fingerprint-compact).

## Convergence fingerprint

*Seed profile — operator extends when this lane is upgraded to a full cognitive profile.*

## Tension fingerprint

*Seed profile — operator extends when upgraded.*

## Signature mechanisms

*Seed profile — operator extends when upgraded.*

## Failure modes / overreads

*Seed profile — operator extends when upgraded.*

## Active weave cues

*Seed profile — operator extends when upgraded.*

## Seed (index mirror — operator may extend)

The block below **Rolling ingest** is replaced on each `strategy_thread.py` / `strategy_expert_corpus.py` run; edit this **Seed** section freely.

### Commentator row (from index)

| expert_id | Name | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |
|-----------|--------|-----------------|------------------|-----------------------------------|
| `mate` | Aaron Maté (`@aaronjmate`) | **Grayzone** / **investigative** lane: **media ownership**, **corporate skin**, and **propaganda** framing; **Israel/Palestine** vocabulary (**colonization** thesis); **CBS** / **billionaire** / outlet **lineage** claims — **tier verify** (filings, corporate docs) before **Links-grade** | `Mate`, `Maté`, `Grayzone`, or `aaronjmate` in cold | × `blumenthal`, × `parsi`, × `mercouris`, × `marandi` |

### Quantitative metrics (illustrative — from index)

| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |
|-----------|-----|----|-----|--------------------------------------------------|
| `mate` | 0.75 | 0.34 | 0.64 | Media-structure and ownership critiques are a steady lane—outlet naming and corporate parentage need primary documents to close. Often read beside the same Grayzone-adjacent week as Blumenthal but keeps a distinct thread id for routing. |

### Published sources (operator web index)

Where **their** commentary is published and accessible (**no Wikipedia**). Re-verify handles and media URLs before cite-grade use outside this notebook.

1. https://x.com/aaronjmate
2. https://thegrayzone.com/author/mate/
3. https://thegrayzone.com/pushback/

---

**Companion files:** [`strategy-expert-mate-transcript.md`](strategy-expert-mate-transcript.md) (7-day rolling verbatim) and [`strategy-expert-mate-thread.md`](strategy-expert-mate-thread.md) (distilled analytical thread).

## Archive / backfill note

- Treat the public author/archive pages as discovery indexes, not completeness mandates; backfill the substantial posts you want preserved and leave light or repetitive archive-visible items out when that is the better editorial call.

## Automation target

- Public Grayzone author-page crawl via [`scripts/backfill_mate_grayzone_raw_input.py`](../../../../../scripts/backfill_mate_grayzone_raw_input.py) or the generic [`scripts/backfill_author_page_raw_input.py`](../../../../../scripts/backfill_author_page_raw_input.py) with `--author-url https://thegrayzone.com/author/aaron-mate/ --domain thegrayzone.com --path-shape date-slug --publication thegrayzone.com --thread mate`.
- Public X profile crawl via [`scripts/backfill_mate_x_raw_input.py`](../../../../../scripts/backfill_mate_x_raw_input.py) or the generic [`scripts/backfill_x_profile_raw_input.py`](../../../../../scripts/backfill_x_profile_raw_input.py) with `--profile-url https://x.com/aaronjmate --thread mate`.
