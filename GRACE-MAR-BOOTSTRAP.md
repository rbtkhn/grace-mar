# GRACE-MAR BOOTSTRAP

Session bootstrap for continuing Grace-Mar in a new agent conversation.

---

## 1) First-Run Checklist (Do This First)

1. Read `AGENTS.md` (guardrails and merge authority rules).
2. Read `docs/README.md` (document map and hierarchy).
3. Read `docs/IDENTITY-FORK-PROTOCOL.md` (canonical protocol contract).
4. Run `git status` and note uncommitted work.
5. Read `docs/DEVELOPMENT-HANDOFF.md` (current state and next tasks).

If working on companion profile operations, also read:
- `users/pilot-001/PENDING-REVIEW.md`
- `users/pilot-001/SELF.md`
- `users/pilot-001/EVIDENCE.md`
- `users/pilot-001/PIPELINE-EVENTS.jsonl`

---

## 2) Non-Negotiable Rules

- **Tricameral mind** — Grace-Mar is a **tricameral mind**: **MIND** (human, conscious, sovereign), **RECORD** (Grace-Mar), **VOICE** (Grace-Mar). Mind holds authority; the Record reflects; the Voice speaks when queried. Grace-Mar serves the companion; the companion serves Grace-Mar. See AGENTS.md and `docs/CONCEPTUAL-FRAMEWORK.md` §8.
- Sovereign Merge Rule: **agent may stage; agent may not merge without explicit companion approval**.
- Knowledge boundary: no undocumented facts enter the Record.
- Evidence linkage: profile claims must trace to evidence artifacts.
- Record authority: `SELF/SKILLS/EVIDENCE` are canonical; MEMORY is ephemeral.
- Preserve contradictions with provenance; do not flatten tension.

---

## 3) Current System Snapshot

### Product state
- Pilot active (`pilot-001`), gated pipeline live.
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
python3 scripts/session_brief.py --user pilot-001
```

### Pipeline merge (receipt-based)
```bash
python3 scripts/process_approved_candidates.py --user pilot-001 --generate-receipt /tmp/receipt.json --approved-by <name>
python3 scripts/process_approved_candidates.py --user pilot-001 --apply --approved-by <name> --receipt /tmp/receipt.json
```

### Intent and integrity
```bash
python3 scripts/export_intent_snapshot.py --user pilot-001
python3 scripts/validate-integrity.py --user pilot-001 --json
python3 scripts/governance_checker.py
```

### OpenClaw
```bash
python3 integrations/openclaw_hook.py --user pilot-001 --format md+manifest --emit-event
python3 integrations/openclaw_stage.py --user pilot-001 --text "we explored X in OpenClaw"
```

### PRP refresh (after profile/prompt updates)
```bash
python3 scripts/export_prp.py -u pilot-001 -n Abby -o grace-mar-abby-prp.txt
```

---

## 6) Primary File Map

- `AGENTS.md` — development guardrails and policy.
- `docs/README.md` — canonical doc map.
- `docs/IDENTITY-FORK-PROTOCOL.md` — protocol compact.
- `docs/ARCHITECTURE.md` — system implementation model.
- `docs/WHITE-PAPER.md` — narrative + technical thesis.
- `docs/BUSINESS-PLAN.md` — execution/commercial operating plan.
- `docs/BUSINESS-PROSPECTUS.md` — concise investor summary.
- `docs/BUSINESS-ROADMAP.md` — strategic priorities and metrics.
- `docs/DEVELOPMENT-HANDOFF.md` — latest engineering handoff.
- `users/pilot-001/*` — active pilot Record files.

---

## 7) End-of-Session Handoff Rule

Before ending a development session:

1. Update `docs/DEVELOPMENT-HANDOFF.md` with what changed and what is next.
2. Ensure PRP is regenerated if Record/prompt changed.
3. Run integrity/governance checks if changes touched pipeline logic.
4. Confirm commit/push status if the companion requested version control actions.

---

END OF FILE — GRACE-MAR BOOTSTRAP
