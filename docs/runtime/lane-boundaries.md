# Lane-scoped memory boundaries

Runtime recall should default to **the active work lane** so session material does not silently contaminate unrelated territories.

## Defaults

- Strategy notebooks and `work-strategy` observations stay in that lane unless you explicitly widen search (`lane_search` without `--lane` searches globally over the ledger — use `--lane` for scoped queries).
- `runtime/memory_policy.json` states the default policy for higher-level tools.

## Record boundary

No `obs_id` or runtime ledger line may be treated as SELF / SKILLS / EVIDENCE fact without **RECURSION-GATE** approval and merge.

See [memory-retrieval.md](memory-retrieval.md) and [governance-unbundling.md](../governance-unbundling.md).
