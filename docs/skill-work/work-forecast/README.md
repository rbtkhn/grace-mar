# work-forecast

**Purpose:** Governed forecasting work for numeric or count-based series that may inform active watches, decision points, and operator planning.

This lane is for:

- cadence analysis
- recurrence analysis
- throughput forecasting
- weak-signal frequency tracking
- bounded external monitoring series

This lane is not for:

- changing identity
- writing directly to SELF
- writing directly to SELF-LIBRARY
- treating forecasts as facts
- bypassing proposal and review workflow

**Core boundary:** Forecast artifacts are WORK-layer decision-support objects. They do not update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE directly. Any forecast-derived conclusion must be separately proposed and human-approved through the existing gated pipeline.

**Read next:** [forecast-protocol.md](forecast-protocol.md) · [GLOSSARY-FOR-BEGINNERS.md](GLOSSARY-FOR-BEGINNERS.md) · [observability.md](observability.md) · [strategy-integration.md](strategy-integration.md) · [forecast-reference-template.md](forecast-reference-template.md)

## Recommended outputs

- point forecast
- uncertainty range / quantiles
- assumptions
- invalidators
- benchmark comparison
- receipt link

## Typical use cases

- operator cadence counts
- journal or note frequency
- recurrence of watched topics over time
- work-lane throughput
- publication cadence of tracked sources
- policy-event counts by week or month

## Minimum standard

A forecast is not complete unless it includes:

1. the source series
2. the horizon
3. the method used
4. assumptions
5. invalidators
6. benchmark comparison or an explicit note that no benchmark was run

## Promotion rule

Forecast outputs may support planning and active watches, but they do not become Record truth unless a human separately stages and approves a downstream claim.

## Suggested workflow

1. Gather a simple time series.
2. Run one or more baseline methods.
3. Save a forecast artifact.
4. Attach a receipt.
5. Optionally use the artifact in work-strategy or an active watch.
6. Only stage downstream conclusions through the normal gate.

## Starter commands

Run baseline forecast generation:

```bash
python3 scripts/run_forecast_baselines.py \
  --input examples/diagnostics/sample-forecast-series.csv \
  --series-name operator_daily_messages \
  --time-col date \
  --value-col count \
  --horizon 7 \
  --out artifacts/forecast/operator_daily_messages.2026-04-12.v1.json
```

Run post-hoc evaluation:

```bash
python3 scripts/backtest_forecast_artifact.py \
  --artifact artifacts/forecast/operator_daily_messages.2026-04-12.v1.json \
  --actuals-csv examples/diagnostics/sample-forecast-series.csv \
  --time-col date \
  --value-col count
```

Build observability report:

```bash
python3 scripts/build_forecast_observability_report.py
```

Append a forecast watch log entry (optional):

```bash
python3 scripts/create_forecast_watch_log.py --help
```
