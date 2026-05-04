# Strategy expert - `diesen`
<!-- word_count: 486 -->

**Canonical index:** [strategy-commentator-threads.md](strategy-commentator-threads.md) - **`diesen`** lane.

## Identity

| Field | Value |
|-------|-------|
| **Name** | Glenn Diesen |
| **expert_id** | `diesen` |
| **Role** | Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer's structural-realist register |
| **Default grep tags** | `Diesen` in cold |
| **Typical pairings** | x `mearsheimer`, x `macgregor`, x `pape`, x `sachs` |
| **Notebook-use tags** | `orient`, `stress-test`, `historicize` |

<a id="voice-fingerprint-compact"></a>

## Voice fingerprint (compact) - Tier B

| Field | Value |
|-------|-------|
| **Voice tier** | `B` |
| **Voice fingerprint - last reviewed** | `2026-04` |

Promotion and refresh defaults: [strategy-expert-template.md section Voice fingerprint (compact)](strategy-expert-template.md#voice-fingerprint-compact).

## Convergence fingerprint

*Seed profile - operator extends when this lane is upgraded to a full cognitive profile.*

## Tension fingerprint

*Seed profile - operator extends when upgraded.*

## Signature mechanisms

*Seed profile - operator extends when upgraded.*

## Failure modes / overreads

*Seed profile - operator extends when upgraded.*

## Active weave cues

*Seed profile - operator extends when upgraded.*

## Seed (index mirror - operator may extend)

The block below **Rolling ingest** is replaced on each `strategy_thread.py` / `strategy_expert_corpus.py` run; edit this **Seed** section freely.

### Commentator row (from index)

| expert_id | Name | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |
|-----------|------|------------------|------------------|-----------------------------------|
| `diesen` | Glenn Diesen | Eurasia / multipolar discourse; non-Western institutional / rationality frames when distinct from Mearsheimer's structural-realist register | `Diesen` in cold | x `mearsheimer`, x `macgregor`, x `pape`, x `sachs` |

### Quantitative metrics (illustrative - from index)

| expert_id | SCI | AD | CTC | Plain-language note (Predictive History reader) |
|-----------|-----|----|-----|--------------------------------------------------|
| `diesen` | 0.77 | 0.43 | 0.79 | Multipolar language is clearly his own - not a copy of standard U.S. structural realism - so you can tell when Diesen is speaking. Closure looks like his peer group: partly about time and evidence. He is frequently read alongside other realist anchors when the week demands comparison. |

### Published sources (operator web index)

Where their commentary is published and accessible (no Wikipedia). Re-verify handles and media URLs before cite-grade use outside this notebook.

1. https://www.usn.no/english/about/contact-us/employees/diesen
2. https://eng.globalaffairs.ru/authors/diesen/
3. https://x.com/Glenn_Diesen
4. https://www.rt.com/podcast/627315-diesen-ukraine-situation-bad/

## Archive / backfill note

- Archive discovery is useful, but it is not a completeness mandate.
- Capture only substantial Diesen items worth preserving; light or repetitive archive-visible items may stay out by design.
- Automation feeds `raw-input/` only. Pages and thread files are composed later in a separate pass.
- The RT podcast item is treated as a source pointer, but not as an automatic completeness target.

## Input workflow for ledger batches

- Use `scripts/update_diesen_ledger.py` when adding a new Diesen guest-stream batch.
- Give the helper a ledger key such as `mearsheimer` or `sachs`, plus the batch URLs.
- The helper canonicalizes each URL to `watch?v=...`, fetches exact YouTube metadata, dedupes by video ID across the Diesen profile, and refreshes `mirrored` vs `needs capture` by checking `raw-input/`.
- Keep each batch grouped by guest stream; if a URL already exists in another Diesen ledger, the helper skips it instead of duplicating it.

## Automation targets

1. `https://www.usn.no/english/about/contact-us/employees/diesen` -> `thread: diesen`
2. `https://eng.globalaffairs.ru/authors/diesen/` -> `thread: diesen`
3. `https://x.com/Glenn_Diesen` -> `thread: diesen`
4. YouTube transcript crawl via [`scripts/backfill_diesen_youtube_raw_input.py`](../../../../../scripts/backfill_diesen_youtube_raw_input.py) or the generic [`scripts/backfill_youtube_channel_raw_input.py`](../../../../../scripts/backfill_youtube_channel_raw_input.py) with `--channel-url https://www.youtube.com/@GDiesen1/videos --channel-slug glenn-diesen --show "Glenn Diesen" --host "Glenn Diesen" --thread diesen --file-prefix youtube-glenn-diesen`.

## Mearsheimer ledger

User-supplied Glenn Diesen / John Mearsheimer episode URLs added outside the page mirror. Rows marked `mirrored` already have a matching `raw-input/` capture; rows marked `needs capture` should stay visible here until mirrored.

<!-- diesen-ledger:mearsheimer:start -->
| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-05-28 | John Mearsheimer: New World Order? US, China & Russia in the New Great Power Rivalry | [https://www.youtube.com/watch?v=zHA_EBmcKb4](https://www.youtube.com/watch?v=zHA_EBmcKb4) | needs capture |
| 2025-09-07 | John Mearsheimer: West's Failure to Adjust to a Multipolar World | [https://www.youtube.com/watch?v=UMgkvvu_pnU](https://www.youtube.com/watch?v=UMgkvvu_pnU) | needs capture |
| 2025-10-08 | John Mearsheimer: West Destroying Itself in Ukraine & Gaza | [https://www.youtube.com/watch?v=bfO9xfn3fdw](https://www.youtube.com/watch?v=bfO9xfn3fdw) | needs capture |
| 2025-11-25 | John Mearsheimer: Bleak Future of Europe - Defeated & Broken | [https://www.youtube.com/watch?v=e7hAS_8kThs](https://www.youtube.com/watch?v=e7hAS_8kThs) | needs capture |
| 2026-01-07 | John Mearsheimer: Venezuela, Greenland & the End of NATO | [https://www.youtube.com/watch?v=-NQ3lnuYcXs](https://www.youtube.com/watch?v=-NQ3lnuYcXs) | mirrored |
| 2026-01-30 | John Mearsheimer: Cold War 2.0 & NATO's Defeat in Ukraine | [https://www.youtube.com/watch?v=OV75YsYnE8U](https://www.youtube.com/watch?v=OV75YsYnE8U) | mirrored |
| 2026-02-25 | John Mearsheimer: The Case for a Nuclear Iran | [https://www.youtube.com/watch?v=vx1KnspP1gM](https://www.youtube.com/watch?v=vx1KnspP1gM) | mirrored |
| 2026-03-10 | John Mearsheimer: U.S. Already Lost Iran War - No Off-Ramp in Sight | [https://www.youtube.com/watch?v=1e9NhLfPNKU](https://www.youtube.com/watch?v=1e9NhLfPNKU) | mirrored |
| 2026-03-27 | John Mearsheimer: Iran Holds All the Cards - The Strategic Defeat of the U.S. | [https://www.youtube.com/watch?v=DBOVT0UdHXg](https://www.youtube.com/watch?v=DBOVT0UdHXg) | mirrored |
| 2026-04-10 | John Mearsheimer: World Changed Forever as Iran Defeated the U.S. | [https://www.youtube.com/watch?v=H2K3qDshr70](https://www.youtube.com/watch?v=H2K3qDshr70) | mirrored |
| 2026-04-22 | John Mearsheimer: U.S. Expands Iran War & Divorces Europe | [https://www.youtube.com/watch?v=8dUsurWcFdI](https://www.youtube.com/watch?v=8dUsurWcFdI) | needs capture |
<!-- diesen-ledger:mearsheimer:end -->

## Sachs ledger

User-supplied Glenn Diesen / Jeffrey Sachs episode URLs added outside the page mirror. Every row in this batch is currently marked `needs capture`; keep them visible here until mirrored into `raw-input/`.

<!-- diesen-ledger:sachs:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-05-02 | Jeffrey Sachs: Chinese Statecraft & a New World Order | [https://www.youtube.com/watch?v=qcTLAX8hF7I](https://www.youtube.com/watch?v=qcTLAX8hF7I) | needs capture |
| 2025-07-15 | Jeffrey Sachs: End of the Western-Centric World & Rise of BRICS | [https://www.youtube.com/watch?v=VusbFzvhsf4](https://www.youtube.com/watch?v=VusbFzvhsf4) | needs capture |
| 2025-09-18 | Jeffrey Sachs: US and China Edge Toward War Over Taiwan | [https://www.youtube.com/watch?v=E2SsiG1jDLs](https://www.youtube.com/watch?v=E2SsiG1jDLs) | needs capture |
| 2025-10-24 | Jeffrey Sachs: Last Chance for Peace in Ukraine Sabotaged by Europe | [https://www.youtube.com/watch?v=7Wrd2J1pLqk](https://www.youtube.com/watch?v=7Wrd2J1pLqk) | needs capture |
| 2025-11-08 | Jeffrey Sachs: Venezuela Regime Change - Oil & Gangster Politics | [https://www.youtube.com/watch?v=73jqtNqjwcw](https://www.youtube.com/watch?v=73jqtNqjwcw) | needs capture |
| 2025-12-02 | Jeffrey Sachs: Europe Only Accepts Hegemony & Bloc Politics | [https://www.youtube.com/watch?v=-IRCm-JLi0w](https://www.youtube.com/watch?v=-IRCm-JLi0w) | needs capture |
| 2025-12-12 | Jeffrey Sachs: Trump's Distorted Version of the Monroe Doctrine | [https://www.youtube.com/watch?v=-cAPBgQOXfQ](https://www.youtube.com/watch?v=-cAPBgQOXfQ) | needs capture |
| 2025-12-19 | Jeffrey Sachs: An Open Letter to Chancellor Merz - Security Is Indivisible and History Matters | [https://www.youtube.com/watch?v=GbyXNj2P9KE](https://www.youtube.com/watch?v=GbyXNj2P9KE) | needs capture |
| 2026-01-04 | Jeffrey Sachs: U.S. Attacks Venezuela & Kidnaps President Maduro | [https://www.youtube.com/watch?v=LhZuTOuwKGA](https://www.youtube.com/watch?v=LhZuTOuwKGA) | needs capture |
| 2026-01-24 | Jeffrey Sachs: Davos - US Empire Unhinged & Europe Subordinated | [https://www.youtube.com/watch?v=99qnlGOa4Tc](https://www.youtube.com/watch?v=99qnlGOa4Tc) | needs capture |
| 2026-01-28 | Jeffrey Sachs: U.S. War on Iran - "An Attack Is Imminent" | [https://www.youtube.com/watch?v=sYAW_XvvreU](https://www.youtube.com/watch?v=sYAW_XvvreU) | needs capture |
| 2026-02-12 | Jeffrey Sachs: U.S. Economic Coercion & the Death of the Dollar | [https://www.youtube.com/watch?v=ls3ynNpMMPk](https://www.youtube.com/watch?v=ls3ynNpMMPk) | needs capture |
| 2026-02-24 | Jeffrey Sachs: Four Years of War in Ukraine - Hegemony or Peace? | [https://www.youtube.com/watch?v=h7WmEAu87WE](https://www.youtube.com/watch?v=h7WmEAu87WE) | needs capture |
| 2026-02-28 | Jeffrey Sachs: US & Israel Attack Iran - War Is Spreading Across the Region | [https://www.youtube.com/watch?v=nPo8lxyjkCY](https://www.youtube.com/watch?v=nPo8lxyjkCY) | needs capture |
| 2026-03-08 | Jeffrey Sachs: We Are Now in the Early Days of World War III | [https://www.youtube.com/watch?v=DeRETBWnNWA](https://www.youtube.com/watch?v=DeRETBWnNWA) | needs capture |
| 2026-03-20 | The Real Reason There’s No Peace According to Jeffrey Sachs | [https://www.youtube.com/watch?v=gmtJZvmOOes](https://www.youtube.com/watch?v=gmtJZvmOOes) | needs capture |
| 2026-03-25 | Jeffrey Sachs: Iran is the Graveyard of American Hegemony | [https://www.youtube.com/watch?v=OcqIEJEk4MY](https://www.youtube.com/watch?v=OcqIEJEk4MY) | needs capture |
| 2026-04-04 | Jeffrey Sachs: Iran War Broke U.S. Empire & Alliance Systems | [https://www.youtube.com/watch?v=KJsNuI9VVyI](https://www.youtube.com/watch?v=KJsNuI9VVyI) | needs capture |
| 2026-04-24 | Jeffrey Sachs: Trump's Defeat in Iran and the Decline of the American Empire | [https://www.youtube.com/watch?v=8lRC8r8Qzk4](https://www.youtube.com/watch?v=8lRC8r8Qzk4) | needs capture |

<!-- diesen-ledger:sachs:end -->

## Ritter ledger

User-supplied Glenn Diesen / Scott Ritter episode URLs added outside the page mirror. Rows are kept here as a separate guest-stream ledger, with mirror status refreshed from `raw-input/`.

<!-- diesen-ledger:ritter:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-06-10 | Scott Ritter: Dangerous Endgame in Ukraine: Collapse or Escalation | [https://www.youtube.com/watch?v=MM7sOk8lwZA](https://www.youtube.com/watch?v=MM7sOk8lwZA) | needs capture |
| 2025-06-13 | Scott Ritter: Israel Attacks Iran - Total War Is Expected | [https://www.youtube.com/watch?v=xiLfoG10KxM](https://www.youtube.com/watch?v=xiLfoG10KxM) | needs capture |
| 2025-08-01 | Scott Ritter: Trump-Medvedev Dangerous Nuclear Rhetoric | [https://www.youtube.com/watch?v=Tq5hdFo6mh8](https://www.youtube.com/watch?v=Tq5hdFo6mh8) | needs capture |
| 2025-08-08 | Scott Ritter: Russia Ends Limits on Intermediate-Range Missiles & Changes the Balance of Power | [https://www.youtube.com/watch?v=P8oTXyN9EU8](https://www.youtube.com/watch?v=P8oTXyN9EU8) | needs capture |
| 2025-09-03 | Scott Ritter: NATO & EU Will Collapse After Major Defeat | [https://www.youtube.com/watch?v=W1m-MZUAre4](https://www.youtube.com/watch?v=W1m-MZUAre4) | needs capture |
| 2025-09-17 | Scott Ritter: NATO Prepares for War with Russia | [https://www.youtube.com/watch?v=ShWxrWtCiKI](https://www.youtube.com/watch?v=ShWxrWtCiKI) | needs capture |
| 2025-10-07 | Scott Ritter: Tomahawks, End of NATO & Coming Nuclear War | [https://www.youtube.com/watch?v=mA1vsz5dq7s](https://www.youtube.com/watch?v=mA1vsz5dq7s) | needs capture |
| 2025-10-24 | Scott Ritter: Russia "Fed Up" With NATO Escalations - Retaliation is Coming | [https://www.youtube.com/watch?v=_mupHuF2It4](https://www.youtube.com/watch?v=_mupHuF2It4) | needs capture |
| 2025-12-01 | Scott Ritter: War Has Been Won & Russia Faces a Dilemma | [https://www.youtube.com/watch?v=-7_XtZ64VG4](https://www.youtube.com/watch?v=-7_XtZ64VG4) | needs capture |
| 2025-12-10 | Scott Ritter: The U.S. Now Considers the EU an Enemy | [https://www.youtube.com/watch?v=m_tHqXt44sU](https://www.youtube.com/watch?v=m_tHqXt44sU) | needs capture |
| 2026-01-13 | Scott Ritter: Trump Set Up Putin & Escalates War With Russia | [https://www.youtube.com/watch?v=zH5xP8GSArg](https://www.youtube.com/watch?v=zH5xP8GSArg) | needs capture |
| 2026-01-28 | Scott Ritter: US-Iran War Imminent as Military Buildup Peaks | [https://www.youtube.com/watch?v=rYpPsDXV0o4](https://www.youtube.com/watch?v=rYpPsDXV0o4) | needs capture |
| 2026-02-04 | Scott Ritter: Threat of Nuclear War as the Last Arms Control Treaty Collapsed | [https://www.youtube.com/watch?v=sCgRDO9leIY](https://www.youtube.com/watch?v=sCgRDO9leIY) | needs capture |
| 2026-02-19 | Scott Ritter: U.S. Revives Empire & Europe Is No Longer An Ally | [https://www.youtube.com/watch?v=BCRE6IDTTLI](https://www.youtube.com/watch?v=BCRE6IDTTLI) | needs capture |
| 2026-02-28 | Scott Ritter: Full-Scale War as Iran Attacks All U.S. Targets | [https://www.youtube.com/watch?v=2zjuZqUrCAo](https://www.youtube.com/watch?v=2zjuZqUrCAo) | needs capture |
| 2026-03-11 | Scott Ritter: Trump Calls Putin for Iran War Off-Ramp | [https://www.youtube.com/watch?v=rQt351IzD54](https://www.youtube.com/watch?v=rQt351IzD54) | needs capture |
| 2026-04-08 | Scott Ritter: War Goes Horribly Wrong - U.S. Could Use Nuclear Weapons | [https://www.youtube.com/watch?v=1JScWpTLn1M](https://www.youtube.com/watch?v=1JScWpTLn1M) | needs capture |
| 2026-04-17 | Scott Ritter: Russia Threatens Strike on Finland & Baltic States | [https://www.youtube.com/watch?v=OOLUsj50ZEE](https://www.youtube.com/watch?v=OOLUsj50ZEE) | mirrored |

<!-- diesen-ledger:ritter:end -->

## Macgregor ledger

User-supplied Glenn Diesen / Douglas Macgregor episode URLs added outside the page mirror. Rows are kept here as a separate guest-stream ledger, with mirror status refreshed from `raw-input/`.

<!-- diesen-ledger:macgregor:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-03-29 | Colonel Douglas Macgregor: US & Russia Normalize Relations, Zelensky Opposes Peace | [https://www.youtube.com/watch?v=IWGhXB1uszI](https://www.youtube.com/watch?v=IWGhXB1uszI) | needs capture |
| 2025-06-10 | Douglas Macgregor: Russia's Retaliation & NATO's Declining Relevance | [https://www.youtube.com/watch?v=OsjQZHUvg-M](https://www.youtube.com/watch?v=OsjQZHUvg-M) | needs capture |
| 2025-06-20 | Col. Douglas Macgregor: America's Attack on Iran Could Start WW3 | [https://www.youtube.com/watch?v=wLWXoSI7IFM](https://www.youtube.com/watch?v=wLWXoSI7IFM) | needs capture |
| 2025-07-01 | Douglas Macgregor: America's New Long War | [https://www.youtube.com/watch?v=MpzGp9GH5v4](https://www.youtube.com/watch?v=MpzGp9GH5v4) | needs capture |
| 2025-07-30 | Col. Douglas Macgregor: Fall of the American Empire - A Study in Decadence | [https://www.youtube.com/watch?v=D6MymK54xh4](https://www.youtube.com/watch?v=D6MymK54xh4) | needs capture |
| 2025-08-13 | Douglas Macgregor: Ukraine War Is Over & NATO Exhausted Itself | [https://www.youtube.com/watch?v=l47tdElSfOA](https://www.youtube.com/watch?v=l47tdElSfOA) | needs capture |
| 2025-08-28 | Douglas Macgregor: With NATO's Collapse, New World Order Emerges | [https://www.youtube.com/watch?v=JzHKAIWCqkQ](https://www.youtube.com/watch?v=JzHKAIWCqkQ) | needs capture |
| 2025-09-05 | Douglas Macgregor: Europe on the Edge of War with Russia | [https://www.youtube.com/watch?v=WfW84CrdDHU](https://www.youtube.com/watch?v=WfW84CrdDHU) | needs capture |
| 2025-09-15 | Douglas Macgregor: 500 Years of Dominance Have Come to an End | [https://www.youtube.com/watch?v=I-CT0dn6sDc](https://www.youtube.com/watch?v=I-CT0dn6sDc) | needs capture |
| 2025-09-25 | Douglas Macgregor: "War Is Inevitable" | [https://www.youtube.com/watch?v=k1FkIZaAhHE](https://www.youtube.com/watch?v=k1FkIZaAhHE) | needs capture |
| 2025-10-09 | Toward War with Russia, Iran & Venezuela | [https://www.youtube.com/watch?v=gR6L-R6fVKY](https://www.youtube.com/watch?v=gR6L-R6fVKY) | needs capture |
| 2025-10-23 | Douglas Macgregor: Broken NATO Escalates War on Russia | [https://www.youtube.com/watch?v=dZdnC1btS4M](https://www.youtube.com/watch?v=dZdnC1btS4M) | needs capture |
| 2025-11-04 | Douglas Macgregor: Decline Out of Control - Ukraine and Venezuela Wars | [https://www.youtube.com/watch?v=JffIjn8HbXE](https://www.youtube.com/watch?v=JffIjn8HbXE) | needs capture |
| 2025-11-26 | Douglas Macgregor: NATO Lost the War - Empire of Lies Collapses | [https://www.youtube.com/watch?v=K6yxxQIX-64](https://www.youtube.com/watch?v=K6yxxQIX-64) | needs capture |
| 2025-12-10 | Douglas Macgregor: U.S. Pivoting Away from Ukraine, Europe & NATO | [https://www.youtube.com/watch?v=FW7vyCwyw84](https://www.youtube.com/watch?v=FW7vyCwyw84) | needs capture |
| 2026-01-05 | Douglas Macgregor: War Without Strategy - Venezuela Today, Iran Next | [https://www.youtube.com/watch?v=-VTdtb5O6CY](https://www.youtube.com/watch?v=-VTdtb5O6CY) | needs capture |
| 2026-01-13 | Douglas Macgregor: U.S. War on Iran Risks Triggering World War | [https://www.youtube.com/watch?v=S7ze8RFhqXk](https://www.youtube.com/watch?v=S7ze8RFhqXk) | needs capture |
| 2026-01-22 | Douglas Macgregor: Why NATO is Finished & the Ukraine War Was Lost | [https://www.youtube.com/watch?v=pTpR5hPV2xw](https://www.youtube.com/watch?v=pTpR5hPV2xw) | needs capture |
| 2026-02-04 | Douglas Macgregor: Russia, China & Iran Seek to Contain U.S. Military | [https://www.youtube.com/watch?v=EiWAwoB7ANM](https://www.youtube.com/watch?v=EiWAwoB7ANM) | needs capture |
| 2026-02-27 | Douglas Macgregor: US-Iran Diplomacy Fail - Full-Scale War Coming Soon | [https://www.youtube.com/watch?v=7ic8wLJnC8c](https://www.youtube.com/watch?v=7ic8wLJnC8c) | needs capture |
| 2026-03-03 | Douglas Macgregor: A New World Emerges: Iran Will Win & Israel May Not Survive | [https://www.youtube.com/watch?v=yd_uJiRcl0Q](https://www.youtube.com/watch?v=yd_uJiRcl0Q) | needs capture |
| 2026-04-02 | Douglas Macgregor: Iran War Destroyed NATO, Gulf States, Israel & U.S. Empire | [https://www.youtube.com/watch?v=vBlS-S9AEoY](https://www.youtube.com/watch?v=vBlS-S9AEoY) | needs capture |

<!-- diesen-ledger:macgregor:end -->

## Daniel Davis ledger

User-supplied Glenn Diesen / Daniel Davis episode URLs added outside the page mirror. Rows are kept here as a separate guest-stream ledger, with mirror status refreshed from `raw-input/`.

<!-- diesen-ledger:daniel-davis:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-06-20 | Lt. Col. Daniel Davis: War Against Iran Escalates Unchecked | [https://www.youtube.com/watch?v=SM8JcMwYeEA](https://www.youtube.com/watch?v=SM8JcMwYeEA) | needs capture |
| 2026-01-06 | Daniel Davis: Chaos & More Wars After the Attack on Venezuela | [https://www.youtube.com/watch?v=Fkqd1bJqaCU](https://www.youtube.com/watch?v=Fkqd1bJqaCU) | needs capture |

<!-- diesen-ledger:daniel-davis:end -->

## Max Blumenthal ledger

User-supplied Glenn Diesen / Max Blumenthal episode URLs added outside the page mirror. Rows are kept here as a separate guest-stream ledger, with mirror status refreshed from `raw-input/`.

<!-- diesen-ledger:max-blumenthal:start -->

| pub_date | Title | URL | raw-input |
|----------|-------|-----|-----------|
| 2025-04-09 | Max Blumenthal: Criminalizing Protests Against Israel | [https://www.youtube.com/watch?v=M3RxWoOV82o](https://www.youtube.com/watch?v=M3RxWoOV82o) | needs capture |
| 2025-06-27 | Max Blumenthal: The War Against Iran Is Not Over | [https://www.youtube.com/watch?v=lEulexO9wd0](https://www.youtube.com/watch?v=lEulexO9wd0) | needs capture |
| 2025-07-23 | Max Blumenthal: The Epstein Files & Rise of Anti-Israeli Sentiments in the US | [https://www.youtube.com/watch?v=tMr_dE7KDY0](https://www.youtube.com/watch?v=tMr_dE7KDY0) | needs capture |
| 2026-01-09 | Max Blumenthal: Operation Absolute Resolve, the Kidnapping of Maduro, and the End of International Law | [https://www.youtube.com/watch?v=vKwvQnR1cTw](https://www.youtube.com/watch?v=vKwvQnR1cTw) | needs capture |
| 2026-04-11 | Max Blumenthal: 'Israel First' in Iran War Sparks MAGA Civil War | [https://www.youtube.com/watch?v=TVmTEA9ViNU](https://www.youtube.com/watch?v=TVmTEA9ViNU) | needs capture |

<!-- diesen-ledger:max-blumenthal:end -->

---

**Companion files:** [`strategy-expert-diesen-transcript.md`](strategy-expert-diesen-transcript.md) (7-day rolling verbatim) and [`strategy-expert-diesen-thread.md`](strategy-expert-diesen-thread.md) (distilled analytical thread).
