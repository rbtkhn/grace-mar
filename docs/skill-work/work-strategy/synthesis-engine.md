# Mind Synthesis Engine (Auto + Human-gated)

**Status:** WORK only. Read-only on Record. Output is draft; final synthesis by the operator and gated for any merge.

## When it runs

After the three analytical lenses ([work-politics/analytical-lenses](../work-politics/analytical-lenses/manifest.md)) have been run on the same neutral fact summary. Do **not** run synthesis at ingest (e.g. step 1.5); run only in the triangulation stage (step 5 / 5.5).

## Algorithm (run after three minds)

1. **Convergence score (0–1)** — % of shared conclusions across the three lens outputs.
2. **Tension flags** — List contradictions with brief explanation (do not flatten).
3. **Campaign Synthesis template** — Draft block that always ends with “Individuals can stay curious by…” (or equivalent invitational close).
4. **Required output block** for every explainer-article / social-thread: **Convergence** | **Productive Tensions** | **Campaign Synthesis**.

## Rules

- Read-only on Record; synthesis output is draft only.
- Log to WORK docs (briefs, session notes, module output); optional ACT- only when the companion approves a candidate that creates an audit line. Do **not** append full deliberation traces to `self-evidence.md`.
- Final synthesis and any ship decision: operator + human sign-off; gated via RECURSION-GATE for any Record or public use.

## Prototype

See [research/prototypes/mind-synthesis.py](../../../research/prototypes/mind-synthesis.py). In production, may call LLM wrapper; output remains draft until operator approves.
