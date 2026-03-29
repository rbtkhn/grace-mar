# Seed Phase Wizard & Good Morning Brief (grace-mar)

**Purpose:** Operator-facing bootstrap and daily start ritual under canonical instance paths. **Governed by:** gated pipeline — these tools do **not** write `self.md`, `self-archive.md`, or `bot/prompt.py`; durable Record changes use [identity-fork-protocol.md](identity-fork-protocol.md).

**Template alignment:** Companion-self **Seed Phase v2** (JSON artifacts + schemas) is documented separately; see [companion-self-seed-phase-v2-mapping.md](companion-self-seed-phase-v2-mapping.md) for how this wizard relates to that protocol.

---

## Canonical stage mapping (Seed Phase v2)

Companion-self defines **stages 0–7** as the portable formation pipeline ([companion-self `docs/seed-phase-stages.md`](https://github.com/rbtkhn/companion-self/blob/main/docs/seed-phase-stages.md)):

0. **Intake** — constraints, context, `seed_intake.json`  
1. **Identity Scaffold** — `seed_identity.json`  
2. **Curiosity Scaffold** — `seed_curiosity.json`  
3. **Pedagogy Scaffold** — `seed_pedagogy.json`  
4. **Expression Scaffold** — `seed_expression.json`  
5. **Memory Contract** — `seed_memory_contract.json`  
6. **Trial Interactions** — `seed_trial_report.json`  
7. **Readiness Gate** — `seed_readiness.json`, dossier  

**Wizard disclaimer:** `seed-phase-wizard.py` is an **instance** operator tool (reflection proposals, `seed/minimal-core.json`, MEMORY tone, completion marker). It **does not** emit the full template JSON set by itself. Use the mapping doc when reconciling wizard output with template validation or future export tooling.

---

## Scripts

| Script | Role |
|--------|------|
| [`scripts/seed-phase-wizard.py`](../scripts/seed-phase-wizard.py) | Interactive wizard: reflection-proposals, `seed/minimal-core.json`, `self-memory.md` tone note, `SEED-PHASE-COMPLETED.json` |
| [`scripts/good-morning-brief.py`](../scripts/good-morning-brief.py) | Short morning ritual; optional daily intention file under `reflection-proposals/` |

Run from repository root:

```bash
python3 scripts/seed-phase-wizard.py
python3 scripts/seed-phase-wizard.py -u my-fork
GRACE_MAR_USER_ID=my-fork python3 scripts/seed-phase-wizard.py
python3 scripts/seed-phase-wizard.py --require-proposal-class   # strict integrity (matches CI)
```

```bash
python3 scripts/good-morning-brief.py
python3 scripts/good-morning-brief.py -u grace-mar
python3 scripts/good-morning-brief.py --skip-warmup-prompt      # non-interactive / tests
```

---

## Paths created (under `users/<id>/`)

| Path | Record? | Notes |
|------|---------|--------|
| `reflection-proposals/SEED-founding-intent.md` | No | Operator narrative; promote via gate if needed |
| `reflection-proposals/SEED-initial-sparks.md` | No | Curiosity seed |
| `reflection-proposals/SEED-tensions-note.md` | No | Optional tensions annotation |
| `reflection-proposals/DAILY-INTENTION-YYYY-MM-DD.md` | No | Written by good-morning-brief |
| `seed/minimal-core.json` | No | **Facts listed here are not merged into IX-A** — stage LEARN / candidates |
| `self-memory.md` (append) | No (MEMORY) | Seed wizard appends good-morning tone; see [memory-template.md](memory-template.md) |
| `SEED-PHASE-COMPLETED.json` | No | Marker + suggested next steps |

There is **no** top-level `Record/` directory; evidence spine is `self-archive.md`.

---

## Validators (seed wizard step)

When `self.md`, `self-archive.md`, and `recursion-gate.md` all exist under `users/<id>/`, the wizard runs:

- `python3 scripts/validate-integrity.py --user <id>` (optional `--require-proposal-class`)
- `python3 scripts/governance_checker.py`

If the instance directory is incomplete, validators are **skipped** with a message (typical during early bootstrap).

---

## Full morning stack

For RECURSION-GATE state, session tail, and work-politics pulse, use the **daily warmup** skill and harness:

- [`.cursor/skills/daily-warmup/SKILL.md`](../.cursor/skills/daily-warmup/SKILL.md)
- `python3 scripts/harness_warmup.py -u <id> [--compact]`

The good-morning brief can offer to run `harness_warmup` after the intention prompt.

---

## See also

- [alpha-mastery-adaptation.md](alpha-mastery-adaptation.md) — Alpha mastery philosophy mapped to the gate, evidence, and seed `minimal-core` progress units (`behavioral-change`, `identity-coherence`, `evidence-quality`).

---

## Template upstream

`companion-self` may adopt a variant of these scripts later. Instance sync contract: [merging-from-companion-self.md](merging-from-companion-self.md).
