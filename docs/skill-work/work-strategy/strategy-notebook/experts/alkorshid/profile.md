# Strategy expert - `alkorshid`
<!-- word_count: ~700 -->

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

Metadata-only index from the public YouTube crawl starting at `2026-01-01`. Transcript bodies are not backfilled in this pass. `needs capture` means the episode is visible on the channel but not yet mirrored in `raw-input/`.

| pub_date | Title | Guest | URL | Routing / note | raw-input |
|----------|-------|-------|-----|----------------|-----------|
| 2026-01-03 | Max Blumenthal: This Is the Utmost Failure: Trump Creates Absolute Chaos - Iran & Venezuela | Max Blumenthal | [https://www.youtube.com/watch?v=aeT3jwwUE6A](https://www.youtube.com/watch?v=aeT3jwwUE6A) | host-hub | mirrored |
| 2026-01-04 | Alastair Crooke: The Hidden Signal: How One Answer Could Ignite the Middle East | Alastair Crooke | [https://www.youtube.com/watch?v=5JVKloRggyo](https://www.youtube.com/watch?v=5JVKloRggyo) | thread: crooke | mirrored |
| 2026-01-09 | Col. Larry Wilkerson: 21st Century Peril: How America’s Power Plays Risk Everything | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=8DpLyv_7IiI](https://www.youtube.com/watch?v=8DpLyv_7IiI) | thread: johnson | mirrored |
| 2026-01-10 | Scott Ritter: Russia All in to Confront the Worst-Case Scenario | Scott Ritter | [https://www.youtube.com/watch?v=DuS17MeaWgE](https://www.youtube.com/watch?v=DuS17MeaWgE) | thread: ritter | mirrored |
| 2026-01-11 | Pepe Escobar: Trump, Greenland, NATO Collapse & Global Power Shock | Pepe Escobar | [https://www.youtube.com/watch?v=W7LVpOQnxx0](https://www.youtube.com/watch?v=W7LVpOQnxx0) | host-hub | mirrored |
| 2026-01-12 | Richard D. Wolff & Michael Hudson: From Oil to Armageddon, Toward Global Conflict | Richard D. Wolff & Michael Hudson | [https://www.youtube.com/watch?v=TyUA89Yh6vA](https://www.youtube.com/watch?v=TyUA89Yh6vA) | host-hub | mirrored |
| 2026-01-13 | Alex Krainer: Trump, Venezuela & The Hidden Logic Behind U.S. Foreign Moves | Alex Krainer | [https://www.youtube.com/watch?v=TS8BBf2_DsI](https://www.youtube.com/watch?v=TS8BBf2_DsI) | host-hub | mirrored |
| 2026-01-14 | Iranian Deputy FM Saeed Khatibzadeh: All-Out War? Iran Says It’s Ready for Any Attack | Iranian Deputy FM Saeed Khatibzadeh | [https://www.youtube.com/watch?v=M_IehjFxDW8](https://www.youtube.com/watch?v=M_IehjFxDW8) | host-hub | mirrored |
| 2026-01-15 | Alastair Crooke: The EU Is Losing Control—And You Can See It | Alastair Crooke | [https://www.youtube.com/watch?v=5rW_GUosll8](https://www.youtube.com/watch?v=5rW_GUosll8) | thread: crooke | mirrored |
| 2026-01-24 | Larry C. Johnson & Col. Larry Wilkerson: Trump’s War Gamble Just Blew Up in His Face | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=k2Hx4x9aGro](https://www.youtube.com/watch?v=k2Hx4x9aGro) | thread: johnson | mirrored |
| 2026-01-25 | Alastair Crooke: Systemic Collapse Explained: Why Two Fronts Matter | Alastair Crooke | [https://www.youtube.com/watch?v=IAKqyzQen04](https://www.youtube.com/watch?v=IAKqyzQen04) | thread: crooke | mirrored |
| 2026-01-26 | Scott Ritter: This Is the Moment the West Started Losing | Scott Ritter | [https://www.youtube.com/watch?v=x9UQLEviJ2o](https://www.youtube.com/watch?v=x9UQLEviJ2o) | thread: ritter | mirrored |
| 2026-01-27 | Patrick Henningsen: The EU Is Facing DEVASTATING Realities | Patrick Henningsen | [https://www.youtube.com/watch?v=9RaFBDfKE8w](https://www.youtube.com/watch?v=9RaFBDfKE8w) | host-hub | mirrored |
| 2026-01-28 | Andrei Martyanov: US-Iran War About to Break Out | Andrei Martyanov | [https://www.youtube.com/watch?v=PB6wU2l1wv8](https://www.youtube.com/watch?v=PB6wU2l1wv8) | host-hub | mirrored |
| 2026-01-29 | Amb. Chas Freeman: Countdown to War between The US and Iran - History Is Repeating Itself | Amb. Chas Freeman | [https://www.youtube.com/watch?v=mH6pV88ScII](https://www.youtube.com/watch?v=mH6pV88ScII) | thread: freeman | needs capture |
| 2026-01-30 | Larry C. Johnson & Col. Larry Wilkerson: One Strike Away from Global Chaos, US-Iran War IMMINENT | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=jyxqTCfydMk](https://www.youtube.com/watch?v=jyxqTCfydMk) | thread: johnson | needs capture |

---

**Companion files:** [`transcript.md`](transcript.md) (7-day rolling verbatim) and [`thread.md`](thread.md) (distilled analytical thread).
