# Multi-agent fork generator (experimental)

**Status:** Design note — optional pattern for richer **WORK** menus without bypassing human judgment or **RECURSION-GATE**.

**Problem:** One assistant turn can enumerate several branches (labels + one-line stubs); some operators want **more creative** fork diversity while staying **rule-compliant**. Enumeration is not execution — substantive work runs only after the human picks.

**Pattern (two-pass or subagent):**

1. **Explorer pass** — Generate 6–8 candidate forks (creative, cross-lane, including unconventional pivots). No file edits; prose only.
2. **Gatekeeper pass** — Filter against **AGENTS.md** / **operator-style** / lane boundaries: no gated Record writes, no faux “done”, no fake precision metrics, Lexile/Voice constraints if the fork touches companion surfaces.
3. **Human** — Picks **one** letter (or **A+C**). Single commit to execution.

**Token budget:** Treat the two passes as **~2×** a normal menu turn; cap explorer output (e.g. one line per fork) before gatekeeper trims to **3–5** options.

**Toggle:** Prefer **operator explicit request** (“two-pass menu”) or a **WORK** doc pointer in-thread — avoid silent multi-agent on every turn.

**Not a fourth triad seat:** Both passes are **WORK execution layer** instrumentation; they do not replace **Mind**, **Record**, or **Voice**.

**See also:** [work-menu-conventions.md](../work-menu-conventions.md), [synthesis-engine.md](synthesis-engine.md).
