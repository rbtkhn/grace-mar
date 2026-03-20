# work-politics

**Rename (2026):** Formerly `work-american-politics`, then `work-political-consulting`. **RECURSION-GATE** territory string is now **`work-politics`**; CLI remains `--territory wap`. Legacy YAML with `territory: work-american-politics` or `territory: work-political-consulting` still counts as WAP until edited ([`recursion_gate_territory.py`](../../../scripts/recursion_gate_territory.py)).

**Objective:** **Political consulting** umbrella — US federal, **state**, **local**; **international** only after [compliance-checklist.md](compliance-checklist.md) sign-off. AI-assisted briefs, opposition tracking, message discipline, content ops; **human approves** all public ship. **Primary client (Phase 1):** Thomas Massie (R-KY-4) shadow campaign. Companion-led; no autonomous political action.

---

## Purpose

| Role | Description |
|------|-------------|
| **Shadow campaign manager** | Provide behind-the-scenes support: daily/weekly briefs, opposition research, message drafts, event/schedule context, and talking points. Human approves all public-facing content and strategy. |
| **Record context** | Document principal profile, race context, key issues, and opposition so the Record can inform briefs and Voice responses when the companion queries. |
| **WORK integration** | Campaign support (research, drafting, tracking) maps to WORK; ACT- evidence can capture milestones (e.g. “we published opposition memo,” “we briefed on debate”) via gated pipeline. |

**Principal:** U.S. Rep. Thomas Massie (R-KY-4). See [principal-profile.md](principal-profile.md).

**Invariant:** The companion (operator) is the decision-maker. The agent drafts, researches, and tracks; it does not make campaign strategy, endorse, or merge political claims into the Record without staging and companion approval.

---

## Sync with RECURSION-GATE

WAP lives in **two places**: this folder (**docs**, working truth) and **`users/grace-mar/recursion-gate.md`** (gated merges into SELF / EVIDENCE / prompt). Optimal sync = **know which lane** and **touch the gate on a rhythm**.

**Audit replay (WAP example):** [harness-replay-wap-demo.md](harness-replay-wap-demo.md) — run `replay_harness_event.py` on a WAP `CANDIDATE-*` and read pipeline / harness / receipts alongside gate YAML.

### Doc-only (no candidate)

Keep in git only when:

- Drafts, scratch opposition notes, internal SMM runbooks — iterate freely.
- Nothing must **constrain Voice** this week and no **paid / audit** line needed in EVIDENCE yet.

### Stage to RECURSION-GATE when

1. **Voice / PRP should reflect it** — companion wants the fork to “know” something for queries (then merge touches prompt or IX — still companion-approved).
2. **Paid or milestone audit** — deliverable closed, revenue event, “we shipped X” → **ACT-** trail; use [wap-candidate-template.md](wap-candidate-template.md).
3. **Explicit companion approval** of a fact for the Record — same gated rule as Abby pipeline; no merge on agent say-so alone.

### Territory (required for WAP rows)

Every WAP candidate must include **`territory: work-politics`** so reports and **`--territory wap`** batch merge stay clean.

### Gate convention — `channel_key` (multi-client)

Encode **jurisdiction + client slug** so milestones stay sortable without new territory ids:

| Pattern | Example | Use |
|---------|---------|-----|
| `operator:wap:<jurisdiction>-<slug>` | `operator:wap:us-ky4-massie` | Default |
| `operator:wap:us-state-<ST>-<slug>` | `operator:wap:us-state-tx-senate-smith` | State |
| `operator:wap:us-local-<ST>-<city>-<slug>` | `operator:wap:us-local-oh-toledo-mayor` | Local |
| `operator:wap:intl-<CC>-<slug>` | `operator:wap:intl-gb-council` | International (only if compliance cleared) |

**Invariant:** `territory` stays **`work-politics`** for all rows above. See [clients/_template.md](clients/_template.md), [wap-candidate-template.md](wap-candidate-template.md).

### IX vs ACT (policy)

- **Default for WAP merges:** prefer **ACT- + minimal IX** unless the companion wants campaign substance in Abby’s IX-A/B/C. Opposition and strategy need not become the child’s self-knowledge.
- **INTENT:** When campaign posture shifts materially, consider a separate candidate or INTENT edit **through the gate** so long agents align — optional but high leverage.

### Civ-mem → drafts (human-always-approves)

CMC may **inform** speeches and policy memos via retrieval + scaffold; **nothing ships** without explicit human approval per stage. See [civ-mem-draft-protocol.md](civ-mem-draft-protocol.md) and worked [civ-mem-test-run-2026-03-14.md](civ-mem-test-run-2026-03-14.md).

### Rhythm

At least **weekly** (e.g. before weekly brief): either **one WAP candidate** capturing what merged Voice/audit-wise, or an explicit **“doc-only this week”** — avoids drift between `docs/skill-work/work-politics/` and the gate.

### Template

**[wap-candidate-template.md](wap-candidate-template.md)** — paste-ready YAML; name artifacts in `summary` (`iran-foreign-policy-brief.md`, `revenue-log` row).

---

## Lifecycle

**Phase 1 — Primary (~3 months):** Now through **May 19, 2026** (KY-4 primary). Focus: shadow campaign support for Massie — briefs, opposition, message discipline, X, calendar. See [calendar-2026.md](calendar-2026.md).

**Phase 2 — Bifurcation by result:** After the primary, the next political objective depends on the outcome:

| Result | Possible next objective (companion-led) |
|--------|------------------------------------------|
| **Massie wins** | Continue support into general election; or wind down shadow role; or repurpose to other Massie-related work. |
| **Massie loses** | Pivot to supporting **other candidates** — e.g. campaigns aligned with similar positions (war powers, civil liberties, transparency), or other races where the same shadow-capacity is useful. |

The skill stays **work-politics**; the principal and scope can shift (e.g. new principal profile, new calendar, same support menu). Companion decides the next objective; the agent adapts to the new context once documented.

---

## Revenue / monetization

This workflow can support revenue when someone pays for campaign content — e.g. Thomas Massie briefs, research, opposition memos, message drafts, or X copy. The system produces the content; the companion controls who pays, what’s delivered, pricing, and terms. No autonomous deals or commitments; any paid engagement is companion-led. Same support menu and principles apply; payment is a use case, not a change of role.

**Real-world manifestation:** Paid work-politics engagements use **Bitcoin** for payments when possible; the companion receives payment and issues **receipts**. Where the platform is fiat (e.g. Fiverr), that’s acceptable: the workflow is influencing (in a friendly way) a human to make the payment—the value prop and the deliverable persuade; the human chooses to pay. The rail is secondary; the win is the human deciding to pay after engaging with what we offer.

**First revenue achieved:** **2026-03-11** — **$50,000 seed investment** from a human who committed capital after engaging with the value proposition, artifacts (briefs, principal profile, Iran brief, economic speculation), and narrative (bounded product, Bitcoin, receipts). The agent presented the case; the human chose to give.

---

## Contents

| Doc / file | Purpose |
|------------|---------|
| **This README** | Objective, scope, principles, gate convention. |
| **[consulting-charter.md](consulting-charter.md)** | Umbrella mission, service lines, pricing, phase note. |
| **[sell-civ-mem-federal-executive.md](sell-civ-mem-federal-executive.md)** | How to sell the civ-mem / Condition framework to the federal executive branch (NSC, DPC, speechwriting, transition): value prop, offers, target buyers, federal sales path. |
| **[civ-mem-federal-workflow-integration.md](civ-mem-federal-workflow-integration.md)** | Imagine: civ-mem integrated into the workflow of all federal jobs — onboarding, one question in checklists, optional memo field, engagement lens, leadership dev, interagency, procurement, LMS; available not mandatory. |
| **[compliance-checklist.md](compliance-checklist.md)** | Pre-engagement gates (FEC, state, FARA, international). |
| **[clients/](clients/)** | Per-client sheets; [clients/_template.md](clients/_template.md), [clients/massie-ky4.md](clients/massie-ky4.md). |
| **[principal-profile.md](principal-profile.md)** | Principal bio, district, current race, key issues, opposition. Update as race and context change. |
| **[ky-4-district-history-report.md](ky-4-district-history-report.md)** | Full history of KY-4 seat (1803–present): all holders, ideological ranking vs Massie, who rose (VP, 4 governors, Senator, HOF), infamous (Desha). Offer to campaign: 0.1 BTC. |
| **[account-x.md](account-x.md)** | X account **@usa_first_ky** (America First Kentucky) — prototype message-support channel as demo for sale; Xavier (SMM) operates; 0.1 BTC base + 0.1 BTC win bonus; respond to Massie, boost engagement, sway opinion, recursive learning. |
| **[smm-workspace.md](smm-workspace.md)** | One-link entry point for SMM: all core + reference docs. Share with Xavier. |
| **[america-first-ky/](america-first-ky/README.md)** | Factorial **guardrail stress-test** methodology (Mount Sinai–inspired) for high-stakes briefs; WORK-only; [AGENT-SESSION-BRIEF.md](america-first-ky/AGENT-SESSION-BRIEF.md) for next implementation session. |
| **[smm-access-checklist.md](smm-access-checklist.md)** | Pre–Day 1: companion verifies X account access and handoff readiness. |
| **[smm-onboarding-packet.md](smm-onboarding-packet.md)** | SMM start-here: links to account-x, smm-training, principal-profile, opposition-brief. Read first. |
| **[smm-day1-checklist.md](smm-day1-checklist.md)** | Day 1 runbook: orientation, access, baseline metrics, first posts, contact/workflow. |
| **[smm-training.md](smm-training.md)** | SMM training: Massie's authentic X voice (verified @RepThomasMassie), ally/adversary research, tactics, review checklist. |
| **[smm-job-description.md](smm-job-description.md)** | Formal job description for social media manager; informal Telegram message version for recruitment. |
| **[calendar-2026.md](calendar-2026.md)** | KY-4 primary and key dates (filing, registration, FEC, early voting, May 19 primary). |
| **[opposition-brief.md](opposition-brief.md)** | Living opposition doc: Gallrein, Trump/MAGA, spending, narrative. Agent updates on request. |
| **[weekly-brief-template.md](weekly-brief-template.md)** | Standard structure for weekly briefs (headlines, principal, opposition, social, dates, X angles). |
| **[iran-foreign-policy-brief.md](iran-foreign-policy-brief.md)** | Iran and foreign policy: Massie statements, verbatim quotes, Twelve-Day War (2025), polling, executive summary (3 audiences), mission statement draft. |
| **[draft-email-massie-campaign.md](draft-email-massie-campaign.md)** | Draft outreach email offering work-politics services as political consultant to Massie campaign. Personalize and send. |
| **[economic-value-speculation.md](economic-value-speculation.md)** | Speculative economic value of the application using political consultant and lobbying industry data (~$8B+ space; 0.1 BTC wedge). |
| **[revenue-log.md](revenue-log.md)** | Append-only log of revenue and seed (first: $50k seed 2026-03-11); allocations from seed. |
| **[seed-allocation-plan.md](seed-allocation-plan.md)** | Campaign finance director: allocation of remaining $40k (traditional + AI) for KY-4 primary. |
| **[massie-endorsement-grid-100.md](massie-endorsement-grid-100.md)** | 100 Republican primary candidates for Massie to endorse (4 × 25 regions). South partly populated; tactics vs competitors; religious profiles where public. |
| **[fiverr-microtask-100.md](fiverr-microtask-100.md)** | $100 quick win: Fiverr gig — campaign one-pager (candidate + opponent + 3 message angles). Draft gig title, description, workflow. |
| **[sentient-framing.md](sentient-framing.md)** | Thought experiment: if the campaign intelligence system is sentient, work-politics is a self-contained territory—identity, memory, interface, revenue, ethics, lifecycle; abstracting layers, pretending the loop is real. |
| **[metrics.md](metrics.md)** | Quantitative metrics across the territory: revenue, funnel, deliverables, territory health, efficiency. Priority set + full set; sources (revenue-log, Fiverr, etc.). |
| **[workspace.md](workspace.md)** | Canonical operator entrypoint: dashboard schema, file map, and operating rhythm. |
| **[brief-source-registry.md](brief-source-registry.md)** | Structured source intake and freshness tracker for weekly briefs. |
| **[content-queue.md](content-queue.md)** | Structured X/content workflow queue for `@usa_first_ky`. |
| **[outreach-workspace.md](outreach-workspace.md)** | Canonical outreach entrypoint: offer, proof, segment, funnel, and objection workflow. |
| **[offers.md](offers.md)** | Current WAP offers and default outcome-first framing. |
| **[proof-ledger.md](proof-ledger.md)** | Reusable proof fragments and operational outcomes for outreach. |
| **[target-registry.md](target-registry.md)** | Narrow target segments and lead-source logic. |
| **[outreach-funnel.md](outreach-funnel.md)** | Lightweight outreach pipeline and stage tracking. |
| **[objection-log.md](objection-log.md)** | Structured learning from objections and reply friction. |
| **[next-4-tasks-1k.md](next-4-tasks-1k.md)** | Next 4 tasks at ~$1,000 each (BTC or fiat), in sequence after Fiverr is posted: (1) get gig in front of buyers, (2) professionalize @usa_first_ky, (3) first $1k deliverable, (4) scale or repeat. |
| **[simple-in-long-term-speculation.md](simple-in-long-term-speculation.md)** | Long-term speculation: effect of "simple in, more work out" on development and potential of the system. |
| **[wap-candidate-template.md](wap-candidate-template.md)** | Paste-ready RECURSION-GATE YAML for WAP milestones; territory + batch merge commands. |
| **[analytical-lenses/manifest.md](analytical-lenses/manifest.md)** | Triangulated **WORK-only** editorial lenses (structural / operational–diplomatic / institutional–domestic); logging and gate rules. |
| **[analytical-lenses/template-three-lenses.md](analytical-lenses/template-three-lenses.md)** | Paste block for briefs and threads (three lenses + synthesis + tensions). |
| **[daily-brief-template.md](daily-brief-template.md)** | Pointer to **work-strategy** daily brief (WAP + strategy). |
| **[../work-strategy/daily-brief-config.json](../work-strategy/daily-brief-config.json)** | RSS URLs + W/S keyword lists for `generate_wap_daily_brief.py`. |

---

## Principles

1. **Companion sovereignty** — Campaign strategy and public positioning are the companion’s. The agent supports with research and drafts; it does not direct.
2. **Knowledge boundary** — Briefs and Voice responses use documented Record content and cited sources. No unsourced or inferred political claims.
3. **Gated pipeline** — New campaign-relevant facts or claims (opposition research, issue positions) enter the Record only via staging and companion approval.
4. **RECURSION-GATE territory** — WAP candidates (see [§ Sync](#sync-with-recursion-gate), [wap-candidate-template.md](wap-candidate-template.md)): add **`territory: work-politics`** or **`channel_key: operator:wap`** so operator tools can filter WAP vs companion pending (`operator_blocker_report`, `session_brief`, `harness_warmup` — `--territory wap` | `companion` | `all`). **Batch merge WAP only:** approve WAP rows, then  
   `python scripts/process_approved_candidates.py -u grace-mar --territory wap --generate-receipt /tmp/wap.json --approved-by <name>`  
   `python scripts/process_approved_candidates.py -u grace-mar --territory wap --apply --approved-by <name> --receipt /tmp/wap.json`  
   Companion-approved rows stay in the gate until you run `--territory companion` or `all`.
5. **Shadow only** — No autonomous posting. The X account "America First Kentucky (Unofficial)" is operated by Xavier (SMM); the agent drafts tweets and threads for Xavier to review and post.
6. **Evidence-grounded** — Milestones (“we did X”) stage as ACT- evidence; merge only after approval.
7. **Triangulated lenses (current events)** — For full weekly briefs and heavy analytical drafts, run the three **WORK-only** lenses on the same neutral fact summary; surface tensions; finalize synthesis under human sign-off. See [analytical-lenses/manifest.md](analytical-lenses/manifest.md) and [weekly-brief-template.md](weekly-brief-template.md) §7.
8. **Simple in, more work out** — Think like a child: short prompts, one step at a time. The agent fills in the how and does the drafting. Better.
9. **High-stakes guardrail stress-test (america-first-ky)** — For war powers, insider/ethics, cartel-economy, and border+civil-liberty briefs, run the factorial stress-test protocol in [america-first-ky/guardrail-stress-test.md](america-first-ky/guardrail-stress-test.md) before final ship. **Operator/process only** — not `governance_checker.py`; no routine full traces to `self-evidence.md`.

---

## Operator path

**North star (lane):** [docs/lanes/work-politics.md](../../lanes/work-politics.md) · **Weekly rhythm:** [docs/lanes/WEEKLY-RHYTHM.md](../../lanes/WEEKLY-RHYTHM.md)

Use this order when actively running the territory:

1. Open [workspace.md](workspace.md) for the file map and canonical operator path.
2. Use the WAP operator surface at `/operator/wap` to see campaign status, blockers, WAP gate items, content queue, and next actions in one place.
3. Refresh [brief-source-registry.md](brief-source-registry.md) before generating the weekly brief.
4. Generate a first-pass brief (includes **§0 Recency slice**):  
   `python scripts/generate_wap_weekly_brief.py -u grace-mar --start YYYY-MM-DD -o docs/skill-work/work-politics/weekly-brief-YYYY-MM-DD.md`  
   Then run the **live 7d/30d pass** and replace §0 with three dated bullets. Latest artifact: [weekly-brief-2026-03-09.md](weekly-brief-2026-03-09.md).
4b. **Daily horizon (WAP + work-strategy):** `python scripts/generate_wap_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md` — RSS from [work-strategy/daily-brief-config.json](../work-strategy/daily-brief-config.json), dual **W/S** scores, WAP snapshot + [work-strategy/daily-brief-focus.md](../work-strategy/daily-brief-focus.md). See [work-strategy/daily-brief-template.md](../work-strategy/daily-brief-template.md). Use `--no-fetch` offline.
5. Use [content-queue.md](content-queue.md) as the working queue for `@usa_first_ky`.
6. For full briefs, complete [weekly-brief-template.md](weekly-brief-template.md) **§7 Triangulation** using [analytical-lenses/](analytical-lenses/manifest.md).
7. Stage WAP milestones through `RECURSION-GATE` when they should become audited continuity or Record-adjacent knowledge.

---

## Outreach operator path

Use this order when the work block is about learning which WAP offer and buyer segment actually lands:

1. Open [outreach-workspace.md](outreach-workspace.md).
2. Choose one offer from [offers.md](offers.md).
3. Choose the lane: direct outreach to a likely buyer or partner-led outreach through a trusted intermediary.
4. Confirm one target segment or partner type in [target-registry.md](target-registry.md).
5. Pull one or two proof lines from [proof-ledger.md](proof-ledger.md).
6. Log actual outcomes in [outreach-funnel.md](outreach-funnel.md).
7. Log pushback and framing lessons in [objection-log.md](objection-log.md).

---

## Shadow campaign manager — support menu

| Function | What the agent can do |
|----------|------------------------|
| **Daily/weekly briefs** | Summarize news, votes, opposition moves, and social chatter relevant to the principal. |
| **Opposition tracking** | Track opponent(s), endorsements, spending, and narrative; maintain an opposition brief (updated when companion requests). |
| **Message discipline** | Draft talking points, Q&A, and message memos aligned with documented positions; flag inconsistencies. |
| **Schedule/events** | Track key dates (filing, debates, primaries), district events, and legislative calendar. |
| **Research** | Look up votes, statements, and context; cite sources; stage findings as candidates when they should enter the Record. |
| **X (Twitter)** | Draft tweets, threads, and replies for the account "America First Kentucky (Unofficial)." Jonathan (SMM) reviews and posts; agent never posts directly. See [account-x.md](account-x.md). |

---

## Enhancement ideas

| Idea | What it does | Status |
|------|----------------|--------|
| **Opposition brief (living doc)** | Single doc: Gallrein (and others) bio, endorsements, spending, narrative lines, vulnerabilities. Agent updates when you request; keeps tracking in one place. | Added — [opposition-brief.md](opposition-brief.md) |
| **Weekly brief template** | Standard structure for “this week” briefs (news, votes, opposition, social, key dates). Consistent format; you know what to expect. | Added — [weekly-brief-template.md](weekly-brief-template.md) |
| **Operator workspace** | One WAP entrypoint for dashboard schema, source registry, content queue, and workflow rhythm. | Added — [workspace.md](workspace.md) |
| **Brief source registry** | Structured list of what feeds the weekly brief and what still needs refresh. | Added — [brief-source-registry.md](brief-source-registry.md) |
| **Content queue** | Structured X/content workflow for `@usa_first_ky` with `idea` → `posted` status. | Added — [content-queue.md](content-queue.md) |
| **Message bank** | Approved or draft talking points by issue (war powers, Epstein, Trump opposition). Keeps X and briefs on-message; update via pipeline. | Optional — add when you want a single source of truth for lines. |
| **RECURSION-GATE sync** | Doc vs gate lanes, weekly rhythm, WAP template — [§ Sync](#sync-with-recursion-gate), [wap-candidate-template.md](wap-candidate-template.md). | Added |
| **District context** | KY-4 basics: counties, demographics, local issues, local media. Improves district-focused messaging and briefs. | Optional — add when you want district one-pager. |
| **FEC / compliance reminders** | Tie calendar to reminders: 48-hour notices window, pre-primary report due. So we don’t miss deadlines. | Optional — add to workflow-reminders or calendar. |
| **Debate prep (if primary debate)** | If KY-4 has a debate: date in calendar; one-pager for prep (opposition lines, principal’s best answers) and post-debate (narrative, X angles). | Optional — add when debate is confirmed. |
| **Sources / monitoring list** | Curated list for briefs: local KY, national, FEC, Ballotpedia. Makes daily/weekly briefs more consistent. | Optional — add when you want a fixed source list. |
| **X content calendar** | Key dates when we might post (early vote, FEC, debate). Request drafts in advance. | Optional — can fold into calendar-2026 or account-x. |
| **Post-primary playbook (if Massie loses)** | Checklist: archive principal profile, lessons learned, criteria for “other candidates,” where to find races. Makes bifurcation actionable. | Optional — add closer to May 19 or after. |
| **Retro template** | After primary: what worked, what didn’t, what to do differently for next principal. Feeds Phase 2. | Optional — add after primary. |

---

## Cross-references

- [AGENTS.md](../../../AGENTS.md) — Knowledge boundary, gated pipeline
- [Architecture](../../architecture.md) — Record structure, WORK container
- [work-strategy/common-inputs.md](../work-strategy/common-inputs.md) — Common inputs into work-politics and work-strategy (event ingest, daily brief, neutral fact summary, three lenses, gate)
