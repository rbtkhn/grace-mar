# External-AI extraction prompt pack

Extract structured portable working-identity data from an external AI system (ChatGPT, Claude, Gemini, Copilot, or any tool with persistent context) into candidate objects that can enter the companion-self review pipeline.

---

## When to use

Use this prompt pack when you want to **import** working context from another AI system into a companion-self instance. The output is **candidate material** — it does not become canonical Record until reviewed and approved through the gated pipeline.

Typical scenarios:

- Moving from one AI tool to another and want to carry calibration forward
- Consolidating working knowledge from multiple AI systems into one governed Record
- Extracting tacit patterns that an AI tool has learned about you over time

---

## Confidentiality rules

The extraction prompt explicitly instructs the source AI to:

1. **Never include** employer-confidential information, proprietary code, client names, or trade secrets
2. **Abstract sensitive specifics** into reusable patterns (e.g. "prefers RFC-style proposals" instead of "wrote RFC-2847 for [Company]")
3. **Flag anything ambiguous** in the `sensitivity_flags` section so the operator can review before import

---

## JSON output contract

The extraction produces a JSON object with seven top-level keys:

| Key | Type | Contains |
|---|---|---|
| `domain_encoding` | array of objects | Reference knowledge, domain expertise, governed sources the AI has observed |
| `workflow_calibration` | array of objects | How you work: tool preferences, review patterns, communication style with tools |
| `behavioral_calibration` | array of objects | Identity signals: personality, values, decision patterns, interaction preferences |
| `artifact_rationale` | array of objects | What you've built and why: demonstrated capability with provenance |
| `candidate_examples` | array of objects | Concrete examples that illustrate any of the above |
| `sensitivity_flags` | array of objects | Items that may contain sensitive, employer-bound, or non-portable content |
| `merge_targets` | array of strings | Suggested companion-self surfaces for review: `SELF`, `SELF-LIBRARY`, `SKILLS`, `EVIDENCE` |

Each object in the arrays should include at minimum:

```json
{
  "claim": "one-sentence description of what was observed",
  "confidence": "high | medium | low",
  "durability": "stable | recurring | ephemeral",
  "examples": ["supporting evidence or context"]
}
```

---

## Extraction prompt

Paste this into your source AI system. Replace `[YOUR NAME]` with your name.

````
I want to extract what you've learned about how I work into a structured format I can import into another system. This is for my personal use — a portable working-intelligence extract.

Rules:
- Do NOT include any employer-confidential information, proprietary code, client names, or trade secrets.
- Abstract sensitive specifics into reusable patterns. For example, say "prefers structured proposals with explicit tradeoffs" instead of naming a specific internal project or document.
- If something is ambiguous about whether it's sensitive, include it in the sensitivity_flags section and I'll review it.
- Focus on patterns you've observed repeatedly, not one-off interactions.
- Be honest about confidence. If you're guessing, say low confidence.

Output valid JSON with these top-level keys:

1. domain_encoding — reference knowledge and domain expertise you've observed me working with. What subjects do I know well? What sources do I reference? What domains do I operate in?

2. workflow_calibration — how I work with tools and systems. What patterns do I follow? What do I prefer in terms of process, review, communication? How do I structure work?

3. behavioral_calibration — who I am as a person, as observed through our interactions. Personality, values, decision-making patterns, interaction preferences, communication style.

4. artifact_rationale — what I've built or produced and why. Demonstrated capabilities with context about the reasoning, not just the output.

5. candidate_examples — concrete examples that illustrate any of the above. Specific interactions, decisions, or artifacts that show the pattern clearly.

6. sensitivity_flags — anything that might contain sensitive, employer-bound, or non-portable content. Flag it so I can review before importing.

7. merge_targets — which categories of my personal record these observations should be reviewed against. Use these values: SELF, SELF-LIBRARY, SKILLS, EVIDENCE.

For each item in sections 1-6, include:
- claim: one sentence describing the observation
- confidence: high, medium, or low
- durability: stable (unlikely to change), recurring (pattern but could shift), or ephemeral (recent/temporary)
- examples: array of supporting evidence

My name is [YOUR NAME].

Output the result as a single valid JSON object.
````

---

## Usage instructions

1. Paste the extraction prompt into your source AI system
2. Review the JSON output for accuracy and sensitivity
3. Save the output as a `.json` file
4. Each item becomes a **candidate** for review — not canonical truth
5. Use the [working-identity candidate schema](working-identity-candidates.md) to normalize items before staging in the gate

---

## JSON template

A blank template with the expected structure is at [`docs/templates/working-identity-extract-template.json`](../templates/working-identity-extract-template.json).

---

## Related

- [working-identity-candidates.md](working-identity-candidates.md) — candidate schema and review process
- [current-capability-map.md](current-capability-map.md) — portability capability inventory
- [../portable-working-identity.md](../portable-working-identity.md) — portability doctrine
