"""Tests for the pages-in-threads architecture: expert_paths, migration,
page reader, page composer, weave analysis, watch tool, and thread updates.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def notebook(tmp_path: Path) -> Path:
    """Create a minimal notebook directory with expert folders."""
    nb = tmp_path / "strategy-notebook"
    for eid in ("pape", "ritter", "davis"):
        d = nb / "experts" / eid
        d.mkdir(parents=True)
        (d / "profile.md").write_text(f"# Expert profile — `{eid}`\n", encoding="utf-8")
        (d / "transcript.md").write_text(
            f"# Expert transcript — `{eid}`\n\n"
            "<!-- Triage appends new date sections below. Do not add content above this line. -->\n"
            "\n## 2026-04-14\n- test line thread:{eid}\n",
            encoding="utf-8",
        )
        thread_content = textwrap.dedent(f"""\
            # Expert thread — `{eid}`

            ## 2026-04

            <!-- strategy-expert-thread:start -->
            ## Machine layer — Extraction (script-maintained)

            _(test placeholder)_
            <!-- strategy-expert-thread:end -->
        """)
        (d / "thread.md").write_text(thread_content, encoding="utf-8")
    return nb


@pytest.fixture()
def notebook_with_pages(notebook: Path) -> Path:
    """Notebook with pre-inserted pages in thread files."""
    pape_thread = notebook / "experts" / "pape" / "thread.md"
    text = pape_thread.read_text(encoding="utf-8")
    page_block = textwrap.dedent("""\
        <!-- strategy-page:start id="escalation-blockade" date="2026-04-16" watch="hormuz" -->
        ### Page: escalation-blockade

        **Date:** 2026-04-16
        **Watch:** hormuz
        **Also in:** ritter

        Test page content for pape.
        <!-- strategy-page:end -->
    """)
    text = text.replace(
        "## 2026-04\n",
        f"## 2026-04\n\n{page_block}\n",
    )
    pape_thread.write_text(text, encoding="utf-8")

    ritter_thread = notebook / "experts" / "ritter" / "thread.md"
    text = ritter_thread.read_text(encoding="utf-8")
    page_block_r = textwrap.dedent("""\
        <!-- strategy-page:start id="escalation-blockade" date="2026-04-16" watch="hormuz" -->
        ### Page: escalation-blockade

        **Date:** 2026-04-16
        **Watch:** hormuz
        **Also in:** pape

        Test page content for ritter.
        <!-- strategy-page:end -->
    """)
    text = text.replace(
        "## 2026-04\n",
        f"## 2026-04\n\n{page_block_r}\n",
    )
    ritter_thread.write_text(text, encoding="utf-8")

    return notebook


# ---------------------------------------------------------------------------
# expert_paths
# ---------------------------------------------------------------------------

class TestExpertPaths:
    def test_returns_correct_structure(self, notebook: Path):
        from strategy_expert_corpus import expert_paths
        paths = expert_paths("pape", notebook)
        assert paths["profile"] == notebook / "experts" / "pape" / "profile.md"
        assert paths["transcript"] == notebook / "experts" / "pape" / "transcript.md"
        assert paths["thread"] == notebook / "experts" / "pape" / "thread.md"
        assert paths["mind"] == notebook / "experts" / "pape" / "mind.md"


# ---------------------------------------------------------------------------
# Page reader
# ---------------------------------------------------------------------------

class TestPageReader:
    def test_discover_pages_empty(self, notebook: Path):
        from strategy_page_reader import discover_pages
        pages = discover_pages(notebook / "experts" / "davis" / "thread.md", "davis")
        assert pages == []

    def test_discover_pages_with_content(self, notebook_with_pages: Path):
        from strategy_page_reader import discover_pages
        pages = discover_pages(
            notebook_with_pages / "experts" / "pape" / "thread.md", "pape"
        )
        assert len(pages) == 1
        assert pages[0].id == "escalation-blockade"
        assert pages[0].date == "2026-04-16"
        assert pages[0].watch == "hormuz"
        assert pages[0].expert_id == "pape"
        assert "Test page content for pape" in pages[0].content

    def test_discover_pages_missing_file(self, tmp_path: Path):
        from strategy_page_reader import discover_pages
        pages = discover_pages(tmp_path / "nonexistent.md", "x")
        assert pages == []

    def test_page_metadata_parsing(self, notebook_with_pages: Path):
        from strategy_page_reader import discover_pages
        pages = discover_pages(
            notebook_with_pages / "experts" / "ritter" / "thread.md", "ritter"
        )
        assert len(pages) == 1
        p = pages[0]
        assert p.id == "escalation-blockade"
        assert p.watch == "hormuz"
        assert p.expert_id == "ritter"

    def test_multi_expert_same_page_id(self, notebook_with_pages: Path):
        from strategy_page_reader import discover_pages
        pape_pages = discover_pages(
            notebook_with_pages / "experts" / "pape" / "thread.md", "pape"
        )
        ritter_pages = discover_pages(
            notebook_with_pages / "experts" / "ritter" / "thread.md", "ritter"
        )
        assert pape_pages[0].id == ritter_pages[0].id == "escalation-blockade"
        assert pape_pages[0].expert_id == "pape"
        assert ritter_pages[0].expert_id == "ritter"

    def test_discover_all_pages_aggregates_monthly_thread_files(self, tmp_path: Path):
        from strategy_page_reader import discover_all_pages

        nb = tmp_path / "nb"
        eid = "pape"
        d = nb / "experts" / eid
        d.mkdir(parents=True)
        fence_march = (
            '<!-- strategy-page:start id="march-only" date="2026-03-15" watch="" -->\n'
            "### Page: march-only\n<!-- strategy-page:end -->"
        )
        (d / f"{eid}-thread-2026-03.md").write_text(
            f"## 2026-03\n\n{fence_march}\n\n"
            "<!-- strategy-expert-thread:start -->\n<!-- strategy-expert-thread:end -->\n",
            encoding="utf-8",
        )
        fence_april = (
            '<!-- strategy-page:start id="april-only" date="2026-04-01" watch="" -->\n'
            "### Page: april-only\n<!-- strategy-page:end -->"
        )
        (d / f"{eid}-thread-2026-04.md").write_text(
            f"## 2026-04\n\n{fence_april}\n\n"
            "<!-- strategy-expert-thread:start -->\n<!-- strategy-expert-thread:end -->\n",
            encoding="utf-8",
        )
        all_p = discover_all_pages(nb)
        assert eid in all_p
        ids = {p.id for p in all_p[eid]}
        assert ids == {"march-only", "april-only"}


# ---------------------------------------------------------------------------
# Page composition (strategy_page.py)
# ---------------------------------------------------------------------------

class TestPageComposer:
    def test_build_page_block(self):
        from strategy_page import build_page_block
        block = build_page_block(
            page_id="test-page",
            page_date="2026-04-18",
            watch="hormuz",
            experts=["davis", "barnes"],
            current_expert="davis",
            inbox_lines=["- test inbox line thread:davis"],
        )
        assert '<!-- strategy-page:start id="test-page"' in block
        assert "**Watch:** hormuz" in block
        assert "**Also in:** barnes" in block
        assert "<!-- strategy-page:end -->" in block

    def test_insert_page_creates_chapter(self, notebook: Path):
        from strategy_page import insert_page
        thread_path = notebook / "experts" / "davis" / "thread.md"
        page_block = textwrap.dedent("""\
            <!-- strategy-page:start id="test" date="2026-05-01" watch="" -->
            ### Page: test
            <!-- strategy-page:end -->""")
        result = insert_page(thread_path, "2026-05", page_block, dry_run=False)
        assert "inserted" in result
        text = thread_path.read_text(encoding="utf-8")
        assert "## 2026-05" in text
        assert '<!-- strategy-page:start id="test"' in text

    def test_insert_page_dry_run(self, notebook: Path):
        from strategy_page import insert_page
        thread_path = notebook / "experts" / "davis" / "thread.md"
        original = thread_path.read_text(encoding="utf-8")
        page_block = '<!-- strategy-page:start id="x" date="2026-04-18" watch="" -->\n<!-- strategy-page:end -->'
        result = insert_page(thread_path, "2026-04", page_block, dry_run=True)
        assert "would insert" in result
        assert thread_path.read_text(encoding="utf-8") == original

    def test_insert_page_into_existing_chapter(self, notebook: Path):
        from strategy_page import insert_page
        thread_path = notebook / "experts" / "pape" / "thread.md"
        page_block = '<!-- strategy-page:start id="new-page" date="2026-04-18" watch="test" -->\n### Page: new-page\n<!-- strategy-page:end -->'
        insert_page(thread_path, "2026-04", page_block, dry_run=False)
        text = thread_path.read_text(encoding="utf-8")
        assert '<!-- strategy-page:start id="new-page"' in text
        assert text.index("new-page") < text.index("strategy-expert-thread:start")

    def test_insert_page_targets_monthly_thread_file(self, tmp_path: Path):
        from strategy_expert_corpus import thread_path_for_page_month
        from strategy_page import insert_page

        nb = tmp_path / "nb"
        eid = "pape"
        d = nb / "experts" / eid
        d.mkdir(parents=True)
        (d / f"{eid}-thread-2026-04.md").write_text(
            "# Expert thread\n\n## 2026-04\n\n"
            "<!-- strategy-expert-thread:start -->\n"
            "<!-- strategy-expert-thread:end -->\n",
            encoding="utf-8",
        )
        tp = thread_path_for_page_month(nb, eid, "2026-04")
        assert tp == d / f"{eid}-thread-2026-04.md"
        page_block = (
            '<!-- strategy-page:start id="monthly-page" date="2026-04-20" watch="" -->\n'
            "### Page: monthly-page\n<!-- strategy-page:end -->"
        )
        insert_page(tp, "2026-04", page_block, dry_run=False)
        text = tp.read_text(encoding="utf-8")
        assert 'id="monthly-page"' in text


# ---------------------------------------------------------------------------
# Weave analysis
# ---------------------------------------------------------------------------

class TestWeave:
    def test_classify_args(self, notebook_with_pages: Path):
        from strategy_weave import classify_args
        experts, watches, keywords = classify_args(
            ["pape", "hormuz", "blockade"], notebook_with_pages
        )
        assert "pape" in experts
        assert "hormuz" in watches
        assert "blockade" in keywords

    def test_classify_unknown_expert(self, notebook_with_pages: Path):
        from strategy_weave import classify_args
        experts, watches, keywords = classify_args(
            ["nonexistent"], notebook_with_pages
        )
        assert experts == []
        assert "nonexistent" in keywords

    def test_gather_pages(self, notebook_with_pages: Path):
        from strategy_weave import _gather_pages
        pages = _gather_pages(["pape"], [], notebook_with_pages)
        assert len(pages) == 1
        assert pages[0].id == "escalation-blockade"

    def test_gather_pages_by_watch(self, notebook_with_pages: Path):
        from strategy_weave import _gather_pages
        pages = _gather_pages([], ["hormuz"], notebook_with_pages)
        assert len(pages) >= 2


# ---------------------------------------------------------------------------
# Watch tool
# ---------------------------------------------------------------------------

class TestWatch:
    def test_list_watches_empty(self, notebook: Path):
        from strategy_watch import list_watches
        watches = list_watches(notebook)
        assert watches == []

    def test_list_watches_with_pages(self, notebook_with_pages: Path):
        from strategy_watch import list_watches
        watches = list_watches(notebook_with_pages)
        assert len(watches) == 1
        assert watches[0]["watch"] == "hormuz"
        assert watches[0]["page_count"] == 2
        assert set(watches[0]["experts"]) == {"pape", "ritter"}

    def test_watch_detail(self, notebook_with_pages: Path):
        from strategy_watch import watch_detail
        connections_path = notebook_with_pages / "knot-connections.yaml"
        connections_path.write_text(
            "schema_version: 1\nconnections: []\n", encoding="utf-8"
        )
        detail = watch_detail("hormuz", notebook_with_pages, connections_path)
        assert detail["watch"] == "hormuz"
        assert "pape" in detail["experts"]
        assert "ritter" in detail["experts"]

    def test_tension_detection(self, notebook_with_pages: Path):
        from strategy_watch import find_tensions_for_watch, _load_tensions
        connections_path = notebook_with_pages / "knot-connections.yaml"
        connections_path.write_text(textwrap.dedent("""\
            schema_version: 1
            connections:
              - from: a.md
                to: b.md
                relation: tension
                reason: "test tension"
                warrant:
                  - "shared-watch:hormuz"
        """), encoding="utf-8")
        tensions = _load_tensions(connections_path)
        assert len(tensions) == 1

        from strategy_page_reader import pages_for_watch
        wp = pages_for_watch(notebook_with_pages, "hormuz")
        relevant = find_tensions_for_watch("hormuz", wp, tensions)
        assert len(relevant) == 1
        assert relevant[0]["reason"] == "test tension"

    def test_format_watches_markdown(self):
        from strategy_watch import format_watches_markdown
        watches = [
            {"watch": "hormuz", "page_count": 3, "experts": ["pape", "ritter"], "dates": ["2026-04-14", "2026-04-16"]},
        ]
        md = format_watches_markdown(watches)
        assert "hormuz" in md
        assert "pape, ritter" in md

    def test_format_watches_empty(self):
        from strategy_watch import format_watches_markdown
        md = format_watches_markdown([])
        assert "No watches found" in md


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------

class TestMigration:
    def test_phase_folder_dry_run(self, tmp_path: Path):
        nb = tmp_path / "strategy-notebook"
        nb.mkdir()
        (nb / "strategy-expert-pape.md").write_text("# profile\n", encoding="utf-8")
        (nb / "strategy-expert-pape-thread.md").write_text("# thread\n", encoding="utf-8")
        (nb / "strategy-expert-pape-transcript.md").write_text("# transcript\n", encoding="utf-8")

        import importlib
        import migrate_knots_to_pages as mkp
        orig_notebook = mkp.NOTEBOOK_DIR
        mkp.NOTEBOOK_DIR = nb
        try:
            actions = mkp.phase_folder(dry_run=True)
        finally:
            mkp.NOTEBOOK_DIR = orig_notebook

        assert any("would move" in a for a in actions)
        assert (nb / "strategy-expert-pape.md").is_file()
        assert not (nb / "experts" / "pape" / "profile.md").exists()

    def test_phase_folder_apply(self, tmp_path: Path):
        nb = tmp_path / "strategy-notebook"
        nb.mkdir()
        (nb / "strategy-expert-davis.md").write_text("# profile\n", encoding="utf-8")
        (nb / "strategy-expert-davis-thread.md").write_text("# thread\n", encoding="utf-8")

        import migrate_knots_to_pages as mkp
        orig_notebook = mkp.NOTEBOOK_DIR
        mkp.NOTEBOOK_DIR = nb
        try:
            actions = mkp.phase_folder(dry_run=False)
        finally:
            mkp.NOTEBOOK_DIR = orig_notebook

        assert any("moved" in a for a in actions)
        assert (nb / "experts" / "davis" / "profile.md").is_file()
        assert (nb / "experts" / "davis" / "thread.md").is_file()
        assert not (nb / "strategy-expert-davis.md").exists()


# ---------------------------------------------------------------------------
# Thread update (page candidate suggestion)
# ---------------------------------------------------------------------------

class TestThreadUpdate:
    def test_suggest_page_candidates(self, notebook_with_pages: Path):
        from strategy_thread import _suggest_page_candidates
        suggestions = _suggest_page_candidates(notebook_with_pages)
        assert len(suggestions) >= 1
        assert any("escalation-blockade" in s for s in suggestions)
        assert any("pape" in s and "ritter" in s for s in suggestions)

    def test_no_candidates_without_shared_pages(self, notebook: Path):
        from strategy_thread import _suggest_page_candidates
        suggestions = _suggest_page_candidates(notebook)
        assert suggestions == []
