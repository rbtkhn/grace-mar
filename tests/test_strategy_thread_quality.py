"""Light tests for report_strategy_thread_quality.py.

Covers: missing file detection, stale thread flagging, roster drift
detection, coverage gap, density computation, batch-analysis alignment,
and report assembly on small fixtures.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from report_strategy_thread_quality import (
    ExpertDiagnostic,
    QualityReport,
    RosterDrift,
    _check_batch_alignment,
    _check_machine_layer,
    _check_missing_files,
    _check_roster_drift,
    _check_transcript_content,
    _compute_density,
    build_report,
    format_json,
    format_markdown,
)
from strategy_expert_corpus import THREAD_MARKER_END, THREAD_MARKER_START


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def notebook_dir(tmp_path: Path) -> Path:
    """Minimal notebook dir with one expert (testexp) having all three files."""
    d = tmp_path / "notebook"
    d.mkdir()
    return d


def _expert_dir(notebook_dir: Path, expert_id: str) -> Path:
    d = notebook_dir / "experts" / expert_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_profile(notebook_dir: Path, expert_id: str) -> None:
    _expert_dir(notebook_dir, expert_id)
    (notebook_dir / "experts" / expert_id / "profile.md").write_text(
        f"# Expert — `{expert_id}`\n", encoding="utf-8"
    )


def _write_transcript(notebook_dir: Path, expert_id: str, dates: dict[str, list[str]]) -> None:
    _expert_dir(notebook_dir, expert_id)
    lines = [
        f"# Expert transcript — `{expert_id}`\n",
        "<!-- Triage appends new date sections below. Do not add content above this line. -->\n",
    ]
    for date_str in sorted(dates.keys(), reverse=True):
        lines.append(f"## {date_str}")
        for entry in dates[date_str]:
            lines.append(entry)
        lines.append("")
    (notebook_dir / "experts" / expert_id / "transcript.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def _write_thread(notebook_dir: Path, expert_id: str, machine_lines: list[str]) -> None:
    _expert_dir(notebook_dir, expert_id)
    inner = "\n".join(machine_lines) if machine_lines else "_(No transcript or knot material for extraction.)_"
    (notebook_dir / "experts" / expert_id / "thread.md").write_text(
        f"# Expert thread — `{expert_id}`\n\n"
        f"{THREAD_MARKER_START}\n"
        f"{inner}\n"
        f"{THREAD_MARKER_END}\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Missing files
# ---------------------------------------------------------------------------

def test_missing_profile(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- line one"]})
    _write_thread(notebook_dir, eid, ["## Machine layer", "- extracted line"])

    diag = _check_missing_files(eid, notebook_dir)
    assert not diag.profile_exists
    assert diag.transcript_exists
    assert diag.thread_exists
    assert any("missing profile" in i for i in diag.issues)


def test_all_files_present(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_profile(notebook_dir, eid)
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- line"]})
    _write_thread(notebook_dir, eid, ["- machine line"])

    diag = _check_missing_files(eid, notebook_dir)
    assert diag.profile_exists
    assert diag.transcript_exists
    assert diag.thread_exists
    assert not diag.issues


# ---------------------------------------------------------------------------
# Stale threads
# ---------------------------------------------------------------------------

def test_stale_thread_no_recent_dates(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_transcript(notebook_dir, eid, {"2026-03-01": ["- old line"]})

    diag = ExpertDiagnostic(expert_id=eid)
    _check_transcript_content(diag, notebook_dir, cutoff=date(2026, 4, 11))
    assert diag.stale
    assert any("stale" in i for i in diag.issues)


def test_fresh_thread(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- fresh line"]})

    diag = ExpertDiagnostic(expert_id=eid)
    _check_transcript_content(diag, notebook_dir, cutoff=date(2026, 4, 11))
    assert not diag.stale
    assert diag.transcript_line_count == 1
    assert diag.newest_transcript_date == "2026-04-18"


def test_stale_no_transcript_file(notebook_dir: Path) -> None:
    diag = ExpertDiagnostic(expert_id="ghost")
    _check_transcript_content(diag, notebook_dir, cutoff=date(2026, 4, 11))
    assert diag.stale


# ---------------------------------------------------------------------------
# Coverage gap
# ---------------------------------------------------------------------------

def test_coverage_gap_transcript_content_empty_machine(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- content line"]})
    _write_thread(notebook_dir, eid, [])

    diag = ExpertDiagnostic(expert_id=eid, transcript_line_count=1)
    _check_machine_layer(diag, notebook_dir)
    assert diag.coverage_gap
    assert diag.machine_layer_line_count == 0


def test_no_coverage_gap_when_machine_has_content(notebook_dir: Path) -> None:
    eid = "testexp"
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- content"]})
    _write_thread(notebook_dir, eid, ["## Machine layer", "- extracted", "- another"])

    diag = ExpertDiagnostic(expert_id=eid, transcript_line_count=1)
    _check_machine_layer(diag, notebook_dir)
    assert not diag.coverage_gap
    assert diag.machine_layer_line_count == 3


# ---------------------------------------------------------------------------
# Density
# ---------------------------------------------------------------------------

def test_density_ratio() -> None:
    diag = ExpertDiagnostic(expert_id="test", transcript_line_count=10, machine_layer_line_count=5)
    _compute_density(diag)
    assert diag.density_ratio == 0.5


def test_density_zero_transcript() -> None:
    diag = ExpertDiagnostic(expert_id="test", transcript_line_count=0, machine_layer_line_count=5)
    _compute_density(diag)
    assert diag.density_ratio is None


# ---------------------------------------------------------------------------
# Roster drift
# ---------------------------------------------------------------------------

def test_roster_drift_ok(tmp_path: Path) -> None:
    from strategy_expert_corpus import CANONICAL_EXPERT_IDS

    header = "| expert_id | Name | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |"
    sep = "|-----------|------|-----------------|------------------|-----------------------------------|"
    rows = [f"| `{eid}` | Name | Role | tag | pair |" for eid in CANONICAL_EXPERT_IDS]
    text = header + "\n" + sep + "\n" + "\n".join(rows) + "\n"
    index = tmp_path / "threads.md"
    index.write_text(text, encoding="utf-8")

    drift = _check_roster_drift(index)
    assert drift.ok
    assert not drift.missing_from_table
    assert not drift.extra_in_table


def test_roster_drift_missing_expert(tmp_path: Path) -> None:
    from strategy_expert_corpus import CANONICAL_EXPERT_IDS

    header = "| expert_id | Name | Role (one line) | Default grep tag | Typical `batch-analysis` pairings |"
    sep = "|-----------|------|-----------------|------------------|-----------------------------------|"
    rows = [f"| `{eid}` | Name | Role | tag | pair |" for eid in CANONICAL_EXPERT_IDS[:-1]]
    text = header + "\n" + sep + "\n" + "\n".join(rows) + "\n"
    index = tmp_path / "threads.md"
    index.write_text(text, encoding="utf-8")

    drift = _check_roster_drift(index)
    assert not drift.ok
    assert CANONICAL_EXPERT_IDS[-1] in drift.missing_from_table


# ---------------------------------------------------------------------------
# Batch-analysis alignment
# ---------------------------------------------------------------------------

def test_batch_alignment_catches_unknown_tag(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox.md"
    inbox.write_text(
        "- batch-analysis | 2026-04-18 | test | thread:nonexistent\n",
        encoding="utf-8",
    )
    issues = _check_batch_alignment(inbox)
    assert len(issues) == 1
    assert issues[0].raw_tag == "nonexistent"


def test_batch_alignment_clean_for_canonical(tmp_path: Path) -> None:
    inbox = tmp_path / "inbox.md"
    inbox.write_text(
        "- batch-analysis | 2026-04-18 | test | thread:pape\n",
        encoding="utf-8",
    )
    issues = _check_batch_alignment(inbox)
    assert len(issues) == 0


# ---------------------------------------------------------------------------
# Full report assembly
# ---------------------------------------------------------------------------

def test_report_assembly_minimal(notebook_dir: Path, tmp_path: Path) -> None:
    """Build a report with one expert having all files and fresh content."""
    from strategy_expert_corpus import CANONICAL_EXPERT_IDS

    eid = CANONICAL_EXPERT_IDS[0]
    _write_profile(notebook_dir, eid)
    _write_transcript(notebook_dir, eid, {"2026-04-18": ["- fresh line"]})
    _write_thread(notebook_dir, eid, ["## Machine layer", "- extracted"])

    inbox = tmp_path / "inbox.md"
    inbox.write_text("", encoding="utf-8")
    index = tmp_path / "threads.md"
    index.write_text("", encoding="utf-8")

    report = build_report(
        notebook_dir=notebook_dir,
        threads_index=index,
        inbox_path=inbox,
        lookback_days=7,
        today=date(2026, 4, 18),
    )
    assert report.expert_count == len(CANONICAL_EXPERT_IDS)
    assert report.summary["total_experts"] == len(CANONICAL_EXPERT_IDS)

    first = next(e for e in report.experts if e.expert_id == eid)
    assert not first.stale
    assert not first.coverage_gap
    assert first.transcript_line_count == 1
    assert first.machine_layer_line_count == 2


def test_format_outputs(notebook_dir: Path, tmp_path: Path) -> None:
    inbox = tmp_path / "inbox.md"
    inbox.write_text("", encoding="utf-8")
    index = tmp_path / "threads.md"
    index.write_text("", encoding="utf-8")

    report = build_report(
        notebook_dir=notebook_dir,
        threads_index=index,
        inbox_path=inbox,
        lookback_days=7,
        today=date(2026, 4, 18),
    )

    md = format_markdown(report)
    assert "# Strategy thread quality report" in md
    assert "Stale threads" in md

    js = format_json(report)
    data = json.loads(js)
    assert "summary" in data
    assert "experts" in data
