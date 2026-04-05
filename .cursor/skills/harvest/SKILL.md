---
name: harvest
preferred_activation: harvest
description: "Cross-agent extraction ritual. Primary trigger: harvest. Reads the same on-disk class as bridge/coffee (instance paths + WORK territory history + git), then emits a structured Session Harvest Packet for pasting into a midstream agent session — analysis import, not cold start. Does not end with coffee."
---

# Session Harvest (`harvest`)

**Preferred activation:** say **`harvest`**. Also responds to **`session harvest`**, **`export session`**, or **`analysis handoff`**.

`harvest` produces a **Session Harvest Packet** — a structured markdown block the operator pastes into **another agent session that is already underway** (parallel tooling, second Cursor thread, review agent). It is **not** a replacement for **`bridge`** (fresh-thread continuity + seal + trailing `coffee`).

**Chat arc limits:** The agent **does not** receive a full Cursor thread export API. **Session arc** = (a) **visible conversation in this thread**, (b) **operator one-line steer** if context is thin, (c) optional **`users/<id>/session-transcript.md`** on disk. Do not promise full transcript replay from the skill alone.

**Dual-repo / EXECUTE scope:** When the operator ships template + instance work, **EXECUTE** messages should name scope: **grace-mar only**, **companion-self (template) only**, or **both** — same discipline as bridge; harvest does **not** require push.

---

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **Parallel or downstream agent needs dense context** | `harvest` | Single paste: outcomes, insights, files, risks, asks — **no** `coffee` tail |
| **Closing Cursor for a fresh thread** | **`bridge`** | Seal repos + **Session Bridge** packet ending with lone `coffee` |
| **Work-start / signing-off hub** | **`coffee`** | Fixed **A–E** menu; not an export packet |
| **End-of-day maintenance** | **`dream`** | MEMORY / integrity / digest; not a handoff packet |

**Harvest vs bridge (one line):** Bridge packet **must** end with standalone **`coffee`** for cold start. Harvest packet **must not** end with **`coffee`**; it ends with the contract closing line so pastes are never confused.

---

## Modes

One skill; adjust emphasis via operator wording or optional script flag:

| Mode | Emphasis |
|------|----------|
| **`default`** | Balanced outcomes + insights + next steps |
| **`technical`** | Files, modules, commands, failure modes |
| **`strategic`** | Decisions, tradeoffs, tensions, executive compression |
| **`minimal`** | Short packet; still follow [harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md) (omit empty sections) |

---

## Guardrails

- **No default commit/push** — harvest is read + synthesize unless the operator explicitly asks for git actions.
- **No RECURSION-GATE merges** — harvest does not approve or merge candidates.
- **No Record authority** — the packet is operator/tooling context, not SELF/EVIDENCE truth.
- **Signal over volume** — compress; tag brittle lines `{fact}` / `{proposal}` / `{uncertain}`.
- **Preserve uncertainty** — do not flatten open questions into false closure.

---

## Step 1 — Read on-disk state

Resolve **`<id>`** from the instance (default **`grace-mar`** in this repo). Read (do not ask — just read):

1. **`users/<id>/self-memory.md`** — pointers, open loops, calibrations
2. **`users/<id>/recursion-gate.md`** — pending candidates (ids, summaries; **do not** merge)
3. **`users/<id>/last-dream.json`** — last dream summary (hints only)
4. **`docs/skill-work/work-coffee/work-coffee-history.md`**
5. **`docs/skill-work/work-dream/work-dream-history.md`**
6. **`docs/skill-work/work-politics/work-politics-history.md`** — if present
7. **`docs/skill-work/work-dev/work-dev-history.md`** — if present
8. Optionally **`users/<id>/session-transcript.md`** — if the operator uses it for continuity

Also run in **this** repo:

9. **`git status -sb`**
10. **`git log --oneline -10`**

**Dual-repo awareness:** If the session touched **companion-self**, add **one line**: `git status -sb` (and branch) there — mirror bridge awareness; **no** required push.

**Optional helper:** `python3 scripts/session_harvest.py -u <id> [--mode MODE] [--emit-template] [--log]` — checklist + template only; the agent still fills narrative from the thread.

---

## Step 2 — Extract from the visible session

From **this thread** (plus operator steer / optional session-transcript), compress into:

- Main outcomes, strongest insights, decisions vs discussion
- Artifacts (paths, roles, existing vs proposed)
- Risks, tensions, critiques, open questions
- Recommended next steps, **suggested asks** for the receiving agent (Analyze…, Critique…, Compare…)

---

## Step 3 — Emit packet

Output **one** markdown block following **[harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)** — section order, **no** trailing **`coffee`**, **required final line** per contract.

---

## Optional persistence

Default: packet **only in chat**. If the operator says **save:** suggest `docs/skill-work/work-cadence/harvest-packets/YYYY-MM-DD-harvest.md` or a rolling `last-harvest.md` — **operator-owned**, not Record.

---

## Related

- **`bridge`** — [SKILL.md](../bridge/SKILL.md)
- **`coffee`** — [SKILL.md](../coffee/SKILL.md)
- **`dream`** — [SKILL.md](../dream/SKILL.md)
- **Cadence hub** — [work-cadence README](../../../docs/skill-work/work-cadence/README.md)
- **Packet contract** — [harvest-packet-contract.md](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)

---

## Revision log

| Date | Change |
|------|--------|
| 2026-04-04 | Initial skill (bridge sibling, real paths, chat-limit note). |
