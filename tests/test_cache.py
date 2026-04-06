"""Unit tests for scripts/cache.py (path-keyed LRU + clear_cache)."""

from __future__ import annotations

import cache


def test_load_json_file_caches_until_cleared(tmp_path) -> None:
    cache.clear_cache()
    p = tmp_path / "x.json"
    p.write_text('{"x": 1}', encoding="utf-8")
    assert cache.load_json_file(p) == {"x": 1}
    p.write_text('{"x": 2}', encoding="utf-8")
    assert cache.load_json_file(p) == {"x": 1}
    cache.clear_cache()
    assert cache.load_json_file(p) == {"x": 2}
    cache.clear_cache()


def test_load_schema_relative(tmp_path, monkeypatch) -> None:
    cache.clear_cache()
    schema_dir = tmp_path / "schema-registry"
    schema_dir.mkdir()
    rel = "schema-registry/test-schema.v1.json"
    f = tmp_path / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text('{"$schema": "https://json-schema.org/draft/2020-12/schema"}', encoding="utf-8")
    monkeypatch.setattr(cache, "REPO_ROOT", tmp_path)
    cache.clear_cache()
    out = cache.load_schema(rel)
    assert isinstance(out, dict)
    assert "$schema" in out
    cache.clear_cache()
