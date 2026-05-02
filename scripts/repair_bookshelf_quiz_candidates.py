#!/usr/bin/env python3
"""Repair known thin bookshelf MCQ candidates with structured source receipts.

This is a bounded operator repair for CANDIDATE-0042..0045. It does not merge
Record surfaces; it only rewrites pending gate candidates into the stronger
bookshelf quiz receipt shape requested by the operator.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GATE = REPO / "users" / "grace-mar" / "recursion-gate.md"


REPAIRED_BLOCKS = {
    "CANDIDATE-0042": '''### CANDIDATE-0042 (IX-A - maritime power as naval-commercial system; bookshelf MCQ)

```yaml
status: pending
timestamp: 2026-05-02
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source: operator - repaired bookshelf MCQ receipt
source_binding_strength: weak
review_needed: true
shelf_refs: [HNSRC-0247, HNSRC-0248]
quiz_receipt:
  source_kind: secondary
  citation_label: "Roger Crowley, City of Fortune; Roger Crowley, Spice"
  visible_prompt: "Drawing on Roger Crowley's accounts of Venetian sea power and the spice contest, which answer best captures the strategic mechanism of maritime power?"
  stem_topic: "Maritime power as naval-commercial system"
  selected_answer: "B - naval commerce, bases, chokepoints, and fleet concentration make maritime power geopolitically decisive."
  correct_answer: "B - naval commerce, bases, chokepoints, and fleet concentration make maritime power geopolitically decisive."
  validation_note: "Companion selected the concept-level answer matching the maritime-power mechanism. Binding is weak because the catalog has Crowley secondary context, not a direct Mahan primary/source row."
  staged_claim: "Knows: Mahan-style sea-power analysis treats naval commerce, bases, chokepoints, and fleet concentration as mechanisms that make maritime power geopolitically decisive."
source_exchange:
  operator: |
    Bookshelf quiz receipt repair. Visible quiz prompt used academic prose and did not expose internal shelf ids.
    Source context: Roger Crowley, City of Fortune; Roger Crowley, Spice.
    Boundary note: secondary contextual support only; no direct Mahan shelf row found in self-library-bookshelf at repair time.
mind_category: knowledge
signal_type: operator_quiz_validated
priority_score: 3
summary: "IX-A: maritime power as naval-commercial system"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: Mahan-style sea-power analysis treats naval commerce, bases, chokepoints, and fleet concentration as mechanisms that make maritime power geopolitically decisive."
warrant: "Revisit if a direct Mahan source is added to self-library-bookshelf or if this should be reframed as Venetian maritime-power context rather than Mahan-style theory."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
impact_tier: low
envelope_class: none
```
''',
    "CANDIDATE-0043": '''### CANDIDATE-0043 (IX-A - offensive realism regional hegemony; bookshelf MCQ)

```yaml
status: pending
timestamp: 2026-05-02
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source: operator - repaired bookshelf MCQ receipt
source_binding_strength: weak
review_needed: true
shelf_refs: []
quiz_receipt:
  source_kind: secondary
  citation_label: "Mearsheimer, offensive realism"
  visible_prompt: "In Mearsheimer's offensive realism, why do great powers seek regional hegemony?"
  stem_topic: "Offensive realism and regional hegemony"
  selected_answer: "B - anarchy leaves states unable to be fully certain of other states' intentions."
  correct_answer: "B - anarchy leaves states unable to be fully certain of other states' intentions."
  validation_note: "Companion selected the concept-level answer matching the offensive-realist mechanism. Binding is weak because no direct Mearsheimer shelf row was found in self-library-bookshelf at repair time."
  staged_claim: "Knows: in Mearsheimer's offensive realism, great powers seek regional hegemony because anarchy leaves states unable to be fully certain of other states' intentions."
source_exchange:
  operator: |
    Bookshelf quiz receipt repair. Visible quiz prompt used academic prose and did not expose internal shelf ids.
    Boundary note: no direct Mearsheimer shelf row found in self-library-bookshelf at repair time; keep as review-needed before approval.
mind_category: knowledge
signal_type: operator_quiz_validated
priority_score: 3
summary: "IX-A: offensive realism and regional hegemony"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: in Mearsheimer's offensive realism, great powers seek regional hegemony because anarchy leaves states unable to be fully certain of other states' intentions."
warrant: "Revisit if a direct Mearsheimer source is added to self-library-bookshelf or if the operator wants only catalog-bound claims approved."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
impact_tier: low
envelope_class: none
```
''',
    "CANDIDATE-0044": '''### CANDIDATE-0044 (IX-A - Melian Dialogue power asymmetry; bookshelf MCQ)

```yaml
status: pending
timestamp: 2026-05-02
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source: operator - repaired bookshelf MCQ receipt
source_binding_strength: strong
review_needed: false
shelf_refs: [HNSRC-0003]
quiz_receipt:
  source_kind: primary
  citation_label: "Thucydides, History of the Peloponnesian War"
  visible_prompt: "In Thucydides' account of the Melian Dialogue, what realist lesson is usually drawn from Athens' argument to Melos?"
  stem_topic: "Melian Dialogue and power asymmetry"
  selected_answer: "C - power asymmetry can override moral argument when no higher enforcing authority exists."
  correct_answer: "C - power asymmetry can override moral argument when no higher enforcing authority exists."
  validation_note: "Companion selected the concept-level answer matching the standard realist reading of the Melian Dialogue."
  staged_claim: "Knows: the Melian Dialogue is commonly read as a realist lesson that power asymmetry can override moral argument when no higher enforcing authority exists."
source_exchange:
  operator: |
    Bookshelf quiz receipt repair. Visible quiz prompt used academic prose and did not expose internal shelf ids.
    Primary source binding: Thucydides, History of the Peloponnesian War.
mind_category: knowledge
signal_type: operator_quiz_validated
priority_score: 5
summary: "IX-A: Melian Dialogue as realist lesson on power asymmetry"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: the Melian Dialogue is commonly read as a realist lesson that power asymmetry can override moral argument when no higher enforcing authority exists."
warrant: "Revisit if I stop treating the Melian Dialogue as a realist power-asymmetry anchor."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
impact_tier: low
envelope_class: none
```
''',
    "CANDIDATE-0045": '''### CANDIDATE-0045 (IX-A - second-strike capability and deterrence; bookshelf MCQ)

```yaml
status: pending
timestamp: 2026-05-02
channel_key: operator:cursor:bookshelf-mcq-self-knowledge
proposal_class: SELF_KNOWLEDGE_ADD
source: operator - repaired bookshelf MCQ receipt
source_binding_strength: weak
review_needed: true
shelf_refs: [HNSRC-0256]
quiz_receipt:
  source_kind: secondary
  citation_label: "H. W. Brands, The General vs. the President"
  visible_prompt: "Against the background of Cold War nuclear escalation debates, what does second-strike capability mean?"
  stem_topic: "Second-strike capability and deterrence"
  selected_answer: "B - a state can absorb a nuclear attack and still retaliate, making a first strike less attractive."
  correct_answer: "B - a state can absorb a nuclear attack and still retaliate, making a first strike less attractive."
  validation_note: "Companion selected the concept-level answer matching deterrence theory. Binding is weak because the available shelf row is secondary Cold War context rather than a dedicated primary nuclear-strategy source."
  staged_claim: "Knows: second-strike capability means a state can absorb a nuclear attack and still retaliate, making a first strike less attractive and stabilizing deterrence."
source_exchange:
  operator: |
    Bookshelf quiz receipt repair. Visible quiz prompt used academic prose and did not expose internal shelf ids.
    Source context: H. W. Brands, The General vs. the President.
    Boundary note: secondary contextual support only; no dedicated primary nuclear-strategy shelf row found at repair time.
mind_category: knowledge
signal_type: operator_quiz_validated
priority_score: 3
summary: "IX-A: second-strike capability and deterrence"
convergence: first
profile_target: IX-A. KNOWLEDGE
suggested_entry: "Knows: second-strike capability means a state can absorb a nuclear attack and still retaliate, making a first strike less attractive and stabilizing deterrence."
warrant: "Revisit if a dedicated nuclear-strategy primary source is added to self-library-bookshelf or if this should remain report-only until better anchored."
prompt_section: YOUR KNOWLEDGE
prompt_addition: none
impact_tier: low
envelope_class: none
```
''',
}


def repair_gate(content: str) -> tuple[str, list[str]]:
    repaired: list[str] = []
    for cid, replacement in REPAIRED_BLOCKS.items():
        pattern = re.compile(
            rf"^### {re.escape(cid)}(?:\s*\([^)]*\))?\s*\n```yaml\n.*?```\n?",
            re.MULTILINE | re.DOTALL,
        )
        content, count = pattern.subn(replacement + "\n", content, count=1)
        if count:
            repaired.append(cid)
    return content, repaired


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gate", type=Path, default=GATE)
    ap.add_argument("--check", action="store_true", help="Check whether repair would change the gate, but do not write")
    args = ap.parse_args()

    if not args.gate.is_file():
        print(f"ERROR: missing gate file: {args.gate}")
        return 1

    before = args.gate.read_text(encoding="utf-8")
    after, repaired = repair_gate(before)
    if not repaired:
        print("no matching candidates repaired")
        return 0
    if args.check:
        print("would repair: " + ", ".join(repaired))
        return 0
    args.gate.write_text(after, encoding="utf-8")
    print("repaired: " + ", ".join(repaired))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
