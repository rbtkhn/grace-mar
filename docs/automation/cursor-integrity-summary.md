# Cursor Weekly Integrity Summary

**Status:** **WORK** documentation. **Not** a scheduled job in this repo, **not** a [GitHub Action](https://github.com/rbtkhn/grace-mar/tree/main/.github/workflows), **not** a live [Cursor Automation](https://cursor.com/docs/cloud-agent/automations) until the **operator** enables it in the Cursor product. **Doctrine:** [AGENTS.md](../../AGENTS.md) · [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md).

**Critical risk to avoid:** A **read-only** summary must **not** run **`bash scripts/regen_grace_mar_derived.sh`** or any command that **writes** derived **artifacts** in the **cloud** run—those are **for the operator** on a **trusted** **machine** only. Suggest, never execute regen in the automation.

---

## Purpose

A **weekly** (or **manual**) **read-only** **clerk** **summarizes** **integrity** and **derived**-**export** **drift** and lists **operator**-**runnable** **commands**—it does **not** **regenerate**, **commit**, **fix** branches, or **merge**.

**Core line:** **Integrity scripts identify drift; Cursor Automation summarizes what the operator should inspect next.**

**Clarify:**

- **Not** a second **CI** system ([test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) / [governance.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/governance.yml) own pass/fail).
- **Not** a **regeneration** bot; **regen** and any script that **writes** derived **artifacts** (including **library** **index** **regen**) is **operator**-**only** (see [work-cadence — stale derived](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports)).
- **Not** a **gate** **processor** and **not** a substitute for **human** cadence: do **not** **frame** this **output** as `coffee`, `dream`, `bridge`, **Steward**, or **gate** **review** **completion** — it is a **read-only** **integrity** **report** only.

**Paste prompt (procedure + identity):** [prompts/cursor-integrity-summary.md](prompts/cursor-integrity-summary.md). **Canonical report template:** [## Output report format (canonical)](#output-report-format-canonical) below.

---

## Recommended trigger (Cursor product)

| Setting | Suggestion |
|---------|------------|
| **Event** | **Schedule** (e.g. **weekly**) **or** **manual** run in Cursor |
| **Destination** | **Slack**, **email**, **automation** **summary** panel, or **one** **issue** **body** the operator opts into — **not** a default new issue unless configured |
| **Frequency** | **One** **concise** **weekly** report; **avoid** high-frequency runs that become **noise** (unless **debugging** the prompt) |

**Suggested** **cadence:** **Monday** **morning** (or the operator’s fixed **review** **window**). **Do** **not** run **many** **times** **per** **day** in production.

---

## Allowed behavior

- **In** a **cloud** run, **if** the **sandbox** **allows** **non-mutating** **Python** **invocations**, prefer **`python3 scripts/validate-integrity.py --user grace-mar --json`** (or **`--require-proposal-class`** to **mirror** [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml)) and **`python3 scripts/governance_checker.py`** — both are **read-only** **introspection** in normal use. **Do** **not** run **`bash scripts/regen_grace_mar_derived.sh`**, **`python3 scripts/build_library_index.py`**, or **any** **command** that **writes** **repo** **files** or **refreshes** **exports**. **If** the **cloud** **cannot** run **Python**, **rely** on **pasted** **log** **excerpts** or **mark** **uncertain** (**CI** still **owns** **deterministic** pass/fail on `main`).
- **Prefer** **summarizing** **pasted** **output** from the **operator** if the **sandbox** **cannot** run **Python** or **lacks** the **full** **repo** **context**.
- **List** **drift** **classes** (manifest, **PRP** / `grace-mar-llm.txt`, **runtime** **bundle**, **library** **index**, etc.) using **only** text **from** the **tool** / **pasted** log.
- **Suggest** up to **three** **local** **commands** the **operator** can **run**; phrase as **“consider running locally”** — the **automation** does **not** **claim** to have run **regen** or **any** **write**-**heavy** **step**.
- **Mark** **uncertain** when logs are **incomplete** or a **path** is **unclear**.

## Prohibited behavior

- **No** `git` **commit**, **push**, or **branch** **create**.
- **No** **in-repo** **file** **edits** (including `users/**`, `bot/prompt.py`, `grace-mar-llm.txt`, manifest, **bundle** **JSON**).
- **No** `bash scripts/regen_grace_mar_derived.sh` (or any **regen** / **export** **that** **writes** **artifacts**) **from** the **automation** **run** — **suggest** **to** the **operator** only.
- **No** `process_approved_candidates.py` (any **mode**); **no** **`CANDIDATE-*`** **changes**; **no** **edits** to **`recursion-gate.md`** (this is **not** the [gate queue nudge](prompts/cursor-gate-queue-nudge.md) prompt).
- **No** **mutating** **shell** **commands** in the **cloud** **environment** **unless** a **future** allowlist **explicitly** **permits** **only** true **read-only** **introspection**.
- **No** **product** **memory** for **logs** / **private** **repo** **content** (see [contract](cursor-safe-automation-contract.md) § 10).
- **No** **ritual** **language** (`coffee` **completion**, `dream` **as** this **bot**, `bridge` **as** this **output**, **Steward** / **gate** **review** **completion**).

**Do** **not** **invent** **scripts** that **are** **not** in `scripts/` **or** **documented** in **this** **repo** — if **unknown**, say **so**.

---

## Integrity classes (heuristics for classification)

| Class | Signals | First place to inspect | Human: consider (only if present in repo / CI) |
| --- | --- | --- | --- |
| **Integrity validation** | `validate-integrity` **failure**; JSON / text lists stale paths | [validate-integrity.py](https://github.com/rbtkhn/grace-mar/blob/main/scripts/validate-integrity.py) **output** | `python3 scripts/validate-integrity.py --user grace-mar --require-proposal-class` (matches [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) step) or `--json` for readout ([work-cadence](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports)) |
| **Derived** **artifact** **drift** | manifest, **fork**-**manifest**, **llms.txt**, **runtime** **bundle** vs **sources** | [work-cadence — When integrity reports](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports) | **After** **operator** **readiness:** `bash scripts/regen_grace_mar_derived.sh` **then** re-**validate** — **automation** **never** runs **regen** |
| **Library** **index** **drift** | CI: `build_library_index` **diff** | [library-index workflow](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/library-index.yml) | `python3 scripts/build_library_index.py -u grace-mar` (then `git diff` if needed — **operator** only) |
| **Prompt** / **PRP** **drift** | `grace-mar-llm.txt` or **export** **stale** vs **self** / **prompt** | [Regen script order in work-cadence](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports) | Same **regen** **path** as **row** 2; **automation** **suggests** only |
| **Strategy** / **history** **validation** | Failing **step** in [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) (notebook checks) | **Log** path / **script** name | **Rerun** the **exact** `python3 scripts/...` from the **failing** **CI** **step** **locally** |
| **Governance** | `governance_checker.py` / **governance** **job** | Output message | `python3 scripts/governance_checker.py` (or `python` as on your PATH) |
| **Unknown** | Ambiguous or **missing** log | **Latest** **CI** / **local** run | “**Uncertain** — **paste** `validate-integrity` **or** **ask** **operator**” |

*Reconcile this table with workflows when [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) **changes**.*

---

<a id="output-report-format-canonical"></a>

## Output report format (canonical)

The paste prompt must **reproduce** **this** **structure** **exactly** (headings/labels; **fill** **values** only). **Do** **not** **nest** **broken** **code** **fences** in **actual** **output**; use **one** `bash` **block** for **commands** and **separate** **lines** for **Notes** and **Boundary**.

```markdown
### Weekly integrity summary

**Status:**  
**Likely drift class:**  
**Files/artifacts to inspect:**  
**Suggested local commands:**

~~~bash
# command 1
# command 2
~~~

**Notes:**  

**Boundary note:** This is a read-only integrity report. It did not regenerate artifacts, commit files, edit Record/gate/prompt/session surfaces, or process the gate.
```

*(Use `~~~` or editor-safe fences so inner \`\`\` does not break rendering; the automation’s **real** **output** may use standard \`\`\`bash if unambiguous.)*

---

## Operator setup

1. Read [cursor-safe-automation-contract.md](cursor-safe-automation-contract.md) and prepend or link it in the Cursor prompt.
2. Paste [prompts/cursor-integrity-summary.md](prompts/cursor-integrity-summary.md) into [Cursor Automations](https://cursor.com/docs/cloud-agent/automations).
3. **Schedule** **weekly** (or **manual** only); set **output** to **Slack** / **summary** as appropriate; **default** to **not** **auto-creating** **issues** **or** **PRs**.
4. **Keep** **regen** and **any** **commit** **off** the **automation** **allowlist** **unless** you **intentionally** **expand** policy **later**.

**See also:** [README — Weekly integrity summary](README.md#weekly-integrity-summary) · [cursor-automations — Trigger map](cursor-automations.md#trigger-map)

**Maintenance:** *Last reviewed: 2026-04* — realign with [work-cadence](https://github.com/rbtkhn/grace-mar/blob/main/docs/skill-work/work-cadence/README.md#when-integrity-reports-stale-derived-exports) and [test.yml](https://github.com/rbtkhn/grace-mar/blob/main/.github/workflows/test.yml) when they change.
