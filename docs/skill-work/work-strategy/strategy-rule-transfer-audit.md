# Strategy rule transfer audit

**Status:** WORK documentation. Not Record. Not a merge path.

Purpose: identify which strategy-oriented `.cursor/rules/*.mdc` files still carry live contract weight, and which already have a neutral SSOT in strategy docs or skills.

---

## Summary

The strategy rule layer is in better shape than the general `.mdc` layer.

Many strategy rules already behave like **adapters** rather than hidden law: they point to strong neutral docs such as `STRATEGY-NOTEBOOK-ARCHITECTURE.md`, `raw-input/README.md`, `NOTEBOOK-PREFERENCES.md`, and `minds/README.md`.

The main remaining work is smaller:

- verify that every strategy `.mdc` with an operational invariant has a neutral SSOT
- identify where the only binding wording still lives in `.mdc`
- leave host-specific convenience behavior in `.mdc` when it is merely routing or ergonomics

---

## Audited rules

### `strategy-input-raw-ingest.mdc`

**Judgment:** mostly transferred already.

Neutral homes present:
- `docs/skill-work/work-strategy/strategy-notebook/raw-input/README.md`
- `docs/skill-work/work-strategy/strategy-notebook/raw-input/CAPTURE-TYPES.md`
- `docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md`
- `docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md`

Conclusion:
- keep the `.mdc` as a host reminder
- no urgent doctrine gap found

### `strategy-inbox-accumulator-date.mdc`

**Judgment:** transferred.

Neutral homes present:
- `docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md`
- verifier script `scripts/verify_strategy_inbox_accumulator.py`

Conclusion:
- `.mdc` is redundant but harmless
- no urgent doctrine gap found

### `strategy-notebook-days-date-semantics.mdc`

**Judgment:** transferred.

Neutral home present:
- `docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md` (`days.md` date semantics)

Conclusion:
- this is already a reminder layer, not hidden law

### `strategy-civ-mem-grounding.mdc`

**Judgment:** mostly transferred, but check the fallback branch wording.

Neutral homes present:
- `.cursor/skills/skill-strategy/SKILL.md`
- `docs/skill-work/work-strategy/minds/CIV-MEM-TRI-FRAME-ROUTING.md`
- `docs/skill-work/work-strategy/strategy-notebook/TRUMP-LEO-CIV-MEM-BARNES-DRILL.md`

Open question:
- whether the fallback branch logic should also live in a neutral strategy doc, not only in the skill and `.mdc`

Conclusion:
- medium-priority follow-up, not a crisis

### `strategy-minds-granular.mdc`

**Judgment:** partially transferred.

Neutral homes present:
- `docs/skill-work/work-strategy/LEARN_MODE_RULES.md`
- `docs/skill-work/work-strategy/minds/README.md`

Likely remaining dependency:
- in-voice authenticity still points to `.cursor/rules/minds-authentic-voice.mdc`

Conclusion:
- the "no default tri-frame" rule is covered
- the authentic-register enforcement may still lack a neutral home

### `strategy-named-expert-mind-gate.mdc`

**Judgment:** likely still carries live contract weight.

This rule says:
- if a named expert lens is requested
- resolve the expert mind file
- read it before substantive in-voice analysis
- refuse impersonation if no mind file exists

This appears important enough to have a neutral home, but no obvious strategy SSOT was surfaced in this audit.

Conclusion:
- high-priority promotion candidate

### `strategy-expert-thread-journal-layer.mdc`

**Judgment:** partly transferred, but verify completeness.

Neutral home likely present:
- `docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md`

Need to confirm that the neutral doc fully carries:
- prose-first journal layer
- machine-layer boundary
- month-segment prose minimum expectations
- cross-check block guidance

Conclusion:
- medium-priority verification

---

## Working classification

### Already neutralized enough

- `strategy-input-raw-ingest.mdc`
- `strategy-inbox-accumulator-date.mdc`
- `strategy-notebook-days-date-semantics.mdc`

### Neutralized, but verify completeness

- `strategy-civ-mem-grounding.mdc`
- `strategy-minds-granular.mdc`
- `strategy-expert-thread-journal-layer.mdc`

### Strongest candidates for promotion next

1. `strategy-named-expert-mind-gate.mdc`
2. any missing neutral equivalent of `minds-authentic-voice.mdc` if expert-lens voice is meant to work cross-host
3. any missing fallback-branch wording for civ-mem grounding

---

## Recommended next pass

1. Read the neutral strategy docs for named-expert lensing and confirm whether the mind-gate contract is written there.
2. Check whether authentic voice constraints for strategy minds have a neutral home or remain `.mdc`-only.
3. Confirm that the expert-thread journal-layer rules are fully mirrored in architecture docs, not merely referenced there.
