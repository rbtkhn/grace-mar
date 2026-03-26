"""record_refs heuristic on merge (process_approved_candidates)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import process_approved_candidates as pac  # noqa: E402


def test_record_refs_ix_a_knowledge():
    fn = getattr(pac, "_record_refs_for_applied")
    refs = fn("grace-mar", "SELF_KNOWLEDGE", "IX-A. KNOWLEDGE", "SELF_KNOWLEDGE_ADD")
    joined = " ".join(refs)
    assert "self.md#IX-A" in joined
    assert "self-archive.md" in joined


def test_record_refs_library_class():
    fn = getattr(pac, "_record_refs_for_applied")
    refs = fn("grace-mar", "SELF_KNOWLEDGE", "", "SELF_LIBRARY_ADD")
    assert any("self-library.md" in r for r in refs)


def test_record_refs_skills():
    fn = getattr(pac, "_record_refs_for_applied")
    refs = fn("grace-mar", "SELF_PERSONALITY", "", "SKILLS_CLAIM")
    assert any("skills.md" in r for r in refs)
