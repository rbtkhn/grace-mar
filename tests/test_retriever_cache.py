"""Retriever disk fingerprint cache and inverted-index path (isolated user dir)."""

import pytest


@pytest.fixture
def minimal_user_dir(tmp_path, monkeypatch):
    uid = "retriever-test-user"
    ud = tmp_path / "users" / uid
    ud.mkdir(parents=True)
    (ud / "self.md").write_text(
        'id: LEARN-0001\ndate: 2020-01-01\ntopic: "Jupiter"\n'
        'her_understanding: "gas giant"\n\n'
        'id: LEARN-0002\ndate: 2020-01-02\ntopic: "Mars"\n'
        'her_understanding: "red planet"\n',
        encoding="utf-8",
    )
    for name in ("skills.md", "skill-think.md", "skill-write.md", "work-alpha-school.md", "work-jiang.md", "self-evidence.md"):
        (ud / name).write_text("", encoding="utf-8")

    monkeypatch.setenv("GRACE_MAR_USER_ID", uid)
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_CACHE", "0")
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_DISK_CACHE", "1")
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_INVERTED_INDEX", "1")

    import bot.retriever as retriever

    monkeypatch.setattr(retriever, "PROFILE_DIR", ud)
    monkeypatch.setattr(retriever, "SELF_PATH", ud / "self.md")
    monkeypatch.setattr(retriever, "SKILLS_PATHS", [ud / "skills.md", ud / "skill-think.md", ud / "skill-write.md"])
    monkeypatch.setattr(retriever, "WORK_PATHS", [ud / "work-alpha-school.md", ud / "work-jiang.md"])
    monkeypatch.setattr(retriever, "EVIDENCE_PATH", ud / "self-evidence.md")
    monkeypatch.setattr(retriever, "DISK_CACHE_PATH", ud / ".cache" / "retriever_chunks.pkl")
    retriever._chunks_cache = None
    retriever._chunks_mtime = 0.0
    retriever._chunks_inv = None

    return ud, retriever


def test_retriever_disk_cache_roundtrip(minimal_user_dir):
    ud, ret = minimal_user_dir
    chunks1 = ret.load_record_chunks()
    assert len(chunks1) >= 1
    cache_file = ud / ".cache" / "retriever_chunks.pkl"
    assert cache_file.is_file()

    ret._chunks_cache = None
    ret._chunks_mtime = 0.0
    ret._chunks_inv = None
    chunks2 = ret.load_record_chunks()
    assert len(chunks2) == len(chunks1)


def test_retrieve_jupiter_uses_inverted_index(minimal_user_dir):
    _, ret = minimal_user_dir
    ret.load_record_chunks()
    out = ret.retrieve("What do you know about Jupiter?", top_k=3)
    assert any("LEARN-0001" in cid for cid, _ in out)


def test_retrieve_inverted_index_off_scans_all(minimal_user_dir, monkeypatch):
    ud, ret = minimal_user_dir
    monkeypatch.setenv("GRACE_MAR_RETRIEVER_INVERTED_INDEX", "0")
    ret._chunks_cache = None
    ret._chunks_mtime = 0.0
    ret._chunks_inv = None
    out = ret.retrieve("Jupiter gas giant knowledge", top_k=3)
    assert any("LEARN-0001" in cid for cid, _ in out)
