# THINK — update ritual and receipts

**Purpose:** Keep THINK **fast** (direct edit still allowed per [we-read-think-self-pipeline.md](../we-read-think-self-pipeline.md)) while leaving a **light audit trail**.

## When to run

After **we read / we studied**, or after editing [think-claims.json](../../artifacts/skill-think/think-claims.json).

## Steps

1. Update **READ** in EVIDENCE if not already logged.
2. Update **`skill-think.md`** prose.
3. Update **`think-claims.json`** if using structured claims.
4. Optional: append a receipt via [record_think_update.py](../../scripts/record_think_update.py).

## Receipts

Append-only JSON lines under `artifacts/skill-think/update-receipts/` — see script help. **Not** Record truth.

## Weekly THINK test loop

1. Select 1-2 existing THINK claims.
2. Run 1 small test (see [think-exercises.md](think-exercises.md)).
3. Record the result in `think-claims.json` (`test_type`, `test_result`, `scaffolding_level`).
4. Update prose only if the test changed the real judgment.
5. Optionally append a receipt.
