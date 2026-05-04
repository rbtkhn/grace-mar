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

Metadata-only index from the public YouTube crawl starting at `2026-01-01` through the latest upload returned by the crawl. Transcript bodies are not backfilled in this pass. `needs capture` means the episode is visible on the channel but not yet mirrored in `raw-input/`.

| pub_date | Title | Guest | URL | Routing / note | raw-input |
|----------|-------|-------|-----|----------------|-----------|
| 2026-01-03 | Max Blumenthal: This Is the Utmost Failure: Trump Creates Absolute Chaos - Iran & Venezuela | Max Blumenthal | [https://www.youtube.com/watch?v=aeT3jwwUE6A](https://www.youtube.com/watch?v=aeT3jwwUE6A) | host-hub | mirrored |
| 2026-01-04 | Alastair Crooke: The Hidden Signal: How One Answer Could Ignite the Middle East | Alastair Crooke | [https://www.youtube.com/watch?v=5JVKloRggyo](https://www.youtube.com/watch?v=5JVKloRggyo) | thread: crooke | mirrored |
| 2026-01-09 | Col. Larry Wilkerson: 21st Century Peril: How Americaâ€™s Power Plays Risk Everything | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=8DpLyv_7IiI](https://www.youtube.com/watch?v=8DpLyv_7IiI) | thread: johnson | mirrored |
| 2026-01-10 | Scott Ritter: Russia All in to Confront the Worst-Case Scenario | Scott Ritter | [https://www.youtube.com/watch?v=DuS17MeaWgE](https://www.youtube.com/watch?v=DuS17MeaWgE) | thread: ritter | mirrored |
| 2026-01-11 | Pepe Escobar: Trump, Greenland, NATO Collapse & Global Power Shock | Pepe Escobar | [https://www.youtube.com/watch?v=W7LVpOQnxx0](https://www.youtube.com/watch?v=W7LVpOQnxx0) | host-hub | mirrored |
| 2026-01-12 | Richard D. Wolff & Michael Hudson: From Oil to Armageddon, Toward Global Conflict | Richard D. Wolff & Michael Hudson | [https://www.youtube.com/watch?v=TyUA89Yh6vA](https://www.youtube.com/watch?v=TyUA89Yh6vA) | host-hub | mirrored |
| 2026-01-13 | Alex Krainer: Trump, Venezuela & The Hidden Logic Behind U.S. Foreign Moves | Alex Krainer | [https://www.youtube.com/watch?v=TS8BBf2_DsI](https://www.youtube.com/watch?v=TS8BBf2_DsI) | host-hub | mirrored |
| 2026-01-14 | Iranian Deputy FM Saeed Khatibzadeh: All-Out War? Iran Says Itâ€™s Ready for Any Attack | Iranian Deputy FM Saeed Khatibzadeh | [https://www.youtube.com/watch?v=M_IehjFxDW8](https://www.youtube.com/watch?v=M_IehjFxDW8) | host-hub | mirrored |
| 2026-01-15 | Alastair Crooke: The EU Is Losing Controlâ€”And You Can See It | Alastair Crooke | [https://www.youtube.com/watch?v=5rW_GUosll8](https://www.youtube.com/watch?v=5rW_GUosll8) | thread: crooke | mirrored |
| 2026-01-24 | Larry C. Johnson & Col. Larry Wilkerson: Trumpâ€™s War Gamble Just Blew Up in His Face | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=k2Hx4x9aGro](https://www.youtube.com/watch?v=k2Hx4x9aGro) | thread: johnson | mirrored |
| 2026-01-25 | Alastair Crooke: Systemic Collapse Explained: Why Two Fronts Matter | Alastair Crooke | [https://www.youtube.com/watch?v=IAKqyzQen04](https://www.youtube.com/watch?v=IAKqyzQen04) | thread: crooke | mirrored |
| 2026-01-26 | Scott Ritter: This Is the Moment the West Started Losing | Scott Ritter | [https://www.youtube.com/watch?v=x9UQLEviJ2o](https://www.youtube.com/watch?v=x9UQLEviJ2o) | thread: ritter | mirrored |
| 2026-01-27 | Patrick Henningsen: The EU Is Facing DEVASTATING Realities | Patrick Henningsen | [https://www.youtube.com/watch?v=9RaFBDfKE8w](https://www.youtube.com/watch?v=9RaFBDfKE8w) | host-hub | mirrored |
| 2026-01-28 | Andrei Martyanov: US-Iran War About to Break Out | Andrei Martyanov | [https://www.youtube.com/watch?v=PB6wU2l1wv8](https://www.youtube.com/watch?v=PB6wU2l1wv8) | host-hub | mirrored |
| 2026-01-29 | Amb. Chas Freeman: Countdown to War between The US and Iran - History Is Repeating Itself | Amb. Chas Freeman | [https://www.youtube.com/watch?v=mH6pV88ScII](https://www.youtube.com/watch?v=mH6pV88ScII) | thread: freeman | needs capture |
| 2026-01-30 | Larry C. Johnson & Col. Larry Wilkerson: One Strike Away from Global Chaos, US-Iran War IMMINENT | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=jyxqTCfydMk](https://www.youtube.com/watch?v=jyxqTCfydMk) | thread: johnson | needs capture |

### Manual additions

User-supplied Dialogue Works rows added outside the January crawl snapshot. Some rows are mirrored in the crawl table; all others are marked `needs capture` until mirrored into `raw-input/`.

| pub_date | Title | Guest | URL | Routing / note | raw-input |
|----------|-------|-------|-----|----------------|-----------|
| 2025-10-16 | Jeffrey Sachs & John Mearsheimer: Spheres of Security to Prevent World War III | Jeffrey Sachs & John Mearsheimer | [https://www.youtube.com/watch?v=Ntkc7AWujEU](https://www.youtube.com/watch?v=Ntkc7AWujEU) | host-hub | needs capture |
| 2025-05-28 | Prof. Ted Postol: Terrifying Cost of Trump's Space Missile Defense: Bankrupt USA, Provoke World War? | Prof. Ted Postol | [https://www.youtube.com/watch?v=DJEnqn5sdyo](https://www.youtube.com/watch?v=DJEnqn5sdyo) | thread: postol | needs capture |
| 2025-06-16 | Prof. Ted Postol: Iran?s Hypersonic Missiles PENETRATE Iron Dome! | Prof. Ted Postol | [https://www.youtube.com/watch?v=X6dZMMvRegQ](https://www.youtube.com/watch?v=X6dZMMvRegQ) | thread: postol | needs capture |
| 2025-06-28 | Prof. Ted Postol on Why No Bomb on Earth Can Destroy Iran's Nuclear Program! | Prof. Ted Postol | [https://www.youtube.com/watch?v=dHvOhBKNs-E](https://www.youtube.com/watch?v=dHvOhBKNs-E) | thread: postol | needs capture |
| 2025-07-24 | Prof. Ted Postol: The War That Solves Nothing: Why Attacking Iran Is a Losing Game | Prof. Ted Postol | [https://www.youtube.com/watch?v=1gTSkc_EMhM](https://www.youtube.com/watch?v=1gTSkc_EMhM) | thread: postol | needs capture |
| 2025-11-05 | Scott Ritter: Russia & Iran Just Triggered It All! | Scott Ritter | [https://www.youtube.com/watch?v=UMTrfuXVD4g](https://www.youtube.com/watch?v=UMTrfuXVD4g) | thread: ritter | needs capture |
| 2025-11-13 | Andrei Martyanov: Frontline FALLING APART: Russia Moves to CRUSH Ukraine’s Entire Army | Andrei Martyanov | [https://www.youtube.com/watch?v=V0IIiN_Pz2o](https://www.youtube.com/watch?v=V0IIiN_Pz2o) | thread: martyanov | needs capture |
| 2025-11-14 | Col. Daniel Davis: Russia’s Final Push in Ukraine — Iran Signals MAJOR Retaliation to Israel! | Col. Daniel Davis | [https://www.youtube.com/watch?v=7QB1RhRw1DI](https://www.youtube.com/watch?v=7QB1RhRw1DI) | thread: davis | needs capture |
| 2025-11-17 | Col. Jacques Baud: If the U.S. Leaves, Ukraine Falls â€” Europe Finally Admits the Truth? | Col. Jacques Baud | [https://www.youtube.com/watch?v=OyNCVoHtc_g](https://www.youtube.com/watch?v=OyNCVoHtc_g) | thread: baud | needs capture |
| 2025-11-20 | Andrei Martyanov: It’s ALL OVER: Iran, Russia & China Move In Together | Andrei Martyanov | [https://www.youtube.com/watch?v=rCalPQD48bc](https://www.youtube.com/watch?v=rCalPQD48bc) | thread: martyanov | needs capture |
| 2025-11-21 | Amb. Chas Freeman: Why Ukraine AND Israel Are Closer to a Dead End Than Ever | Amb. Chas Freeman | [https://www.youtube.com/watch?v=Uh8gaC1gxlg](https://www.youtube.com/watch?v=Uh8gaC1gxlg) | thread: freeman | needs capture |
| 2025-12-01 | Col. Jacques Baud: Is Corruption the Hidden Key to Ukraineâ€™s War? | Col. Jacques Baud | [https://www.youtube.com/watch?v=M6q-2VVX2Sw](https://www.youtube.com/watch?v=M6q-2VVX2Sw) | thread: baud | needs capture |
| 2025-12-02 | Mohammad Marandi: Middle East Shifts as Two More Wars ERUPT | Mohammad Marandi | [https://www.youtube.com/watch?v=_YDctqUbxJE](https://www.youtube.com/watch?v=_YDctqUbxJE) | thread: marandi | needs capture |
| 2025-12-04 | Andrei Martyanov: Russia Has Made Its Choice, Wiping Out Every Threat | Andrei Martyanov | [https://www.youtube.com/watch?v=08Y6K95zKfI](https://www.youtube.com/watch?v=08Y6K95zKfI) | thread: martyanov | needs capture |
| 2025-12-05 | Amb. Chas Freeman: Israel???s Strategy Is Collapsing \| EU Seems Paralyzed \| Ceding the Future to China | Amb. Chas Freeman | [https://www.youtube.com/watch?v=oKuDN1rYFTM](https://www.youtube.com/watch?v=oKuDN1rYFTM) | thread: freeman | needs capture |
| 2025-12-08 | Col. Jacques Baud: Ukraineâ€™s Defense Falls Apart After Putinâ€™s Devastating Attacks! | Col. Jacques Baud | [https://www.youtube.com/watch?v=Wv_BZBUrKfo](https://www.youtube.com/watch?v=Wv_BZBUrKfo) | thread: baud | needs capture |
| 2025-12-11 | Andrei Martyanov: Russia’s “Game Over” Strategy Is Now LIVE | Andrei Martyanov | [https://www.youtube.com/watch?v=CtMwRfJok38](https://www.youtube.com/watch?v=CtMwRfJok38) | thread: martyanov | needs capture |
| 2025-12-12 | Col. Larry Wilkerson & Amb. Chas Freeman: The U.S. Just Triggered a Chain Reaction It Canâ€™t Reverse | Col. Larry Wilkerson & Amb. Chas Freeman | [https://www.youtube.com/watch?v=W1h2i5NscpI](https://www.youtube.com/watch?v=W1h2i5NscpI) | thread: freeman | needs capture |
| 2025-12-15 | Larry C. Johnson: Russia Launches Largest Missile & Drone Attack Yet | Larry C. Johnson | [https://www.youtube.com/watch?v=-1Cpb5Nh7zc](https://www.youtube.com/watch?v=-1Cpb5Nh7zc) | thread: johnson | needs capture |
| 2025-12-23 | Colonel Jacques Baud: Sanctioned, Not Silent | Colonel Jacques Baud | [https://www.youtube.com/watch?v=CNWKPJSYumA](https://www.youtube.com/watch?v=CNWKPJSYumA) | thread: baud | needs capture |
| 2025-12-26 | Larry C. Johnson & Col. Larry Wilkerson: Colossal Shifts Rock the Middle East & Europe | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=95MnFFUtSeQ](https://www.youtube.com/watch?v=95MnFFUtSeQ) | thread: johnson | needs capture |
| 2025-12-29 | Col. Jacques Baud: Is the West Finally Waking Up? | Col. Jacques Baud | [https://www.youtube.com/watch?v=V0vDYf_YXmc](https://www.youtube.com/watch?v=V0vDYf_YXmc) | thread: baud | needs capture |
| 2025-12-30 | Alastair Crooke: The West Is Redrawing Strategy: Russia Just Went All In | Alastair Crooke | [https://www.youtube.com/watch?v=2vk5T6ZOdI8](https://www.youtube.com/watch?v=2vk5T6ZOdI8) | thread: crooke | needs capture |
| 2025-12-30 | Col. Larry Wilkerson: The Alarms Are Screaming And America Is Ignoring It | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=nVxq4eCzK64](https://www.youtube.com/watch?v=nVxq4eCzK64) | thread: johnson | needs capture |
| 2025-12-31 | Max Blumenthal: Trump?s 2025 Wrap-Up: Wars Still Burning | Max Blumenthal | [https://www.youtube.com/watch?v=FHZaYOLj4mE](https://www.youtube.com/watch?v=FHZaYOLj4mE) | thread: blumenthal | needs capture |
| 2026-01-01 | Andrei Martyanov: IT’S ALL OVER… Iran & Russia Just Went ALL IN | Andrei Martyanov | [https://www.youtube.com/watch?v=9zqRNDWkiGU](https://www.youtube.com/watch?v=9zqRNDWkiGU) | thread: martyanov | needs capture |
| 2026-01-02 | Amb. Chas Freeman & Mohammad Marandi: Trump Issues Warning to Iran â€” Tehran Fires Back Immediately | Amb. Chas Freeman & Mohammad Marandi | [https://www.youtube.com/watch?v=ZTblriezXv0](https://www.youtube.com/watch?v=ZTblriezXv0) | thread: marandi | needs capture |
| 2026-01-02 | Larry C. Johnson & Col. Larry Wilkerson: Russia & Iran Just Built a WAR Shield - China Warns | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=dqMTzR4vYek](https://www.youtube.com/watch?v=dqMTzR4vYek) | thread: johnson | needs capture |
| 2026-01-03 | Max Blumenthal: This Is the Utmost Failure: Trump Creates Absolute Chaos - Iran & Venezuela | Max Blumenthal | [https://www.youtube.com/watch?v=aeT3jwwUE6A](https://www.youtube.com/watch?v=aeT3jwwUE6A) | thread: blumenthal | mirrored |
| 2026-01-06 | Col. Jacques Baud: The World Is Entering a Lawless Era | Col. Jacques Baud | [https://www.youtube.com/watch?v=-62UrB2Nyl0](https://www.youtube.com/watch?v=-62UrB2Nyl0) | thread: baud | needs capture |
| 2026-01-06 | Mohammad Marandi: Locked and Loadedâ€™: US and Iran Trade Warnings - Venezuela Enters the Picture | Mohammad Marandi | [https://www.youtube.com/watch?v=oHjWJ44AYgQ](https://www.youtube.com/watch?v=oHjWJ44AYgQ) | thread: marandi | needs capture |
| 2026-01-07 | Col. Daniel Davis: Trump’s Venezuela Disaster - Greenland Proves NATO Is Collapsing | Col. Daniel Davis | [https://www.youtube.com/watch?v=4tYch_1OqM4](https://www.youtube.com/watch?v=4tYch_1OqM4) | thread: davis | needs capture |
| 2026-01-07 | Scott Ritter & Pepe Escobar: Trumpâ€™s Venezuela Strategy Is Falling Apart | Scott Ritter & Pepe Escobar | [https://www.youtube.com/watch?v=8O49reYeJRw](https://www.youtube.com/watch?v=8O49reYeJRw) | thread: ritter | needs capture |
| 2026-01-15 | Alastair Crooke: The EU Is Losing Control?And You Can See It | Alastair Crooke | [https://www.youtube.com/watch?v=5rW_GUosll8](https://www.youtube.com/watch?v=5rW_GUosll8) | thread: crooke | mirrored |
| 2026-01-19 | Col. Jacques Baud: EU Drops a Bombshell While NATO Faces Serious Trouble | Col. Jacques Baud | [https://www.youtube.com/watch?v=aGFaT9WDChM](https://www.youtube.com/watch?v=aGFaT9WDChM) | thread: baud | needs capture |
| 2026-01-22 | Amb. Chas Freeman: Iran Vows Huge Response to US-Israel Attack | Amb. Chas Freeman | [https://www.youtube.com/watch?v=AtJJohRHHV0](https://www.youtube.com/watch?v=AtJJohRHHV0) | thread: freeman | needs capture |
| 2026-01-25 | Alastair Crooke: Systemic Collapse Explained: Why Two Fronts Matter | Alastair Crooke | [https://www.youtube.com/watch?v=IAKqyzQen04](https://www.youtube.com/watch?v=IAKqyzQen04) | thread: crooke | mirrored |
| 2026-02-02 | Col. Jacques Baud: Why the EU Is Failing on Every Front | Col. Jacques Baud | [https://www.youtube.com/watch?v=3Q4PNfLiGv8](https://www.youtube.com/watch?v=3Q4PNfLiGv8) | thread: baud | needs capture |
| 2026-02-03 | Col. Larry Wilkerson: Trump Caves Under Pressure ? Iran?s Capabilities Now Bigger Than Ever | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=0_4oSjl8Z2M](https://www.youtube.com/watch?v=0_4oSjl8Z2M) | thread: johnson | needs capture |
| 2026-02-04 | Scott Ritter: Game Over? Trumpâ€™s Iran Strategy Might Blow Up and Start a Regional War | Scott Ritter | [https://www.youtube.com/watch?v=iuc_pPvcFC0](https://www.youtube.com/watch?v=iuc_pPvcFC0) | thread: ritter | needs capture |
| 2026-02-06 | Amb. Chas Freeman: Negotiationsâ€¦ or the Brink of All-Out War? | Amb. Chas Freeman | [https://www.youtube.com/watch?v=AdJzX_YXSEU](https://www.youtube.com/watch?v=AdJzX_YXSEU) | thread: freeman | needs capture |
| 2026-02-06 | Larry C. Johnson & Col. Larry Wilkerson: The New Axis? Russia, Iran War Shield & Chinaâ€™s WARNING | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=ezGG_nNcm18](https://www.youtube.com/watch?v=ezGG_nNcm18) | thread: johnson | needs capture |
| 2026-02-10 | Col. Larry Wilkerson: The U.S. Just Hit a Point of No Return | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=EyzGGI5hQA8](https://www.youtube.com/watch?v=EyzGGI5hQA8) | thread: johnson | needs capture |
| 2026-02-10 | Mohammad Marandi & Larry C. Johnson: U.S. & Iran on the Brink as Critical Negotiations Unfold LIVE | Mohammad Marandi & Larry C. Johnson | [https://www.youtube.com/watch?v=-CAqyFWDBbQ](https://www.youtube.com/watch?v=-CAqyFWDBbQ) | thread: johnson | needs capture |
| 2026-02-11 | Scott Ritter: Trump in MAJOR Trouble â€” China & Russia Arm Iran With Deadly Weapons! | Scott Ritter | [https://www.youtube.com/watch?v=DCZn8RZS9Zk](https://www.youtube.com/watch?v=DCZn8RZS9Zk) | thread: ritter | needs capture |
| 2026-02-12 | Andrei Martyanov: Iran’s Trap Is Already Set… And the U.S. Is Moving In | Andrei Martyanov | [https://www.youtube.com/watch?v=_6_8JvP6Y9Y](https://www.youtube.com/watch?v=_6_8JvP6Y9Y) | thread: martyanov | needs capture |
| 2026-02-13 | Larry C. Johnson & Col. Larry Wilkerson: Russia + Iran + China: War Shield That Changes the World | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=zN8Pp6YQNME](https://www.youtube.com/watch?v=zN8Pp6YQNME) | thread: johnson | needs capture |
| 2026-02-14 | Prof. Ted Postol: The U.S.?Iran War About to Break Out - Who Has the Edge? | Prof. Ted Postol | [https://www.youtube.com/watch?v=llW5RUMkZLo](https://www.youtube.com/watch?v=llW5RUMkZLo) | thread: postol | needs capture |
| 2026-02-16 | Col. Jacques Baud: Iran Goes All In -This Could Be the EUâ€™s Biggest Blunder Yet | Col. Jacques Baud | [https://www.youtube.com/watch?v=0ZGC4Uswerk](https://www.youtube.com/watch?v=0ZGC4Uswerk) | thread: baud | needs capture |
| 2026-02-16 | Larry C. Johnson: Iran Just Leveled Up | Larry C. Johnson | [https://www.youtube.com/watch?v=WIiWaLL5SeQ](https://www.youtube.com/watch?v=WIiWaLL5SeQ) | thread: johnson | needs capture |
| 2026-02-17 | Col. Larry Wilkerson: The Strategy Trump Is Betting Everything On Is Crumbling | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=9ZiTVDZnecU](https://www.youtube.com/watch?v=9ZiTVDZnecU) | thread: johnson | needs capture |
| 2026-02-17 | Mohammad Marandi: Iran JUST Closed the Strait of Hormuz - Wiped Out: Iran Plans to Sink the US Navy | Mohammad Marandi | [https://www.youtube.com/watch?v=7Oy1q6zGcQs](https://www.youtube.com/watch?v=7Oy1q6zGcQs) | thread: marandi | needs capture |
| 2026-02-18 | Scott Ritter: Hormuz Blocked! Iranâ€™s Missile Fire Can Leave the US Navy DEFENSELESS | Scott Ritter | [https://www.youtube.com/watch?v=DCDuxei5dj8](https://www.youtube.com/watch?v=DCDuxei5dj8) | thread: ritter | needs capture |
| 2026-02-19 | Andrei Martyanov: IRAN BOMBSHELL: Hypersonic Missile Could Sink US Navy Carrier — Trump WARNED! | Andrei Martyanov | [https://www.youtube.com/watch?v=7gT4A9FO7KQ](https://www.youtube.com/watch?v=7gT4A9FO7KQ) | thread: martyanov | needs capture |
| 2026-02-20 | Alastair Crooke: Trump?s Final Gamble: Iran Dares to Strike Back | Alastair Crooke | [https://www.youtube.com/watch?v=rSvsMr-wnq0](https://www.youtube.com/watch?v=rSvsMr-wnq0) | thread: crooke | needs capture |
| 2026-02-20 | Amb. Chas Freeman: Is Israel Dragging the U.S. Into Israelâ€™s Next Endless War? | Amb. Chas Freeman | [https://www.youtube.com/watch?v=Dm5QS9WLZGk](https://www.youtube.com/watch?v=Dm5QS9WLZGk) | thread: freeman | needs capture |
| 2026-02-20 | Larry C. Johnson & Col. Larry Wilkerson: Iran Warns U.S. in Urgent Letter to UN Vowing to WIPE OUT | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=NLFq45I4cm0](https://www.youtube.com/watch?v=NLFq45I4cm0) | thread: johnson | needs capture |
| 2026-02-23 | Larry C. Johnson: Existential Fight: The 'Hell' Iran Has Prepared for a War w/ US and it's happening | Larry C. Johnson | [https://www.youtube.com/watch?v=VP-9Yp9wYxM](https://www.youtube.com/watch?v=VP-9Yp9wYxM) | thread: johnson | needs capture |
| 2026-02-24 | Col. Larry Wilkerson: Pentagon Drops URGENT Warning on Trump: 'This Will Be a Long War' | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=rxS8lUTrGgw](https://www.youtube.com/watch?v=rxS8lUTrGgw) | thread: johnson | needs capture |
| 2026-02-24 | Max Blumenthal: Boasting of ?deploying? 200 Starlinks to Iran amid violence | Max Blumenthal | [https://www.youtube.com/watch?v=frPTFPj80WA](https://www.youtube.com/watch?v=frPTFPj80WA) | thread: blumenthal | needs capture |
| 2026-02-24 | Mohammad Marandi: U.S. and Iran Position Final Assets, Tensions Hit the Final Hour | Mohammad Marandi | [https://www.youtube.com/watch?v=77_n4Hh-kR0](https://www.youtube.com/watch?v=77_n4Hh-kR0) | thread: marandi | needs capture |
| 2026-02-25 | Scott Ritter: The Triad of Power: What China, Russia & Iran Are Really Building | Scott Ritter | [https://www.youtube.com/watch?v=QzxLeLICcQs](https://www.youtube.com/watch?v=QzxLeLICcQs) | thread: ritter | needs capture |
| 2026-02-27 | Amb. Chas Freeman: Emergency Diplomacy! Omanâ€™s FM Flies to Washington to Avert War with Iran | Amb. Chas Freeman | [https://www.youtube.com/watch?v=Vt84YYBocq0](https://www.youtube.com/watch?v=Vt84YYBocq0) | thread: freeman | needs capture |
| 2026-02-27 | Larry C. Johnson & Col. Larry Wilkerson: Iran-US Talks on the Edge, War Could Break Out ANY MOMENT! | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=t4d42-oT7nw](https://www.youtube.com/watch?v=t4d42-oT7nw) | thread: johnson | needs capture |
| 2026-03-01 | Mohammad Marandi: Iranâ€™s Supreme Leader MARTYRED in US-Israeli Attacks, Tehran Says You Will Regret | Mohammad Marandi | [https://www.youtube.com/watch?v=U2mFiQk8oLA](https://www.youtube.com/watch?v=U2mFiQk8oLA) | thread: marandi | needs capture |
| 2026-03-01 | Prof. Theodore Postol: Iran War Is HERE ? U.S. & Israel ATTACK & Iran?s Devastating Counterattack | Prof. Theodore Postol | [https://www.youtube.com/watch?v=iH6nN0EUGvM](https://www.youtube.com/watch?v=iH6nN0EUGvM) | thread: postol | needs capture |
| 2026-03-01 | Scott Ritter: Iran TARGETS the USS Abraham Lincoln Aircraft Carrier â€” Obliterating US Bases & Israel | Scott Ritter | [https://www.youtube.com/watch?v=NOwpAySRwG4](https://www.youtube.com/watch?v=NOwpAySRwG4) | thread: ritter | needs capture |
| 2026-03-02 | Col. Jacques Baud: Middle East on Fire â€” Is This the Start of Something Bigger? | Col. Jacques Baud | [https://www.youtube.com/watch?v=0HZWfVt_Pjg](https://www.youtube.com/watch?v=0HZWfVt_Pjg) | thread: baud | needs capture |
| 2026-03-03 | Col. Larry Wilkerson: US Warplanes Downed, Tel Aviv & U.S. Bases ROCKED by Missiles | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=VSM5yjbYrbY](https://www.youtube.com/watch?v=VSM5yjbYrbY) | thread: johnson | needs capture |
| 2026-03-03 | Mohammad Marandi: Tehran Under FIRE & Israel Faces OBLITERATION | Mohammad Marandi | [https://www.youtube.com/watch?v=EhBb6F7tPps](https://www.youtube.com/watch?v=EhBb6F7tPps) | thread: marandi | needs capture |
| 2026-03-04 | Scott Ritter: Iran Wins the Long War â€” U.S. & Israel Losing Ground! | Scott Ritter | [https://www.youtube.com/watch?v=MWlCgZMYqk8](https://www.youtube.com/watch?v=MWlCgZMYqk8) | thread: ritter | needs capture |
| 2026-03-05 | Andrei Martyanov: IT'S OVER for the Bases! Radar Destroyed! F-15 Fighters Shot Down! | Andrei Martyanov | [https://www.youtube.com/watch?v=V7W6hk-vyok](https://www.youtube.com/watch?v=V7W6hk-vyok) | thread: martyanov | needs capture |
| 2026-03-06 | Amb. Chas Freeman: The War With Iran Is Breaking Everything the U.S. Planned | Amb. Chas Freeman | [https://www.youtube.com/watch?v=FM1WOmbdzmA](https://www.youtube.com/watch?v=FM1WOmbdzmA) | thread: freeman | needs capture |
| 2026-03-06 | Larry C. Johnson & Col. Larry Wilkerson: Iran WIPES OUT Huge Targets, Explosions in Tehran | Larry C. Johnson & Col. Larry Wilkerson | [https://www.youtube.com/watch?v=0eEFS75Z6pY](https://www.youtube.com/watch?v=0eEFS75Z6pY) | thread: johnson | needs capture |
| 2026-03-09 | Col. Jacques Baud: The Middle East Just Changed Forever | Col. Jacques Baud | [https://www.youtube.com/watch?v=iYcnztEdjq0](https://www.youtube.com/watch?v=iYcnztEdjq0) | thread: baud | needs capture |
| 2026-03-10 | Col. Larry Wilkerson: Israel Can?t Survive This? What Just Happened Changes Everything | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=7yo7wGFQRYw](https://www.youtube.com/watch?v=7yo7wGFQRYw) | thread: johnson | needs capture |
| 2026-03-10 | MIT Prof. Ted Postol: Iranian Missiles vs Israeli Air Defense: Who Would Actually Win? | MIT Prof. Ted Postol | [https://www.youtube.com/watch?v=nMjMz8yL_kk](https://www.youtube.com/watch?v=nMjMz8yL_kk) | thread: postol | needs capture |
| 2026-03-11 | Scott Ritter: The U.S. Has Lost and Is Trapped in the Iran War With No Way Out | Scott Ritter | [https://www.youtube.com/watch?v=s3cNS4lyJ60](https://www.youtube.com/watch?v=s3cNS4lyJ60) | thread: ritter | needs capture |
| 2026-03-12 | Andrei Martyanov: It’s OVER: Iran Just EXPOSED the Weakness of US-Israel Air Defense | Andrei Martyanov | [https://www.youtube.com/watch?v=jC5Eb8R_B1Q](https://www.youtube.com/watch?v=jC5Eb8R_B1Q) | thread: martyanov | needs capture |
| 2026-03-13 | Amb. Chas Freeman: Israelâ€™s Agenda Is Collapsingâ€¦ And Itâ€™s Happening Fast | Amb. Chas Freeman | [https://www.youtube.com/watch?v=ybrIJMPMn8I](https://www.youtube.com/watch?v=ybrIJMPMn8I) | thread: freeman | needs capture |
| 2026-03-13 | Larry Johnson & Col. Wilkerson: U.S. KC-135 Down â€” Carrier Abraham Lincoln Hit by Missiles & Drones | Larry Johnson & Col. Wilkerson | [https://www.youtube.com/watch?v=LxecocoahPM](https://www.youtube.com/watch?v=LxecocoahPM) | thread: johnson | needs capture |
| 2026-03-16 | Pepe Escobar & Larry C. Johnson: Trump is LOSING Control - Iran WIPES OUT Strategic Military Targets | Pepe Escobar & Larry C. Johnson | [https://www.youtube.com/watch?v=7ROzzOkmHsY](https://www.youtube.com/watch?v=7ROzzOkmHsY) | thread: johnson | needs capture |
| 2026-03-17 | Alastair Crooke: Iran Was Ready for This War? And It Could Change the Middle East Forever | Alastair Crooke | [https://www.youtube.com/watch?v=bfZMcqICySg](https://www.youtube.com/watch?v=bfZMcqICySg) | thread: crooke | needs capture |
| 2026-03-17 | Col. Larry Wilkerson: Trump Intelligence Pick Joe Kent QUITS - Israel Goes Nuclear Loses EVERYTHING | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=bNFQ4a8JeE8](https://www.youtube.com/watch?v=bNFQ4a8JeE8) | thread: johnson | needs capture |
| 2026-03-17 | Mohammad Marandi: â€œNo Truce, No Talksâ€: Iran SLAMS US Claims as War Drags On | Mohammad Marandi | [https://www.youtube.com/watch?v=53WrfDcWyuc](https://www.youtube.com/watch?v=53WrfDcWyuc) | thread: marandi | needs capture |
| 2026-03-18 | Scott Ritter: Iran UNLEASHES Missiles on Tel Aviv & US Bases | Scott Ritter | [https://www.youtube.com/watch?v=483Mn6Jl4nQ](https://www.youtube.com/watch?v=483Mn6Jl4nQ) | thread: ritter | needs capture |
| 2026-03-19 | Andrei Martyanov: Iran Hits US F-35… MASSIVE Retaliation After Israel Hits MAJOR Energy Hub | Andrei Martyanov | [https://www.youtube.com/watch?v=Dp5FDSAgjiY](https://www.youtube.com/watch?v=Dp5FDSAgjiY) | thread: martyanov | needs capture |
| 2026-03-20 | Amb. Chas Freeman: Ground Troops in Iran? This Could Collapse Netanyahuâ€™s Strategy | Amb. Chas Freeman | [https://www.youtube.com/watch?v=gwobyOxdf08](https://www.youtube.com/watch?v=gwobyOxdf08) | thread: freeman | needs capture |
| 2026-03-20 | Larry Johnson & Col. Wilkerson: Second F-35 Down - Iran War Spirals Into DEVASTATING New Phase | Larry Johnson & Col. Wilkerson | [https://www.youtube.com/watch?v=O8nDFUPG0Hs](https://www.youtube.com/watch?v=O8nDFUPG0Hs) | thread: johnson | needs capture |
| 2026-03-23 | Col. Jacques Baud: Iranâ€™s $Billion Power Move: Monetizing the Worldâ€™s Oil Lifeline | Col. Jacques Baud | [https://www.youtube.com/watch?v=w00jitzvnTM](https://www.youtube.com/watch?v=w00jitzvnTM) | thread: baud | needs capture |
| 2026-03-23 | Prof. Ted Postol: Israel?s Air Defense in TOTAL COLLAPSE | Prof. Ted Postol | [https://www.youtube.com/watch?v=FOs4skvj5F8](https://www.youtube.com/watch?v=FOs4skvj5F8) | thread: postol | needs capture |
| 2026-03-24 | Seyed M. Marandi: Israel Hits Iran Energy Sites, Iranâ€™s Next Move: Israelâ€™s Energy & Water Systems | Seyed M. Marandi | [https://www.youtube.com/watch?v=b3h1gOSKR_E](https://www.youtube.com/watch?v=b3h1gOSKR_E) | thread: marandi | needs capture |
| 2026-03-25 | Lt Col. Daniel Davis: Iran’s Trap Is Already Set… And the U.S. Is Moving In | Lt Col. Daniel Davis | [https://www.youtube.com/watch?v=_6_8JvP6Y9Y](https://www.youtube.com/watch?v=_6_8JvP6Y9Y) | thread: davis | needs capture |
| 2026-03-27 | Chas Freeman: If Troops Enter Iranâ€¦ Israelâ€™s Entire Strategy FALLS APART | Chas Freeman | [https://www.youtube.com/watch?v=FnMwyOTXhAU](https://www.youtube.com/watch?v=FnMwyOTXhAU) | thread: freeman | needs capture |
| 2026-03-27 | Larry Johnson & Col. Wilkerson: USâ€“Iran Ground Conflict Could DEVASTATE Israel & UAE | Larry Johnson & Col. Wilkerson | [https://www.youtube.com/watch?v=nZEDlBdZTQ4](https://www.youtube.com/watch?v=nZEDlBdZTQ4) | thread: johnson | needs capture |
| 2026-03-28 | Seyed M. Marandi: Yemen Enters the War - US-Israeli Strikes on Energy Sites Spark IRANâ€™S RETALIATION | Seyed M. Marandi | [https://www.youtube.com/watch?v=8SF7zqg5lP8](https://www.youtube.com/watch?v=8SF7zqg5lP8) | thread: marandi | needs capture |
| 2026-03-30 | Col. Jacques Baud: What a US Ground Invasion of Iran Would REALLY Look Like | Col. Jacques Baud | [https://www.youtube.com/watch?v=-e4HBuhGbrE](https://www.youtube.com/watch?v=-e4HBuhGbrE) | thread: baud | needs capture |
| 2026-03-30 | Larry C. Johnson: FULL ESCALATION: Yemen Joins, Hezbollah Crushes Tanks, USâ€“Iran on Brink | Larry C. Johnson | [https://www.youtube.com/watch?v=EpnEi-bLyRQ](https://www.youtube.com/watch?v=EpnEi-bLyRQ) | thread: johnson | needs capture |
| 2026-03-31 | Col. Larry Wilkerson: Israel Might Not Survive This? END EVERYTHING? Israel & Iran Nuclear Scenario | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=dQCTCUR9WHs](https://www.youtube.com/watch?v=dQCTCUR9WHs) | thread: johnson | needs capture |
| 2026-04-02 | Andrei Martyanov: IT’S OVER: The U.S. Just LOST to Iran… Here’s Why | Andrei Martyanov | [https://www.youtube.com/watch?v=3EzbLrujYzY](https://www.youtube.com/watch?v=3EzbLrujYzY) | thread: martyanov | needs capture |
| 2026-04-02 | Scott Ritter: Will Iran Force the US Out of the Middle East? | Scott Ritter | [https://www.youtube.com/watch?v=ALxr05y5YaE](https://www.youtube.com/watch?v=ALxr05y5YaE) | thread: ritter | needs capture |
| 2026-04-03 | Amb. Chas Freeman: Trump PUSHES ESCALATION â€” Israelâ€™s Strategy COLLAPSES Overnight | Amb. Chas Freeman | [https://www.youtube.com/watch?v=wJcTHrczIgA](https://www.youtube.com/watch?v=wJcTHrczIgA) | thread: freeman | needs capture |
| 2026-04-03 | Prof. Ted Postol: Iran Already Achieved NUCLEAR DETERRENCE Against Israel | Prof. Ted Postol | [https://www.youtube.com/watch?v=ab1cfVNWF48](https://www.youtube.com/watch?v=ab1cfVNWF48) | thread: postol | needs capture |
| 2026-04-06 | Col. Jacques Baud: Iran HAMMERS Israel AND GCC Countries After US-Israel Attacks on Key Facilities | Col. Jacques Baud | [https://www.youtube.com/watch?v=ClZ0Bt_wJTU](https://www.youtube.com/watch?v=ClZ0Bt_wJTU) | thread: baud | needs capture |
| 2026-04-06 | Larry C. Johnson: Iran's 'Dead' Defense WIPES OUT US Jets & Black Hawks â€“ Trump Ultimatum FAILS | Larry C. Johnson | [https://www.youtube.com/watch?v=l2QJXZnf1A8](https://www.youtube.com/watch?v=l2QJXZnf1A8) | thread: johnson | needs capture |
| 2026-04-07 | Seyed M. Marandi: Iran SLAMS Trumpâ€™s Ultimatum w/ COUNTER ULTIMATUM â€” War Headed DECIMATING Attacks | Seyed M. Marandi | [https://www.youtube.com/watch?v=k-ZXf1Gd1-Y](https://www.youtube.com/watch?v=k-ZXf1Gd1-Y) | thread: marandi | needs capture |
| 2026-04-10 | Amb. Chas Freeman: Israelâ€™s STRATEGY in TATTERS - Trump TAKES OVER | Amb. Chas Freeman | [https://www.youtube.com/watch?v=fFoKpqMTpq8](https://www.youtube.com/watch?v=fFoKpqMTpq8) | thread: freeman | needs capture |
| 2026-04-10 | Prof. Ted Postol: It?s Over? ? Israel Faces Total Collapse If This War Continues | Prof. Ted Postol | [https://www.youtube.com/watch?v=AizjSdHvjt8](https://www.youtube.com/watch?v=AizjSdHvjt8) | thread: postol | needs capture |
| 2026-04-13 | Col. Jacques Baud: EU Destroys Trumpâ€™s War Fantasy â€“ Leaves Him HUMILIATED | Col. Jacques Baud | [https://www.youtube.com/watch?v=3mtsBSkqW7M](https://www.youtube.com/watch?v=3mtsBSkqW7M) | thread: baud | needs capture |
| 2026-04-13 | Seyed M. Marandi: US Blockade on Iran Just Triggered Iranâ€™s HARSHEST Response Yet | Seyed M. Marandi | [https://www.youtube.com/watch?v=-zLI8STtzB0](https://www.youtube.com/watch?v=-zLI8STtzB0) | thread: marandi | needs capture |
| 2026-04-14 | Col. Larry Wilkerson: ?It?s Over?: Iran Wipes Out Trump?s Bully Tactic on Live Map | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=pqKhinZt3wM](https://www.youtube.com/watch?v=pqKhinZt3wM) | thread: johnson | needs capture |
| 2026-04-15 | Scott Ritter: Trump Panics as Iranâ€™s Strategy Exposes His Biggest Defeat Yet | Scott Ritter | [https://www.youtube.com/watch?v=Gmb40cjXpEw](https://www.youtube.com/watch?v=Gmb40cjXpEw) | thread: ritter | needs capture |
| 2026-04-16 | Andrei Martyanov: How Iran Exposed Trump’s Military & Strategic Failure (Full Breakdown) | Andrei Martyanov | [https://www.youtube.com/watch?v=9QGnItz7CsU](https://www.youtube.com/watch?v=9QGnItz7CsU) | thread: martyanov | needs capture |
| 2026-04-17 | Amb. Chas Freeman: Israelâ€™s Strategy Just COLLAPSED â€“ Trump Steps In | Amb. Chas Freeman | [https://www.youtube.com/watch?v=6qdsG_BfTJ8](https://www.youtube.com/watch?v=6qdsG_BfTJ8) | thread: freeman | needs capture |
| 2026-04-17 | Prof. Ted Postol: Israel NAKED: No Air Defense, No Radars, No Interceptors - Escalation = Suicide | Prof. Ted Postol | [https://www.youtube.com/watch?v=E1AbgZspGjw](https://www.youtube.com/watch?v=E1AbgZspGjw) | thread: postol | needs capture |
| 2026-04-20 | Col. Jacques Baud: DESPERATE Move? Israel Just LOST â€“ Trumpâ€™s Last-Minute Move Changes Everything | Col. Jacques Baud | [https://www.youtube.com/watch?v=UrEuENJ13UA](https://www.youtube.com/watch?v=UrEuENJ13UA) | thread: baud | needs capture |
| 2026-04-20 | Larry Johnson: The Strait of Hormuz Just Became a GRAVEYARD for US DOMINANCE | Larry Johnson | [https://www.youtube.com/watch?v=aUIRaWUtgTA](https://www.youtube.com/watch?v=aUIRaWUtgTA) | thread: johnson | needs capture |
| 2026-04-21 | Max Blumenthal: Israel?s Defeat Begins: Zionist Power Structure FALLING APART in the US | Max Blumenthal | [https://www.youtube.com/watch?v=ZNu4dUynW2w](https://www.youtube.com/watch?v=ZNu4dUynW2w) | thread: blumenthal | needs capture |
| 2026-04-23 | Andrei Martyanov: Iran Just SHOT DOWN Trump’s Blockade… And Israel’s Strategy Is IN TATTERS | Andrei Martyanov | [https://www.youtube.com/watch?v=UZt2dMeq6QM](https://www.youtube.com/watch?v=UZt2dMeq6QM) | thread: martyanov | needs capture |
| 2026-04-24 | Chas Freeman: Israelâ€™s Agenda Is Collapsing Faster Than Anyone Expected | Chas Freeman | [https://www.youtube.com/watch?v=fie-q0V82_E](https://www.youtube.com/watch?v=fie-q0V82_E) | thread: freeman | needs capture |
| 2026-04-25 | Seyed M. Marandi: The Strike That Wiped Out Trumpâ€™s Plan (Itâ€™s Over) | Seyed M. Marandi | [https://www.youtube.com/watch?v=WvNHRluUVjs](https://www.youtube.com/watch?v=WvNHRluUVjs) | thread: marandi | needs capture |
| 2026-04-27 | Col. Jacques Baud: Trumpâ€™s Final Card Just ENDED Israel â€“ Full Breakdown | Col. Jacques Baud | [https://www.youtube.com/watch?v=iZ5xSBYxxyQ](https://www.youtube.com/watch?v=iZ5xSBYxxyQ) | thread: baud | mirrored |
| 2026-04-28 | Col. Larry Wilkerson: Trump?s Own Advisors Now SPLIT on Iran  - Israel?s Plan DECIMATED | Col. Larry Wilkerson | [https://www.youtube.com/watch?v=786X0CXFctA](https://www.youtube.com/watch?v=786X0CXFctA) | thread: johnson | needs capture |
| 2026-05-01 | Amb. Chas Freeman: Israelâ€™s Grand Plan Collapsed in Record Time | Amb. Chas Freeman | [https://www.youtube.com/watch?v=xjRDqdqEl4Y](https://www.youtube.com/watch?v=xjRDqdqEl4Y) | thread: freeman | needs capture |
| 2026-05-01 | Larry C. Johnson & Col. Wilkerson: Itâ€™s Over: Iran Just Wiped Out Trumpâ€™s Blockade - War IMMINENT | Larry C. Johnson & Col. Wilkerson | [https://www.youtube.com/watch?v=Y5Ij0cWArw0](https://www.youtube.com/watch?v=Y5Ij0cWArw0) | thread: johnson | needs capture |
| 2026-05-01 | Prof. Ted Postol: How Iran War Bankrupted the US & Israeli Military | Prof. Ted Postol | [https://www.youtube.com/watch?v=qSmvkuSjGOY](https://www.youtube.com/watch?v=qSmvkuSjGOY) | thread: postol | needs capture |
