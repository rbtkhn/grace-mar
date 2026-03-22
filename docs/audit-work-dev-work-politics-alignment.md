# Audit: work-dev and work-politics alignment

**Date:** 2026-03-18  
**Scope:** Governance, structure, RECURSION-GATE usage, operator paths, cross-references, and gaps between `docs/skill-work/work-dev/` and `docs/skill-work/work-politics/` (work-politics territory).

---

## 1. Governance alignment

| Dimension | work-dev | work-politics | Aligned? |
|-----------|----------|----------------------------------|-----------|
| **Companion sovereignty** | Merge authority stays with companion; OpenClaw stages, companion approves. | Campaign strategy and public positioning are companion’s; agent supports with research/drafts, does not direct. | ✅ Yes |
| **Knowledge boundary** | Voice uses only documented Record; no LLM inference into identity. | Briefs and Voice use documented Record and cited sources; no unsourced political claims. | ✅ Yes |
| **Gated pipeline** | Stage-only automation; no merge into SELF/EVIDENCE/prompt without approval. | New campaign-relevant facts enter Record only via staging and companion approval. | ✅ Yes |
| **Invariant wording** | “OpenClaw or downstream systems must never become control-grid infrastructure.” | “The agent drafts, researches, tracks; it does not make campaign strategy, endorse, or merge … without staging and companion approval.” | ✅ Same spirit |
| **Evidence / ACT** | Handback → stage → companion approves → merge → ACT-* + IX. | Milestones (“we did X”) stage as ACT- evidence; merge only after approval. | ✅ Yes |

**Verdict:** Governance is aligned. Both territories enforce companion-as-gate, no autonomous merge, and evidence-through-pipeline.

---

## 2. Structure alignment

| Element | work-dev | work-politics | Gap / note |
|---------|----------|-----|------------|
| **README** | Objective, Purpose table, Invariant, Contents table, Principles (7), Quick ref (CLI), Operator path, Business path, Cross-refs. | Objective, Purpose table, Principal, Invariant, **§ Sync with RECURSION-GATE** (doc-only vs stage, territory, channel_key, IX vs ACT, civ-mem, rhythm, template), Lifecycle, Revenue, Contents table, Principles (7), Operator path, **Outreach operator path**, Support menu, Enhancement ideas, Cross-refs. | work-politics has explicit **gate sync** and **outreach** lanes; work-dev has **integration-status** and **provenance** focus. Structure is intentionally different by domain. |
| **workspace.md** | Current state summary, canonical files, operator path, business layer (3 lanes), blockers, next actions. | Dashboard schema (campaign, clients, compliance, gate items, brief readiness, content queue, revenue, outreach, next actions), canonical files, operating rhythm. | Both use workspace as operator entrypoint. work-politics dashboard schema is more granular (campaign vs outreach); work-dev is integration/implementation state. |
| **Operator path** | workspace → integration-status → known-gaps → provenance-checklist → economic-benchmarks; counterfactual harness. | workspace → work-politics operator surface → brief-source-registry → generate_wap_weekly_brief → content-queue → stage work-politics milestones. Plus **North star** in `docs/lanes/work-politics.md` and WEEKLY-RHYTHM. | work-politics has a **lanes** doc and **weekly rhythm**; work-dev has no lanes doc and no calendar-driven rhythm. |
| **Business / outreach** | offers, target-registry, proof-ledger, engagement-model, delivery-playbook, partner-channel, objection-log. | Same pattern: offers, target-registry, proof-ledger, outreach-workspace, outreach-funnel, objection-log. | ✅ Shared pattern (offers, proof-ledger, target-registry, objection-log). |

**Verdict:** Structure is aligned at the “README + workspace + principles + business surface” level. work-politics adds gate-sync policy, lanes, and weekly rhythm; work-dev adds integration-status, known-gaps, provenance-checklist. Differences are domain-appropriate.

---

## 3. RECURSION-GATE usage

| Aspect | work-dev | work-politics | Aligned? |
|--------|----------|-----|----------|
| **Territory tag** | No dedicated territory string. Handback candidates use `channel_key` (e.g. `openclaw:stage`, `operator:cli`). Treated as **companion** in `recursion_gate_territory.py`. | Explicit **`territory: work-politics`** (and legacy `work-american-politics`); **`channel_key: operator:wap`** or `operator:wap:*`. Filtered as work-politics in `recursion_gate_territory.py`. | ✅ By design: work-dev = default companion pipeline; work-politics = territory-filtered batch merge. |
| **Batch merge** | `process_approved_candidates.py` default (no `--territory`) = all approved. | `--territory wap` → only work-politics rows merged; `--territory companion` → only non-work-politics. | ✅ Same script; work-politics uses territory to separate batches. |
| **Doc-only vs stage** | Not formalized in README; staging is per handback/session. | Explicit: “Doc-only (no candidate)” vs “Stage to RECURSION-GATE when” (Voice/PRP, paid/milestone audit, explicit companion approval). Rhythm: weekly work-politics candidate or “doc-only this week.” | ⚠️ work-dev could add a short “when to stage” (e.g. after OpenClaw session, before export refresh) for parity. |
| **Template** | No candidate template in repo (analyst output shapes block). | **wap-candidate-template.md** — paste-ready YAML; territory + channel_key. | Optional: work-dev could add a minimal “handback candidate” template for operator use. |

**Verdict:** Gate usage is aligned: one gate file, same merge script; work-politics has territory and rhythm for batch separation; work-dev correctly stays “companion” and does not need a territory tag unless you introduce one later.

---

## 4. Operator surface and tooling

| Surface | work-dev | work-politics |
|---------|----------|-----|
| **CLI** | `openclaw_hook.py`, `openclaw_stage.py`, export commands. | `generate_wap_weekly_brief.py`, `process_approved_candidates.py --territory wap`, receipt flow. |
| **Harness warmup** | `harness_warmup.py`; `--territory wap` = work-politics pending only; `companion` = Record pending only. | Same; work-politics uses warmup for “pending work-politics gate items.” |
| **Lanes** | No `docs/lanes/work-dev.md`. | **docs/lanes/work-politics.md** — north star, done looks like, weekly minimum. |
| **Bootstrap** | Default session focus in `bootstrap/grace-mar-bootstrap.md` is work-dev (README + openclaw-integration). | work-politics is “other” focus; operator finds work-politics via lanes and workspace. |

**Verdict:** work-dev is the default bootstrap focus; work-politics has a dedicated lane and weekly rhythm. No conflict; optional improvement: add `docs/lanes/work-dev.md` for parity if you want a “north star” for dev territory.

---

## 5. Cross-references

| From → To | work-dev → work-politics | work-politics → work-dev |
|-----------|----------------|----------------|
| **README** | No reference to work-politics. | No reference to work-dev. Sentient-framing and simple-in-long-term list “build-ai” (legacy name) among territories (politics, gems, health, build-ai). |
| **Shared docs** | AGENTS.md, Architecture, openclaw-integration, crypto-roadmap, INTENT. | AGENTS.md, Architecture. OpenClaw appears in workspace (lessons-openclaw-skills-video), civ-mem, competitor notes. |
| **Gate / pipeline** | openclaw-integration, pipeline-events, RECURSION-GATE (implicit). | RECURSION-GATE, territory, wap-candidate-template, process_approved_candidates. |

**Gaps:**

- **work-politics** still says “build-ai” in sentient-framing and simple-in-long-term — should say **work-dev** (or “dev”) for consistency.
- **work-dev** does not mention work-politics or other territories; optional to add one line (e.g. “Other work territories: work-politics, work-civ-mem; same gate, different territory tags.”).

**Verdict:** Cross-refs are mostly one-way to shared docs. Naming fix: work-politics docs that list territories should use “work-dev” instead of “build-ai.”

---

## 6. Shared artifact pattern

Both territories use:

- **offers.md** — what we sell / offer.
- **target-registry.md** — who we sell to.
- **proof-ledger.md** — proof fragments for outreach.
- **objection-log.md** — learning from objections.

work-dev also has: engagement-model, delivery-playbook, partner-channel.  
work-politics also has: outreach-workspace, outreach-funnel, consulting-charter, compliance-checklist, revenue-log.

**Verdict:** Shared pattern is consistent; no alignment change needed.

---

## 7. Recommendations

| Priority | Action | Owner |
|----------|--------|--------|
| **High** | In work-politics: replace “build-ai” with “work-dev” in sentient-framing.md and simple-in-long-term-speculation.md where territories are listed. | Docs |
| **Medium** | In work-dev README: add one sentence under Cross-references: “Other work territories (e.g. work-politics) share the same RECURSION-GATE and companion-approval rule; they use territory tags for batch merge.” | work-dev |
| **Low** | Consider a short “When to stage” in work-dev README (after OpenClaw session, before export refresh, or when companion approves handback). | work-dev |
| **Low** | Consider adding `docs/lanes/work-dev.md` (north star, done looks like, “never without approval”) if you want lane parity with work-politics. | work-dev |
| **Optional** | In harness-warmup.mdc, update “work-build-ai” to “work-dev” in the “Relation to bootstrap” sentence. | .cursor/rules |

---

## 8. Summary

- **Governance:** Fully aligned (companion gate, no autonomous merge, evidence through pipeline).
- **Structure:** Aligned at README/workspace/principles level; work-politics adds gate-sync and lanes; work-dev adds integration-status and provenance.
- **RECURSION-GATE:** Correctly split: work-dev = companion (no territory); work-politics = territory + batch merge + rhythm.
- **Naming:** work-politics still references “build-ai”; should use “work-dev.”
- **Optional:** work-dev could add a “when to stage” line, a lanes doc, and a cross-ref to other territories.

No blocking misalignment; a few doc and naming updates will complete alignment.
