"""Unit tests for validate_strategy_expert_threads.py."""

from __future__ import annotations

import textwrap

from pathlib import Path

from scripts.validate_strategy_expert_threads import (
    OPT_OUT_BULLETS_LEDGER,
    analyze_month_body,
    iter_month_h2_bodies,
    validate_thread_file,
)


def test_iter_month_h2_bodies_splits_months(tmp_path: Path) -> None:
    human = textwrap.dedent(
        """\
        ## Segment 1 — x

        ## 2026-01
        - a
        - b

        ## 2026-02
        Para line with enough chars here.

        ## 2026-03
        - only
        - bullets
        - here
        """
    )
    blocks = iter_month_h2_bodies(human)
    assert [m for m, _ in blocks] == ["2026-01", "2026-02", "2026-03"]
    assert "- a" in blocks[0][1]
    assert "Para line" in blocks[1][1]


def test_analyze_month_body_counts_bullets_and_prose() -> None:
    b, p = analyze_month_body(
        "- one\n- two\n- three\n\nSome prose line that is long enough.\n"
    )
    assert b == 3
    assert p == 1


def test_validate_thread_file_warns_bullet_only_month(tmp_path: Path) -> None:
    p = tmp_path / "strategy-expert-test-expert-thread.md"
    p.write_text(
        textwrap.dedent(
            """\
            # Expert thread

            ## 2026-01
            - [strength: high] a
            - [strength: high] b
            - [strength: high] c

            <!-- strategy-expert-thread:start -->
            machine
            <!-- strategy-expert-thread:end -->
            """
        ),
        encoding="utf-8",
    )
    warns = validate_thread_file(p)
    assert len(warns) == 1
    assert "2026-01" in warns[0]


def test_validate_thread_file_opt_out_suppresses(tmp_path: Path) -> None:
    p = tmp_path / "strategy-expert-test-expert-thread.md"
    p.write_text(
        textwrap.dedent(
            f"""\
            # Expert thread
            {OPT_OUT_BULLETS_LEDGER}

            ## 2026-01
            - [strength: high] a
            - [strength: high] b
            - [strength: high] c

            <!-- strategy-expert-thread:start -->
            x
            <!-- strategy-expert-thread:end -->
            """
        ),
        encoding="utf-8",
    )
    assert validate_thread_file(p) == []


def test_validate_thread_file_prose_mixed_ok(tmp_path: Path) -> None:
    p = tmp_path / "strategy-expert-test-expert-thread.md"
    p.write_text(
        textwrap.dedent(
            """\
            # Expert thread

            ## 2026-01
            This month opened with a clear arc in the Gulf narrative space.

            - [strength: high] a
            - [strength: high] b
            - [strength: high] c

            <!-- strategy-expert-thread:start -->
            x
            <!-- strategy-expert-thread:end -->
            """
        ),
        encoding="utf-8",
    )
    assert validate_thread_file(p) == []
