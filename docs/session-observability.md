# Session Observability

**Companion-Self template -- Native metrics for session awareness**

---

## Purpose

A unified script that computes companion-self-native metrics in one pass. Answers: "What happened this session?" with quantities relevant to identity formation, governance health, and operational surface activity — not generic telemetry.

## Metrics

| Metric | Source | Computation |
|--------|--------|-------------|
| Seeds created this session | `seed-registry.jsonl` last_seen within window | Count new seed_ids |
| Seeds updated | Same file | Count observation_count increments |
| Promotions staged | Same file | Claims that changed to `candidate` |
| Contradictions introduced | Same file | New contradiction_refs |
| Claims approaching promotion | `evaluate_seed_promotion.py` | Verdict = `approaching` |
| Gate candidates pending | `recursion-gate.md` | Count `status: pending` blocks |
| Authority level active | `config/authority-map.json` | Report current surface policy summary |
| Surfaces touched | git diff --name-only | Classify: durable vs exploratory vs other |

## CLI

```bash
python3 scripts/session_observability.py -u grace-mar
python3 scripts/session_observability.py -u grace-mar --since "2h"
python3 scripts/session_observability.py -u grace-mar --since "1d"
python3 scripts/session_observability.py -u grace-mar --json
python3 scripts/session_observability.py -u grace-mar --oneline
```

## Output modes

- **Full** (default): Multi-line dashboard with all metrics
- **One-line** (`--oneline`): Compact summary for embedding in coffee/bridge output
- **JSON** (`--json`): Machine-readable for downstream tooling

## Integration points

- **coffee Step 1:** The `--oneline` flag produces a one-line status suitable for the grounding stack
- **bridge Step 1:** The full output or `--oneline` provides a "session stats" block for the transfer prompt
- **dream:** Can reference the `--since "8h"` window for end-of-day summary

## Surface classification

Files are classified as:
- **Durable:** `self.md`, `self-archive.md`, `self-skills.md`, `recursion-gate.md`, `bot/prompt.py`
- **Exploratory:** `self-memory.md`, `session-log.md`, `session-transcript.md`, `docs/skill-work/`, `.cursor/`
- **Other:** Everything else

## Cross-references

- [layer-architecture.md](layer-architecture.md) — Where this fits in the four-layer model
- [seed-registry.md](seed-registry.md) — Seed claim lifecycle
- [seed-promotion-thresholds.md](seed-promotion-thresholds.md) — Promotion evaluation
- [authority-map.md](authority-map.md) — Surface authority classes
