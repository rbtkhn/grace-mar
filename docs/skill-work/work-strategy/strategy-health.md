# work-strategy — health interpretation

**Companion doc** to [observability.md](observability.md) and `artifacts/work-strategy/strategy-observability.json`.

## Green / yellow / red (heuristic)

| Signal | Healthy | Investigate |
|--------|---------|-------------|
| Open decision points | Few, intentional | Many stale `open` without notebook movement |
| Authorized sources YAML | Growing toward parity with [work-strategy-sources.md](work-strategy-sources.md) | Stalled count vs markdown “Total: N sources” |
| Promotion policy | Present | Missing file |

## Actions

- Run [build_strategy_observability.py](../../../scripts/build_strategy_observability.py) after ladder or sources changes.
- Use [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md) for full work-plane sequencing.
