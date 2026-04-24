# Visual inspection protocol (Workbench)

**Purpose:** Required steps when a generated artifact is **visually** rendered (web UI, React, browser canvas, SVG in viewer, local HTML). Headless tools may skip *screenshot* steps but should still set `inspection.method` to something like `n/a_headless` and document the substitute.

**Maps to:** [WORKBENCH-RECEIPT-SPEC.md](WORKBENCH-RECEIPT-SPEC.md) → `inspection`, `launchCommand`, `commandsRun`, `revisionSummary`, `status`.

## 1. Launch command

- Record the **exact** command or URL the operator used (e.g. `npm run dev`, `open path/to/index.html`, `python3 -m http.server`).
- Put it in `launchCommand` and mirror any setup commands in `commandsRun`.

## 2. Screenshot or manual observation

- For browser UIs: capture at least one **repo-relative** path to a saved image under `inspection.screenshots`, **or** write a single explicit sentence in `inspection.method` (e.g. `manual_observation_no_artifact: described in observedFailures/acceptanceChecklist if needed`) *only* when you truly cannot store an image and must rely on a named witness note — default is: **save a screenshot to disk and link it**.
- Note viewport / theme if material (e.g. “dark mode,” “mobile width”).

## 3. Visible failure notes

- List anything that did not render, misaligned, threw in the console, or failed a visible acceptance criterion under `inspection.observedFailures`. Copy/paste the **first** console error line if useful.

## 4. Acceptance checklist

- Write short, checkable items in `inspection.acceptanceChecklist` (each line can be `criterion: ok|fail|skipped`).
- These prove **UI behavior in this build**, not external truth.

## 5. Revision log

- If you fix CSS, props, or routes and re-run, append to `revisionSummary` (what changed, not a git commit list unless that is the only trace).

## 6. Final status

- Set `status` to `pass`, `fail`, or `inconclusive` to match the checklist and observed failures.
- If you revoke a prior receipt, prefer a **new** receipt with `status: "revoked"` and pointer to the superseded `receiptId` in `revisionSummary`, or a clear convention your team uses.

## Truth scope (repeat)

- Screenshots and visible checks = **artifact behavior** only. They do not validate geopolitical, medical, or other **world** claims in the data the UI *displays*.
