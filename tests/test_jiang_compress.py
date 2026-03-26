"""Tests for scripts/jiang-compress.py (hyphenated name — importlib load)."""

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_jiang_compress():
    path = REPO_ROOT / "scripts" / "jiang-compress.py"
    spec = importlib.util.spec_from_file_location("jiang_compress_mod", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jiang_compress_mod"] = mod
    spec.loader.exec_module(mod)
    return mod


REQUIRED_KEYS = frozenset(
    {
        "schemaVersion",
        "userId",
        "title",
        "category",
        "compressedAt",
        "sourceLength",
        "compressedLength",
        "coreFactsReferenced",
        "oneSentenceSummary",
        "executableNextActions",
        "linkedEvidence",
        "intentLink",
        "sourceExcerpt",
        "outputPath",
    }
)


def test_slugify_title():
    mod = _load_jiang_compress()
    assert mod.slugify_title("Q3 Planning Sync!") == "q3-planning-sync"
    assert mod.slugify_title("!!!") == "compression"


def test_write_compression_json_writes_expected_keys(tmp_path):
    mod = _load_jiang_compress()
    repo = tmp_path / "repo"
    (repo / "users" / "u1" / "seed").mkdir(parents=True)
    (repo / "users" / "u1" / "seed" / "minimal-core.json").write_text(
        '{"coreFacts": ["alpha beta gamma"]}', encoding="utf-8"
    )
    (repo / "research" / "external" / "work-jiang" / "compressions").mkdir(parents=True)

    raw = "x" * 60 + " alpha keyword in body for core fact match"
    out = mod.write_compression_json(
        repo,
        "u1",
        title="Test Artifact",
        raw_content=raw,
        category="analytical",
        one_sentence="Shipped the test.",
        actions=["Run validators"],
        linked=["research/external/work-jiang/STATUS.md"],
        minimal_core=json.loads((repo / "users" / "u1" / "seed" / "minimal-core.json").read_text()),
        intent_link=None,
    )
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert REQUIRED_KEYS <= set(data.keys())
    assert data["schemaVersion"] == "1.0"
    assert data["userId"] == "u1"
    assert data["category"] == "analytical"
    assert data["executableNextActions"] == ["Run validators"]
    assert data["linkedEvidence"] == ["research/external/work-jiang/STATUS.md"]
    assert not (repo / "users" / "u1" / "self.md").exists()


def test_build_gate_stub_contains_compression_path():
    mod = _load_jiang_compress()
    text = mod.build_gate_stub(
        user_id="u1",
        title="T",
        category="operational",
        one_sentence="Summary here.",
        output_rel="research/external/work-jiang/compressions/t-20260101.json",
    )
    assert "CANDIDATE-JIANG-COMPRESS" in text
    assert "recursion-gate.md" in text
    assert "compression_artifact" in text
