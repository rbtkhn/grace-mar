# Strategy expert - `alkorshid`
<!-- word_count: 310 -->

WORK only; not Record.

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) - **`alkorshid`** lane.

---

## Identity

| Field | Value |
|-------|-------|
| **Name** | Nima Alkorshid |
| **expert_id** | `alkorshid` |
| **Role** | Dialogue Works host / interviewer for long-form geopolitical dialogue; use `thread:alkorshid` alongside `thread:<guest>` on shared episodes so inbox triage and raw-input thread lists mirror both sides. |
| **Default grep tags** | `Alkorshid`, `Dialogue Works`, or `DialogueWorks` in cold |
| **Typical pairings** | x `marandi`, x `diesen`, x `mercouris`, x `davis` |
| **Notebook-use tags** | `narrate` |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) - Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint - last reviewed** | `2026-04` |

Promotion and refresh defaults: [strategy-expert-template.md section Voice fingerprint (compact)](strategy-expert-template.md#voice-fingerprint-compact).

## Convergence fingerprint

*Minimal lane - operator extends when upgraded.*

## Tension fingerprint

*Minimal lane - operator extends when upgraded.*

## Signature mechanisms

- Interview framing: sets agenda and follow-ups; distinguish host routing from guest analytic claims on the same ingest.

## Failure modes / overreads

- Guest `thread:` lines without `thread:alkorshid` on the same episode can create asymmetric raw-input mirroring; fix by adding the host line when host prompts are load-bearing.

## Archive / backfill note

- Archive discovery is useful, but it is not a completeness mandate.
- Treat Dialogue Works as a discovery index; capture only substantial episodes worth preserving.
- Automation feeds `raw-input/` only. Pages and thread files are composed later in a separate pass.
- Host prompts matter on shared episodes, so keep `thread:alkorshid` when the host framing is load-bearing.

## Automation target

1. `https://www.youtube.com/@dialogueworks01/videos` -> `thread: alkorshid`
2. Graph-first YouTube queue: [`youtube-transcript-queue.md`](../../raw-input/youtube-transcript-queue.md) and [`scripts/backfill_youtube_channel_raw_input.py`](../../../../../scripts/backfill_youtube_channel_raw_input.py)

## Published sources (operator web index)

Where Dialogue Works / host content is published (no Wikipedia). Re-verify URLs before cite-grade use.

1. https://www.youtube.com/@dialogueworks01 - Dialogue Works (YouTube)
2. https://www.podchaser.com/podcasts/dialogue-works-5841625 - podcast index (metadata)
3. https://shows.acast.com/dialogueworks - Acast show page (when cite-grade episode URLs are needed)

## Dialogue Works episode inventory

Canonical raw-input rows already present under `raw-input/`. Use these links as the fast corpus index for the lane; pin or promote watch URLs in the raw-input file itself when needed. This is the current 2026 corpus found in the notebook tree as of the last audit.

| pub_date | Episode / raw-input | Guest | Routing / note |
|----------|---------------------|-------|----------------|
| 2026-04-28 | [transcript-alkorshid-helmer-middle-east-unthinkable-iran-play-2026-04-28.md](../../raw-input/2026-04-28/transcript-alkorshid-helmer-middle-east-unthinkable-iran-play-2026-04-28.md) | Unknown / Helmer | `thread: alkorshid` (host-framing capture) |
| 2026-04-28 | [transcript-marandi-dialogue-works-trump-plan-dead-after-strike-2026-04-28.md](../../raw-input/2026-04-28/transcript-marandi-dialogue-works-trump-plan-dead-after-strike-2026-04-28.md) | Seyed Mohammad Marandi | `thread: marandi` |
| 2026-04-27 | [transcript-baud-dialogue-works-nima-2026-04-27.md](../../raw-input/2026-04-27/transcript-baud-dialogue-works-nima-2026-04-27.md) | Col. Jacques Baud | `thread: baud` |
| 2026-04-24 | [transcript-nima-freeman-israel-agenda-collapsing-2026-04-24.md](../../raw-input/2026-04-24/transcript-nima-freeman-israel-agenda-collapsing-2026-04-24.md) | Amb. Chas W. Freeman | `thread: freeman` |
| 2026-04-21 | [transcript-marandi-blockade-trump-nima-2026-04-21.md](../../raw-input/2026-04-21/transcript-marandi-blockade-trump-nima-2026-04-21.md) | Seyed Mohammad Marandi | `thread_expert: marandi` |
| 2026-04-18 | [transcript-freeman.md](../../raw-input/2026-04-18/transcript-freeman.md) | Amb. Chas W. Freeman | `thread: freeman` (stub) |
| 2026-04-18 | [transcript-marandi.md](../../raw-input/2026-04-18/transcript-marandi.md) | Seyed Mohammad Marandi | `thread: marandi` (stub) |
| 2026-04-17 | [transcript-freeman.md](../../raw-input/2026-04-17/transcript-freeman.md) | Amb. Chas W. Freeman | `thread: freeman` (stub) |
---

**Companion files:** [`transcript.md`](transcript.md) (7-day rolling verbatim) and [`thread.md`](thread.md) (distilled analytical thread).
