# Operator Dependencies

People, systems, sources, and timing dependencies that shape the operator's work.

## Boundary

This file is a WORK-side map of what the operator depends on.
It is not a contact book and not a broad systems inventory.

## What belongs here

- people dependencies
- system dependencies
- source dependencies
- timing dependencies
- blocking inputs
- trusted vs weak sources
- external waits that shape workflow

## People dependencies

*Source: session observation + repo structure. Operator should confirm and extend.*

### Companion (grace-mar instance)

- Name / role: the companion whose Record this system serves
- Why it matters: all Record merges require companion approval; the system exists to serve them
- What is usually needed: approval of RECURSION-GATE candidates; feedback on elicitation outputs; direction on lane priorities
- Timing sensitivity: gate candidates queue until companion session; no blocking — operator work continues
- What happens if delayed: pending candidates accumulate; no Record drift since merges are blocked by design

### Xavier / Cici (OB1 adjacent instance)

- Name / role: adjacent companion-self instance (work-xavier lane)
- Why it matters: cross-instance learning, shared template evolution, OB1 upstream patterns
- What is usually needed: GitHub digest, inbox review, journal sync
- Timing sensitivity: daily or as events arise; not blocking for grace-mar core work
- What happens if delayed: xavier journal falls behind; no grace-mar impact

## Systems and tools

*Source: session observation + repo structure.*

### Cursor IDE

- Name: Cursor (AI-assisted IDE)
- Why it matters: primary operator–agent interface; all WORK execution happens here
- Common failure mode: thread context loss (cold start); StrReplace Unicode mismatches; shell backtick interpretation noise
- Workaround if unavailable: git CLI + text editor (degrades to manual); scripts still run standalone

### Git / GitHub (grace-mar repo)

- Name: git + GitHub remote (rbtkhn/grace-mar)
- Why it matters: audit trail, version control, push/pull for persistence across sessions
- Common failure mode: uncommitted work lost on thread boundary; push failures on network issues
- Workaround if unavailable: local commits survive; push when restored

### Cadence scripts (Python)

- Name: `log_cadence_event.py`, `auto_dream.py`, `operator_coffee.py`, `harness_warmup.py`
- Why it matters: cadence telemetry, warmup grounding, dream maintenance — system rhythm depends on these
- Common failure mode: script raises on missing optional dependencies (civ-mem, relevance index); strict mode halts
- Workaround if unavailable: manual cadence logging; skip warmup (degrades reentry quality)

### Strategy notebook scripts

- Name: `strategy_thread.py`, `parse_batch_analysis.py`, `strategy_expert_corpus.py`
- Why it matters: thread triage, expert distillation, batch-analysis snapshot generation
- Common failure mode: inbox format drift breaks parsers; new expert IDs not added to canonical tuple
- Workaround if unavailable: manual triage and distillation (slower but functional)

## Sources

*Source: session observation + inbox structure.*

### Wire sources (§1d–§1h channels)

- Name: §1d Kremlin/MID, §1e US executive, §1g PRC MFA, §1h IRI MFA/IRGC, Rome/Pontifex
- Trust level: primary (official statements, transcripts, MFA readouts)
- Why used: ground strategy notebook Signal and Judgment in attributed, datable material
- Typical use: wire capture lines in daily-strategy-inbox.md with `verify:` tails
- Caution: official statements are positions, not ground truth; treat as declared intent, not operational fact

### Expert commentariat (strategy-commentator-threads)

- Name: 21 canonical expert IDs (Mercouris, Mearsheimer, Barnes, Ritter, Davis, Parsi, etc.)
- Trust level: analytical overlay — not primary sources; each has documented lanes and biases
- Why used: multi-frame analysis; thread distillation; notebook Judgment composition
- Typical use: `thread:<expert_id>` tags on inbox lines; `crosses:` and `seam:` on batch-analysis
- Caution: expert claims require tier discipline (verify against primaries before folding into Judgment)

### Cadence telemetry

- Name: work-cadence-events.md
- Trust level: high (machine-generated, append-only)
- Why used: rhythm analysis, reentry grounding (Recent rhythm), session continuity
- Typical use: read by coffee/thanks/dream/bridge skills; analyzed by elicitation (this lane)
- Caution: records events, not intentions; frequency != importance

## Timing dependencies

- Same-day dependencies: wire sources update throughout the day; strategy notebook captures are time-sensitive (news cycle); cadence events must be logged before thread boundary
- Weekly dependencies: expert thread distillation (7-day rolling window); weekly brief run (work-politics)
- Event-driven dependencies: RECURSION-GATE candidates queue until companion session; breaking news triggers wire capture; OB1 upstream changes trigger xavier sync

## Notes

- Focus on what actually changes workflow, not every possible dependency.
- This file is grounded in one session's observation. The people dependencies section is thin — expand after operator review.
- Tool dependencies are skewed toward Cursor/git because that's where the work happens; external tools (Telegram, WeChat) are not yet documented here.
