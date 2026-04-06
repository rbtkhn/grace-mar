# work-cadence

**Purpose:** Template-level doctrine, boundaries, and architecture for the daily cadence triad — `coffee` (orientation), `dream` (consolidation), and `bridge` (session handoff) — plus **`thanks`** (micro-pause telemetry) and **`harvest`** as **operator tools on other axes** (harvest: cross-agent extraction; on demand, not a fourth clock). Executable triggers live in `.cursor/skills/coffee/SKILL.md`, `.cursor/skills/thanks/SKILL.md`, `.cursor/skills/dream/SKILL.md`, `.cursor/skills/bridge/SKILL.md`, and `.cursor/skills/harvest/SKILL.md`.

**Not** Record truth. **Not** a merge path. **Not** identity-relevant unless gated.

---

## Role

| Role | Description |
|------|-------------|
| **Cadence architecture** | Defines the shape of daily rhythm: coffee (orientation, repeated), thanks (micro-pause), dream (consolidation, once), bridge (session carry-forward), harvest (cross-agent packet; midstream import). |
| **Night-to-morning handoff** | Documents the `daily-handoff/night-handoff.json` data contract that bridges dream output to coffee Step 1. |
| **Cadence event audit** | Append-only telemetry via `work-cadence-events.md` and `scripts/log_cadence_event.py` (optional **`harvest`** kind for consistency). |
| **Boundary surface** | Explains what belongs in operational/ephemeral surfaces versus what must escalate to the gate. |
| **Script topology** | Maps how consolidated runners delegate to underlying brief generators. |

---

## Daily rhythm

`coffee`, `dream`, and `bridge` form the cadence triad:

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (standard) | Read dream handoff, context snapshot, skill focus, session options |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **End of day** | `dream` | Capture signal, set carry-forward, write handoff JSON |
| **Session close** | `bridge` | Seal (commit/push), synthesize transfer prompt for next session |

**Many coffees, one dream, one bridge.** `coffee` is for repetition. `dream` is for closure. `bridge` is for carry-forward.

`coffee` should feel like a sip. `dream` should feel like sleep. `bridge` should feel like sealing an envelope.

---

## Cadence choreography

**Choreography** means *who runs when*, *what each beat hands to the next*, and *how the operator stays oriented* without collapsing distinct jobs into one overweight ritual. It is not a moral schedule — it is a **failure-mode map**: each ritual answers a different kind of slip (framing decay, day residue, session amnesia, mid-day pause, cross-agent handoff).

### The beats (roles, not personalities)

| Beat | Clock | Primary job | Typical frequency |
|------|--------|-------------|-------------------|
| **coffee** | Hours (framing) | Reorientation: grounding, priorities, menu of next forks | Many per day |
| **thanks** | Minutes (pause) | Bookmark: optional park line + one telemetry line; **no** maintenance stack | As needed |
| **dream** | Day (residue) | Consolidation: memory normalize, integrity/governance, contradiction digest, night handoff | Usually once |
| **bridge** | Session (context) | Seal: commit/push where appropriate, transfer prompt for the **next** Cursor thread | Per session close |
| **harvest** | Cross-thread (import) | Ship dense substance **into** a session that is already running — not a clock | On demand |

**harvest** is **not** a fifth daily clock. It answers a different question: *how* to feed another agent or parallel session, not *when* to frame, settle, or seal.

### Order and pairing (common paths)

- **Morning after a dream:** `coffee` picks up `last-dream.json` / night-handoff context (see **Handoff contract** below). Dream already ran; coffee does not re-run dream.
- **Mid-day drift:** `coffee` again — a new sip, new Step 1 + menu. The cadence log shows the rhythm; it is normal to see several `coffee` lines in one day.
- **Stepping away briefly:** `thanks` — light telemetry + optional park text. It does **not** replace `coffee` for reorientation or `dream` for consolidation.
- **End of day, session continues:** `dream` alone — writes handoff artifacts; no commit/push requirement from dream itself.
- **End of day + closing Cursor:** `dream` then `bridge` — settle first, then seal and generate the transfer prompt.
- **Mid-day session end:** `bridge` alone — no obligation to run `dream` if the day is not closing.
- **End-of-day bundle:** `operator_end_of_day.py` chains dream-weight maintenance with handoff-check; if the operator is also **closing the session**, they still say **`bridge`** afterward for seal + transfer prompt.

Signing-off **`coffee`** (closeout mode) is a **lighter** alternative to `bridge` when the operator wants handoff-weighted text without full bridge mechanics — see [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) for the full decision tree.

### Data flow between beats (what crosses the boundary)

1. **Dream → morning coffee:** `users/<id>/daily-handoff/night-handoff.json` and, in grace-mar-style instances, `users/<id>/last-dream.json` — collapsed “Last dream” in warmup unless verbose flags are used.
2. **Bridge → next thread:** Transfer prompt (packet contract) — ends with a lone **`coffee`** line for cold start when that contract applies.
3. **All beats → audit trail:** [work-cadence-events.md](work-cadence-events.md) — one append-only line per successful leaf run (`scripts/log_cadence_event.py`). This file is **operator ephemera**: rhythm telemetry, not Record.

### Cadence tail synthesis (agent-facing)

Skills may ask the agent to **read** `work-cadence-events.md` **before** running scripts that **append** a new line at the end of the run, then **synthesize** recent events into the reply so the operator sees **recent rhythm** without opening the log.

| Ritual | Prior events synthesized | Rationale |
|--------|----------------------------|-----------|
| **thanks** | **2** | Minimal pause — just enough “what just happened” to anchor the bookmark |
| **coffee** | **4** | Reorientation — roughly half a day of mixed beats at typical spacing |
| **bridge** | **4** | Same depth as **coffee** — the next session almost always opens with **`coffee`** on the packet tail; matching tail length keeps seal → sip symmetric |
| **dream** | **8** | Day-close — wider window to see coffee/bridge/thanks/dream mix before consolidation |
| **harvest** | **none** | The **Harvest Packet** is already dense context for a midstream receiver; a cadence tail would duplicate rhythm info without adding load-bearing substance. Optional **`harvest`** cadence **telemetry** (`--log`) does not require synthesis in the reply |

Synthesis should be **plain prose**: a human-readable sense of **rhythm and mood** from the last *n* events — **not** a leading line of UTC timestamps or `key=value` telemetry (those stay in the log and in Step 1 script output). Compressed technical detail is optional **below** the prose if the operator asks. If the log is empty or short, skills specify fallbacks.

### Choreography vs governance

Choreography operates in **Maintenance / operational** territory. It does **not** approve gate candidates or merge the Record. The **integration moment** for identity remains the instance gate. Cadence can **surface** gate pressure (e.g. steward tracks in coffee); it does not **substitute** for companion approval.

### Where to read the executable spec

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) — Step 0 cadence tail, Step 1 scripts, A–E menu
- [.cursor/skills/thanks/SKILL.md](../../../.cursor/skills/thanks/SKILL.md) — pause beat + cadence tail (2)
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) — Step 0 cadence tail (8), `auto_dream.py`, handoff
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) — Step 0 cadence tail (4), seal + transfer prompt
- [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) — packet contract (no trailing `coffee`; no cadence tail synthesis)

---

## Why three rituals

Work fails on three clocks:

**The framing clock (hours).** During the day, orientation degrades under context load. Not lack of information — degraded framing. `coffee` restores it. Many sips per day.

**The residue clock (day).** By evening, unresolved threads, integrity drift, and unprocessed signals accumulate. `dream` settles them without dramatic mutation.

**The context clock (session).** At session boundaries, agent memory goes to zero. Everything not on disk is lost. `bridge` seals the session and produces a transfer prompt so the next thread starts oriented instead of blank.

Each clock needs its own ritual because the failure modes are different. Reorientation is not consolidation. Consolidation is not transfer. Merging them into one ritual would either make it too heavy for frequent use or too shallow for end-of-day closure.

---

## Fourth operator tool: cross-agent extraction (`harvest`)

**Not a fourth clock.** `coffee`, `dream`, and `bridge` answer **when** the operator needs framing, day-close residue, or session-boundary transfer. **`harvest`** answers **how** to ship dense session substance to **another agent or thread that is already running** (parallel review, tooling handoff, second Cursor session without a cold start). Thread narrative uses **soft** depth limits and explicit **truncation honesty** (skill § *Thread depth and honesty*).

- **Skill:** [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md)
- **Packet contract:** [harvest-packet-contract.md](harvest-packet-contract.md) (section headings; **no** trailing `coffee` — contrast [bridge-packet-contract.md](bridge-packet-contract.md))
- **Optional script:** `scripts/session_harvest.py` — checklist + template + optional `--log` → `log_cadence_event.py --kind harvest`

**Instances:** Built-from-template repos (e.g. grace-mar) reconcile cadence doc drift via their own upgrade workflow; the template remains the structural home for the skill and contract.

---

## Script topology

```
cadence-coffee.py
  ├─ reads/writes users/<id>/daily-handoff/last-coffee-state.json   (delta since last coffee; operational)
  ├─ writes users/<id>/daily-handoff/.coffee-run-context.json         (runner → brief; operational; gitignored in instance policy if desired)
  └─ good-morning-brief.py        context, bridges, session options, handoff pickup, coffeeOrientationHints
       └─ write_style_bridge.py   optional WRITE synthesis

cadence-dream.py
  └─ good-night-brief.py          signal capture, handoff write, gate suggestion
  └─ git status summary           uncommitted-work awareness
  └─ merge worktree triage        writes worktreeState / worktreeAdvice into night-handoff.json

bridge_last_state.py              (after successful bridge push; agent-run ritual)
  └─ users/<id>/daily-handoff/last-bridge-state.json   session-to-session delta for bridge packet; operational; gitignored
```

**Runners** are lightweight dispatch wrappers. **Briefs** hold all the parsing, bridge-building, and output logic. Instances may extend or replace the runners while keeping the briefs stable.

---

## Handoff contract

`dream` (via `good-night-brief.py --write-closeout`) writes `users/<id>/daily-handoff/night-handoff.json`.

`coffee` (via `good-morning-brief.py`) reads that file the next morning.

### night-handoff.json schema

| Field | Type | Purpose |
|-------|------|---------|
| `user` | string | Instance user id |
| `date` | ISO date | When dream ran |
| `mode` | string | Dream mode |
| `dayStatus` | string | `finished_well` / `partial` / `blocked` |
| `oneSignal` | string | Strongest signal from the day |
| `tomorrowTopAction` | string | Carry-forward action for morning |
| `stopCondition` | string | What not to overdo tomorrow |
| `optionalResetCue` | string | What to let go of tonight |
| `handoffSchemaVersion` | int | **2** = extended handoff (optional on legacy files) |
| `topActionReason` | string | Why `tomorrowTopAction` was chosen (heuristic; not identity truth) |
| `tomorrowEnergyFit` | string | `low` / `normal` / `high` — shapes stop-condition copy |
| `quietRun` | bool | When true, morning coffee may use softer framing |
| `activeLaneHint` | string | `GATE` / `WORK` / `SEED` / `NONE` — light lane foregrounding |
| `ignoreTomorrow` | string | Noise to deprioritize (complements stop condition) |
| `residueLedger` | object | At most one short string per bucket: `must_resume`, `safe_to_drop`, `blocked`, `watch_later` |
| `worktreeState` | string | `clean` / `light residue` / `risky residue` (from `cadence-dream.py`) |
| `worktreeAdvice` | string | Read-only triage line (still no commit/push in dream) |
| `gateSuggestions` | array | Strings or `{item, reason, urgency}` objects — advisory only |
| `warnings` | string[] | Parse/fallback warnings |

**Morning checkback (optional):** `good-morning-brief.py --write-checkback --checkback-helpful yes|no|partial` writes `morning-checkback-<YYYY-MM-DD>.json` under `daily-handoff/` (operational telemetry; not Record).

**Weekly reflection:** `weekly-reflection.json` in `daily-handoff/` is updated when dream runs in **reflective** mode.

The handoff artifact is an operational file, not identity truth. It should not be committed to the Record or treated as evidence.

---

## Gate threshold

`work-cadence` is **operational by default**.

Keep changes in territory docs when they are about:

- cadence architecture (what each ritual does, in what order)
- handoff contract shape and fields
- runner mode definitions and dispatch logic
- coffee/dream choreography and timing

Stage to the instance's gate (`recursion-gate.md` or `review-queue/`) only when a cadence insight would change governed behavior, such as:

- durable prompt or policy behavior
- changes to how identity-relevant signals are captured
- new surfaces that cross into Record territory

This territory never creates a merge path. The instance's gate remains the membrane.

---

## Modes reference

### Coffee modes

| Mode | Brief mode | Sync checks | Branch snapshot | When to use |
|------|-----------|-------------|-----------------|-------------|
| `standard` | `standard` | Only if `--check-sync` | Full | Most mornings |
| `light` | `minimal` | Only if `--check-sync` | Compact (one line) | Quick reorientation |
| `deep` | `deep` | Yes (automatic) | Full | Start of week, template updates |
| `closeout` | N/A (delegates to dream) | No | No | End of day (prefer `dream`) |

### Dream modes

| Mode | Duration | When to use |
|------|----------|-------------|
| `minimal` | ~1-2 min | Low-energy nights |
| `standard` | ~2-4 min | Most nights |
| `reflective` | ~4-6 min | End of sprint/week |

---

## Instance extensions

Instances built from this template may extend cadence with:

- **Custom menu systems** (e.g. grace-mar's A-H multi-choice pattern)
- **Additional maintenance passes** (e.g. integrity checks, contradiction digest, memory normalization)
- **Territory-specific tracks** (e.g. work-politics, Predictive History)
- **Instance-specific runners** (replacing or wrapping the template runners)

These extensions belong in instance-local skills and territories, not in this template. The template provides the structural pattern; instances customize for their needs.

---

## Cadence event audit

Each coffee, dream, bridge, and optional **harvest** run appends one line to [work-cadence-events.md](work-cadence-events.md) via `scripts/log_cadence_event.py`. This is operator-facing telemetry — not the Record, not self-memory.

**Emitters (typical):**
- **coffee** / **dream** / **bridge** — runner or agent logs after successful completion (see instance template)
- **harvest** — optional; operator or agent runs `session_harvest.py --log` or `log_cadence_event.py --kind harvest` after emitting a packet

**Leaf-only rule:** Orchestrator scripts (wrappers that chain multiple steps) do not emit their own events. Only the leaf ritual logs.

**Split threshold:** If cadence events exceed ~200 lines/month, consider adding a JSONL sibling and keeping monthly rollup bullets in the markdown file.

---

## Write authority map

Which on-disk surfaces each ritual reads, writes, and whether companion approval is required.

| Ritual | Reads | Writes | Gate required? |
|--------|-------|--------|---------------|
| **coffee** | self-memory, gate, dream handoff, git status | nothing (read-only planning) | No |
| **dream** | self-memory, SELF, EVIDENCE, gate | self-memory, night handoff JSON, cadence events | No (Maintenance mode) |
| **bridge** | self-memory, gate, dream handoff, territories, git | git commits, cadence events | No (operational) |
| **harvest** | same class as coffee (self-memory, gate, dream handoff, territories, git; optional session-transcript) | **default none**; optional operator-requested save under `work-cadence/harvest-packets/` or `last-harvest.md`; optional cadence event line | No |
| **gate merge** | gate candidates, SELF, EVIDENCE, prompt | SELF, EVIDENCE, prompt, session-log, gate, pipeline events | **Yes — companion approval required** |

**Key boundary:** coffee and bridge never write to identity surfaces. Dream writes to ephemeral/operational surfaces only. Only the gated merge path touches the Record.

---

## End-of-session decision tree

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals and generates transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repo, carry context forward; no maintenance needed |
| **Quick check before stepping away** | coffee closeout (instance-defined) | Lightweight status; no commit/push, no transfer prompt |

**Default:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

---

## Cadence troubleshooting

When a cadence run produces unexpected output, check these in order:

### Coffee output looks wrong

1. **Dream handoff missing?** Check the night handoff JSON — if absent or stale, dream didn't run or didn't complete.
2. **Wrong mode?** Check which mode was passed to the coffee runner. Run with the intended mode explicitly.
3. **Script failed silently?** Consolidated runners chain sub-scripts and stop on first failure. Check exit codes.

### Dream output looks wrong

1. **Integrity or governance failed?** Check the dream summary for failure flags. In strict mode, dream halts — no memory update, no handoff written.
2. **Handoff not written?** Dream only writes the handoff artifact when `apply=True` and maintenance is not halted.
3. **Cadence event not logged?** Gated on successful completion. Dry-run and halted dreams produce no cadence line by design.

### Bridge output looks wrong

1. **Commit failed?** Bridge commits are agent-driven. Check `git status -sb` in all relevant repos.
2. **Push rejected?** Usually means remote has new commits. Pull-rebase and retry.
3. **Transfer prompt thin?** Bridge synthesizes from on-disk state. Sparse sections mean those surfaces had nothing to report.
4. **Coffee didn’t run after paste?** The bridge transfer block should end with a lone line `coffee` per [bridge-packet-contract.md](bridge-packet-contract.md). If that line was dropped when copying, append `coffee` or re-copy from the bridge output.

### Harvest packet confusion

1. **Wrong ritual?** If the target session needs a **cold start**, use **`bridge`** (ends with `coffee`). **`harvest`** packets **must not** end with `coffee`; see [harvest-packet-contract.md](harvest-packet-contract.md).
2. **Thin narrative sections?** The script only prints paths and git; the agent fills outcomes from the **visible thread** (no full Cursor export API). Add a one-line operator steer or read `session-transcript.md` if the instance uses it.

### General

- **Which cadence events actually ran?** Check `work-cadence-events.md` — one line per run.
- **Agent reading stale skill file?** Long sessions can cache file contents. Ask the agent to re-read.
- **Runner vs skill mismatch?** If `cadence-coffee.py` / brief output disagrees with `.cursor/skills/coffee/SKILL.md`, update the **spec or skill** so the next run does not guess.

---

## Closing the troubleshooting loop (doc-only)

If the **same** troubleshooting bullet applies **twice in a short window**, add **one line** to the relevant **SKILL** or **packet contract** and optionally a **pointer** back into the subsection above. Instances that mirror grace-mar may align prose with grace-mar `docs/skill-work/work-cadence/README.md` § *Closing the troubleshooting loop*.

---

## Continuity and trail

`work-cadence` does **not** replace any existing continuity surface.

- **Spec docs:** `docs/good-morning-brief-spec.md`, `docs/good-night-brief-spec.md`, `docs/good-night-template.md`
- **Sync pack:** `docs/skill-work/self-work/sync-pack/` (optional territory sync module)
- **Operational handoff:** `users/<id>/daily-handoff/night-handoff.json`
- **Ephemeral memory:** `users/<id>/self-memory.md`
- **Governed changes:** Instance-specific gate (`recursion-gate.md` or `review-queue/`)

---

## Adjacent surfaces

- [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md) — coffee trigger
- [.cursor/skills/thanks/SKILL.md](../../../.cursor/skills/thanks/SKILL.md) — thanks micro-pause (cadence tail ×2)
- [.cursor/skills/dream/SKILL.md](../../../.cursor/skills/dream/SKILL.md) — dream trigger
- [.cursor/skills/bridge/SKILL.md](../../../.cursor/skills/bridge/SKILL.md) — bridge trigger
- [.cursor/skills/harvest/SKILL.md](../../../.cursor/skills/harvest/SKILL.md) — harvest trigger
- [harvest-packet-contract.md](harvest-packet-contract.md) — Session Harvest Packet contract
- [work-cadence-events.md](work-cadence-events.md) — per-run cadence telemetry
- [scripts/log_cadence_event.py](../../../scripts/log_cadence_event.py) — cadence event append helper
- [scripts/session_harvest.py](../../../scripts/session_harvest.py) — harvest checklist + optional template + `--log`
- [scripts/cadence-coffee.py](../../../scripts/cadence-coffee.py) — coffee runner
- [scripts/cadence-dream.py](../../../scripts/cadence-dream.py) — dream runner
- [scripts/good-morning-brief.py](../../../scripts/good-morning-brief.py) — morning brief generator
- [scripts/good-night-brief.py](../../../scripts/good-night-brief.py) — night brief generator
- [docs/good-morning-brief-spec.md](../../good-morning-brief-spec.md) — full morning spec
- [docs/good-night-brief-spec.md](../../good-night-brief-spec.md) — full night spec
- [docs/good-night-template.md](../../good-night-template.md) — recommended night sequence

---

## Scope boundaries

In scope:

- daily cadence architecture (coffee/dream/bridge triad + thanks micro-pause + harvest on a separate cross-agent axis)
- handoff contract design and schema
- cadence event audit (per-run telemetry)
- runner mode definitions and dispatch
- script topology and extension points
- boundary rules for operational vs gated content

Out of scope:

- instance-specific menu systems (A-H, etc.)
- instance-specific maintenance passes (integrity, governance, contradiction)
- Record merges or identity edits without the gate
- individual work-territory content (politics, dev, business, etc.)
- sync-pack mechanics (those live in `self-work/sync-pack/`)
