# Daily brief — work-politics & work-strategy

**Date:** 2026-03-23  
**Assembled:** 2026-03-23 12:11 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 56
- **Work-politics gate:** 0 pending candidate(s)

### Upcoming (from calendar)

- ****Apr 20, 2026**** — **Voter registration deadline** (in-person and mail; mail = postmark) — Push registration in-district; remind supporters.
- ****May 5, 2026**** — Mail-in absentee ballot request portal closes — Voters who need absentee must request by this date.
- ****May 7, 2026**** — **FEC pre-primary report due** — Covers period Apr 1–Apr 29. Registration/certification & overnight mail deadline May 4.
- ****May 19, 2026**** — **Primary election day** — Polls open; final GOTV.

### Territory signals (from docs)

- **research_gap:** Opposition brief still has placeholder sections
- **gate_rhythm:** No live work-politics candidates in RECURSION-GATE
- **brief_readiness:** Weekly brief sources are not fully ready

## 1b. Work-strategy focus

_From `docs/skill-work/work-strategy/daily-brief-focus.md` § Active focus._

- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw ↔ repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs Alpha-style bundles (see [work-alpha-school](../work-alpha-school/README.md), [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) — use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.

_Product / integration context: [work-dev/workspace.md](../work-dev/workspace.md), [work-strategy/README.md](../../work-strategy/README.md)._

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World, BBC News — World, Defense One — All, NPR — national news, NBC News — politics, The Hill — politics, Roll Call — Congress, Le Monde — français (France / monde), Der Spiegel — Deutsch (Schlagzeilen), BBC Mundo — español (Américas / global), France 24 — العربية (MENA), Hacker News — front page._

_No items parsed or all outside recency window._ Try `--max-age-hours` or check feed URLs.

## 3. Lead themes (manual synthesis — 2026-03-23)

_RSS ingest failed for configured feeds (§2); themes below lean on [principal-profile](../work-politics/principal-profile.md), [iran-foreign-policy-brief](../work-politics/iran-foreign-policy-brief.md), [brief-source-registry](../work-politics/brief-source-registry.md), and [integration-status](../work-dev/integration-status.md). Cite external claims before public use._

### Work-politics / campaign angle

- **Clock and compliance:** Primary is **56 days** out (May 19); **Apr 20** registration deadline and **May 7** FEC pre-primary reporting window shape what “urgent” means this month — calendar is the spine; see §1.
- **War powers / Iran on the record:** [iran-foreign-policy-brief](../work-politics/iran-foreign-policy-brief.md) documents the **March 5, 2026** House vote rejecting the Khanna–Massie war-powers resolution (**212–219**) and captures floor messaging (Congress must vote; regional blowback; constitutional line). This is the strongest **documented** national hook tied to the principal’s stated posture.
- **Race dynamics:** [principal-profile](../work-politics/principal-profile.md) already notes Trump’s attacks, Gallrein endorsement, and outside spend; national press (e.g. NPR, **2026-03-17**) reported Trump endorsing the challenger — treat as **live race pressure**, verify quotes and spend numbers against FEC/outlets before hard numbers in client copy.
- **Doc debt:** [opposition-brief](../work-politics/opposition-brief.md) remains **`needs_refresh`** per registry — do not lean on placeholder opposition sections for messaging until refreshed; use profile + Iran brief + live recency pass instead.

### Work-strategy angle (product / governance / tech)

- **Integration facts:** [integration-status](../work-dev/integration-status.md) — OpenClaw export, runtime bundle, stage-only handback, and gate metadata are **`implemented`**; continuity JSONL append and compute-ledger on export remain **partial / documented_only**. Strategy talk should match that table, not aspirational wiring.
- **Vocabulary season:** [external-tech-scan.md](external-tech-scan.md) (refreshed **2026-03-23**) lists enterprise trust, inference economics, agent runtimes, and portable-stack themes for **positioning language** — not as unsourced brief facts. Pair with [work-dev/workspace.md](../work-dev/workspace.md) when describing handback and provenance.
- **Schools / governance:** Active focus (§1b) still points AI-in-schools and identity-substrate narrative vs Alpha-style bundles — no RSS headline today; pull governance items manually when feeds recover or add stable feeds in `daily-brief-config.json`.

## 4. Triangulation (when lead is political)

For **campaign-facing** copy, use [work-politics analytical-lenses](../work-politics/analytical-lenses/template-three-lenses.md) on a shared fact summary.

**Shared fact summary for today:** KY-4 Republican primary on **2026-05-19** with an incumbent facing a **Trump-endorsed** challenger; concurrent national story: **House vote 2026-03-05** on Iran **war powers** (resolution failed; principal on-record per Iran brief).

| Structural | Operational / diplomatic | Institutional |
|---|---|---|
| **Primary calendar + rules** compress the window: registration (**Apr 20**), absentee request close (**May 5**), FEC pre-primary report (**May 7**), then **May 19** — structural “when” beats narrative noise for GOTV and compliance. | **Iran / war powers** is the live operational wedge: March 5 vote outcome and floor quotes are in [iran-foreign-policy-brief](../work-politics/iran-foreign-policy-brief.md); **Trump–Massie** friction and **Gallrein** lane are in [principal-profile](../work-politics/principal-profile.md) — operational story is “national conflict + local primary.” | **House GOP** alignment on the war-powers vote, **Trump/MAGA** spending and endorsements, and **press** framing (national vs NKY) set which voices amplify which facts — institutional before creative. |

**Product / strategy thread:** Treat **staging vs merge** and export receipts ([integration-status](../work-dev/integration-status.md), [openclaw-integration.md](../../openclaw-integration.md)) as the parallel “institutional truth” for work-dev: what is implemented is what you promise externally; the Q1 tech-scan themes are **labeling only** until tied to product milestones.

## 5. Operator synthesis

**Work-politics:** Today’s brief is **light on automated headlines** because RSS failed; the usable through-line is still clear from territory docs: the principal is **on record** on Iran war powers (March 5 vote and quotes in the Iran brief), and the primary is a **Trump-endorsed challenger** race with a hard **April/May** compliance and registration ramp. Priorities: (1) run the registry’s **recency pass** on principal X and one local outlet before shipping campaign copy; (2) **refresh opposition-brief** placeholders before leaning on Gallrein/MAGA lines; (3) keep **Apr 20** registration in front of narrative experiments.

**Work-strategy:** Product and integration messaging should stay anchored to **integration-status** — handback and gate metadata are real; continuity logging and export cost on the ledger are not fully closed. Use **external-tech-scan** for vocabulary and partner conversations, not as cited news. When RSS is fixed or feeds are updated, regenerate this file’s §2–3 so W/S scoring can resume; until then, treat this synthesis as **doc-grounded** and **manually maintained**.

## 6. Next actions (work-politics snapshot)

- Prepare for **Voter registration deadline** (in-person and mail; mail = postmark) on **Apr 20, 2026**.
- Refresh Gallrein, Trump/MAGA, and spending lines before relying on the brief heavily.
- Confirm this is a doc-only week or stage one work-politics milestone so audit continuity stays current.
- Refresh items marked `needs_refresh` in `brief-source-registry.md` before generating the next brief.

---

_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `docs/skill-work/work-strategy/daily-brief-config.json`._
