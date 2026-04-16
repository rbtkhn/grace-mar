# Operator Decisions

Recurring operator judgment patterns and decision classes.

## Boundary

This file captures recurring decision logic in WORK terms.
It is not a full theory of the operator and not Record truth.

## What belongs here

- recurring decision types
- common inputs used for judgment
- easy vs hard decision classes
- escalation triggers
- common "definition of done" patterns
- decision failure modes
- recurring uncertainty patterns

## Decision classes

*Source: session observation (2026-04-15 through 2026-04-16) + cadence telemetry.*

### Evaluate-then-pick

- Name: proposal evaluation → menu selection
- Typical context: agent presents a plan, assessment, or multi-option menu (A–E); operator evaluates the proposal and picks one or more options
- Inputs usually consulted: the agent's assessment quality, alignment with existing repo conventions, whether the proposal adds maintenance burden
- What makes it easy: the agent's proposal is well-structured with clear tradeoffs; options are real forks, not filler
- What makes it hard: agent presents too many options, or options aren't distinct enough; agent pre-develops options instead of presenting stubs
- What usually determines the answer: whether the proposed work is load-bearing (does it solve a real gap?) and whether it fits existing architecture
- Common failure mode: agent implements before the operator has confirmed; operator's short "a" is misread as approval of something not yet proposed

### Evaluate-external-proposal

- Name: bring external proposal → ask agent to assess
- Typical context: operator pastes a detailed proposal, plan, or external material and asks "do you agree with any of this" or "correct and enhance this plan, unless unwise"
- Inputs usually consulted: repo conventions, existing architecture, doctrinal alignment (AGENTS.md, work-template.md, lane contracts)
- What makes it easy: the proposal is concrete and repo-shaped (not abstract); the agent can compare against existing files
- What makes it hard: the proposal introduces concepts that partially overlap with existing surfaces (risk of duplication)
- What usually determines the answer: alignment with existing patterns + whether the proposal solves a gap no existing lane covers
- Common failure mode: agent accepts the proposal wholesale without checking repo conventions; or agent over-corrects and loses the operator's intent

### Ship-or-defer

- Name: deciding whether to commit/push or keep working
- Typical context: a piece of work is functionally complete; operator decides whether to ship it or extend/refine
- Inputs usually consulted: current git state, whether the work is self-contained, whether downstream lanes need it now
- What makes it easy: the work is clean, tested, and doesn't touch other lanes
- What makes it hard: the work is entangled with pending changes in other files; or there's a known imperfection the operator might want to fix first
- What usually determines the answer: is the work useful as-is? (bias toward shipping increments over perfecting before commit)
- Common failure mode: sitting on completed work too long; or committing half-finished work that requires immediate follow-up

### Lane-pivot

- Name: switching from one WORK territory to another mid-session
- Typical context: a work block is complete (thanks pause logged); operator restarts with coffee or picks a new option from the menu
- Inputs usually consulted: what was just completed, what's pending across lanes, energy level (inferred from prompt length and cadence)
- What makes it easy: clear park line from the prior thanks; fresh coffee with Recent rhythm synthesis
- What makes it hard: no park line; cold thread with no warmup; multiple lanes have pending work
- What usually determines the answer: what the operator is curious about or what feels load-bearing right now (not a fixed priority queue)
- Common failure mode: agent assumes the operator wants to continue the same lane when they actually want to pivot

### Combo-pick

- Name: selecting multiple options simultaneously
- Typical context: agent presents A–E menu; operator responds with "a,b,c" or "b and a" or "A+C"
- Inputs usually consulted: whether the options are independent (can run in parallel) or sequential (must be ordered)
- What makes it easy: options are genuinely independent; agent can sequence them sensibly
- What makes it hard: options have dependencies the operator didn't notice; or the combined scope is too large for one pass
- What usually determines the answer: operator's judgment that multiple small pieces are worth doing together rather than in separate turns
- Common failure mode: agent treats combo as sequential when they could be parallel, or vice versa

## Escalation logic

*Source: session observation.*

- Escalate when: a proposed change touches SELF, Record, or RECURSION-GATE merge authority; or when the operator's intent is ambiguous and the wrong guess would be costly (e.g., "approve" without a candidate ID)
- Do not escalate when: the task is bounded, WORK-only, and the operator has already confirmed scope (e.g., "implement the plan as specified")
- Ask for clarification when: a bare directive could apply to multiple targets (per AGENTS.md: echo candidate ID + summary before merging)
- Default action when uncertainty is acceptable: default to PLAN (per operator-style); propose before editing; answer in prose rather than editing files

## Definition of done patterns

*Source: session observation.*

- Done for analysis: the assessment covers alignment with existing patterns, names specific tradeoffs, and proposes concrete next steps (not open-ended "we could also...")
- Done for writing: the output matches the target format (inbox line, notebook entry, knot, X post); it cites sources where required; it doesn't introduce claims the operator hasn't provided
- Done for strategy: the notebook entry has Signal, Judgment, Links, and Open sections filled; knot index and connections updated; expert threads distilled if relevant
- Done for maintenance: the script runs, the output shape matches the spec, lints are clean, cadence event is logged

## Notes

- Prefer operational distinctions over abstract personality claims.
- The operator's decision style is **selection-heavy**: enumerate options, pick, execute. The agent's job is to enumerate well (real forks, not filler) and execute faithfully after selection.
- "Unless unwise" is a recurring qualifier — it means the operator trusts the agent's judgment to veto individual items in a batch request if there's a concrete reason.
