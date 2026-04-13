---
name: dream
preferred_activation: dream
description: "Grace-Mar night-close maintenance ritual. Primary trigger: dream. Dream is the end-of-day consolidation pass: a bounded maintenance ritual that settles continuity, checks integrity and governance, refreshes contradiction visibility, and prepares governed follow-up without merge authority. Agent steps also cover strategy-notebook closeout and Xavier journal day-file generation (see skill body). Before auto_dream.py runs, synthesize the previous eight events from work-cadence-events.md into **Recent rhythm** prose (no internal ops jargon or timestamps in chat). Usually one dream session per day."
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

1. **One sentence** — what tomorrow should pick up (mirror `tomorrow_inherits` in the JSON or say it in plain language).
2. **One letter** — the coffee menu lean from the handoff: **C** = Strategy / daily brief (`today_field`), **A** = Build (`build`), **B** = Steward / gate (`steward`) — from `execution_paths[suggested_execution_path_index]`. The next **`coffee`** Step 1 (`operator_daily_warmup.py`) prints a single line **`Dream → coffee menu:`** with the same mapping.

If **`auto_dream.py --strict`** halted, **`last-dream.json` was not updated** — yesterday’s file may still be on disk; do not treat the handoff as fresh until the next successful dream; fix integrity/governance first.

## Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `auto_dream.py` (and `operator_end_of_day.py`) append a new **`dream`** line when the pass completes successfully, so the log must be read **before** those commands if the rhythm read is to exclude this run.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 8** such lines already in the file. If there are fewer than eight, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in a short paragraph** using the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)): acknowledge the day's arc in *felt* terms (what was productive, what was settled, what was a good call), then name what **tomorrow inherits** — where the energy naturally goes next. Use **"we"** framing. The operator should feel **settled and ready to rest**, not debriefed. **Do not** put dates, clock times, commit hashes, or process names in this prose. Anchored in the actual eight log lines (no generic filler), but the day is *felt and closed forward*, not recapped. Script output below still carries the full machine snapshot.
4. Hold this synthesis for **What to return** — it belongs **at the top** of the night-close brief, before `self-memory` / integrity lines.

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

**Morning handoff:** When `apply=True` (the default), dream writes `users/grace-mar/last-dream.json` — a compact summary that tomorrow's `coffee` Step 1 (`operator_daily_warmup.py`) automatically picks up and displays as **"Last dream (night handoff)"**. This closes the choreography gap: coffee knows what dream found without the operator carrying it across threads. The JSON includes **`agent_surface.cursor_model`** (same meaning as bridge/harvest **Agent surface** / cadence **`cursor_model=`**): pass **`--cursor-model`** to `auto_dream.py` or set **`CURSOR_MODEL`** in the environment when running from a context that knows the Cursor UI label; otherwise **`unknown`**.

## What to return

Return a short night-close brief with:

- **Recent rhythm:** (synthesis from Step 0 — always first)
- **Phase:** which phase ran (`both`, `recent`, or `structural`)
- `self-memory` changed: yes/no *(recent phase)*
- integrity: pass/fail *(structural phase)*
- governance: pass/fail *(structural phase)*
- contradiction digest: total counts, plus **recent entries** (today's candidates) vs **structural entries** (older candidates) when phase=both
- artifact drafts: none / count
- **`dream_catchup` (since previous dream):** `local_calendar_dates`, `strategy_notebook_missing_day_headers`, `timezone`, `previous_dream_generated_at` — from `auto_dream.py` / `last-dream.json`; drives strategy-notebook stubs and Xavier `--catch-up-from-last-dream` (operational; not Record).
- **When present in `last-dream.json`:** coffee **24h rollup** (runs, mode mix, optional **menu picks** from `coffee_pick` cadence lines), **three execution paths** with **suggested index**: Steward when this run’s **integrity or governance failed**, else Steward when **gate pending > `max_pending_candidates`** (from `config/fork-config.json`), else **calendar mod-3** on tomorrow’s yearday; **`tomorrow_inherits`** one-liner (operational hint only); **civ-mem echoes** (default **one** hit above overlap threshold — each carries **“Analogy candidate only — not evidence, not recommendation, not Record”**; cite the disclaimer)
- **capability shift** (model category): sources checked / total, REVIEW alerts, monitor alerts — or "no alerts" if quiet
- one sentence on what tomorrow inherits from this run
- **Strategy notebook** / **Xavier journal:** one line each when those steps ran (see §§ above)

If nothing important changed, say so plainly. A quiet run is success.

**Done when:** The night-close brief is returned with all fields populated (or explicitly noted as unchanged), and the operator knows what tomorrow inherits.

## Example return shape

```md
## Dream

- Recent rhythm: (e.g. two work-start coffees, a thanks pause with a short park line, then bridge with two short commit refs)
- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 0, contradiction 0
- artifact drafts: none

- capability shift [model]: 6/6 sources — no alerts

Tonight's pass cleaned continuity and left no governed follow-up items.
```

Or, when something needs attention:

```md
## Dream

- Recent rhythm: (compressed rhythm from Step 0, no timestamps in chat)
- self-memory changed: yes
- integrity: pass
- governance: pass
- contradiction digest: reviewable 2, contradiction 1
- artifact drafts: 1 prepared

- capability shift [model]: 5/6 sources — 1 REVIEW (ASSUME-007), 2 monitor

Tonight's pass surfaced one contradiction worth governed review tomorrow; nothing was merged automatically.
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

## Strategy notebook (LIB-0153) — production closeout (**since previous dream**)

**Formal window (spec):** Production means ensuring a `## YYYY-MM-DD` daily block exists for **each local calendar date** in the **since-previous-dream** range — not only “today.” The range is computed **before** this run overwrites `last-dream.json`:

- Read `users/<id>/last-dream.json` **`generated_at`** (previous successful handoff). If **missing** (first dream ever): the window is **today only** in the catch-up timezone.
- Otherwise: all local dates **strictly after** the local calendar date of `generated_at`, **through today** (inclusive), in timezone **`DREAM_CATCHUP_TZ`** or **`TZ`** or **`UTC`**.

**Machine source of truth:** `python3 scripts/auto_dream.py --json` (or successful run’s written `last-dream.json`) includes **`dream_catchup`**: `local_calendar_dates`, `previous_dream_generated_at`, `timezone`, and **`strategy_notebook_missing_day_headers`** (dates in the window whose `## YYYY-MM-DD` heading is absent in the relevant `chapters/YYYY-MM/days.md` files). Use that object so agent and operator agree on **which days** need stubs or condense notes.

**Yes, it makes sense** if **dream** is the **end-of-day accountability point** that **initiates production closeout** for that window — not a second full `strategy` analysis pass, and not a substitute for daytime judgment.

**What “initiates production” means here**

- **During the day:** `coffee` / **`strategy`** (and linked briefs) may **capture** in [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) (paste-ready lines) or the operator may **draft directly** in [`chapters/YYYY-MM/days.md`](../../../docs/skill-work/work-strategy/strategy-notebook/chapters/YYYY-MM/days.md). **Assistants:** do **not** fold inbox into `days.md` on ingest alone; **fold** at **`dream`** (day-end, timestamp-aligned), when the operator **explicitly** directs (**`fold`**, intra-day cadence), or equivalent — see inbox § *Fold rhythm* and § **Fold** (see [`.cursor/skills/skill-strategy/SKILL.md`](../skill-strategy/SKILL.md)).
- **At `dream`:** For **each** date in `dream_catchup.local_calendar_dates` (or at minimum each date in `strategy_notebook_missing_day_headers`), ensure a **minimal** stub or filled block per [daily template](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#daily-entry-template) where missing (headings through **Open**; optional **Jiang** / **History resonance** as `none` or **deferred** when not used); align [`strategy-notebook/STATUS.md`](../../../docs/skill-work/work-strategy/strategy-notebook/STATUS.md) **Last daily entry** when page state changes.

**Strategy + WRITE on the page:** Sealing that day’s `## YYYY-MM-DD` block is where **`strategy`** judgment (architecture, links, optional lenses) and **`self-skill-write`** discipline (compression, voice, word budget — see [skills-modularity](../../../docs/skills-modularity.md)) **meet**: analysis and prose qualify each other. The notebook is **WORK** (not gate merge), but the integration is the same. Most drafting may happen in daytime **`strategy`**; **`dream`** is still the **scheduled accountability** where missing pieces, STATUS, and optional condense **ship** before sleep — or where a heavier strategy+write pass runs if that is when you work.

**Daily inbox → page (no mandatory reset):** If the operator uses [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) as an append-only buffer, **`dream`** is the default **day-end** fold into `chapters/YYYY-MM/days.md` for the **timestamp-matching** date (synthesize into Signal / Judgment / Links / Open — not a raw dump). **Manual fold** during the day is also valid when the operator directs (same synthesis rules). Pull **URLs and load-bearing claims** from **paste-ready** lines into **`### Links`** and Judgment as appropriate; micro-format spec: inbox § *Paste-ready one-liner* only (do not restate here). **Do not** automatically zero the rolling file each dream unless the operator asks; **prune** when the scratch section exceeds **~20000 characters** (drop oldest content first in **~5000-character blocks** until **≤ ~20000**). See [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox*.

**Optional — fold learning ledger:** After a fold, the operator may append one line with [`scripts/log_strategy_fold.py`](../../../scripts/log_strategy_fold.py) (`--fold-kind dream` when this pass folded the inbox) and run [`scripts/report_strategy_fold_learning.py`](../../../scripts/report_strategy_fold_learning.py) on a schedule — see [FOLD-LEARNING.md](../../../docs/skill-work/work-strategy/strategy-notebook/FOLD-LEARNING.md). **Not** required for `dream` to complete.

**Optional — thread touch on fold:** When folding [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) into **`days.md`**, if lines contain **`thread:<id>`**, the agent **may** add **one bullet** under **`### Open`** for that date: **which** `thread_id`s appeared and **one** **pairing or tension** worth carrying (from [strategy-commentator-threads.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md)). **Skip** if no `thread:` tags, if **Open** is already crowded, or if the operator opts out. **Do not** append a separate weekly rollup file by default — **optional** monthly **`meta.md`** one-liner remains operator-directed. WORK only.

**Same pattern — Xavier journal:** [daily-xavier-journal-inbox.md](../../../docs/skill-work/work-xavier/xavier-journal/daily-xavier-journal-inbox.md) folds into **`inbox/YYYY-MM-DD.md`**; optional manual clear; **prune** when scratch exceeds **~20000 characters** (from the top in **~5000-character blocks** until **≤ ~20000**); then run digest as in § *Xavier journal* below.

**Same pattern — dev journal:** [daily-dev-journal-inbox.md](../../../docs/skill-work/work-dev/dev-journal/daily-dev-journal-inbox.md) folds into **`YYYY-MM-DD-day-NN.md`** in [dev-journal](../../../docs/skill-work/work-dev/dev-journal/README.md); optional clear; **same prune rule** (**~20000** / **~5000** blocks).

**Agent behavior when `dream` is invoked**

1. After **Step 0** (Recent rhythm), run Step 1 (`auto_dream.py`) **or** read `--json` output / `last-dream.json` for **`dream_catchup`**.
2. Open active (and span) month **`days.md`** files as needed for the date range; cross-check **`strategy_notebook_missing_day_headers`**.
2b. If [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) has content for today’s date, **fold** it into the matching **`## YYYY-MM-DD`** block (synthesize; do not paste raw inbox wholesale). Route material from **paste-ready** lines into **`### Links`** / Judgment per synthesis rules above. **Do not** auto-clear the inbox unless the operator asks; if scratch length exceeds **~20000 characters**, **prune** from the top in **~5000-character blocks** until **≤ ~20000**.
2c. If [daily-xavier-journal-inbox.md](../../../docs/skill-work/work-xavier/xavier-journal/daily-xavier-journal-inbox.md) has content, **fold** into **`inbox/YYYY-MM-DD.md`** for that date; if scratch length exceeds **~20000 characters**, **prune** from the top in **~5000-character blocks** until **≤ ~20000**; then proceed with Xavier digest / catch-up as below.
2d. If [daily-dev-journal-inbox.md](../../../docs/skill-work/work-dev/dev-journal/daily-dev-journal-inbox.md) has content, **fold** into the correct **`YYYY-MM-DD-day-NN.md`** under dev-journal; **same prune rule** if needed.
3. For **each missing** `## YYYY-MM-DD` — add a **minimal** stub (Signal + Judgment one line each + Links) *or* report a **notebook gap** in the night-close brief (operator preference).
4. If any block is **over** the word budget — note **condense required**; run [condense-to-target](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#condense-to-target-mechanism-fit-1000-words) **only** if the operator asks in the same `dream` message to **ship** the edit (otherwise defer).
5. **Do not** add long lens/DEMO bodies during dream by default; **outboard** heavy material per architecture.

**Boundaries:** **WORK only** — not Record, not `self.md` / EVIDENCE / gate merge. **No** autonomous promotion to [`STRATEGY.md`](../../../docs/skill-work/work-strategy/STRATEGY.md) unless the operator explicitly asks (same rule as `skill-strategy`).

**Return brief:** **Strategy notebook:** `ok` / `stubs for [dates]` / `condense deferred` / `gap noted` — cite **`dream_catchup`** dates when useful.

## Xavier journal (LIB-0154) — page generation (**since previous dream**)

**Purpose:** At **`dream`**, **generate** (or confirm) **one journal file per local day** in the **same since-previous-dream window** as strategy-notebook (see above). Different artifact; same temporal contract.

**Mechanism:** [`scripts/xavier_journal_ob1_digest.py`](../../../scripts/xavier_journal_ob1_digest.py) builds **`YYYY-MM-DD.md`** from **Cici** (OB1) GitHub commits per calendar day (journal ordinal **Day N** inside the file), optional **`inbox/`** markdown (after any fold from [daily-xavier-journal-inbox.md](../../../docs/skill-work/work-xavier/xavier-journal/daily-xavier-journal-inbox.md)), optional **`--full-day-synthesis`** (strategy-notebook same-day block + session-transcript), per-flag includes, and optional **artifact** paths — see [xavier-journal README](../../../docs/skill-work/work-xavier/xavier-journal/README.md) and [SYNTHESIS-SOURCES.md](../../../docs/skill-work/work-xavier/xavier-journal/SYNTHESIS-SOURCES.md).

**Catch-up (formal):** From repo root, with operator `TZ` aligned to **`dream_catchup.timezone`** when possible:

```bash
TZ=America/New_York python3 scripts/xavier_journal_ob1_digest.py --catch-up-from-last-dream --full-day-synthesis --write
```

This reads **`users/<id>/last-dream.json` before overwrite**, computes the same local dates as `dream_catchup`, and writes **one file per day** (skips existing files unless **`--force`**). **`--full-day-synthesis`** embeds **strategy-notebook** + **session-transcript** for each date (omit it for git+inbox only). Dry-run: omit `--write` to print the date list only. Each day picks up matching **`inbox/YYYY-MM-DD.md`** (and folder / artifacts) if present.

**Agent behavior when `dream` is invoked**

1. After **Step 0**, run Step 1 (`auto_dream.py`) so **`dream_catchup`** is fresh in JSON / handoff; then run the **catch-up** command above on a **network**-capable path (operator machine or agent with `full_network`).
2. Optional: `GITHUB_TOKEN` / `GH_TOKEN` for API rate limits — public repo works for light use.
3. Optional: operator drops Cursor exports or notes into **`docs/skill-work/work-xavier/xavier-journal/inbox/`** before catch-up (same-day file names). For **transcript + geopolitical synthesis** on the journal page, prefer **`--full-day-synthesis`** (or `XAVIER_JOURNAL_FULL_DAY_SYNTHESIS=1`) so **strategy-notebook** and **session-transcript** merge in; use inbox for spillover.
4. If **GitHub API** or **network** fails, record **Xavier journal:** `skipped (API/network)` — do **not** fail the whole `dream` maintenance story on this alone.

**Boundaries:** **WORK / operator coaching** — not Xavier’s **Record** in her repo, not grace-mar **SELF** / gate merge. **No secrets** in prose (generated overview + commit links are safe; inbox/session content is operator-vetted).

**Return brief:** **Xavier journal:** `catch-up written N file(s)` / `skipped (exists|network)` — list paths or dates.

## Dev journal (LIB-0155) — optional fold

**Purpose:** Same **rolling inbox → fold** contract as strategy-notebook and Xavier (no mandatory nightly reset; length-based prune) — see [daily-dev-journal-inbox.md](../../../docs/skill-work/work-dev/dev-journal/daily-dev-journal-inbox.md) and [dev-journal README](../../../docs/skill-work/work-dev/dev-journal/README.md). No digest script; the agent **synthesizes** into **`docs/skill-work/work-dev/dev-journal/YYYY-MM-DD-day-NN.md`** when the operator uses the buffer.

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

`coffee`, `dream`, and `bridge` form Grace-Mar's cadence triad; **`thanks`** is a **light pause** (telemetry + optional park line + synthesis of prior two events — see [.cursor/skills/thanks/SKILL.md](../thanks/SKILL.md)).

| Time | Ritual | What it does |
|------|--------|-------------|
| **Morning** | `coffee` (work-start) | Read dream handoff, grounding scripts, **A–E** menu |
| **During day** | `coffee` (reorientation) | Re-sip as needed — many per day is normal |
| **During day** | `thanks` (micro-pause) | Synthesis of prior two log events (recent rhythm) + optional park + one telemetry line — no maintenance stack |
| **End of day** | `dream` | Memory normalization, integrity, governance, contradiction digest; **strategy-notebook** closeout + **Xavier journal** day file generation (see §§ Strategy notebook, Xavier journal) |
| **Session close** | `bridge` | Seal repos (commit/push), synthesize transfer prompt for next session |

**Dream's role is maintenance, not session closure.** Dream settles continuity and writes the handoff artifact. It does not commit, push, or produce a transfer prompt. If the operator is also closing the Cursor session, `bridge` follows dream.

| Scenario | Path |
|----------|------|
| End of day + closing session | `dream` then `bridge` |
| End of day, keeping session | `dream` alone |
| Mid-day, closing session | `bridge` alone (no dream needed) |

**One-command bundle:** `python3 scripts/operator_end_of_day.py -u grace-mar` runs dream + handoff-check. If also closing the session, say `bridge` afterward.

**Morning pickup:** `operator_daily_warmup.py` reads `last-dream.json` and displays a **collapsed** “Last dream” block by default; use **`--verbose-dream`** for full paths, civ-mem snippets, and followups.

For the full decision tree including signing-off **`coffee`** (lightweight alternative to bridge), see [bridge SKILL.md](../bridge/SKILL.md).

**Deeper choreography** (ordering, data flow, synthesis depths, harvest vs clocks): [work-cadence README — Cadence choreography](../../../docs/skill-work/work-cadence/README.md#cadence-choreography).

## Cadence audit

Each successful dream run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required; the line includes **`cursor_model=…`** (see **Morning handoff** above for how to set it). **`operator_end_of_day.py`** forwards **`--cursor-model`** to `auto_dream.py`.

## Related files

- `docs/skill-work/work-dream/README.md` — territory doctrine and boundaries
- `docs/skill-work/work-dream/work-dream-history.md` — design history (architecture changes, not per-run telemetry)
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/coffee/SKILL.md` — morning-side counterpart
- `.cursor/skills/thanks/SKILL.md` — micro-pause (not a substitute for dream)
- `.cursor/skills/bridge/SKILL.md` — session-scale handoff
- `scripts/detect_capability_shift.py` — capability shift detector (live fetch during dream; cached in warmup)
