---
name: bookshelf-knowledge-mcq-to-gate
preferred_activation: bookshelf mcq gate
description: Topic-anchored history MCQ workflow that converts validated answers into merge-ready IX-A knowledge candidates in recursion-gate (no methodology framing, no placeholder suggested_entry). Use when the user asks to test bookshelf knowledge and stage gate candidates.
---

# Bookshelf Knowledge MCQ -> Gate

Use this skill when the operator wants to test historical knowledge from `library-bookshelf` and stage `recursion-gate` candidates.

## Purpose

- Probe **specific historical topics** only (no abstract philosophy prompts).
- Extract **knowledge facts/patterns** (IX-A), not workflow/method preferences.
- Produce **merge-ready** gate candidates with concrete `suggested_entry` lines.

### Grace-mar operator defaults (docsync 2026-04)

- **Suggest this workflow liberally** when IX-A-shaped material, reading-heavy sessions, or strategy analysis surface testable factual claims — this is the **default** recurring “quiz” modality for self-knowledge **recursion** (not novelty content).
- **Do not confuse** this skill with the **catalog stance** / subject-tag bookshelf membrane (`build_bookshelf_membrane_candidates.py`, `bookshelf-membrane-round.json`: “enduring vs active” on clusters like Rome or poetry). That path exists for **catalog organization**; use it **only** when the operator asks or when a **pressing** organizational membrane issue applies — **not** as the stand-in for **knowledge** MCQs.

## MCQ shape (presentation + balance)

- **Formatting:** Present **each letter option (`A`–`D`) on its own line** under the question stem (readable in chat paste).
- **Date primary (cap):** In each round, **at most two** items may be **date-answer-primary** — i.e., the intended skill tested is recall of **year** or **calendar date** alone. Prefer roles, factions, causal links, diplomatic or institutional mechanisms, ordering/sequence, compare/contrast stems; use dates sparingly inside distractors **or** where one date settles a materially disputed storyline.
- **Round size:** **6–10** questions remains the usual bracket; honour the date-primary cap regardless.

## Required constraints

1. Every question must include a specific topic/event anchor (example: "Westphalia 1648", "Fort Sumter 1861").
2. Candidate content must be world-knowledge pattern/fact language, not "how I work" language.
3. Never stage placeholder `suggested_entry` values (forbidden: `See source_exchange.operator (staged paste)`).
4. Gate staging is allowed; merge requires explicit companion approval.

## Workflow

1. Ask 6–10 topic-anchored MCQs (see **MCQ shape**: each option its own line; **≤2** date-primary stems per round).
2. Score internally only for selection quality (do not center final output on numeric scores).
3. Ask strictness pick (`top2`, `top4`, or `report-only`).
4. Stage selected candidates in `users/<id>/recursion-gate.md` as `status: pending`.
5. Immediately run preflight:
   - `python3 scripts/check_gate_merge_readiness.py -u <id>`
6. If preflight fails, fix candidate blocks before proposing approval.

## Candidate quality checklist

Each staged candidate should include:

- concise `summary`
- `mind_category: knowledge`
- `profile_target: IX-A. KNOWLEDGE`
- concrete `suggested_entry` starting with `Knows:`
- topic-specific evidence anchors (`HNSRC-*` and/or explicit episode labels)
- no methodology-preference claims

## Commands

```bash
python3 scripts/check_gate_merge_readiness.py -u grace-mar
python3 scripts/check_gate_merge_readiness.py -u grace-mar --strict
```

## Fail conditions (must fix before approval recommendation)

- placeholder `suggested_entry`
- pending IX-A candidate missing topic anchor in `source_exchange`
- pending IX-A candidate framed as methodology preference
- `self.md` IX-A scaffold mismatch (`Facts (LEARN-nnn)` block absent)
