# Operator Frictions

Recurring annoyances, bottlenecks, and energy drains that reduce leverage.

## Boundary

This file is for operational friction, not general complaint logging.

## What belongs here

- repeated interruptions
- recurring context-switch costs
- unclear or underspecified workflows
- tool pain
- waiting pain
- information retrieval pain
- friction between lanes or rituals
- recurring causes of rework

## Friction log

*Source: session observation (2026-04-15 through 2026-04-16) + cadence telemetry patterns.*

### StrReplace Unicode mismatch

- Name: StrReplace fails on smart quotes / em-dashes
- Frequency: recurring (observed twice in one session)
- Where it appears: editing markdown files that contain Unicode characters (smart quotes `\u201C` `\u201D`, em-dashes `\u2014`)
- Why it matters: blocks file edits; requires fallback to Python scripts with explicit Unicode escapes
- What it costs: 2–5 minutes per occurrence + context switch to write a workaround script
- Current workaround: Python script that reads the file, performs the replacement with correct Unicode, and writes back
- Better fix idea: agent pre-check for Unicode characters in old_string before attempting StrReplace; or normalize smart quotes to ASCII in SKILL files at authoring time

### Shell backtick interpretation

- Name: shell interprets backticks in Python heredocs
- Frequency: occasional (observed once this session)
- Where it appears: running Python scripts via Shell tool when the script string contains markdown backticks
- Why it matters: produces `base64`/`eval` noise in output; sometimes corrupts the file being written
- What it costs: 1–3 minutes to verify whether the script actually succeeded despite the noise, then fix corrupted content
- Current workaround: use `\x60` hex escapes for backticks inside Python strings passed through shell
- Better fix idea: write Python to a temp file first, then execute it (avoids shell interpretation entirely)

### Cursor thread cold start

- Name: new Cursor thread loses all prior context
- Frequency: every thread boundary (multiple times per day given ~6 coffee events/day)
- Where it appears: starting a new Cursor session or thread
- Why it matters: the agent must re-read rules, warm up, and reconstruct state before productive work can start
- What it costs: 30–120 seconds of warmup per thread + risk of doctrinal drift if warmup is skipped
- Current workaround: `harness_warmup.py`, `bridge` transfer prompt, `coffee` Recent rhythm synthesis
- Better fix idea: already mitigated by cadence architecture; further reduction possible with compressed context artifacts (`artifacts/context/`)

### False positive parsing

- Name: keyword-based parsers match documentation/template lines
- Frequency: on first run of new parsers
- Where it appears: `parse_batch_analysis.py` initially matched 26 lines (10 were documentation mentions, not data entries)
- Why it matters: pollutes output with noise; requires a second pass to tighten filters
- What it costs: 5–10 minutes to diagnose and fix
- Current workaround: add structural checks (line must start with the token after cleanup, not just mention it)
- Better fix idea: inbox lines could use a machine-parseable prefix that documentation prose never uses (e.g. always backtick-wrapped)

### StrReplace fuzzy match failures

- Name: StrReplace old_string doesn't match due to whitespace or content drift
- Frequency: occasional (observed in `days.md` Links update this session)
- Where it appears: editing files that have been modified earlier in the same session or by other tools
- Why it matters: blocks the edit; requires re-reading the file to find the exact current content
- What it costs: 1–2 minutes per occurrence
- Current workaround: re-read the target section before each StrReplace
- Better fix idea: always read before edit (already a rule; enforcement is the issue)

## Pattern clusters

- Reentry friction: cold thread start (mitigated by cadence architecture but still the biggest per-occurrence cost)
- Delegation friction: agent sometimes implements before the operator has confirmed (hypothesis mode helps; Plan mode is the structural fix)
- Documentation friction: documentation prose containing the same keywords as data lines creates parsing ambiguity
- Retrieval friction: finding the right file/section in a large repo when context is cold
- Review friction: *(not yet observed — fill in from experience)*

## Downstream candidates

- Feed to cadence: cold-start friction → improve warmup compression; Recent rhythm already helps
- Feed to strategy: *(none identified yet)*
- Feed to think: *(none identified yet)*
- Feed to write: *(none identified yet)*
- Feed to work-dev: StrReplace Unicode issue → consider a pre-flight check script; false positive parsing → inbox format conventions

## Notes

- Prefer repeated pain over one-off annoyance.
- Current log covers one extended session. Patterns will sharpen with more sessions.
- The Unicode and backtick frictions are tool-level (Cursor/shell), not workflow-level — they may resolve with tool updates rather than process changes.
