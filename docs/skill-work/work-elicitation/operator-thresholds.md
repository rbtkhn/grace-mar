# Operator Thresholds

Operational thresholds for escalation, sufficiency, review, and stop/continue decisions.

## Boundary

This file captures practical thresholds that make delegation and routing safer and more useful.
It is not legal policy and not Record truth.

## What belongs here

- good-enough thresholds
- escalation thresholds
- review thresholds
- stop conditions
- continue conditions
- uncertainty tolerance
- acceptable autonomy boundaries

## Good enough

*Source: session observation (2026-04-15 through 2026-04-16). Operator should confirm and extend.*

### Strategy notebook entry

- Name: daily `days.md` entry (Signal / Judgment / Links / Open)
- Good enough means: Signal has attributed wire captures with dates and sources; Judgment names tensions and does not collapse distinct positions; Links has at least one primary URL per claim; Open has falsifiable follow-up items
- Not good enough when: Judgment merges distinct actors into one position ("Iran says"); Links are missing primaries; Open items are vague ("follow up on this")
- Typical acceptable imperfection: some Links may be `verify:` stubs awaiting URL confirmation; Open items may be speculative

### Synthesis knot

- Name: strategy-notebook-knot-*.md
- Good enough means: thesis is falsifiable; page type is marked; Judgment section has at least one named tension; connections to sister knots are wired in knot-connections.yaml
- Not good enough when: thesis is a summary rather than a claim; no connections to existing knots; clusters/patterns not indexed in knot-index.yaml
- Typical acceptable imperfection: some "Weak bridge" connections may be provisional

### Script / parser

- Name: Python scripts under scripts/
- Good enough means: runs against real data without errors; output shape matches the architecture spec; CLI has sensible defaults; lints clean
- Not good enough when: false positives in output; missing edge cases that corrupt downstream consumers; no CLI help text
- Typical acceptable imperfection: alias matching may have low-confidence false positives (flagged as `confidence: low`)

### WORK lane scaffold

- Name: new work-* territory
- Good enough means: README with boundary, contents table, related links; history file in standard format; registered in skill-work README and history principle
- Not good enough when: missing lane contract elements (per work-template.md checklist); boundary section omits governing gate; not registered
- Typical acceptable imperfection: operator-working files may be blank scaffolds on first ship

### Cadence event

- Name: coffee / thanks / dream / bridge log line
- Good enough means: kind, user, ok status, and relevant key-value pairs logged; park text is a meaningful slug (not `none`)
- Not good enough when: event is silently skipped; park text is generic filler
- Typical acceptable imperfection: `cursor_model=unknown` (env var not set)

## Escalate

### Record / SELF boundary

- Trigger: any proposed edit to `self.md`, `self-archive.md`, or `bot/prompt.py`
- Why escalate: these are Record truth surfaces; only companion-approved merges via `process_approved_candidates.py` are authorized
- When not to escalate: WORK-only edits that never touch Record surfaces
- Preferred escalation surface: echo CANDIDATE-XXXX + one-line summary before any merge action

### Ambiguous operator intent

- Trigger: bare "approve" without candidate ID; short directive that could apply to multiple targets; "do it" when scope is unclear
- Why escalate: wrong guess is costly (irreversible merge, wrong file edited)
- When not to escalate: operator has already confirmed scope in this thread (e.g., "implement the plan as specified")
- Preferred escalation surface: list plausible candidates with one-line summaries and ask

### Doctrinal drift

- Trigger: proposed change contradicts AGENTS.md, operator-style, or lane contracts
- Why escalate: drift compounds silently; better to name it immediately
- When not to escalate: the operator explicitly overrides (e.g., "unless unwise" qualifier means they trust the agent to veto)
- Preferred escalation surface: inline note in the reply naming the specific drift and the governing rule

## Review

### Agent-authored prose (strategy, analysis, X drafts)

- Requires review when: always — no auto-publish from agent to any external surface
- Can skip review when: never for public-facing output
- Common false positive: agent shows a draft and operator says "good" meaning "I see it" not "publish it"

### WORK file edits

- Requires review when: first population of a blank file (show checkpoint summary); edits that change boundary or membrane
- Can skip review when: appending a history line; logging a cadence event; mechanical registration (adding a row to a table)
- Common false positive: agent asks for confirmation on trivial edits that slow the operator down

### Commit scope

- Requires review when: commit touches files in multiple unrelated lanes; commit includes both WORK and Record-adjacent files
- Can skip review when: commit is scoped to one lane and the operator said "commit and push"
- Common false positive: cadence event file (work-cadence-events.md) is modified alongside unrelated work — this is normal, not a scope concern

## Stop / continue

- Stop when: the operator says `thanks` (micro-pause), `dream` (day-close), or `bridge` (session seal); or when four attempts at the same action fail without new evidence
- Continue when: the operator picks from a menu (letter selection); says "implement the plan"; or combines options ("a,b,c, unless unwise")
- Ask when: the operator's intent is ambiguous; the combined scope of a combo-pick might be too large for one pass; a proposed edit touches a surface the operator hasn't explicitly named

## Notes

- Thresholds should help downstream lanes act with less ambiguity.
- The "unless unwise" qualifier is a standing delegation: the operator trusts the agent to veto individual items in a batch if there's a concrete reason, without needing to ask first.
- "Good enough" in this system biases toward shipping increments. Perfecting before commit is a known anti-pattern; the operator prefers to ship and iterate.
