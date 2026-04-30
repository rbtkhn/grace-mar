---
name: ideation-engine
preferred_activation: ideation engine
description: "Generate approval-first Top 3 opportunity briefs from existing lanes, current assets, and source-backed signals for a solo operator."
portable: true
version: 0.1.0
tags:
  - operator
  - entrepreneurship
  - strategy
  - opportunity
---

# Ideation Engine

**Preferred activation (operator):** say **`ideation engine`**, **`weekly opportunity brief`**, **`new lane ideas`**, or **`opportunity scan`**.

Use this skill to generate grounded opportunity briefs from what already exists: active lanes, current assets, source-backed signals, operator constraints, and reusable capabilities.

The default posture is **approval-first**. This skill proposes. It does not stage, execute, spend money, create public posts, spawn lanes, or start automations.

## When To Use

- You want a weekly opportunity brief.
- You want new project, micro-business, product, or service ideas grounded in existing work.
- You have many active lanes and need to find the highest-leverage next opportunity.
- You want a concise approval memo before investing time, tokens, or reputation.

## Inputs

Inspect the host's available equivalents:

| Input | Portable placeholder |
|-------|----------------------|
| Operator identity / values / risk appetite | `<operator-profile>` |
| Existing lanes, projects, or assets | `<active-lanes>` |
| Source library or evidence base | `<source-library>` |
| Recent work logs or cadence notes | `<recent-work>` |
| Budget / time / compute constraints | `<budget-policy>` |
| Approval inbox or decision process | `<approval-process>` |

Prioritize existing lanes before new abstractions. An opportunity is stronger when it reuses something already built, documented, trusted, or connected.

## Workflow

1. **Gather signals**
   - Read current lanes, recent work, source-backed notes, and constraints.
   - If source signal is thin, say so and recommend a broader scan instead of inventing demand.
2. **Generate candidates**
   - Produce a small set of plausible opportunities.
   - Prefer ideas that connect at least two existing assets, lanes, skills, or relationships.
3. **Score simply**
   - Score each candidate from 1-5 on the rubric below.
   - Use short explanations instead of false precision.
4. **Select Top 3**
   - Return exactly three opportunity briefs unless the operator asks for a wider portfolio.
   - Include one recommended winner when the evidence supports it.
5. **Prepare approval memo**
   - Recommend approve, refine, or archive.
   - Name the first reversible next step.

## Scoring Rubric

Score 1-5:

| Dimension | Question |
|-----------|----------|
| **Existing-lane leverage** | Does this reuse current assets, documents, relationships, scripts, or habits? |
| **Identity fit** | Does it fit the operator's documented taste, values, risk appetite, and constraints? |
| **Feasibility** | Can the first useful version happen with available time, tools, and budget? |
| **Proof strength** | Are there sources, receipts, or observed demand rather than vibes alone? |
| **Risk** | Are reputational, financial, regulatory, or trust risks bounded and visible? |

Risk scoring convention:

- `5` = low / bounded risk,
- `1` = high / poorly understood risk.

## Output Template

```markdown
## Weekly Opportunity Brief - [Date]

**Inputs checked:** [active lanes, recent work, source library, budget constraints]
**Cycle quality:** strong / mixed / thin

### Top 3 Opportunities

#### 1. [One-line hook]

**Why this fits now:** [source-backed reason]

| Dimension | Score | Note |
|-----------|-------|------|
| Existing-lane leverage | 1-5 |  |
| Identity fit | 1-5 |  |
| Feasibility | 1-5 |  |
| Proof strength | 1-5 |  |
| Risk | 1-5 |  |

**First reversible step:** [smallest useful action]
**Estimated effort / budget:** [rough range]
**Success metric:** [what would count as early proof]
**Kill criteria:** [when to stop]
**Approval memo:** approve / refine / archive - [reason]

#### 2. [One-line hook]

[same compact shape]

#### 3. [One-line hook]

[same compact shape]

**Recommended operator move:** [one sentence]
```

## Guardrails

- **Approval-first** - Do not execute, stage, spend, publish, create lanes, or start automations.
- **Source discipline** - Do not invent market size, demand, pricing, or competitor facts.
- **Existing-lane bias** - Prefer leverage from current assets before proposing new surfaces.
- **Thin-cycle honesty** - If evidence is weak, say "thin cycle" and recommend what to inspect next.
- **Risk visibility** - Public-facing ideas must flag verification, identity, trust, regulatory, and reputation issues.
- **No silent proliferation** - New lanes or projects require explicit human approval through the host's decision process.

## Unresolved Tensions

Keep these tensions visible instead of smoothing them into false certainty:

| Tension | Watchpoint |
|---------|------------|
| **Optimism vs proof** | Strong ideas should feel energizing, but the brief must still separate observed demand from hope, analogy, or taste. |
| **Existing-lane leverage vs fresh opportunity** | Reusing current assets is preferred, but do not overfit to stale lanes when a source-backed opening clearly points elsewhere. |
| **Speed vs authority** | The skill can shorten decision cycles, but approval remains a human act; faster packaging is not permission to execute. |
| **Risk visibility vs risk paralysis** | Name financial, reputational, regulatory, and trust risks without turning every uncertainty into a veto. |
| **Top 3 clarity vs portfolio richness** | The default answer is three briefs, but the notes may preserve promising runners-up when they explain the shape of the opportunity field. |

## Collaboration Norms

- Keep the first answer concise: Top 3 first, details second.
- Use grounded builder language: practical, optimistic, and allergic to fake certainty.
- Treat approval memos as decision support, not authorization.
- Ask for more context only when missing constraints would materially change the ranking.

## Related Future Skills

Future companion skills may include:

- `opportunity-scoring` for deeper weighted scoring,
- `model-router` for budget-aware model selection,
- `work-lane-spawner` for approved lane-start packets.

Do not assume those skills exist unless the host provides them.
