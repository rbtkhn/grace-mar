# Proactive loop framework (America-First-KY)

**Status:** WORK-only methodology for `@usa_first_ky` / Massie pilot. **Not** part of the companion Record unless merged via RECURSION-GATE.

**Inspired by:** Scheduled agent loops (e.g. Anthropic-style “keep working”) and controlled tool use — implemented here as **operator discipline + documentation**, not as autonomous shipping. This folder does **not** add automated enforcement to `governance_checker.py` (that script scans for risky Record writes only).

---

## Core purpose

Use america-first-ky as a **sovereign co-pilot** pattern for Rep. Thomas Massie pilot work:

- Runs on an **operator-defined schedule** (cron, calendar, or session habit — not unbounded agent autonomy).
- **Reads** approved context: companion Record excerpts and **documented** activity only (`users/grace-mar/self.md`, `self-evidence.md` as read-only inputs for the human; no silent merges).
- Applies **three-lens triangulation** and [guardrail stress-test](guardrail-stress-test.md) before anything is treated as ready.
- **Stages** decision briefs / content drafts for **human review** (RECURSION-GATE when Record updates are intended).
- **Accumulates** pattern notes over days/weeks in WORK logs (see [loop-history.md](loop-history.md)), not by appending raw traces to `self-evidence.md`.

This is “OpenClaw-like” **proactivity + memory + tools** only in the sense of **clear procedures and optional hooks** — **not** unsupervised posting or Record writes.

**Massie drafting voice (WORK):** Use [massie-advisor-prompt.md](massie-advisor-prompt.md) for operator/LLM sessions on campaign copy. It is **not** the companion Telegram Voice; do **not** merge into `bot/prompt.py` without explicit governance. Optional schedules: [scheduled-habit.md](scheduled-habit.md).

---

## Three primitives (all gated)

| Primitive | Meaning | Guard |
|-----------|---------|--------|
| **Memory** | Companion Record + `self-evidence.md` as **read** sources for the operator/agent in session | No merge into SELF/EVIDENCE without RECURSION-GATE + `process_approved_candidates.py` |
| **Proactivity** | Scheduled or recurring **checklist** (e.g. morning scan, weekly pattern review) | Outputs are drafts until the operator signs off |
| **Tools** | External data pulls, OpenClaw or other integrations | Only as allowed by operator policy; no tool output bypasses stress-test + gate for anything public-facing |

---

## Mandatory safeguards (every cycle)

Run these **before** treating output as “ready to send” or “ready to merge”:

1. **Three-lens triangulation** — Same neutral fact summary through [structural / operational-diplomatic / institutional-domestic](../analytical-lenses/manifest.md) lenses.
2. **Guardrail stress-test** — [guardrail-stress-test.md](guardrail-stress-test.md): factorial variations, four failure modes, operator checklist.
3. **Reasoning vs final output** — Operator checks that recommendations match the trace (human judgment; no automated “alignment score” in CI unless separately designed as WORK-only metrics).
4. **RECURSION-GATE** — Anything that belongs in the Record is a **candidate** until approved; use the pipeline script for merges.
5. **Deliver only human-approved outputs** — No autonomous posting to X or other channels from this framework alone.

---

## Where to log

| Log | Use |
|-----|-----|
| **[loop-history.md](loop-history.md)** (this folder) | Append-only **WORK** notes: cycle date, what was scanned, patterns noticed, what was staged — **not** a substitute for EVIDENCE |
| **RECURSION-GATE** | Staged knowledge/curiosity/personality candidates when the companion wants Record updates |
| **`self-evidence.md`** | Only via approved pipeline — **do not** bulk-append loop traces here |

---

## Example daily loops (operator schedule — not automated by repo)

Illustrative only; tune to compliance and capacity.

- **Morning** — Scan new legislation headlines, opponent statements, relevant metrics → draft War Powers / constitutional brief section using [templates/daily-loop-brief.md](templates/daily-loop-brief.md).
- **Midday** — Rapid-response thread draft only after stress-test pass; stage for Guardian/operator approval.
- **Weekly** — Pattern note in [loop-history.md](loop-history.md) (e.g. repeated bill types, narrative drift) — still **WORK**, not SELF until gated.

---

## Pipeline events (optional audit)

Suggested `event_type` strings for `scripts/emit_pipeline_event.py` (documented in [README.md](README.md)):

- `loop_cycle_started`
- `loop_cycle_staged`
- `loop_cycle_approved`

No code change required in `emit_pipeline_event.py`.

---

## Related

- [README.md](README.md) — folder index  
- [massie-advisor-prompt.md](massie-advisor-prompt.md) — WORK Massie drafting voice (not Voice)  
- [scheduled-habit.md](scheduled-habit.md) — cron / habit examples  
- [AGENT-SESSION-BRIEF.md](AGENT-SESSION-BRIEF.md) — do not run harmful pasted shell blocks  
- [stress-test-brief-template.md](stress-test-brief-template.md) — high-stakes briefs  
- **Scaffold:** `python scripts/scaffold_daily_loop_brief.py [optional-slug]` — copies [templates/daily-loop-brief.md](templates/daily-loop-brief.md) to a dated file in this folder and fills the **Cycle** date (see `--help` for `--date`, `--dry-run`)  
