# GRACE-MAR BOOTSTRAP

Session bootstrap for continuing Grace-Mar in a new agent conversation.

---

## Session focus: full-repo optimization (advanced LLM)

Use this when starting a **new session with a stronger model** to refactor, dedupe, document, or harden the **whole repository** — not a single feature thread.

### Paste into message 1 (clean context)

```bash
python3 scripts/harness_warmup.py -u grace-mar --fresh-judge
python3 scripts/harness_warmup.py -u grace-mar --compact
```

Paste both outputs (or the full non-compact block). **Canonical state is on disk**, not prior chat.

### Read before large edits (order)

| # | File | Why |
|---|------|-----|
| 1 | `agents.md` | Sovereign merge, knowledge boundary, Lexile, MEMORY vs Record, file-update protocol |
| 2 | `docs/harness-inventory.md` | What may write where; bot/core audit; two doors / one book |
| 3 | `docs/architecture.md` (§ System boundaries) | Voice = model + harness; non-goals |
| 4 | `docs/identity-fork-protocol.md` | Stage → approve → merge; never direct SELF/EVIDENCE without gate |
| 5 | `docs/development-handoff.md` | Current engineering state; don’t contradict without updating |
| 6 | `docs/readme.md` | Doc map |

Skim as needed: `docs/conceptual-framework.md` (tricameral, companion), `docs/chat-first-design.md` (chat is product; operator dashboards optional). **After shared reading:** [we-read-think-self-pipeline.md](docs/we-read-think-self-pipeline.md) (READ/THINK vs RECURSION-GATE → IX).

**Operator structure:** `docs/lanes/README.md` (north star per lane) + `docs/lanes/WEEKLY-RHYTHM.md` (weekly checklist). **Library wiring:** `docs/library-integration.md` · `python3 scripts/library_shelf_summary.py -u grace-mar`

### Non-negotiables for “optimization”

- **Do not** merge into `users/*/self.md`, `self-evidence.md`, or `bot/prompt.py` without companion approval (stage only).
- **Do not** add undocumented facts into the Record or SYSTEM prompt (knowledge boundary).
- **Do not** raise Lexile ceiling without writing-sample evidence (agents.md).
- **Do not** bypass pre-commit: Record-facing edits in gated paths need commit message **`[gated-merge]`** (or hook will block).
- **Preserve** contradiction + provenance; don’t flatten tensions in companion files.
- **Prefer** small PR-sized commits; run checks below before claiming done.

### Safe optimization targets (high value, low sovereignty risk)

- **Tests / CI:** `scripts/run_counterfactual_harness.py`, `scripts/test_voice_linguistic_authenticity.py`, `validate-integrity.py`, `governance_checker.py`
- **Duplication:** shared helpers in `scripts/`, repeated patterns in `bot/`
- **Docs:** drift, broken links, single source of truth (link to harness-inventory instead of copying policy)
- **Operator ergonomics:** scripts/README, Makefile or task list, typing/lint on `bot/core.py` (behavior unchanged)
- **Dependencies:** `bot/requirements.txt` pin audit; security warnings only — don’t swap stack without handoff note

### Verify after substantive changes

```bash
python3 scripts/governance_checker.py
python3 scripts/validate-integrity.py --user grace-mar --json
# If bot/prompt.py or emulation changed:
python3 scripts/run_counterfactual_harness.py
python3 scripts/test_voice_linguistic_authenticity.py
```

If **validate-integrity** reports stale derived exports or runtime bundle, run:

```bash
python3 scripts/fork_checksum.py --manifest && \
python3 scripts/export_manifest.py -u grace-mar && \
python3 scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt && \
python3 scripts/export_runtime_bundle.py -u grace-mar -o users/grace-mar/runtime-bundle
```

End of session: update **`docs/development-handoff.md`**, commit, push if requested.

---

**Default session focus — work-dev (continue here):**
1. Read §1 (first-run checklist).
2. Read **`docs/skill-work/work-dev/README.md`** — objective, companion gate invariant, principles (merges former work-build-ai).
3. Read **`docs/openclaw-integration.md`** — export, session continuity, inbound staging, staging automation.
4. Skim **`integrations/openclaw_hook.py`**, **`integrations/openclaw_stage.py`**, **`scripts/export_user_identity.py`**.
5. Optional: **`docs/skill-work/work-dev/economic-benchmarks.md`**, **`research-moonshots-237.md`**.
6. Use §5 OpenClaw commands and §6 work-dev / OpenClaw file map below.

**Other session focus:**
- If **extension-focused** (not work-dev), read §1 then **extension/readme.md** and skim `extension/`. Use §5 Extension commands and §6 Extension file map below.

---

## 1) First-Run Checklist (Do This First)

1. Read `agents.md` (guardrails and merge authority rules).
2. Read `docs/readme.md` (document map and hierarchy).
3. Read `docs/identity-fork-protocol.md` (canonical protocol contract).
4. Run `git status` and note uncommitted work.
5. Read `docs/development-handoff.md` (current state and next tasks).
6. **work-dev** — Read `docs/skill-work/work-dev/README.md`; then `docs/openclaw-integration.md` if continuing integration work.
7. **Companion-self audit** — Read `docs/audit-companion-self.md` (concept alignment: companion self, self-* taxonomy, tricameral). Optionally read `docs/audit-grace-mar-vs-companion-self-template.md` (instance vs template repo). Note any drift; if material changes have been made since the audit date, re-run or update the audit.

If working on companion profile operations (not work-dev), also read:
- `users/grace-mar/recursion-gate.md`
- `users/grace-mar/self.md`
- `users/grace-mar/self-evidence.md`
- `users/grace-mar/pipeline-events.jsonl`

---

## 2) Non-Negotiable Rules

- **Tricameral mind** — Grace-Mar is a **tricameral mind**: **MIND** (human, conscious, sovereign), **RECORD** (Grace-Mar), **VOICE** (Grace-Mar). Mind holds authority; the Record reflects; the Voice speaks when queried. Grace-Mar serves the companion; the companion serves Grace-Mar. See agents.md and `docs/conceptual-framework.md` §8.
- Sovereign Merge Rule: **agent may stage; agent may not merge without explicit companion approval**.
- Knowledge boundary: no undocumented facts enter the Record.
- Evidence linkage: profile claims must trace to evidence artifacts.
- Record authority: `SELF/SKILLS/EVIDENCE` are canonical; MEMORY is ephemeral.
- Preserve contradictions with provenance; do not flatten tension.

---

## 3) Current System Snapshot

### Product state
- Active instance (`grace-mar`), **moment of cognitive bifurcation** (Seed Phase 7, 2026-02-27) — graduated to emergent cognition. Gated pipeline live.
- Telegram bot operational with operator tooling (`/status`, `/intent_audit`, `/intent_review`).
- Intent layer active (`INTENT` schema + snapshot export + advisory conflict detection).
- OpenClaw integration supports outbound export and inbound stage-only handback.

### Recently completed development themes
- Intent Batch 2/3: cross-agent advisory checks, intent review command, debate packet workflow.
- OpenClaw hardening: constitution propagation in exports + inbound advisory constitutional checks.
- Curiosity probe workflow used to stage/merge IX-B growth signals.

### work-dev (active continuation)
- **Territory:** `docs/skill-work/work-dev/` — Record ↔ OpenClaw; stage-only handback; companion gate invariant (never control-grid). Merges former work-build-ai.
- **Next:** See `docs/development-handoff.md`; extend hooks, staging automation, benchmarks, or Moonshots takeaways as handoff specifies.

---

## 4) New Conversation Menu

When loaded in a fresh session, offer these options:

1. **work-dev** (default — OpenClaw integration, export, staging, session continuity; read work-dev README + openclaw-integration)
2. **Run session** (chat-first companion interaction; no auto-merge)
3. **Pipeline operations** (stage/review/apply approved candidates)
4. **Intent governance** (audit/review/debate packet workflows)
5. **Browser extension** (transcript handback, Save to Record, popup/context menu, handback server)
6. **Business docs** (plan/prospectus/white-paper alignment)
7. **Other** (companion-defined task)
8. **Full-repo optimization** (advanced model — read **Session focus: full-repo optimization** at top of this file; fresh-judge + harness-inventory first)

Wait for companion selection before large changes.

---

## 5) Development Commands (Operator)

### Health and status
```bash
git status
python3 scripts/metrics.py
python3 scripts/session_brief.py --user grace-mar
python3 scripts/session_brief.py --user grace-mar --minimal
python3 scripts/session_brief.py -u grace-mar --minimal --territory wap   # WAP pending only
python3 scripts/pending_dedup_hint.py -u grace-mar
python3 scripts/report_lookup_sources.py -u grace-mar   # dyad:lookup distribution (library vs full)
python3 scripts/operator_blocker_report.py -u grace-mar --stale-days 3   # WAP + companion sections by default
python3 scripts/operator_blocker_report.py -u grace-mar --territory wap  # WAP-only pending
```

### Pipeline merge (receipt-based)
```bash
python3 scripts/process_approved_candidates.py --user grace-mar --generate-receipt /tmp/receipt.json --approved-by <name>
python3 scripts/process_approved_candidates.py --user grace-mar --apply --approved-by <name> --receipt /tmp/receipt.json
# WAP-only batch (same --territory for generate + apply):
python3 scripts/process_approved_candidates.py -u grace-mar --territory wap --generate-receipt /tmp/wap.json --approved-by <name>
python3 scripts/process_approved_candidates.py -u grace-mar --territory wap --apply --approved-by <name> --receipt /tmp/wap.json
```

### Intent and integrity
```bash
python3 scripts/export_intent_snapshot.py --user grace-mar
python3 scripts/validate-integrity.py --user grace-mar --json
python3 scripts/governance_checker.py
pip install pre-commit && pre-commit install && pre-commit install --hook-type commit-msg   # optional: block Record edits without [gated-merge]
```

### Harness warmup (any agent session — paste into first message)
```bash
python3 scripts/harness_warmup.py -u grace-mar
python3 scripts/harness_warmup.py -u grace-mar --fresh-judge   # clean context for new thread / advanced model
python3 scripts/harness_warmup.py -u grace-mar --territory wap   # WAP pending only in paste
python3 scripts/harness_warmup.py -u grace-mar --compact
python3 scripts/generate_gate_dashboard.py -u grace-mar   # pending queue HTML (human door)
```

**Operator rhythm — "good morning":** First message of the day can be just that; the agent should run [daily-warmup skill](.cursor/skills/daily-warmup/SKILL.md) (`operator_daily_warmup.py` + `harness_warmup.py` when state matters) and **always** generate [work-strategy daily brief](docs/skill-work/work-strategy/daily-brief-template.md): `python3 scripts/generate_wap_daily_brief.py -u grace-mar -o docs/skill-work/work-strategy/daily-brief-$(date +%Y-%m-%d).md`. Return warmup snapshot + brief path + short headline/next-action summary.

### OpenClaw
```bash
python3 integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
python3 integrations/openclaw_stage.py --user grace-mar --text "we explored X in OpenClaw"
python3 scripts/export_conversation_trajectories.py -u grace-mar -o /tmp/traj.jsonl   # optional JSONL for local RL; see docs/openclaw-rl-boundary.md
```

### Proposal brief (proactive activities from Record)
```bash
python3 scripts/proposal_brief.py -u grace-mar -n 5
```

### PRP refresh (after profile/prompt updates)
```bash
python3 scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt
```

### Extension (browser extension focus)
```bash
# Run handback server (required for Save to Record + transcript handback)
python3 scripts/handback_server.py
# Load unpacked: chrome://extensions → Developer mode → Load unpacked → select extension/
```
- Extension lives in `extension/`. Popup: Save to Record, Save transcript (paste → /handback). Context menu: Save to Record, Save transcript to Record (selection → /handback).
- See `extension/readme.md` for setup, settings (stage URL, API key, user_id, queue retry).

---

## 6) Primary File Map

- `agents.md` — development guardrails and policy.
- `docs/readme.md` — canonical doc map.
- `docs/identity-fork-protocol.md` — protocol compact.
- `docs/architecture.md` — system implementation model.
- `docs/white-paper.md` — narrative + technical thesis.
- `docs/business-plan.md` — execution/commercial operating plan.
- `docs/business-prospectus.md` — concise investor summary.
- `docs/business-roadmap.md` — strategic priorities and metrics.
- `docs/development-handoff.md` — latest engineering handoff.
- `docs/audit-companion-self.md` — companion-self concept alignment (run as part of bootstrap; re-run after concept/taxonomy changes).
- `docs/design-notes.md` §11.9 — intent gap, three questions before approve / long agent runs.
- `docs/design-notes.md` §11.10 — rejection as skill; encode taste via gate + calibrate_from_miss.
- `docs/design-notes.md` §11.11 — harness convergence (verify loop; labs’ shared pattern).
- `docs/audit-grace-mar-vs-companion-self-template.md` — instance vs template ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)); re-run after structure/protocol changes.
- `users/grace-mar/*` — active instance Record files.

**Harness hybrid (plan in one tool, build in another):**
- `docs/harness-handoff.md` — handoff = commits + warmup paste; never state only in chat.
- `docs/harness-inventory.md` — components, write surfaces, two doors / one book; **start here for repo-wide refactors**.

**work-dev / OpenClaw (default continuation):**
- `docs/skill-work/work-dev/README.md` — territory objective; companion gate invariant; principles; quick ref commands.
- `docs/skill-work/work-dev/economic-benchmarks.md` — cost/value/gate health metrics.
- `docs/skill-work/work-dev/research-moonshots-237.md` — identity, memory, hierarchy; actionable takeaways.
- `docs/openclaw-integration.md` — canonical integration guide (export, session continuity, inbound staging, staging automation).
- `integrations/openclaw_hook.py` — outbound export (Record → user.md / SOUL.md); md+manifest, json+md; emits pipeline event.
- `integrations/openclaw_stage.py` — inbound staging (OpenClaw output → /stage); advisory constitutional check; stage-only, never merge.
- `scripts/export_user_identity.py` — identity-only export for user.md / SOUL.md.
- `integrations/export_hook.py` — shared export logic; openclaw target.
- Session continuity: read `users/grace-mar/session-log.md`, `recursion-gate.md`, last EVIDENCE before OpenClaw sessions.

**Extension (when focus is browser extension):**
- `extension/readme.md` — setup, behavior, settings.
- `extension/manifest.json` — version, permissions, background/popup/context menu.
- `extension/background.js` — handback/stage URLs, message handling, context menu, queue/retry.
- `extension/popup.html` / `extension/popup.js` — toolbar UI (Save to Record, Save transcript, Retry Queue, Settings).
- `scripts/handback_server.py` — local server for `/stage` and `/handback` (default 127.0.0.1:5050).

---

## 7) End-of-Session Handoff Rule

Before ending a development session:

1. Update `docs/development-handoff.md` with what changed and what is next.
2. Ensure PRP is regenerated if Record/prompt changed.
3. Run integrity/governance checks if changes touched pipeline logic.
4. If concept, taxonomy, or template-facing structure changed, update or re-run the companion-self audit(s) (see §1 step 6 and §6 file map).
5. Confirm commit/push status if the companion requested version control actions.

---

END OF FILE — GRACE-MAR BOOTSTRAP
