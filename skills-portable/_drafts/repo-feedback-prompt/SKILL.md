---
name: repo-feedback-prompt
preferred_activation: repo feedback prompt
description: "Compose short, constructive prompts (issues/DMs) for maintainers of external GitHub repos after verifying upstream docs—non-redundant, high-leverage asks, respectful tone, optional PR offer."
portable: true
version: 0.1.0
tags:
  - operator
  - work-dev
  - communication
---

# Repo Feedback Prompt

**Preferred activation (operator):** say **`repo feedback prompt`**, **`OSS feedback prompt`**, or **`constructive GitHub prompt`**.

Use this skill when you have **reviewed someone else’s public repo** and want a **maintainer-ready message** that suggests improvements **without** generic praise, **false gaps**, or scope creep.

## When to run

- You read README, API/skill doc, or core source and formed an opinion.
- You want **one screen** of feedback an busy maintainer might actually adopt.
- You care that suggestions are **not already solved** by their documentation.

## Workflow (verify, then prompt)

1. **Ground in evidence** — Read at least **README**, the main integration surface (e.g. `SKILL.md`, API doc, or `CONTRIBUTING.md`), and only dip into code if the ask is technical. **Do not** claim the project “misses” something their docs already state.

2. **Gap table (scratch)** — For each instinct you might suggest:

   | Your instinct | What upstream already says | Still a gap? |
   |---------------|----------------------------|--------------|
   | (bullet)      | (quote or section)         | yes / no     |

   **Drop** rows where the gap is **no** or only **weakly** incremental.

3. **Leverage filter** — Keep at most **one or two themes**. Prefer:

   - **Documentation** that changes default behavior for **all** users or agent harnesses (security model, trust assumptions, norms).
   - **Small API or UX** hooks only when docs alone cannot fix the confusion.

   **Deprioritize** restating their README, naming your private stack, or bundling unrelated nice-to-haves.

4. **Tone guardrails** — Use **suggestion** language (“might strengthen,” “optional subsection”). Credit **what already works** in one or two sentences. End with **offer to PR** or **propose wording** when you can.

5. **Length** — Default: **one short issue or email**. Deeper audits are a **separate** request, not this skill.

## Output template (copy-paste)

Use this shape unless the operator asks otherwise.

```text
Subject: <repo or feature> — <one-line theme: doc suggestion / security framing / …>

<context: 1–2 sentences on what the project already does well, from their docs>

<suggestion: 1–2 paragraphs OR 3 tight bullets — each tied to a real gap>

<scope: e.g. “Even a short README subsection would help; API changes optional.”>

<closing: offer to open a PR with proposed text if they want>
```

## Anti-patterns

- **Praise-only or generic advice** with no tied gap.
- **Kitchen-sink** feedback (many frameworks, many asks).
- **False redundancy** — suggesting “document X” when X is already explicit.
- **Leakage** — tying their project to **your** internal system names or private workflows unless the operator explicitly wants that bridge.

## Optional variants

| Variant | When |
|---------|------|
| **Maintainer DM** | 3–5 sentences; single highest-leverage gap only. |
| **Verification appendix** | For your own notes: files read, URLs — **omit** from the outbound message unless the maintainer likes receipts. |

## Promotion

When this draft has been **reused on a second external repo** with good results, consider promoting to `skills-portable/repo-feedback-prompt/` per the repo’s portable-skills ladder (`manifest.yaml` + sync).
