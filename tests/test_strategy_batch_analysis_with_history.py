"""Tests for scripts/strategy_batch_analysis_with_history.py."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from scripts import strategy_batch_analysis_with_history as mod


def test_find_snapshot_rows_prefers_batch_analysis_refs() -> None:
    snap = {
        "batch_analysis_refs": [
            {
                "expert_ids": ["ritter", "davis"],
                "date": "2026-04-14",
            },
            {"expert_ids": ["other"], "date": "x"},
        ]
    }
    rows = mod.find_snapshot_rows(snap, "ritter", "davis")
    assert len(rows) == 1
    assert rows[0]["date"] == "2026-04-14"


def test_find_snapshot_rows_fallback_substring() -> None:
    snap = {
        "rows": [
            {"note": "crosses ritter and davis in raw text"},
        ]
    }
    rows = mod.find_snapshot_rows(snap, "ritter", "davis")
    assert len(rows) == 1


def test_find_snapshot_rows_plain_list() -> None:
    snap = [
        {"expert_ids": ["davis", "ritter"], "label": "pair"},
    ]
    rows = mod.find_snapshot_rows(snap, "ritter", "davis")
    assert len(rows) == 1


def test_compact_block_regex_extracts_fence_body() -> None:
    md = """## Historical stance summary
- one
```text
historical-expert-context | expert-a | stance=x
```
"""
    m = mod.COMPACT_BLOCK_RE.search(md)
    assert m is not None
    assert "historical-expert-context | expert-a" in m.group(1)


def test_load_historical_context_stance_preview(tmp_path: Path) -> None:
    hist_file = tmp_path / "ritter-2026-01-to-2026-03.md"
    hist_file.write_text(
        """## Historical stance summary
- first bullet
- second bullet
- third bullet
- fourth bullet
- fifth should not appear in preview

## Other section
""",
        encoding="utf-8",
    )
    with patch.object(mod, "REPO_ROOT", tmp_path), patch.object(mod, "HISTORY_DIR", tmp_path):
        ctx = mod.load_historical_context("ritter", "2026-01", "2026-03")
    assert len(ctx.preview_lines) == 4
    assert ctx.preview_lines[0] == "first bullet"


def test_iter_month_segments_inclusive() -> None:
    assert mod.iter_month_segments("2026-01", "2026-03") == ["2026-01", "2026-02", "2026-03"]
    assert mod.iter_month_segments("2025-11", "2026-02") == [
        "2025-11",
        "2025-12",
        "2026-01",
        "2026-02",
    ]


def test_load_historical_context_prefers_segment_files(tmp_path: Path) -> None:
    seg_dir = tmp_path / "ritter"
    seg_dir.mkdir()
    for month, tag in (
        ("2026-01", "alpha"),
        ("2026-02", "beta"),
        ("2026-03", "gamma"),
    ):
        (seg_dir / f"{month}.md").write_text(
            f"""## Historical stance summary
- stance {tag} one
- stance {tag} two

## Prompt-ready compact block
```text
historical-expert-context | ritter | stance={tag}
```
""",
            encoding="utf-8",
        )
    rollup = tmp_path / "ritter-2026-01-to-2026-03.md"
    rollup.write_text(
        """## Historical stance summary
- rollup only

## Prompt-ready compact block
```text
historical-expert-context | ritter | stance=ROLLUP
```
""",
        encoding="utf-8",
    )
    with patch.object(mod, "REPO_ROOT", tmp_path), patch.object(mod, "HISTORY_DIR", tmp_path):
        ctx = mod.load_historical_context("ritter", "2026-01", "2026-03")
    assert ctx.compact_block is not None
    assert "stance=alpha" in ctx.compact_block
    assert "stance=beta" in ctx.compact_block
    assert "stance=gamma" in ctx.compact_block
    assert "ROLLUP" not in ctx.compact_block
    assert ctx.preview_lines[0] == "stance alpha one"


def test_load_historical_context_falls_back_when_segment_incomplete(tmp_path: Path) -> None:
    seg_dir = tmp_path / "ritter"
    seg_dir.mkdir()
    (seg_dir / "2026-01.md").write_text(
        """## Historical stance summary
- seg only

## Prompt-ready compact block
```text
historical-expert-context | ritter | stance=SEG
```
""",
        encoding="utf-8",
    )
    rollup = tmp_path / "ritter-2026-01-to-2026-03.md"
    rollup.write_text(
        """## Historical stance summary
- from rollup

## Prompt-ready compact block
```text
historical-expert-context | ritter | stance=ROLLUP_OK
```
""",
        encoding="utf-8",
    )
    with patch.object(mod, "REPO_ROOT", tmp_path), patch.object(mod, "HISTORY_DIR", tmp_path):
        ctx = mod.load_historical_context("ritter", "2026-01", "2026-03")
    assert ctx.compact_block is not None
    assert "ROLLUP_OK" in ctx.compact_block
    assert "SEG" not in ctx.compact_block


def test_main_requires_dry_run_or_apply() -> None:
    import subprocess

    r = subprocess.run(
        [
            "python3",
            str(mod.REPO_ROOT / "scripts" / "strategy_batch_analysis_with_history.py"),
            "--pair",
            "a,b",
            "--history-start",
            "2026-01",
            "--history-end",
            "2026-03",
        ],
        capture_output=True,
        text=True,
        cwd=mod.REPO_ROOT,
    )
    assert r.returncode == 2
