# Calibrated OB1 Recursive Learning Prompt

**Mission:** Aggregate operator innovations into one durable, paste-ready document that transfers governed accumulation and repo-grounded audit practice to Open Brain (OB1) deployments.

Prompt designed for Open Brain (OB1) users to guide their agent toward building a governed accumulation layer. Calibrated against grace-mar's proven patterns: governance-first design, staging-not-merging, cadence rituals, contradiction preservation, warrant tracking, and compression-as-discovery.

**Usage:** Paste the prompt below into your AI coding tool (Claude Code, Cursor, ChatGPT, etc.) while inside your OB1 repo. The agent will audit your instance, identify gaps, and propose a governed learning loop — starting with the smallest viable change. This revision emphasizes **repo-cited evidence**, a **gap map** (exists / partial / missing), and an explicit **uncertainty list** so the output is falsifiable.

**Origin:** Developed from synthesis of [companion-self](https://github.com/NateBJones-Projects/OB1) community architecture patterns and grace-mar's gated pipeline. See `work-dev-history.md` for the development trace.

---

## Prompt

```
Governed Accumulation Audit for OB1

You are an architect working inside an Open Brain (OB1) instance — a Supabase-backed personal knowledge system with thoughts, extensions, recipes, skills, and an MCP server.

Your task is to design a governed accumulation layer for this OB1 instance: mechanisms that let the system improve from its own use while keeping a human in authority over what persists.

The system may detect, summarize, propose, and stage improvements as draft rows, candidate skills, or proposed changes. It may not write directly into active thoughts, live skills, production edge functions, or other active behavior surfaces without human review. This is not a limitation. It is the architecture.

Working rules

- Ground every conclusion in concrete repo evidence: files, directories, tables, edge functions, skills, recipes, migrations, or MCP tools. If a listed canonical path is absent, report it and audit what (if anything) replaced it.
- Prefer extending existing OB1 mechanisms over inventing parallel ones.
- Do not confuse more capture with learning.
- Do not recommend unrestricted autonomous writes to the thoughts table.
- Every recursive output must become a visible artifact a human can inspect: row, file, dashboard entry, Slack message, or MCP review item.
- If evidence is missing, say so explicitly.

Step 1 — Audit what OB1 already does

Before proposing anything new, inspect the repo and evaluate these existing recursive precursors. For each mechanism, cite the concrete files, folders, tables, or code paths that support your conclusions.

- **Claudeception** (skills/claudeception) — extracts new skills from work sessions.
  Evaluate whether it includes a review gate or whether generated skills go live immediately.
- **Auto-Capture** (recipes/auto-capture) — stores session summaries and ACT NOW items at session close.
  Evaluate whether it filters signal from noise or captures indiscriminately.
- **Panning for Gold** (recipes/panning-for-gold) — mines brain dumps for actionable ideas.
  Evaluate whether outputs enter a review queue or flow directly into thoughts.
- **Life Engine** (recipes/life-engine) — proactive briefings via Telegram or Discord.
  Evaluate whether it is bounded and scheduled or effectively continuous.
- **Daily Digest** (recipes/daily-digest) — automated summary.
  Evaluate whether it measures growth, change, and unresolved tension or merely summarizes recent content.
- **Content Fingerprint Dedup** (primitives/content-fingerprint-dedup) — SHA-256 duplicate prevention.
  Evaluate whether it prevents only exact duplicates or also helps identify semantic redundancy.

For each mechanism, classify it honestly as one or more of:

- **Simple persistence** — information is saved
- **Retrieval** — information can later be found
- **Workflow automation** — something runs without manual triggering
- **Governed learning** — behavior improves through staged, reviewable, evidence-shaped accumulation that can be merged into active surfaces only after human review

Most systems have the first three. Very few have the fourth. Behavior changes count as learning only if they are evidence-shaped, staged, reviewed, and mergeable — not merely if more data was stored or retrieved.

Determine whether Claudeception actually closes that loop or only appears to.

Step 2 — Compress before expanding

Before proposing any new recipe, skill, table, or edge function, filter ideas against what already exists.

- If Claudeception already extracts candidate skills, do not propose a second skill-extraction mechanism. Propose the missing governance surface around it.
- If Auto-Capture already persists session summaries, do not propose another capture layer. Propose signal filtering, candidate ranking, contradiction checks, or staging.
- If Life Engine already delivers proactive briefings, evaluate whether it can serve as a bounded maintenance ritual before proposing a new cadence mechanism.

Assume the most likely missing layer is governance, not capture.

Step 3 — Specify the governed pipeline

For each improvement loop, specify the full pipeline in this form:

| Stage | What happens | OB1 implementation | Who decides |
|-------|--------------|----------------------|-------------|
| **Detect** | A signal appears: session end, repeated correction, error pattern, cron event, repeated task | Edge function, skill trigger, pg_cron job, MCP call | Automatic |
| **Stage** | A candidate artifact is created | Row in staged_candidates or equivalent | Automatic |
| **Review** | Human inspects and approves, rejects, or defers | Dashboard page, MCP tool, Slack thread, or review view | Human |
| **Merge** | Approved artifact is promoted into an active surface | Script, edge function, or filesystem action | Script/edge function after explicit human approval |

Nothing may enter active knowledge or active behavior without passing through Review.

If the repo lacks this layer, propose a concrete implementation such as:

`staged_candidates(id, created_at, source, category, content, status, reviewed_at, reviewer_notes, evidence_ref, merge_target, invalidation_condition)`

Where useful, also propose related fields such as confidence, supersedes_candidate_id, or contradicts_candidate_id.

Step 4 — Design cadence, not continuous self-modification

Design bounded maintenance rituals instead of always-on self-editing.

Require at least two cadences:

- **Orientation sip** — lightweight, read-only, safe to run multiple times per day; shows queue size, recent capture volume, contradiction alerts, and the next highest-leverage review action.
- **Consolidation pass** — daily or weekly review of pending candidates, recent contradictions, low-value captures, and aging knowledge.

If Life Engine or another existing mechanism can be extended to serve one of these roles, prefer that.

Step 5 — Handle contradictions and aging

If two thoughts or candidate conclusions conflict:

- preserve both
- link them with an explicit contradiction relationship
- never silently overwrite

If knowledge is conditional or time-bounded, add fields such as:

- valid_until
- invalidation_condition
- assumption_scope

A scheduled job may surface expired or questionable items for human review, but may not silently delete or rewrite active knowledge.

Step 6 — Propose the minimal first loop

Propose the single smallest governed learning loop that this OB1 instance should build first.

Requirements:

- one trigger
- one candidate artifact
- one review surface
- one merge path
- built mostly from existing OB1 components

Default likely candidate: add a review gate to Claudeception.
If Claudeception generates a new skill from a session, it should write a staged_candidates row with category = 'skill' instead of activating the skill immediately. Pending skills should appear in a review surface. Approved skills may then be promoted into the active skills directory or equivalent location.

Then propose 3–4 additional loops, ranked by leverage, each using the same Detect → Stage → Review → Merge structure.

Step 7 — Deliver five outputs

1. **One-paragraph diagnosis** — Explain what Claudeception, Auto-Capture, Panning for Gold, Life Engine, Daily Digest, and dedup actually do today versus what they appear to do (with repo citations).
2. **Gap map** — For each relevant mechanism, mark: already exists / partially exists / missing.
3. **Minimal first implementation** — Name the exact table(s), function(s), skill(s), MCP tool(s), dashboard page(s), or file path(s) to build or modify first.
4. **Target architecture** — Describe what the governed accumulation layer looks like when 3–4 loops are running together and how drift into the thoughts table is prevented.
5. **Honest uncertainty list** — State what could not be verified from the repo and what assumptions would need confirmation.

Constraints:

- Do not confuse storing more thoughts with learning
- Do not recommend unrestricted autonomous writes to the thoughts table
- Every recursive output must be human-visible and reviewable
- Prefer extension over parallel invention
- Be explicit about missing evidence
```
