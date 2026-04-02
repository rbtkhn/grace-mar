# COFFEE (daily rhythm) — Xavier instance (`fork_id`: xavier, **her repo**)

*Filename `GOOD-MORNING.md` is legacy; grace-mar operator activation is **coffee** (work-start vs **signing-off** intent — same **A–I** menu; **I** = work-strategy-rome), with legacy **hey** still accepted — mirror the current vocabulary in chat.*

**Where Record paths live:** [INSTANCE-PATHS.md](INSTANCE-PATHS.md). Run harness / integrity / gate steps **in Xavier’s `companion-xavier` repository**, not in grace-mar.

**First-ever session?** Start with [DAY-1-NO-TERMINAL.md](DAY-1-NO-TERMINAL.md), then [first-good-morning-runbook.md](first-good-morning-runbook.md), then return here for normal rhythm.

**Prerequisite:** **Session 0** complete — seed survey MCQ in **her repo** (all MCQs answered and saved). **Do not** start the ten beginner tasks until Session 0 is done.

## Daily rhythm (shape)

Mirror grace-mar **coffee** cadence in *shape* — edit for Xavier’s lanes (companion-self build + EA/SMM client work when applicable):

1. Optional: `python3 scripts/operator_daily_warmup.py -u xavier` (if bundled in template).
2. `python3 scripts/harness_warmup.py -u xavier` — gate / session tail snapshot.
3. `python3 scripts/validate-integrity.py --user xavier --json` — review issues.
4. Skim **work-politics** content queue / client block if active — [work-politics README](../work-politics/README.md).
5. Run daily `work-dev` mirror sync check — [work-dev-mirror/SYNC-CONTRACT.md](work-dev-mirror/SYNC-CONTRACT.md).
6. Run daily `work-politics` mirror sync check — [work-politics-mirror/SYNC-CONTRACT.md](work-politics-mirror/SYNC-CONTRACT.md).
7. Update unified sync snapshot — [SYNC-DAILY.md](SYNC-DAILY.md).
8. Run template-alignment sync check against [self-work/sync-pack](../self-work/sync-pack/README.md).
9. Publish final daily run plan in [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md).

**Distinguish:** “Coffee” here = **her** Record + **her** work stack. Massie/client material is **WORK**, not SELF.

## Required daily output: work-dev sync check

Each `coffee` should include:

- `work-dev sync status:` no relevant updates / relevant updates found / blocked
- if relevant updates found: up to 5 proposed `work-dev-mirror` file updates with one-line reason each
- score per proposed update: `impact/urgency/xavier-readiness` and total out of 9
- one log row appended in [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md)

### No-terminal scan prompt (copy/paste)

```text
Run my daily work-dev mirror sync check.

Use:
- docs/skill-work/work-dev/
- docs/skill-work/work-xavier/work-dev-mirror/SYNC-CONTRACT.md
- docs/skill-work/work-xavier/work-dev-mirror/SYNC-LOG.md

Output:
1) work-dev sync status
2) relevant files (max 5) with one-line reasons
3) score each file (impact/urgency/xavier-readiness + total)
4) recommended mirror edits (paths only)
5) one SYNC-LOG row draft
6) SYNC-DAILY update block draft
```

## Required daily output: work-politics sync check

Each `coffee` should include:

- `work-politics sync status:` no relevant updates / relevant updates found / blocked
- if relevant updates found: up to 5 proposed `work-politics-mirror` file updates with one-line reason each
- score per proposed update: `impact/urgency/xavier-readiness` and total out of 9
- one log row appended in [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md)

### No-terminal scan prompt (copy/paste)

```text
Run my daily work-politics mirror sync check.

Use:
- docs/skill-work/work-politics/
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-CONTRACT.md
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-LOG.md

Output:
1) work-politics sync status
2) relevant files (max 5) with one-line reasons
3) score each file (impact/urgency/xavier-readiness + total)
4) recommended mirror edits (paths only)
5) one SYNC-LOG row draft
6) SYNC-DAILY update block draft
```

## Required daily output: unified sync snapshot

Each `coffee` should update [SYNC-DAILY.md](SYNC-DAILY.md) with:

- both mirror statuses
- top scored candidate updates
- one combined next action

Staleness rule (Xavier-only):
- if either sync log is older than 3 days, mark `stale sync state: yes` in `SYNC-DAILY.md` and run forced scans first.

## Required daily output: template alignment sync check

Each `coffee` should include:

- `template upstream:` repo + ref used for this check
- `template sync alignment status:` aligned / minor drift / major drift
- any drift found between Xavier mirrors and template sync-pack expectations
- up to 3 proposed alignment edits (paths only) for same-day or weekly batch
- one template-alignment block updated in [SYNC-DAILY.md](SYNC-DAILY.md)

### No-terminal alignment prompt (copy/paste)

```text
Run my daily template-alignment sync check for Xavier.

Use template upstream:
- repo: https://github.com/rbtkhn/companion-self
- ref: main (or a pinned tag/commit if set in SYNC-DAILY)

Compare:
- companion-self/docs/skill-work/self-work/sync-pack/SYNC-CONTRACT.template.md
- companion-self/docs/skill-work/self-work/sync-pack/SYNC-LOG.template.md
- companion-self/docs/skill-work/self-work/sync-pack/SYNC-DAILY.template.md

Against:
- docs/skill-work/work-xavier/work-dev-mirror/SYNC-CONTRACT.md
- docs/skill-work/work-xavier/work-dev-mirror/SYNC-LOG.md
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-CONTRACT.md
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-LOG.md
- docs/skill-work/work-xavier/SYNC-DAILY.md

Output:
1) template upstream used (repo + ref)
2) template sync alignment status: aligned / minor drift / major drift
3) concrete drift list (max 5)
4) recommended edits (paths only)
5) SYNC-DAILY template-alignment block draft
```

## Required daily output: suggested development path

Every `coffee` should include one **suggested change/development path** for `work-xavier` that directs Xavier toward:

1. one **learning objective** from [LEARNING-OBJECTIVES-CONTROL-PLANE.md](LEARNING-OBJECTIVES-CONTROL-PLANE.md), and  
2. one **business skill outcome** (content execution, sourcing discipline, stress-test judgment, KPI/budget ops, or escalation quality).

### Daily suggestion format (use this block)

```md
### Suggested work-xavier development path (today)
- **Focus objective:** LO-0X (<objective name>)
- **Business skill focus:** <one concrete skill>
- **Proposed change:** <one scoped doc/process improvement in work-xavier>
- **Why now:** <1-2 lines tied to current friction or KPI trend>
- **Success check (today):**
  - [ ] <observable completion criterion #1>
  - [ ] <observable completion criterion #2>
```

Rules:
- Scope to one small, finishable change per day.
- Prefer improvements to runbooks, checklists, source discipline, and weekly execution quality.
- No changes to identity truth files unless through gated candidate flow.

## Required daily output: Daily Ops Card (final step)

After all sync/alignment checks, complete [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md).

The card must include:

- one top sync action
- one top execution action
- one top gate action
- explicit stop condition (to prevent maintenance overrun)
- timeboxed `0-30`, `30-60`, `60-90` plan
- risk + escalation trigger

### No-terminal card prompt (copy/paste)

```text
Build my Daily Ops Card for today using:
- SYNC-DAILY status
- work-dev and work-politics sync outputs
- template-alignment status
- today's suggested development path

Write/update:
- docs/skill-work/work-xavier/DAILY-OPS-CARD.md

Rules:
- pick exactly one top action in each category (sync, execution, gate)
- make each done condition objectively checkable
- include a stop condition to prevent over-maintenance
- keep plan runnable in 90 minutes total
```

## First coffee — ten beginner tasks

**Prerequisite:** Session 0 (MCQ) **complete.**

| # | Task |
|---|------|
| 1 | Open **Xavier’s `companion-xavier` repository** in Cursor (her instance repo, not grace-mar). |
| 2 | Open her repo `README.md` (instance root); read top to bottom. |
| 3 | Open `users/xavier/self.md`. Skim — **IX empty** until gate merges survey outputs. |
| 4 | Command palette → Terminal → `pwd` / `ls` (or `dir` on Windows). |
| 5 | `python3 --version` — if missing, note for companion before installing runtimes. |
| 6 | Quick open **her** `users/xavier/recursion-gate.md` — read **Candidates** header. |
| 7 | Open [LANES.md](LANES.md) — WORK vs Record once. |
| 8 | Ask the AI to summarize **her** repo’s `AGENTS.md` (or the companion-self template copy): what may the agent do without approval vs what requires approval? |
| 9 | Optional: run harness + warmup from **her** repo root; paste output to a scratch note. |
| 10 | Add one line to **her** `users/xavier/session-log.md`: date + “Session 0 complete; first coffee tasks 1–10 done.” |

**Operator:** Pair first run with a short screen share if steps 4–6 stall.
