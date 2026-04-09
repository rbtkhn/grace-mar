---
name: harvest
preferred_activation: harvest
description: "Cross-agent extraction ritual. Primary trigger: harvest. Reads the same on-disk class as bridge/coffee (instance paths + WORK territory history + git), then emits a structured Session Harvest Packet for pasting into a midstream agent session — analysis import, not cold start. Soft thread-depth heuristics (visible arc ~15–25 exchanges; optional session-transcript tail 200 lines or deep read). Does not end with coffee."
---

# Session Harvest (`harvest`)

**Preferred activation:** say **`harvest`**. Also responds to **`session harvest`**, **`export session`**, or **`analysis handoff`**.

`harvest` produces a **Session Harvest Packet** — a structured markdown block the operator pastes into **another agent session that is already underway** (parallel tooling, second Cursor thread, review agent). It is **not** a replacement for **`bridge`** (fresh-thread continuity + seal + trailing `coffee`).

**Dual-repo / EXECUTE scope:** When the operator ships template + instance work, **EXECUTE** messages should name scope: **grace-mar only**, **companion-self (template) only**, or **both** — same discipline as bridge; harvest does **not** require push.

---

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **Parallel or downstream agent needs dense context** | `harvest` | Single paste: outcomes, insights, files, risks, asks — **no** `coffee` tail |
| **Closing Cursor for a fresh thread** | **`bridge`** | Seal repos + **Session Bridge** packet ending with lone `coffee` |
| **Work-start / signing-off hub** | **`coffee`** | Fixed **A–G** menu; not an export packet |
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
- **Cadence voice (where applicable):** Harvest does not include Step 0 rhythm synthesis, but any companion-facing prose in the packet (e.g. `## Current session purpose`, `## Important developments`) should still follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)) — forward-oriented, "we" framing, felt not listed.

---

## Thread depth and honesty

The agent **does not** receive a full Cursor thread export API. Do **not** promise full transcript replay.

**Default intent (what to prioritize in Step 2):**

1. The **current task arc** — what this working session is trying to finish or decide.
2. The **most recent substantive operator directive** (e.g. **EXECUTE** scope, lane pick, “do it,” pasted errors, explicit constraints).

**Soft exchange heuristic (not a hard cap):** Treat roughly the **last 15–25** user/assistant **message groups** visible in this chat as the **primary spine** for narrative extraction. If fewer are visible, use everything available. Cursor context length varies; this number is **orientation for the model**, not a product guarantee.

**Truncation honesty:** If early turns are clearly **not** in context, **do not** imply the packet summarizes the entire session from hour one. Add **`## Thread coverage`** (see [harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)) with a one-line caveat, **or** fold the same caveat into **`## Current session purpose`**.

**Disk vs chat:** Step 1 on-disk reads (gate, git, `work-*-history`, etc.) are **anchors** for facts; chat extraction is **compression** of the visible arc. When in doubt, tag narrative `{uncertain}` and lean on disk.

**`session-transcript.md` (optional file):**

| Operator signal | Transcript read |
|-----------------|-----------------|
| **Default** (no extra wording) | If the file **exists**, read the **tail: last 200 lines** (if the file has fewer lines, read the whole file). Blend with visible thread in Step 2. |
| **Deep / full transcript / harvest deep** in the **same** turn as **`harvest`** | Read the **entire** `session-transcript.md`. If it is **very large** (roughly **>800 lines**), read the **last 500 lines** instead and state that in **`## Thread coverage`** (partial tail only). |

If the transcript file is **absent**, rely on visible thread + disk only.

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
8. **`users/<id>/session-transcript.md`** — if **missing**, skip. If **present**, read per **Thread depth and honesty** (default **tail 200 lines**; **deep** = full file or last 500 if huge).

Also run in **this** repo:

9. **`git status -sb`**
10. **`git log --oneline -10`**

**Dual-repo awareness:** If the session touched **companion-self**, add **one line**: `git status -sb` (and branch) there — mirror bridge awareness; **no** required push.

**Optional helper:** `python3 scripts/session_harvest.py -u <id> [--mode MODE] [--emit-template] [--log]` — checklist + template only; the agent still fills narrative from the thread.

---

## Step 2 — Extract from the session arc

From **this thread** (visible context), **plus** transcript tail or full read from Step 1 when present, **plus** an **operator one-line steer** if the arc is thin, compress per **Thread depth and honesty** into:

- Main outcomes, strongest insights, decisions vs discussion
- Artifacts (paths, roles, existing vs proposed)
- Risks, tensions, critiques, open questions
- Recommended next steps, **suggested asks** for the receiving agent (Analyze…, Critique…, Compare…)

If context is thin, ask **one** short question before emitting the packet **only** when necessary; otherwise note uncertainty under **`## Thread coverage`** / **`## Current session purpose`** and proceed.

---

## Step 3 — Emit packet

Output **one** markdown block following **[harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)** — section order, **`## Agent surface`** with **Cursor model:** from the Cursor UI (see contract), **no** trailing **`coffee`**, **required final line** last per contract.

---

## After the paste — improve the ritual (no extra tooling)

**Optional operator habit** (scratch or mental note is enough): once the packet is in the **receiving** session, briefly score:

1. **Load** — Did the receiver skip re-discovery? (yes / partial / no)
2. **Accuracy** — Any wrong `{fact}` or missing caveat?
3. **Action** — Did **Suggested asks** produce useful work without scope creep?

**Recursive tightening:** If the **same friction** shows up **twice** (e.g. missing git-scope warning, wrong `##` headings, weak suggested asks), patch **[harvest-packet-contract](../../../docs/skill-work/work-cadence/harvest-packet-contract.md)** or **this skill** — not the Record. Optional: save an especially good packet under `harvest-packets/` as an informal quality bar.

**Cadence telemetry** (`log_cadence_event.py --kind harvest` or `session_harvest.py --log`) stays **optional**; this loop does not require it. When logging, pass **`--cursor-model`** (or **`CURSOR_MODEL`**) so the line matches bridge/coffee/dream **Agent surface** audit.

**Step 0 recent rhythm in reply:** **None.** Unlike **thanks** / **coffee** / **dream** / **bridge**, **harvest** does **not** prepend a read of `work-cadence-events.md`. The **Session Harvest Packet** is already the compressed handoff; adding the same rhythm strip would overlap the packet’s arc without clear load-bearing value. See [work-cadence README — Step 0 recent rhythm](../../../docs/skill-work/work-cadence/README.md#step-0-recent-rhythm-companion-facing).

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
| 2026-04-06 | Doc-only post-paste review loop (load / accuracy / action); recursive tighten contract or skill. |
| 2026-04-07 | Thread depth: soft 15–25 exchange heuristic; truncation honesty; transcript tail 200 / deep full-or-500; optional **## Thread coverage** in contract. |
