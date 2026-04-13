# Daily brief — work-politics & work-strategy

**Purpose:** One dated file: **work-politics snapshot** + **work-strategy focus** + **RSS ingest** with **two relevance scores** (W = campaign/KY-4, S = product/governance/tech), then operator synthesis.

**Filename (canonical):** `daily-brief-YYYY-MM-DD.md` in this directory — stem `daily-brief-`, ISO date, `.md` only. Example: `daily-brief-2026-03-29.md`. Do not use other prefixes (e.g. `wap-`) or date formats for dated outputs.

Repository-wide date rules: [date-time-conventions.md](../../date-time-conventions.md).

**Canonical config:** [daily-brief-config.json](daily-brief-config.json)  
**Grok-style post-process layer (headings only — on top of generated §§):** [grok-daily-brief.md](grok-daily-brief.md)  
**Strategy focus bullets:** [daily-brief-focus.md](daily-brief-focus.md)  
**Weak-signal discipline:** [weak-signals.md](weak-signals.md)  
**Weak-signal block template:** [weak-signal-template.md](weak-signal-template.md)  
**Native-language triangulation (international stories):** [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md)

---

## Generate

```bash
python scripts/generate_work_politics_daily_brief.py -u grace-mar \
  -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
```

- Default `--config` resolves to this folder’s `daily-brief-config.json`.
- Legacy: `docs/skill-work/work-politics/daily-brief-feeds.json` if strategy config is missing.
- `--no-fetch` — offline; work-politics + strategy sections still populate from docs/gate.

---

## Sections in the output

| Section | Source |
|---------|--------|
| **1. work-politics snapshot** | `get_wap_snapshot()` |
| **1b. Work-strategy** | [daily-brief-focus.md](daily-brief-focus.md) + pointers to work-dev |
| **1c. Two horizons (fast vs slow)** | Operator prose in generator + [daily-brief-jiang-layer.md](daily-brief-jiang-layer.md) § **Active work-jiang hooks** — **slow** structural pointers (work-jiang); **fast** = §2 RSS + §1 (scored **W / S / G** in generator) |
| **1d. Putin — last 48 hours** | Operator fill per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) + [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md) when Russia is a load-bearing thread |
| **1e. JD Vance — last 48 hours** | Operator fill per [daily-brief-jd-vance-watch.md](daily-brief-jd-vance-watch.md) + [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md) when Iran / third-country talks are load-bearing |
| **1f. Weak signal worth watching** | Operator block using [weak-signal-template.md](weak-signal-template.md); optional “none today” if threshold not met |
| **1g. PRC — last 48 hours** | Operator fill per [daily-brief-prc-watch.md](daily-brief-prc-watch.md) + [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md) when the PRC / Beijing thread is load-bearing |
| **1h. IRI — last 48 hours** | Operator fill per [daily-brief-iran-watch.md](daily-brief-iran-watch.md) + [daily-brief-native-international-pass.md](daily-brief-native-international-pass.md) when the Iran / Islamabad thread is load-bearing; complements [islamabad-operator-index.md](islamabad-operator-index.md) |
| **2. Headlines** | RSS; each line `[W:x S:y]` ranked by **W+S** then recency |
| **3. Lead themes** | **W** campaign angle, **S** strategy angle, **slow** work-jiang stub (tie §1c to today’s headlines) |
| **4. Triangulation** | [work-politics analytical lenses](../work-politics/analytical-lenses/manifest.md) when the lead is political |
| **5–6** | Operator synthesis + work-politics next actions |
| **7** | **Context efficiency (CEL)** — optional footer when `config/context_budgets/daily_brief.json` has `append_cel_footer: true`; links to [context-efficiency-layer.md](../context-efficiency-layer.md), [context-compaction-protocol.md](../context-compaction-protocol.md), `session_brief --compact` |

**Raw X / transcript strategy ingests:** Do **not** duplicate a full ingest list in this file — scratch lives in [strategy-notebook/daily-strategy-inbox.md](strategy-notebook/daily-strategy-inbox.md) (paste-ready one-liner SSOT); fold into `days.md` per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox*.

---

## Weak signal rule

Each brief should include one compact weak-signal block (**§1f**) when a credible candidate exists.

A weak signal should:

- be early
- be incomplete
- matter strategically if true
- remain only low or medium confidence

Do not force an entry on low-information days. Use this line instead:

> No credible weak signal exceeded the threshold today.

When a weak signal includes a historical parallel, complete a short analogy audit using [analogy-audit-template.md](analogy-audit-template.md) and summarize the result inside **§1f**.

---

## Not Voice / not SELF

Complete synthesis in the output file; cite sources; **human sign-off** before client-facing or public ship. See [work-politics consulting-charter](../work-politics/consulting-charter.md).
