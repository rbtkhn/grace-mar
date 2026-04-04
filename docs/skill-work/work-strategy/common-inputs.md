# Common inputs — work-politics & work-strategy

**Purpose:** Articulate what feeds **both** [work-politics](../work-politics/README.md) and work-strategy so operator and tooling treat them as one daily horizon with two lenses.

---

## Predictive History — **work-strategy–first** channel corpus

**Primary path:** [youtube-channels/predictive-history/README.md](../../../research/external/youtube-channels/predictive-history/README.md) — `fetch_youtube_channel_transcripts.py`, `index.json`, `transcript_manifest.json`, local `transcripts/*.txt` (often gitignored).

| Use in work-strategy | Point to |
|----------------------|----------|
| **Bulk caption pulls** / video listing | PH README **Generate / refresh** and **`--index-only`** commands |
| **Perceiver / current-events** step 1 | Paste or copy `.txt` into [work-strategy/transcripts/](../../../research/external/work-strategy/transcripts/README.md) as digest `.md`, or analyze in-session from PH path |
| **LEARN MODE** extractions | [LEARN_MODE_RULES.md](LEARN_MODE_RULES.md) + long-form body from PH-derived or work-jiang curated text |
| **Daily brief §1c (slow layer)** | [daily-brief-jiang-layer.md](daily-brief-jiang-layer.md) — **work-jiang** lecture hooks; canonical **curated** lectures live under [work-jiang/lectures/](../../../research/external/work-jiang/lectures/) (often sourced from this channel) |
| **Source registry** | [work-jiang-sources.md](../work-jiang/work-jiang-sources.md) |

**Boundary:** PH is **operator research**, not Record. **work-politics** may **consume** the same intellectual content when surfaced via daily brief §1c or Massie-facing briefs, but the **channel tooling and raw tree** are owned by the **work-strategy / work-jiang** pipeline — not the campaign source registry (contrast [tucker-carlson-book](../../../research/external/youtube-channels/tucker-carlson-book/README.md), which is **work-politics–first**).

---

## Shared inputs (same source, both territories)

| Input | How it reaches both | Notes |
|-------|----------------------|------|
| **Event ingest** | OpenClaw hook, Telegram, manual paste, newsletter | Raw event → [persuasive-content-pipeline](persuasive-content-pipeline.md) step 1; same event can feed work-politics briefs and strategy analysis. |
| **RSS feeds** | [daily-brief-config.json](daily-brief-config.json) — one config, one script | `generate_work_politics_daily_brief.py` fetches the same feeds; each headline is scored for **W** (work-politics) and **S** (strategy). Single run produces one brief with dual scores. |
| **Daily brief output** | One dated file: work-politics snapshot + strategy focus + **§1c** work-jiang hooks + **§1d** Putin watch + **§1e** weak signal + headlines | [daily-brief-template.md](daily-brief-template.md). Snapshot, [daily-brief-focus.md](daily-brief-focus.md), [weak-signals.md](weak-signals.md), and [daily-brief-jiang-layer.md](daily-brief-jiang-layer.md) § Active hooks are **combined** in the same artifact. Optional **jiang_ref** on work-politics gate candidates links ship to research paths ([wap-candidate-template.md](../work-politics/wap-candidate-template.md)). |
| **Neutral fact summary** | Output of Perceiver (and, when relevant, energy-chokepoint hook) | [current-events-analysis](current-events-analysis.md) step 1–1.5. After Analyst, step **2.5** analogy audit applies when a historical parallel is proposed. This summary is the **common input** to the 4-lens Analyst and to the three [analytical lenses](../work-politics/analytical-lenses/manifest.md) in the triangulation stage. Same summary, no lens-specific cherry-picking. |
| **Transcripts (strategy)** | On-disk text under [work-strategy transcripts](../../../research/external/work-strategy/transcripts/README.md) | Optional **upstream** for Perceiver: paste, digest `.md`, or fetched `.txt`. **Default channel bulk pull:** [Predictive History](../../../research/external/youtube-channels/predictive-history/README.md) — see **§ Predictive History** above. Curated lecture book under [work-jiang/lectures/](../../../research/external/work-jiang/lectures/). |
| **Three analytical lenses** | work-politics [analytical-lenses](../work-politics/analytical-lenses/manifest.md) | Structural, operational-diplomatic, institutional-domestic. Used by **both** territories for triangulation; work-strategy runs synthesis after the three minds. |
| **CIV-MEM / governed library** | Lookups and citations | Both pipelines may cite historical precedent (e.g. 1973 embargo); citations do not auto-enter the Record. |
| **RECURSION-GATE** | `users/grace-mar/recursion-gate.md` | Single queue. work-politics candidates use `territory: work-politics` or `channel_key: operator:wap`; strategy uses e.g. `channel_key: operator:work-strategy`. Same gate, same merge script; territory filter for batch review. |
| **Operator / companion** | Human sign-off, approval, synthesis | Final synthesis and any ship decision are human. No autonomous Record merge or public ship. |
| **External tech scan (optional)** | [external-tech-scan.md](external-tech-scan.md); work-dev lens [../work-dev/external-signals.md](../work-dev/external-signals.md) | **Narrative vocabulary** and partner positioning — **not** a fact source for campaign copy or integration specs. Conflicts with headlines / integration-status → prefer cited news and repo truth. |

---

## Territory-specific inputs (only one side)

| Territory | Main context inputs |
|-----------|----------------------|
| **work-politics** | [principal-profile.md](../work-politics/principal-profile.md), [opposition-brief.md](../work-politics/opposition-brief.md), [brief-source-registry.md](../work-politics/brief-source-registry.md), calendar, content-queue, work-politics snapshot logic. |
| **work-strategy** | [daily-brief-focus.md](daily-brief-focus.md), [manifest-principles.md](manifest-principles.md), [modules/energy-chokepoint](modules/energy-chokepoint/manifest.md), [modules/economic-blowback](modules/economic-blowback/guardrail-test.md), **[Predictive History](../../../research/external/youtube-channels/predictive-history/README.md)** (transcript spine — § Predictive History above). |

---

## Flow (common → split)

```
Event / RSS
    → Daily brief run (feeds + W/S scores)
    → Perceiver → neutral fact summary
    → [Energy-chokepoint hook if energy-related]
    → Analyst (4-lens) + Triangulation (3 lenses) on same summary
    → Synthesis draft → staged for approval
    → RECURSION-GATE (work-politics or strategy channel_key)
    → Operator approves → merge or ship (human-only)
```

Same event and same brief can drive **work-politics** deliverables (weekly brief, X copy, opposition tracking) and **strategy** deliverables (positioning, product, governance angles) without duplicating ingest.
