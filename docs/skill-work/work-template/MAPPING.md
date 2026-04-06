# Template ↔ existing lanes

**Purpose:** Map **work-template** concepts to **canonical paths today**. Use this to avoid duplicating standards or blindly copying § numbers from the generic [daily-brief-template.md](daily-brief-template.md).

---

## Concept → lane files

| Template concept | work-strategy | work-politics | work-dev |
|------------------|---------------|---------------|----------|
| **README / lane hub** | [work-strategy/README.md](../work-strategy/README.md) | [work-politics/README.md](../work-politics/README.md) | [work-dev/README.md](../work-dev/README.md) |
| **WORK-LEDGER** | [STRATEGY.md](../work-strategy/STRATEGY.md) (CORE, II-A watches, SCHOLAR, III-A analogy watchlist, §IV operator log) | Distributed: charter, principal-profile, revenue-log, brief registry — no single `WORK-LEDGER.md` | **Primary state:** [workspace.md](../work-dev/workspace.md); compounding story: [three-compounding-loops.md](../work-dev/three-compounding-loops.md). **Optional additive:** [WORK-LEDGER.md](../work-dev/WORK-LEDGER.md) (from [work-template/WORK-LEDGER.md](WORK-LEDGER.md) scaffold) — judgment index + pointers, not integration spec. |
| **Daily horizon / brief** | [daily-brief-template.md](../work-strategy/daily-brief-template.md) + `generate_work_politics_daily_brief.py` | Consumes same brief; snapshot from work-politics docs + §1 | No single dated daily brief; integration status + handback rhythm in workspace |
| **Lane focus** | [daily-brief-focus.md](../work-strategy/daily-brief-focus.md) | [principal-profile.md](../work-politics/principal-profile.md), campaign docs | [workspace.md](../work-dev/workspace.md) priorities |
| **Fast vs slow** | §1c + [daily-brief-jiang-layer.md](../work-strategy/daily-brief-jiang-layer.md); RSS §2 | Same brief §§ | Fast: PRs, incidents; slow: architecture, OpenClaw / template sync |
| **Emerging patterns** | [weak-signals.md](../work-strategy/weak-signals.md), [weak-signal-template.md](../work-strategy/weak-signal-template.md) §1e | Operator-defined (opposition, coalition shifts); no single weak-signals file | Tech / platform shifts in workspace or ADRs (informal) |
| **Framing audit** | [analogy-audit-template.md](../work-strategy/analogy-audit-template.md); [current-events-analysis.md](../work-strategy/current-events-analysis.md) §2.5 | Electoral / institutional precedent when drafting; [civ-mem-draft-protocol.md](../work-politics/civ-mem-draft-protocol.md) for civ-mem copy | Architecture / benchmark comparisons before big bets |
| **Multi-frame review** | Analytical lenses + synthesis: [current-events-analysis.md](../work-strategy/current-events-analysis.md), [synthesis-engine.md](../work-strategy/synthesis-engine.md) | [analytical-lenses/manifest.md](../work-politics/analytical-lenses/manifest.md) — **frame registry** | Product vs architecture vs ops (implicit in reviews; no single manifest) |
| **Background context** | CIV-MEM, work-jiang, [external-tech-scan.md](../work-strategy/external-tech-scan.md) | District, polling, legal calendar — see politics README + [brief-source-registry.md](../work-politics/brief-source-registry.md) | [openclaw-integration.md](../../openclaw-integration.md), export provenance |
| **History log** | [work-strategy-history.md](../work-strategy/work-strategy-history.md) (if present) | [work-politics-history.md](../work-politics/work-politics-history.md) | [work-dev-history.md](../work-dev/work-dev-history.md) |
| **Gate / CI** | [LANE-CI.md](../work-strategy/LANE-CI.md) | work-politics LANE / labels in README | work-dev boundary in README |

### Optional lanes (thin wire)

| Template concept | work-civ-mem | work-coffee |
|------------------|--------------|-------------|
| **Ledger / rhythm** | Stewardship README + external repo workflow | [work-coffee/README.md](../work-coffee/README.md) — cadence **doctrine** |
| **Telemetry** | — | Operator ritual: [work-cadence/work-cadence-events.md](../work-cadence/work-cadence-events.md) (distinct from **lane-cadence.md** in this template) |

---

## work-xavier (advisor module)

Grace-mar **operator/advisor** lane for Xavier (mirrors, BrewMind, runbooks). Not her Record repo; see [work-xavier/README.md](../work-xavier/README.md).

| Template concept | work-xavier path |
|------------------|------------------|
| **README / lane hub** | [work-xavier/README.md](../work-xavier/README.md), [INDEX.md](../work-xavier/INDEX.md) |
| **WORK-LEDGER** | [WORK-LEDGER.md](../work-xavier/WORK-LEDGER.md) + distributed mirror logs: [work-dev-mirror/SYNC-LOG.md](../work-xavier/work-dev-mirror/SYNC-LOG.md), [work-politics-mirror/SYNC-LOG.md](../work-xavier/work-politics-mirror/SYNC-LOG.md) |
| **Daily horizon / brief** | [SYNC-DAILY.md](../work-xavier/SYNC-DAILY.md), [DAILY-OPS-CARD.md](../work-xavier/DAILY-OPS-CARD.md) |
| **Lane focus** | Content plans, KPI logs, [xavier-smm-capability-rubric.md](../work-xavier/xavier-smm-capability-rubric.md); BrewMind hub [brewmind-philippines-onboarding-guide.md](../work-xavier/brewmind-philippines-onboarding-guide.md) |
| **Emerging patterns** | Week plans + rubric vs execution; informal until promoted in WORK-LEDGER II-A |
| **Framing audit** | Not a dedicated file yet; use strategy/politics parent lanes when drafting campaign-adjacent copy |
| **Multi-frame review** | Partial — [LANES.md](../work-xavier/LANES.md) + consumption of work-strategy / work-politics mirrors; no single `frames.md` |
| **Background context** | PH market + operator depth: [work-xavier-sources.md](../work-xavier/work-xavier-sources.md), [work-dev/work-dev-sources.md](../work-dev/work-dev-sources.md) |
| **History log** | [work-xavier-history.md](../work-xavier/work-xavier-history.md) |
| **Gate / CI** | [LANE-CI.md](../work-xavier/LANE-CI.md); label `lane/work-xavier` in [.github/pull_request_template.md](../../../.github/pull_request_template.md) |

---

## work-business (operator ventures)

Business planning, accounting, marketing, and market research for **operator-owned ventures** (Grace Gems, future ventures). Instance-specific to grace-mar; nothing syncs to companion-self.

| Template concept | work-business path |
|------------------|-------------------|
| **README / lane hub** | [work-business/README.md](../work-business/README.md) |
| **WORK-LEDGER** | [WORK-LEDGER.md](../work-business/WORK-LEDGER.md) — watches: ledger staleness, tax prep, marketing plan freshness |
| **Daily horizon / brief** | Not a daily brief lane; summaries via `scripts/business_ledger_summary.py` on demand |
| **Lane focus** | [accounting/README.md](../work-business/accounting/README.md), [marketing/README.md](../work-business/marketing/README.md), [grace-gems/README.md](../work-business/grace-gems/README.md) |
| **Emerging patterns** | Market research docs; informal until promoted in WORK-LEDGER II-A |
| **Background context** | [grace-gems/market-research-and-automation-ideas.md](../work-business/grace-gems/market-research-and-automation-ideas.md), [worldland-decentralized-ai-mainnet-2026-03.md](../work-business/worldland-decentralized-ai-mainnet-2026-03.md) |
| **History log** | [work-business-history.md](../work-business/work-business-history.md) |

---

## Generic daily brief ↔ work-strategy § numbers

The generic [daily-brief-template.md](daily-brief-template.md) uses **semantic headings only** (no `1b` / `1d`). **work-strategy** combined brief uses **fixed numbers** for operator habits (e.g. coffee **C**, Putin watch):

| Semantic block (generic) | work-strategy § (numbered) |
|----------------------------|----------------------------|
| Lane snapshot | **§1** work-politics snapshot |
| Lane focus | **§1b** Work-strategy focus |
| Fast vs slow horizon | **§1c** Two horizons |
| _(lane-specific standing watch)_ | **§1d** Putin — last 48 hours |
| Emerging pattern | **§1e** Weak signal worth watching |
| Inputs / signals | **§2** Headlines (RSS) |
| Lead themes | **§3** |
| Multi-frame review | **§4** Triangulation (when lead is political) |
| Synthesis + next actions | **§5–6** |

**Do not** renumber work-strategy sections without updating the generator ([generate_wap_daily_brief.py](../../../scripts/generate_wap_daily_brief.py)), [daily-brief-putin-watch.md](../work-strategy/daily-brief-putin-watch.md), and coffee docs.

---

## Frame registry rule

- **work-politics:** Lenses live in **one** manifest: [analytical-lenses/manifest.md](../work-politics/analytical-lenses/manifest.md).  
- **work-strategy:** Uses that manifest for triangulation; Tri-Frame / minds under [minds/](../work-strategy/minds/README.md) for LEARN / civ-mem-adjacent work.  
- **New lane:** Add a small `frames.md` or `manifest.md` rather than scattering frame definitions across many files.  

---

**Index:** [work-template README](README.md).
