# INTEGRATION-PROGRAM — OpenClaw ⟷ Grace-Mar (one-loop spec)

**Purpose:** Single canonical **operator program** for how OpenClaw and repo agents interact with Grace-Mar: **read order**, **export**, **stage-only handback**, and **merge** (human/operator only). This compresses behavior scattered across [openclaw-integration.md](../../openclaw-integration.md), hooks, and skills into one checklist-shaped doc — **not** a replacement for the full guide.

**Audience:** Operator, Cursor/Codex/Claude sessions, OpenClaw startup scripts.  
**Invariant:** Companion is always the gate. **Stage ≠ merge.**

**Related:** [PARALLEL-MACRO-ACTIONS.md](PARALLEL-MACRO-ACTIONS.md) (non-interfering branches), [session-continuity-contract.md](session-continuity-contract.md), [safety-story-ux.md](safety-story-ux.md).

**Related research (discourse ingested; not operational law):**

- [research-no-priors-karpathy-end-of-coding.md](research-no-priors-karpathy-end-of-coding.md) — end-of-coding / priors framing
- [research-agent-readable-writable-commerce.md](research-agent-readable-writable-commerce.md) — agent-readable/writable commerce and third-party narrative boundary

---

## 1. Read order (before doing work)

Run in this order so **staged vs canonical** stays mentally straight:

| Step | Source | Why |
|------|--------|-----|
| 1 | `users/[id]/session-log.md` | What happened last |
| 2 | `users/[id]/recursion-gate.md` | Pending candidates (not yet Record) |
| 3 | `users/[id]/self-evidence.md` (last 1–2 ACT blocks) | Recent approved activity |

Optional proof-of-read:

```bash
python scripts/continuity_read_log.py -u grace-mar
```

New **agent chat** in repo (no memory):

```bash
python scripts/harness_warmup.py -u grace-mar
# optional: --compact, --tail N
```

Long OpenClaw sessions:

```bash
python scripts/openclaw_heartbeat.py -u grace-mar
```

---

## 2. Export loop (identity → OpenClaw / bundle)

**Allowed:** Read Record, emit exports. **Not allowed:** writing SELF/EVIDENCE/prompt except via gated pipeline.

| Action | Command (examples) |
|--------|---------------------|
| Identity + manifest | `python integrations/openclaw_hook.py --user grace-mar --format md+manifest --emit-event` |
| Runtime bundle | `python scripts/export_runtime_bundle.py --user grace-mar --mode adjunct_runtime -o <dir>` |
| User identity only | `python scripts/export_user_identity.py --user grace-mar` |

Post-merge refresh (optional):

```bash
python scripts/process_approved_candidates.py --apply ... --export-openclaw --openclaw-format md+manifest
```

Do **not** treat raw EVIDENCE dumps or RECURSION-GATE as identity exports (see full guide).

---

## 3. Stage-only loop (OpenClaw / artifacts → gate)

**Allowed:** Stage candidates via `openclaw_stage` or analyst flow. **Not allowed:** merge, flip candidate to processed, edit SELF directly.

| Action | Command |
|--------|---------|
| Text + optional artifact | `python integrations/openclaw_stage.py --user grace-mar --text "…"` |
| Artifact | `python integrations/openclaw_stage.py --user grace-mar --artifact <path>` |

Inbound payloads get **advisory** constitutional critique vs `intent.md` / INTENT (events only — not auto-block). Prefer **structured** artifact refs; avoid anchoring narrative risk in the same blob as facts ([agent-reliability-playbook.md](agent-reliability-playbook.md)).

**Signal-only staging** (Cursor/analyst): append candidates to `recursion-gate.md` in the documented YAML block shape — still **no merge**.

---

## 4. Merge loop (human gate only)

Agents **never** merge. After companion approval:

```bash
python scripts/process_approved_candidates.py --apply
# or receipt flow: --generate-receipt then --apply --receipt <path>
```

Then refresh PRP/export as documented in AGENTS.md File Update Protocol.

---

## 5. Permission matrix (short)

| Action | Agent/automation | Companion / approved operator |
|--------|------------------|-------------------------------|
| Export identity | ✅ | — |
| Read SESSION-LOG, gate, EVIDENCE | ✅ | ✅ |
| Stage to RECURSION-GATE | ✅ | ✅ |
| Approve / reject | ❌ | ✅ |
| Merge SELF / EVIDENCE / prompt | ❌ | ✅ (via script only) |

---

## 6. Script index

| Script | Role |
|--------|------|
| `integrations/openclaw_hook.py` | Export + optional events |
| `integrations/openclaw_stage.py` | Stage-only handback |
| `scripts/continuity_read_log.py` | Log continuity read |
| `scripts/harness_warmup.py` | New-session gate/evidence snapshot |
| `scripts/openclaw_heartbeat.py` | Long-session pulse |
| `scripts/process_approved_candidates.py` | **Only** merge path for gate-approved candidates |
| `scripts/integration_macro_actions.py` | Optional branch names + merge order for parallel work ([PARALLEL-MACRO-ACTIONS.md](PARALLEL-MACRO-ACTIONS.md)) |
| `scripts/check_integration_readiness.py` | Dry-run: user dir, continuity files, `py_compile` on hooks, `continuity_read_log --dry-run`, import smoke for `openclaw_hook` / `openclaw_stage` |

---

## Guardrail

If this program conflicts with [integration-status.md](integration-status.md) or [known-gaps.md](known-gaps.md), **integration-status / known-gaps win** on what is implemented today. Use this file for **rhythm and ordering**, not for inventing features.

---

## 7. Risk mitigation

### Success criteria

| Metric | Target | How to measure |
|--------|--------|----------------|
| Export determinism | 100% — repeated exports produce identical output | Run export twice, diff manifests |
| Stage → gate consistency | 100% of staged candidates appear in `recursion-gate.md` with correct YAML shape | `scripts/validate-integrity.py` after staging |
| Readiness check pass rate | `check_integration_readiness.py` passes on every operator machine | Run as part of session warmup |
| Script import health | All scripts in §6 import cleanly (`py_compile`) | CI or manual `python -m py_compile` sweep |
| Gate backlog from integrations | < 20 pending integration-sourced candidates | Monitor `channel_key` counts in gate |

### Sustainment

| Task | Cadence | What to check |
|------|---------|---------------|
| Script smoke test | After any Python or dependency upgrade | Run `check_integration_readiness.py --dry-run` |
| OpenClaw schema compatibility | Before upgrading OpenClaw | Do `openclaw_hook.py` and `openclaw_stage.py` still produce valid output? |
| Parser drift audit | Quarterly or after 3+ new scripts touch gate/self/evidence | Is there still a single canonical parser, or have new ad-hoc parsers appeared? |
| Permission matrix spot-check | After adding any new script to §6 | Does the new script respect the agent/companion boundary in §5? |

### Deprecation path

If OpenClaw is abandoned, evolves incompatibly, or the operator decides the integration no longer delivers value:

1. **Stop staging from OpenClaw.** Pending OpenClaw-sourced candidates in the gate are reviewed and cleared normally through the existing pipeline.
2. **Stop exporting.** The Record continues in companion-self unaffected. OpenClaw retains its last export but receives no updates.
3. **Archive integration scripts.** Move `integrations/openclaw_hook.py` and `integrations/openclaw_stage.py` to `integrations/archived/` with a README note. Remove references from this program doc.
4. **No Record data is lost.** The integration only read from and staged to the existing pipeline. Retirement is cleanup, not migration.

### Scope creep guardrail

This program covers **one loop**: read → export → stage → human-gate merge. It does not authorize:

- **Bidirectional sync** (OpenClaw writing back to companion-self without staging)
- **Autonomous merge** (any path that bypasses companion approval)
- **New integration targets** (e.g. OB1, Telegram bots, third-party agents) without a separate integration plan per target — see [OB1 bridge](../../integrations/ob1/README.md) for the pattern
- **Scheduled or automated execution** (cron, GitHub Actions, webhooks) — every invocation is a conscious operator decision

Adding any of these requires a new plan document with operator approval, not an incremental PR to this file.
