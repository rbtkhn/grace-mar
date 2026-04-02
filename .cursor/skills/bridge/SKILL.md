---
name: bridge
preferred_activation: bridge
description: "Session-scale handoff ritual. Primary trigger: bridge. Commits and pushes both repos, then synthesizes current state into a structured transfer prompt for pasting into a fresh Cursor session. Run once when closing a session and carrying context forward."
---

# Bridge

**Preferred activation:** say **`bridge`**. Also responds to **`session handoff`**, **`close session`**, or **`transfer`**.

`bridge` is the session-scale handoff. It seals the current session — committing and pushing all work — then synthesizes the state into a single structured markdown block that the operator pastes into the next fresh Cursor session as the opening message.

Its purpose is **high-fidelity context transfer** across the session boundary where agent memory goes to zero. A good bridge means the next session starts with full orientation instead of spending turns reconstructing what happened.

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals repos and generates the transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same Cursor thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repos, carry context forward; no maintenance needed |
| **Quick check before stepping away** | **`coffee`** + signing-off intent (`--mode closeout` / handoff Step 1) | Lightweight status; no commit/push, no transfer prompt; same **A–I** menu as work-start |

**Default:** If in doubt, `bridge`. It commits, pushes, and produces a transfer prompt. If it's also end of day, run `dream` first.

**Bridge vs signing-off `coffee`:** Signing-off **`coffee`** is lightweight — handoff-weighted Step 1, no required git operations from the ritual. Bridge is structural — seals the session with commits and produces the carry-forward block. Bridge is the default for any session close.

This is event-driven: the operator says `bridge` when they're ready. There is no scheduled cadence.

---

## Step 1 — Read on-disk state

When the operator says `bridge`, read the following files (do not ask — just read them):

1. **`users/grace-mar/self-memory.md`** — long-horizon pointers, open loops, calibrations
2. **`users/grace-mar/recursion-gate.md`** — pending candidates (ids, summaries, status)
3. **`users/grace-mar/last-dream.json`** — last dream summary (integrity, governance, contradictions, followups)
4. **`docs/skill-work/work-coffee/work-coffee-history.md`** — recent coffee lane activity
5. **`docs/skill-work/work-dream/work-dream-history.md`** — recent dream lane activity
6. **`docs/skill-work/work-politics/work-politics-history.md`** — if exists, recent politics activity
7. **`docs/skill-work/work-dev/work-dev-history.md`** — if exists, recent dev activity

Also run:

8. **`git status -sb`** — uncommitted work (in both grace-mar and companion-self)
9. **`git log --oneline -10`** — recent commits (what moved)

---

## Step 2 — Commit and push both repositories

Seal the session by committing and pushing. Use a **two-bucket** approach per repo:

### Bucket 1: Runtime residue (auto-commit, no confirmation needed)

Files that are always safe to commit without review:

**grace-mar:**
- `users/grace-mar/compute-ledger.jsonl`
- `users/grace-mar/runtime-bundle/audit/compute-ledger.jsonl`
- `users/grace-mar/session-transcript.md`
- `users/grace-mar/self-memory.md`
- `users/grace-mar/last-dream.json`
- `users/grace-mar/harness-events.jsonl`
- `users/grace-mar/pipeline-events.jsonl`

Commit message: `chore: bridge session residue [YYYY-MM-DD]`

**companion-self:** Check `git status` — if dirty, same pattern (runtime/generated files get a residue commit).

### Bucket 2: Substantive work (commit with summary)

Any remaining dirty files (docs, scripts, skills, territory edits, config changes) are real work. For these:

1. Run `git diff --stat` to see what changed
2. Draft a concise commit message that summarizes the substantive changes
3. Commit and report what was included

Commit message: a real summary of the work, not a generic label.

### Push

After both buckets are committed (or if the worktree was already clean), push both repos:

```bash
cd /path/to/grace-mar && git push
cd /path/to/companion-self && git push
```

If push fails (e.g. remote has new commits), pull-rebase first, then push. If there are conflicts, stop and report — do not force-push.

**After push, run `git status -sb` in both repos to confirm clean state.**

### Cadence audit

After confirming clean state, log the bridge event:

```bash
python3 scripts/log_cadence_event.py --kind bridge -u grace-mar --ok --kv refs=<grace-mar-SHA>,<companion-self-SHA>
```

Replace `<grace-mar-SHA>` and `<companion-self-SHA>` with the HEAD commits just pushed (from `git rev-parse --short HEAD` in each repo). If only one repo had changes, include only that SHA.

---

## Step 3 — Generate the transfer prompt

Now that both repos are sealed and pushed, synthesize the readings from Step 1 into a single markdown block following this exact format. The canonical section contract lives in companion-self at `docs/skill-work/work-cadence/bridge-packet-contract.md`.

**Coffee tail (required):** The copyable transfer prompt must end with a **final line that is exactly `coffee`** (lowercase, alone on its line, not inside a code fence). That way the operator’s **first message** in the new session is both the bridge packet **and** the `coffee` skill trigger — work-start Step 1 runs immediately on top of this context. Do not tell the operator to send a second message just for `coffee`.

```markdown
# Session Bridge — [YYYY-MM-DD]

## Arc
[2-4 sentences: what the session accomplished, what shifted, current posture.
This is narrative, not a list. Write it from what you observed in the readings.]

## Carry-forward from last dream
[Condensed from last-dream.json: integrity/governance status, contradiction count,
followup items. If no dream ran or file is missing, say so.]

## RECURSION-GATE snapshot
[Pending count. Top 1-3 candidate ids with one-line summaries from the gate file.
If none pending, say "Gate clear."]

## Active territories
[Which work lanes had recent motion based on history files. One line each.
Skip lanes with no recent activity.]

## Priority lanes for next session
1. [Top priority — derived from gate state, territory momentum, and arc]
2. [Second priority]
3. [Third if warranted]

## Watch this
[One sentence: the single most important thing the next session should be alert to.
Synthesize from arc + gate + territories — what could go wrong or slip if unattended.]

## Commits sealed in this bridge
[List the commit(s) made in Step 2, or "Worktree was already clean."]

## Recent commits
[Last 5-10 commits from git log, verbatim — includes the bridge commits]

## Instructions for next session
**Operator:** Send everything from `# Session Bridge` through the line below as the **only** first message in a new Cursor session (one paste). **Assistant:** Context is above; run work-start **coffee** Step 1 now (see `.cursor/skills/coffee/SKILL.md`). The next line is the skill trigger.

coffee
```

Output the entire block so the operator can copy it.

---

## Step 4 — Done

Bridge is complete. Both repos are pushed, the transfer prompt is generated. The operator copies the prompt and closes the session.

## Guardrails

- **Commits only to the current branch.** Never switch branches, force-push, or commit to a branch the operator didn't intend.
- **No gate action.** Report gate state; do not process, approve, or defer candidates.
- **No merges into Record.** Committing files to git is not the same as merging into SELF/EVIDENCE. The gated pipeline is untouched.
- **Signal over volume.** The transfer prompt should be concise. Aim for one screen of text, not a wall. Omit sections that have nothing to report.
- **Narrative arc matters.** The "Arc" section is the most valuable part — it's the thing no script can produce. Synthesize, don't just list.
- **Stop on conflict.** If push fails after pull-rebase due to conflicts, stop and report. Do not force-push or resolve conflicts silently.
- **Ephemeral output.** The transfer prompt exists only in the chat. It persists only if the operator chooses to save it.

## Relation to coffee and dream

`bridge` sits alongside coffee and dream but at a different timescale:

- **`coffee`** — many per day (orientation sips)
- **`dream`** — once per day (nightly consolidation)
- **`bridge`** — once per session (seal, push, carry forward)

**Typical close sequence:** `dream` first (if end of day), then `bridge` (seals and generates the handoff). Or just `bridge` alone if mid-day and you simply want a fresh thread.

**Next session:** Paste the bridge prompt as the first message; it **ends with `coffee`** so one paste runs the grounding stack on top of the carried context.

## Related files

- `.cursor/skills/coffee/SKILL.md` — morning cadence (run after pasting bridge)
- `.cursor/skills/dream/SKILL.md` — nightly cadence (run before bridge if end of day)
- `.cursor/skills/repo-hygiene-pass/SKILL.md` — deeper commit-grouping when needed
- `users/grace-mar/self-memory.md` — continuity context
- `users/grace-mar/recursion-gate.md` — gated pipeline queue
- `users/grace-mar/last-dream.json` — dream handoff artifact
