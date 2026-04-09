# Operator session review — verification checklist

**Purpose:** Manual and CI-backed checks for recurring session friction (UX, procedure, tooling). Automated guards live in `tests/test_operator_session_review_contracts.py`, `tests/test_auto_dream_memory_telemetry.py`, and `tests/test_operator_clock.py`.

**Not** Record truth. WORK-only operator doc.

---

## How to use

- **CI / pre-push:** `python3 -m pytest tests/test_operator_session_review_contracts.py tests/test_auto_dream_memory_telemetry.py tests/test_operator_clock.py`
- **Calibration (quarterly or after ritual changes):** Run the **Manual** rows once and note pass/fail in your own log.

---

| Issue | How to verify | Pass signal |
|-------|----------------|-------------|
| **Time / date inconsistency** | Paste `python3 scripts/operator_clock.py` (or `--date-only`) at thread open; align “today” in prose with that line and [docs/date-time-conventions.md](../../date-time-conventions.md). | One explicit UTC line per thread when dating matters. |
| **Bare compass vs full coffee** | Read [menu-reference.md § Bare compass](menu-reference.md#bare-compass-vs-coffee-then-c) + contract test. Optionally drill: `compass` only vs `coffee` then `C`. | Doc + test green; drill matches expected Step 1 behavior. |
| **Duplicate / recycled context** | Not automatable. Use “this message supersedes …” or a fresh thread on long arcs. | Operator judgment; no wrong-turn replies. |
| **Dream dry-run telemetry** | [docs/memory-self-audit.md](../../memory-self-audit.md) § Telemetry note + `pytest tests/test_auto_dream_memory_telemetry.py`. | `blank_lines_collapsed > 0` with `changed: False` understood as OK on fixture. |
| **Lane clarity (EXECUTE / DOCSYNC)** | Contract test on [operator-agent-lanes.md](../../operator-agent-lanes.md); you use **`EXECUTE`** / **`DOCSYNC`** when you want unambiguous ship. | Tests green; commits match your lane intent. |
| **Plan mode handoff** | Manual: Plan → approve → **`EXECUTE`** in a follow-up (or same message if product allows). | No surprise edits while still in Plan-only intent. |
| **RECURSION-GATE / Record** | Contract test: `users/grace-mar/recursion-gate.md` parseable; `git log` shows no gated files without merge discipline. | No ad-hoc SELF/EVIDENCE/prompt edits without gate + script. |
| **Harness vs coffee** | [harness-warmup.mdc](../../../.cursor/rules/harness-warmup.mdc) “skip when warmup pasted” + `operator_coffee.py` runs `harness_warmup.py` in work-start modes. | Contract tests green; cold thread either pastes harness or runs `coffee`. |
| **Skill capture optional close** | Grep or skim `skills-portable/skill-candidates.md` after you said yes. | Row exists when you opted in. |
| **Compass exit rule** | Coffee SKILL + menu-reference: **C** exits unless **`stay in coffee`**. | Contract test on SKILL.md strings. |
| **Todos / UI duplication** | Cursor product; watch for duplicate todo rows. | N/A in repo tests. |

---

## Related

- [menu-reference.md](menu-reference.md) — full **A–G** protocol.
- [work-coffee-history.md](work-coffee-history.md) — lane breadcrumbs.
