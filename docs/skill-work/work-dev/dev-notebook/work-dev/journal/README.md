# Dev journal — work-dev learning log

**Parent:** [Work notebook (multi-lane)](../../README.md) → **work-dev** lane — this subfolder is the **day-scale journal**; other lanes hold prompts/specs by territory. **Lane index (map + history):** [../README.md](../README.md).

**Discoverability:** The same tree is linked from **`users/grace-mar/SELF-LIBRARY/dev-journal`** (repo-relative symlink) for agents and tools that prioritize the companion tree. **LIB:** [LIB-0155](../../../../../../users/grace-mar/self-library.md#operator-analytical-books) in [`self-library.md`](../../../../../../users/grace-mar/self-library.md) (Operator analytical books).

**Book:** Short daily notes on **learning and building** the **work-dev** lane in grace-mar: OpenClaw / export–stage–merge discipline, harness and cadence wiring, integration scripts, capability contracts, portable skills, OB1 ↔ companion-self bridge thinking, and adjacent operator infrastructure — **without** treating WORK drafts as Record truth.

**Territory:** `docs/skill-work/work-dev/dev-notebook/work-dev/journal/` in grace-mar — **WORK / operator trajectory**, not the companion **Record**, not Voice knowledge, not a substitute for [work-dev-history.md](../../../work-dev-history.md) (append-only milestone log) or [workspace.md](../../../workspace.md) (canonical entrypoint).

### Routing: dev-journal vs cici-notebook

**One line:** **dev-journal** (this folder) = **inward-facing** — Grace-Mar’s own work-dev lane (tooling, integration, scripts in *this* repo). **cici-notebook** = **outward-facing** — Xavier’s OB1 / Cici stack and your coaching or tracking of it from inside grace-mar. See [cici-notebook README](../../../../work-cici/cici-notebook/README.md#routing-dev-journal-vs-cici-notebook).

**Center of gravity belongs here** when you are building or reflecting on grace-mar **internal** work-dev: OpenClaw, export–stage–merge discipline, harness/cadence wiring, integration scripts, capability contracts, portable skills, bridge thinking between OB1 and companion-self, and adjacent operator infrastructure.

**Write in [cici-notebook](../../../../work-cici/cici-notebook/README.md)** when the center of gravity is **Xavier’s** instance (Cici), upstream OB1, BrewMind tie-ins, same-day commits from Xavier’s repo, or what Xavier’s OB1 trajectory means operationally — including digest-driven day files from `scripts/cici_journal_ob1_digest.py`.

**Quick test**

- “In **Grace-Mar**, I changed / learned / wired …” → **dev-journal** (this folder).
- “In **Xavier’s** OB1/Cici world, I observed / coached / compared …” → **cici-notebook**.

**When a day touches both:** split — grace-mar implementation and tooling reflection **here**; Xavier/OB1 observation or coaching **there**.

**How to use**

- One file per **calendar day you choose to capture**: `YYYY-MM-DD-day-NN.md` (**NN** = journal day number from your chosen **anchor** — e.g. first entry = Day 1; skip days you do not journal).
- Keep entries **short** (about 10–20 lines): focus, actions, wins, blockers, one line for tomorrow.
- **No secrets** (API keys, raw Supabase URLs with keys, MCP secrets, private tokens). Reference env vars, script names, and doc paths only.

### Daily inbox (rolling accumulator)

**File:** [daily-dev-journal-inbox.md](daily-dev-journal-inbox.md) — **append-only** during the local day for rough work-dev capture. **`dream`** is the usual time to **fold** into the canonical **`YYYY-MM-DD-day-NN.md`** for that calendar window (create or extend the day file; **NN** follows your journal-day anchor). **No automatic reset** each dream — same **fold + optional prune** pattern as [strategy-notebook daily-strategy-inbox](../../../../work-strategy/strategy-notebook/daily-strategy-inbox.md). **Missed `dream`:** resolve stale inbox before appending on a new day (merge into the correct `*-day-NN.md`).

**Relation to other surfaces**

| Surface | Role |
|---------|------|
| **This journal** | Reflective **day-scale** narrative — what you understood, tried, or struggled with. |
| [work-dev-history.md](../../../work-dev-history.md) | **Milestone / artifact** log (commits, scripts shipped, gaps closed). |
| [workspace.md](../../../workspace.md) | **Current** blockers and next actions. |

**Contrast:** [cici-notebook](../../../../work-cici/cici-notebook/README.md) vs this journal — full routing rules under [Routing](#routing-dev-journal-vs-cici-notebook) above.

**vs [work-dev-history.md](../../../work-dev-history.md):** History = **milestones** (SHA, artifact, gap closed). Journal = **narrative** when useful — avoid copying every history bullet; link the date or commit and add friction / “what clicked” only the history line cannot carry.

### Conductor in dev journal

**When** you run [`.cursor/skills/conductor/SKILL.md`](../../../../../../.cursor/skills/conductor/SKILL.md) (or **`conductor`**) on **work-dev** **objects** (harness, export, `workspace` wedge, derived regen), **land** a **durable** pass in this folder:

- Add **`### Conductor close`** to the **day file** you are closing (`YYYY-MM-DD-day-NN.md`) using the same bullet **shape** as [CONDUCTOR-CLOSE-TEMPLATE.md](../../../../work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) (**Stance / conductor**, **Object**, **What moved / seam**, **Falsify / next test**, **Escalation**). Strategy **chapters/…/days.md** is **not** the home for this lane — **this** **journal** (or a **spec** under [dev-notebook/work-dev/](../)) is.
- **Optional** cadence only: `coffee_conductor_outcome` with `notebook_ref=` → path to this file — [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../../work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) § 3.

**Kleiber** **action** **MCQ** options may **point** at [workspace.md](../../../workspace.md) and concrete paths under `dev-notebook/work-dev/`.

### Optional habit telemetry

Light **follow-through** discipline (tomorrow line, blocker carryover, friction resolution) without turning this into a dashboard: [journal-metrics-habit.md](../../../../journal-metrics-habit.md). **Phase 0** = weekly 5‑minute check; **Phase 1** = optional YAML frontmatter. Rhythm snapshot (filename dates): `python3 scripts/journal_habit_snapshot.py`.
