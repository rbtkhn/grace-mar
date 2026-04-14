# Policy modes

JSON here defines **named policy envelopes** for operator and automation: how strongly to abstain, what staging is allowed, and retrieval posture — **not** Record truth. See [docs/policy-modes.md](../../docs/policy-modes.md).

| File | Consumers |
|------|-----------|
| `defaults.json` | `scripts/runtime/policy_mode_config.py`; CLIs that accept `--policy-mode` or `GRACE_MAR_POLICY_MODE` (`build_budgeted_context.py`, `review_orchestrator.py`, `checkpoint_session.py`, `build_handoff_packet.py`, `stage_candidate_from_observations.py`, `precheck_gate_staging.py`) |

**Companion / gate authority unchanged:** modes inform scripts; merges remain via `recursion-gate.md` and companion approval only.
