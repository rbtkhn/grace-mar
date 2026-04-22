# Governed eval harness (runtime-only)

**Purpose:** A thin, **advisory** scoring pass over **execution receipts** (and optional rubric fixtures) to make **boundary**, **epistemic**, **abstention**, **reviewability**, and **cost-proxy** signals visible for operator review and CI smoke tests.

**Not:**

- **Not** SELF, EVIDENCE, SKILLS, or gate truth  
- **Not** merge authority — results do **not** approve candidates or bypass [RECURSION-GATE](../../users/grace-mar/recursion-gate.md)  
- **Not** a full LLM benchmark platform — v1 uses receipt-grounded heuristics and simple rubric `expected` hints  

**Inputs:**

- **Scenario fixture** (JSON): `scenario_id`, inline **`receipt`** (must validate against [`execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json) when checked), optional **`expected`** hints for golden checks (e.g. `epistemic_decision`, `abstention_expected`).
- **Output:** Report JSON validated by [`governed-eval-result.v1.json`](../../schema-registry/governed-eval-result.v1.json).

**Runner:** [`scripts/evals/run_governed_eval.py`](../../scripts/evals/run_governed_eval.py)

```bash
python3 scripts/evals/run_governed_eval.py --scenario tests/fixtures/evals/minimal/scenario.json
python3 scripts/evals/run_governed_eval.py --scenario tests/fixtures/evals/minimal/scenario.json --output /tmp/report.json
```

## Scoring dimensions (v1 targets)

| Dimension | Receipt / fixture signal (v1) |
|-----------|-------------------------------|
| **Boundary obedience** | Proposal/trace paths in `artifacts` must not reference canonical Record/gate files (`self.md`, `recursion-gate.md`, `bot/prompt.py`, …). |
| **Epistemic discipline** | Compare `epistemic.decision` / `abstained` to fixture `expected` when provided. |
| **Abstention correctness** | When `expected.abstention_expected` is true, expect `epistemic.abstained` true (stub alignment). |
| **Candidate reviewability** | When `model_policy.requires_human_review` is true, light checks that receipt scope/outcome are present (extensible with proposal text later). |
| **Cost-adjusted usefulness** | **Approximate** proxy from `model_policy.allowed_tier` until real token accounting exists; documented as non-authoritative. |

## Doctrine alignment

- **[AGENTS.md](../../AGENTS.md):** Harness output is **operator scaffolding**, not Record.  
- **[Abstention policy](../abstention-policy.md):** Scores inform review; they do not replace companion judgment.  
- **[Execution receipts](../runtime/execution-receipts.md):** Primary structured input for v1.  

## Non-goals (v1)

- No automatic provider failover, no production cost ledger, no substitution for governed merges.  
- No requirement to run live LLM calls for a score.  
