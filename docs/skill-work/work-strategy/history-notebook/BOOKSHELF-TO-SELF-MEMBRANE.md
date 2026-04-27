# Bookshelf to Self-Knowledge Membrane

WORK-only implementation contract for promoting validated bookshelf signals into draft Record candidates.

This membrane is integrated into `coffee` as a fixed branch under `E` (system choice): **Self-knowledge quiz**.

## Purpose

- Keep `self-library-bookshelf` as the source layer.
- Use multiple-choice quiz rounds to capture companion judgment about book subject matter.
- Convert claim-reviewed outcomes into **draft** `CANDIDATE-XXXX` proposals only.
- Preserve existing authority: no merge without companion approval in `recursion-gate.md`.

## Coffee Integration

- Entry: `coffee` -> Step 2 -> `E` -> choose **self-knowledge quiz**.
- Session mode: **multi-round** (5-10 MCQs per round).
- After each round, ask: continue or stop.
- On stop, emit:
  - report: `research/BOOKSHELF-MEMBRANE-REPORT.md`
  - draft queue: `research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`

## Data Boundary

- Inputs:
  - `research/bookshelf-catalog.yaml`
  - optional `research/bookshelf-web-enrichment-*.yaml`
  - quiz responses (session JSON)
- Outputs:
  - work artifact report
  - draft candidate blocks (pending; not auto-inserted in gate)
- Prohibited:
  - direct writes to `users/grace-mar/recursion-gate.md` unless explicitly requested
  - any direct merge into `self.md`, `self-archive.md`, or prompt files

## Tier Rules

Tiering evaluates both evidence and companion response strength.

- **Low**
  - weak, single-book, or contradictory signal
  - draft wording must remain tentative
  - default action: hold in work report; optional draft candidate

- **Medium**
  - coherent signal across 2-3 books or one strong cluster
  - draft wording bounded and specific
  - produce pending candidate draft with clear evidence links

- **High**
  - repeated cross-cluster signal (multiple books/authors/tags) plus high response confidence
  - include fuller rationale and possible contradiction note
  - produce pending candidate draft with strong evidence packet

## Claim Selection Model (v2)

Each answered tag produces one explicit proposed self-knowledge statement.

Decision path:

1. Companion selection -> stance (`enduring` / `active` / `context` / `deferred`)
2. Evidence fitness -> supporting `HNSRC-*` depth + author spread
3. Cross-tag repeat -> whether the same type of signal appears across distinct clusters

Tiering is epistemic, not numeric:

- `high`: enduring claim with strong evidence fit and repeat across multiple affirmed tags
- `medium`: active/enduring claim with bounded evidence fit
- `low`: context-only, weak-evidence, or deferred claim

Low/deferred claims remain primarily in the report unless explicitly promoted.

## Candidate Draft Schema

Each draft block must include:

- one-line summary
- `profile_target` suggestion (usually `ix-b` or `ix-c`; `ix-a` only when factual)
- evidence bullets with `HNSRC-*` ids
- uncertainty note when applicable
- `status: pending`

## Companion Review Checklist

Before approving any membrane-derived draft:

1. Grounded in companion answers, not model inference.
2. Supported by cited bookshelf evidence.
3. Appropriate destination (`self-library` vs `self-knowledge`).
4. Non-duplicative with existing `self.md` claims.
5. Wording remains proportional to evidence strength.

## Commands

Generate round + evaluate responses:

```bash
python3 scripts/build_bookshelf_membrane_candidates.py --emit-round --round-index 1
python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json
python3 scripts/build_bookshelf_membrane_candidates.py --responses-file docs/skill-work/work-strategy/history-notebook/research/bookshelf-membrane-responses.json --check
```

## Notes

- Narnia/boxed-set and other edition-ambiguous holdings may be used for quiz context but should not receive bibliographic certainty claims unless edition identity is confirmed.
- Membrane output is advisory-to-gate, never a substitute for companion approval.
