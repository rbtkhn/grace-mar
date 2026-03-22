"""Unit tests for grace_mar.merge surface mutators (IX, evidence, prompt)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

SELF_FIXTURE = """## IX. MIND

### IX-A. KNOWLEDGE

#### Books Read

```yaml
books_read: []
```

#### Facts (LEARN-nnn)

```yaml
entries:
  - id: LEARN-0001
    date: 2026-01-01
    topic: "Alpha"
    source: test
    provenance: human_approved

```

### IX-B. CURIOSITY

```yaml
entries:
  - id: CUR-0001
    date: 2026-01-01
    topic: "Beta"
    trigger: test
    response_signal: x
    intensity: 1
    provenance: human_approved

```

### IX-C. PERSONALITY (Observed)

```yaml
entries:
  - id: PER-0001
    date: 2026-01-01
    type: observed
    observation: "Gamma"
    provenance: human_approved

```
"""

EVIDENCE_FIXTURE = """## I. READING LIST

```yaml
entries: []

# Example entry format:
# - id: READ-0001
```

## V. ACTIVITY LOG

```yaml
entries:
  - id: ACT-0001
    date: 2026-01-01
    summary: "x"
```

## VI. ATTESTATION LOG

(empty)
"""


def test_insert_ix_a_targets_facts_block_not_books() -> None:
    from grace_mar.merge.self_ix import insert_ix_a_entry

    new = "  - id: LEARN-0002\n    date: 2026-01-02\n    topic: \"New\"\n    source: pipeline merge\n    provenance: human_approved\n\n"
    out = insert_ix_a_entry(SELF_FIXTURE, new)
    assert "books_read:" in out
    assert 'topic: "New"' in out
    # Must appear after Facts heading, in same entries list as LEARN-0001
    idx_facts = out.index("#### Facts (LEARN-nnn)")
    idx_new = out.index('topic: "New"')
    assert idx_new > idx_facts
    idx_books = out.index("books_read:")
    assert idx_new > idx_books


def test_append_act_before_attestation() -> None:
    from grace_mar.merge.evidence_log import append_act_entry

    frag = "\n  - id: ACT-0002\n    date: 2026-01-02\n    summary: \"y\"\n"
    out = append_act_entry(EVIDENCE_FIXTURE, frag)
    assert out.index("ACT-0002") < out.index("## VI. ATTESTATION LOG")


def test_upsert_reading_list_first_then_append() -> None:
    from grace_mar.merge.evidence_log import upsert_reading_list_entry

    step1 = upsert_reading_list_entry(
        EVIDENCE_FIXTURE,
        read_id="READ-0001",
        title="Hello",
    )
    assert "entries: []" not in step1
    assert "READ-0001" in step1
    assert "Hello" in step1

    step2 = upsert_reading_list_entry(
        step1,
        read_id="READ-0002",
        title="Second",
    )
    assert "READ-0002" in step2
    assert "READ-0001" in step2


def test_rebuild_prompt_from_self_min_fixture() -> None:
    from grace_mar.merge.prompt_sync import rebuild_observation_sections_from_self

    prompt = """## YOUR KNOWLEDGE (from observations)

- old bullet

## YOUR CURIOSITY (what catches your attention)

- old cur

## YOUR PERSONALITY (observed)

- old per

## IMPORTANT CONSTRAINTS

- stay six
"""
    out = rebuild_observation_sections_from_self(prompt, SELF_FIXTURE)
    assert "old bullet" not in out or "Alpha" in out
    assert "Alpha" in out
    assert "Beta" in out
    assert "Gamma" in out
    assert "## IMPORTANT CONSTRAINTS" in out
    assert "stay six" in out


@pytest.mark.skipif(not (REPO_ROOT / "bot" / "prompt.py").exists(), reason="prompt fixture missing")
def test_rebuild_ix_on_real_prompt_smoke() -> None:
    from grace_mar.merge.prompt_sync import rebuild_observation_sections_from_self

    prompt = (REPO_ROOT / "bot" / "prompt.py").read_text(encoding="utf-8")
    self_md = (REPO_ROOT / "users" / "grace-mar" / "self.md").read_text(encoding="utf-8")
    m = prompt.find('SYSTEM_PROMPT = """')
    assert m != -1
    start = prompt.find('"""', m) + 3
    end = prompt.find('"""', start)
    body = prompt[start:end]
    rebuilt = rebuild_observation_sections_from_self(body, self_md)
    assert "## YOUR KNOWLEDGE (from observations)" in rebuilt
    assert "## IMPORTANT CONSTRAINTS" in rebuilt
    assert len(rebuilt) > 500
