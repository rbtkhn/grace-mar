# Strategy Integration

Forecast artifacts may support work-strategy without contaminating Record surfaces.

Allowed uses:

- active watch support
- threshold monitoring
- timing judgments
- cadence drift review
- decision-point framing

Disallowed uses:

- direct Record updates
- converting a forecast into a fact claim
- bypassing proposal and review workflow
- identity interpretation from narrow numeric patterns

## Good pattern

1. Run forecast.
2. Save artifact.
3. Write receipt.
4. Review observability.
5. Optionally reference the artifact in a strategy note or active watch.
6. Stage any downstream durable claim separately if needed.

## Example phrasing

Good:

- “This artifact suggests possible weakening in weekly output over the next 14 days.”
- “This supports opening an active watch on cadence drift.”

Bad:

- “The user is now less disciplined.”
- “This is true in the Record.”

## Rule

Forecasting supports judgment.
Forecasting does not replace judgment.
