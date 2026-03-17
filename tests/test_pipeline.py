"""Tests for pipeline invariants: gate sections, filter logic, merge path."""
import pytest

from recursion_gate_review import filter_review_candidates, parse_review_candidates, split_gate_sections


def test_split_gate_sections_empty_processed():
    """Processed section is empty when marker absent."""
    md = "# Gate\n\n## Candidates\n\n### CANDIDATE-001\n```yaml\nstatus: pending\n```\n"
    active, processed = split_gate_sections(md)
    assert "CANDIDATE-001" in active
    assert processed == ""


def test_split_gate_sections_with_processed():
    """Active ends before ## Processed; processed contains rest."""
    md = (
        "# Gate\n\n## Candidates\n\n### CANDIDATE-001\n```yaml\nstatus: pending\n```\n\n"
        "## Processed\n\n### CANDIDATE-000\n```yaml\nstatus: approved\n```\n"
    )
    active, processed = split_gate_sections(md)
    assert "CANDIDATE-001" in active
    assert "CANDIDATE-000" in processed
    assert "## Processed" not in active


def test_filter_review_candidates_status():
    """Filter by status=pending keeps only pending."""
    rows = [
        {"id": "CANDIDATE-001", "status": "pending", "summary": "a"},
        {"id": "CANDIDATE-002", "status": "approved", "summary": "b"},
        {"id": "CANDIDATE-003", "status": "pending", "summary": "c"},
    ]
    out = filter_review_candidates(rows, status="pending")
    assert len(out) == 2
    assert all(r["status"] == "pending" for r in out)


def test_filter_review_candidates_empty_status():
    """No status filter returns all."""
    rows = [{"id": "CANDIDATE-001", "status": "pending"}]
    out = filter_review_candidates(rows, status="")
    assert len(out) == 1
