# Known-path workflow fitness test

**Purpose:** Checklist for deciding whether a recurring Grace-Mar process is eligible for **known-path** treatment (documented assistance within explicit authority), versus staying **manual**, **narrower**, or **open-ended**.

**Not a merge gate:** Passing this test does **not** approve Record changes or add surfaces to [`config/authority-map.json`](../../../config/authority-map.json).

---

## Fitness test summary

Answer the **required questions** below. If **any** required answer is “no” or unknown, the workflow is **not** eligible as a full known-path workflow until scope is tightened. Then apply **disqualifiers** and **checks**. End with a **final classification**.

---

## Required questions

### 1. Repetition

- Does this workflow recur **daily**, **weekly**, **monthly**, or in response to a **recognizable event** (same class of trigger each time)?

### 2. Stable input

- Are **input surfaces** known?
- Can the workflow name **exactly** which files, folders, artifacts, inboxes, or runtime surfaces it **reads**?

### 3. Stable output

- Does the workflow produce a **predictable output type** (e.g. “draft markdown in path X”, “candidate block for recursion-gate”, “receipt JSON”)?
- Can a **human** distinguish a **good** output from a **bad** output using criteria written in the workflow doc?

### 4. Known reviewer

- **Who** reviews the output?
- Is there a **named human** or **explicit role** (e.g. “operator”, “companion”) responsible for **final judgment**?

### 5. Authority class

- Is **`authority_class`** one of: `read_only`, `draftable`, `review_required`, `human_only`, `ephemeral_only` (see [authority map](../../authority-map.md))?
- What is the **maximum action** the workflow may take (one clear sentence)?

### 6. No durable bypass

- Does the workflow **preserve** [recursion-gate](../../../users/grace-mar/recursion-gate.md) and Record boundaries?
- Does it **avoid** writing directly to **canonical** SELF, EVIDENCE, SKILLS, prompt, or merging candidates without **human approval** and the **documented merge path**?

### 7. Load-lift

- What **manual work** does it reduce (minutes or concrete steps)?
- How will **review burden** be measured (time box, checklist depth, spot-check rate)?
- Would the **operator miss** this workflow if it were disabled for a week?

### 8. Failure visibility

- Are **errors** obvious within **one run** or **one review cycle**?
- Can **missed signals**, **false promotions**, or **bad summaries** be detected before they hit canonical state?

---

## Disqualifiers

If **any** of these apply, the workflow is **not** eligible as a known-path workflow (at most: manual checklist or needs narrower scope):

- **Open-ended strategy generation** without stable output shape.
- **Long-horizon autonomous operation** (runs unattended across days without human checkpoints).
- **Durable Record writes** without human approval and the normal merge pipeline.
- **Ambiguous ownership** (no named reviewer).
- **Unknown or drifting input surfaces** (“whatever is in the repo”).
- **No measurable review burden** estimate (cannot do load-lift).
- **No clear good/bad output** standard.
- **Sensitive connector or repo access** without an explicit **maximum_action** and authority alignment.

---

## Authority check

- Cross-check **`authority_class`** and **`maximum_action`** with [authority map](../../authority-map.md) and, for concrete paths, `python3 scripts/check-authority.py --surface <key> --json` when a surface key exists.
- If the workflow touches multiple surfaces, list **each** and the **strictest** class that applies.

---

## Load-lift check

- **Manual time saved** per run (or per week): documented number or range.
- **Review time** expected: documented.
- **Acceptable if:** inequality “saved ≥ review + coordination overhead” or explicit operator exception (documented).
- **Retire if:** false positives, review fatigue, or drift in inputs/outputs.
- After a pilot or when comparing runs, optionally record a [Load-Lift Receipt](load-lift-receipts.md) (time fields + `decision`); not required for a **paper** fitness test, **recommended** before `status: active`.

---

## Reviewer check

- Reviewer name or role is **in the workflow doc**.
- Escalation path exists if the reviewer is unavailable (e.g. “defer run”, not “auto-approve”).

---

## Output check

- Output **path or artifact type** is fixed in the doc.
- **Good / bad** examples or a short rubric exist (can be in “Example run” section).

---

## Promotion check

- **Promotion** to Record or prompt is **explicitly** via existing gate + merge steps ([AGENTS.md](../../../AGENTS.md)); the workflow does not define a shortcut.

---

## Final classification

Pick **one**:

| Classification | Meaning |
|----------------|--------|
| **Eligible: known-path workflow** | All required questions satisfied; no disqualifiers; ready to register with `status: proposed` or `active`. |
| **Eligible only as manual checklist** | Useful discipline doc; inputs/outputs not stable enough for semi-automation. |
| **Needs narrower scope** | Partial fit; tighten inputs, outputs, or reviewer before re-testing. |
| **Not eligible: open-ended reasoning or judgment-heavy work** | Keep out of known-path registry until the work can be bounded. |

---

## Checklist (compact)

**A workflow is eligible only if all of the following are true:**

1. **Repetition:** Recurs on a defined cadence or recognizable event.
2. **Stable input:** Input surfaces are known and nameable.
3. **Stable output:** Predictable output type; human can judge good vs bad.
4. **Known reviewer:** Named human or role for final judgment.
5. **Authority class:** One of `read_only`, `draftable`, `review_required`, `human_only`, `ephemeral_only`; **maximum_action** stated.
6. **No durable bypass:** Preserves recursion-gate and Record boundaries; no direct canonical writes.
7. **Load-lift:** Manual reduction and review burden estimated; operator would miss it if valuable.
8. **Failure visibility:** Errors and bad outputs detectable within one run or review cycle.

Then confirm **no disqualifiers** and assign a **final classification** above.
