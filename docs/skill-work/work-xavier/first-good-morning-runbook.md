# First Good Morning Runbook — Xavier

**Scope:** First-ever load of `companion-xavier` by a new Cursor user.  
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

Good morning, Xavier.

Today is your first load in `companion-xavier`.  
This is orientation, not performance.

You are not expected to know Cursor yet.  
Your only goal today is to understand the structure and complete first setup safely.

### What this space is
- `work-xavier` is the interface layer.
- Your instance files live in `companion-xavier/users/xavier/`.
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

Good morning, Xavier. Welcome to your first session.

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
| 5 | Complete `seed-survey-capture.md` rows (Q1-31) | Xavier | [ ] |
| 5a | Initialize `docs/skill-work/work-business/xavier/` starter pack from survey + business docs | Xavier + Operator | [ ] |
| 6 | Confirm no hand-edits to `users/xavier/self.md` | Operator | [ ] |
| 7 | Stage first candidate set in `users/xavier/recursion-gate.md` | Operator | [ ] |
| 8 | Xavier reviews/approves candidates | Xavier | [ ] |
| 9 | Run merge script only after approval | Operator | [ ] |
| 10 | Add session-log line: first good morning complete | Xavier | [ ] |

---

## 5) Execution order (commands and files)

### Required file path sequence
1. `companion-xavier/docs/seed-survey/seed-survey-initiation.md`
2. `companion-xavier/docs/seed-survey/seed-survey-capture.md`
3. `companion-xavier/users/xavier/recursion-gate.md`
4. `companion-xavier/users/xavier/session-log.md`

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

