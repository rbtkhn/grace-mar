---
name: politics-massie
preferred_activation: massie x
description: 'Draft-only X copy for @usa_first_ky (unofficial KY-4 analysis): real-time web search, cited news briefs, suggested posts—operator must approve before any post; never auto-post or publish. Triggers: politics-massie, Massie X, tweet draft, KY-4 news today, breaking story hooks, usa_first_ky.'
portable: true
version: 1.1.0
tags:
- operator
- work-politics
- social
portable_source: skills-portable/politics-massie/SKILL.md
synced_by: sync_portable_skills.py
---
# Massie X — real-time news search and draft posts

**Preferred activation (operator):** say **`massie x`**.

Use this skill when drafting **suggested** X (Twitter) content for the **America First Kentucky** account (@usa_first_ky). The agent **searches the live web** for recent stories, then produces **draft-only** posts for human review. **No autonomous posting.**

## Canonical context (configure in your instance)

Map these to **your** repo or handbook (see **Cursor / grace-mar instance** appendix when using grace-mar):

| Topic | What to link |
|--------|----------------|
| Account rules, tone, workflow | SMM / brand doc for the shadow analysis account |
| Principal positions | Profile or policy sheet — **do not invent** stances |
| Opposition / race context | Brief or filing summarizing challengers and dynamics |
| Doctrine / messaging checklist | Internal checklist for what the account may imply |
| Issue wedges | Optional hook map (asymmetry / priorities) |
| Polling / markets | If you cite odds or polls, **caveat**: markets ≠ vote shares; internals ≠ public polls |

## Hard guardrails

| Rule | Detail |
|------|--------|
| **Draft only** | Output is for **SMM** to edit and post. Never imply the post is live. |
| **Not the principal** | Do not write as the officeholder or as official campaign unless explicitly authorized. Unofficial analysis = analysis + context + message support. |
| **Cite everything** | Every factual claim in the news brief and every hook in a draft must trace to a **search result URL** (or your static policy doc if allowed). No unsourced speculation. |
| **Documented positions** | Tie posts to **documented** stances (profile, votes, public quotes). If the story doesn’t map, say “no clean hook” and offer neutral context-only drafts or skip. |
| **Doctrine pass** | Match your account checklist: tone, taboo topics, local vs national framing. |
| **Tone** | Professional, evidence-based, pro–principal where aligned; avoid personal attacks unless your doctrine explicitly allows contrast ads. |

## Workflow

### 1. Clarify scope (if missing)

If the operator gave no topic, default searches:

- `Thomas Massie KY-4` OR `Massie Congress` (last few days)
- `KY-4 House primary 2026` OR `Ed Gallrein`
- `from:RepThomasMassie OR site:x.com RepThomasMassie` (latest X posts)
- One national lane tied to profile: e.g. `Iran war powers Congress`, `Epstein files DOJ`, or `FISA House vote` (pick what’s timely)

If they named a topic, run **2–4 focused queries** on that topic plus one KY-4 race query.

### 2. Real-time news search

- Use **web search** (or equivalent) to pull **recent** articles (prefer last 24–72 hours unless operator specifies).
- Collect **5–10 bullet facts** with **title + outlet + date + URL**.
- Drop duplicate angles; flag **unverified** or **single-source** items.

### 3. Map stories to principal

For each promising item:

- Does it connect to a **documented** position or record?
- **Primary vs general** audience: adjust framing (intra-party consistency vs crossover kitchen-table).
- If no honest hook, list under “No post — monitor only.”

### 4. Generate suggested X posts

Deliver in this order:

**A. News scan (for operator)**

- Short table or bullets: story | why it matters for KY-4 / principal | URL

**B. Draft posts — `DRAFT — NOT POSTED — @usa_first_ky`**

For each idea:

- **Hook** (one line): what the tweet is doing.
- **Suggested tweet(s):** 1–3 variants, **≤280 characters** each (note if thread needed).
- **Sources:** URLs the copy depends on.
- **Risk note:** e.g. defamation, stale fact, or “needs quote check.”

**C. Optional thread**

- Numbered outline (Tweet 1 / 2 / 3) with character estimates; same sourcing discipline.

**D. Reply / quote opportunities**

- If principal or challenger posted recently (only if search confirms), 1–2 **reply-style** drafts that add context + link — still draft-only.

### 5. Close the loop

- Remind: **SMM approves** before any post.
- If useful: suggest logging in your **content queue** doc as idea → draft.

## Output template (copy-paste)

```markdown
## Massie X — news + drafts (DRAFT)

**Searched:** [queries used]  
**As of:** [date]

### News brief
- ...

### Suggested posts (NOT POSTED)
1. **Hook:** ...  
   **Tweet:** ...  
   **Sources:** ...

### Skip / monitor
- ...

**Operator:** Review with account guidelines; SMM posts only after approval.
```

## When search is thin

Say so plainly. Offer: (1) broaden query, (2) pivot to evergreen wedge from your asymmetry doc with a fresh headline from search, or (3) wait for next news cycle.

---

## After the draft run — doc-only loop

**Optional:** If the same **search** or **doctrine** gap repeats, add **one** line to your **account checklist** (instance path) or to this portable core. Draft output still needs human approval before any post. In grace-mar, the instance appendix lists the canonical checklist path.


## Cursor / grace-mar instance

Use these paths **in this repository** when applying the portable skill. Replace with your own tree when forking.

| Topic | Path |
|--------|------|
| Account rules, tone, workflow | [account-x.md](../../../docs/skill-work/work-politics/account-x.md) |
| Principal positions | [principal-profile.md](../../../docs/skill-work/work-politics/principal-profile.md) |
| Opposition snapshot | [opposition-brief.md](../../../docs/skill-work/work-politics/opposition-brief.md) |
| Doctrine filter | [massie-ky4-operator-checklist.md](../../../docs/skill-work/work-politics/clients/massie-ky4-operator-checklist.md) |
| Issue wedges | [massie-issue-asymmetry.md](../../../docs/skill-work/work-politics/clients/massie-issue-asymmetry.md) |
| Polling + Polymarket | [polling-and-markets.md](../../../docs/skill-work/work-politics/polling-and-markets.md) |
| Content queue (optional log) | [content-queue.md](../../../docs/skill-work/work-politics/content-queue.md) |

**SMM label in portable body:** In grace-mar, **Xavier** = SMM role for @usa_first_ky (see account-x doc).
