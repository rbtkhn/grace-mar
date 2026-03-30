---
name: massie-x-news-search-draft
description: "Draft-only X copy for @usa_first_ky (unofficial KY-4 analysis): real-time web search, cited news briefs, suggested posts—operator must approve before any post; never auto-post or publish. Triggers: Massie X, tweet draft, KY-4 news today, breaking story hooks, usa_first_ky."
---

# Massie X — real-time news search and draft posts

Use this skill when drafting **suggested** X (Twitter) content for the **America First Kentucky** account (@usa_first_ky). The agent **searches the live web** for recent stories, then produces **draft-only** posts for human review. **No autonomous posting.**

## Canonical context (read as needed)

- Account rules, tone, workflow: [docs/skill-work/work-politics/account-x.md](docs/skill-work/work-politics/account-x.md)
- Principal positions (do not invent): [docs/skill-work/work-politics/principal-profile.md](docs/skill-work/work-politics/principal-profile.md)
- Opposition snapshot: [docs/skill-work/work-politics/opposition-brief.md](docs/skill-work/work-politics/opposition-brief.md)
- Doctrine filter: [docs/skill-work/work-politics/clients/massie-ky4-operator-checklist.md](docs/skill-work/work-politics/clients/massie-ky4-operator-checklist.md)
- Issue wedges (optional hooks): [docs/skill-work/work-politics/clients/massie-issue-asymmetry.md](docs/skill-work/work-politics/clients/massie-issue-asymmetry.md)
- Polling + Polymarket (good morning routine): [docs/skill-work/work-politics/polling-and-markets.md](docs/skill-work/work-politics/polling-and-markets.md) — if you cite odds or polls in X copy, **caveat** (markets ≠ vote shares; internals ≠ public polls).

## Hard guardrails

| Rule | Detail |
|------|--------|
| **Draft only** | Output is for **Xavier** (SMM) to edit and post from @usa_first_ky. Never imply the post is live. |
| **Not the principal** | Do not write as Rep. Massie or as official campaign. Unofficial analysis = analysis + context + message support. |
| **Cite everything** | Every factual claim in the news brief and every hook in a draft must trace to a **search result URL** (or principal-profile / house.gov if static). No unsourced speculation. |
| **Documented positions** | Tie posts to **documented** Massie stances (profile, votes, public quotes). If the story doesn’t map, say “no clean Massie hook” and offer neutral context-only drafts or skip. |
| **Doctrine pass** | Prefer engineer/farmer, anti-waste, anti-surveillance/war framing; one KY-4-plain sentence per idea; avoid forced culture-war cosplay. |
| **Tone** | Professional, evidence-based, pro–principal, not slash-and-burn. No personal attacks. |

## Workflow

### 1. Clarify scope (if missing)

If the operator gave no topic, default searches:

- `Thomas Massie KY-4` OR `Massie Congress` (last few days)
- `KY-4 House primary 2026` OR `Ed Gallrein`
- `from:RepThomasMassie OR site:x.com RepThomasMassie` (his latest X posts)
- One national lane tied to profile: e.g. `Iran war powers Congress`, `Epstein files DOJ`, or `FISA House vote` (pick what’s timely)

If they named a topic, run **2–4 focused queries** on that topic plus one KY-4 race query.

### 2. Real-time news search

- Use **web search** (or equivalent) to pull **recent** articles (prefer last 24–72 hours unless operator specifies).
- Collect **5–10 bullet facts** with **title + outlet + date + URL**.
- Drop duplicate angles; flag **unverified** or **single-source** items.

### 3. Map stories to Massie

For each promising item:

- Does it connect to a **documented** position or record? (See principal-profile, asymmetry doc.)
- **Primary vs general** audience: adjust framing (intra-R consistency vs crossover kitchen-table).
- If no honest hook, list under “No post — monitor only.”

### 4. Generate suggested X posts

Deliver in this order:

**A. News scan (for operator)**

- Short table or bullets: story | why it matters for KY-4 / Massie | URL

**B. Draft posts — `DRAFT — NOT POSTED — @usa_first_ky`**

For each idea:

- **Hook** (one line): what the tweet is doing.
- **Suggested tweet(s):** 1–3 variants, **≤280 characters** each (note if thread needed).
- **Sources:** URLs the copy depends on.
- **Risk note:** e.g. defamation, stale fact, or “needs principal quote check.”

**C. Optional thread**

- Numbered outline (Tweet 1 / 2 / 3) with character estimates; same sourcing discipline.

**D. Reply / quote opportunities**

- If Massie or Gallrein posted recently (only if search confirms), 1–2 **reply-style** drafts that add context + link — still draft-only.

### 5. Close the loop

- Remind: **Xavier approves** before any post.
- If useful: suggest logging in [content-queue.md](docs/skill-work/work-politics/content-queue.md) as idea → draft.

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

**Operator:** Review with account-x guidelines; SMM posts only after approval.
```

## When search is thin

Say so plainly. Offer: (1) broaden query, (2) pivot to evergreen wedge from asymmetry doc with a fresh headline from search, or (3) wait for next news cycle.
