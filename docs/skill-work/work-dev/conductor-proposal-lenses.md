# Conductor Proposal Lenses

**Scope:** WORK prompt convention — shapes **coding-agent proposals**, not Record merges.

---

## 1. Purpose

This file translates the five **conductor modes** into **coding-agent proposal discipline**. It helps prevent Grace-Mar PR prompts from flattening into the same generic structure regardless of the chosen conductor.

For **which document owns doctrine vs ritual vs routing**, see [`../work-coffee/CONDUCTOR-LAYER-MAP.md`](../work-coffee/CONDUCTOR-LAYER-MAP.md).

---

## 2. Core Rule

A **conductor lens** should change the **shape** of a coding proposal, **not merely its prose style**. It should influence **scope**, **non-goals**, **validation**, **file selection**, **acceptance criteria**, and **follow-up sequencing**.

---

## 3. Proposal Lens Template

Use this reusable block when stance selection helps:

```text
Conductor lens:
- Primary conductor:
- Proposal style:
- What this conductor emphasizes:
- What this conductor forbids:
- What would count as overreach:
- What evidence would show the PR succeeded:
```

**Explain:** This block may be inserted into coding-agent prompts when a Grace-Mar task benefits from explicit stance selection.

---

## 4. The Five Proposal Signatures

| Conductor | Proposal Signature | Best PR Types | Typical Artifacts | Main Risk |
|-----------|-------------------|---------------|-------------------|-----------|
| Toscanini | Validate, parse, enforce, test, clarify seams | schema validation, link checks, authority audits, parser fixes | tests, validators, strict docs, failure cases | becoming too brittle or over-enforcing |
| Furtwängler | Preserve ambiguity, expose tension, prefer warnings over premature closure | advisory reports, ambiguity maps, review packets, competing interpretations | tension registers, warning reports, side-by-side analyses | refusing necessary resolution |
| Bernstein | Improve operator comprehension, stakes, adoption, and live usability | onboarding docs, UX copy, error messages, executive summaries, operator prompts | vivid explanations, decision-oriented messages, “why this matters” sections | becoming ornamental prose |
| Karajan | Shape the whole system; improve balance, taxonomy, architecture, long-arc coherence | layer maps, registry cleanup, naming normalization, dashboard consolidation | taxonomies, relationship maps, coherence docs | over-polishing or over-architecting |
| Kleiber | Narrow ruthlessly; choose one hotspot; explicitly refuse excess | PR slicing, anti-sprawl, limited migrations, deferrals, deletion candidates | non-goal blocks, narrow diffs, “not this PR” sections | under-solving by refusing too much |

---

## 5. Conductor-Specific Prompt Blocks

Copy one block into the coding-agent prompt when that stance applies.

### Toscanini Prompt Block

```
Conductor lens: Toscanini
- Proposal style: verification-first, testable, seam-enforcing.
- Emphasize: parser validity, exact relative links, schema correctness, boundary clarity, binary acceptance criteria.
- Forbid: broad redesign, aesthetic rewrites, new doctrine without evidence, undocumented authority expansion.
- Overreach: adding new concepts instead of validating existing ones.
- Success evidence: invalid files fail loudly; links resolve; tests or parse checks prove the fix.
```

### Furtwängler Prompt Block

```
Conductor lens: Furtwängler
- Proposal style: tension-preserving, advisory, ambiguity-aware.
- Emphasize: competing interpretations, unresolved overlaps, warning states, review packets, human judgment.
- Forbid: premature consolidation, forced renaming, hard failures where ambiguity should remain visible.
- Overreach: resolving conceptual tension before evidence or operator review supports it.
- Success evidence: the human reviewer can see the live tension clearly and choose whether to resolve, watch, or defer.
```

### Bernstein Prompt Block

```
Conductor lens: Bernstein
- Proposal style: operator-legible, stakes-forward, adoption-oriented.
- Emphasize: vivid failure messages, clear next actions, onboarding, executive summaries, human-readable “why this matters.”
- Forbid: ornamental prose that does not improve operator action.
- Overreach: making documentation more dramatic without making the system easier to use.
- Success evidence: the operator understands what happened, why it matters, and what to do next.
```

### Karajan Prompt Block

```
Conductor lens: Karajan
- Proposal style: system-shaping, taxonomic, long-arc coherent.
- Emphasize: layer maps, surface registries, naming consistency, architectural balance, relationship tables.
- Forbid: local fixes that worsen the whole-system shape, duplicated taxonomies, dashboard sprawl.
- Overreach: over-architecting a small issue into a new subsystem.
- Success evidence: adjacent surfaces become easier to navigate and the whole system reads more coherently.
```

### Kleiber Prompt Block

```
Conductor lens: Kleiber
- Proposal style: narrow, selective, refusal-centered.
- Emphasize: one hotspot, small diff, explicit non-goals, deferral list, anti-sprawl, limited migration.
- Forbid: “while we’re here” expansion, repo-wide rewrites, new dashboards, broad migrations.
- Overreach: touching more files than necessary or converting a surgical PR into a program.
- Success evidence: the highest-value hotspot is improved without widening scope.
```

---

## 6. Same Problem, Five Different Proposals

### Example A — “Receipt taxonomy overlap”

**Toscanini**

**PR:** Validate receipt schemas and examples.

- Parse all receipt-like schemas.
- Check enum consistency.
- Validate examples.
- Fail on invalid JSON.
- Do not rename any receipt type.

**Furtwängler**

**PR:** Add advisory receipt-overlap map.

- Identify overlapping receipt purposes.
- Preserve unresolved tensions.
- Mark watch items.
- Do not consolidate yet.

**Bernstein**

**PR:** Improve receipt selection guidance for operators.

- Add “Which receipt should I use?” guide.
- Use plain language.
- Add examples.
- Improve operator confidence.

**Karajan**

**PR:** Add receipt taxonomy and relationship map.

- Define receipt classes.
- Clarify hierarchy.
- Align schema registry README.
- Link adjacent docs.

**Kleiber**

**PR:** Choose one receipt overlap to fix.

- Pick the highest-confusion pair.
- Clarify only that pair.
- Defer broader taxonomy.
- Add explicit non-goals.

### Example B — “Dashboard sprawl”

| Conductor | Proposal thrust |
|-----------|-------------------|
| Toscanini | Validate dashboard source/rebuild links and registration expectations. |
| Furtwängler | Map unresolved dashboard overlaps without merging them into one surface. |
| Bernstein | Improve operator-facing dashboard descriptions (“what this is for”). |
| Karajan | Create or extend an operator surface registry so dashboards sit in one coherent taxonomy. |
| Kleiber | Refuse new dashboard; add one registry row instead of a new surface family. |

---

## 7. How to Use in Coding-Agent Prompts

- Use a conductor lens when a task could be approached in **multiple legitimate ways**.
- Do **not** force a conductor lens onto trivial fixes.
- If the user says **“make it tighter,”** prefer **Kleiber**.
- If the user says **“verify,”** prefer **Toscanini**.
- If the user says **“what are the tensions,”** prefer **Furtwängler**.
- If the user says **“make it usable/clear for people,”** prefer **Bernstein**.
- If the user says **“make the system coherent,”** prefer **Karajan**.
- When uncertain, choose **Kleiber** for scope control or **Toscanini** for validation.

---

## 8. Appendix: Beethoven Test for Conductor Distinctiveness

### Purpose

The **Beethoven test** prevents the five conductors from flattening into decorative names for the same coding-agent proposal. Beethoven exposes each conductor’s approach to structure, time, energy, tension, and resolution. When two conductor lenses appear to produce the same PR, use the Beethoven test to recover the difference.

### Core Beethoven Distinctions

| Conductor | Beethoven Premise | Musical Signature | Coding-Agent Translation |
|-----------|-------------------|-------------------|---------------------------|
| Toscanini | Beethoven as disciplined score-pressure | taut pulse, exact attack, strict seams, forward argument | validation, parsing, authority seams, binary acceptance criteria |
| Furtwängler | Beethoven as organic emergence under harmonic tension | elastic tempo, unresolved pressure, form becoming through crisis | advisory maps, ambiguity registers, warnings, preserved tensions |
| Bernstein | Beethoven as human rhetoric and moral address | communicative gesture, public drama, emotional intelligibility | operator legibility, vivid failure messages, adoption-oriented docs |
| Karajan | Beethoven as long-line sonic architecture | blended sonority, total shape, polished continuity, long arc | taxonomy, layer maps, naming alignment, surface consolidation |
| Kleiber | Beethoven as selective kinetic electricity | concentrated energy, exact gesture, refusal of excess, high-voltage selection | narrow PRs, explicit non-goals, anti-sprawl, one-hotspot intervention |

### Refined Conductor Formulae

- **Toscanini** enforces the score.
- **Furtwängler** lets the form become.
- **Bernstein** makes Beethoven speak.
- **Karajan** shapes the total sound-world.
- **Kleiber** ignites only what must be ignited.

### Applying the Beethoven Test to Code Proposals

If two conductor lenses generate the same implementation plan, ask:

**Toscanini**

- What must be validated, parsed, enforced, or made falsifiable?
- What unsupported rhetoric should be stripped?
- What failure should become impossible to miss?

**Furtwängler**

- What tension is being resolved too early?
- Should this be a warning, watch state, or advisory report instead of a hard rule?
- Which competing interpretations should remain side-by-side for human judgment?

**Bernstein**

- What does the operator need to understand emotionally and practically?
- Does the proposal make the stakes visible?
- Does it improve adoption, onboarding, or live usability?

**Karajan**

- Does this improve the whole system’s long line?
- Are neighboring surfaces, names, and layers more coherent afterward?
- Does it reduce fragmentation rather than polish one isolated surface?

**Kleiber**

- What is the one intervention that matters?
- What should be explicitly refused?
- Can the diff be smaller without losing the essential improvement?

### Same Problem, Beethoven-Tested Proposals

**Problem:** “Known-path workflows are creating pressure for another dashboard.”

**Toscanini Response**

Implement a validator or checklist that prevents unregistered dashboard-like surfaces from being added without source inputs, authority status, and rebuild expectations.

**Proposal signature:** strict rule · validation or checklist · binary acceptance criteria · failure visibility

**Furtwängler Response**

Create an advisory overlap map showing where known-path workflow visibility needs overlap with existing dashboards, receipts, packets, and reports.

**Proposal signature:** preserve unresolved tension · no forced consolidation yet · warnings and watch markers · human review

**Bernstein Response**

Improve operator-facing guidance explaining where known-path workflow outputs should be seen and why another dashboard may increase cognitive load.

**Proposal signature:** plain-language explanation · user adoption focus · decision guidance · “why this matters”

**Karajan Response**

Extend the operator surface registry so known-path workflows fit into the whole artifact taxonomy without creating a separate dashboard family.

**Proposal signature:** layer coherence · taxonomy · relationship table · long-arc architecture

**Kleiber Response**

Refuse the new dashboard and add only one small registry row or receipt link proving the visibility need can be satisfied without a new surface.

**Proposal signature:** one hotspot · explicit non-goals · anti-sprawl · narrow diff

---

## 9. Non-Authority Statement

Conductor Proposal Lenses and the Beethoven test shape **coding-agent proposals only**. They do **not** create new authority, bypass recursion-gate, approve durable changes, or alter Record surfaces.
