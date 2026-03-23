"""score_gate_candidates.py — blockquote scoring without touching real gate files."""

import textwrap

import pytest

from score_gate_candidates import (
    annotate_active_section,
    compute_composite,
    estimate_subscores,
)


def test_compute_composite_deterministic():
    sub = {k: 0.8 for k in ("density_delta", "uniqueness", "evidence_grounding", "ix_balance", "readability")}
    assert compute_composite(sub) == 80.0


def test_annotate_inserts_auto_score_line():
    active = textwrap.dedent(
        """\
        ## Candidates

        ### CANDIDATE-0001 (pending test)

        ```yaml
        status: pending
        summary: "novel gap evidence https://example.com"
        mind_category: knowledge
        profile_target: IX-A.1
        ```
        """
    )
    new, n = annotate_active_section(active, threshold=0.0, pending_only=True)
    assert n == 1
    assert "> **Auto-score**:" in new
    assert "```yaml" in new


def test_annotate_skips_non_pending():
    active = textwrap.dedent(
        """\
        ## Candidates

        ### CANDIDATE-0002 (rejected)

        ```yaml
        status: rejected
        summary: "x"
        ```
        """
    )
    new, n = annotate_active_section(active, threshold=99.0, pending_only=True)
    assert n == 0
    assert "**Auto-score**" not in new


def test_estimate_subscores_range():
    sub = estimate_subscores("IX-A knowledge " * 20 + " artifact ACT-0001 " + "novel gap")
    for k in ("density_delta", "uniqueness", "evidence_grounding", "ix_balance", "readability"):
        assert 0.0 <= sub[k] <= 1.0
