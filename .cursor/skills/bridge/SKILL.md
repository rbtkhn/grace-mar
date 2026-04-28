---
name: bridge
preferred_activation: bridge
requires: [handoff-check]
description: "Session-scale handoff ritual. Primary trigger: bridge. Before Step 1, synthesizes the previous four events from work-cadence-events.md into **Recent rhythm** prose (no internal ops jargon or timestamps in chat). Assesses grace-mar + companion-self (and asks about other repos if relevant), recommends whether each needs commit/push, then seals and generates a structured transfer prompt for pasting into a fresh Cursor session. Run once when closing a session and carrying context forward."
---

# Bridge

**Preferred activation:** say **`bridge`**. Also responds to **`session handoff`**, **`close session`**, or **`transfer`**.

`bridge` is the session-scale handoff. It **assesses** whether **grace-mar** and **companion-self** (and optionally other repos) need commit/push, **recommends** actions, **asks** when ambiguous, then seals what the operator agrees to and synthesizes state into a single structured markdown block for the next fresh Cursor session.

Its purpose is **high-fidelity context transfer** across the session boundary where agent memory goes to zero. A good bridge means the next session starts with full orientation instead of spending turns reconstructing what happened.

## When to use

| Scenario | Path | Why |
|----------|------|-----|
| **End of day + closing session** | `dream` then `bridge` | Dream settles continuity; bridge seals repos and generates the transfer prompt |
| **End of day, keeping session** | `dream` alone | Maintenance pass; same Cursor thread continues tomorrow |
| **Mid-day, closing session** | `bridge` alone | Seal repos, carry context forward; no maintenance needed |
| **Quick check before stepping away** | **`coffee`** + signing-off intent (`--mode closeout` / handoff Step 1) | Lightweight status; no commit/push, no transfer prompt; same fixed **A–E** hub as work-start (**A** Steward · **B** Engineer · **C** Historian · **D** Capitalist · **E** Conductor) |

**Default:** If in doubt, `bridge`. It surfaces push/sync recommendations, then commits and pushes per scope, and produces a transfer prompt. If it's also end of day, run `dream` first.

**Bridge vs signing-off `coffee`:** Signing-off **`coffee`** is lightweight — handoff-weighted Step 1, no required git operations from the ritual. Bridge is structural — assesses repos, seals agreed scope, and produces the carry-forward block. Bridge is the default for any session close.

This is event-driven: the operator says `bridge` when they're ready. There is no scheduled cadence.

---

## Step 0 — Recent rhythm (before Step 1 and before bridge log)

**Read first** — a successful bridge appends a **`bridge`** line **after** push (see **Cadence audit** under Step 3). Read the log **before** that happens so this session’s bridge is not included in the rhythm window.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 4** such lines already in the file. If fewer than four exist, use what exists; if none, **Recent rhythm:** _(no prior events)_.
3. **Synthesize** using the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)): briefly acknowledge the recent past in *felt* terms (what was settled, what was decided), then project the **optimal next direction**. Use **"we"** framing — warm, direct, future-facing. No dates, clock times, commit hashes, or process names in the prose. Lead with acknowledgment, end with direction. Anchored in the actual log lines, but felt and projected forward, not listed.
4. Place **Recent rhythm:** at the **top** of the **first** bridge reply (before push/sync assessment and before Step 1 file reads are summarized). Same **4** as **coffee** so seal → **`coffee`** on the transfer packet stays rhythm-symmetric.

If the file is missing or empty below the anchor, note that and continue.

---

## Step 1 — Read on-disk state

When the operator says `bridge`, read the following files (do not ask — just read them):

1. **`users/grace-mar/self-memory.md`** — long-horizon pointers, open loops, calibrations
2. **`users/grace-mar/recursion-gate.md`** — pending candidates (ids, summaries, status)
3. **`users/grace-mar/last-dream.json`** — last dream summary (integrity, governance, digest counts, `tomorrow_inherits`, optional rollup / paths / civ-mem — hints only, not policy)
4. **`docs/skill-work/work-coffee/work-coffee-history.md`** — recent coffee lane activity
5. **`docs/skill-work/work-dream/work-dream-history.md`** — recent dream lane activity
6. **`docs/skill-work/work-politics/work-politics-history.md`** — if exists, recent politics activity
7. **`docs/skill-work/work-dev/work-dev-history.md`** — if exists, recent dev activity

Also run:

8. **`git status -sb`** — uncommitted work (in both grace-mar and companion-self)
9. **`git log --oneline -10`** — recent commits (what moved)
10. **`users/grace-mar/daily-handoff/last-bridge-state.json`** (if present) — prior bridge snapshot for **Since last bridge** deltas in Step 4. If missing, the packet says there is no prior delta.

---

## Step 2 — Push/sync assessment (required before git writes)

When the operator says **`bridge`**, do **not** assume both repositories need the same treatment. After Step 1 reads, for **each** of the default pair:

- **grace-mar** (this workspace)
- **companion-self** (sibling clone or `GRACE_MAR_COMPANION_SELF` / `./companion-self` per repo layout)

gather:

- `git status -sb` (dirty? branch?)
- whether **`origin`** is configured and whether **`HEAD` is ahead of `@{u}`** (unpushed commits) — e.g. `git rev-list --left-right --count @{u}...HEAD` when upstream exists

### Worktree risk preflight (read-only; before recommendations)

From the same `git status -sb` and `git diff --stat` output, classify each repo in scope:

| Class | Meaning |
|-------|---------|
| **safe** | Clean worktree (no meaningful unstaged/untracked body lines). |
| **inspect** | Light residue — some changed files; moderate diff. |
| **conflict-prone** | Unmerged paths, conflict markers, or very large/wide change set. |

Emit one line per repo, e.g. `Worktree risk (grace-mar): inspect — review diff before sealing.`

**Pause and ask** the operator before Step 3 if any in-scope repo is **conflict-prone** — confirm proceed after manual inspect/reconcile, or stop. Bridge still does not resolve conflicts silently.

**Multi-repo map (instance extension):** If the session spans more than the default pair, have the operator list **path + role** in one bullet list (e.g. companion-xavier — pedagogy drafts). No extra automation in the template; status only unless Step 2 includes that repo.

Then output a short **Push/sync recommendation** block:

| Repo | Dirty? | Unpushed commits? | Recommendation |
|------|--------|-------------------|----------------|
| grace-mar | … | … | push after seal / already clean — nothing to push / pull first |
| companion-self | … | … | same |

**Default recommendation:** Seal **grace-mar** if dirty or ahead; touch **companion-self** only if it is dirty or ahead, or if the session clearly edited it (otherwise recommend *skip* with reason — e.g. clean and untouched).

**Ask the operator** when:

- Only one repo needs action but the ritual might expect both (confirm *grace-mar only* or *both*).
- A **third** repo may matter for handoff (e.g. **companion-xavier**, other worktrees) — one line: *“This session may also need push/sync for &lt;repo&gt; — include?”*
- Either repo is **behind** origin, has **conflicts**, or **no upstream** — stop and ask how to proceed.

**Operator override:** If the same message says **`bridge grace-mar only`** (or equivalent), limit commit/push to grace-mar and still state companion-self status in the recommendation block.

**Done when:** Recommendation table is shown and the operator has confirmed scope (or no ambiguity exists).

---

## Step 3 — Commit and push (per recommendation)

Seal the session by committing and pushing **according to Step 2**. Use a **two-bucket** approach per repo that Step 2 said to touch:

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

After buckets are committed for each repo in scope (or if that worktree was already clean and only `git push` is needed), **`git push` only the repos Step 2 included** — for example:

```bash
cd /path/to/grace-mar && git push
# Only if Step 2 recommended companion-self:
cd /path/to/companion-self && git push
```

If push fails (e.g. remote has new commits), pull-rebase first, then push. If there are conflicts, stop and report — do not force-push.

**After push, run `git status -sb` in each repo that was pushed to confirm clean state.**

### Cadence audit

After confirming clean state (for repos that were part of this bridge), log the bridge event:

```bash
python3 scripts/log_cadence_event.py --kind bridge -u grace-mar --ok --kv refs=<grace-mar-SHA>,<companion-self-SHA> --cursor-model "<same as ## Agent surface>"
```

Replace `<grace-mar-SHA>` and `<companion-self-SHA>` with the HEAD commits just pushed (from `git rev-parse --short HEAD` in each repo). If only one repo was in scope, include only that SHA (and note which repos were skipped).

### Bridge state snapshot (operational)

After a successful bridge (clean `git status -sb` in every repo that was pushed), update the session-to-session delta file:

```bash
python3 scripts/bridge_last_state.py -u grace-mar --write
```

This writes `users/grace-mar/daily-handoff/last-bridge-state.json` (gitignored). For **Since last bridge** bullets in the packet, you may instead run `python3 scripts/bridge_last_state.py -u grace-mar --print-delta` before composing Step 4.

**Done when:** All in-scope repos show clean `git status -sb` after push, cadence line is logged, and bridge state snapshot is written.

---

## Step 4 — Generate the transfer prompt

Now that the recommended repos are sealed and pushed (or explicitly skipped with operator consent), synthesize the readings from Step 1 into a single markdown block following this exact format. The canonical section contract lives in companion-self at `docs/skill-work/work-cadence/bridge-packet-contract.md`. Include **`## Agent surface`** with **Cursor model:** copied from the **Cursor UI** (model picker for this composer); in Cursor that label is usually visible — use `unknown` only if it is not.

**Closing `coffee` line (required):** The copyable transfer prompt must end with a **final line that is exactly `coffee`** (lowercase, alone on its line, not inside a code fence). That way the operator’s **first message** in the new session is both the bridge packet **and** the `coffee` skill trigger — work-start Step 1 runs immediately on top of this context. Do not tell the operator to send a second message just for `coffee`. (This is **not** the same as Step 0 **Recent rhythm** — it is the packet’s required last line.)

```markdown
# Session Bridge — [YYYY-MM-DD]

## Session Arc
[Episodic — what happened, in what order:
- Started: initial intent or task
- Pivots: where direction changed and why
- Ended: current state, what's unfinished
2-4 sentences. This is narrative, not a list. Write from what you observed.]

## Session Output
[Semantic — what was figured out or produced:
- Decisions made (with warrant if available — the assumption that would invalidate them)
- Patterns identified
- Artifacts created or modified
- Open questions surfaced
Bullet list, 2-5 items. Facts and deliverables, not narrative.]

## Carry-forward from last dream
[Condensed from last-dream.json: integrity/governance status, contradiction / reviewable counts,
`tomorrow_inherits` (if present), optional note on coffee rollup / menu picks. If strict dream halted
without rewriting the file, say the handoff may be stale. If no file, say so.]

## RECURSION-GATE snapshot
[Pending count. Top 1-3 candidate ids with one-line summaries from the gate file.
If none pending, say "Gate clear."]

## Active territories
[Which work lanes had recent motion based on history files. One line each.
Skip lanes with no recent activity.]

## Priority lanes for next session
1. [Lane or theme — one short reason why this rank]
2. [Lane or theme — one short reason]
3. [Third only if warranted — lane or theme — reason]

## Watch this
**Risk kind:** continuity | git | governance | focus | context — [one sentence: the single most important alert; synthesize from arc + gate + territories + worktree risk.]

## Since last bridge
[Max 3-4 bullets: delta vs `last-bridge-state.json` or output of `bridge_last_state.py --print-delta`. If no prior file, say first bridge / no prior delta.]

## Bridge transfer quality
- **Confidence:** high | medium | low
- **Signals:** [2-4 short phrases: e.g. clean push, dream handoff present, gate readable, territories detected]
- **Gaps:** [one line — what is missing or weak in this packet]
- **Seal:** [post-push `git status -sb` per repo in scope + `git rev-parse --short HEAD` per repo — note clean / ahead / diverged]

## Next session posture
**Posture:** reorient | execute | inspect | resolve | write — [three to six words tied to arc + gate + worktree risk]

## Not transferred on purpose
[Optional; max 2 bullets, or omit section. What the packet deliberately left out — e.g. noisy branches, speculative threads.]

## Commits sealed in this bridge
[Per repo: list commit(s) made in Step 3. One composite line: `Residue commit: <msg or none> / Substantive commit: <msg or none>`. Which repos were pushed, or "Worktree was already clean" / "Skipped per operator".]

## Recent commits
[Last 5-10 commits from git log, verbatim — includes the bridge commits]

## Agent surface
- **Cursor model:** [Copy the model name from the Cursor chat UI / model picker for this composer. Use `unknown` only if it is not visible.]

## Instructions for next session
**Operator:** Send everything from `# Session Bridge` through the line below as the **only** first message in a new Cursor session (one paste). **Assistant:** Context is above; run work-start **coffee** Step 1 now (see `.cursor/skills/coffee/SKILL.md`). The next line is the skill trigger.

**Parallel import:** If you also need a dense packet for an **already-running** session, run **harvest** separately after this paste — do not append a second packet here (keeps the closing **`coffee`** line unambiguous).

coffee
```

Output the entire block so the operator can copy it.

---

## Step 5 — Done

Bridge is complete. Pushed repos match Step 2 recommendation (or operator override); the transfer prompt is generated; `bridge_last_state.py --write` was run after a successful seal. The operator copies the prompt and closes the session.

**Optional receipt:** To keep a durable copy, save the transfer block under `docs/skill-work/work-cadence/bridge-packets/YYYY-MM-DD-session.md` (or another path the operator prefers). Default remains chat-only.

---

## After the new session opens — doc-only loop

**Optional operator habit** (no scripts): once the paste is the **first message** in the fresh thread, note:

1. **Coffee** — Did work-start **coffee** Step 1 run on top of the block (not a generic reply that skipped scripts)?
2. **Tail** — Is the final line still exactly **`coffee`** alone (not dropped, not inside a fence)?
3. **Load** — Was the packet ~one screen, or did the receiver choke on length?

**Recursive tightening:** If the **same failure** happens **twice** (e.g. lost `coffee` line, wrong heading levels, missing dual-repo status), patch **this skill** or [companion-self `bridge-packet-contract.md`](companion-self/docs/skill-work/work-cadence/bridge-packet-contract.md). Optional: save a **gold** bridge packet under `bridge-packets/` as a shape reference.

---

## Guardrails

- **Commits only to the current branch.** Never switch branches, force-push, or commit to a branch the operator didn't intend.
- **No gate action.** Report gate state; do not process, approve, or defer candidates.
- **No merges into Record.** Committing files to git is not the same as merging into SELF/EVIDENCE. The gated pipeline is untouched.
- **Signal over volume.** The transfer prompt should be concise. Aim for one screen of text, not a wall. Omit sections that have nothing to report.
- **Narrative arc matters.** The "Session Arc" section is the most valuable part — it's the thing no script can produce. Synthesize, don't just list. "Session Output" is the semantic complement — facts and deliverables.
- **Stop on conflict.** If push fails after pull-rebase due to conflicts, stop and report. Do not force-push or resolve conflicts silently.
- **Push/sync clarity.** Always give the Step 2 recommendation (and ask when ambiguous) before writing commits; do not treat “both repos” as mandatory if companion-self is clean and untouched unless the operator confirms.
- **Ephemeral output.** The transfer prompt exists only in the chat unless the operator saves it (optional `bridge-packets/` path in Step 5).

## Relation to coffee and dream

`bridge` sits alongside coffee and dream but at a different timescale:

- **`coffee`** — many per day (orientation sips)
- **`dream`** — once per day (nightly consolidation)
- **`bridge`** — once per session (seal, push, carry forward)

**Typical close sequence:** `dream` first (if end of day), then `bridge` (seals and generates the handoff). Or just `bridge` alone if mid-day and you simply want a fresh thread.

**Next session:** Paste the bridge prompt as the first message; it **ends with `coffee`** so one paste runs the grounding stack on top of the carried context.

## Related files

- `docs/skill-work/work-cadence/README.md` — **Cadence choreography** (recent rhythm window depths: bridge ×4, harvest ×0)
- `.cursor/skills/coffee/SKILL.md` — morning cadence (run after pasting bridge)
- `.cursor/skills/dream/SKILL.md` — nightly cadence (run before bridge if end of day)
- `.cursor/skills/harvest/SKILL.md` — parallel-session import (separate from bridge paste)
- `.cursor/skills/repo-hygiene-pass/SKILL.md` — deeper commit-grouping when needed
- `scripts/bridge_last_state.py` — operational `last-bridge-state.json` + `--print-delta`
- `companion-self/docs/skill-work/work-cadence/bridge-packet-contract.md` — canonical section contract
- `users/grace-mar/self-memory.md` — continuity context
- `users/grace-mar/recursion-gate.md` — gated pipeline queue
- `users/grace-mar/last-dream.json` — dream handoff artifact

## Revision log

| Date | Change |
|------|--------|
| 2026-04-06 | Doc-only cold-thread loop § *After the new session opens*. |
| 2026-04-06 | Split Arc into Session Arc (episodic) + Session Output (semantic) — LoreSpec-derived. |
