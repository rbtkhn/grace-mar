#!/usr/bin/env python3
"""
Governance checker: scan for principle violations.

Aligns with white paper §8: "agent as potential adversary," 70/30 sovereignty.
Use as pre-commit hook or in CI to catch violations before merge.

Principles (from AGENTS.md, DESIGN-NOTES):
  - Never leak LLM knowledge
  - The user is the gate (no merge without approval)
  - Calibrated abstention (say "I don't know" when outside knowledge)
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns that suggest violations (agent merging without user approval)
MERGE_WITHOUT_APPROVAL_PATTERNS = [
    (r"\.merge\s*\(|merge\s+into\s+SELF|merge\s+into\s+EVIDENCE", "merge without approval"),
    (r"write\s*\([^)]*SELF\.md|write\s*\([^)]*EVIDENCE\.md", "direct write to SELF/EVIDENCE"),
    (r"open\s*\([^)]*SELF\.md.*['\"]w['\"]|open\s*\([^)]*EVIDENCE\.md.*['\"]w['\"]", "direct write to Record"),
    (r"process_approved_candidates\.py\s+--apply(?!.*--receipt)", "merge apply without receipt"),
]

# Patterns that suggest LLM knowledge leak (referencing non-profile knowledge)
LLM_LEAK_PATTERNS = [
    (r"def.*response.*:.*\b(Wikipedia|training data|I was trained)\b", "LLM knowledge reference"),
    # Less strict: look for hardcoded facts not from profile
]

# Files/dirs to skip
SKIP_DIRS = {".git", "node_modules", "__pycache__", "tools", ".cursor"}
SKIP_FILES = {"governance_checker.py"}  # Don't flag self

# Only these paths may write to SELF.md or EVIDENCE.md (Record). Staging to PENDING-REVIEW is allowed from bot.
ALLOWED_RECORD_WRITERS = frozenset({
    "scripts/process_approved_candidates.py",
})


def scan_file(path: Path, path_rel: Path | None = None) -> list[tuple[int, str, str]]:
    """Return list of (line_num, rule, detail)."""
    violations = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    path_rel = path_rel or path.relative_to(REPO_ROOT)
    path_str = str(path_rel).replace("\\", "/")

    for i, line in enumerate(content.splitlines(), 1):
        for pattern, rule in MERGE_WITHOUT_APPROVAL_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                # Allow comments and string literals (e.g. docstrings)
                stripped = line.strip()
                if stripped.startswith("#") or '"""' in line or "'''" in line:
                    continue
                if "PENDING-REVIEW" in line or "approval" in line or "approved" in line:
                    continue  # Likely documenting the gate
                # Write to SELF.md or EVIDENCE.md only allowed from whitelist
                if "SELF.md" in line or "EVIDENCE.md" in line:
                    if path_str in ALLOWED_RECORD_WRITERS:
                        continue
                violations.append((i, rule, line.strip()[:80]))

    return violations


def scan_repo() -> list[tuple[Path, int, str, str]]:
    """Scan Python files for governance violations."""
    results = []
    for path in REPO_ROOT.rglob("*.py"):
        if any(s in path.parts for s in SKIP_DIRS):
            continue
        if path.name in SKIP_FILES:
            continue
        path_rel = path.relative_to(REPO_ROOT)
        for line_num, rule, detail in scan_file(path, path_rel):
            results.append((path_rel, line_num, rule, detail))
    return results


def main() -> int:
    """Return 0 if clean, 1 if violations found."""
    violations = scan_repo()
    if not violations:
        print("Governance check: OK")
        return 0

    print("Governance check: VIOLATIONS", file=sys.stderr)
    for path, line_num, rule, detail in violations:
        print(f"  {path}:{line_num} — {rule}", file=sys.stderr)
        print(f"    {detail}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
