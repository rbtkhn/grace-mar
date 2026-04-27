# Automation Readiness Ledger

**Status:** **WORK** documentation. This ledger classifies Grace-Mar **scripts**, **GitHub Actions**, **cadence rituals**, and **Cursor** **automation** **candidates** by **unattended** **safety** using [R0–R5](automation-readiness-policy.md#readiness-classes-r0r5) from [automation-readiness-policy.md](automation-readiness-policy.md).

**Advisory only:** These rows do not change CI or Cursor behavior until a workflow or runbook references them. For new work, **cite** a row here or add one (after [automation-classification-template.md](automation-classification-template.md)) and reconcile when [`.github/workflows/`](../../.github/workflows/) changes. (A future `scripts/audit_automation_readiness.py` is out of scope for this doc set.)

**Doctrine:** [AGENTS.md](../../AGENTS.md) · [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md)

---

## Column legend

| Column | Meaning |
| --- | --- |
| **Surface** | Name or path of the script, skill, workflow, or prompt. |
| **Type** | e.g. cadence ritual, script, GitHub Action, Cursor prompt candidate. |
| **Class** | R0–R5; **dual** (e.g. R0 / R1) = see **Reason** for scope split; [policy](automation-readiness-policy.md#readiness-classes-r0r5). |
| **Allowed** **unattended** | **Max** **permitted** **unattended** **behavior** for **that** **surface** **and** **context** (local vs CI vs Cursor). |
| **Prohibited** **unattended** | Must **not** be **fully** **replaced** **by** a **bot** / **or** **must** **not** **run** **without** **policy**. |
| **Reason** | Short **justification** **(links** to **skills** / **workflows** **as** **needed**). |

---

## Cadence rituals

| Surface | Type | Class | Allowed unattended | Prohibited unattended | Reason |
| --- | --- | --- | --- | --- | --- |
| `coffee` (skill) | Cadence ritual | R0 | None for ritual “completion” | Auto-selection, bot claiming cadence is done, ritual substitution | [AGENTS.md](../../AGENTS.md) L66–L68, [.cursor/skills/coffee/SKILL.md](../../.cursor/skills/coffee/SKILL.md) — human **orientation** **menu** **A–E** **;** **operator** **voice**. |
| `dream` (skill) | Cadence / maintenance | R0 / R1 | R1: read-only preflight (e.g. integrity text) **if** **explicitly** **scoped** as **read-only** | Autonomous `auto_dream.py` **as** **ritual** **closure** **without** **operator**; **merge** **or** **Record** **writes** in **that** **pass** | [dream skill](../../.cursor/skills/dream/SKILL.md); **R0** = **operator**-**driven** **end-of-day** **consolidation**; **R1** = **inspection** **only** **for** **preflight** **helpers**. |
| `bridge` (skill) | Session handoff | R0 | None for transfer prompt / seal | **Automatic** **transfer** **prompt** **without** **operator**; **staged** as **if** **bridge** **ran** | [.cursor/skills/bridge/SKILL.md](../../.cursor/skills/bridge/SKILL.md) — **operator** **voice** **and** **seal** **matter**. |
| `thanks` (skill) | Micro-beat | R0 (operator-invoked) / R2 (hypothetical nudge) | R0: none for **beat** **completion**; R2: **nudge** text only | Claiming the **ritual** **is** **done**; **R2** is **not** in repo **as** a **default** | [AGENTS.md](../../AGENTS.md) L66 **—** `thanks` **deprecated** in favor of **conductor** / **coffee** **light**; [.cursor/skills/thanks/SKILL.md](../../.cursor/skills/thanks/SKILL.md). **Future** “thanks nudge” bot: **R2** **at** **most**, not ritual completion. |
| Conductor | Cadence / strategy session | R0 (substance) / R2 (reminder) | R2: **reminder** or **summary** on a **schedule** (if **configured**) | Conductor **MCQ** **or** **substance** **as** **fully** **autonomous** **without** **operator** | [AGENTS.md](../../AGENTS.md) L66–L68, [.cursor/skills/conductor/SKILL.md](../../.cursor/skills/conductor/SKILL.md), [CONDUCTOR-PASS.md](../skill-work/work-coffee/CONDUCTOR-PASS.md). **Substance** **=** **R0** **(human** **holds** **reins**). |
| `harvest` (skill) | Extraction / packet | R1 / R2 | R1: read-only **packet** for **pasting**; R2: **comment**-like **if** “post only” | **Merging** **or** **gate** **touches** in **harvest** | [.cursor/skills/harvest/SKILL.md](../../.cursor/skills/harvest/SKILL.md) **—** **analysis** **import**, **not** **cold** **start**. |
| Handoff / re-entry (scripts + skill) | Diagnostics | R1 / R2 | R1: run **read-only** [operator_handoff_check.py](../../scripts/operator_handoff_check.py), [operator_reentry_stack.py](../../scripts/operator_reentry_stack.py); R2: **paste** **nudge** or **summary** for **operator** | **Gate** **decisions**, **re-entry** as **Steward** **/ **dream** | [.cursor/skills/handoff-check/SKILL.md](../../.cursor/skills/handoff-check/SKILL.md) **(coffee** **Step** **1** **in** some **intents**); **voice** = **R0** **(operator**). |

---

## Gate and Record authority

| Surface | Type | Class | Allowed unattended | Prohibited unattended | Reason |
| --- | --- | --- | --- | --- | --- |
| `process_approved_candidates.py --apply` | Script | R5 | **None** unattended | **Any** run **without** **explicit** **companion/operator** **merge** **intent** on **trusted** **path** | [AGENTS.md](../../AGENTS.md), [instance-doctrine.md](../../users/grace-mar/instance-doctrine.md) **—** only **merge** path **to** **Record** for **approved** **candidates** **(when** **operator** **runs** **it**). |
| `recursion-gate.md` (content decisions) | Record-adjacent | R5 for approve/move/delete candidates | **None** for **mutations** | **Unattended** **staging** from **untrusted** **text**; **automation** **editing** **queue** [contract](cursor-safe-automation-contract.md) §1–3 | Gate **is** **human**-**governed** **;** **read**-**only** **visibility** in **nudge** **prompts** is **R1/R2** **(see** **Cursor** **section**). |
| `self.md` / `self-archive.md` / `session-log.md` / `bot/prompt.py` | Protected paths | R5 (direct **edit**) | **None** for **unattended** **direct** **edits** | **Automation** **or** **CI** **writing** these **as** “Cursor” without **gated** **path** | [contract](cursor-safe-automation-contract.md), [policy §2](automation-readiness-policy.md#authority-rules-concrete). |
| Staging from untrusted PR/issue text | Pattern | R5 (blocked) | **None** (default) | Staging **new** **candidates** from **untrusted** **bodies** | [contract](cursor-safe-automation-contract.md) §4 **—** **unless** **future** **policy** **carves** **a** **narrow** **exception**. |
| `recursion-gate.md` (read-only list / counts) | Visibility | R1 / R2 | **List** **ids** and **one-line** **excerpt** **per** [gate-queue-nudge](prompts/cursor-gate-queue-nudge.md) if **dedicated** **prompt** **allows** | **Approving**, re-ordering, re-staging from **untrusted** **source** | [contract](cursor-safe-automation-contract.md) **§3** (list read-only where prompt says so). |

---

## Diagnostics and validation (scripts / tests)

| Surface | Type | Class | Allowed unattended | Prohibited unattended | Reason |
| --- | --- | --- | --- | --- | --- |
| [validate-integrity.py](../../scripts/validate-integrity.py) | Script | R1 | Run in **CI** **or** **local**; **report** **(exit** **non-zero** in **CI**); **Cursor** may **only** **summarize** | **Auto-fix** **drift** **or** **silently** **rewrite** **manifests** in **a** **cloud** **agent** | Read-mostly **;** [test.yml workflow](../../.github/workflows/test.yml). |
| [governance_checker.py](../../scripts/governance_checker.py) | Script | R1 | Run in **CI** / **local**; **report** | **Auto-edit** **“governance** **files**” **or** **Record** to **satisfy** check | [governance workflow](../../.github/workflows/governance.yml) **invocation**. |
| [audit_cadence_rhythm.py](../../scripts/audit_cadence_rhythm.py) | Script | R1 | Default: stdout/JSON (read-only). Optional `--pressure-report` may **write** a machine JSON under `artifacts/work-cadence/`; still R1 (metrics, not merge authority) | **Pretend** to **close** **cadence** **rituals** | [cadence-pressure-signals.md](../skill-work/work-cadence/cadence-pressure-signals.md) documents the pressure-report artifact. |
| [operator_handoff_check.py](../../scripts/operator_handoff_check.py) | Script | R1 | **Read** **+** **print**; **no** **merge** | **Applies** **candidates** | [handoff-check skill](../../.cursor/skills/handoff-check/SKILL.md). |
| [operator_reentry_stack.py](../../scripts/operator_reentry_stack.py) | Script | R1 / R2 | R1: **output** for **operator**; R2: **if** “post **summary** to **Slack/comment**” **only** | **Gate** **/ **Record** **writes** | Re-entry **nudge** is **R2** **narration** **only** **(see** **Cursor**). |
| `pytest` / `python -m pytest` (as in [test.yml](../../.github/workflows/test.yml)) | Test runner | R1 in CI; R1 local | **Fail** / **pass** in **GHA** | **Auto-merge** on **green** | Deterministic **test** **surface**; **R1** = **enforcement** **,** not **R2** **“comment** **bot**” **(unless** a **separate** **tool** **posts** **a** **summary**). |

---

## Derived artifacts (non-Record generated files)

| Surface | Type | Class | Allowed unattended | Prohibited unattended | Reason |
| --- | --- | --- | --- | --- | --- |
| [regen_grace_mar_derived.sh](../../scripts/regen_grace_mar_derived.sh) | Script | R4 (operator or approved CI) | **Operator** **run**; **or** **job** **explicitly** **documented** in **workflow** | **Cursor** **cloud** **automation** **running** this **as** “fix” [cursor-integrity-summary.md](cursor-integrity-summary.md) | **Regen** **=** **writes**; [When integrity reports stale derived exports](../skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports) (operator choice; human runs regen). |
| `grace-mar-llm.txt`, `manifest.json` / `fork-manifest.json`, runtime **bundle** JSON | Artifacts | R4 (under regen/CI) | **Regen** **via** **policy**; **not** **Record** **truth** by **themselves** | **Direct** **edit** **in** **Cursor** **as** “merge” | **Generated**; **source** of **truth** **lives** in **gated** **/ **self** **surfaces** **per** **doctrine**. |
| [build_library_index.py](../../scripts/build_library_index.py) (see [library-index.yml](../../.github/workflows/library-index.yml)) | Script | R4 in CI/operator; not Cursor default | **CI** **or** **local** `python3 ... -u grace-mar` | **Unreviewed** **Cursor** **auto-run** on **PR** [integrity guide](cursor-integrity-summary.md) | **Writes** `library-index.md` **(generated)**. |
| `generate_profile.py` (Pages deploy) | Script | R4 in CI (pages profile) | **GHA** on `main` as in [pages.yml](../../.github/workflows/pages.yml) | N/A | Regenerates site artifact; `users/grace-mar/**` path filters; not R5 merge; R4 under CI policy. |

---

## GitHub Actions workflows (complete set, 12)

*Paths:* [../../.github/workflows/](../../.github/workflows/). R-class = enforcement + effect. For **CI**, “unattended” means **repo-defined** triggers (not the same as **Cursor** authority); see [policy — Surfaces](automation-readiness-policy.md#surfaces-who-runs-what-unattended).*

| Surface | Type | Class | Allowed unattended (CI) | Prohibited / notes | Reason |
| --- | --- | --- | --- | --- | --- |
| [test.yml](../../.github/workflows/test.yml) | Workflow | R1 (enforcement) | Run full **test** + **validations** on **PR**/**push** | Replaces R0 **rituals**; **does** not **apply** `process_approved_candidates` | **Deterministic** pass/fail; **validates** many **R1** **scripts**. |
| [governance.yml](../../.github/workflows/governance.yml) | Workflow | R1; **R5** if step implies **gated** **Record** **commit** **discipline** (human) | **Govern** **+** **integrity** **jobs** as **defined** | **Unattended** **merge** | **Gated** **commit** **message** / **file** **rules** **(human** **commits** to **gated** **paths**). |
| [harness.yml](../../.github/workflows/harness.yml) | Workflow | R1 (diagnostic) | **Counterfactual** **harness** **(needs** `OPENAI_API_KEY` **secret**)** | Replaces **companion** **judgment** on **candidates** | **External** **LLM** **call** **in** **CI** **;** still **R1** **(check)** **,** not **R2** **PR** **comment** **layer**. |
| [naming-check.yml](../../.github/workflows/naming-check.yml) | Workflow | R1 | **Naming** **/ **convention** **check** as **file** **defines** | N/A | **Policy** **enforcement**. |
| [library-index.yml](../../.github/workflows/library-index.yml) | Workflow | R1 (verify) / R4 (regen) **per** **job** | **Build** or **check** **library** **index** **as** **workflow** | **Conflate** with **Cursor** **R2** | Often **R4**-style **regen** in **a** **job**; **treat** **as** **CI-owned** **regen** **(see** **workflow** **steps**). |
| [prp-refresh.yml](../../.github/workflows/prp-refresh.yml) | Workflow | R4 | **Scheduled/defined** **PRP** / **export** **refresh** **(derived)** | **Duplicate** in **separate** **ad-hoc** **Cursor** **automation** **without** **policy** | **Existing** **derived** **automation** **—** **do** **not** **duplicate** **unless** **policy** **says** **so**. |
| [newsletter.yml](../../.github/workflows/newsletter.yml) | Workflow | R4 | **Build** / **emit** **newsletter** **artifact** as **defined** | **Same** | **Scheduled** **derived** **artifact** **(non-Record** **unless** **policy** **elsewhere**). |
| [work-jiang.yml](../../.github/workflows/work-jiang.yml) | Workflow | R1 (validation / rebuild check) | **Jiang** **lane** **checks** as **in** **workflow** | N/A | **Domain**-specific **validation** **(see** **workflow** **body** for **exact** **commands**). |
| [lane-scope.yml](../../.github/workflows/lane-scope.yml) | Workflow | R1 (enforcement) | **Enforce** **lane** **scope** on **PRs** | **Label** **substitution** for **companion** **intent** | **Matches** **declared** **lane** **vs** **paths**. |
| [lane-pr-hint.yml](../../.github/workflows/lane-pr-hint.yml) | Workflow | R2 (comment helper) | **Suggest** **lane** **label** **comment** | **Set** **merge** **or** **approve** | Deterministic **PR** **comment** **hint**; same *family* as R2 **Cursor** **onboarding** **(narration** **only**). |
| [pages.yml](../../.github/workflows/pages.yml) | Workflow | R1 (build) + R4 (generate) + **external** side effect (deploy) | **Generate** **profile** + **deploy** **to** **Pages** on **`main` **path** **filters** | **Not** “optional** **Cursor**” **;** is **GHA** **product** | **Touched** **paths** include [users/grace-mar/**](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/pages.yml) **;** **deploy** **is** **repo** **policy** **(see** [policy](automation-readiness-policy.md#surfaces-who-runs-what-unattended)). |
| [deploy-profile.yml](../../.github/workflows/deploy-profile.yml) | Workflow | R1 + R4 + **publish** (similar) | **Build** + **upload** + **Pages** for **grace-mar.com** | **Same** as **pages** row | **Parallel** / **CNAME**-aware **deploy**; **classify** **as** **CI** **,** not **Cursor** **. |

---

## Cursor Automation candidates (prompt pack)

*See [trigger map](cursor-automations.md#trigger-map), [README](README.md), and guides in this directory.*

| Surface | Type | Class | Allowed unattended | Prohibited unattended | Reason |
| --- | --- | --- | --- | --- | --- |
| CI failure triage | Cursor prompt + guide | R2 | **One** **PR** **or** **check** **comment** **(triage** **text**)** | **Fix** **commits** **,** **push** **,** **protected** **edits** | [cursor-ci-failure-triage.md](cursor-ci-failure-triage.md) **(pass/fail** **stays** **in** GHA**).** |
| PR onboarding | Cursor | R2 | **PR** **comment** **(briefing** **)** | **Set** **labels** **,** **merge** | [cursor-pr-onboarding.md](cursor-pr-onboarding.md) **(lane** **enforcement** **is** [lane-scope](../../.github/workflows/lane-scope.yml)). |
| Weekly integrity summary | Cursor | R1 / R2 | R1: read-only `validate-integrity` / `governance_checker` in **sandbox** when **allowed**; R2: **summary** to **Slack** **(no** **file** **writes**)** | **regen** **,** **build_library_index** **,** **commit** | [cursor-integrity-summary.md](cursor-integrity-summary.md) **(report** **only**). **Max** is **R2** **(output** **channel**), **not** **R4** **. |
| Gate queue nudge | Cursor | R1 / R2 with **R5** boundary | **Read-only** **excerpt** **;** **nudge** **text** | **Applies** **candidates** **,** **edits** **gate** **content** for **decisions** | [prompts/cursor-gate-queue-nudge.md](prompts/cursor-gate-queue-nudge.md) **(decisions** **=** R5**).** |
| Cold re-entry nudge (candidate) | Not in prompt pack (hypothetical) | R2 | **Summary** **/ **suggestion** **to** **operator** **only** | **Substitute** for **operator** **read** of **`bridge`** / **re-entry** | **Narration** only **(if** **added** **later** **);** **compare** [operator_reentry_stack.py](../../scripts/operator_reentry_stack.py). |
| “Auto-fix” PR bot (candidate) | Hypothetical | **≤** R3 (draft) | **Open** / **suggest** **draft** **PR** | **Direct** **mutations** to **protected** **paths** **,** **or** R5 without human | [policy](automation-readiness-policy.md#readiness-classes-r0r5) R3; **default** down **,** not **R4** on **self** / **gate** **. |

---

## Maintenance

- When you add a workflow under `.github/workflows/`, add or update a row in **GitHub Actions workflows (complete set)**.
- When you add a new Cursor paste prompt, add a row under **Cursor Automation candidates** (or run the [classification template](automation-classification-template.md) first).
- Re-read [automation-readiness-policy.md](automation-readiness-policy.md) after any authority-relevant change to [AGENTS.md](../../AGENTS.md) or the [safe automation contract](cursor-safe-automation-contract.md).

**Last reconciled (workflow count):** 12 workflow files in [`.github/workflows/`](../../.github/workflows/) (verify at merge time; update this doc if a workflow is added or removed).
