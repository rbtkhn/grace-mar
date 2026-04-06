"""
Read-only Record slices for lesson / delegation prompts.

Builds a bounded, provenance-labeled payload from on-disk surfaces only.
No API calls, no LLM, no gate merges. See docs/schema-record-api.md
(Record-derived lesson prompt) and docs/canonical-paths.md.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from repo_io import profile_dir, read_path, read_surface_markdown


def _trunc(text: str, max_len: int) -> tuple[str, bool]:
    if max_len <= 0 or not text:
        return text, False
    if len(text) <= max_len:
        return text, False
    return text[:max_len] + "\n\n… [truncated]\n", True


def load_record_slices_for_lesson(
    user_id: str,
    *,
    max_chars: int = 32000,
) -> dict[str, Any]:
    """
    Load whitelisted Record markdown for a lesson-style prompt.

    Returns:
      ok: bool
      error: optional machine code (e.g. ERR_USER_NOT_FOUND)
      slices: dict of excerpt strings (may be empty if files missing)
      provenance: per-slice { source, char_count, truncated }
      warnings: list of human-readable strings
    """
    warnings: list[str] = []
    provenance: dict[str, dict[str, Any]] = {}
    slices: dict[str, str] = {}

    user_dir = profile_dir(user_id)
    if not user_dir.is_dir():
        return {
            "ok": False,
            "error": "ERR_USER_NOT_FOUND",
            "slices": {},
            "provenance": {},
            "warnings": [f"users/{user_id}/ is not a directory"],
        }

    self_raw = read_path(user_dir / "self.md")
    if not self_raw.strip():
        warnings.append("self.md missing or empty")

    skill_think_raw = read_path(user_dir / "skill-think.md")
    if not skill_think_raw.strip():
        warnings.append("skill-think.md missing or empty (edge/THINK context may be thin)")

    self_skills_raw = read_surface_markdown(user_dir, "self_skills")
    if not self_skills_raw.strip():
        warnings.append("self-skills.md (or legacy skills.md) missing or empty")

    b_self = max(1000, int(max_chars * 0.55))
    b_think = max(500, int(max_chars * 0.30))
    b_skills = max(200, int(max_chars * 0.15))

    s_self, tr_self = _trunc(self_raw, b_self)
    s_think, tr_think = _trunc(skill_think_raw, b_think)
    s_skills, tr_skills = _trunc(self_skills_raw, b_skills)

    combined = len(s_self) + len(s_think) + len(s_skills)
    if combined > max_chars:
        overflow = combined - max_chars
        if overflow < len(s_self):
            s_self, tr_self = _trunc(s_self, len(s_self) - overflow)
        else:
            s_self, tr_self = _trunc(s_self, max(500, len(s_self) - overflow // 2))
            s_think, tr_think = _trunc(s_think, max(200, len(s_think) - overflow // 4))
            s_skills, tr_skills = _trunc(s_skills, max(100, len(s_skills) - overflow // 4))
        warnings.append(f"re-trimmed slices to stay within max_chars={max_chars}")

    slices["self"] = s_self
    slices["skill_think"] = s_think
    slices["self_skills"] = s_skills

    provenance["self"] = {
        "source": f"users/{user_id}/self.md",
        "char_count": len(s_self),
        "truncated": tr_self,
    }
    provenance["skill_think"] = {
        "source": f"users/{user_id}/skill-think.md",
        "char_count": len(s_think),
        "truncated": tr_think,
    }
    provenance["self_skills"] = {
        "source": f"users/{user_id}/self-skills.md (or legacy skills.md)",
        "char_count": len(s_skills),
        "truncated": tr_skills,
    }

    return {
        "ok": True,
        "error": None,
        "slices": slices,
        "provenance": provenance,
        "warnings": warnings,
    }


def format_minimal_lesson_prompt(payload: dict[str, Any], *, task_hint: str = "") -> str:
    """
    Map slices into the minimal shape described in docs/schema-record-api.md.
    Placeholders are explicit when slices are empty.
    """
    sl = payload.get("slices") or {}
    self_t = sl.get("self") or "(empty — add content to self.md)"
    think_t = sl.get("skill_think") or "(empty — add skill-think.md for THINK edge)"
    skills_t = sl.get("self_skills") or "(empty — add self-skills.md)"
    task_line = task_hint.strip() or "(operator did not pass --task)"
    return f"""You are tutoring a learner one-on-one. Use only the following about them to personalize this lesson.

What they know / who they are (SELF excerpt):
{self_t}

THINK / edge context (skill-think excerpt):
{think_t}

Skills / capability index excerpt:
{skills_t}

Session focus (operator-supplied, not Record truth):
{task_line}

Deliver one short, focused lesson (or activity) suited to their level and interests. Do not add facts about them beyond the excerpts above; the learner will capture what was done via their own system.
"""
