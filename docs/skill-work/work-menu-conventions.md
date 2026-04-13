# WORK menu conventions (Cursor operator)

**Purpose:** When you are in **work-strategy**, **work-politics**, **work-jiang**, or **work-dev**, the assistant ends most substantive turns with **labeled forks** (multiple choice). This doc names the **shape** so menus stay **useful, grounded, and pivot-only** (no faux “done”).

**Rule source:** [`.cursor/rules/operator-style.mdc`](../../.cursor/rules/operator-style.mdc) (always-on).

---

## 1. Real forks only

Each option must be a **different next move** (different file, command, lane, or depth). Avoid filler (“continue”, “nothing else”) — work **switches**, it does not terminate in-menu.

---

## 2. Evidence-linked options (Fork explorer)

When a fork touches the **Record** or **gate**, include at least one **explicit anchor** per option where helpful:

- `` `users/grace-mar/recursion-gate.md` `` and **`CANDIDATE-XXXX`** when relevant
- Repo-relative paths: `` `docs/skill-work/...` ``, `` `scripts/....py` ``
- Links to GitHub are fine for **read-only** context; **canonical edits** stay in this repo

This turns selection into **grounded** handoff without bypassing **RECURSION-GATE**.

---

## 3. Cost and impact tags (heuristic)

Optional short tags on each line, **clearly heuristic** (not estimates of wall-clock certainty):

- **Time:** `~15m`, `~45m` — rough order of magnitude
- **Leverage:** `high-leverage`, `hygiene`, `deep` — qualitative
- **Do not** present uncalibrated **percentages** as oracle metrics (e.g. fake “gate merge probability %”) unless a **defined script** computes them

---

## 4. Combo and hybrid options

- The operator may answer **`A+C`** (or similar); the assistant executes both compatible branches.
- When two options combine naturally, you may add one line: **Combo:** `B + half of D` — *brief label explaining the merge* (still one human pick; do not develop the combo content until selected).
- **`F` — All (strategy-notebook hygiene bundle):** In one pass — (1) **verify hooks** / Primary-pull targets in `daily-strategy-inbox.md`, (2) **MINDS** cross-pointer to dated mind-file addenda (e.g. `CIV-MIND-MERCOURIS.md` **III.M**), (3) **Carry** lines that tie inbox ↔ mind. **Exclude** folding scratch into `chapters/YYYY-MM/days.md` unless **`dream`** or **explicit operator direction** — early fold risks duplicate **Judgment** before **Links** verify.
- **`strategy + verify`** — **Work-strategy** fork: same intent as **`strategy`** / **`strategy ingest`**, plus a **triage fact-check** ([`.cursor/skills/fact-check/SKILL.md`](../../.cursor/skills/fact-check/SKILL.md)) and/or **web pass** on **load-bearing** claims — especially **rosters**, **dates**, and **stats** from **transcripts**. Land outcomes in **`daily-strategy-inbox.md`** (**`verify:`**, **Primary pulls**) and, when folding, **`### Web verification`** / **`### Links`** in `days.md` — not **`### Judgment`** without sources. Spec: [`.cursor/skills/skill-strategy/SKILL.md`](../../.cursor/skills/skill-strategy/SKILL.md) (**Modes** → **+ verify**, **Transcript / analyst capture**); architecture: [STRATEGY-NOTEBOOK-ARCHITECTURE.md](work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *skill-strategy modes and verification passes*.

---

## 5. Optional confidence / LLM assist (off by default)

If the operator enables an **experimental** “confidence” or “explain first” mode:

- Any numeric score is **assistant uncertainty**, not ground truth.
- Prefer a **one-sentence** rationale over blocking the whole menu.

**Scripted morning ranking + optional LLM re-rank:** [`scripts/suggest_morning_forks.py`](../../scripts/suggest_morning_forks.py) (`--llm` requires `OPENAI_API_KEY`).

---

## 6. Auditing picks (Choice journal)

**Do not** auto-append operator menu picks to **`memory.md`** / **self-memory** from the Voice or analyst without governance change ([`docs/memory-template.md`](../../memory-template.md)).

**Do** log picks **explicitly** when the operator wants a trail:

```bash
python3 scripts/log_operator_choice.py -u grace-mar --context WORK --picked A --tags "~20m,gate" --note "optional"
```

Appends `### [WORK-choice]` blocks to **`users/<id>/session-transcript.md`** (operator continuity, not gated Record).

**`coffee` session trail:** Sessions started with **`coffee`** (work-start vs signing-off Step 1; optional light, minimal, survey; legacy **`hey`** still works) can leave traces in **`users/<id>/session-transcript.md`** (raw lines and **`[WORK-choice]`** via `log_operator_choice.py`) and/or dated bullets under **`docs/skill-work/work-*/*-history.md`** (per-lane milestones — [work-modules-history-principle.md](work-modules-history-principle.md)). Distinct from **`self-memory.md`** (companion continuity). See [canonical paths](../canonical-paths.md).

**Aggregate after ~30 days:**

```bash
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30 --print-gate-stub
```

The gate stub is **stdout only** — paste and edit **`CANDIDATE-XXXX`** before any merge.

**Strategy ingest session receipt (optional):** End-of-session tally for **X / transcript ingests** without duplicating full lines in `session-transcript.md` — the **SSOT** for paste-ready lines stays [strategy-notebook/daily-strategy-inbox.md](work-strategy/strategy-notebook/daily-strategy-inbox.md). Example:

```bash
python3 scripts/log_operator_choice.py -u grace-mar --context WORK --picked strategy-ingest \
  --tags "count=7" --note "see daily-strategy-inbox 2026-04-12"
```

`--note` is truncated at **500 characters** by the script — use a **pointer** (date / file), not a full paste dump. First-class `--context INGEST` is **not** required; `WORK` + `picked` + tags is enough for aggregation.

**Strategy fold ledger (optional):** After folding [strategy-notebook/daily-strategy-inbox.md](work-strategy/strategy-notebook/daily-strategy-inbox.md) into `chapters/YYYY-MM/days.md`, append one JSONL event (compression proxies, optional ratings) — not session-transcript, not MEMORY:

```bash
python3 scripts/log_strategy_fold.py -u grace-mar --notebook-date 2026-04-13 --fold-kind manual \
  --inbox-chars 12000 --days-delta-chars 4000 --note "tight merge; verify pins next"
python3 scripts/report_strategy_fold_learning.py -u grace-mar --days 30
```

Spec: [FOLD-LEARNING.md](work-strategy/strategy-notebook/FOLD-LEARNING.md).

---

## 7. Multi-agent fork generation (experimental)

See [work-strategy/multi-agent-fork-generator.md](work-strategy/multi-agent-fork-generator.md) — optional two-pass / subagent pattern; human still chooses one branch.

---

## 8. Dated filenames and CLI dates

Dated WORK outputs (daily brief, weekly scaffold, newsletter digest, optional `morning-forks-*.md`) use **`YYYY-MM-DD`** in the basename unless the doc names a compact id pattern. Full rules, UTC timestamps, and **`YYYYMMDD`** exceptions: [Date and time formats](../date-time-conventions.md).

---

## See also

- **`strategy + verify`** (named fork) — §4 **Combo and hybrid options** above; full spec under **work-strategy** in [skill-strategy SKILL](../../.cursor/skills/skill-strategy/SKILL.md).
- **Fixed session menu (`coffee` — same A–G for work-start and signing-off; legacy hey still works):** not the 3–5 WORK pattern — use the canonical **`coffee`** fixed menu, listed **A, B, C, D, E, F, G** (seven modes; **no** close letter). **A — Daily Brief**, **B — Build**, **C — Compass** (includes work-strategy-rome), **D — Book**, **E — Steward**, **F — Xavier next**, **G — Dev next** (`workspace.md` § Next actions). **C** and **D** exit the coffee hub by default unless **`stay in coffee`**; **skills** / **meta:** say with **B**. Roles: [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md).
- [Operator–agent lanes](../../operator-agent-lanes.md)
- [Coffee skill](../../../.cursor/skills/coffee/SKILL.md)
- [Work territory history logs](work-modules-history-principle.md) (`docs/skill-work/work-*/*-history.md`)
- [Bootstrap — coffee](../../../bootstrap/grace-mar-bootstrap.md)
- [Date and time formats](../date-time-conventions.md)
