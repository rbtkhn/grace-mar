# work-xavier — advisor / project module (grace-mar)

**Purpose:** **WORK territory** in the grace-mar repo for coordinating work with **Xavier** as **employee / business partner** (SMM and related execution) — contracts, mirrors, runbooks, content plans, operator navigation, **employee work profile / skills portfolio** ([xavier-work-profile.md](xavier-work-profile.md)), and **SMM capability evaluation** against those plans ([xavier-smm-capability-rubric.md](xavier-smm-capability-rubric.md)). This is the layer **you** work in together; it is **not** Xavier’s sovereign **Record** repository.

**Separate concern — `companion-xavier` (her repo):** Xavier’s **instance** (Identity Fork Protocol paths under `users/<id>/`, gate, seed survey, Voice), when she creates it from [companion-self](https://github.com/rbtkhn/companion-self), lives in **her own GitHub repository** (often named like **companion-xavier**). That code and Record **do not** need to be copied into grace-mar. This folder documents how grace-mar interfaces with that work **without** hosting her fork.

**Read first:** [INDEX.md](INDEX.md) · [ALIGNMENT.md](ALIGNMENT.md) · [LANES.md](LANES.md) · [TERMS-XAVIER.md](TERMS-XAVIER.md) · Template baseline (canonical): [work-companion-self/TEMPLATE-BASELINE.md](../work-companion-self/TEMPLATE-BASELINE.md) · Boundaries: [audit-boundary-grace-mar-companion-self.md](../../audit-boundary-grace-mar-companion-self.md) (grace-mar · template); her instance follows the same rules **in her repo**.

**Never copy** `users/grace-mar/**` into another companion’s instance tree. See [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

**Session 0 / seed survey:** Lives **in Xavier’s repository** (paths such as `docs/seed-survey/` or `users/xavier/` per her layout from the template) — not under `docs/skill-work/work-xavier/` here. Operator docs: [GOOD-MORNING.md](GOOD-MORNING.md), [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md). **Day-one instance setup (GitHub + open only):** [xavier-instance-two-step.md](xavier-instance-two-step.md) — send before first Good Morning if she does not have her repo yet.

**Daily sync surface (advisor view):** [SYNC-DAILY.md](SYNC-DAILY.md). **Mirrors:** [work-dev-mirror/README.md](work-dev-mirror/README.md), [work-politics-mirror/README.md](work-politics-mirror/README.md).

**Operator observations (progress / evidence):** [xavier-progress-log.md](xavier-progress-log.md) — qualitative notes, hypotheses, coaching hooks; artifacts in [evidence/](evidence/). **Milestones + dated pointers:** [work-xavier-history.md](work-xavier-history.md).

**BrewMind (Philippines pilot):** [brewmind-philippines-onboarding-guide.md](brewmind-philippines-onboarding-guide.md) — bundle hub for strategy, brand, field script, and PH market notes ([INDEX.md](INDEX.md) lists all BrewMind WORK files).

**Portability:** Patterns in this module are intended to be **mirrored or adapted** for other companion-self operator/agent workspaces; the instance Record stays in each companion’s repo.

**Template alignment:** [work-xavier-sources.md](work-xavier-sources.md) (feeds / pointers), [LANE-CI.md](LANE-CI.md) (PR labels), [WORK-LEDGER.md](WORK-LEDGER.md) (watches + compounding). Concept map: [work-template/MAPPING.md](../work-template/MAPPING.md) (section *work-xavier (advisor module)*).

**Scripts (repo):** [scripts/build_xavier_handbook_bundle.py](../../../scripts/build_xavier_handbook_bundle.py) — assemble `smm-xavier-handbook-bundle.md` for print/PDF inputs. [scripts/generate_smm_xavier_pdf.sh](../../../scripts/generate_smm_xavier_pdf.sh) — regenerate print HTML + PDF via headless Chrome (run on a normal macOS host if CI/sandbox blocks).

### Record, Voice, and WORK execution (this folder)

- **Record** — Lived identity under `users/<id>/` in **her** instance repo; durable truth enters only through **her** recursion-gate and merge script.
- **Voice** — Speaks the Record when queried; bounded by what is merged and by prompt rules.
- **WORK execution** — Operator, AI assistant, and scripts running **WORK modules** (this folder, mirrors, Cursor workflows): drafts, plans, and **optional ongoing sync** of pattern docs with a source tree. This layer does **not** own the Record; anything that changes identity or Voice obligations must surface as **candidates** in **her** `recursion-gate.md` (or explicit companion-approved policy), not as silent edits to `self.md`.

### Words we use (avoid confusion)

- **Cognitive fork / Record** — The governed self (Identity Fork Protocol). Not “a copy of someone else’s markdown tree.”
- **Git repository / instance repo** — Where that Record lives (e.g. `companion-xavier`). “Fork” on GitHub is **hosting**; it is not the same word as **cognitive fork**.
- **Mirror / track / sync** — Use for `work-*` **advisor** layouts you keep **aligned over time** with a golden source. Prefer this over **“fork once”** when you mean **ongoing** alignment.

---

## Governance contract (compact)

1. **Primary output (grace-mar):** `work-xavier` = advisor project + operator artifacts; **not** Xavier’s gated Record files.
2. **Primary output (her repo):** `companion-xavier` (or her chosen repo name) = her instance; durable identity truth enters only through **her** gate and merge script.
3. **Mirror scope:** Mirror workflow docs and ops artifacts **here** for your advisory cadence; do **not** mirror identity Record prose across repos without her pipeline.
4. **Directionality:** Approved patterns flow from grace-mar skill-work into mirrors; conflicts require human resolution.
5. **Ownership (RACI):** operator / AI assistant drafts; Xavier / operator review; companion approves gated merges **in her repo** for identity; you approve public ship for your content.
6. **Promotion path (her repo):** candidate → `recursion-gate.md` → approval → `process_approved_candidates.py --apply`.
7. **Security boundary:** no secrets in shared mirror docs.
