# Current-Events Analysis (WORK-STRATEGY)

**Status:** WORK only. Run as staged prototype or via bot session; outputs → recursion-gate staging. No direct Record writes.

## Pipeline

### 1. Perceiver (neutral fact summary)

- Extract: who / what / when / where / why / how + primary sources.
- Output: Neutral fact summary (≤200 words).
- **Long-form ingest:** Transcripts from **[Predictive History](../../../research/external/youtube-channels/predictive-history/README.md)** (bulk `.txt`) or digests under [work-strategy/transcripts/](../../../research/external/work-strategy/transcripts/README.md) are valid inputs — still produce **neutral** summary, not lecturer rhetoric as fact. See [common-inputs.md § PH](common-inputs.md).

### 1.5 Energy-Chokepoint Hook (mandatory for any energy-related event)

- Run [modules/energy-chokepoint/perceiver-hook.py](modules/energy-chokepoint/perceiver-hook.py).
- Append to neutral fact summary: chokepoint status + CIV-MEM parallel (e.g. 1973 embargo, 1990 Kuwait).
- Log to WORK docs / session notes; optional ACT-only when companion approves a candidate that creates an audit line.

### 2. Analyst (4-lens breakdown)

- Historical / CIV-MEM parallel: What patterns from civilizational memory match?
- Systems impact: Economic, tech, geopolitical, ecological ripple effects.
- (Other lenses as defined in territory.)

### 2.5 Analogy Audit (mandatory when a historical parallel is proposed)

Use [analogy-audit-template.md](analogy-audit-template.md).

For any historical analogy or CIV-MEM parallel proposed during analysis, record:

- the analogy explicitly
- strongest structural fit
- strongest mismatch
- falsifier
- usefulness judgment
- risk of overextension
- recommended usage: illustrative / framing only / core model

**Rule:** No analogy should pass into final synthesis unmarked.  
If the analogy is weak, misleading, or merely decorative, say so explicitly.

### 3. Council Deliberation

- (As defined in persuasive-content-pipeline.)

### 4. Draft Generation

- (As defined in persuasive-content-pipeline.)

### 5. Triangulation Stage — Specialized Minds (mandatory)

- Run the three analytical lenses ([work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md)) on the same neutral fact summary.
- Structural / operational / institutional views; surface tensions.
- Where relevant, carry forward the analogy-audit judgment so the three minds respond to the same clarified framing rather than an unexamined historical comparison.

### 5.5 Synthesis (after three minds)

- Run [synthesis-engine](synthesis-engine.md) (e.g. `research/prototypes/mind-synthesis.py`).
- Output block: **Convergence** | **Productive Tensions** | **Campaign Synthesis**.
- Do **not** run synthesis at ingest (step 1.5); only here after the three minds.

### 5.6 Deliberation receipt (optional)

- For runs that need an auditable WORK trail, complete [modules/verifiable-personal-ai/deliberation-receipt-template.md](modules/verifiable-personal-ai/deliberation-receipt-template.md) and store next to the draft or link from the gate candidate.
- “Verifiable” = documented process and sign-off, not cryptographic proof. See [modules/verifiable-personal-ai/manifest.md](modules/verifiable-personal-ai/manifest.md).

**Council output:** Consolidated markdown draft + citations → staged for approval. All usage gated via recursion-gate + companion approval.
