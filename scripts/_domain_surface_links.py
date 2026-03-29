"""
Rebase markdown links in DOMAIN wisdom surfaces from _template/DOMAIN.md placeholders
to paths relative to the output file. Shared by create-domain.py and migrate-to-domain-surface.py.
"""

from __future__ import annotations

import os
from pathlib import Path

# Template literals (must match _template/DOMAIN.md)
_TEMPLATE_HREF_AGENTS = "../AGENTS.md"


def _relpath_posix(target: Path, start: Path) -> str:
    return os.path.relpath(target.resolve(), start.resolve()).replace("\\", "/")


def rebase_domain_surface_markdown(
    content: str,
    output_file: Path,
    repo_root: Path,
    user_id: str = "grace-mar",
) -> str:
    """Replace template ../ links with paths relative to output_file.parent."""
    out_dir = output_file.parent.resolve()
    rr = repo_root.resolve()
    agents_s = _relpath_posix(rr / "AGENTS.md", out_dir)
    self_s = _relpath_posix(rr / "users" / user_id / "self.md", out_dir)
    content = content.replace(f"]({_TEMPLATE_HREF_AGENTS})", f"]({agents_s})")
    content = content.replace("](../users/grace-mar/self.md)", f"]({self_s})")
    if user_id != "grace-mar":
        content = content.replace(f"](../users/{user_id}/self.md)", f"]({self_s})")
    return content


def assert_domain_surface_links_rebased(content: str, output_file: Path | None = None) -> None:
    """Fail if template-relative links remain where they would be wrong for depth.

    Under repo-root ``work-*/``, ``../AGENTS.md`` matches ``os.path.relpath``; skip strict check.
    Under ``docs/skill-work/work-*/``, template ``../`` links must be rewritten.
    """
    path_s = str(output_file.resolve()) if output_file is not None else ""
    if "/docs/skill-work/" in path_s.replace("\\", "/"):
        if f"]({_TEMPLATE_HREF_AGENTS})" in content:
            raise ValueError("unrebased AGENTS.md link (../AGENTS.md) still in content")
        if "](../users/" in content and "self.md)" in content:
            raise ValueError("unrebased users/.../self.md link still in content")
