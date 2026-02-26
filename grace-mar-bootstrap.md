# GRACE-MAR BOOTSTRAP

Session bootstrap for continuing Grace-Mar in a new agent conversation.

---

## 1) First-Run Checklist (Do This First)

1. Read `agents.md` (guardrails and merge authority rules).
2. Read `docs/readme.md` (document map and hierarchy).
3. Read `docs/identity-fork-protocol.md` (canonical protocol contract).
4. Run `git status` and note uncommitted work.
5. Read `docs/development-handoff.md` (current state and next tasks).
6. **Companion-self audit** — Read `docs/audit-companion-self.md` (concept alignment: companion self, self-* taxonomy, tricameral). Optionally read `docs/audit-grace-mar-vs-companion-self-template.md` (instance vs template repo). Note any drift; if material changes have been made since the audit date, re-run or update the audit.

If working on companion profile operations, also read:
- `users/grace-mar/pending-review.md`
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
- Pilot active (`grace-mar`), gated pipeline live.
- Telegram bot operational with operator tooling (`/status`, `/intent_audit`, `/intent_review`).
- Intent layer active (`INTENT` schema + snapshot export + advisory conflict detection).
- OpenClaw integration supports outbound export and inbound stage-only handback.

### Recently completed development themes
- Intent Batch 2/3: cross-agent advisory checks, intent review command, debate packet workflow.
- OpenClaw hardening: constitution propagation in exports + inbound advisory constitutional checks.
- Curiosity probe workflow used to stage/merge IX-B growth signals.

---

## 4) New Conversation Menu

When loaded in a fresh session, offer these options:

1. **Run session** (chat-first companion interaction; no auto-merge)
2. **Pipeline operations** (stage/review/apply approved candidates)
3. **Intent governance** (audit/review/debate packet workflows)
4. **Integrations** (OpenClaw, extension, handback server)
5. **Business docs** (plan/prospectus/white-paper alignment)
6. **Other** (companion-defined task)

Wait for companion selection before large changes.

---

## 5) Development Commands (Operator)

### Health and status
```bash
git status
python3 scripts/metrics.py
python3 scripts/session_brief.py --user grace-mar
```

### Pipeline merge (receipt-based)
```bash
python3 scripts/process_approved_candidates.py --user grace-mar --generate-receipt /tmp/receipt.json --approved-by <name>
python3 scripts/process_approved_candidates.py --user grace-mar --apply --approved-by <name> --receipt /tmp/receipt.json
```

### Intent and integrity
```bash
python3 scripts/export_intent_snapshot.py --user grace-mar
python3 scripts/validate-integrity.py --user grace-mar --json
python3 scripts/governance_checker.py
```

### OpenClaw
```bash
python3 integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event
python3 integrations/openclaw_stage.py --user grace-mar --text "we explored X in OpenClaw"
```

### PRP refresh (after profile/prompt updates)
```bash
python3 scripts/export_prp.py -u grace-mar -n Abby -o grace-mar-llm.txt
```

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
- `docs/audit-grace-mar-vs-companion-self-template.md` — instance vs template ([github.com/rbtkhn/companion-self](https://github.com/rbtkhn/companion-self)); re-run after structure/protocol changes.
- `users/grace-mar/*` — active pilot Record files.

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
