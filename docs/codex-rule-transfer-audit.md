# Codex rule transfer audit

**Status:** WORK documentation. Not Record. Not a merge path.

Purpose: map the repo's local Cursor-oriented rule surfaces onto Codex behavior, identify what already transfers well, and recommend which rules should be promoted into repo-neutral doctrine.

---

## How Codex sees local rules

Codex does **not** automatically activate every file under `.cursor/`.

Three practical buckets:

| Bucket | What it means in Codex | Typical surfaces |
|--------|-------------------------|------------------|
| **Always-on in this repo** | Loaded as repo instruction context or otherwise treated as authoritative in-session | `AGENTS.md`; host-provided developer/system instructions; repo files explicitly surfaced into the session |
| **Invocation-bound / read-to-apply** | Not auto-loaded, but should be consulted when the task clearly invokes that workflow | `.cursor/skills/*/SKILL.md`; lane specs under `docs/skill-work/**`; specific rule files read during work |
| **Cursor-only unless rewritten** | Depend on Cursor auto-application, UI assumptions, or menu mechanics that Codex does not inherit automatically | many `.cursor/rules/*.mdc`; UI/menu routing details tied to Cursor conventions |

Short rule: in Codex, **`AGENTS.md` and instance doctrine carry the always-on load**. `.cursor/skills` are callable local protocols. `.cursor/rules` are **not** globally active just because they exist.

---

## Current repo surfaces

### Strong cross-agent surfaces

These already transfer well, or should be treated as the main cross-host doctrine:

- `AGENTS.md`
- `users/grace-mar/instance-doctrine.md`
- `docs/architecture.md`
- `docs/skill-work/work-cadence/**`
- `docs/skill-work/work-strategy/strategy-notebook/**` when that territory is active

### Invocation-bound surfaces

These work well in Codex when deliberately opened:

- `.cursor/skills/bridge/SKILL.md`
- `.cursor/skills/coffee/SKILL.md`
- `.cursor/skills/conductor/SKILL.md`
- `.cursor/skills/dream/SKILL.md`
- `.cursor/skills/harvest/SKILL.md`
- `.cursor/skills/skill-strategy/SKILL.md`
- other lane-specific `.cursor/skills/*/SKILL.md`

### Rule files that need interpretation

The following `.mdc` files contain useful policy, but should not be assumed active in Codex without promotion or deliberate read:

- `.cursor/rules/operator-style.mdc`
- `.cursor/rules/territory-awareness.mdc`
- `.cursor/rules/grace-mar.mdc`
- `.cursor/rules/strategy-expert-thread-journal-layer.mdc`
- territory-specific strategy rules such as raw-ingest, date semantics, minds, and named-expert gates

---

## Transfer recommendations

### Promote to repo-neutral doctrine

These are important enough to be always-on across hosts:

1. **Rule surface awareness**
   - Codex does not auto-load `.cursor/rules`.
   - Critical rules must live in `AGENTS.md`, instance doctrine, or a neutral doc under `docs/`.

2. **Territory entry discipline**
   - On entering `docs/skill-work/<territory>/`, read the territory README and key specs first.
   - Respect lane boundaries and vocabulary.

3. **Operator comfort / execution hygiene**
   - Already partly promoted in `AGENTS.md`: minimize approval prompts, batch escalations, verify before asking.

4. **Record boundary and pipeline invariants**
   - Already mostly covered by `AGENTS.md` and instance doctrine.
   - Keep these in repo-neutral surfaces, not only `.mdc`.

### Keep invocation-bound

These are valuable, but should remain protocol-on-demand rather than always-on:

- coffee menus and subtracks
- conductor selection and action MCQs
- bridge packet ritual details
- dream closeout procedure
- harvest packet shaping
- strategy notebook micro-protocols for a specific file family

### Rewrite before promotion

These contain useful intent but should be translated before becoming cross-host doctrine:

- Cursor menu mechanics expressed as if every host enforces them
- proposal-first rules that may conflict with a host's higher-priority autonomy contract
- fixed UI references such as "Cursor model picker" or "fresh Cursor session"

---

## Candidate-by-candidate notes

### `operator-style.mdc`

**Value:** high. Contains real operator preferences, message-lane semantics, hypothesis-mode handling, menu discipline, and gate UX.

**Transfer judgment:** partial promotion.

Promote:
- hypothesis mode / "perhaps" means think first
- gate approval echo discipline
- short prompts are intentional
- menu discipline in WORK lanes where locally meaningful

Do not promote verbatim:
- any assumption that fixed coffee menus are globally active without invocation
- proposal-first language that conflicts with host-level "implement unless clearly brainstorming" behavior
- Cursor-only menu routing details

**Sharper shortlist from this file:** only three items look worth promoting next as cross-host doctrine:

1. **Territory entry discipline** — belongs in `AGENTS.md` because it applies across hosts and lanes.
2. **Short prompts are intentional** — belongs in instance doctrine because it is a durable operator preference.
3. **Message lanes (`PLAN`, `EXECUTE`, `DOCSYNC`, `EXECUTE_LOCAL`)** — now promoted as cross-host doctrine. The prefixes are host-neutral scope signals; detailed behavior should live in `docs/operator-agent-lanes.md`, not only in `.cursor` rules.

### `territory-awareness.mdc`

**Value:** high. Cross-host useful.

**Transfer judgment:** promote in distilled form.

Promote:
- read territory README/specs on entry
- do not leak assumptions across territories
- use local territory vocabulary

### `grace-mar.mdc`

**Value:** medium-high, but much of it duplicates stronger repo-neutral doctrine.

**Transfer judgment:** mostly already transferred.

Keep as a local shorthand, but prefer `AGENTS.md` + instance doctrine as the canonical cross-host source.

### `strategy-expert-thread-journal-layer.mdc`

**Value:** high inside strategy-notebook editing, low outside it.

**Transfer judgment:** keep invocation-bound, but make sure the normative rule also lives in strategy docs.

Promote only if missing from neutral docs:
- prose-first journal layer
- machine-layer boundary
- month-segment prose expectations

---

## Recommended next promotions

If we continue this cleanup, the next best transfers are:

1. Audit strategy `.mdc` rules and make sure every real data contract has a neutral home in `docs/skill-work/work-strategy/strategy-notebook/`.
2. Leave coffee / conductor / dream / bridge ritual detail in `.cursor/skills`, but keep their meaning and boundary rules in neutral docs.

---

## Working policy

Until further promotion work is done:

- Treat `AGENTS.md` and instance doctrine as the always-on source of truth.
- Treat `.cursor/skills/*/SKILL.md` as invocation-bound protocols.
- Treat `.cursor/rules/*.mdc` as advisory unless explicitly read.
- When a `.mdc` rule matters across hosts, promote the invariant into repo-neutral doctrine rather than assuming host magic.
