# Strategy expert — `ritter`
<!-- word_count: 416 -->

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) — **`ritter`** lane.

## Identity

| Field | Value |
|-------|-------|
| **Name** | Scott Ritter |
| **expert_id** | `ritter` |
| **Role** | U.S. **military dissent**: Hormuz **sea control**, blockade ops, Vance frame; **faith-politics** register when **Ritter** is the speaking expert |
| **Default grep tags** | `JDVance`, `IRAN`, or `Ritter` |
| **Typical pairings** | × `marandi`, × `barnes`, × `rome-invective` (split from ecumenical) |
| **Notebook-use tags** | `validate`, `authorize`, `stress-test` |

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
| `ritter` | Scott Ritter | U.S. **military dissent**: Hormuz **sea control**, blockade ops, Vance frame; **faith-politics** register when **Ritter** is the speaking expert | `JDVance`, `IRAN`, or `Ritter` | × `marandi`, × `barnes`, × `rome-invective` (split from ecumenical) |

### Quantitative metrics (illustrative — from index)

| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |
|-----------|-----|----|-----|--------------------------------------------------|
| `ritter` | 0.82 | 0.48 | 0.74 | His lane is recognizable—sea control, blockade mechanics, the military story under the headlines—so he does not drift into generic punditry as often. Operational claims need time and evidence to judge, so verdicts arrive slowly. He is often placed beside diplomats or lawyers of war in the same week’s analysis, which raises the “compares with others” score. |

### Published sources (operator web index)

Where **their** commentary is published and accessible (**no Wikipedia**). Re-verify handles and media URLs before cite-grade use outside this notebook.

1. https://x.com/RealScottRitter
2. https://scottritter.com/
3. https://scottritter.substack.com/
4. https://www.youtube.com/@therealscottritter

## Archive / backfill note

- Treat the public site, Substack, and video surfaces as discovery indexes, not completeness mandates; backfill the substantial items you want preserved and leave lighter archive-visible items out when they do not merit raw-input retention.

## Automation target

- Public X profile crawl via [`scripts/backfill_ritter_x_raw_input.py`](../../../../../scripts/backfill_ritter_x_raw_input.py) or the generic [`scripts/backfill_x_profile_raw_input.py`](../../../../../scripts/backfill_x_profile_raw_input.py) with `--profile-url https://x.com/RealScottRitter --thread ritter`; public Substack backfill via [`scripts/backfill_ritter_substack_raw_input.py`](../../../../../scripts/backfill_ritter_substack_raw_input.py) or the generic [`scripts/backfill_substack_raw_input.py`](../../../../../scripts/backfill_substack_raw_input.py) with `--hostname scottritter.substack.com --thread ritter`. Treat these archives as discovery indexes, not completeness mandates.
- Site-hosted article alias crawl via [`scripts/backfill_ritter_site_raw_input.py`](../../../../../scripts/backfill_ritter_site_raw_input.py) or the generic [`scripts/backfill_substack_raw_input.py`](../../../../../scripts/backfill_substack_raw_input.py) with `--hostname scottritter.com --thread ritter`; this hostname currently resolves into the same Substack-hosted archive, so it is an alias path, not a separate content universe.

---

**Companion files:** [`transcript.md`](transcript.md) (7-day rolling verbatim), [`thread.md`](thread.md) (analytical thread — multi-month during phased split), and [`ritter-thread-2026-01.md`](ritter-thread-2026-01.md) (January 2026 monthly chapter; canonical for that month when present).
