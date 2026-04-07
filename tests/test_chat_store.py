"""Tests for bot/chat_store.py — persistent conversation store."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Make bot importable when running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Patch DB_PATH before import to use a temp file
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp_db.close()
_TMP_DB_PATH = Path(_tmp_db.name)


@pytest.fixture(autouse=True)
def _clean_db():
    """Reset DB for each test."""
    import bot.chat_store as cs

    cs.DB_PATH = _TMP_DB_PATH
    cs.init_db()
    yield
    conn = cs._get_conn()
    try:
        conn.execute("DELETE FROM chat_messages")
        conn.execute("DELETE FROM chat_summaries")
        conn.commit()
    finally:
        conn.close()


def _cs():
    import bot.chat_store as cs
    cs.DB_PATH = _TMP_DB_PATH
    return cs


class TestStoreAndLoad:
    def test_store_and_load_recent(self):
        cs = _cs()
        cs.store_message("test:1", "user", "hello")
        cs.store_message("test:1", "assistant", "hi there")
        msgs = cs.load_recent("test:1", limit=10)
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"
        assert msgs[0]["content"] == "hello"
        assert msgs[1]["role"] == "assistant"
        assert msgs[1]["content"] == "hi there"

    def test_load_recent_limit(self):
        cs = _cs()
        for i in range(10):
            cs.store_message("test:2", "user", f"msg {i}")
        msgs = cs.load_recent("test:2", limit=3)
        assert len(msgs) == 3
        assert msgs[-1]["content"] == "msg 9"

    def test_channel_isolation(self):
        cs = _cs()
        cs.store_message("ch:a", "user", "alpha")
        cs.store_message("ch:b", "user", "beta")
        assert len(cs.load_recent("ch:a")) == 1
        assert len(cs.load_recent("ch:b")) == 1
        assert cs.load_recent("ch:a")[0]["content"] == "alpha"

    def test_load_empty(self):
        cs = _cs()
        assert cs.load_recent("nonexistent") == []


class TestSummary:
    def test_get_summary_none_when_empty(self):
        cs = _cs()
        assert cs.get_summary("test:1") is None

    def test_summary_roundtrip(self):
        cs = _cs()
        conn = cs._get_conn()
        try:
            conn.execute(
                "INSERT INTO chat_summaries (channel_key, summary, covers_through) VALUES (?, ?, ?)",
                ("test:1", "talked about dinosaurs", "2025-01-01T00:00:00"),
            )
            conn.commit()
        finally:
            conn.close()
        assert cs.get_summary("test:1") == "talked about dinosaurs"


class TestSearch:
    def test_search_messages(self):
        cs = _cs()
        cs.store_message("test:1", "user", "I love dinosaurs")
        cs.store_message("test:1", "assistant", "me too! trex is cool")
        cs.store_message("test:1", "user", "what about cats?")
        results = cs.search_messages("test:1", "dinosaurs")
        assert len(results) == 1
        assert results[0]["content"] == "I love dinosaurs"

    def test_search_case_insensitive(self):
        cs = _cs()
        cs.store_message("test:1", "user", "DINOSAURS are great")
        results = cs.search_messages("test:1", "dinosaurs")
        assert len(results) == 1

    def test_search_no_results(self):
        cs = _cs()
        cs.store_message("test:1", "user", "hello world")
        results = cs.search_messages("test:1", "quantum")
        assert len(results) == 0

    def test_search_includes_summary(self):
        cs = _cs()
        conn = cs._get_conn()
        try:
            conn.execute(
                "INSERT INTO chat_summaries (channel_key, summary) VALUES (?, ?)",
                ("test:1", "discussed quantum physics"),
            )
            conn.commit()
        finally:
            conn.close()
        results = cs.search_messages("test:1", "quantum")
        assert len(results) == 1
        assert results[0]["source"] == "summary"


class TestCompaction:
    def test_maybe_compact_below_threshold(self):
        cs = _cs()
        for i in range(5):
            cs.store_message("test:1", "user", f"msg {i}")
        assert cs.maybe_compact("test:1", threshold=80) is False

    @patch("bot.chat_store._summarize_messages")
    def test_maybe_compact_above_threshold(self, mock_summarize):
        cs = _cs()
        mock_summarize.return_value = "Summary of old messages"

        conn = cs._get_conn()
        try:
            for i in range(100):
                conn.execute(
                    "INSERT INTO chat_messages (channel_key, role, content, created_at) VALUES (?, ?, ?, ?)",
                    ("test:1", "user", f"old msg {i}", "2020-01-01T00:00:00"),
                )
            conn.commit()
        finally:
            conn.close()

        result = cs.maybe_compact("test:1", threshold=80, min_age_hours=1)
        assert result is True
        assert cs.get_summary("test:1") == "Summary of old messages"
        remaining = cs.load_recent("test:1", limit=200)
        assert len(remaining) == 0

    @patch("bot.chat_store._summarize_messages")
    def test_compaction_preserves_recent(self, mock_summarize):
        cs = _cs()
        mock_summarize.return_value = "Old stuff summarized"

        conn = cs._get_conn()
        try:
            for i in range(100):
                conn.execute(
                    "INSERT INTO chat_messages (channel_key, role, content, created_at) VALUES (?, ?, ?, ?)",
                    ("test:1", "user", f"old msg {i}", "2020-01-01T00:00:00"),
                )
            conn.commit()
        finally:
            conn.close()

        cs.store_message("test:1", "user", "recent message")

        cs.maybe_compact("test:1", threshold=80, min_age_hours=1)
        remaining = cs.load_recent("test:1", limit=200)
        assert len(remaining) == 1
        assert remaining[0]["content"] == "recent message"


class TestClearChannel:
    def test_clear_removes_messages_and_summary(self):
        cs = _cs()
        cs.store_message("test:1", "user", "hello")
        cs.store_message("test:1", "assistant", "hi")
        conn = cs._get_conn()
        try:
            conn.execute(
                "INSERT INTO chat_summaries (channel_key, summary) VALUES (?, ?)",
                ("test:1", "old summary"),
            )
            conn.commit()
        finally:
            conn.close()

        cs.clear_channel("test:1")
        assert cs.load_recent("test:1") == []
        assert cs.get_summary("test:1") is None

    def test_clear_does_not_affect_other_channels(self):
        cs = _cs()
        cs.store_message("ch:a", "user", "alpha")
        cs.store_message("ch:b", "user", "beta")
        cs.clear_channel("ch:a")
        assert cs.load_recent("ch:a") == []
        assert len(cs.load_recent("ch:b")) == 1


class TestMessageCount:
    def test_count(self):
        cs = _cs()
        assert cs.message_count("test:1") == 0
        cs.store_message("test:1", "user", "a")
        cs.store_message("test:1", "user", "b")
        assert cs.message_count("test:1") == 2
