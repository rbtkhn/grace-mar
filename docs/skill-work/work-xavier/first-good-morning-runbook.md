# First Good Morning Runbook — Xavier

**Scope:** First-ever load of **Xavier’s instance repo** (often named `companion-xavier` on GitHub) by a new Cursor user. Advisor docs (`work-xavier` in grace-mar) live **here**; her Record lives **there**. See [INSTANCE-PATHS.md](INSTANCE-PATHS.md).  
**Goal:** Safe orientation, Session 0 completion, and correct gate workflow.

---

## 1) Session intent

This session is onboarding only.

Do:
- orient to folder purpose and boundaries
- complete Session 0 capture
- stage (do not merge) first candidate set

Do not:
- publish content
- hand-edit identity truth into `self.md`
- copy any `users/grace-mar/**` content into Xavier paths

---

## 2) Operator script (read/send to Xavier)

Hey, Xavier.

Today is your first load in `companion-xavier`.  
This is orientation, not performance.

You are not expected to know Cursor yet.  
Your only goal today is to understand the structure and complete first setup safely.

### What this space is
- **Grace-mar** holds `docs/skill-work/work-xavier/` — operator/advisor module for your coach (optional reading).
- **Your repo:** instance files live under `users/xavier/` (see template / [INSTANCE-PATHS.md](INSTANCE-PATHS.md)).
- The fork starts blank by design.

### What this space is not
- It is not Grace-Mar’s Record.
- Do not copy `users/grace-mar/**` into Xavier instance files.
- Durable identity updates go through the gate pipeline only.

### Non-negotiables
- Human approves public ship.
- No autonomous posting.
- No hand-merge into `self.md`.

---

## 3) Xavier startup script (what she sees)

Hey, Xavier. Welcome to your first session.

Today is orientation and setup:
1. Learn the workspace layout
2. Complete Session 0 capture
3. Stage candidates safely

Important boundary:
- Local notes/chat are not Record truth
- Nothing enters durable identity without gate approval and script merge

If unclear at any step, pause and ask before posting or merging.

---

## 4) First-run checklist (operator + Xavier)

| # | Task | Owner | Done |
|---|---|---|---|
| 1 | Open `docs/skill-work/work-xavier/README.md` | Xavier | [ ] |
| 2 | Open `docs/skill-work/work-xavier/INDEX.md` | Xavier | [ ] |
| 3 | Open `docs/skill-work/work-xavier/GOOD-MORNING.md` | Xavier | [ ] |
| 4 | Open `docs/skill-work/work-xavier/SESSION-0-OPERATOR.md` | Xavier + Operator | [ ] |
| 5 | Complete **her repo** `docs/seed-survey/seed-survey-capture.md` rows (Q1-31) | Xavier | [ ] |
| 5a | Initialize `docs/skill-work/work-business/xavier/` starter pack from survey + business docs | Xavier + Operator | [ ] |
| 6 | Confirm no hand-edits to `users/xavier/self.md` | Operator | [ ] |
| 7 | Stage first candidate set in `users/xavier/recursion-gate.md` | Operator | [ ] |
| 8 | Xavier reviews/approves candidates | Xavier | [ ] |
| 9 | Run merge script only after approval | Operator | [ ] |
| 10 | Add session-log line: first hey complete | Xavier | [ ] |

---

## 5) Execution order (commands and files)

### Required file path sequence (**her repo** root)
1. `docs/seed-survey/seed-survey-initiation.md`
2. `docs/seed-survey/seed-survey-capture.md`
3. `users/xavier/recursion-gate.md`
4. `users/xavier/session-log.md`

### Merge command (only after candidate approval)
```bash
python3 scripts/process_approved_candidates.py --apply
```

---

## 6) Completion criteria

Session passes when:
- Session 0 capture is complete
- at least one candidate set is staged in Xavier gate
- no boundary leak occurred
- first session-log line is written

---

## 7) Escalation rules

Escalate immediately if:
- Xavier asks to copy from Grace-Mar files into her instance
- uncertainty exists about factual merges into identity fields
- stress/confusion with Cursor blocks setup progress

If blocked for more than 10 minutes, switch to screen-share and continue live.

