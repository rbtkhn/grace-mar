# Seed Phase — Survey prompts

**Companion-Self template · Intake copy**

Operators use these prompts to collect answers that map into seed-phase JSON artifacts. This doc is **not** the live Record.

**New to roles, the gate, or the triad?** Read [start-here.md](start-here.md) first—including **[Choose your path](start-here.md#choose-your-path)** (A–F)—then return here to capture answers.

See [seed-phase-artifacts.md](seed-phase-artifacts.md) for the file layout and [seed-phase.md](seed-phase.md) for the protocol.

<a id="calibrate-from-your-start-here-path"></a>

## Calibrate from your start-here path

Use this table after you pick **A–F** on [start-here — Choose your path](start-here.md#choose-your-path). These hints **only** shape how you read and prioritize questions; they do **not** change JSON schemas, required artifacts, or validation.

| Pick | Who | How to use this survey |
|------|-----|-------------------------|
| **A** | Companion | Normally you complete this **with** your operator. Focus free text on **comfort, boundaries, and topics to avoid** (maps well to `important_constraints` and `notes`). Let the operator handle enum fields and file names—you sanity-check meaning, not syntax. |
| **B** | Parent or guardian | Read **[work-dev](#work-dev-seed-survey)** Q9–10 and **[work-business](#work-business-seed-survey)** Q9 **first** as guardrail prompts. The operator transcribes into JSON; you align on **who approves**, **who has repo access**, and **what must not be implied** about the companion. Skim the rest only if the companion has real dev or business exposure. |
| **C** | Operator | **Default path:** work through **[work-dev](#work-dev-seed-survey)** and **[work-business](#work-business-seed-survey)** as the instance needs. If **time-boxed**: do **work-dev** first when the fork is dev-heavy; **work-business** first when commerce is central. Always fill **`important_constraints`** (and equivalents) in each section you use. |
| **D** | Technical contributor | Prioritize **work-dev** with **strict** enum mapping per the tables. For **work-business**: at minimum Q1 (`business_involvement`), Q9 (constraints), Q10 (focuses); expand the full block unless `business_involvement` is `none`. |
| **E** | Curious visitor | **Skip this file** unless you step into an operator role. Concepts live on [start-here](start-here.md) and [conceptual-framework.md](conceptual-framework.md). |
| **F** | Journalist / blogger | **Not interview copy.** Do not publish answers or infer private facts without **operator and companion** consent. Use [start-here door F](start-here.md#door-f) and cited links there; treat this doc as **internal formation** only. |

**Combos:** **B then C** — apply row **B**, then row **C** for capture order. **C with D** — follow **C** ordering; apply **D** enum discipline on work-dev.

**Optional artifact field:** When you create or update **`seed_intake.json`**, you may set **`start_here_pick`** to **`A`**–**`F`** to record which path was chosen (reproducibility for operators and tooling). It is **not** companion identity data—omit the key if unknown.

### Optional cadence ritual metadata

If the instance uses a cadence ritual for re-entry or orientation, you may also record optional **`cadence_preference`** metadata in **`seed_intake.json`**.

- Default trigger word: **`coffee`**
- Recommended timing: **do not** ask the new user to rename it during first-contact intake
- Better rule: offer renaming **later**, after the ritual has proven useful across several successful uses
- This is **operator UX metadata**, not Record truth

Recommended default policy block:

```json
"cadence_preference": {
  "default_trigger_word": "coffee",
  "active_trigger_word": "coffee",
  "word_source": "default",
  "personalization_timing": "post_adoption_optional",
  "rename_offer": {
    "status": "not_yet_eligible",
    "offer_after_successful_uses": 3,
    "offer_after_distinct_days": 2,
    "minimum_successful_followthrough_uses": 2,
    "snooze_days": 14
  }
}
```

Suggested user-facing copy when the instance becomes eligible later:

- `You've used 'coffee' a few times now. Want to keep it, or switch to a cadence word that fits you better?`
- Choices: **Keep coffee** / **Choose a new word** / **Not now**

---

## work-dev seed survey

Answers feed **`work_dev_seed.json`** (validated by **`schema-registry/work-dev-seed.v1.json`**). Map free-text lists into JSON arrays; use the schema enums for single-choice fields.

**Mapping hints**

| Question theme | JSON field | Enum / shape |
|----------------|------------|----------------|
| Involvement level | `development_involvement` | `none`, `light`, `regular`, `core` |
| Role modes | `development_role_modes` | `builder`, `architect`, `debugger`, `reviewer`, `researcher`, `integrator`, `other` (array, unique) |
| Work kinds | `work_modes` | `feature_design`, `implementation`, `debugging`, `architecture`, `refactoring`, `documentation`, `integration`, `research`, `code_review`, `other` (array, unique) |
| Companion help | `companion_help_priorities` | `brainstorming`, `planning`, `code_generation`, `review_and_critique`, `debugging`, `architecture_mapping`, `repo_audits`, `prioritization`, `technical_writing`, `other` (array, unique) |

1. Do you do software development or technical systems work?
   - Maps to `development_involvement`: no → `none`; occasionally → `light`; regularly → `regular`; major part of work → `core`.

2. Which of these best describe your development role? (multi-select)
   - builder / implementer → `builder`
   - architect / planner → `architect`
   - debugger / fixer → `debugger`
   - reviewer / auditor → `reviewer`
   - researcher / explorer → `researcher`
   - product / systems integrator → `integrator`
   - other (specify in `notes`)

3. What repositories, products, or systems are most important to your development work right now?
   - `primary_repos` and/or `systems_or_products` (string arrays).

4. Which languages or stacks do you actively use or care about?
   - `preferred_languages` (string array).

5. Which tools do you prefer for development work?
   - `preferred_tools` (string array).

6. What kinds of development work do you most often do? (multi-select)
   - Align labels with `work_modes` enum values above.

7. What kind of technical help do you want this companion to be best at? (multi-select)
   - Align labels with `companion_help_priorities` enum values above.

8. Are there any repositories, systems, languages, or workflows this companion should treat as especially important?
   - `active_focuses` and/or repeat structured fields as needed.

9. Are there any development preferences or constraints this companion should avoid violating?
   - `important_constraints` (string array).

10. Is development work central to this companion, secondary, or mostly absent?
    - Cross-check `development_involvement` and summarize in `notes` if nuance is needed.

After capture, set `evidence_basis` to `seed_survey` when answers are survey-driven; use `explicit_user_input` for direct statements only; `mixed` when both apply. Leave `none` only while no evidence is recorded yet.

---

## work-business seed survey

Answers feed **`work_business_seed.json`** (validated by **`schema-registry/work-business-seed.v1.json`**). Map free-text lists into JSON arrays; use the schema enums for single-choice and multi-select fields.

**Mapping hints**

| Question theme | JSON field | Enum / shape |
|----------------|------------|----------------|
| Involvement | `business_involvement` | `none`, `light`, `regular`, `core` |
| Role modes | `business_role_modes` | `founder`, `operator`, `investor`, `advisor`, `employee`, `side_project`, `student_entrepreneur`, `researcher_commercial`, `other` (array, unique) |
| Commerce surfaces | `commerce_surfaces` | `none`, `etsy_or_marketplace`, `saas`, `consulting_services`, `content_or_media`, `nonprofit_earned_revenue`, `physical_goods`, `other` (array, unique) |
| Activity kinds | `business_activity_modes` | `market_research`, `competitive_analysis`, `positioning`, `fundraising`, `partnerships`, `operations`, `sales`, `product_strategy`, `content_marketing`, `regulatory_compliance`, `ecommerce_ops`, `other` (array, unique) |
| Companion help | `companion_help_priorities` | `brainstorming`, `planning`, `market_research`, `positioning`, `pitch_review`, `partnership_mapping`, `prioritization`, `business_writing`, `ecommerce_ops`, `competitive_intel`, `other` (array, unique) |

1. Do you run or plan to run a business, side project, or commercial activity?
   - Maps to `business_involvement`: no → `none`; occasional → `light`; regular → `regular`; central to life → `core`.

2. Which roles fit you? (multi-select)
   - founder, operator, investor, advisor, employee, side project, student entrepreneur, commercial researcher, other (note in `notes`).

3. What ventures, brands, or offerings matter most right now?
   - `primary_ventures_or_brands` (string array).

4. Which markets or sectors are you in or watching?
   - `markets_or_sectors` (string array).

5. How do you sell or earn revenue (if at all)?
   - Map to `commerce_surfaces` (Etsy/marketplace, SaaS, consulting, content, nonprofit earned revenue, physical goods, none, other).

6. What kinds of business work do you do most often? (multi-select)
   - Align with `business_activity_modes` above.

7. What commercial or market topics should this companion help you research or think through?
   - `research_or_interest_areas` (string array).

8. What should the companion prioritize when helping with business questions? (multi-select)
   - Align with `companion_help_priorities` above.

9. What business topics, claims, or activities should the companion **avoid** or treat carefully (compliance, privacy, no financial advice, etc.)?
   - `important_constraints` (string array).

10. What are your top 1–3 business focuses for the next few months?
    - `active_focuses` (string array).

After capture, set `evidence_basis` to `seed_survey` when answers are survey-driven; `explicit_user_input` for direct statements only; `mixed` when both apply. Leave `none` only while no evidence is recorded yet.
