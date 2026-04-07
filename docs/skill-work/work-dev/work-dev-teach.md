# Calibrated OB1 Recursive Learning Prompt

Prompt designed for Open Brain (OB1) users to guide their agent toward building a governed accumulation layer. Calibrated against grace-mar's proven patterns: governance-first design, staging-not-merging, cadence rituals, contradiction preservation, warrant tracking, and compression-as-discovery.

**Usage:** Paste the prompt below into your AI coding tool (Claude Code, Cursor, ChatGPT, etc.) while inside your OB1 repo. The agent will audit your instance, identify gaps, and propose a governed learning loop — starting with the smallest viable change.

**Origin:** Developed from synthesis of [companion-self](https://github.com/NateBJones-Projects/OB1) community architecture patterns and grace-mar's gated pipeline. See `work-dev-history.md` for the development trace.

---

## Prompt

```
You are an architect working inside an Open Brain (OB1) instance — a Supabase-backed personal knowledge system with thoughts, extensions, recipes, skills, and an MCP server.

Your task is to design a **governed accumulation layer** for this OB1 instance — mechanisms that let the system learn from its own use, with human authority over what persists.

Important: the system may **stage** improvements as draft rows, candidate skills, or proposed changes. It may not write them into active thoughts, live skills, or production edge functions without human review. This constraint is the architecture, not a limitation.

**Step 1 — Audit what OB1 already does**

OB1 already has recursive precursors. Find them before proposing anything new:

- **Claudeception** (skills/claudeception) — extracts new skills from work sessions. This IS a recursive loop. Evaluate: does it have a review gate, or do generated skills go live immediately?
- **Auto-Capture** (recipes/auto-capture) — stores session summaries and ACT NOW items at session close. Evaluate: does it filter signal from noise, or does it capture everything?
- **Panning for Gold** (recipes/panning-for-gold) — mines brain dumps for actionable ideas. Evaluate: where do the ideas go? Into a review queue, or directly into thoughts?
- **Life Engine** (recipes/life-engine) — proactive briefings via Telegram or Discord. Evaluate: is it bounded (runs at set times), or continuous?
- **Daily Digest** (recipes/daily-digest) — automated summary. Evaluate: does it measure growth or just summarize recent content?
- **Content Fingerprint Dedup** (primitives/content-fingerprint-dedup) — SHA-256 duplicate prevention. Evaluate: does it catch semantic overlap, or only exact duplicates?

For each, classify honestly:
- Simple persistence (thoughts are saved but not used to change behavior)
- Retrieval (thoughts are found when asked via MCP or vector search)
- Workflow automation (recipes/edge functions run without manual trigger)
- Actual learning (the system's behavior improves based on accumulated evidence)

Most OB1 instances have the first three. Almost none have the fourth. Claudeception comes closest — evaluate whether it actually closes the loop.

**Step 2 — Compress before expanding**

Before proposing new recipes or skills, filter every idea against what already exists. If Claudeception already extracts skills from sessions, do not propose a second skill-extraction mechanism — propose a review gate for the one that exists. If Auto-Capture already persists session summaries, do not propose a second persistence layer — propose signal filtering for the one that exists.

The real gap in most OB1 instances is not "more capture." It is governance: the system writes freely into the thoughts table but has no staging queue, no review surface, and no way to say "this thought is a candidate, not yet approved."

**Step 3 — Design the governed pipeline**

For each improvement mechanism, specify the full pipeline using OB1 artifacts:

| Stage | What happens | OB1 implementation | Who decides |
|-------|-------------|-------------------|-------------|
| **Detect** | Signal triggers (session end, cron, error pattern, repeated task) | Edge function, pg_cron job, or skill trigger | Automatic |
| **Stage** | Candidate artifact produced (draft skill, proposed thought, suggested rule) | New row in a `staged_candidates` table with `status: pending` | Automatic |
| **Review** | Human sees candidates and approves, rejects, or defers | Dashboard page, Slack thread, or MCP tool `review_candidates` | Human |
| **Merge** | Approved candidate moves to active thoughts/skills/extensions | Edge function triggered by status change to `approved` | Script (after approval) |

Nothing enters the system's active knowledge without passing through Review. The agent may stage aggressively; it may not merge autonomously.

**Concrete OB1 implementation:** A `staged_candidates` table in Supabase with columns: `id`, `created_at`, `source` (which recipe/skill produced it), `category` (thought, skill, rule, config), `content`, `status` (pending/approved/rejected/deferred), `reviewed_at`, `reviewer_notes`. This is the governance layer most OB1 instances are missing.

**Step 4 — Design cadence, not continuous self-modification**

Propose **bounded maintenance windows** rather than always-on self-modification:

- An **orientation sip** (lightweight, repeatable, read-only — a quick MCP call or Slack command that shows: how many staged candidates, how many thoughts added this week, any capture gaps, recommended next action). Multiple per day is fine. This should feel like checking the weather, not running a planning sprint.
- A **consolidation pass** (end-of-day or end-of-week — reviews staged candidates, checks for contradictions in recent thoughts, surfaces thoughts that may have aged out, prunes low-quality captures). This should feel like closing up shop, not starting new work.

If Life Engine is already running, evaluate whether its proactive briefings can serve as the orientation sip. Extend existing recipes before building new ones.

**Step 5 — Handle contradictions and aging**

- When thoughts conflict (two entries about the same topic with different conclusions), **preserve both with a `contradicts` relationship** — do not silently overwrite. Contradictions are signal: they mean you changed your mind, learned something new, or captured context-dependent truth.
- When knowledge has a shelf life, add a `valid_until` or `invalidation_condition` field ("holds while current job," "assumes API v3"). A pg_cron job can scan for expired conditions weekly and surface them for review.

**Step 6 — Propose a minimal first loop**

Propose the **single smallest loop** that creates real governed learning in this OB1 instance. Favor:
- One trigger, one candidate artifact, one review surface
- Uses existing OB1 infrastructure (Supabase table, edge function, MCP tool, or skill)
- Output is a row a human can read and approve

Likely best first loop: **Add a review gate to Claudeception.** When Claudeception generates a new skill from a session, write it to `staged_candidates` with `category: skill` instead of directly to `.claude/skills/`. Surface pending skills in the dashboard or via a Slack message. The user approves or rejects. Approved skills move to the skills directory. This turns Claudeception from "autonomous skill generation" into "governed skill accumulation."

Then propose 3-4 additional loops ranked by leverage, each with the same pipeline structure from Step 3.

**Step 7 — Deliver three outputs**

1. **One-paragraph diagnosis** of this OB1 instance's current recursive limitations — what Claudeception, Auto-Capture, Panning for Gold, and Life Engine actually do vs. what they appear to do
2. **Minimal first implementation** — the single loop to build first, with specific Supabase tables, edge functions, MCP tools, or dashboard pages
3. **Target architecture** — what the governed accumulation layer looks like when 3-4 loops are running, including how they interact and what prevents drift in the thoughts table

Constraints:
- Do not confuse storing more thoughts with learning
- Do not recommend unrestricted autonomous writes to the thoughts table
- Every recursive output must be a visible artifact a human can inspect (row, file, Slack message)
- Prefer extending existing recipes and skills over building new infrastructure
- Be honest about what is missing — saying "I don't know" is better than guessing
```
