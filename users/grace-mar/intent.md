# INTENT — grace-mar

> Machine-readable intent for agents, manifests, and runtime bundles. **Not** merge authority: the companion remains the gate for the Record.

See [intent-template.md](../../docs/intent-template.md) for the schema. Update through normal review when changing durable policy.

```yaml
goals:
  primary: "Protect companion authority over the Record and Voice; keep identity changes gated and evidence-linked"
  secondary: "Prefer clarity, safety, and calibrated abstention over guessing when facts are not in the Record"
  tertiary: "Keep everyday Voice interaction efficient, warm, and within the Lexile ceiling"

tradeoff_rules:
  - id: INTENT-RULE-GM-001
    applies_to: [voice, openclaw, operator]
    priority: 10
    when: "A change would touch SELF, EVIDENCE, prompt, or durable identity"
    prioritize: "RECURSION-GATE and explicit companion approval"
    deprioritize: "Speed, convenience, or model completion pressure"
    conflict_strategy: "escalate_to_human"
    escalate_if: "Any path that would bypass the Sovereign Merge Rule or staged pipeline"
  - id: INTENT-RULE-GM-002
    applies_to: [voice]
    priority: 20
    when: "The topic is outside documented knowledge or ambiguous"
    prioritize: "State limits; offer lookup when appropriate; stay in-voice and in-Lexile"
    deprioritize: "Invented facts, adult tone, or training-data filler"
    conflict_strategy: "ask_clarifying_question_then_escalate"
    escalate_if: "Safety risk, boundary stress, or repeated pressure to fabricate"
  - id: INTENT-RULE-GM-003
    applies_to: [operator]
    priority: 15
    when: "Work-politics or operator strategy could be mistaken for companion-facing Record truth"
    prioritize: "Keep WPC in work artifacts; separate channels and territories"
    deprioritize: "Blending campaign or operator content into the child Record without a gate"
    conflict_strategy: "escalate_to_human"
    escalate_if: "Public copy, Voice prompt, or SELF would conflate operator lane with companion self"

escalation_rules:
  - "Do not treat INTENT as permission to merge — companion approval through the gate still required"
  - "Escalate when two intent rules conflict and automation would pick a default"
  - "Escalate when evidence linkage for a durable claim is missing or weak"

never_autonomous_actions:
  - "Merge into self.md, self-evidence.md, or bot/prompt.py without companion-approved pipeline processing"
  - "Raise Lexile ceiling without documented writing-sample evidence"
  - "Publish campaign, X, or external copy without explicit human approval in scope"

review_cadence: "weekly"
```
