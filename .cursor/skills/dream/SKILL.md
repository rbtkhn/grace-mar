---
name: dream
preferred_activation: dream
description: "Grace-Mar night-close maintenance ritual. Primary trigger: dream. Dream is the end-of-day consolidation pass: a bounded maintenance ritual that settles continuity, checks integrity and governance, refreshes contradiction visibility, and prepares governed follow-up without merge authority. Agent steps also cover strategy-notebook closeout and Cici notebook day-file generation (see skill body). Before auto_dream.py runs, synthesize the last four cadence lines (eight when the operator asks for full day-close rhythm) from work-cadence-events.md into **Recent rhythm** prose (no internal ops jargon or timestamps in chat). Usually one dream session per day."
---

# Dream

**Preferred activation (operator):** say **`dream`**.

`dream` is not another work-start ritual. `dream` is the **end-of-day consolidation pass**.

Its purpose is to help the system settle, compress, and prepare for tomorrow. A dream session does not try to push work forward aggressively. It closes the day by cleaning continuity, checking integrity, refreshing contradiction visibility, and surfacing any governed follow-up that tomorrow may need.

Normally there is only one `dream` session per day, near the end of the day. Extra `dream` runs are allowed, but they are exceptional rather than the norm.

## Design intent

`dream` should feel like closure, settling, and quiet integration. It should not feel like another stimulant or another planning sprint. Because `dream` is a consolidation ritual, it should be bounded, calm, and trustworthy: enough maintenance to reduce entropy, but never so much autonomy that it blurs governance or begins acting like a second operator.

## Success condition

A `dream` succeeds if, after using it, the system feels quieter, cleaner, and better prepared for tomorrow.

Its success condition is not dramatic change. Its success condition is that continuity is lighter, integrity is confirmed, contradiction visibility is refreshed, and no ungated mutation has occurred.

## Cadence

`dream` is normally a once-per-day closeout ritual.

Typical use:
- near the end of the day
- after the last substantial work block
- before sleep or final sign-off
- before handing the system forward to tomorrow's `coffee`

Extra runs are allowed when needed, especially for:
- dry-run inspection
- recovery after an unusual maintenance event
- explicit operator request

But the default pattern is:
- many `coffee` sessions are normal
- one `dream` session is normal

## Five-second closeout (operator)

Optional but high-leverage before leaving the dream thread after a **successful** `auto_dream.py` (writes `last-dream.json`):

1. **Primary** — **one** sentence for tomorrow: mirror **`tomorrow_inherits`** from `last-dream.json` (or the same idea in plain language). That field is the main human-facing hint; do not stack it with unrelated “do next” lists.
2. **Secondary** — the coffee menu letter (**A** Steward / **B** Engineer / **C** Historian) from `execution_paths[suggested_execution_path_index]` only if it **adds** something beyond the inherits line, or if you need to align with **`Dream → coffee menu:`** on the next **`coffee`** Step 1 (`operator_daily_warmup.py`). Dream paths do **not** emit **D** / **E** — those are operator picks on the full hub. If the letter and `tomorrow_inherits` **conflict**, say so in **one** clarifying sentence—do not present three parallel “tomorrow” signals without priority.

If **`auto_dream.py --strict`** halted, **`last-dream.json` was not updated** — yesterday’s file may still be on disk; do not treat the handoff as fresh until the next successful dream; fix integrity/governance first (see **When `--strict` halts** below).

## Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `auto_dream.py` (and `operator_end_of_day.py`) append a new **`dream`** line when the pass completes successfully, so the log must be read **before** those commands if the rhythm read is to exclude this run.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. **How many lines:** **Default: last 4** (lighter, aligned with coffee/bridge depth). **Full day-close: last 8** when the operator signals a wider rhythm window—e.g. **`dream full`**, **`deep rhythm`**, **`wide rhythm`**, or explicit ask for the full cadence tail. If fewer lines exist than requested, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in a short paragraph** using the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)): acknowledge the day's arc in *felt* terms (what was productive, what was settled, what was a good call), then name what **tomorrow inherits** — where the energy naturally goes next. Use **"we"** framing. The operator should feel **settled and ready to rest**, not debriefed. **Do not** put dates, clock times, commit hashes, or process names in this prose. Anchor in the **actual** log lines you read (no generic filler); the day is *felt and closed forward*, not recapped. Script output below still carries the full machine snapshot.
4. Hold this synthesis for **What to return** — it belongs **at the top** of the night-close brief, before run status / integrity lines.

If the file is missing or empty below the anchor, note that under **Recent rhythm** and continue.

## Step 1 — Automated actions

Run the bounded maintenance pass:

```bash
python3 scripts/auto_dream.py
```

For the stricter maintenance variant:

```bash
python3 scripts/auto_dream.py --strict
```

For a specific phase only (see *Two-phase substrate separation* below):

```bash
python3 scripts/auto_dream.py --phase recent       # memory + fresh digest only
python3 scripts/auto_dream.py --phase structural    # integrity + governance only
python3 scripts/auto_dream.py --phase both          # default: full pass
```

Alternative via swarm bridge (same underlying logic):

```bash
python3 auto-research/swarm/orchestrator.py dream
```

**End-of-day bundle (optional):** To run dream + handoff-check in one pass (night-side equivalent of `operator_reentry_stack.py`):

```bash
python3 scripts/operator_end_of_day.py -u grace-mar
```

**civ-mem checkout vs CI pin (optional):** When the day’s work leaned on tri-frame civ-mem routing, `bash scripts/check_civ_mem_upstream_pin.sh` checks that `research/repos/civilization_memory` `HEAD` matches the SHA in `docs/ci/civilization_memory_upstream.env`. No local checkout prints a skip line and exits successfully; a mismatch exits non-zero so you can re-clone or checkout the pinned commit before the next strategy pass.

The ritual should:

1. normalize `self-memory.md` (optional **length prune** when the file is very large: `python3 scripts/prune_self_memory.py -u <id> --dry-run` then `--apply`; see [memory-template.md](../../../docs/memory-template.md) § *Lifespan & decay*)
2. run integrity checks
3. run governance checks
4. refresh the derived contradiction digest
5. prepare governed artifact drafts if needed
6. emit one maintenance summary/event

`dream --strict` is the same ritual in a sharper maintenance posture: stricter integrity parity, stricter contradiction classification, clearer failure states, and fail-fast closeout when checks do not pass. It does not change companion-facing tone, canonical memory surfaces, or merge authority.

This is a maintenance pass, not a merge pass.

**Done when:** `auto_dream.py` exits successfully (or `--strict` halts with a clear reason), and script output is captured for the return brief.

**Memory observability:** After a successful non-dry-run dream, `auto_dream.py` may rebuild `artifacts/memory/memory-observability.md` and `.json`. If the resulting dashboard is `watch`, `stale`, or `missing`, return exactly one **`Memory observability:`** line after the dream summary. Do not block dream if the rebuild fails; treat any rebuild failure as a non-blocking `watch` line. Do not paste the full dashboard into dream.

**Morning handoff:** When `apply=True` (the default), dream writes `users/grace-mar/last-dream.json` — a compact summary that tomorrow's `coffee` Step 1 (`operator_daily_warmup.py`) automatically picks up and displays as **"Last dream (night handoff)"** (or a **one-line quiet handoff** when there is nothing to surface). This closes the choreography gap: coffee knows what dream found without the operator carrying it across threads. The JSON may include optional **`last_coffee_echo`** (derived from the same 24h coffee rollup as `coffee_rollup_24h`—a short narrative hint about the last session, not canonical memory or Record). The JSON includes **`agent_surface.cursor_model`** (same meaning as bridge/harvest **Agent surface** / cadence **`cursor_model=`**): pass **`--cursor-model`** to `auto_dream.py` or set **`CURSOR_MODEL`** in the environment when running from a context that knows the Cursor UI label; otherwise **`unknown`**.

**Conductor compression:** Successful dream handoff may also include **`conductor_rollup_24h`**: a WORK-only compression of recent Conductor picks and outcomes (`last_master`, `completed_passes`, `orientation_only`, `off_menu_refusals`, recent commits/falsifiers, and a one-line echo for coffee). This is compression, not continuation: dream does not generate fresh Conductor options, does not auto-compose notebooks, and treats off-menu/no-action outcomes as parked/refused telemetry rather than as another menu choice.

## What to return

Use a **short default brief** every time. Add **Details** only when load-bearing (failure, noteworthy counts, operator asked) — do not fill every optional slot on a quiet run.

### Default brief (always)

- **Recent rhythm:** Step 0 synthesis — **first**.
- **Run status:** phase (`both` | `recent` | `structural`), whether the run **ok** / quiet; **self-memory** changed yes/no; integrity / governance **pass | fail | skipped** (when a phase skips those checks, say so).
- **One closing sentence** — e.g. quiet run is success, or what needs attention tomorrow (no merge authority).

### Primary tomorrow hint

- Prefer **one** line from **`tomorrow_inherits`** (script stdout / `last-dream.json`) when present. The coffee **execution path** letter (**A** Steward / **B** Engineer / **C** Historian) and **`Dream → coffee menu:`** are **derived** hints—see **Five-second closeout**. Do **not** stack **`tomorrow_inherits` + path letter + civ-mem + rollup** as separate “do tomorrow” orders without stating priority; **tomorrow_inherits wins** unless you note a direct conflict.

### Details — expand when load-bearing

Include only what matters this run:

- Contradiction digest totals; **recent vs structural** entry counts when `phase=both`
- Artifact drafts: none / count
- **`dream_catchup`:** local dates, `strategy_notebook_missing_day_headers`, timezone, `previous_dream_generated_at` — FYI for calendar coverage; drives Cici notebook `--catch-up-from-last-dream` (operational; not Record)
- Coffee **24h rollup**, **execution paths** + suggested index, **civ-mem echoes** (with **“Analogy candidate only — not evidence, not recommendation, not Record”** when cited)
- **Capability shift** (sources, REVIEW / monitor alerts)
- **Strategy notebook** / **Cici notebook** / **Dev journal:** one line each when relevant (strategy-notebook **deferred** unless operator asked **`strategy page`**, **`strategy page compose`**, or **EOD notebook compose** in-thread; Cici notebook per § below)
- **`last30days` breadcrumb (advisory only):** If strategy residue needs fresh external provenance, mention at most **one** tomorrow query; see the strategy-notebook behavior below.
- **`raw-input` hygiene (advisory):** If cadence shows pasted **strategy inputs** (long verbatim + URL) today, note whether **`docs/skill-work/work-strategy/strategy-notebook/raw-input/`** already holds matching captures — **WORK only**; not merge authority. When unsure, suggest confirming paths or running [`scripts/strategy_raw_input_gap_hint.py`](../../../scripts/strategy_raw_input_gap_hint.py) (**advisory** heuristic).

If nothing important changed, say so plainly. A quiet run is success.

**Done when:** The operator sees **Recent rhythm**, **run status**, and **what tomorrow inherits** (or explicit “unchanged / quiet”); Details are optional unless something failed or stands out.

## Example return shape

**Quiet run:**

```md
## Dream

- Recent rhythm: (short felt closeout from Step 0 — no timestamps)
- Run status: phase=both; ok; self-memory changed: no; integrity: pass; governance: pass

Tonight's pass was quiet; handoff is fresh for tomorrow's coffee.
```

**Something to review:**

```md
## Dream

- Recent rhythm: (short felt closeout from Step 0)
- Run status: phase=both; self-memory changed: yes; integrity: pass; governance: pass
- Details: contradiction digest — reviewable 2, contradiction 1; artifact drafts: 1 prepared; capability shift: 1 REVIEW (ASSUME-007)

Tomorrow: skim reviewable digest rows; nothing was merged automatically.
```

## Two-phase substrate separation

Dream's maintenance pass separates work into two phases, inspired by Kjaerby et al. (Nature 2024) showing that non-REM sleep alternates between substates that replay recent vs. older memories in distinct temporal windows to prevent catastrophic forgetting.

**Phase A — Recent:** Memory normalization + contradiction digest entries from today. Focuses on what this session or day introduced — fresh signals, new candidates, recent changes to `self-memory.md`. This phase runs quickly (no subprocess calls to integrity or governance checkers).

**Phase B — Structural:** Integrity checks + governance checks + contradiction digest entries from before today. Focuses on long-horizon health — file parity, export freshness, template drift, rule compliance. This phase runs the full validation sub-processes.

The default (`--phase both`) runs both phases sequentially and tags the output so the night-close brief and tomorrow's coffee can see what came from each. Using `--phase recent` or `--phase structural` runs only that phase, which is useful for targeted checks or when time is short.

The `last-dream.json` handoff includes a `phases` object that separates results by source, so morning coffee can display recent signals and structural health independently.

## Governance doctrine (soft boundary)

**Suggestions** emitted by dream (execution path index, `tomorrow_inherits`, civ-mem echoes, coffee rollup) are **operational hints only**. They do **not** establish truth, priority, or policy, and must **never** substitute for gate review, integrity status, companion approval, or operator judgment. Cadence and handoff files are **not** a shadow Record.

## Strict halt and `last-dream.json`

When **`auto_dream.py --strict`** halts because integrity or governance failed, a **new** `last-dream.json` is **not** written (the previous file, if any, is left unchanged). Morning pickup may show an **older** handoff until the next successful dream. Rotation overrides, civ-mem echoes, and rollup fields apply to **successful** writes only.

### When `--strict` halts — recovery (three steps)

1. **Read the failure** — stderr and the **`auto_dream.py` stdout** (headline line first, then the rest). Identify whether integrity, governance, or another check failed.
2. **Fix operationally** — stale derived exports: [work-cadence README](../../../docs/skill-work/work-cadence/README.md) § *When integrity reports stale derived exports* and **Guardrails** below; governance / integrity per script messages; config or parity issues. **Do not** merge **RECURSION-GATE** candidates to “fix” integrity or governance.
3. **Re-run** — `python3 scripts/auto_dream.py --strict` after the fix; treat handoff as fresh only after **exit 0**.

---

## Strict halt repeats — doc-only loop

If **strict** dream halts for the **same** integrity or governance **reason** more than once, the fix is usually **operational** (refresh exports, resolve parity, adjust config) — not a gate merge.

**Recursive tightening:** Add **one** bullet to **this skill** (e.g. under *Step 1* or this section) or to `docs/skill-work/work-dream/README.md` describing the recurring cause and the **first** recovery step. Do not use this loop to bypass companion merge authority.

---

## Guardrails

- Do not create a new canonical memory surface.
- Do not treat strict mode as a global prompt override.
- Do not bypass `recursion-gate.md`.
- Do not directly rewrite `self.md` or `self-archive.md`.
- Do not let `dream` become an autonomous merge agent.
- Prefer bounded maintenance over speculative semantic intervention.
- A quiet run is normal; do not manufacture significance.
- If **integrity** fails with **stale derived export** (not contradictions), refresh exports: `bash scripts/regen_grace_mar_derived.sh` from repo root, then `python3 scripts/validate-integrity.py --user grace-mar --json` — see [`docs/skill-work/work-cadence/README.md`](../../../docs/skill-work/work-cadence/README.md) § *When integrity reports stale derived exports*.

## Strategy notebook (LIB-0153) — optional FYI; **not** owned by `dream`

**Contract (repo):** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Entry model* / § *End-of-day strategy session* — **hybrid** dated + episodic sections; **inbox + `raw-input/` = capture**, **notebook = synthesized** in the **EOD strategy session** when the operator says **`strategy page`**, **`strategy page compose`**, or runs **`strategy`** with **notebook compose** intent — **not** because night close ran. *Deprecated:* operator token **`weave`**.

**Morning conductor → night settle (optional):** If you ran a **[strategy coffee cadence (conductor protocol)](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md)** in the morning, the notebook holds **seeds** (`[watch]`, `[decision]`, `[promote]` only in WORK). **Step 0 “Recent rhythm”** in `dream` *may* acknowledge that arc in plain language (rehearsal → rest) when it helps closure — it does **not** add merge obligations, does **not** auto-compose `days.md`, and does **not** replace an explicit **`strategy` / EOD compose** when you want the notebook written.

**Telemetry only:** `python3 scripts/auto_dream.py` (and `last-dream.json`) still include **`dream_catchup`**: `local_calendar_dates`, `previous_dream_generated_at`, `timezone`, and **`strategy_notebook_missing_day_headers`** (dates in the catch-up window with no matching `## YYYY-MM-DD` in the relevant `chapters/YYYY-MM/days.md` files). Treat this as **optional FYI** if you track calendar coverage — **not** a mandatory stub list and **not** a reason for the agent to auto-write the notebook during `dream`.

**What `dream` does *not* do:** **`dream` does not** require **EOD-composing** [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) + [`raw-input/`](../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/README.md) into `days.md`, does **not** require minimal daily stubs, and does **not** replace a **`strategy`** **EOD session**. If the operator **asks** in the same `dream` thread to **compose the strategy notebook** / **fold** the strategy inbox, treat that as **explicit direction** — same synthesis rules as [skill-strategy](../skill-strategy/SKILL.md) / architecture § *Daily strategy inbox*.

**STATUS:** [STATUS.md](../../../docs/skill-work/work-strategy/strategy-notebook/STATUS.md) tracks **last substantive entry** when you close real work — update there after **EOD compose**; `dream` does not bump it by default.

**Optional — fold learning ledger:** After **EOD compose**, the operator may append one line with [`scripts/log_strategy_fold.py`](../../../scripts/log_strategy_fold.py) and run [`scripts/report_strategy_fold_learning.py`](../../../scripts/report_strategy_fold_learning.py) — see [FOLD-LEARNING.md](../../../docs/skill-work/work-strategy/strategy-notebook/FOLD-LEARNING.md). **Not** required for `dream` to complete.

**Optional — thread touch on compose:** When composing inbox into **`days.md`**, if lines contain **`thread:<id>`**, the agent **may** add **one bullet** under **`### Foresight`** (from [strategy-commentator-threads.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md)) **only when the operator directed that compose** — not by default at `dream`.

**Other lanes:** Cici and dev journals keep their own **inbox → compose / fold** habits — see **§ Cici notebook** and **§ Dev journal** below (`dream` may still run those when the operator expects it; strategy-notebook does not inherit that obligation).

**Agent behavior when `dream` is invoked (strategy notebook)**

1. After Step 1, you **may** read **`dream_catchup.strategy_notebook_missing_day_headers`** and mention it **one line** in the night-close brief if useful — **or skip** if the operator does not calendar-track the notebook.
2. **Do not** auto-compose strategy notebook, **do not** add stubs, **do not** edit `days.md` unless the operator **explicitly** asks in this thread.
3. If strategy residue needs fresh external provenance, recommend at most **one** `last30days "<topic>"` as a tomorrow breadcrumb; do not run it inside dream unless the operator explicitly asks for research in that same message.
4. If the operator **explicitly** asks to run **`strategy page`**, **`strategy page compose`**, **EOD strategy notebook**, fold strategy inbox, or add stubs in the same message, follow [skill-strategy](../skill-strategy/SKILL.md) and architecture; otherwise defer to a later **`strategy`** session.

**Boundaries:** **WORK only** — not Record, not `self.md` / EVIDENCE / gate merge.

**Return brief:** **Strategy notebook:** `deferred` / `FYI missing headers: …` / `composed (operator asked)` — as applicable.

## Cici notebook (LIB-0154) — page generation (**since previous dream**)

**Purpose:** At **`dream`**, **generate** (or confirm) **one journal file per local day** in the **same since-previous-dream window** as strategy-notebook (see above). Different artifact; same temporal contract.

**Mechanism:** [`scripts/cici_journal_ob1_digest.py`](../../../scripts/cici_journal_ob1_digest.py) builds **`YYYY-MM-DD.md`** from **Cici** (OB1) GitHub commits per calendar day (journal ordinal **Day N** inside the file), optional **`inbox/`** markdown (after any fold from [daily-cici-notebook-inbox.md](../../../docs/skill-work/work-cici/cici-notebook/daily-cici-notebook-inbox.md)), optional **`--full-day-synthesis`** (strategy-notebook same-day block + session-transcript), per-flag includes, and optional **artifact** paths — see [cici-notebook README](../../../docs/skill-work/work-cici/cici-notebook/README.md) and [SYNTHESIS-SOURCES.md](../../../docs/skill-work/work-cici/cici-notebook/SYNTHESIS-SOURCES.md).

**Catch-up (formal):** From repo root, with operator `TZ` aligned to **`dream_catchup.timezone`** when possible:

```bash
TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py --catch-up-from-last-dream --full-day-synthesis --write
```

This reads **`users/<id>/last-dream.json` before overwrite**, computes the same local dates as `dream_catchup`, and writes **one file per day** (skips existing files unless **`--force`**). **`--full-day-synthesis`** embeds **strategy-notebook** + **session-transcript** for each date (omit it for git+inbox only). Dry-run: omit `--write` to print the date list only. Each day picks up matching **`inbox/YYYY-MM-DD.md`** (and folder / artifacts) if present.

**Agent behavior when `dream` is invoked**

1. After **Step 0**, run Step 1 (`auto_dream.py`) so **`dream_catchup`** is fresh in JSON / handoff; then run the **catch-up** command above on a **network**-capable path (operator machine or agent with `full_network`).
2. Optional: `GITHUB_TOKEN` / `GH_TOKEN` for API rate limits — public repo works for light use.
3. Optional: operator drops Cursor exports or notes into **`docs/skill-work/work-cici/cici-notebook/inbox/`** before catch-up (same-day file names). For **transcript + geopolitical synthesis** on the journal page, prefer **`--full-day-synthesis`** (or `CICI_JOURNAL_FULL_DAY_SYNTHESIS=1`) so **strategy-notebook** and **session-transcript** merge in; use inbox for spillover.
4. If **GitHub API** or **network** fails, record **Cici notebook:** `skipped (API/network)` — do **not** fail the whole `dream` maintenance story on this alone.

**Boundaries:** **WORK / operator coaching** — not Xavier’s **Record** in her repo, not grace-mar **SELF** / gate merge. **No secrets** in prose (generated overview + commit links are safe; inbox/session content is operator-vetted).

**Return brief:** **Cici notebook:** `catch-up written N file(s)` / `skipped (exists|network)` — list paths or dates.

## Dev journal (LIB-0155) — optional fold

**Purpose:** Same **rolling inbox → fold** contract as strategy-notebook and the Cici notebook (no mandatory nightly reset; length-based prune) — see [daily-dev-journal-inbox.md](../../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/daily-dev-journal-inbox.md) and [dev-journal README](../../../docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md). No digest script; the agent **synthesizes** into **`docs/skill-work/work-dev/dev-notebook/work-dev/journal/YYYY-MM-DD-day-NN.md`** when the operator uses the buffer.

**Return brief:** **Dev journal:** `inbox folded` / `empty` / `deferred` — cite path if written.

## Relation to coffee

`coffee` and `dream` form a biological-cognitive pair.

- **`coffee`** = repeated framing dose
- **`dream`** = end-of-day consolidation pass

`coffee` restores orientation, clarity, and agency.
`dream` settles continuity, checks integrity, and prepares tomorrow's state.

Multiple `coffee` sessions per day are normal.
Usually one `dream` session per day is normal.

`coffee` should feel like a sip.
`dream` should feel like sleep.

## Cadence choreography

`coffee`, `dream`, and `bridge` form Grace-Mar's cadence triad. **Mid-day depth:** **`coffee` hub E — Conductor** after **`coffee`** Step 1, or **standalone** **Conductor** ([conductor SKILL](../conductor/SKILL.md)) via master name / **`conductor`** without opening **`coffee`** — orientation + action MCQ + optional close. **`thanks`** is **deprecated** as a primary operator beat ([thanks SKILL](../thanks/SKILL.md)); prefer **conductor** or **`coffee` light/minimal** for pauses and re-grounding.

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, grounding scripts, fixed coffee menu (**A–E**) |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **During day** | `conductor` / hub **E** (Symphony / execution emphasis) | Master pick → orientation → Conductor action MCQ; `coffee_pick` + optional `coffee_conductor_outcome` — see [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest; optional strategy-notebook **FYI** + **Cici notebook** day file generation (see §§ Strategy notebook, Cici notebook) |
| **Session close** | `bridge` | Seal repos (commit/push), synthesize transfer prompt for next session |

**Dream's role is maintenance, not session closure.** Dream settles continuity and writes the handoff artifact. It does not commit, push, or produce a transfer prompt. If the operator is also closing the Cursor session, `bridge` follows dream.

| Scenario | Path |
|----------|------|
| End of day + closing session | `dream` then `bridge` |
| End of day, keeping session | `dream` alone |
| Mid-day, closing session | `bridge` alone (no dream needed) |

**One-command bundle:** `python3 scripts/operator_end_of_day.py -u grace-mar` runs dream + handoff-check. If also closing the session, say `bridge` afterward.

**Morning pickup:** `operator_daily_warmup.py` reads `last-dream.json` and displays a **collapsed** “Last dream” block by default (a **one-line quiet handoff** when there is nothing to flag; a fuller “night handoff” when there are signals). Optional **`--verbose-dream`** expands paths, civ-mem snippets, followups, and still appends any **`last_coffee_echo`** line.

For the full decision tree including signing-off **`coffee`** (lightweight alternative to bridge), see [bridge SKILL.md](../bridge/SKILL.md).

**Deeper choreography** (ordering, data flow, synthesis depths, harvest vs clocks): [work-cadence README — Cadence choreography](../../../docs/skill-work/work-cadence/README.md#cadence-choreography).

## Cadence audit

Each successful dream run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required; the line includes **`cursor_model=…`** (see **Morning handoff** above for how to set it). **`operator_end_of_day.py`** forwards **`--cursor-model`** to `auto_dream.py`.

## Related files

- `docs/skill-work/work-dream/README.md` — territory doctrine and boundaries
- `docs/skill-work/work-dream/work-dream-history.md` — design history (architecture changes, not per-run telemetry)
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/coffee/SKILL.md` — morning-side counterpart
- `.cursor/skills/thanks/SKILL.md` — **deprecated** micro-pause beat; prefer **conductor** / **`coffee` light**
- `.cursor/skills/bridge/SKILL.md` — session-scale handoff
- `scripts/detect_capability_shift.py` — capability shift detector (live fetch during dream; cached in warmup)
