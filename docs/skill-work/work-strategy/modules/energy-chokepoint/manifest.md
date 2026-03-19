# Energy-Chokepoint Monitoring (WORK-STRATEGY module)

**Status:** WORK only. Not part of SELF or Record unless the companion approves a candidate that documents usage (e.g. optional ACT- via RECURSION-GATE).

## Purpose

Real-time ingestion of shipping, refinery, and sanction signals for every current-event analysis that touches energy or multipolar stress.

## Mandatory Triggers

- Strait of Hormuz tanker count
- South Pars / Ras Laffan / Mina Al-Ahmadi status
- Sanction reversal signals (Treasury/IEA statements)
- Price spikes >5% in 24h

## Integration Points

- Feeds directly into Perceiver stage ([current-events-analysis.md](../../current-events-analysis.md))
- Requires CIV-MEM cross-ref (1973, 1990, 1979 patterns) when relevant
- Logging: use WORK docs (briefs, module output, session notes) and/or optional ACT- entry only when the companion approves a candidate that creates an audit line (e.g. “we used energy-chokepoint for event X”). Do **not** append full deliberation traces to `self-evidence.md`.

All usage gated via recursion-gate.md + approval inbox.
