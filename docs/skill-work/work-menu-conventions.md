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
- When two options combine naturally, you may add one line: **Combo:** `B + half of D` — *merge preview in prose* (still one human pick).

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

**Aggregate after ~30 days:**

```bash
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30
python3 scripts/menu_choice_evolution.py -u grace-mar --days 30 --print-gate-stub
```

The gate stub is **stdout only** — paste and edit **`CANDIDATE-XXXX`** before any merge.

---

## 7. Multi-agent fork generation (experimental)

See [work-strategy/multi-agent-fork-generator.md](work-strategy/multi-agent-fork-generator.md) — optional two-pass / subagent pattern; human still chooses one branch.

---

## 8. Dated filenames and CLI dates

Dated WORK outputs (daily brief, weekly scaffold, newsletter digest, optional `morning-forks-*.md`) use **`YYYY-MM-DD`** in the basename unless the doc names a compact id pattern. Full rules, UTC timestamps, and **`YYYYMMDD`** exceptions: [Date and time formats](../date-time-conventions.md).

---

## See also

- [Operator–agent lanes](../../operator-agent-lanes.md)
- [Daily warmup skill](../../../.cursor/skills/daily-warmup/SKILL.md)
- [Bootstrap — good morning](../../../bootstrap/grace-mar-bootstrap.md)
- [Date and time formats](../date-time-conventions.md)
