# work-strategy

**Identity (one sentence):** This lane does one thing no other surface does — **cross-territory governed accumulation of judgment** with civilizational depth and explicit distance from Record truth.

**Default path (fast start):** [DEFAULT-PATH.md](DEFAULT-PATH.md) — three moves for a normal pass; everything else is optional. Start there if the full skill file feels heavy.

**Full sequence (SSOT):** [STRATEGY-NOTEBOOK-ARCHITECTURE.md — Default operating path](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#default-operating-path-ssot) — inbox-first numbered path (weave, optional escalation markers, STRATEGY promotion when stable, no Record). **Conductor / cadence → durable notebook anchor:** [CONDUCTOR-IMPROVEMENT-LOOP.md](strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) (optional close template: [CONDUCTOR-CLOSE-TEMPLATE.md](strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md)).

**Strategy run wrapper (optional):** [STRATEGY-RUN-OPERATOR.md](STRATEGY-RUN-OPERATOR.md) — session-scoped `run_id`, derived `state.json` + receipts under `artifacts/`; does not replace or auto-edit notebook files. Shared vocabulary: [run-contract.md](../../run-contract.md).

**Carry harness (optional):** [carry-harness.md](carry-harness.md) — derived JSON receipts for task-level intake → artifact presence checks (`scripts/work_strategy/run_carry_harness.py`); not strategic truth.

**Bottom line:** **`skill-strategy`** is not loose “analysis”; it is **governed strategic accumulation** — preserving an operator’s evolving **geopolitical–historical judgment** in a **bounded WORK layer**, with **explicit seams** (notebook, inbox, `crosses:` / `seam:` / PH overlays), **explicit promotion rules** ([STRATEGY.md](STRATEGY.md), month `meta.md` when arcs stabilize), and **explicit distance** from **identity-facing Record** (MEMORY and WORK continuity are not SELF; the companion gate governs merges — [AGENTS.md](../../../AGENTS.md)).

**Purpose:** Cross-territory **operator strategy** — how political consulting ([work-politics](../work-politics/README.md)), integration / portability ([work-dev](../work-dev/README.md)), and other WORK lanes share a single **daily horizon** without mixing into SELF or Voice. The **[strategy-notebook](strategy-notebook/README.md)** is the **primary** artifact where daily cross-territory judgment is captured; other files here support ingest, frameworks, or optional stitch to [STRATEGY.md](STRATEGY.md).

**Not** a replacement for territory READMEs. **Not** Record truth. Companion gate and knowledge boundary rules still apply.

## Forecast integration

Forecast artifacts from [`docs/skill-work/work-forecast/`](../work-forecast/README.md) may be referenced inside work-strategy as planning inputs.

Allowed uses:

- active watch support
- threshold monitoring
- timing judgments
- decision-point framing

Disallowed uses:

- direct Record updates
- converting a forecast into a fact claim
- bypassing proposal and review workflow

Recommended flow:

1. run forecast
2. save artifact
3. write receipt
4. review summary
5. reference in [forecast-watch-log](strategy-notebook/forecast-watch-log.md) or a [decision point](decision-points/forecast-informed-decision-point-template.md) if useful
6. stage any durable downstream claim separately if needed

**GitHub / gate CI:** [LANE-CI.md](LANE-CI.md) — label **`lane/work-strategy`**, gate paste convention (`territory: work-politics` + `channel_key: operator:work-strategy` when using the work-politics **`operator:pol:`** channel bucket), paste-snippet CLI.

### Cursor skills — disambiguation

| Intended use | Typical trigger | What it does | Primary artifacts / scripts |
|--------------|-----------------|--------------|-----------------------------|
| **Work-politics territory pulse** | _(no skill — run script)_ | Stale docs, brief blockers, gate rhythm, content queue, campaign-facing next actions. | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (legacy: `operator_wap_pulse.py`) |
| **Weekly brief workflow** | `weekly brief` | **Weekly** brief **readiness**, blockers, optional scaffold generation (not the daily generator). | [weekly-brief-run SKILL](../../.cursor/skills/weekly-brief-run/SKILL.md); `operator_weekly_brief_run.py` |
| **Strategy pass** (`skill-strategy`) | **`strategy`**, **`strategy pass`**, **`work-strategy`** | Cross-territory **judgment** slice: **[strategy-notebook/](strategy-notebook/README.md)** first (daily/monthly blocks), then [STRATEGY.md](STRATEGY.md) when promoting watches/log; Islamabad / Rome threads, weak-signal and [analogy-audit](analogy-audit-template.md) flags — **not** the pulse script or weekly brief runner. | [strategy-notebook/](strategy-notebook/README.md), [STRATEGY.md](STRATEGY.md); [skill-strategy SKILL](../../.cursor/skills/skill-strategy/SKILL.md) |

**Coffee** [Compass](../../.cursor/skills/coffee/SKILL.md) (**C**) can include **work-strategy-rome** (ROME-PASS) but is a **session hub**, not a full strategy pass.

### Strategy session helpers (`skill-strategy`)

Quick index for **Capture**-adjacent surfaces: **narrative register**, **Grok-style prose**, **long-arc placement**, and **standing hypothesis logs** — WORK only; weave into knots per [STRATEGY-NOTEBOOK-ARCHITECTURE](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md).

**`strategy-context` (CLI):** Cold-thread re-entry — one bounded paragraph (default **≤120 words**) from notebook `days.md` **Open**, inbox accumulator, `daily-brief-YYYY-MM-DD.md` §1b, STRATEGY + promotion ladder + commentator index presence — or **`--compact`** paths/status only. **`--meta`** adds `chapters/YYYY-MM/meta.md` (month **Theme** excerpt); **`--minds`** adds `minds/README.md` + `minds/outputs` filenames for the date or recent month scaffolds. **`--log`** appends a **`WORK-choice`** receipt to `session-transcript.md` via `log_operator_choice.py` (pointer, not full stdout). **`--recent N`** (or **`--history`** for N=20) appends a **lightweight recent-activity** block after state: merges `users/<id>/strategy-fold-events.jsonl`, **strategy-filtered** `### [WORK-choice]` lines from `session-transcript.md`, and optionally **`--recent-git K`** commits under `docs/skill-work/work-strategy` (merged, sorted by time, truncated to N; omitted if no events). `python3 scripts/strategy_context.py -u grace-mar` · `--date YYYY-MM-DD` · `--max-words N`

**`strategy_thread` (CLI):** Operator **`thread`** — rebuild **`strategy-expert-<expert_id>.md`** rolling ingest blocks from [daily-strategy-inbox.md](strategy-notebook/daily-strategy-inbox.md) lines that carry **`thread:<expert_id>`**; delegates to `strategy_expert_corpus.py` (**same** `--inbox`, `--threads`, `--out`, `--days`, `--today`, `--dry-run`). **Not** a **`weave`** (no `days.md` / knots). Spec: [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Thread (terminology)](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#thread-terminology). `python3 scripts/strategy_thread.py`

| File | Role |
|------|------|
| [grok-daily-brief.md](grok-daily-brief.md) | Headings-only **magazine layer** on top of generated `daily-brief-YYYY-MM-DD.md`. |
| [strategy-notebook/trump-religion-papacy-arc.md](strategy-notebook/trump-religion-papacy-arc.md) | **Trump ↔ Christianity / papacy / religion** arc (anchor 2016→); placement for **Trump–Leo** / **`narrative-escalation`** ingests. |
| [strategy-notebook/rome-persia-legitimacy-signal-check.md](strategy-notebook/rome-persia-legitimacy-signal-check.md) | Append-only **legitimacy-plane** falsifiers (Rome–Tehran wedge); orthogonal to Hormuz/Islamabad **hard security**. |
| [strategy-notebook/narrative-escalation-trump-timeline.md](strategy-notebook/narrative-escalation-trump-timeline.md) | **Stub** — canonical content moved to [trump-religion-papacy-arc.md](strategy-notebook/trump-religion-papacy-arc.md). |
| [skill-strategy / SKILL](../../../.cursor/skills/skill-strategy/SKILL.md) | § **Narrative escalation**, optional **retroactive spine**, **Modes** (Capture / Weave / Promote). |

---

## Contents

| Artifact | Role |
|----------|------|
| **[Strategy session helpers (`skill-strategy`)](#strategy-session-helpers-skill-strategy)** | Compact index subsection **above** (`strategy-context`, **`strategy_thread`** / operator **`thread`**, Grok layer, Trump arc, Rome–Persia signal check, narrative stub, skill-strategy SKILL). |
| **[common-inputs.md](common-inputs.md)** | Shared inputs into work-politics and work-strategy (event ingest, RSS, neutral fact summary, three lenses, gate, operator). |
| **Transcript ingest** | [research/external/work-strategy/transcripts/README.md](../../../research/external/work-strategy/transcripts/README.md) — raw or digest `.md`/`.txt` for Perceiver / current-events / LEARN MODE. **Bulk PH pulls:** [predictive-history/README.md](../../../research/external/youtube-channels/predictive-history/README.md) (work-strategy–first — [common-inputs § PH](common-inputs.md)). |
| **[external-tech-scan.md](external-tech-scan.md)** | Curated **themes** from long-form tech/business discourse (e.g. GTC, podcasts) — strategy vs work-politics angles; **work-dev integration lens:** [../work-dev/external-signals.md](../work-dev/external-signals.md). **Not** canonical news. |
| **[daily-brief-config.json](daily-brief-config.json)** | Feeds (`locale` per feed) + global + per-locale keyword lists (`pol_keyword_phrases_by_locale`, legacy `wap_keyword_phrases_by_locale`, and `strategy_keyword_phrases_by_locale`) for `generate_work_politics_daily_brief.py` — **W+S** scoring only; no translation API. **`ingest_caps`** + per-feed **`tier`** (1–3) and optional **`max_items`** cap each feed **before** ranking (newest first), so one noisy RSS does not dominate. Optional **`story_dedupe`** clusters headlines that share enough `story_anchor_phrases` overlap (Jaccard + shared anchors) so the same crisis in EN/FR/DE/ES/AR does not flood §2; tune thresholds or pass `--no-story-dedupe` for a flat list. CLI **`--max-per-feed N`** overrides every feed’s cap. |
| **[daily-brief-focus.md](daily-brief-focus.md)** | Operator-maintained bullets: what the strategy lane is watching (product, partners, policy). |
| **[daily-brief-native-international-pass.md](daily-brief-native-international-pass.md)** | **Native-language triangulation** for international load-bearing stories (§1d / §1e / §1g / §1h + coffee C); one native bullet per jurisdiction alongside wires. |
| **[daily-brief-jiang-layer.md](daily-brief-jiang-layer.md)** | **Slow layer** pointers (work-jiang) embedded in the daily brief as **§1c** — compressions, sweep snippets, lecture tracks; not breaking news. |
| **[daily-brief-template.md](daily-brief-template.md)** | Spec for the combined daily brief output. |
| **[daily-brief-minds-config.json](daily-brief-minds-config.json)** | Optional Tri-Frame **scaffold** overlays after the daily brief (Barnes / Mearsheimer / Mercouris); strategy-expert **`-mind.md`** paths (SSOT); outputs under [minds/outputs](minds/outputs). See [minds/DAILY-BRIEF-MINDS-WORKFLOW.md](minds/DAILY-BRIEF-MINDS-WORKFLOW.md). |
| **[daily-brief-minds-menu.md](daily-brief-minds-menu.md)** | Human-readable A–D menus per mind (program order B → M → M). |
| **[brief-source-registry.md](brief-source-registry.md)** | Human-readable source-governance layer for work-strategy: 6 source classes, artifact-by-artifact usage policy (§6), corroboration expectations by claim strength (§9), transcript discipline (§10), historical/civilizational use policy (§7), weak-signal source bounds (§11), promotion eligibility (§8). Complements (does not duplicate) the [work-politics weekly-brief registry](../work-politics/brief-source-registry.md). WORK only. |
| **[weak-signals.md](weak-signals.md)** | Weak-signal discipline: **§1f** block, promotion to STRATEGY **§II-A / §III-A / §IV**, analogy audit before overclaiming (WORK only). |
| **[weak-signal-template.md](weak-signal-template.md)** | Markdown stub for **§1f** in the daily brief. |
| **[analogy-audit-template.md](analogy-audit-template.md)** | Short form when a historical parallel is proposed (current-events + brief). |
| **[civilizational-strategy-surface.md](civilizational-strategy-surface.md)** | Thin bridge from civilization_memory to strategy-grade objects: 8 lenses, 12 reusable case families, fit/mismatch/falsifier discipline, promotion targets. WORK only. |
| **[case-index.md](case-index.md)** | Thin local index of reusable strategy-grade historical and civilizational cases (15 initial entries, required template, fit/mismatch/falsifier per case, compression and review protocol). Companion to civilizational-strategy-surface. WORK only. |
| **[decision-point-template.md](decision-point-template.md)** | Structured options when an escalating watch needs a recommendation before promotion. Three-minds perspectives default. |
| **[context-efficiency-layer.md](../context-efficiency-layer.md)** | Cross-lane: hot/warm/cold operator context, recovery links, budgets — pairs with [context-compaction-protocol.md](../context-compaction-protocol.md). |
| **[promotion-ladder.md](promotion-ladder.md)** | 7-stage promotion path for civilizational, historical, and strategy-relevant material into reusable work-strategy artifacts (case hit → resonance note → analogy audit → watch support → decision point → doctrine note → optional gate candidate); shortcut, demotion, and compression rules; minimum reasoning standard. **WORK-only**. |
| **[watch-promotion-rules.md](watch-promotion-rules.md)** | When to promote watches and open decision points. |
| **[decision-points/](decision-points/README.md)** | Instance files (`YYYY-MM-DD-slug.md`). |
| **[promotion-policy.json](promotion-policy.json)** | Machine-readable stage ids (v0). |
| **[authorized-sources.yaml](authorized-sources.yaml)** | Machine-readable source registry: 6 source classes, artifact eligibility per source, trust tiers (1–4), review rules, maintenance policy. 16 sources (primary, data, reporting, analyst, transcript, operator note). Pairs with [brief-source-registry.md](brief-source-registry.md) (human policy) and [work-strategy-sources.md](work-strategy-sources.md) (URL catalog). |
| **[source-tiers.md](source-tiers.md)** | Trust tier meanings + phased enforcement. |
| **[observability.md](observability.md)** | Lane metrics artifact (`artifacts/work-strategy/strategy-observability.json`). |
| **[strategy-health.md](strategy-health.md)** | How to read observability numbers. |
| **[../WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md)** | Full work-layer sequencing (strategy → dev → cadence → dashboard). |
| **[current-events-analysis.md](current-events-analysis.md)** | Standard workflow for converting live events into disciplined strategy judgment: Perceiver (neutral fact summary) → verify seam → event classification → case-index check → energy-chokepoint hook → analyst (structured breakdown) → resonance note or analogy audit → watch-support decision → decision-point trigger → three minds → synthesis → optional deliberation receipt. 11 sections including failure modes and operator checklist. **WORK only**. |
| **[STRATEGY.md](STRATEGY.md)** | WORK-only ledger: CORE / **§II-A active watches** / SCHOLAR / **§III-A analogy watchlist** / **§IV operator strategy log** (additive notes in-file; not CMC `MEM–*` shards); not Record. |
| **[strategy-notebook/](strategy-notebook/README.md)** | **Page-first operator notebook** for strategy judgment — knots are atomic pages; `days.md` = chronology; PH-style month chapters (`chapters/YYYY-MM/`), [architecture](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md), [STATUS](strategy-notebook/STATUS.md); **`### History resonance`** wires [history-notebook](history-notebook/README.md) chapter ids into knots. Not [work-strategy-history](work-strategy-history.md). WORK only. |
| **[theology-notebook/](theology-notebook/README.md)** | **Theology** — define the operator’s own beliefs through **writing** the book; [LIB-0159](../../../users/grace-mar/self-library.md#operator-analytical-books); [research](theology-notebook/research/), [ideas](theology-notebook/ideas/); **not** a substitute for governed Theology entries in `self-library.md`. WORK only. |
| **[strategy-notebook/daily-strategy-inbox.md](strategy-notebook/daily-strategy-inbox.md)** | **SSOT** for **X / strategy ingest** scratch: cadence, **paste-ready one-liner** shape, default assistant target. Weave at **dream** → `days.md` ([architecture](strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox*). |
| **[LEARN_MODE_RULES.md](LEARN_MODE_RULES.md)** | LEARN MODE adapter: Tri-Frame protocol, extraction format, governance aligned with STRATEGY §VI. |
| **[LEARN_MODE_OPERATOR_PROMPT.md](LEARN_MODE_OPERATOR_PROMPT.md)** | Copy-paste operator / Composer prompt for work-strategy sessions and LEARN MODE. |
| **[minds/](minds/README.md)** | Tri-Frame entry stubs (Mercouris, Mearsheimer, Barnes) → `CIV–MIND–*.md` in civilization_memory. Advisory patterns: [minds/MINDS-SKILL-STRATEGY-PATTERNS.md](minds/MINDS-SKILL-STRATEGY-PATTERNS.md). |
| **[manifest-principles.md](manifest-principles.md)** | Operator principles (truth > persuasion, triangulation, energy-chokepoint mandatory, etc.). |
| **[persuasive-content-pipeline.md](persuasive-content-pipeline.md)** | Ingest → energy-chokepoint flags → Council → Triangulation → Draft; staged for approval. |
| **[synthesis-engine.md](synthesis-engine.md)** | Spec for mind-synthesis after three lenses; prototype: `research/prototypes/mind-synthesis.py`. |
| **[multi-agent-fork-generator.md](multi-agent-fork-generator.md)** | Experimental two-pass / subagent richer WORK menus; token budget; human still picks one branch. |
| **[../work-menu-conventions.md](../work-menu-conventions.md)** | Cursor WORK multiple-choice shape (evidence links, tags, choice log to `session-transcript`). |
| **[modules/energy-chokepoint/](modules/energy-chokepoint/manifest.md)** | Energy-chokepoint monitoring (manifest + perceiver-hook); mandatory for energy-related events. |
| **[modules/economic-blowback/](modules/economic-blowback/guardrail-test.md)** | Guardrail checklist for inflation/gas/oil content (everyday impact, CIV-MEM, tone). |
| **[modules/verifiable-personal-ai/](modules/verifiable-personal-ai/manifest.md)** | Operator deliberation receipts — auditable pipeline trace (WORK only; not crypto proof). |
| **[modules/moonshot-orchestration/](modules/moonshot-orchestration/README.md)** | WORK-only moonshot mapping module: source-tier assessment, contribution maps, boundary checks, dashboard entries, and optional gated proposals. Not Record truth; not a canonical skill. |
| **[work-moonshots/](../work-moonshots/README.md)** | **work-moonshots** lane — PMOS templates + [Moonshot Orchestration](../work-moonshots/moonshot-orchestration/README.md) (maps, source tiers, dashboard, optional gated proposals). Not Record. |
| **[work-strategy-rome/](work-strategy-rome/README.md)** | WORK project: Vatican / papal soft power and moral-diplomatic signals vs multipolar and Western-legitimacy themes ([manifest](work-strategy-rome/manifest.md), pre-skill [ROME-PASS](work-strategy-rome/ROME-PASS.md)). |
| **[founding-influences-graeco-roman-vs-english.md](founding-influences-graeco-roman-vs-english.md)** | Working paper: classical-republic vs English constitutional idiom on a 32-unit founding corpus (rubric + lexical methods; `scripts/founding_lexical_compare.py`). Not Record. |
| **[islamabad-operator-index.md](islamabad-operator-index.md)** | **Islamabad bundle — operator index:** single bookmark listing all Islamabad artifacts (this lane + [work-jiang intake](../../../research/external/work-jiang/intake/Islamabad-5-point-reconciliation-plan-with-jiang-commentary.md)). **Not** work-cici. WORK only. |
| **[islamabad-framework.md](islamabad-framework.md)** | **Islamabad Framework** — diplomatic working document (not treaty): six sections, formal register, §6 implementation sequence, dual-audience architecture. WORK only. |
| **[islamabad-framework-summary.md](islamabad-framework-summary.md)** | **Islamabad Framework — summary**: short cover note (~150 words) for social media, email, and channel propagation. Preserves the Leo XIV named reference. WORK only. |
| **[islamabad-framework-operator-edition.md](islamabad-framework-operator-edition.md)** | Same framework — **operator edition**: annexes, Jiang commentary block, Leo XIV rhetoric blend, rubric / phase notes, distribution checklist. See [us-framed-five-point-gulf-peace-framework-2026-04-08.md](us-framed-five-point-gulf-peace-framework-2026-04-08.md) and [work-jiang intake](../../../research/external/work-jiang/intake/Islamabad-5-point-reconciliation-plan-with-jiang-commentary.md). WORK only. |

---

## Daily brief

**Output name:** `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` (example: `daily-brief-2026-03-29.md`). See [daily-brief-template.md](daily-brief-template.md).

**Template SSOT (single source of truth):** [daily-brief-template.md](daily-brief-template.md) is the **authoritative** spec for the combined generator output. [work-politics/daily-brief-template.md](../work-politics/daily-brief-template.md) is a **compatibility pointer** (same content as a stub—do not duplicate the full spec there). [work-template/daily-brief-template.md](../work-template/daily-brief-template.md) is the **cross-lane semantic** scaffold; its numbered mapping points back here.

### Regenerate a dated brief without losing post-process tails

When you have already written a **`## 2c. Narrative layer retrofit`** tail (and optional **`## 8. Quality rubric footer`** bundled after it), use the merge helper so a regen does not erase operator work:

```bash
python3 scripts/merge_daily_brief_postprocess.py -u grace-mar --date YYYY-MM-DD --no-fetch
```

- **`--no-fetch`** is the safer default for “template/config changed, re-render spine” work; omit it only when you intentionally want a fresh RSS pull (expect headline drift vs the original capture day).
- **`--force`** strips any duplicate **`## 2c. Narrative layer retrofit`** tail from the freshly generated base before splicing the preserved post-process material.
- **Tail cleanup (built-in):** if an older brief accidentally folded **`## 3`–`## 7`** stubs after **`## 2c`** (before **`## 8`**), the merge script removes that duplicate outline from the preserved tail and drops a **trailing** duplicate `_Generated by … daily-brief-config.json` signature when present (the regenerated base already emits the signature once before **`## 2c`**).
- Generator detail flag: **`--brief-date YYYY-MM-DD`** on `scripts/generate_work_politics_daily_brief.py` (see [daily-brief-template.md](daily-brief-template.md) **Generate** section).

Portable draft skill: [`skills-portable/_drafts/daily-brief-regen-merge/SKILL.md`](../../skills-portable/_drafts/daily-brief-regen-merge/SKILL.md).

**Brief source registry:** Weekly-brief source readiness is tracked in [work-politics/brief-source-registry.md](../work-politics/brief-source-registry.md) (operator WPC rhythm). The [work-strategy brief-source-registry](brief-source-registry.md) governs how sources are used inside this lane — source classes, artifact-level usage policy, corroboration expectations, transcript discipline, and historical/civilizational use bounds.

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

**Operator habit:** Starting Cursor with **`coffee`** runs warmup in [.cursor/skills/coffee/SKILL.md](../../.cursor/skills/coffee/SKILL.md) (see bootstrap); legacy **`hey`** still works. **Generating** today's daily brief to `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` is **coffee menu C — Strategy (daily brief)** — Step 1 does **not** run the generator.

### Daily brief mind overlays

After `daily-brief-YYYY-MM-DD.md` exists, the operator may run optional **Tri-Frame mind scaffolds** (same generator; **scaffold-only** — no LLM inside the script):

- **Config:** [daily-brief-minds-config.json](daily-brief-minds-config.json)
- **Mind fingerprints (SSOT):** `strategy-expert-barnes-mind.md`, `strategy-expert-mearsheimer-mind.md`, `strategy-expert-mercouris-mind.md` under [`strategy-notebook/`](strategy-notebook/) — [`strategy-notebook/minds/CIV-MIND-*.md`](strategy-notebook/minds/) redirect to the same bodies (see [minds/README.md](minds/README.md))
- **Outputs:** `docs/skill-work/work-strategy/minds/outputs/` — dated sidecar files; complete analysis in Cursor or a **`strategy`** pass
- **CLI:** `scripts/generate_wap_daily_brief.py` — `--offer-minds`, `--mind`, `--mind-option`, `--mind-all`, `--brief-path`, `--skip-brief` (see [minds/DAILY-BRIEF-MINDS-WORKFLOW.md](minds/DAILY-BRIEF-MINDS-WORKFLOW.md))

### X post strategy ingest

Cadence, **paste-ready** micro-format, and default on-disk target for chat ingests: **[strategy-notebook/daily-strategy-inbox.md](strategy-notebook/daily-strategy-inbox.md)** (SSOT). Optional session receipt: [work-menu-conventions § Auditing picks](../work-menu-conventions.md#6-auditing-picks-choice-journal).

---

## Boundaries

- **WORK only** — drafts, briefs, commercial context.
- **Generic pattern library** (tiers, ledger shape, mapping): [work-template/README.md](../work-template/README.md).
- **Triangulation** for political copy stays under [work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md).
- **Merge to Record** only via RECURSION-GATE + companion approval.
