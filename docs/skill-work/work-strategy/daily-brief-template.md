# Daily brief — work-politics & work-strategy

**Purpose:** One dated file: **work-politics snapshot** + **work-strategy focus** + **RSS ingest** with **two relevance scores** (W = campaign/KY-4, S = product/governance/tech), then operator synthesis.

**Canonical config:** [daily-brief-config.json](daily-brief-config.json)  
**Strategy focus bullets:** [daily-brief-focus.md](daily-brief-focus.md)

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
| **2. Headlines** | RSS; each line `[W:x S:y]` ranked by **W+S** then recency |
| **3. Lead themes** | work-politics-heavy vs strategy-heavy stubs from top titles |
| **4. Triangulation** | [work-politics analytical lenses](../work-politics/analytical-lenses/template-three-lenses.md) when the lead is political |
| **5–6** | Operator synthesis + work-politics next actions |

---

## Not Voice / not SELF

Complete synthesis in the output file; cite sources; **human sign-off** before client-facing or public ship. See [work-politics consulting-charter](../work-politics/consulting-charter.md).
