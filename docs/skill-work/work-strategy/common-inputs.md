# Common inputs — work-politics & work-strategy

**Purpose:** Articulate what feeds **both** [work-politics](../work-politics/README.md) and work-strategy so operator and tooling treat them as one daily horizon with two lenses.

---

## Shared inputs (same source, both territories)

| Input | How it reaches both | Notes |
|-------|----------------------|------|
| **Event ingest** | OpenClaw hook, Telegram, manual paste, newsletter | Raw event → [persuasive-content-pipeline](persuasive-content-pipeline.md) step 1; same event can feed WAP briefs and strategy analysis. |
| **RSS feeds** | [daily-brief-config.json](daily-brief-config.json) — one config, one script | `generate_wap_daily_brief.py` fetches the same feeds; each headline is scored for **W** (WAP) and **S** (strategy). Single run produces one brief with dual scores. |
| **Daily brief output** | One dated file: WAP snapshot + strategy focus + headlines | [daily-brief-template.md](daily-brief-template.md). WAP snapshot (gate, blockers, next actions) and [daily-brief-focus.md](daily-brief-focus.md) bullets are **combined** in the same artifact. |
| **Neutral fact summary** | Output of Perceiver (and, when relevant, energy-chokepoint hook) | [current-events-analysis](current-events-analysis.md) step 1–1.5. This summary is the **common input** to the 4-lens Analyst and to the three [analytical lenses](../work-politics/analytical-lenses/manifest.md) in the triangulation stage. Same summary, no lens-specific cherry-picking. |
| **Three analytical lenses** | work-politics [analytical-lenses](../work-politics/analytical-lenses/manifest.md) | Structural, operational-diplomatic, institutional-domestic. Used by **both** territories for triangulation; work-strategy runs synthesis after the three minds. |
| **CIV-MEM / governed library** | Lookups and citations | Both pipelines may cite historical precedent (e.g. 1973 embargo); citations do not auto-enter the Record. |
| **RECURSION-GATE** | `users/grace-mar/recursion-gate.md` | Single queue. WAP candidates use `territory: work-politics` or `channel_key: operator:wap`; strategy uses e.g. `channel_key: operator:work-strategy`. Same gate, same merge script; territory filter for batch review. |
| **Operator / companion** | Human sign-off, approval, synthesis | Final synthesis and any ship decision are human. No autonomous Record merge or public ship. |

---

## Territory-specific inputs (only one side)

| Territory | Main context inputs |
|-----------|----------------------|
| **work-politics** | [principal-profile.md](../work-politics/principal-profile.md), [opposition-brief.md](../work-politics/opposition-brief.md), [brief-source-registry.md](../work-politics/brief-source-registry.md), calendar, content-queue, WAP snapshot logic. |
| **work-strategy** | [daily-brief-focus.md](daily-brief-focus.md), [manifest-principles.md](manifest-principles.md), [modules/energy-chokepoint](modules/energy-chokepoint/manifest.md), [modules/economic-blowback](modules/economic-blowback/guardrail-test.md). |

---

## Flow (common → split)

```
Event / RSS
    → Daily brief run (feeds + W/S scores)
    → Perceiver → neutral fact summary
    → [Energy-chokepoint hook if energy-related]
    → Analyst (4-lens) + Triangulation (3 lenses) on same summary
    → Synthesis draft → staged for approval
    → RECURSION-GATE (WAP or strategy channel_key)
    → Operator approves → merge or ship (human-only)
```

Same event and same brief can drive **WAP** deliverables (weekly brief, X copy, opposition tracking) and **strategy** deliverables (positioning, product, governance angles) without duplicating ingest.
