# Persuasive Content Pipeline (WORK-STRATEGY)

**Status:** WORK only. Outputs staged for approval; no direct Record writes.

## Steps

1. **Ingest Event**
   - Via OpenClaw hook, Telegram, manual paste, or newsletter trigger.
   - Log raw input per territory policy (WORK docs / session log; optional ACT- only when companion approves a candidate).

1.5 **Energy + Multipolar Auto-Flags (ingest-time only)**
   - Run [modules/energy-chokepoint/perceiver-hook.py](modules/energy-chokepoint/perceiver-hook.py) for energy-related events.
   - Do **not** run mind-synthesis here; synthesis runs only after the three minds (triangulation stage, step 5 / 5.5 in [current-events-analysis.md](current-events-analysis.md)).

2. **Council Deliberation**
   - (As defined in territory.)

2.5 **Triangulation (mandatory)**
   - Invoke the three analytical lenses per [work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md).
   - Then run [synthesis-engine](synthesis-engine.md) (e.g. `prototypes/mind-synthesis.py`) to produce the **Convergence** | **Productive Tensions** | **Grace-Mar Synthesis** block.

3. **Draft Generation**
   - Consolidate into markdown draft + citations; stage for approval.

3.5 **Deliberation receipt (optional)**
   - Before staging, attach a completed [verifiable-personal-ai receipt](modules/verifiable-personal-ai/deliberation-receipt-template.md) if the companion or operator wants a one-page audit trail (steps, sources, sign-off).

All usage gated via recursion-gate + companion approval.
