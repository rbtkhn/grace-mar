# work-strategy

**Purpose:** Cross-territory **operator strategy** — how political consulting ([work-politics](../work-politics/README.md)), integration / portability ([work-dev](../work-dev/README.md)), and other WORK lanes share a single **daily horizon** without mixing into SELF or Voice.

**Not** a replacement for territory READMEs. **Not** Record truth. Companion gate and knowledge boundary rules still apply.

---

## Contents

| Artifact | Role |
|----------|------|
| **[common-inputs.md](common-inputs.md)** | Shared inputs into work-politics and work-strategy (event ingest, RSS, neutral fact summary, three lenses, gate, operator). |
| **[daily-brief-config.json](daily-brief-config.json)** | Feeds + keyword profiles for `generate_wap_daily_brief.py` (WAP + strategy scores). |
| **[daily-brief-focus.md](daily-brief-focus.md)** | Operator-maintained bullets: what the strategy lane is watching (product, partners, policy). |
| **[daily-brief-template.md](daily-brief-template.md)** | Spec for the combined daily brief output. |
| **[current-events-analysis.md](current-events-analysis.md)** | Pipeline: Perceiver → energy-chokepoint hook → Analyst → Triangulation → Synthesis (WORK only). |
| **[manifest-principles.md](manifest-principles.md)** | Operator principles (truth > persuasion, triangulation, energy-chokepoint mandatory, etc.). |
| **[persuasive-content-pipeline.md](persuasive-content-pipeline.md)** | Ingest → energy-chokepoint flags → Council → Triangulation → Draft; staged for approval. |
| **[synthesis-engine.md](synthesis-engine.md)** | Spec for mind-synthesis after three lenses; prototype: `prototypes/mind-synthesis.py`. |
| **[modules/energy-chokepoint/](modules/energy-chokepoint/manifest.md)** | Energy-chokepoint monitoring (manifest + perceiver-hook); mandatory for energy-related events. |
| **[modules/economic-blowback/](modules/economic-blowback/guardrail-test.md)** | Guardrail checklist for inflation/gas/oil content (everyday impact, CIV-MEM, tone). |
| **[modules/verifiable-personal-ai/](modules/verifiable-personal-ai/manifest.md)** | Operator deliberation receipts — auditable pipeline trace (WORK only; not crypto proof). |

---

## Daily brief

One script covers **work-politics + work-strategy**:

```bash
python scripts/generate_wap_daily_brief.py -u grace-mar \
  -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
```

Default config path: `docs/skill-work/work-strategy/daily-brief-config.json`.

**Operator habit:** Starting Cursor with **“good morning”** is wired in [.cursor/skills/daily-warmup/SKILL.md](../../.cursor/skills/daily-warmup/SKILL.md) and [grace-mar-bootstrap.md](../../grace-mar-bootstrap.md) as the cue to run warmup + **always** generate today's daily brief to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (read-only otherwise until you direct).

---

## Boundaries

- **WORK only** — drafts, briefs, commercial context.
- **Triangulation** for political copy stays under [work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md).
- **Merge to Record** only via RECURSION-GATE + companion approval.
