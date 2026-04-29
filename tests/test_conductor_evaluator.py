"""Tests for conductor action-menu heuristics and eval harness."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from grace_mar.conductor_evaluator import (
    evaluate_action_menu,
    evaluate_markdown_menu,
    parse_action_menu_lines,
)
from grace_mar.conductor_metrics import build_metrics_payload

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "conductor"
HARNESS = REPO_ROOT / "scripts" / "run_conductor_eval_harness.py"

REQUIRED_KEYS = frozenset(
    {
        "schema_version",
        "created_at",
        "user",
        "conductor_slug",
        "session_origin",
        "action_mcq_count",
        "grounding_reference_count",
        "discrimination_score",
        "grounding_score",
        "actionability_score",
        "fidelity_score",
        "continuity_signal",
        "recommendation_signal",
        "warnings",
        "evaluation",
        "score_notes",
    }
)


def _load_fixture(name: str) -> str:
    data = json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))
    return str(data["body_markdown"])


def test_parse_action_menu_order() -> None:
    md = "**B.** Line two body.\n**A.** Line one body.\n"
    lines = parse_action_menu_lines(md)
    assert lines == ["Line one body.", "Line two body."]


def test_fidelity_differs_by_slug() -> None:
    lines = [
        "Verify seams and falsify weak claims with tier discipline.",
        "Open docs/a.md",
        "Check precision",
        "Read scripts/x.py",
        "Trim flourish",
    ]
    t = evaluate_action_menu("toscanini", lines).fidelity_score
    b = evaluate_action_menu("bernstein", lines).fidelity_score
    assert t > b


def test_discrimination_good_gt_bad_dup() -> None:
    good_md = _load_fixture("good")
    bad_md = _load_fixture("bad_dup")
    _, s_good = evaluate_markdown_menu("toscanini", good_md)
    _, s_bad = evaluate_markdown_menu("toscanini", bad_md)
    assert s_good.discrimination_score > s_bad.discrimination_score


def test_grounding_good_gt_bad_vague() -> None:
    good_md = _load_fixture("good")
    bad_md = _load_fixture("bad_vague")
    _, s_good = evaluate_markdown_menu("toscanini", good_md)
    _, s_bad = evaluate_markdown_menu("toscanini", bad_md)
    assert s_good.grounding_score > s_bad.grounding_score
    assert s_good.grounding_reference_count > s_bad.grounding_reference_count


def test_build_metrics_payload_rejects_unknown_slug() -> None:
    with pytest.raises(ValueError, match="unknown conductor_slug"):
        build_metrics_payload(
            body_markdown="**A.** x\n",
            conductor_slug="not-a-slug",
            session_origin="coffee",
            user="grace-mar",
        )


def test_build_metrics_payload_rejects_bad_origin() -> None:
    with pytest.raises(ValueError, match="invalid session_origin"):
        build_metrics_payload(
            body_markdown="**A.** x\n",
            conductor_slug="toscanini",
            session_origin="invalid",
            user="grace-mar",
        )


def test_harness_emits_schema_shaped_json(tmp_path: Path) -> None:
    out = tmp_path / "metrics.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(HARNESS),
            "--fixture",
            str(FIXTURES / "good.json"),
            "--slug",
            "toscanini",
            "--user",
            "grace-mar",
            "--origin",
            "coffee",
            "--out",
            str(out),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert REQUIRED_KEYS <= set(payload.keys())
    assert payload["schema_version"] == "conductor-session-metrics.v1"
    assert payload["evaluation"] == {"method": "heuristic_v1", "deterministic": True}
    assert payload["conductor_slug"] == "toscanini"


def test_harness_refuses_forbidden_users_output() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(HARNESS),
            "--fixture",
            str(FIXTURES / "good.json"),
            "--slug",
            "toscanini",
            "--user",
            "grace-mar",
            "--origin",
            "coffee",
            "--out",
            str(REPO_ROOT / "users" / "grace-mar" / "conductor-metrics.json"),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    assert "forbidden" in (proc.stderr + proc.stdout).lower()
