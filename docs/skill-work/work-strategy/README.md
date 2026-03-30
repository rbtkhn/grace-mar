# work-strategy

**Purpose:** Cross-territory **operator strategy** — how political consulting ([work-politics](../work-politics/README.md)), integration / portability ([work-dev](../work-dev/README.md)), and other WORK lanes share a single **daily horizon** without mixing into SELF or Voice.

**Not** a replacement for territory READMEs. **Not** Record truth. Companion gate and knowledge boundary rules still apply.

**GitHub / gate CI:** [LANE-CI.md](LANE-CI.md) — label **`lane/work-strategy`**, gate paste convention (`territory: work-politics` + `channel_key: operator:work-strategy` when using the work-politics **`operator:pol:`** channel bucket), paste-snippet CLI.

---

## Contents

| Artifact | Role |
|----------|------|
| **[common-inputs.md](common-inputs.md)** | Shared inputs into work-politics and work-strategy (event ingest, RSS, neutral fact summary, three lenses, gate, operator). |
| **Transcript ingest** | [research/external/work-strategy/transcripts/README.md](../../../research/external/work-strategy/transcripts/README.md) — raw or digest `.md`/`.txt` for Perceiver / current-events / LEARN MODE (not work-jiang lectures). |
| **[external-tech-scan.md](external-tech-scan.md)** | Curated **themes** from long-form tech/business discourse (e.g. GTC, podcasts) — strategy vs work-politics angles; **work-dev integration lens:** [../work-dev/external-signals.md](../work-dev/external-signals.md). **Not** canonical news. |
| **[daily-brief-config.json](daily-brief-config.json)** | Feeds (`locale` per feed) + global + per-locale keyword lists (`pol_keyword_phrases_by_locale`, legacy `wap_keyword_phrases_by_locale`, and `strategy_keyword_phrases_by_locale`) for `generate_work_politics_daily_brief.py` — **W+S** scoring only; no translation API. **`ingest_caps`** + per-feed **`tier`** (1–3) and optional **`max_items`** cap each feed **before** ranking (newest first), so one noisy RSS does not dominate. Optional **`story_dedupe`** clusters headlines that share enough `story_anchor_phrases` overlap (Jaccard + shared anchors) so the same crisis in EN/FR/DE/ES/AR does not flood §2; tune thresholds or pass `--no-story-dedupe` for a flat list. CLI **`--max-per-feed N`** overrides every feed’s cap. |
| **[daily-brief-focus.md](daily-brief-focus.md)** | Operator-maintained bullets: what the strategy lane is watching (product, partners, policy). |
| **[daily-brief-jiang-layer.md](daily-brief-jiang-layer.md)** | **Slow layer** pointers (work-jiang) embedded in the daily brief as **§1c** — compressions, sweep snippets, lecture tracks; not breaking news. |
| **[daily-brief-template.md](daily-brief-template.md)** | Spec for the combined daily brief output. |
| **[current-events-analysis.md](current-events-analysis.md)** | Pipeline: Perceiver → energy-chokepoint hook → Analyst → Triangulation → Synthesis (WORK only). |
| **[STRATEGY.md](STRATEGY.md)** | WORK-only ledger: CORE / SCHOLAR-style heuristics / **WS–MEM** execution log for history & geopolitics; not CMC, not Record. |
| **[LEARN_MODE_RULES.md](LEARN_MODE_RULES.md)** | LEARN MODE adapter: Tri-Frame protocol, extraction format, governance aligned with STRATEGY §VI. |
| **[LEARN_MODE_OPERATOR_PROMPT.md](LEARN_MODE_OPERATOR_PROMPT.md)** | Copy-paste operator / Composer prompt for work-strategy sessions and LEARN MODE. |
| **[minds/](minds/README.md)** | Tri-Frame entry stubs (Mercouris, Mearsheimer, Barnes) → `CIV–MIND–*.md` in civilization_memory. |
| **[manifest-principles.md](manifest-principles.md)** | Operator principles (truth > persuasion, triangulation, energy-chokepoint mandatory, etc.). |
| **[persuasive-content-pipeline.md](persuasive-content-pipeline.md)** | Ingest → energy-chokepoint flags → Council → Triangulation → Draft; staged for approval. |
| **[synthesis-engine.md](synthesis-engine.md)** | Spec for mind-synthesis after three lenses; prototype: `research/prototypes/mind-synthesis.py`. |
| **[multi-agent-fork-generator.md](multi-agent-fork-generator.md)** | Experimental two-pass / subagent richer WORK menus; token budget; human still picks one branch. |
| **[../work-menu-conventions.md](../work-menu-conventions.md)** | Cursor WORK multiple-choice shape (evidence links, tags, choice log to `session-transcript`). |
| **[modules/energy-chokepoint/](modules/energy-chokepoint/manifest.md)** | Energy-chokepoint monitoring (manifest + perceiver-hook); mandatory for energy-related events. |
| **[modules/economic-blowback/](modules/economic-blowback/guardrail-test.md)** | Guardrail checklist for inflation/gas/oil content (everyday impact, CIV-MEM, tone). |
| **[modules/verifiable-personal-ai/](modules/verifiable-personal-ai/manifest.md)** | Operator deliberation receipts — auditable pipeline trace (WORK only; not crypto proof). |

---

## Daily brief

**Output name:** `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (example: `daily-brief-2026-03-29.md`). See [daily-brief-template.md](daily-brief-template.md).

One script covers **work-politics + work-strategy**:

```bash
python scripts/generate_work_politics_daily_brief.py -u grace-mar \
  -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md
```

Default config path: `docs/skill-work/work-strategy/daily-brief-config.json`.

**Ranked morning forks (gate + memory signals):** `python3 scripts/suggest_morning_forks.py -u grace-mar` (see `--markdown`, `--llm`). **Menu evolution:** `python3 scripts/menu_choice_evolution.py -u grace-mar --days 30`.

**Foreign-language feeds:** Each feed may set `"locale": "fr"` (etc.). Phrases in `pol_keyword_phrases_by_locale` (legacy `wap_*`) / `strategy_keyword_phrases_by_locale` are **added** to the global lists when scoring that feed’s items (substring match on the original headline). Non-`en` locales are shown in the headline line (`· _fr_`). Tuning those lists is the **zero-API** way to align ranking with non-English copy; a future optional path could add translated-title scratch for scoring only.

**Ingest volume:** `ingest_caps.default_max_items_per_feed` and `max_items_by_tier` apply when a feed has no explicit `max_items`. Tier **1** = core US/congress feeds; **2** = international language feeds; **3** = long-tail (e.g. HN). Explicit `max_items` on a feed wins over tier.

**Same-story grouping:** After ranking, items can be clustered by anchor overlap on `title + link` (default anchor list in the script; optional `story_anchor_phrases` in JSON extends it). This is **not** semantic dedupe—raise `jaccard_min` / `min_shared_anchors` if clusters feel loose; disable via config `story_dedupe.enabled: false` or CLI `--no-story-dedupe`.

**Operator habit:** Starting Cursor with **“hey”** runs warmup in [.cursor/skills/operator-cadence/SKILL.md](../../.cursor/skills/operator-cadence/SKILL.md) (see bootstrap). **Generating** today's daily brief to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is **hey menu C** — Step 1 does **not** run the generator.

---

## Boundaries

- **WORK only** — drafts, briefs, commercial context.
- **Triangulation** for political copy stays under [work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md).
- **Merge to Record** only via RECURSION-GATE + companion approval.
