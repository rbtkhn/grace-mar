# Current-Events Analysis (WORK-STRATEGY)

**Status:** WORK only. Run as staged prototype or via bot session; outputs → recursion-gate staging. No direct Record writes.

## Pipeline

1. **Perceiver (neutral fact summary)**
   - Extract: who / what / when / where / why / how + primary sources.
   - Output: Neutral fact summary (≤200 words).

1.5 **Energy-Chokepoint Hook (mandatory for any energy-related event)**
   - Run [modules/energy-chokepoint/perceiver-hook.py](modules/energy-chokepoint/perceiver-hook.py).
   - Append to neutral fact summary: chokepoint status + CIV-MEM parallel (e.g. 1973 embargo, 1990 Kuwait).
   - Log to WORK docs / session notes; optional ACT- only when companion approves a candidate that creates an audit line.

2. **Analyst (4-lens breakdown)**
   - Historical / CIV-MEM parallel: What patterns from civilizational memory match?
   - Systems impact: Economic, tech, geopolitical, ecological ripple effects.
   - (Other lenses as defined in territory.)

3. **Council Deliberation**
   - (As defined in persuasive-content-pipeline.)

4. **Draft Generation**
   - (As defined in persuasive-content-pipeline.)

5. **Triangulation Stage — Specialized Minds (mandatory)**
   - Run the three analytical lenses ([work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md)) on the same neutral fact summary.
   - Structural / operational / institutional views; surface tensions.

5.5 **Synthesis (after three minds)**
   - Run [synthesis-engine](synthesis-engine.md) (e.g. `prototypes/mind-synthesis.py`).
   - Output block: **Convergence** | **Productive Tensions** | **Grace-Mar Synthesis**.
   - Do **not** run synthesis at ingest (step 1.5); only here after the three minds.

5.6 **Deliberation receipt (optional)**
   - For runs that need an auditable WORK trail, complete [modules/verifiable-personal-ai/deliberation-receipt-template.md](modules/verifiable-personal-ai/deliberation-receipt-template.md) and store next to the draft or link from the gate candidate.
   - “Verifiable” = documented process and sign-off, not cryptographic proof. See [modules/verifiable-personal-ai/manifest.md](modules/verifiable-personal-ai/manifest.md).

**Council output:** Consolidated markdown draft + citations → staged for approval. All usage gated via recursion-gate + companion approval.
