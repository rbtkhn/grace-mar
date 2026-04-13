# Lane-scoped memory boundaries

**Supplements** [memory-retrieval.md](memory-retrieval.md) (normative progressive disclosure, commands, and cross-lane flags). This file is **lane scope only**.

Runtime recall should default to **the active work lane** so session material does not silently contaminate unrelated territories.

## Defaults

- Strategy notebooks and `work-strategy` observations stay in that lane unless you explicitly widen search (`lane_search` without `--lane` searches globally over the ledger — use `--lane` for scoped queries).
- [`runtime/memory_policy.json`](../../runtime/memory_policy.json) states default scope for higher-level tools (e.g. `memory_brief.py --cross-lane` to widen).

## Record boundary

No `obs_id` or runtime ledger line may be treated as SELF / SKILLS / EVIDENCE fact without **RECURSION-GATE** approval and merge. Full rules: [memory-retrieval.md](memory-retrieval.md), [governance-unbundling.md](../governance-unbundling.md).
