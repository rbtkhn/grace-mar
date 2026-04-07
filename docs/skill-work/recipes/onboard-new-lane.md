# Recipe: Onboard New Lane

**Trigger:** `onboard [lane-name]` or "new lane" before creating a work territory.

**Purpose:** Sequence three existing skills into a single workflow that takes a new lane from landscape scan to clean first commit. This is a composition recipe — it defines ordering and handoffs, not new behavior.

---

## Sequence

```
lane-survey  -->  work-template checklist  -->  repo-hygiene-pass
(landscape)       (create files)                (clean commit)
```

### Step 1: Lane Survey

Run `.cursor/skills/lane-survey/SKILL.md` with the lane name.

**Input:** Operator's stated objective for the lane.
**Output:** `docs/skill-work/work-[lane]/SURVEY_[lane].md` — landscape summary, key tools, gaps, recommendations.

**Skip when:** The domain is well-known to the operator and no external tooling is relevant.

**Done when:** Survey doc exists (or skip is explicitly acknowledged).

### Step 2: Work-Template Checklist

Follow `docs/skill-work/work-template.md` — the standard lane creation checklist.

**Input:** Survey output informs the README's Objective and Boundary sections.
**Output:** README, history file, territory registration, history registration.

**Handoff from Step 1:** Survey recommendations feed into the README's cross-links and the Boundary section's "adopt vs build" framing.

**Done when:** All four required artifacts exist and the territory is registered.

### Step 3: Repo Hygiene Pass

Run `.cursor/skills/repo-hygiene-pass/SKILL.md` to split the new files into a clean commit.

**Input:** The files created in Step 2.
**Output:** One focused commit with the new lane scaffolding.

**Done when:** Commit is clean, no scratch noise included, `git status` is tidy.

---

## Skip rules

| Condition | What to skip |
|-----------|-------------|
| Domain is well-known, no tooling landscape | Skip Step 1 (survey) |
| Lane already has scaffolding files | Skip Step 2, go to hygiene |
| Only one or two files changed | Hygiene pass is optional |

## Done when (whole recipe)

The lane has a survey (or acknowledged skip), all required scaffolding files, territory registration, and a clean commit. The operator can start working in the lane immediately.

---

## Related

- `.cursor/skills/lane-survey/SKILL.md`
- `docs/skill-work/work-template.md`
- `.cursor/skills/repo-hygiene-pass/SKILL.md`
