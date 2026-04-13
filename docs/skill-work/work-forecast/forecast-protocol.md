# Forecast Protocol

## Purpose

This protocol defines how forecasting work is performed inside Grace-Mar without contaminating Record surfaces.

Forecasting is allowed as a WORK-layer activity.
Forecasting is not allowed to silently redefine identity, memory, or canonical truth.

## Boundary law

Forecast artifacts are provisional decision-support objects.

They may:

- support timing judgments
- support active watches
- support threshold monitoring
- support strategy discussion
- support planning under uncertainty

They may not:

- write directly to SELF
- write directly to SELF-LIBRARY
- write directly to SKILLS
- write directly to EVIDENCE
- convert forecasts into facts without review
- bypass proposal and approval workflow

## Required fields for any forecast artifact

Every forecast artifact must include:

- series name
- time unit
- history window
- forecast horizon
- method
- point forecast
- assumptions
- invalidators

Strongly recommended:

- quantile forecast or uncertainty range
- covariates
- benchmark results
- operator note
- receipt id
- source artifact links

## Method hierarchy

Preferred order:

1. naive baselines
2. simple trend or average methods
3. seasonal baselines when appropriate
4. optional advanced model adapters

Rule: Do not use a more complex model unless the forecast can still be explained in plain language.

## Benchmark rule

A forecast should be compared against at least one simple baseline whenever possible.

Acceptable baseline examples:

- last value
- moving average
- linear trend
- seasonal naive

If no benchmark is run, the artifact must say so explicitly.

## Assumptions rule

Each forecast must state the assumptions that make it intelligible.

Examples:

- recent cadence remains informative
- no major regime change is expected during the forecast horizon
- the observation process remains comparable across the history window

## Invalidators rule

Each forecast must state what would make it unreliable.

Examples:

- schedule shock
- policy shock
- new workflow introduced
- missing or broken data pipeline
- major external event

## Interpretation rule

Interpretation belongs downstream from the forecast artifact.

Correct:

- “This forecast suggests a possible slowdown in weekly note production.”
- “This artifact supports opening an active watch on cadence drift.”

Incorrect:

- “The user is becoming less disciplined.”
- “This is now true in the Record.”

## Promotion rule

If a forecast informs a durable conclusion, that durable conclusion must be:

1. stated separately
2. staged separately
3. reviewed separately
4. approved separately

The forecast artifact itself remains a WORK object.

## Operator style

Use forecasting to support judgment, not replace judgment.

Preferred tone:

- conditional
- concrete
- benchmark-aware
- uncertainty-aware
- brief unless depth is requested
