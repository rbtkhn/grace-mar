# work-cadence

**Purpose:** Doctrine, boundaries, and architecture for the daily cadence triad — `coffee` (morning orientation), `dream` (night consolidation), and `bridge` (session-scale handoff) — plus **`harvest`** as a **fourth operator tool on a different axis** (cross-agent extraction; on demand, not a fourth clock). Executable trigger surfaces live in `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/dream/SKILL.md`, `.cursor/skills/bridge/SKILL.md`, and `.cursor/skills/harvest/SKILL.md`.

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of operator rhythm: coffee (orientation, repeated), dream (consolidation, once per day), bridge (session-scale carry-forward), harvest (cross-agent packet; midstream import). |
| **Night-to-morning handoff** | Documents the `last-dream.json` data contract that bridges dream output to coffee Step 1. |
| **Cadence event audit** | Append-only telemetry of each run via `work-cadence-events.md` and `scripts/log_cadence_event.py` (kinds include optional **`harvest`** for tooling consistency). |
| **Context paste budgets** | Optional JSON caps for dream write-path and coffee display (`config/context_budgets/`); `scripts/audit_context_tax.py` approximates ritual paste size. |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |

---

## Daily rhythm

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, warmup brief, harness, branch snapshot, A–E menu |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest, handoff JSON |
| **Session close** | `bridge` | Seal (commit/push), synthesize transfer prompt for next Cursor session |

**Many coffees, one dream, one bridge.** `coffee` is for repetition. `dream` is for closure. `bridge` is for carry-forward.

---

## Why three rituals

Work fails on three clocks:

**The framing clock (hours).** During the day, orientation degrades under context load. Not lack of information — degraded framing. `coffee` restores it. Many sips per day.

**The residue clock (day).** By evening, unresolved threads, integrity drift, and unprocessed signals accumulate. `dream` settles them without dramatic mutation.

**The context clock (session).** At session boundaries, agent memory goes to zero. Everything not on disk is lost. `bridge` seals the session and produces a transfer prompt so the next thread starts oriented instead of blank.

Each clock needs its own ritual because the failure modes are different. Reorientation is not consolidation. Consolidation is not transfer. Merging them into one ritual would either make it too heavy for frequent use or too shallow for end-of-day closure.

---

## Fourth operator tool: cross-agent extraction (`harvest`)

**Not a fourth clock.** `coffee`, `dream`, and `bridge` answer **when** the operator needs framing, day-close residue, or session-boundary transfer. **`harvest`** answers **how** to ship dense session substance to **another agent or thread that is already running** (parallel review, tooling handoff, second Cursor session without a cold start).

- **Skill:** [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md)
- **Packet contract:** [harvest-packet-contract.md](harvest-packet-contract.md) (section headings; **no** trailing `coffee` — contrast **bridge**, whose transfer block ends with `coffee` for cold start; bridge packet contract may live upstream in companion-self)
- **Optional script:** `scripts/session_harvest.py` — checklist + template + optional `--log` → `log_cadence_event.py --kind harvest`

**Template home:** Canonical skill + contract + cadence doc edits land in **companion-self** first; **grace-mar** reconciles via `template_diff.py` / operator **EXECUTE** scope (**grace-mar only** / **template only** / **both**). If you only have this repo checked out, implement here and reconcile the template on the next dual-repo pass.

---

## Contents

| File | Purpose |
|------|---------|
| **This README** | Scope, rhythm, boundaries for work-cadence. |
| **[harvest-packet-contract.md](harvest-packet-contract.md)** | Session Harvest Packet headings and rules vs bridge. |
| **[work-cadence-events.md](work-cadence-events.md)** | Append-only audit of cadence runs (coffee/dream/bridge; optional harvest). Not Record. |

---

## Cadence event audit

Each coffee, dream, bridge, and optional **harvest** run appends one line to [work-cadence-events.md](work-cadence-events.md) via `scripts/log_cadence_event.py`. This is operator-facing telemetry — not the Record, not self-memory.

**Emitters:**
- **dream** — `auto_dream.py` appends after successful completion (gated on `apply=True`)
- **coffee** — `operator_coffee.py` appends after all steps succeed
- **bridge** — agent runs `log_cadence_event.py --kind bridge` in Step 2 after push
- **harvest** — optional; operator or agent runs `session_harvest.py --log` or `log_cadence_event.py --kind harvest` after emitting a packet (lighter than bridge; telemetry consistency only)

**Leaf-only rule:** Orchestrators (`operator_end_of_day.py`, `operator_coffee.py` when it chains) do not emit their own events. Only the leaf ritual logs.

**Split threshold:** If cadence events exceed ~200 lines/month, consider adding a JSONL sibling and keeping monthly rollup bullets in this markdown file.

---

## Script topology (grace-mar)

```
operator_coffee.py          consolidated morning runner (modes: work-start, light, minimal, closeout, reentry)
  ├─ operator_daily_warmup.py    priorities, gate, territories, integrity, dream handoff pickup
  ├─ harness_warmup.py           compact state snapshot
  └─ operator_handoff_check.py   (closeout mode only)

operator_end_of_day.py      night-side bundle
  ├─ auto_dream.py               memory normalization, integrity, governance, contradiction, last-dream.json (+ 24h coffee rollup, execution paths, optional civ-mem echoes)
  └─ operator_handoff_check.py   gate, commits, worktree, re-entry prompt
```

---

## Gate threshold

`work-cadence` is **operational by default**. Stage to `recursion-gate.md` only when a cadence insight would change governed behavior (prompt, policy, identity-relevant signals).

---

## Write authority map

Which on-disk surfaces each ritual reads, writes, and whether companion approval is required.

| Ritual | Reads | Writes | Gate required? |
|--------|-------|--------|---------------|
| **coffee** | self-memory, recursion-gate, last-dream.json, git status, territories | nothing (read-only planning) | No |
| **dream** | self-memory, SELF, EVIDENCE, recursion-gate | self-memory, last-dream.json, contradiction digest, cadence events, pipeline events | No (Maintenance mode) |
| **bridge** | self-memory, recursion-gate, last-dream.json, territories, git status/log | git commits, cadence events | No (operational) |
| **harvest** | same class as coffee (self-memory, recursion-gate, last-dream.json, territories, git; optional session-transcript) | **default none**; optional operator-requested save under `work-cadence/harvest-packets/` or `last-harvest.md`; optional cadence event line | No |
| **gate merge** | recursion-gate candidates, SELF, EVIDENCE, prompt | SELF, EVIDENCE, prompt, session-log, recursion-gate, pipeline events, PRP | **Yes — companion approval required** |

**Key boundary:** coffee and bridge never write to identity surfaces. Dream writes to ephemeral/operational surfaces only (self-memory, handoff artifacts). Only the gated merge path — triggered by companion approval, executed by `process_approved_candidates.py` — touches the Record.

---

## End-of-session decision tree

When the operator signals they're done (end of day, closing the session, stepping away), use this tree:

| Scenario | Recommended path | What it does |
|----------|-----------------|--------------|
| **Ending the day AND closing this Cursor session** | `dream` then `bridge` | Dream settles continuity; bridge seals both repos and generates the transfer prompt |
| **Ending the day, keeping the session** | `dream` alone | Dream runs maintenance; session continues tomorrow with the same thread |
| **Mid-day, closing this Cursor session** | `bridge` alone | Seals repos and generates transfer prompt; no maintenance pass needed |
| **Quick status check before stepping away** | **`coffee`** + signing-off intent (`operator_coffee.py --mode closeout` / handoff Step 1) | Lightweight handoff summary; no commit/push, no maintenance; **same** **A–E** menu as work-start |

**Default for 80% of cases:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

**Signing-off `coffee` vs bridge:** Signing-off **`coffee`** is the lightweight option — quick gate/worktree status, no commits, no push, no transfer prompt. Bridge is the structural option — seals the session with commits and produces the carry-forward block. They do not overlap; bridge remains the session-end default when you need git seal + transfer prompt.

---

## Cadence troubleshooting

When a cadence run produces unexpected output, check these in order:

### Coffee output looks wrong

1. **Dream handoff missing?** Check `users/grace-mar/last-dream.json` — if the file is absent or stale (timestamp older than last night), dream didn't run or didn't complete. Run `dream` manually.
2. **Gate data stale?** The warmup reads `recursion-gate.md` directly. If gate counts look wrong, check the file itself — not the warmup output.
3. **Wrong mode?** `operator_coffee.py` defaults to `work-start`. If you got a minimal harness when you expected a full brief, check which mode was passed. Run with `--mode work-start` explicitly.
4. **Script failed silently?** Check the exit code. `operator_coffee.py` chains sub-scripts and stops on first failure. If the harness ran but the warmup didn't, the warmup script errored.

### Dream output looks wrong

1. **Integrity or governance failed?** Check the dream summary output for `integrity ok: False` or `governance ok: False`. In strict mode, dream halts on failure — self-memory won't be updated, no handoff written.
2. **Self-memory not updated?** Dream only writes self-memory when `apply=True` (not `--dry-run`) and maintenance is not halted. Check the `self_memory_changed` field in `last-dream.json`.
3. **Cadence event not logged?** The event is gated on `apply=True and not halted`. Dry-run dreams and halted strict dreams produce no cadence line — by design.

### Bridge output looks wrong

1. **Commit failed?** Bridge commits are done by the agent, not a script. If a commit failed, the agent should have reported it. Check `git status -sb` in both repos.
2. **Push rejected?** Usually means remote has new commits. The agent should pull-rebase and retry. If it didn't, run `git pull --rebase && git push` manually.
3. **Transfer prompt thin?** Bridge synthesizes from on-disk state. If territories have no recent history or the gate is empty, those sections will be sparse — that's correct, not broken.
4. **Coffee didn’t run after paste?** The transfer block must end with a lone line `coffee` (no code fence). If that line was dropped when copying, append `coffee` or re-copy from the bridge output; see `.cursor/skills/bridge/SKILL.md` Step 3.

### Harvest packet confusion

1. **Wrong ritual?** If the target session needs a **cold start**, use **`bridge`** (ends with `coffee`). **`harvest`** packets **must not** end with `coffee`; see [harvest-packet-contract.md](harvest-packet-contract.md).
2. **Thin narrative sections?** The script only prints paths and git; the agent fills outcomes from the **visible thread** (no full Cursor export API). Add a one-line operator steer or read `session-transcript.md` if needed.

### General

- **Which cadence events actually ran?** Check `docs/skill-work/work-cadence/work-cadence-events.md` — one line per run with timestamp, kind, mode, and outcome.
- **Agent reading stale skill file?** Long Cursor sessions can cache file contents. If the agent's behavior doesn't match the current SKILL.md, ask it to re-read the file.

---

## Adjacent surfaces

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) — coffee trigger
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) — dream trigger
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) — bridge trigger
- [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) — harvest trigger
- [work-coffee/](../work-coffee/) — coffee design history and menu reference
- [work-dream/](../work-dream/) — dream design history and doctrine
- [work-modules-history-principle.md](../work-modules-history-principle.md) — cross-territory history convention
