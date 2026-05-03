# cici-ai Daily Report Template

**Status:** WORK / daily synthesis template  
**Scope:** `cici-ai` team activity, progress, and evidence synthesis  
**Boundary:** This is a reporting template only. It does not replace source evidence, the dashboard, or the weekly governance review.

---

## Purpose

Use this template to produce one daily report that synthesizes:

- GitHub activity
- Telegram group messages
- cici-ai docs and tracking files

The report should show what changed, who moved forward, what remains blocked, and what should happen next.

---

## Daily report structure

```md
# cici-ai Daily Report

- Date:
- Reporting window:
- Sources reviewed:
- Confidence level of report: A / B / C

## Executive Summary

One short paragraph on the overall state of the team.

## Key Activity

- Bullet the most important GitHub and Telegram signals from the day.

## Member Progress

| Member | GitHub | Telegram signal | Progress | Confidence |
|---|---|---|---|---|
|  |  |  |  |  |

## GitHub Signals

- New forks
- New commits
- New PRs / issues
- Repo edits
- Visible implementation of personal goals

## Telegram Signals

- New introductions
- Fork confirmations
- Goal statements
- Questions
- Peer-help moments

## Documents Updated

- List the cici-ai docs that changed or were added.
- Say why each one matters.

## Blockers / Open Loops

- Who still needs confirmation
- Which evidence is incomplete
- Which goals are still only self-reported

## Next Actions

- Short, specific recommendations for the operator or team

## Confidence Notes

- A = direct repo-visible or artifact-visible evidence
- B = operator-visible evidence or direct chat evidence
- C = self-report or inference requiring confirmation
```

---

## Reporting rules

- Prefer evidence over summary language.
- Use GitHub links, Telegram evidence, or document links when possible.
- Do not mark a step as complete without visible proof.
- Separate self-report from confirmed evidence.
- If Telegram and GitHub disagree, show the mismatch instead of smoothing it over.
- Keep the tone factual, warm, and operator-friendly.

---

## Good report behavior

- Treat GitHub as the proof layer.
- Treat Telegram as the coordination layer.
- Treat docs as the memory and tracking layer.
- Keep the report short enough to read quickly, but specific enough to act on.

---

## Prompt note for report agents

When generating a daily report for `cici-ai`, follow this template exactly unless the operator asks for a shorter form:

- Use the section order in this file.
- Put the executive summary first.
- Use the member progress table for per-person status.
- Call out GitHub evidence before Telegram-only signals when both exist.
- Mark uncertainty clearly with the confidence labels.
- Mention documents updated only when there is a real file change.
- End with short next actions, not a long essay.

---

## Suggested sources to review

- `docs/skill-work/work-cici/cici-ai-community-dashboard.md`
- `docs/skill-work/work-cici/cici-ai-first-task-proof-packet.md`
- `docs/skill-work/work-cici/cici-ai-weekly-governance-review-template.md`
- `docs/skill-work/work-cici/cici-ai-progress/README.md`
- `docs/skill-work/work-cici/cici-ai-telegram/README.md`
- `docs/skill-work/work-cici/evidence/`
- Telegram export / transcript files
- Recent GitHub commit / fork activity
