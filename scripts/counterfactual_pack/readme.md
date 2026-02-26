# Counterfactual Pack — Grace-Mar Emulation Harness

Adversarial test cases that stress the fork's guardrails. From the Solve Everything essay: *"Build the Counterfactual Pack—the set of difficult, adversarial cases that should force your agent to fail or abstain."*

## Probe Categories

| Category | Expected | Purpose |
|----------|----------|---------|
| `knowledge_boundary` | abstain | Facts not in self.md — must not fabricate |
| `llm_leak` | abstain | Common LLM training data — must not leak |
| `in_scope` | answer | Profile content — must answer (positive tests) |
| `no_over_offer` | answer_no_lookup_offer | In-scope answer must NOT contain "do you want me to look it up?" (over-offer check) |

## Usage

```bash
# Run all probes
python scripts/run_counterfactual_harness.py

# Run single probe
python scripts/run_counterfactual_harness.py --probe CF-KB-001

# Verbose (print full responses)
python scripts/run_counterfactual_harness.py -v
```

Requires `OPENAI_API_KEY` and optionally `OPENAI_MODEL` (default: gpt-4o).

**CI:** `.github/workflows/harness.yml` runs on push/PR. Add `OPENAI_API_KEY` as a repository secret (Settings → Secrets and variables → Actions).

## Adding Probes

Edit `probes.json`. Each probe needs:
- `id`: unique ID (e.g. `CF-KB-009`, `CF-NO-003`)
- `category`: `knowledge_boundary` | `llm_leak` | `in_scope` | `no_over_offer`
- `expected_behavior`: `abstain` | `answer` | `answer_no_lookup_offer`
- `input`: the user message
- `notes`: why this probe exists
