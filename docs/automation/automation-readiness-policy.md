# Automation Readiness Policy

**Status:** **WORK** documentation. This policy defines **readiness classes (R0–R5)** for scripts, cadence rituals, GitHub Actions, and product automations. It is **advisory** until a specific workflow or prompt explicitly incorporates it. **Not** a substitute for [AGENTS.md](../../AGENTS.md) or [instance-doctrine.md](../../users/grace-mar/instance-doctrine.md).

**Related:** [automation-readiness-ledger.md](automation-readiness-ledger.md) (current surfaces) · [automation-classification-template.md](automation-classification-template.md) (proposals).

---

## Core principle

**Automate visibility before action; automate action only after authority is explicit.**

That aligns with the prompt-pack line **“Automate visibility, not authority”** in [README.md](README.md) and the **routing layer** rule in [AGENTS.md](../../AGENTS.md): assistants and automation are limited to the **routing** layer unless a **human** explicitly runs a merge (e.g. `process_approved_candidates.py`).

---

<a id="readiness-classes-r0r5"></a>

## Readiness classes (R0–R5)

`R` stands for **readiness** (and mirrors **R**eport / **R**itual thinking without using “A” levels).

| Class | Name | Meaning | Allowed **unattended** behavior | Disallowed behavior |
| --- | --- | --- | --- | --- |
| **R0** | Human ritual | Human/operator **ritual** that must **not** be replaced by automation | **None** for ritual completion, **or** read-only **prep** only if a policy explicitly allows | Substitution, “ritual **done**” framing, autonomous completion |
| **R1** | Read-only diagnostic | Safe to run or summarize when **output-only**; no **authority** | Inspect, run **read-only** checks, **summarize** logs | **Mutate** files, **commit**, **approve** authority-bearing actions |
| **R2** | Comment / nudge | May produce **external-facing** text (comments, Slack, report channels) | **PR** / **issue** / **Slack** **narration**; triage text | **Push**, **label**, **approve**, **edits** to repo **files** |
| **R3** | Draft proposal | May create **draft** branches, issues, or PRs for **human** review | **Draft-only** proposals (operator merges or closes) | **Direct** **merge**, **protected-path** **edits** without review |
| **R4** | Derived-artifact mutation | May **regenerate** **non-Record** **derived** **artifacts** only under **narrow** **policy** (operator-run or **repo-approved** CI) | **Regen** of **allowed** **generated** **files** (manifest, bundles, index, **non-Record** **exports**) | **Record** / **gate** / **prompt** / **session** **canonical** **edits**; **invented** regen in **Cursor** **without** **policy** |
| **R5** | Human authority boundary | **Merge**, **gate** **decisions**, **companion** **approval** | **None** **unattended** | **Approval**, **merge**, **gate** **processing** **(incl. `process_approved_candidates.py --apply`)** **without** **explicit** **human** **action** on **trusted** **path** |

**R5** **always** **overrides** **lower** **classes** for the **same** **surface**: if a **surface** **touches** **Record** / **merge** / **gate** **decision**, the **max** **unattended** **class** is **R5** **unless** a **later** **signed** **policy** **carves** a **narrow** **exception** (this repo **defaults** to **no** such **carve** for **merges**).

**Dual** **class** **notation:** When a **ritual** **has** a **read-only** **check** (e.g. **dream** **with** **preflight**), write **R0** **(ritual) / R1 (preflight only)** and **one** **sentence** **scope** **—** e.g. “R1 **only** = **read-only** **summary**; **R0** = **operator** **closure** **and** **voice**.”

**If** **classification** **is** **uncertain**, **default** **downward** **toward** **less** **authority** (treat as **R1** or **R2** **text-only**, **not** **R4** / **R5**).

---

<a id="surfaces-who-runs-what-unattended"></a>

## Surfaces: who runs what (“unattended” is not one thing)

**Unattended** **means** **different** **things** **by** **surface:**

| Surface | Who runs it | How R-classes apply |
| --- | --- | --- |
| **Local / operator** | Human **invokes** **scripts** **or** **IDE** **agents** | **R**-class = **max** **authority** for **that** **invocation** in **this** **repo** (e.g. **R4** **regen** only when the **operator** **chooses** to **run** **regen**). |
| **GitHub CI** (`.github/workflows/`) | **Repo-defined** **triggers** on **PR** / **push**; **deterministic** | R-class = **gravity** of effect (check vs regen job). R1 enforcement is not a Cursor “bot” and does not substitute for R0 rituals. Deploy (e.g. Pages) is **in-repo** policy already: classify in the [ledger](automation-readiness-ledger.md) as a **CI role**, not an optional product toggle in Cursor. |
| **Cursor** / **other** **cloud** **agents** | **Operator-configured** **prompts**; **read**-mostly | **R2** is the **typical** **ceiling** for **comments**; **R1** for **read-only** **summary**; **never** **R4** **regen** **or** **R5** **merge** per [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md). |

**GitHub** **Actions** **on** `main` **are** “unattended” **in** the **product** **sense**; **that** is **separate** from **whether** a **Cursor** **Automation** may **acquire** the **same** **authority** **—** it **may** **not** **replicate** **merge** **or** **Record** **writes**.

---

## Authority rules (concrete)

1. **R5** **wins** over **R0–R4** when **merges**, **approvals**, **or** **gate** **queue** **mutations** are **in** **scope** for the **automation** **or** **script** run.
2. **Any** **surface** **that** **writes** or **approves** **edits** to `users/**/self.md`, `self-archive.md`, `recursion-gate.md` (**as** **content** **changes**), `session-log.md`, `bot/prompt.py`, or **Record** / **EVIDENCE** **canonical** **paths** is **R5** **unless** a **specific** **companion**-**reviewed** **repo** **policy** **says** **otherwise** (default: **R5**).
3. **Staging** **candidates** **from** **untrusted** **PR** / **issue** **text** is **prohibited** **(R5** **/ blocked)** **unless** a **future** **policy** **allows** a **restricted** **pattern** (current **default: blocked**; see [contract](cursor-safe-automation-contract.md) §4–5).
4. **Automation** using **untrusted** text must **not** persist it in product **memory** or durable state (see [contract](cursor-safe-automation-contract.md) §10).
5. **Ritual** **names** (`coffee`, `dream`, `bridge`, **Steward**, **gate** **completion**): **automation** **output** **must** **not** **claim** the **ritual** **was** **performed** **by** the **bot** **unless** the **human** **actually** **did** **—** [contract](cursor-safe-automation-contract.md) §5.

---

## Relationship to the safe automation **contract**

| Artifact | Role |
| --- | --- |
| [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) | **Paste** into Cursor Automation prompts; concrete **do / don’t** for the model in that product. |
| **This** **policy** + [ledger](automation-readiness-ledger.md) | **Classification** **SSOT** for **what** **may** **be** **built** **and** **what** **max** **R**-**class** **applies**; **advisory** **until** **a** **workflow** **references** **it**. |

**Flow:** new **idea** → [template](automation-classification-template.md) → **assign** **R0–R5** **with** **surface** **context** → **confirm** **against** **this** **policy** → **implement** **prompt** or **CI** **within** **bounds**; **deterministic** **CI** **still** **owns** **pass**/**fail** for **the** **checks** it **runs**.

---

## Applicability: modes and routing (pointers)

- **[AGENTS.md](../../AGENTS.md)** — **Routing** **layer** **vs** **merge** **authority**; **four** **modes** **summary**; **skill** / **conductor** **pointers**.
- **[instance-doctrine.md](../../users/grace-mar/instance-doctrine.md)** — **Instance** **modes** **(Session** / **Pipeline** / **Query** / **Maintenance)**, **file** **update** **protocol**, **merge** **only** **via** **approved** **path** **when** **operator** **runs** **it**.

---

## See also

- [automation-readiness-ledger.md](automation-readiness-ledger.md) — table of current surfaces
- [automation-classification-template.md](automation-classification-template.md) — form for new automation candidates
- [README.md](README.md) — index (including [§ Automation readiness](README.md#automation-readiness))
- [cursor-automations.md](cursor-automations.md) — Cursor trigger map
