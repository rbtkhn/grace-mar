# Swarm lane

This lane is the operator-facing swarm bridge for auto-research.

It does not create a second staging path. In this first slice, it reuses
accepted artifacts from `auto-research/self-proposals/accepted/` and promotes
them into the live gate only through the shared artifact-promotion helper.

## Contract

- keep experiments and read models under `auto-research/swarm/`
- do not append ad hoc content to `users/<id>/recursion-gate.md`
- do not emit custom gate-only events in place of `staged`
- keep promotion explicit and operator-mediated
- keep swarm state off the child Voice surface

## State

`swarm-state.json` is a read model written by `orchestrator.py`. It is safe to
regenerate. It summarizes:

- last refresh timestamp
- runner status
- recent accepted artifacts
- recent promotions
- pending artifact count

## Commands

Refresh and print status:

```bash
python3 auto-research/swarm/orchestrator.py status
```

Show the latest swarm-visible artifact:

```bash
python3 auto-research/swarm/orchestrator.py last
```

Promote an artifact with operator review note:

```bash
python3 auto-research/swarm/orchestrator.py promote latest --review-note "Operator reviewed grounding and wants gate visibility."
```

## First-slice scope

This slice intentionally excludes daemon lifecycle management. No `start` or
`stop` command is provided here or in Telegram. Background supervision belongs
outside the bot process.
