---
name: skill-cici
preferred_activation: skill-cici
description: "Cici / OB1 learning rhythm and day journal — distilled from cici-notebook. Two modes: (A) mentor in grace-mar with GitHub digest + inbox + optional full-day synthesis; (B) Xavier in Cici repo with the same section template, manual commit spine, governed-state checks. Triggers: skill-cici, cici journal, Cici day, OB1 learning log (legacy phrasing: xavier journal)."
---

# skill-cici — Cici notebook baseline

**Primary triggers:** **`skill-cici`**, **`cici journal`**, **`Cici day`**, **`OB1 learning log`**.

**Purpose:** Run a **consistent daily (or session) learning log** for **Open Brain (OB1)**, the **[Cici](https://github.com/Xavier-x01/Cici)** instance repo, and **BrewMind** — without confusing **WORK coaching** with **Record** or **gate** merges.

**Canonical prose + automation spec (grace-mar):** [docs/skill-work/work-cici/cici-notebook/README.md](../../../docs/skill-work/work-cici/cici-notebook/README.md) · [SYNTHESIS-SOURCES.md](../../../docs/skill-work/work-cici/cici-notebook/SYNTHESIS-SOURCES.md).

---

## Routing (do this first)

Answer one question:

- **“In Xavier’s OB1 / Cici / BrewMind world, I am observing, coaching, or logging …”** → this skill (and **cici-notebook** paths in grace-mar if Mode A).
- **“In grace-mar’s own work-dev / integration / harness, I am building …”** → [dev-journal (dev-notebook/journal)](../../../docs/skill-work/work-dev/dev-notebook/journal/README.md), not this skill.

If a day touches **both**, split: Xavier trajectory **here**; grace-mar implementation reflection **dev-journal**.

---

## Day file template (both modes)

Use one file per calendar day: **`YYYY-MM-DD.md`**. Put **Journal day:** *N* (ordinal) in the body, not only in the filename.

**Sections (keep headings stable):**

1. **Focus** — what matters today in *her* words (not only git).
2. **What I did today** — concrete actions.
3. **What clicked** — durable insight.
4. **Friction / questions** — blockers, repo confusion, setup gaps.
5. **Tomorrow** — one or two next steps.
6. **One line for my advisor** — compress the day for mentor scan.

**Optional block when there is git activity**

- **OB1 repo activity** — bullet list of commits (links to GitHub) plus a one-line summary. In Mode A this can be **filled or prefilled** by the digest script; in Mode B fill from [Cici commits](https://github.com/Xavier-x01/Cici/commits/main) or `git log`.

---

## Layer mental model (L1 / L2 / L3)

| Layer | Meaning | Mode A (grace-mar) | Mode B (Cici) |
|-------|---------|---------------------|---------------|
| **L1** | Git signal — what shipped | [cici_journal_ob1_digest.py](../../../scripts/cici_journal_ob1_digest.py) pulls **Cici** `main` for the calendar window | Paste commits or link to GitHub compare for that day |
| **L2** | Operator / same-day context | `cici-notebook/inbox/`, optional `--full-day-synthesis` (strategy-notebook + session-transcript per [SYNTHESIS-SOURCES](../../../docs/skill-work/work-cici/cici-notebook/SYNTHESIS-SOURCES.md)) | Short notes in-repo (e.g. `docs/personal/` or a `journal/` folder **you** create — keep **no secrets**) |
| **L3** | Artifact pointers | `artifacts:` in inbox frontmatter or `YYYY-MM-DD-artifacts.txt` | Repo-relative links to docs you touched |

If **L1 (commits)** and **L2 (notes)** disagree, do not force resolution: add a single **`Tension:`** line in prose (per SYNTHESIS-SOURCES).

---

## Mode A — Mentor / operator in grace-mar

**Where files live:** `docs/skill-work/work-cici/cici-notebook/`

**Steps**

1. **Optional rolling capture** during the day: append to [daily-cici-notebook-inbox.md](../../../docs/skill-work/work-cici/cici-notebook/daily-cici-notebook-inbox.md). At **`dream`**, fold into `inbox/YYYY-MM-DD.md` (see [inbox README](../../../docs/skill-work/work-cici/cici-notebook/inbox/README.md)).
2. **Generate or refresh the day file** from repo root (set **`TZ`** to your local calendar day):
   ```bash
   TZ=America/New_York python3 scripts/cici_journal_ob1_digest.py --full-day-synthesis --write
   ```
   Git-only: omit `--full-day-synthesis` or use `--no-inbox`. See [cici-notebook README](../../../docs/skill-work/work-cici/cici-notebook/README.md) for flags, `GITHUB_TOKEN`, catch-up, and `--force`.
3. **Edit** the generated file: fill **Focus**, narrative sections, and **One line for my advisor**. Keep **secrets out** (no API keys, no credentialed URLs).
4. **End-of-day:** [dream SKILL](../dream/SKILL.md) may include running the digest for “today” if the day file is missing — follow dream skill; digest does **not** run inside `auto_dream.py` by itself.

**Recursive learning (optional):** Strong days → one line in [work-cici-history.md](../../../docs/skill-work/work-cici/work-cici-history.md); occasional [harvest](../harvest/SKILL.md) over recent `cici-notebook/*.md`.

---

## Mode B — Xavier in Cici ([Xavier-x01/Cici](https://github.com/Xavier-x01/Cici))

**No grace-mar scripts required.** Same **section template** and **routing** rules; paths are **hers**.

**Steps**

1. **Pick calendar day** and create or edit a markdown file where she keeps learning notes (Cici is config/docs–centric; there is no built-in `cici-notebook/` mirror unless she adds one — e.g. `docs/journal/YYYY-MM-DD.md` or personal paths under `docs/personal/` per her README).
2. **L1:** List that day’s commits on **`main`** (GitHub UI or `git log --since --until`).
3. **L2:** Short notes: what she tried (Supabase, MCP, BrewMind site), what blocked.
4. If she changed **`proposals/`**, **`users/cici/`**, or **`config/`**, run Cici’s validator when present:
   ```bash
   python3 scripts/validate-governed-state.py
   ```
   Align with [Governed State Model](https://github.com/Xavier-x01/Cici#governed-state-model-phase-1) and `docs/governed-state-doctrine.md` on Cici.

**Closeout (no grace-mar dream):** Three bullets — **Shipped / Blocked / Tomorrow** — optional but recommended.

---

## Guardrails

- **WORK / coaching only** — not Xavier’s **Record** in her companion repo; not **RECURSION-GATE** merges unless material is explicitly staged through her pipeline.
- **No secrets** in journal text or inbox (tokens, MCP keys in URLs). Reference env vars and dashboards in prose.
- **Do not** treat journal text as canonical identity truth for grace-mar **SELF** without the normal gate.
- **Companion / operator roles:** Mentor uses grace-mar **work-cici**; Xavier uses **Cici** for instance truth-in-git; keep leakage rules in [LEAKAGE-CHECKLIST.md](../../../docs/skill-work/work-cici/LEAKAGE-CHECKLIST.md) in mind when pasting paths across repos.

---

## Relation to strategy, skill-write, and THINK

Borrowings are **light** — cici-notebook stays **WORK coaching**, not strategy geopolitics, not operator public copy, not Record THINK.

### skill-strategy (best alignment)

- **Frontier on disk:** Treat the latest written **`YYYY-MM-DD.md`** (and **Journal day** line) as the checkpoint — read files; do not rely on chat memory alone.
- **Capture → fold → digest:** Same rhythm as strategy’s inbox → dream: [daily-cici-notebook-inbox](../../../docs/skill-work/work-cici/cici-notebook/daily-cici-notebook-inbox.md) → `inbox/YYYY-MM-DD.md` → [cici_journal_ob1_digest.py](../../../scripts/cici_journal_ob1_digest.py).
- **Same calendar day, mixed work:** When the day mixes OB1 trajectory and strategy judgment, **`--full-day-synthesis`** is the integration hook (strategy-notebook + session-transcript per [SYNTHESIS-SOURCES](../../../docs/skill-work/work-cici/cici-notebook/SYNTHESIS-SOURCES.md)). Git-only days can omit it.

### skill-write (edge cases only)

- **Private journal** does not need Locals/X craft. When **One line for my advisor** (or an excerpt) becomes **public** BrewMind or social copy, apply [topic-first ledes](../../rules/drafting-topic-lede.mdc) and [operator writing preferences](../../../docs/skill-write/write-operator-preferences.md) for that surfaced line — not for full private sections.

### THINK (boundary, not merge)

| Surface | Role |
|--------|------|
| **cici journal** | WORK learning log; not gate input unless explicitly staged elsewhere. |
| **THINK** (`skill-think.md` / index) | Record capability intake; promotion to SELF via gate when identity-facing. |
| **SELF / EVIDENCE** | Canonical fork truth and dated spine — journal text does **not** substitute. |

See [think-purpose-and-boundary.md](../../../docs/skill-think/think-purpose-and-boundary.md).

---

## Porting this skill to Cici

1. Copy **`.cursor/skills/skill-cici/`** into the Cici repo under **`.cursor/skills/skill-cici/`**.
2. In **SKILL.md**, trim or stub **Mode A** if confusing; keep **Mode B**, **template**, **guardrails**, and **validator** pointer.
3. Optionally add one line to **Cici `CLAUDE.md`**: e.g. “Daily learning log: follow `.cursor/skills/skill-cici/SKILL.md` (Mode B).”

---

## Related

| Topic | Link |
|--------|------|
| Full journal spec | [cici-notebook README](../../../docs/skill-work/work-cici/cici-notebook/README.md) |
| Synthesis flags | [SYNTHESIS-SOURCES.md](../../../docs/skill-work/work-cici/cici-notebook/SYNTHESIS-SOURCES.md) |
| Digest script | [scripts/cici_journal_ob1_digest.py](../../../scripts/cici_journal_ob1_digest.py) |
| Work-xavier index | [INDEX.md](../../../docs/skill-work/work-cici/INDEX.md) |
| skill-strategy (parallel rhythm) | [skill-strategy/SKILL.md](../skill-strategy/SKILL.md) |
| THINK boundary | [think-purpose-and-boundary.md](../../../docs/skill-think/think-purpose-and-boundary.md) |
| Operator writing (public excerpts only) | [write-operator-preferences.md](../../../docs/skill-write/write-operator-preferences.md) |
