"""Tests for the hybrid retrieval layer: scoring, surface dispatch, CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_RUNTIME = REPO_ROOT / "scripts" / "runtime"

sys.path.insert(0, str(SCRIPTS_RUNTIME))
import hybrid_scoring as hs  # noqa: E402


# ── hybrid_scoring unit tests ─────────────────────────────────────────


class TestTokenize:
    def test_basic_tokenization(self) -> None:
        tokens = hs.tokenize("The quick brown fox jumps over the lazy dog")
        assert "quick" in tokens
        assert "brown" in tokens
        assert "the" not in tokens  # stop word

    def test_empty_string(self) -> None:
        assert hs.tokenize("") == []


class TestTermOverlap:
    def test_full_overlap(self) -> None:
        q = ["sovereignty", "lecture"]
        d = ["sovereignty", "lecture", "jiang", "history"]
        assert hs.term_overlap_score(q, d) == 1.0

    def test_partial_overlap(self) -> None:
        q = ["sovereignty", "lecture", "missing"]
        d = ["sovereignty", "lecture", "jiang"]
        score = hs.term_overlap_score(q, d)
        assert abs(score - 2.0 / 3.0) < 0.01

    def test_no_overlap(self) -> None:
        assert hs.term_overlap_score(["alpha"], ["beta"]) == 0.0

    def test_empty_query(self) -> None:
        assert hs.term_overlap_score([], ["beta"]) == 0.0


class TestTfidfCosine:
    def test_identical_docs(self) -> None:
        tokens = ["foo", "bar", "baz"]
        idf = hs.build_idf([tokens, tokens])
        score = hs.tfidf_cosine(tokens, tokens, idf)
        assert score > 0.99

    def test_disjoint_docs(self) -> None:
        idf = hs.build_idf([["alpha"], ["beta"]])
        assert hs.tfidf_cosine(["alpha"], ["beta"], idf) == 0.0

    def test_partial_match_ordering(self) -> None:
        all_docs = [
            ["jiang", "sovereignty", "lecture", "history"],
            ["cooking", "recipe", "cake", "flour"],
            ["jiang", "sovereignty"],
        ]
        idf = hs.build_idf(all_docs + [["jiang", "sovereignty"]])
        s1 = hs.tfidf_cosine(["jiang", "sovereignty"], all_docs[0], idf)
        s2 = hs.tfidf_cosine(["jiang", "sovereignty"], all_docs[1], idf)
        s3 = hs.tfidf_cosine(["jiang", "sovereignty"], all_docs[2], idf)
        assert s1 > s2
        assert s3 > s2


class TestNormalizeScores:
    def test_spread(self) -> None:
        normed = hs.normalize_scores([1.0, 5.0, 10.0])
        assert normed[0] == 0.0
        assert normed[-1] == 1.0

    def test_single_value(self) -> None:
        normed = hs.normalize_scores([3.0])
        assert normed == [1.0]

    def test_all_zero(self) -> None:
        normed = hs.normalize_scores([0.0, 0.0])
        assert normed == [0.0, 0.0]

    def test_empty(self) -> None:
        assert hs.normalize_scores([]) == []


class TestSemanticHook:
    def test_stub_returns_zero(self) -> None:
        assert hs.semantic_score("any query", "any text") == 0.0

    def test_not_available(self) -> None:
        assert hs.semantic_available() is False


class TestRecency:
    def test_recent_timestamp_high(self) -> None:
        now = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
        one_hour_ago = "2026-04-18T11:00:00Z"
        score = hs.recency_from_iso(one_hour_ago, now=now)
        assert score > 0.95

    def test_old_timestamp_low(self) -> None:
        now = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
        two_weeks_ago = "2026-04-04T12:00:00Z"
        score = hs.recency_from_iso(two_weeks_ago, now=now)
        assert score == 0.0

    def test_none_returns_zero(self) -> None:
        assert hs.recency_from_iso(None) == 0.0

    def test_mtime_recent(self) -> None:
        now = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
        mtime = now.timestamp() - 3600  # 1 hour ago
        score = hs.recency_from_mtime(mtime, now=now)
        assert score > 0.95

    def test_mtime_old(self) -> None:
        now = datetime(2026, 4, 18, 12, 0, 0, tzinfo=timezone.utc)
        mtime = now.timestamp() - 14 * 86400  # 14 days ago
        score = hs.recency_from_mtime(mtime, now=now)
        assert score == 0.0


class TestCombineScores:
    def test_default_weights_no_semantic(self) -> None:
        score = hs.combine_scores(1.0, 0.0, 1.0, semantic_active=False)
        # w_lex=0.95, w_rec=0.05 when semantic inactive
        assert abs(score - 1.0) < 0.01

    def test_with_semantic(self) -> None:
        score = hs.combine_scores(1.0, 1.0, 1.0, semantic_active=True)
        assert abs(score - 1.0) < 0.01

    def test_custom_weights(self) -> None:
        score = hs.combine_scores(1.0, 0.0, 0.0, weights=(1.0, 0.0, 0.0), semantic_active=False)
        assert abs(score - 1.0) < 0.01

    def test_recency_alone(self) -> None:
        score = hs.combine_scores(0.0, 0.0, 1.0, weights=(0.0, 0.0, 1.0), semantic_active=False)
        assert abs(score - 1.0) < 0.01

    def test_recency_modest_influence(self) -> None:
        no_recency = hs.combine_scores(0.8, 0.0, 0.0, semantic_active=False)
        with_recency = hs.combine_scores(0.8, 0.0, 1.0, semantic_active=False)
        diff = with_recency - no_recency
        assert 0 < diff < 0.10  # recency influence is small


# ── CLI integration tests ─────────────────────────────────────────────

def _run_cli(*extra_args: str) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCRIPTS_RUNTIME / "hybrid_retrieve.py"), *extra_args]
    return subprocess.run(cmd, capture_output=True, text=True)


class TestCLI:
    def test_unsupported_surface_rejected(self) -> None:
        result = _run_cli("--surface", "invalid_surface", "--query", "test")
        assert result.returncode != 0
        assert "invalid surface" in result.stderr.lower()

    def test_semantic_on_rejected_in_v1(self) -> None:
        result = _run_cli(
            "--surface", "prepared_context",
            "--query", "test",
            "--use-semantic", "on",
        )
        assert result.returncode != 0
        assert "not available" in result.stderr.lower()

    def test_json_output_shape(self) -> None:
        result = _run_cli(
            "--surface", "artifact_lookup",
            "--query", "skill card strategy",
            "--json",
            "--top-k", "2",
        )
        assert result.returncode == 0
        out = json.loads(result.stdout)
        assert "query" in out
        assert "surface" in out
        assert "semantic_active" in out
        assert isinstance(out["results"], list)
        assert out["surface"] == "artifact_lookup"
        for r in out["results"]:
            assert "path" in r
            assert "final_score" in r
            assert "lexical_score" in r
            assert "semantic_score" in r
            assert "recency_score" in r
            assert "matched_terms" in r

    def test_text_output_runs(self) -> None:
        result = _run_cli(
            "--surface", "notebook_lookup",
            "--query", "Iran sanctions",
            "--top-k", "1",
        )
        assert result.returncode == 0

    def test_recency_off_flag(self) -> None:
        result = _run_cli(
            "--surface", "artifact_lookup",
            "--query", "test",
            "--use-recency", "off",
            "--json",
        )
        assert result.returncode == 0
        out = json.loads(result.stdout)
        for r in out["results"]:
            assert r["recency_score"] == 0.0

    def test_custom_weights(self) -> None:
        result = _run_cli(
            "--surface", "artifact_lookup",
            "--query", "test",
            "--weights", "1.0,0.0,0.0",
            "--json",
        )
        assert result.returncode == 0

    def test_bad_weights_rejected(self) -> None:
        result = _run_cli(
            "--surface", "artifact_lookup",
            "--query", "test",
            "--weights", "bad",
        )
        assert result.returncode != 0


# ── lexical ordering test (fixture-based) ─────────────────────────────

class TestLexicalOrdering:
    def test_better_match_ranks_higher(self, tmp_path: Path) -> None:
        """A file with more query terms scores higher than one with fewer."""
        (tmp_path / "strong.md").write_text("# Jiang sovereignty lecture\nDetailed analysis of sovereignty.")
        (tmp_path / "weak.md").write_text("# Cooking recipes\nHow to make pasta and bread.")

        sys.path.insert(0, str(SCRIPTS_RUNTIME))
        from hybrid_retrieve import _scan_md_files

        results = _scan_md_files(
            tmp_path, "Jiang sovereignty lecture", 5, "notebook_lookup",
            use_recency=False, weights=(1.0, 0.0, 0.0),
        )
        if len(results) >= 2:
            assert results[0].path.endswith("strong.md") or "strong" in results[0].path
            assert results[0].final_score > results[1].final_score

    def test_recency_boosts_recent_file(self, tmp_path: Path) -> None:
        """With recency on, a newer file with the same content ranks higher."""
        import os

        content = "# Strategy notebook entry\nIran sanctions analysis and framing."
        (tmp_path / "old.md").write_text(content)
        os.utime(tmp_path / "old.md", (0, 0))  # epoch = very old
        (tmp_path / "new.md").write_text(content)
        # new.md keeps its natural mtime (just created = very recent)

        from hybrid_retrieve import _scan_md_files

        results = _scan_md_files(
            tmp_path, "Iran sanctions", 5, "notebook_lookup",
            use_recency=True, weights=(0.80, 0.0, 0.20),
        )

        assert len(results) == 2
        by_name = {r.meta["filename"]: r for r in results}
        assert by_name["new.md"].recency_score > by_name["old.md"].recency_score
        assert by_name["new.md"].final_score > by_name["old.md"].final_score
