# Swarm debate review

This lane adds a bounded advisory debate pass for swarm-visible artifacts.

It is not a second authority surface. It does not stage candidates. It does
not merge anything. It writes derived review artifacts only.

## Contract

- keep debate advisory and rebuildable
- review accepted artifacts or sandbox-adjacent outputs only
- write outputs under `users/<id>/derived/debate/`
- do not append directly to `users/<id>/recursion-gate.md`
- do not create a new canonical memory surface
- prefer deterministic review functions over opaque prompt theater

## Review functions

- `coordinator`: synthesizes the pass and final recommendation
- `grounding`: checks grounding presence and placeholder risk
- `logic`: checks hard gates and projection completeness
- `critic`: applies stronger rejection pressure to weak artifacts

## Output

Each debate run emits one derived artifact with:

- target artifact reference
- target projection summary
- per-role findings
- blocking flags
- consensus level
- promotion readiness
- final recommendation

Allowed recommendations:

- `promote_candidate`
- `needs_operator_review`
- `request_more_grounding`
- `reject_artifact`

## Command

Run a debate review on the latest swarm-visible accepted artifact:

```bash
python3 auto-research/swarm/orchestrator.py debate latest
```

Run a debate review and print JSON:

```bash
python3 auto-research/swarm/orchestrator.py debate latest --json
```
