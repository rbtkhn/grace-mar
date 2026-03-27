# companion-xavier dry-run prompts

Use these prompts in order for a deletion-readiness validation run.

---

## Prompt 1 — clean-room setup check

```text
I am running a clean-room template bootstrap test.

Goal:
- validate that onboarding works from companion-self template without companion-xavier-specific rescue steps.

Please:
1) List required files in this repo for the first-run flow.
2) Flag any missing prerequisites.
3) Give me the first 3 actions only.
```

## Prompt 2 — seed survey + capture completion

```text
Guide me through completing Session 0 seed survey safely.

Rules:
- use the 30-question survey only
- record in seed-survey-capture.md
- no edits to self.md

When done, summarize which answers should likely map to curiosity vs personality vs WORK config.
```

## Prompt 3 — WORK intake initialization

```text
Use my capture answers and uploaded business docs to initialize WORK intake.

Create or update:
- work-business/<instance>/source-index.md
- work-business/<instance>/objectives-and-constraints.md
- work-business/<instance>/week-0-priority-stack.md

Rules:
- cite source files
- keep outputs 7-day actionable
- do not write identity files
```

## Prompt 4 — full good-morning run

```text
Run the full good-morning workflow for this instance.

Include:
1) work-dev sync check + score
2) work-politics sync check + score
3) template alignment check vs companion-self GitHub upstream (repo + ref)
4) SYNC-DAILY updates
5) DAILY-OPS-CARD draft

Show any blockers clearly.
```

## Prompt 5 — gate-safe staging

```text
Stage first candidate set from today's outputs.

Rules:
- write only recursion-gate.md
- no self.md edits
- keep claims neutral and sourceable
- show diff before apply
```

## Prompt 6 — deletion readiness verdict

```text
Evaluate deletion readiness using:
- COMPANION-XAVIER-DELETION-READINESS.md

Return:
- PASS/FAIL per section
- top 3 blockers (if any)
- smallest next fixes to reach delete-ready state
```

