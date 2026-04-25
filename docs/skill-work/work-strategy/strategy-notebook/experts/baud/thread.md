# Expert thread — `baud`

WORK only; not Record.

**Source:** Distilled from [`strategy-expert-baud-transcript.md`](strategy-expert-baud-transcript.md) (what the expert said recently) and relevant pages (where that material was used in strategy work).
**Process:** `python3 scripts/strategy_thread.py` triages inbox → transcript, then fills **only** the **machine layer** between the **strategy-expert-thread** HTML start and end comments. Operator / assistant maintains the **journal layer** above the start marker in **readable prose** (optional **ledger** after the end marker).
**Updated:** Narrative — when you distill; **machine layer** — when you run **`thread`**.
**Companion files:** [`strategy-expert-baud.md`](strategy-expert-baud.md) (profile) and [`strategy-expert-baud-transcript.md`](strategy-expert-baud-transcript.md) (7-day verbatim).

---
## Journal layer — Narrative (operator)

_Write here in full sentences. Dated arcs are welcome (e.g. **2026-04-12 → 04-15**). Cover: what this voice did this week, how it **intersects** named **pages**, convergence/tension with other **`thread:`** experts, and **Open** pins. The **journal layer** is **not** overwritten by the **`thread`** script._

**Layout:** Stay on **one** `strategy-expert-baud-thread.md` file. Within the **journal layer**, each **`## YYYY-MM`** heading is a **month segment**. For **2026:** **Segment 1** = January (`## 2026-01`), **Segment 2** = February (`## 2026-02`), **Segment 3** = March (`## 2026-03`), **Segment 4** = April (`## 2026-04`, ongoing). The **machine layer** (script-maintained) is **only** the fenced block between the **strategy-expert-thread** HTML start and end comments — do not call that "Segment 2" in the month sense.

_(No narrative distillation yet — add prose above the markers, not inside them.)_

**Optional journal-layer extensions (still above the thread start HTML comment):**

- **`## YYYY-MM` month headings** — each heading opens **one month-segment** of the readable journal (quarter-scale or ongoing). **Default:** **at least ~500 words** of **prose** per month-segment (words on non-bullet substantive lines; see `validate_strategy_expert_threads.py`), then optional bullets. A short lede alone is not enough when tooling expects a full segment. Bullet stacks with `[strength: …]` hooks are **compressed ledger** material — fine for lattice discipline — but they **do not** count toward the prose minimum and are **not** an equally canonical substitute for the prose-first journal unless the operator opts into ledger-only months (see HTML comment below). To scaffold prose to the minimum from roster metadata, run `python3 scripts/expand_strategy_expert_segment_prose.py --apply` from repo root.

- **Historical expert context (optional rebuild)** — `python3 scripts/strategy_historical_expert_context.py --expert-id baud --start-segment YYYY-MM --end-segment YYYY-MM --apply` emits batch-analysis handoff under `artifacts/skill-work/work-strategy/historical-expert-context/`: a **range rollup** (`baud-<start>-to-<end>.md`) plus **per-month** files (`baud/<YYYY-MM>.md`). [`strategy_batch_analysis_with_history.py`](../../../../scripts/strategy_batch_analysis_with_history.py) loads **per-month** artifacts when every month in the requested window exists; otherwise it uses the rollup. See `historical-expert-context/README.md` in that folder.

- **`<!-- backfill:baud:start -->` … `end` blocks** — reconstructed historical arc from out-of-repo URLs; not contemporaneous journal prose; keep scope/rules inside the block.

- **Machine hint / opt-out:** `python3 scripts/validate_strategy_expert_threads.py` warns when a `## YYYY-MM` block is heavy on list lines and has **no** prose lines (optional `--month MM` to audit one month only). For a **whole file** where month bullets-only is intentional (transitional ledger), add once in the human layer: `<!-- strategy-expert-thread:segment-1-month-bullets-ledger-ok -->`. Editing assistants: `.cursor/rules/strategy-expert-thread-journal-layer.mdc`.
## 2026-01

January has **no dated** notebook ingest for Baud in this snapshot; the lane stays **NATO / UN / law-of-war vs narrative** — complements ORBAT lanes without duplicating them — per roster.


Finally, 2026-01 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them), **pairing map** (× ritter, × macgregor, × davis, × barnes), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Open pins belong in prose, not only as bullets. For this `baud` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

When historical expert context artifacts exist for `baud` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-01 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Verification stance for Jacques Baud in 2026-01 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.

The 2026-01 segment for the Jacques Baud lane (`baud`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (page cites, transcript rows, or hub URLs) without pretending those pins are already closed.

The `baud` lane’s role (NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Identity anchor:** The Postil + IHL reference instrument (Seed).  
  [thepostil.com](https://www.thepostil.com/) · [OHCHR — IHL instruments](https://www.ohchr.org/en/instruments-mechanisms/instruments/international-humanitarian-law)
## 2026-02

February shows **no indexed Q1 primary** in-repo; use **`ritter`** / **`macgregor`** crosses only with explicit **European mandate / classification** seams.


When historical expert context artifacts exist for `baud` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-02 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-02, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

The 2026-02 segment for the Jacques Baud lane (`baud`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (page cites, transcript rows, or hub URLs) without pretending those pins are already closed.

If pages named this expert during 2026-02, the narrative should eventually say **which page** and **what job** the voice did (pressure, validate, narrate) in plain English. If legacy index lines are still empty, say that plainly too—absence matters for pipeline honesty. The machine block below the marker will populate page references when the index points here; Segment 1 should still record what the operator noticed at human speed before automation catches up.

Open pins belong in prose, not only as bullets. For this `baud` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

The `baud` lane’s role (NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Secondary pointer:** Transcend TMS reprint (Dec 2025 URL in profile) — **not** a February 2026 dated primary; tier-C context only.  
  [Transcend — EU/NATO censorship architecture](https://www.transcend.org/tms/2025/12/baud-and-the-eu-nato-censorship-architecture-%E2%9B%94/)
## 2026-03

March remains **thin** on calendar-facing rows here; treat any third-party “Baud + Iran” index line as **verify-tier** until pinned.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × ritter, × macgregor, × davis, × barnes as the default **short list** of other experts whose fingerprints commonly collide with `baud` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

When historical expert context artifacts exist for `baud` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

Finally, 2026-03 should remain safe for **operator rotation**: someone returning after weeks should be able to read this segment and recover **lane orientation** (role: NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them), **pairing map** (× ritter, × macgregor, × davis, × barnes), and **next verification moves** without loading the entire quarter. That recoverability is why the minimum prose budget exists—not to pad, but to force a minimum coherent account of what this month was for in the notebook.

Typical pairings on file for `baud` emphasize contrast surfaces: × ritter, × macgregor, × davis, × barnes. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-03 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-03, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

Verification stance for Jacques Baud in 2026-03 should stay tier-honest: web-index rows, newsletter dates, and YouTube upload metadata differ in **claim strength**. The notebook uses `[strength: low|medium|high]` precisely because not every cite supports the same inference. Prose here can narrate **what kind of mistake** would happen if a low-strength hook were promoted to a headline judgment—without turning that caution into a substitute for fresh primary checks when the operator needs cite-grade output.


Cross-lane convergence and tension are notebook-native concepts. For 2026-03, read × ritter, × macgregor, × davis, × barnes as the default **short list** of other experts whose fingerprints commonly collide with `baud` on batch passes. Convergence is not friendship; tension is not feud. Both are **pattern labels** for what repeated comparative reading tends to show, subject to update when new evidence changes the shape of disagreement.

When historical expert context artifacts exist for `baud` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-03 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

- [strength: low] **Repeat anchor:** The Postil hub — scope unchanged.
<!-- backfill:baud:start -->
## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `baud` from **2026-01-01** through **2026-04-30** (partial April).
**Status:** Reconstructed summary; no dated primary lines in the Q1 ledger at authoring time.
**Rules:** Hub anchors only where dated captures are missing.

### 2026-01

- **2026-01** — No dated notebook ingest — The Postil hub.  
  _Source:_ web: `https://www.thepostil.com/`

### 2026-02

- **2026-02** — No dated notebook ingest — profile secondary (Dec 2025 article).  
  _Source:_ web: `https://www.transcend.org/tms/2025/12/baud-and-the-eu-nato-censorship-architecture-%E2%9B%94/`

### 2026-03

- **2026-03** — No dated notebook ingest — OHCHR IHL instruments (reference).  
  _Source:_ web: `https://www.ohchr.org/en/instruments-mechanisms/instruments/international-humanitarian-law`


### 2026-04

- **2026-04** — Ledger mirror 1 (partial month).  
  _Source:_ web: `https://www.thepostil.com/`

<!-- backfill:baud:end -->
## 2026-04

_Partial month — no April machine line for Baud in-repo; **NATO / UN / law-of-war** lane — profile Seed hubs only._


The 2026-04 segment for the Jacques Baud lane (`baud`) exists so the notebook keeps a **prose spine** alongside any strength-tagged bullets. The roster describes this voice as centered on NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them. That one-line role is not a substitute for transcript truth; it is a **routing label** so batch-analysis passes know which mechanism vocabulary to expect when dated material lands. When this month is still partial or ingest-light, the prose layer still records **where verification should attach** (page cites, transcript rows, or hub URLs) without pretending those pins are already closed.

Open pins belong in prose, not only as bullets. For this `baud` month segment, explicitly reserve space for **what remains unresolved**: which claims await transcript confirmation, which geopolitical sub-claims depend on translation or primary document access, and which institutional facts are stable enough to reuse in weave scaffolding. That habit keeps later strategy passes from mistaking silence for certainty.

Typical pairings on file for `baud` emphasize contrast surfaces: × ritter, × macgregor, × davis, × barnes. In WORK, those pairings are **operational**: they tell the operator which other `thread:` lanes to open when a claim needs a second fingerprint, not a second opinion dressed as neutrality. This 2026-04 segment should be read as **mesh navigation**—which lanes to pull into the same batch pass—rather than as a claim that those voices agreed or disagreed on any particular day unless a dated bullet below says so explicitly.

Segment discipline here follows the strategy-notebook contract: Segment 1 is human journal prose; Segment 2 is machine extraction. For 2026-04, the point of a long prose block is to prevent the month from collapsing into a **compressed ledger** that *looks* like analysis but is really a hook list. Hooks are valuable; they are also incomplete without the surrounding sentences that say **why** the hook matters for pages, for open pins, or for the next verify pass.

When historical expert context artifacts exist for `baud` (per-month files or rollups under `artifacts/skill-work/work-strategy/historical-expert-context/`), this 2026-04 narrative should be read as **adjacent** to those summaries: the artifact compresses stance for handoff; the thread segment preserves operator-facing **arc and intent**. If the two ever diverge, treat dated ingests and explicit ledger lines as the stricter ground, and use prose to explain tension rather than smoothing it away.

The `baud` lane’s role (NATO / UN / intelligence-adjacent framing: law-of-war, HUMINT vs OSINT limits, European security and cross-theater reads; convergence vs tension between official narrative and evidential claims — complements ORBAT lanes without duplicating them) also implies **failure-mode awareness**: where this voice tends to overread incentives, flatten complexity, or overweight a single domain. This segment is a place to name that risk in calm language when the month’s material invites it, especially before weave work pulls the voice into a page as primary commentator. Naming failure mode is WORK hygiene; it is not an attack on the voice.

- [strength: low] **Identity anchor:** [thepostil.com](https://www.thepostil.com/) — not a dated April posting list.
- [strength: low] **Note:** Use beside **`ritter`** / European mandate seams when **`batch-analysis`** crosses alliance narrative vs evidential limits.

Canonical page paths and raw ingest lines live in **Segment 2** below (regenerated each **`thread`** run).

---
<!-- strategy-expert-thread:start -->
## Machine layer — Extraction (script-maintained)

_Auto-generated from `-transcript.md` + `strategy-page` blocks in this thread + optional empty legacy on-disk index rows. **Journal layer** (narrative) lives **above** the **strategy-expert-thread** start HTML comment. The machine-layer HTML block is replaced on each `thread` run._

### Recent transcript material

## 2026-04-25
- YT | cold: **Daniel Davis** × **Col. Jacques Baud** (*Daniel Davis Deep Dive*) — **Trump** **Fox** **Pakistan-signing** **frame** **vs** **IRI** **no-show** **Islamabad** **(CBS** **wire** **in** **voice);** **carrot–stick** **/** **blackmail** **read;** **ceasefire** **as** **rear** **arm** **(Ukraine** **parallel);** **Strait** **/** **Hormuz** **deterrent;** **UNGA** **3314** **co-belligerent** **(GCC** **territory** **/** **airspace);** **UAE** **FM** **“gulf** **of** **trust”** **vs** **aggression** **facts;** **perfidy** **/** **Geneva** **timing;** **Keane** **blockade** **claims** **vs** **energy** **/** **Bab** **el-Mandeb** **escalation** **geometry;** **Europe** **vassal** **thesis** **(E3** **Mar** **1)** // hook: **`thread:baud`** **law-of-war** **+** **alliance** **mandate** **—** **host** **`thread:davis`**; **full** **verbatim** [raw-input/2026-04-20/davis-deep-dive-baud-iran-pakistan-diplomacy.md](raw-input/2026-04-20/davis-deep-dive-baud-iran-pakistan-diplomacy.md) | https://www.youtube.com/watch?v=TBD-davis-baud-deep-dive | verify:full-text+raw-input+pin-canonical-URL+aired:TBD | thread:baud | grep:Baud+Davis+Pakistan+Hormuz+3314+trust
## 2026-04-20
- YT | cold: **Daniel Davis** × **Col. Jacques Baud** (*Daniel Davis Deep Dive*) — **Trump** **Fox** **Pakistan-signing** **frame** **vs** **IRI** **no-show** **Islamabad** **(CBS** **wire** **in** **voice);** **carrot–stick** **/** **blackmail** **read;** **ceasefire** **as** **rear** **arm** **(Ukraine** **parallel);** **Strait** **/** **Hormuz** **deterrent;** **UNGA** **3314** **co-belligerent** **(GCC** **territory** **/** **airspace);** **UAE** **FM** **“gulf** **of** **trust”** **vs** **aggression** **facts;** **perfidy** **/** **Geneva** **timing;** **Keane** **blockade** **claims** **vs** **energy** **/** **Bab** **el-Mandeb** **escalation** **geometry;** **Europe** **vassal** **thesis** **(E3** **Mar** **1)** // hook: **`thread:baud`** **law-of-war** **+** **alliance** **mandate** **—** **host** **`thread:davis`**; **full** **verbatim** [raw-input/2026-04-20/davis-deep-dive-baud-iran-pakistan-diplomacy.md](raw-input/2026-04-20/davis-deep-dive-baud-iran-pakistan-diplomacy.md) | https://www.youtube.com/watch?v=TBD-davis-baud-deep-dive | verify:full-text+raw-input+pin-canonical-URL+aired:TBD | thread:baud | grep:Baud+Davis+Pakistan+Hormuz+3314+trust
# Daniel Davis Deep Dive — Col. Jacques Baud (US–Iran diplomacy, Pakistan, Hormuz, trust)
Daniel Davis: We are either on the cusp of a major diplomatic breakthrough to end the American-Iranian war, or we're on the cusp of accelerating and escalating it to even more violence—with outcomes that could harm not just the American economy, not just the Iranian or Middle Eastern economies, but the global economy.
There is so much at stake here, and we want to try and parse the truth from the fiction and see if there's room for hope or optimism—or if there's too much pessimism. We need to take a look at that. We're always focused on what is true on the ground, because that is where all the reality lies. To help us make sense of it today, we have back with us Colonel Jacques Baud, former member of the Swiss Strategic Intelligence Service and NATO officer, and author of many books on the Middle East. He's about as knowledgeable as anybody can get. Colonel, welcome back to the show.
Col. Jacques Baud: Thank you very much for inviting me. Happy to be back on the show.
Daniel Davis: Let's jump right into it. President Trump made an interesting statement on Fox News yesterday (Sunday morning) about something he says is supposed to happen tonight. He told Maria Bartiromo that he had just spoken with the president for the third time in a week, and Trump said he is expecting Iran to sign an agreement tomorrow night in Pakistan—and that all items have now been negotiated. However, the president said if they do not sign the deal, the US will blow up every power plant and more in Iran.
Trump told her this should be quick because the negotiation is done. They tried to go back on the deal, but now they are not—and he is expecting Iran to sign the agreement tomorrow night.
Daniel Davis: As I see it, there's one of three things at play here. Either 1) there's been some back-channel stuff that nobody knows about yet, and yay, this war is about to be over. Or 2) he's just claiming this so that he can then make the second part of his threat come through—using it as cover to say "we tried diplomacy" and then go back to war when they don't sign. Or 3) he's just detached from reality and may actually believe some of what he's saying.
How do you see it?
Col. Jacques Baud: I have a different view. It's a complex situation for him because he's cornered right now. He expected a very quick success, but it turned into a quick failure. Now he doesn't know how to get out of this mess, so he's trying different things.
First, as he usually does, it's his "art of the deal"—a carrot-and-stick approach. He says, "Here's an agreement or a proposal, and here's my pistol. If you don't accept the deal, then I shoot." It's closer to blackmail than actual negotiation.
The Iranian Foreign Minister explained what they understand by negotiation. Last time in Islamabad, the discussions lasted just 20-21 hours. The Iranian delegation expected to stay longer, but the Americans just left.
For the Iranians, a discussion means the two parties sit at the table, each with their own proposals, and you talk until you find common ground. You make the proposals converge until you reach an agreement. But that's not how Trump does it. He comes with a proposal and it's "take it or leave it"—and if you leave it, you'll have the "fire and fury" on your head.
Second, since the very beginning of this conflict (and even before), Trump has bragged that he had a deal, that everything was solved, that 100% of the Iranian navy was destroyed. There's a lot of wishful thinking in all of this.
From what I know, there is no real negotiation as such between the US and Iran right now. I'm not sure when Trump says "everything has been settled" that Iran has actually agreed to anything. Maybe he's talking about the 10-point plan proposed by Iran, and the Americans have accepted that—but I don't see that the Iranians have accepted even the first point of the 15-point plan the US proposed about 10 days ago.
Third, the effects on the Strait of Hormuz, international trade, financial markets, and oil markets have been dramatic. So he's obliged to send some positive messages, even if they're not true. That's exactly what he did last week when he said everything was okay and the Strait of Hormuz was open—only to close it himself hours later.
We have three elements here: the personality and psychology of Donald Trump; the actual status of the discussions (which, to my knowledge, are close to zero at this stage); and the need for the US to maintain some stability in the energy market. All of this combines into these allegations and declarations.
So far, I don't see any progress. The Iranians are not keen to engage in further discussions about a ceasefire. They are in exactly the same situation as the Russians in Ukraine: they consider that a ceasefire is only an opportunity for the Israelis and the US to reinforce their positions in the Middle East. Since the Israelis don't respect ceasefires anyway, why should they have one?
Only the US has asked for negotiations. The Iranians proposed a 10-point plan and said, "This is what we want. Period." Now the US is the one demanding negotiations because the US is cornered—not the Iranians.
The Iranians are almost condemned to a decisive victory. If they don't achieve that, the conflict will resume in the coming weeks or months. They want to solve the situation, not just have a pause. I'm not sure Donald Trump has understood that. Probably the intelligence community and a few people around him understand it, but I'm not sure he does.
Daniel Davis: From conversations I had over the weekend, there are people in the intelligence community and his inner circle telling him those kinds of facts. But he is surrounded by other folks who have his ear, and he apparently listens more to them.
That comment he made to Maria Bartiromo yesterday was that we have a deal, we're going to sign it tomorrow night in Pakistan—or we're going to go back to fighting and the bombs are going to start falling. But according to CBS News just moments ago, the Iranian regime has said it has no plans to attend peace talks in Pakistan with Trump's top negotiators (Vance and the others, including possibly Kushner) because they consider the White House demands unrealistic and unreasonable.
So we have two very far-apart visions of diplomacy. I want to get into this because I think Vali Nasr really hit the nail on the head with the "gulf of trust."
Iran thinks it signed a nuclear deal in 2015. The United States took what Iran gave, did not genuinely reciprocate, and then left the deal. President Trump has negotiated with Iran twice and then bombed Iran in the middle of negotiations. So when the Speaker of the Parliament says they want a step-by-step process, he's saying: unlike last time, we don't want to give everything and then have the United States pocket those gains and leave the deal again. Iran also does not trust that Trump will actually implement any deal he signs.
How do you see that?
Col. Jacques Baud: This is exactly it. We can even add the issue of the current ceasefire. The very day they wanted to start the ceasefire, Israel started operations on its own in Lebanon—although Lebanon was apparently part of the deal. So who should you trust?
There's obviously a lack of trust. The US and Israel have each time used negotiations to bring in more weapons and prepare more operations. So what's the point for Iran? They are not the ones demanding a ceasefire. Diplomatically, when you demand a ceasefire, it means you are in the weaker position—and that's where the US is now. Iran knows it.
Even if Iran may suffer from renewed bombing, they have their own "nuclear bomb"—the Strait of Hormuz. It's not a nuclear weapon in the usual sense, but it's their deterrent capability. If they decide to close it permanently or for a long time, it will put the US (and the world economy) in a very difficult situation.
Now you also have more problems between the US and its allies in the region, because those Middle Eastern countries also need the Strait for their oil, aluminum, and other exports. There's no cash coming in for them. That's the power of Iran. Before the war, passage through the Strait was free. The war prompted the Iranians to block it. If Trump wants to reopen it, he needs to resume normal diplomatic—and normal—relations with Iran. They are not ready to do that.
The Iranians don't want to go to Islamabad because they saw last time it was just a waste of time. They don't trust the Americans because they know the US can quit any agreement, as they did with the JCPOA. So what's the point?
The US has trapped itself here.
Daniel Davis: We're going to see just what the cost of that trap has been. On the negative side, today is Memorial Day in Israel, and while Trump is probably trying to use coercion to force a deal, Netanyahu says the job is not yet finished with Iran. He seems to want a military victory. How do you see this contrasting dynamic between supposed allies?
Col. Jacques Baud: First, there's been a lot of discussion in the US about why the US entered this war and the very negative role Israel played. Israel's image has deteriorated dramatically around the world. Nobody sees Israel as a normal state anymore. The aggressiveness, the destruction of whole villages in Lebanon, Gaza—it's extremely negative. Being an ally of Israel doesn't speak in your favor anymore. More and more countries in Europe (Spain, for instance) no longer support Israel.
We may see a similar situation in the US. The problem is that the US is now cornered with no real exit strategy. Instead of trying to find a solution or a middle way, Israel is saying we should go for the full destruction of Iran. That doesn't make any sense. Everybody understands that.
The destruction of Iran seems nearly impossible. The regime has proven much more stable than expected. The bombing of 763 schools and over 300 medical facilities follows the same pattern as in Gaza. That doesn't make Iranians favorable to the US and Israel. Even those who didn't like the government are now joining the national resistance because these war crimes cannot be accepted.
It's extremely poor calculus on the Israeli and US side. We see the same pattern as in Afghanistan or Iraq: nobody knows exactly what the objective is or what the expected result is.
The regime has not changed. The population is now much closer to its government. Iran has been under sanctions for decades, so they are used to living with limited outside connections. They have developed relations with Russia and China, including a huge railroad system for exports and imports. Iran is not weak—it is a very strong country.
If they resume sending missiles to Israel, Israel will pay the price. I'm surprised the Iranians have not yet resumed missile launches against Israel. They are trying to stick to some kind of ceasefire, but if they wanted to, they could probably destroy much of Israel very quickly.
Iran is definitely in the driver's seat. Trump is in a face-saving exercise at this stage.
Daniel Davis: Most people in the world just want this to end diplomatically because of the costs—to Iran, but also to people around the world through loss of fertilizers, petroleum products, etc. It's driving up costs everywhere.
Let's bring some realism to what may be possible. Trump wants a deal right now, but the Iranian side isn't even going to Pakistan. We also have problems with the impression of what diplomacy can do.
Yesterday on ABC News, the UAE Foreign Minister talked about a "der of trust" (gulf of trust). She said trust is earned, and the onus is on Iran to demonstrate they're not going to continue on their current trajectory.
But she didn't mention that the US and Israel launched a war against Iran, and then Iran retaliated against proxies and Gulf countries. Is the ball really in Iran's court?
Col. Jacques Baud: There is UN General Assembly Resolution 3314 from December 1974 that explains exactly who the aggressor is in such a situation: those who started the attack (Israel and the US), and also those who provided their territory or airspace to allow these attacks.
Legally speaking, countries like the UAE, Saudi Arabia, Kuwait, Qatar, Bahrain—all these countries are part of the aggressors. If Iran retaliated against them, it was completely justified from a legal point of view.
Some people tend to forget this. The French Foreign Minister, for example, said Iran attacked the Arab countries in an unjustified way. That's not true—it's perfectly justified. The consequences of having military bases on your territory are serious, especially in wartime.
This is explicitly stated in Resolution 3314: helping an aggressor by providing territory or airspace equates to being an aggressor.
It's a two-way street. The Iranians are also saying: how can we trust you?
Iranian Spokesman (quoted): We certainly cannot forget the very costly experience we had over the past year... The United States on two occasions within less than nine months turned negotiations into a betrayal of diplomacy... We Iranians believe that retesting what has already been tested is a mistake.
Daniel Davis: That shows the two sides remain very far apart. Neither seems in a painful enough position to compromise. The Iranian side seems to be saying: you tried for 40 days and couldn't destroy our government, our long-range missiles, or take control of the Strait of Hormuz. If you want to try again, you're welcome to it—but it won't work the second time either.
If Trump makes good on his threat to destroy every energy facility and more, the Iranian side seems prepared for that too. How do you see it?
Col. Jacques Baud: Coming back to the Iranian spokesman: when you start a war and attack an adversary in the middle of negotiations, that's technically "perfidy"—defined in the Geneva Conventions as a serious war crime. The negotiations in Geneva had prospects, according to the Omani Foreign Minister, but that's precisely when the US and Israel attacked.
How do we expect the Iranians to trust such adversaries?
Yes, the Iranian spokesman is right. The Iranians have been threatened for decades and have prepared accordingly. Their underground missile installations are fantastic—almost like underground cities with highway-like systems under the rock, similar to what Switzerland had during the Cold War. They are built for resilience. You may destroy some launchers, but not the whole system.
Iran cannot reach the US mainland with missiles, but it can reach Israel and US assets in the region. Israel is a tiny country; Iran is huge. While it might be possible to destroy many installations in Iran over time, in the meantime Iran has the ability to destroy Israel 10 or 20 times over in terms of damage.
This is the calculation the US and Israel have to make. They have constantly underestimated Iran's capabilities. This is now the fourth conflict in two years (2024 and 2025), and each time it ended up as a victory for Iran.
Daniel Davis: Retired 4-star General Jack Keane said on TV that we don't need to give Iran anything—they're the ones who need to worry. He said Trump's blockade has stopped 80% of Iran's revenue, and if it continues, the regime will collapse economically. He also said targeting bridges and energy infrastructure is legitimate.
But Trump has threatened to knock out every energy facility and many bridges. Is that a war crime?
Col. Jacques Baud: Yes, absolutely this is a war crime. But the real problem is escalation. Iran can do the same to the whole region. Remember that all those Gulf countries (Kuwait, Qatar, etc.) participated in the aggression, so they are legitimate targets too.
If you destroy Iran's oil installations, Iran may destroy oil and energy facilities across the peninsula. Overnight, Iranian news agencies reported plans to strike targets that would take 32% of global oil supplies offline: the Yanbu pipeline in Saudi Arabia (bypassing Hormuz), the Fujairah facility in the UAE, and complete closure of the Bab al-Mandab Strait by the Houthis.
The Houthis have already tried to disrupt Bab al-Mandab. If both straits are blocked and most Gulf oil facilities are hit, it would be the major oil supply catastrophe in history. The West would suffer much more than Iran.
Iran has been under sanctions for nearly 50 years and has survived. In survival mode, they can probably endure better than our societies.
We're approaching the hot season in the Middle East. Destroying energy supplies would be devastating—think air conditioning, desalination plants (the main source of water for Gulf countries). Without energy, these countries could literally struggle to function.
This would further sink trust toward the US. Having US bases on their territory has become a liability. We may see a complete reshaping of relationships in the Middle East and with the West, and a consolidation of the Eurasian continent with increased Chinese and Russian influence.
China has already played a key diplomatic role (the recent Pakistan ceasefire effort and the Iran-Saudi rapprochement). In the first week of the conflict, every Middle Eastern head of state called Vladimir Putin—not European leaders.
Turkey is contemplating security agreements with Russia and China despite being in NATO. Taiwan's opposition is rethinking its US relationship. Even in Japan, questions about US bases persist.
The trust between the Middle East and the West is crumbling. The US failed to protect these countries, and their early warning systems favored Israel over Arab states.
Daniel Davis: This conflict has consequences for the entire global economy—oil prices, fertilizers, food. The IMF expects food prices to rise around 40%. The West will suffer the most because we are far more dependent on these supplies.
What strikes me is the total absence of Europe in all this discussion. Europe will probably be the most affected continent, yet European diplomacy is dead—there's no reaction, no initiative.
Col. Jacques Baud: Exactly. We talk about the US and Iran, and Russia and China possibly mediating, but nothing from Europe. How will European interests be defended? It's concerning.
Daniel Davis: Do you think European leaders will ever stand up to the US when it's harming their own economies, or will they stay subservient even to their own harm?
Col. Jacques Baud: They are not in a position to do that. They're afraid of the United States. Remember the Greenland issue—they didn't even dare push back. They feel they depend on the US to deal with Russia in Ukraine, so they will never criticize.
Look at the March 1st communiqué from the E3 (France, UK, Germany): they didn't even condemn the US/Israeli attack on Iran—they only condemned Iran's reaction.
The Europeans didn't dare lift sanctions on Iran even when Iran was complying with the JCPOA, because they feared Trump's reaction. From the Iranian point of view, why talk to the "vassal" when you can speak to "God"? (As the French saying goes.)
European diplomacy has no weight anymore in the region. In Lebanon (a former French mandate), France could have mediated, but it's absent. Everything relies on US diplomacy.
There's also a huge discrepancy in Europe between the elite/leadership and the population. That gap is increasing in Germany, France, the UK, etc. But the institutional mechanisms keep the current elite in power. It's very hard for real opposition to gain power.
We saw it in Romania, Hungary—wherever dissenting voices emerge. Even the EU interferes in elections to keep the current leadership, according to a recent US report.
So, for the foreseeable future, I don't see much prospect for change. It's a bit dramatic, but that's the situation.
Daniel Davis: Well, I guess we'll have to wait and see how that works out—as we will with all this. We're so grateful for you coming on today and providing this depth of understanding.
Thank you so much.
Col. Jacques Baud: Thank you for inviting me.
Daniel Davis: And we appreciate you guys too. We'll be back in about an hour. We're going to look at how the Iran war—bombs more likely than talks—as some things have been developing even since we've been on the air here. That makes restarting the war more likely than bringing it to an end. We'll talk about some of that this afternoon.
See you then on the Daniel Davis Deep Dive.
<!-- strategy-expert-thread:end -->
