# Strategy expert predictions (ledger)

**Purpose:** Single **WORK** place to register **falsifiable** claims attributed to indexed **`thread:<expert_id>`** commentators, with **resolution** and **receipts**—notebook calibration, not a public ranking.

**Not:** Record truth, Voice truth, or a competitive **leaderboard** (see [gamification-metrics.md](gamification-metrics.md)). Prefer **sparse** high-quality rows over scoreboard theater; see guardrails in [strategy-commentator-threads.md](strategy-commentator-threads.md) § *Expert threads: predictive accuracy and opinion drift*.

**Related:** [forecast-watch-log.md](forecast-watch-log.md) (forecast **artifacts**, not per-expert rows) · [daily-brief-YYYY-MM-DD.md](../daily-brief-YYYY-MM-DD.md) **`strategy + verify`** · [`.cursor/skills/fact-check/SKILL.md`](../../../.cursor/skills/fact-check/SKILL.md) for tiered verdicts.

---

## Operator calibration (how this file is maintained)

- **Primary surfaces (equal weight):** append **`pred_id` rows** in the prediction table *and* keep the **`topic_slug` registry** accurate as themes evolve (new rows or notes when a bucket becomes load-bearing).
- **Ingest:** capturing claims in [daily-strategy-inbox.md](daily-strategy-inbox.md) first is **recommended** for traceability; **direct edits to this file are allowed** when you already have cite-grade material.
- **Resolution:** when a row moves past `open`, record **`resolution_confidence`** (evidence tier for the closing receipt), not only status text.
- **Automation:** `scripts/validate_expert_predictions.py` checks roster **`expert_id`**s and registry **`topic_slug`**s; CI runs it with other strategy-notebook validators.

---

## Guardrails

- Only claims that are **checkable** against **primaries or twin wires** (not vibes).
- **Conditional** forecasts (`if X then Y`) need **both** legs scored or deferred.
- Distinguish **Bayesian update** from **flip**; new facts may justify revised judgment.
- **Ingest flow:** inbox first when practical; this file holds **canonical adjudication rows** + optional pointers from [`chapters/YYYY-MM/days.md`](chapters/2026-04/days.md) **`### Foresight`**. **Direct rows here are OK** without a prior inbox line when attribution is already solid.

---

## Status vocabulary

Use one of: `open` · `resolved-supported` · `resolved-contradicted` · `resolved-partial` · `deferred-horizon` · `deferred-ambiguous` · `withdrawn` (expert explicitly walks back).

---

## Row template

| Field | Description |
|--------|-------------|
| `pred_id` | Stable slug, grep-friendly, e.g. `pred-2026-04-19-example` |
| `expert_id` | Roster slug from [strategy-commentator-threads.md](strategy-commentator-threads.md) |
| `topic_slug` | One of the **2026 prediction-topic registry** slugs below |
| `stated_claim` | One tight sentence (quote or tight paraphrase + attribution) |
| `source` | URL + optional timestamp; inbox line or `days.md` anchor |
| `date_stated` | ISO date |
| `horizon` | Expected first fair check-in window: **`≤1m`** (~30d) · **`≤1y`** (~12mo) · **`—`** unknown |
| `falsifier` | One sentence: what would make the call wrong |
| `resolution_confidence` | Evidence tier for the **closing** receipt (when not `open`): `wire` · `primary` · `expert-echo` · `unclear` — or `—` while still open |
| `resolution` | Status + date + receipt link(s) when closed |
| `notes` | Seams to other experts, `batch-analysis` keys |

---

## Topic-level falsifiable predictions (multi-expert overlap)

**Use:** One **expert-agnostic** falsifiable statement per row (**≤25 words** in the first column)—what the **world** would have to show for the fork to be wrong—when **two or more** roster commentators have **overlapping** (converging or conflicting) claims in the same week or arc. This is **not** a duplicate ledger: per-expert receipts stay in **Logged rows** below. **Not** checked by `validate_expert_predictions.py` (that script validates **`pred_id`** rows only).

| Falsifiable prediction (topic — ≤25 words; no named expert) | `topic_slug` | Experts who weight this fork (indicative `expert_id`s) | Where to adjudicate (`pred_id` + seams) |
|-------------------------------------------------------------|--------------|--------------------------------------------------------|----------------------------------------|
| **One primary Hormuz regime: open route, Iranian gatekeeping, or executive “open”—not all three without a seam.** | `hormuz-strait` | `davis`, `marandi`, `parsi`, `barnes` | `pred-2026-04-17-davis-hormuz-commercial-ceasefire-route` · `pred-2026-04-17-marandi-hormuz-three-conditions` · `pred-2026-04-18-parsi-hormuz-tehran-decides` · `pred-2026-04-18-barnes-hormuz-not-open-counter-trump`; seam `pred-2026-04-16-marandi-hormuz-no-toll-free` |
| **Pakistan-mediated U.S.–Iran deal closes on a days-to-30–60d calendar from mid-April Beltway reporting.** | `islamabad-us-iran-talks` | `parsi`, `marandi` | `pred-2026-04-17-parsi-pakistan-mediation-window`; same-week BP **Islamabad** authority seam [daily-strategy-inbox.md](daily-strategy-inbox.md) `thread:marandi` **2026-04-16** |
| **Lebanon trends toward durable settlement versus sectarian or civil-war-like violence; wires and map-thesis stay distinct until primaries.** | `lebanon-vs-nuclear-scope` | `pape`, `parsi` | `pred-2026-04-14-pape-lebanon-civil-war-fork` · `pred-2026-04-17-pape-lebanon-power-shift-nyt`; inbox `thread:parsi` Lebanon / TRT / Kent cross-refs **2026-04-17** |
| **Blockade shock lands on named calendar checkpoints (May/Jun-style); not smooth adjustment or moved goalposts.** | `sanctions-energy-oil` | `pape`, `jermy` | `pred-2026-04-16-pape-blockade-shock-calendar`; **`jermy`** when the same fork is ingested with `thread:jermy` + logistics primaries |
| **U.S. executive demands still leave negotiable space for Islamabad talks; not a pure ultimatum that forecloses.** | `escalation-trap-coercion` | `davis`, `pape` | `pred-2026-04-17-davis-trump-ts-maximalist-slams-door`; inbox § **2026-04-16** Pape Janssen **escalation trap** `thread:pape` + `batch-analysis | 2026-04-16 | Pape × Mearsheimer lattice` |
| **Large-scale Iran–Israel shooting resumes soon after ceasefire; not a long ambiguous pause.** | `ceasefire-pause-resumption` | `marandi`, `pape`, `davis` | `pred-2026-04-16-marandi-israel-restart-war-soon`; Pape **Israel as spoiler** / stages [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-16** `thread:pape`; `davis` **resumption clock** lines same arc (add `pred_id` when distilled) |
| **Enriched uranium does not leave Iran under cited Washington–Tehran negotiation authorities.** | `escalation-trap-coercion` | `macgregor`, `pape` | `pred-2026-04-18-macgregor-iran-nsc-no-uranium-out`; Pape Janssen **Vance / uranium** fork same § **2026-04-16** `thread:pape` |

---

## 2026 prediction-topic registry (frequency-informed)

**Method:** Keyword / document-frequency scan across [daily-strategy-inbox.md](daily-strategy-inbox.md), [experts/\*/thread.md](experts/mercouris/thread.md) (**`strategy-page`** blocks), [chapters/2026-04/days.md](chapters/2026-04/days.md), and [meta.md April arc](chapters/2026-04/meta.md). Counts are **indicative** (keyword overlap, not a statistical model). Dense **2026** expert activity in-repo is currently strongest in **2026-04**; extend this registry when other months accumulate comparable ingest volume.

| Order | `topic_slug` | Bucket | Typical falsifiable shape | Often-involved `expert_id` lanes |
|-------|----------------|--------|---------------------------|----------------------------------|
| 1 | `hormuz-strait` | Strait of Hormuz status, transit, closure/reopen, chokepoint leverage | Named strait / blockade / toll / flag-state receipts vs headline | `ritter`, `davis`, `jermy`, `pape`, `johnson`, `marandi`, `mercouris` |
| 2 | `islamabad-us-iran-talks` | Islamabad (or successor venue) negotiation track, MOU, delegation rounds | Scheduled talks / readouts / walk-away vs continuation | `davis`, `freeman`, `parsi`, `mercouris`, `pape`, `marandi` |
| 3 | `ceasefire-pause-resumption` | Ceasefire clock, pause vs resumed strikes, “deal” vs extension | Date-bound ceasefire state + kinetic receipts | `pape`, `davis`, `johnson`, `mercouris`, `marandi` |
| 4 | `naval-blockade-interdiction` | Blockade credibility, interdiction, ORBAT, “porous” vs enforced | AIS / hull / interdiction throughput vs rhetoric | `ritter`, `davis`, `jermy`, `johnson` |
| 5 | `escalation-trap-coercion` | Escalation trap, commitment ratchet, ultimatum geometry | Stated demand sequence + branch outcomes | `pape`, `davis`, `mearsheimer` |
| 6 | `lebanon-vs-nuclear-scope` | Lebanon theater vs nuclear file / EU accountability language | Which fork official rhetoric prioritizes; field vs diplomacy lag | `parsi`, `mercouris`, `mearsheimer`, `blumenthal`, `marandi` |
| 7 | `sanctions-energy-oil` | Sanctions waivers, oil price, SPR, energy macro under war | Policy instrument + market / inventory receipts | `jermy`, `johnson`, `diesen`, `sachs`, `mercouris` |
| 8 | `nato-alliance-europe` | NATO / Article 5 / European theater spillover | Alliance posture statements vs ORBAT / readiness | `johnson`, `ritter`, `mearsheimer`, `macgregor`, `baud` |
| 9 | `war-powers-congress` | U.S. domestic: war powers, authorization, executive vs legislature | Vote / resolution / WH readout chain | `parsi`, `davis`, `barnes` |
| 10 | `multipolar-institutions-dc-process` | Multipolar framing, institutional decay, ExCom vs Truth Social process | Institutional artifact vs personality-driven announcements | `diesen`, `sachs`, `jiang` (PH overlay), `freeman` |

**Optional adjacent slug (not in top-10 density):** `rome-legitimacy` — Rome / papacy / ecumenical seams per [NOTEBOOK-PREFERENCES.md](NOTEBOOK-PREFERENCES.md) grep tags; use when that plane is load-bearing without collapsing into Hormuz/Lebanon mechanics.

### Adding a `topic_slug`

When a recurring falsifiable theme does not fit the table, **append** a new numbered row (next `Order` index), **kebab-case** slug, short **Bucket**, **Typical falsifiable shape**, and **Often-involved** lanes. Then run `python3 scripts/validate_expert_predictions.py` (or rely on CI) so the slug is recognized. **Extended** slugs not in the numbered table must be listed in `EXTENDED_TOPIC_SLUGS` inside `scripts/validate_expert_predictions.py` until promoted into the registry.

---

## Prediction rows (append below)

### Logged rows

| pred_id | expert_id | topic_slug | stated_claim | source | date_stated | horizon | falsifier | resolution_confidence | resolution | notes |
|---------|-----------|------------|--------------|--------|-------------|---------|-----------|----------------------|------------|-------|
| `pred-2026-04-17-davis-hormuz-commercial-ceasefire-route` | `davis` | `ceasefire-pause-resumption` | **Davis** (X, same calendar day) **packages** **IRI FM @araghchi** (~06:45): Hormuz passage **open** for **all commercial vessels** for **remaining ceasefire period** on **PMO coordinated route** (Ports & Maritime Organisation framing). | [daily-strategy-inbox.md](daily-strategy-inbox.md) (`thread:davis` + `IRI+TEHRAN` **2026-04-17**); [days.md §2026-04-17](chapters/2026-04/days.md#2026-04-17) **IRI FM primary** + expert continuity | 2026-04-17 | `≤1m` | Dated primary or wire that commercial passage on the PMO coordinated route **does not** hold for the billed ceasefire remainder in the sense Davis’s packaging asserts. | — | `open` | Same-day **tension** with `thread:marandi` three-condition Hormuz gloss (commercial-only / Iran route control); **seam**, not merge. |
| `pred-2026-04-17-marandi-hormuz-three-conditions` | `marandi` | `hormuz-strait` | **Marandi** (X): Hormuz opening is **not** unrestricted — **commercial ships only**, **Iran** decides which ships pass, transit **only** on **Iran-designated route**. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-17** `thread:marandi`; [assets/marandi/x-2026-04-17-hormuz-three-conditions.png](assets/marandi/x-2026-04-17-hormuz-three-conditions.png) | 2026-04-17 | `≤1m` | Sustained PMO/IRI + field receipts showing **unrestricted** passage with **no** Iranian route control or commercial-only filter as Marandi’s conditions describe. | — | `open` | **Seam** to same-day `thread:davis` Araghchi **open** packaging; not merged. |
| `pred-2026-04-17-davis-trump-ts-maximalist-slams-door` | `davis` | `escalation-trap-coercion` | **Davis** (X): embeds **Trump** Truth Social **~09:57** — reads **maximalist** terms (nuclear reprocessing, no money, Lebanon–Hezbollah seam, Israel barred from bombing Lebanon by USA) as **slamming door** on diplomatic space. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-17** `thread:davis`; `verify:truth-social-primary+embed-chain` | 2026-04-17 | `≤1m` | **Authoritative** subsequent deal text or round **matching** space for Iranian negotiators on those dimensions within the **same** crisis arc Davis treats as foreclosed. | — | `open` | **Dual-register** with §1e executive primary; not a merge with IRI FM line. |
| `pred-2026-04-17-parsi-pakistan-mediation-window` | `parsi` | `islamabad-us-iran-talks` | **Parsi** (X): US–Iran framework reportedly **close** via **Pakistani** mediation **within days**; **30–60** day window to **final** agreement; **Israel** may sabotage. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-17** `thread:parsi` (earlier same-day post) | 2026-04-17 | `≤1m` | **No** dated negotiation readouts or **walk-away** patterns within the Beltway-stated **days / 30–60d** window that support “close within days” as operative (per tiered wires + official where available). | — | `open` | Beltway mechanism tier — not same evidence as **04-16** Marandi BP. |
| `pred-2026-04-18-parsi-hormuz-tehran-decides` | `parsi` | `hormuz-strait` | **Parsi** (X): **Hormuz** “fully open” vs **Trump blockade** **unclear**; **Tehran** shows it **alone** decides strait **open/closed**. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-18** `thread:parsi` | 2026-04-18 | `≤1m` | **Joint** U.S.–flag or published operational regime **contradicting** exclusive Tehran control while claim is live. | — | `open` | **Dual-register** vs maritime primaries; verify shipping tier. |
| `pred-2026-04-14-pape-lebanon-civil-war-fork` | `pape` | `lebanon-vs-nuclear-scope` | **Pape** (X, **2026-04-14** + map): Israel in talks with **Christian & Sunni** Lebanese leadership, **Shia** opposed; trajectory likelier **south Shia cleansing + civil war** than **peace**. | [daily-strategy-inbox.md](daily-strategy-inbox.md) `thread:pape`; wire context **AP 14 Apr** in same inbox subsection | 2026-04-14 | `≤1y` | **Durable** ceasefire + political settlement **without** large-scale sectarian violence along the axis Pape’s map thesis stresses — or authoritative field denial of the **talks composition** claim. | — | `open` | **Seam** to AP Washington talks shell — **separate Judgment objects** until primaries pin. |
| `pred-2026-04-16-pape-blockade-shock-calendar` | `pape` | `sanctions-energy-oil` | **Pape** (Janssen **2026-04-16** transcript): blockade **framework** — price rise → ~**45d** shortages → **60–90d** commodity contraction; names checkpoints **May 1** shortages / **Jun 1** contraction. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **§ Expert ingest — 2026-04-16** `thread:pape`; `verify:operator-transcript+primary-econ-data-needed` | 2026-04-16 | `≤1m` | **Credible** macro / trade / inventory series by those **checkpoint dates** that **fail** the staged-shock shape **without** redefining endpoints. | — | `open` | **Hypothesis-grade** until primaries — do not cite IMF shell claims as proof. |
| `pred-2026-04-17-pape-lebanon-power-shift-nyt` | `pape` | `lebanon-vs-nuclear-scope` | **Pape** (X ~08:07): Israel–Lebanon truce as **signal of shifting global power**; **Iran** demanded end to **Israeli attacks in Lebanon** and **U.S. delivered**; amplifies **NYT Opinion** “major world power” / **4th** card. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-17** `thread:pape` | 2026-04-17 | `≤1m` | **Authoritative** reporting that the **U.S. delivery** / **Iran-demand** causal chain Pape spotlights is **wrong** on the dates, or **NYT** card misread vs full text. | — | `open` | **Op-ed tier** — not independent ORBAT; **homophone** risk vs Janssen **“fourth center”** (different object). |
| `pred-2026-04-16-marandi-israel-restart-war-soon` | `marandi` | `ceasefire-pause-resumption` | **Marandi** (Breaking Points **2026-04-16**): **Israel WILL restart** Iran war; post-ceasefire military prep for next war **“quite soon.”** | [daily-strategy-inbox.md](daily-strategy-inbox.md) **BP** ingest **2026-04-16** `thread:marandi` | 2026-04-16 | `≤1y` | **Extended** window with **no** large-scale **resumed** interstate Iran–Israel **shooting** after the billed prep arc **or** explicit Israeli **stand-down** matching “not soon.” | — | `open` | **Hypothesis-grade** timing word — horizon long. |
| `pred-2026-04-16-marandi-hormuz-no-toll-free` | `marandi` | `hormuz-strait` | **Marandi** (BP **2026-04-16**): **Hormuz**: Iran **retains control**; **no toll-free passage**; Gulf monarchies **complicit**. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **BP** ingest **2026-04-16** `thread:marandi` | 2026-04-16 | `≤1m` | Published **toll-free** or **neutral-flag** toll regime **matching** open-strait commerce **without** Iranian control levers as described. | — | `open` | Same BP stack as Islamabad / restart-war lines. |
| `pred-2026-04-17-ritter-article-5-narrow-read` | `ritter` | `nato-alliance-europe` | **Ritter** (Diesen YT **2026-04-17** episode): **Article 5** **narrow** read — **national** drone programs **≠** **NATO institutional** Article 5 decision; Ramstein “bragging” as proxy-war acknowledgment. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **YT** **2026-04-17** `thread:ritter` (pin canonical URL per inbox) | 2026-04-17 | `≤1y` | **Alliance** institutional **Article 5** invocation + force generation **matching** a **broad** collective-defense read **for the same crisis** Ritter argues is **national-program**-only. | — | `open` | **Europe** theater stack; pair **MoD target list** / **Shoigu** lines in transcript. |
| `pred-2026-04-18-macgregor-iran-nsc-no-uranium-out` | `macgregor` | `escalation-trap-coercion` | **Macgregor** (X): Iran **national security committee** will **not** allow **enriched uranium** transferred **out** of country. | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-18** `thread:macgregor` | 2026-04-18 | `≤1m` | **Verified** transfer / MOU text **executed** moving **stockpile out** consistent with official U.S.–Iran framework claims. | — | `open` | **§1h** nuclear fork; verify **IRI NSC** primary. |
| `pred-2026-04-18-barnes-hormuz-not-open-counter-trump` | `barnes` | `hormuz-strait` | **Barnes** (X): counters **Trump** “reopened **Hormuz**” narrative — **“A few minutes later: the Strait is not open.”** | [daily-strategy-inbox.md](daily-strategy-inbox.md) **2026-04-18** `thread:barnes` | 2026-04-18 | `≤1m` | **Sustained** commercial throughput + **official** U.S./IRI lines **matching** a stable **open** strait story **without** the reversal Barnes highlights. | — | `open` | Domestic **liability** pole on strait narrative; **seam** to maritime primaries. |

_Append further rows above this line; keep one primary `expert_id` per row per [strategy-commentator-threads.md](strategy-commentator-threads.md) pairing rules._
