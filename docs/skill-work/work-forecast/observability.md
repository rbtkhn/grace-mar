# Forecast Observability

Forecasting in Grace-Mar should be legible before it becomes powerful.

This lane tracks:

- how many forecast runs occurred
- which methods were selected
- which series were forecast
- how many artifacts included quantiles
- how many artifacts included benchmarks
- whether receipts were written successfully

These observability surfaces are WORK-layer support objects.
They exist for audit, review, and operator trust.

They do not update Record surfaces directly.

## Suggested metrics

### Receipt metrics

- total forecast receipts
- receipts by status
- receipts by method
- receipts by series

### Artifact metrics

- total forecast artifacts
- artifacts with quantiles
- artifacts with covariates
- artifacts with benchmarks
- artifacts by selected method

## Suggested command

```bash
python3 scripts/build_forecast_observability_report.py
```

## Interpretation rule

Observability tells us whether the lane is being used and how.
It does not tell us that any forecast is true.
Truth claims remain downstream and separately reviewable.
