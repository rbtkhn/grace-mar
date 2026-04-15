# Current-Events Analysis (WORK-STRATEGY)

**Status:** WORK only
**Scope:** Staged prototype or bot/session workflow
**Outputs:** WORK docs, notebook entries, watch support, decision-point support, optional recursion-gate staging
**No direct Record writes**
Last updated: 2026-04-14

## 1. Purpose

This file defines the standard workflow for turning a live event, transcript, brief item, or operator question into a disciplined work-strategy analysis.

Its purpose is not merely to summarize events. Its purpose is to convert current events into reusable strategic judgment while preventing three common failures:

- rhetoric masquerading as fact
- loose historical analogy
- synthesis before the analytical seams are visible

This workflow should remain compatible with the broader work-strategy lane, where the strategy notebook is the primary daily judgment artifact and where all outputs remain WORK-only unless separately reviewed.
See:
- [README.md](README.md)
- [civilizational-strategy-surface.md](civilizational-strategy-surface.md)
- [case-index.md](case-index.md)
- [promotion-ladder.md](promotion-ladder.md)

## 2. Core rule

Every run must preserve the seam between:

- observed facts
- interpretive framing
- historical or civilizational comparison
- recommendation or synthesis

Do not blur these layers.

## 3. Inputs

Valid inputs include:

- breaking news item
- operator question
- RSS-derived daily-brief item
- transcript or long-form digest
- strategic note requiring a refresh
- energy or chokepoint event
- event cluster requiring tri-frame review

Long-form transcript ingest is allowed, including Predictive History and work-strategy transcript digests, but the first output must still be a neutral fact summary rather than lecturer rhetoric restated as fact. See `common-inputs.md`.

## 4. Output classes

A run may produce one or more of the following:

- neutral fact summary
- analysis block
- resonance note
- analogy audit
- watch support note
- strategy-notebook entry
- decision-point support
- synthesis block
- optional deliberation receipt
- optional gate candidate

Not every run should produce all outputs.

## 5. Standard pipeline

### 5.1 Perceiver — neutral fact summary

First produce a neutral fact summary.

Required fields:
- who
- what
- when
- where
- why stated by actors
- how
- source type
- dated URLs or references where practical

Rules:
- keep this section neutral
- separate verified facts from actor claims
- do not smuggle tri-frame conclusions into this stage
- when transcript-based, treat lecturer framing as interpretation unless independently supported

**Output target:** ≤200 words unless the event is unusually complex.

### 5.2 Verify seam

Before analysis begins, mark any claims that are:

- direct observation
- actor claim
- inference
- unresolved contradiction

Optional:
- add verify tier if the run needs a stronger audit trail
- add plane tags when the event is likely to bleed structural, operational, and institutional claims together

### 5.3 Event classification

Classify the event before deeper interpretation.

Required categories:
- domain: political | military | energy | financial | civilizational | institutional | mixed
- tempo: breaking | developing | consolidating | retrospective
- relevance: low | medium | high
- immediate need: summary | watch support | decision support | doctrine candidate

This stage exists to prevent over-processing minor events and under-processing major ones.

### 5.4 Case-index check

Before proposing a historical or CIV-MEM parallel, check the local `case-index.md` first.

If a suitable case exists:
- cite the case ID or label
- extract the mechanism
- record fit / mismatch / falsifier notes

If no suitable case exists:
- do **not** force a named analogy
- create a resonance note or proceed without a historical layer

Rule:
Current-events analysis should prefer an existing local case object over ad hoc historical recall whenever possible.

### 5.5 Energy-chokepoint hook (mandatory for energy-related events)

For any energy-related event:
- run `modules/energy-chokepoint/perceiver-hook.py`
- append chokepoint status to the neutral fact summary
- check `case-index.md` for energy and chokepoint cases before naming a parallel
- if a parallel is proposed, run analogy audit before it enters final synthesis

Typical candidate cases may include:
- embargo / denial logic
- resource leverage without full control
- corridor vulnerability
- coalition response to resource seizure

Rule:
No energy event should jump directly from price movement to grand strategic conclusion without passing through chokepoint status, dependency structure, and analogy discipline.

### 5.6 Analyst — structured breakdown

After the neutral summary and case-index check, run the analysis block.

Minimum required lenses:
- historical / civilizational parallel
- systems impact
- one additional lens appropriate to territory
- one explicit uncertainty block

Recommended lenses:
- structural
- operational
- institutional
- legitimacy
- timing / sequencing
- narrative authority

For the historical / civilizational lens, prefer:
- case family or case ID
- named mechanism
- scope conditions
- mismatch conditions

Avoid:
- essay-like historical detours
- decorative analogy
- treating analogy as proof

### 5.7 Resonance note rule

Create a resonance note instead of a stronger historical claim when:
- the fit feels real but remains partial
- no strong case-index entry exists
- the event rhymes with a civilizational pattern but not tightly enough to justify a named parallel

Minimum resonance note fields:
- event or signal
- candidate mechanism
- strongest fit
- strongest mismatch
- provisional falsifier
- review trigger

If the same pattern recurs, consider promotion under `promotion-ladder.md`.

### 5.8 Analogy audit (mandatory when any historical parallel is proposed)

Use `analogy-audit-template.md`.

For every historical analogy or CIV-MEM parallel, record:
- the analogy explicitly
- strongest structural fit
- strongest mismatch
- falsifier
- usefulness judgment
- risk of overextension
- recommended usage: illustrative | framing only | core model

**Rule:** No analogy should pass into final synthesis unmarked.

If the analogy is weak, misleading, or merely decorative, say so explicitly and downgrade it.

### 5.9 Watch-support decision

Ask whether this event materially sharpens an existing watch.

If yes, record:
- linked watch
- what changed in interpretation
- linked case or mechanism, if any
- disconfirming condition
- review cadence

If no, do not force a watch update.

A historical layer should only support a watch if it changes monitoring, prioritization, or signal interpretation in a real way.

### 5.10 Decision-point trigger

Open or support a decision point when:
- timing matters
- sequencing matters
- option ranking changes because of the analysis
- a historical or civilizational pattern materially affects risk framing

If a decision point is opened:
- link the case or mechanism used
- state why it matters for this decision
- state mismatch and falsifier
- state why not the next-best option

If the event does not affect choice, do not inflate it into a decision point.

### 5.11 Three minds / specialized lenses (mandatory)

Run the three analytical lenses on the same neutral fact summary and the same clarified historical framing.

Rule:
The three minds should respond to the same audited framing, not to three different versions of an unexamined analogy.

Carry forward:
- neutral fact summary
- case or mechanism used
- analogy audit judgment
- key uncertainty
- plane tags where useful

Goal:
surface convergence, productive tension, and differing emphasis without allowing one mind to smuggle in unaudited historical claims.

### 5.12 Synthesis

Only synthesize after:
- neutral summary
- classification
- case-index check
- any required resonance note or analogy audit
- three minds

Use the synthesis engine only after those seams are visible.

Output block:
- **Convergence**
- **Productive Tensions**
- **Campaign Synthesis** or **Strategic Synthesis**

Synthesis should state:
- what seems most solid
- what remains uncertain
- whether the historical layer is illustrative, framing-only, or core-model grade

### 5.13 Deliberation receipt (optional)

For runs that need a stronger WORK audit trail:
- complete the deliberation receipt template
- store it next to the draft or link it from the gate candidate

"Verifiable" here means documented process and sign-off, not cryptographic proof.

## 6. Required reasoning seam for any historical layer

Whenever a historical or civilizational pattern is used, include these mini-fields where practical:

- Case family or case ID:
- Mechanism:
- Why this fits:
- Why this may not fit:
- Falsifier:
- Confidence: low | medium | high
- Use type: illustrative | framing-only | core model

If those fields cannot be filled honestly, downgrade to resonance note or remove the historical layer.

## 7. Promotion logic

Use [promotion-ladder.md](promotion-ladder.md).

Typical paths:
- Event → case hit → resonance note
- Event → case hit → analogy audit
- Event → case hit → analogy audit → watch support
- Event → case hit → analogy audit → decision point
- Repeated event pattern → repeated audits → doctrine note candidate

Promotion is justified only when the next artifact becomes more reusable, more testable, or more decision-relevant.

## 8. Relation to other work-strategy artifacts

### [civilizational-strategy-surface.md](civilizational-strategy-surface.md)
Defines the thin bridge between current events and reusable civilizational strategy mechanisms.

### [case-index.md](case-index.md)
First stop for reusable historical and civilizational cases.

### [promotion-ladder.md](promotion-ladder.md)
Defines how a case hit becomes resonance, audit, watch support, decision support, or doctrine.

### [strategy-notebook/](strategy-notebook/README.md)
Primary daily judgment surface where many outputs should ultimately land.

### [history-notebook/](history-notebook/README.md)
Preferred destination for richer local historical treatment when a thin case abstraction is no longer enough.

### [decision-point-template.md](decision-point-template.md)
Use when the analysis materially affects options, sequencing, or recommendation.

## 9. Minimal operator checklist

Before closing a run, ask:

1. Did I separate fact from interpretation?
2. Did I classify the event before synthesizing it?
3. Did I check the case index before naming a historical parallel?
4. If I used a parallel, did I record mismatch and falsifier?
5. Did the historical layer improve judgment, or only decorate it?
6. Did the three minds inherit the same clarified framing?
7. Is the output best treated as summary, watch support, decision support, or only a resonance note?

## 10. Failure modes

Common failure modes:

- treating transcript rhetoric as neutral fact
- using history as ornament
- skipping the case-index check
- promoting a weak analogy into synthesis
- letting one mind smuggle in a stronger parallel than the audit allows
- confusing narrative excitement with decision relevance
- opening a decision point when no real choice is affected

If any of these occur, downgrade and rerun the smallest necessary stage.

## 11. Minimal maintenance standard

This workflow is healthy when:

- the neutral summary is actually neutral
- historical comparison is disciplined
- synthesis comes last
- current events are converted into reusable strategy objects
- weak parallels are marked as weak
- the workflow improves judgment rather than producing prettier prose

This workflow is unhealthy when:

- every event becomes a doctrine lesson
- every analogy is treated as profound
- the case index is ignored
- analysis cannot show its seams
- synthesis is doing the work that earlier stages should have done
