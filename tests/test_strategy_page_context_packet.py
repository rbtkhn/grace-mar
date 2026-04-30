"""Tests for bounded thread-context packet generation."""

from __future__ import annotations

from pathlib import Path

from scripts.strategy import build_crooke_refined_pages as crooke_builder
from scripts.strategy.page_context_packet import (
    build_thread_context_packet,
    context_packet_path,
    render_thread_context_packet,
)


def test_thread_context_packet_uses_previous_months_and_classifies_snippets(
    tmp_path: Path,
) -> None:
    thread = tmp_path / "thread.md"
    thread.write_text(
        """# Expert thread

## 2026-01
Crooke says Iran remains resilient and time is on the side of the Iranians.

Open question about sanctions and whether Trump can manage the conflict.

## 2026-02
However, there is a contradiction over the blockade and the response path.

New tactic emerges as the argument shifts toward economic cost.

## 2026-03
Iran remains an anchor for the lane and still matters for later pages.
""",
        encoding="utf-8",
    )

    packet = build_thread_context_packet(
        expert_id="crooke",
        page_date="2026-04-27",
        thread_paths=[thread],
        page_title="Iran / Hormuz update",
    )

    assert packet.source_months == ["2026-01", "2026-02", "2026-03"]
    assert "selected the last 3 prior month segment(s) before 2026-04" in packet.selection_note
    assert any("open question" in s.lower() for s in packet.unresolved)
    assert any("contradiction" in s.lower() or "blockade" in s.lower() for s in packet.contradicted)
    assert any("new tactic" in s.lower() or "shifts" in s.lower() for s in packet.newly_changed)
    assert any("remains an anchor" in s.lower() or "still matters" in s.lower() for s in packet.settled)
    assert any("iran" in theme.lower() for theme in packet.recurring_themes)

    rendered = render_thread_context_packet(packet)
    assert "Thread context packet" in rendered
    assert "## Month briefs" in rendered
    assert "## Drafting guidance" in rendered


def test_thread_context_packet_falls_back_when_no_prior_month_exists(
    tmp_path: Path,
) -> None:
    thread = tmp_path / "thread.md"
    thread.write_text(
        """# Expert thread

## 2026-01
Initial month anchor. Iran remains the frame.
""",
        encoding="utf-8",
    )

    packet = build_thread_context_packet(
        expert_id="crooke",
        page_date="2026-01-08",
        thread_paths=[thread],
    )

    assert packet.source_months == ["2026-01"]
    assert "fell back" in packet.selection_note
    assert packet.month_contexts[0].month == "2026-01"


def test_crooke_builder_surfaces_context_packet_link(
    tmp_path: Path,
    monkeypatch,
) -> None:
    notebook = tmp_path / "notebook"
    raw_dir = notebook / "raw-input" / "2026-04-27"
    crooke_dir = notebook / "experts" / "crooke"
    raw_dir.mkdir(parents=True)
    crooke_dir.mkdir(parents=True)

    raw = raw_dir / "substack-crooke-example-2026-04-27.md"
    raw.write_text(
        """---
pub_date: 2026-04-27
thread: crooke
source_url: https://example.com/crooke
title: Example Crooke Piece
---

# Example Crooke Piece
""",
        encoding="utf-8",
    )
    (crooke_dir / "thread.md").write_text(
        """# Crooke thread

## 2026-01
Base line.
""",
        encoding="utf-8",
    )

    monkeypatch.setattr(crooke_builder, "NOTEBOOK", notebook)
    monkeypatch.setattr(crooke_builder, "RAW", notebook / "raw-input")
    monkeypatch.setattr(crooke_builder, "CROOKE", crooke_dir)
    monkeypatch.setattr(crooke_builder, "MANIFEST_PATH", crooke_dir / "crooke-pages-manifest.yaml")

    entries = crooke_builder.build_entries([raw])
    assert entries[0]["page_filename"] == "crooke-page-2026-04-27-example.md"
    assert entries[0]["context_packet_relative"] == "page-context/crooke-page-2026-04-27-example.context.md"

    scaffold = crooke_builder.render_scaffold(entries[0])
    assert "Context packet:" in scaffold
    assert "prior-month thread distillation" in scaffold

    packet_path = context_packet_path(crooke_dir, entries[0]["page_filename"])
    assert packet_path.parent.name == "page-context"
