#!/usr/bin/env python3
"""
Lightweight validation for governance-critical structured files.

Checks JSON parseability (schema-registry, workflow examples, artifacts under size cap),
pyproject.toml (tomllib), .pre-commit-config.yaml when PyYAML is installed (optional dev dep;
see requirements-dev.txt — CI installs it), and relative Markdown links in a fixed doc list.

Does not modify Record or runtime behavior. Reference-style link definitions [ref]: url are
not validated (V1 limitation).

Exit codes: 0 success (warnings/skips ok); 1 hard validation failure.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent

# Skip very large JSON under artifacts/ (historical blobs, etc.); still counts toward summary.
MAX_ARTIFACT_JSON_BYTES = 512 * 1024

LONG_LINE_WARN_CHARS = 500

# Sorted relative paths from repo root (deterministic).
CRITICAL_MARKDOWN_PATHS: tuple[str, ...] = (
    "artifacts/README.md",
    "docs/operator-dashboards.md",
    "docs/operator-surface-registry.md",
    "docs/operator-surface-staleness.md",
    "docs/workflows/README.md",
    "docs/workflows/known-path-workflows/README.md",
    "docs/workflows/known-path-workflows/load-lift-receipts.md",
    "docs/workflows/known-path-workflows/workflow-agent-template.md",
    "docs/workflows/known-path-workflows/workflow-fitness-test.md",
)

# Inline [text](target); exclude image links ![...](...)
_INLINE_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")


def validate_json_file(path: Path) -> str | None:
    """Return an error string if JSON cannot be parsed; None if ok."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return f"{path}: read error: {e}"
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        return f"{path}: JSON: {e}"
    return None


def validate_schema_registry_json(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    reg = repo_root / "schema-registry"
    if not reg.is_dir():
        return [f"{reg}: missing schema-registry directory"]
    for path in sorted(reg.glob("*.json")):
        err = validate_json_file(path)
        if err:
            errors.append(err)
    return errors


def validate_example_workflow_json(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    examples = repo_root / "docs" / "workflows" / "known-path-workflows" / "examples"
    if not examples.is_dir():
        return []
    for path in sorted(examples.glob("*.json")):
        err = validate_json_file(path)
        if err:
            errors.append(err)
    return errors


def validate_artifacts_json(repo_root: Path = REPO_ROOT) -> tuple[list[str], int]:
    """Validate *.json under artifacts/ under size cap. Returns (errors, skipped_oversized_count)."""
    errors: list[str] = []
    skipped = 0
    root = repo_root / "artifacts"
    if not root.is_dir():
        return [], 0
    paths = sorted(root.rglob("*.json"))
    for path in paths:
        try:
            size = path.stat().st_size
        except OSError as e:
            errors.append(f"{path}: stat error: {e}")
            continue
        if size > MAX_ARTIFACT_JSON_BYTES:
            skipped += 1
            continue
        err = validate_json_file(path)
        if err:
            errors.append(err)
    return errors, skipped


def validate_json_globs(repo_root: Path = REPO_ROOT) -> tuple[list[str], int]:
    """Run all JSON glob validations. Returns (errors, artifacts_skipped_oversized_count)."""
    errors: list[str] = []
    errors.extend(validate_schema_registry_json(repo_root))
    errors.extend(validate_example_workflow_json(repo_root))
    art_err, skipped = validate_artifacts_json(repo_root)
    errors.extend(art_err)
    return errors, skipped


def validate_pyproject(repo_root: Path = REPO_ROOT) -> str | None:
    path = repo_root / "pyproject.toml"
    try:
        tomllib.loads(path.read_text(encoding="utf-8"))
    except ImportError as e:  # pragma: no cover — Python 3.11+ expected
        return f"{path}: tomllib unavailable: {e}"
    except OSError as e:
        return f"{path}: read error: {e}"
    except Exception as e:
        return f"{path}: TOML parse error: {e}"
    return None


def validate_pre_commit_yaml(repo_root: Path = REPO_ROOT) -> str | None:
    """
    Parse .pre-commit-config.yaml when PyYAML is installed.
    Returns None if ok or skipped (ImportError printed by caller); error string on parse failure.
    """
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return None  # caller prints skip
    path = repo_root / ".pre-commit-config.yaml"
    try:
        raw = path.read_text(encoding="utf-8")
        yaml.safe_load(raw)
    except OSError as e:
        return f"{path}: read error: {e}"
    except Exception as e:
        return f"{path}: YAML parse error: {e}"
    return None


def iter_markdown_links(path: Path) -> Iterator[tuple[int, str]]:
    """
    Yield (1-based line number, raw link target) for inline [text](target) links,
    excluding fenced code blocks and image links. Does not filter protocols — caller does.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    out_lines: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out_lines.append((i, line))
    for line_no, line in out_lines:
        for m in _INLINE_LINK_RE.finditer(line):
            yield line_no, m.group(1).strip()


def _should_skip_target(raw: str) -> bool:
    t = raw.strip()
    if not t:
        return True
    low = t.lower()
    if low.startswith("mailto:"):
        return True
    if low.startswith("http://") or low.startswith("https://"):
        return True
    if low.startswith("#"):
        return True
    # Strip angle brackets sometimes used in Markdown URLs
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1].strip()
        low = t.lower()
        if low.startswith("http://") or low.startswith("https://"):
            return True
        if low.startswith("mailto:"):
            return True
    # Fragment-only after trim (e.g. `foo.md#` resolved later)
    path_part = t.split("#", 1)[0].strip()
    if not path_part:
        return True
    return False


def validate_markdown_links(
    paths: list[Path],
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    """Resolve local relative links; report sorted error strings for missing targets."""
    errors: list[str] = []
    rows: list[tuple[str, str, str]] = []
    for md_path in paths:
        if not md_path.is_file():
            errors.append(f"{md_path}: missing Markdown file")
            continue
        base = md_path.parent
        for _, raw in iter_markdown_links(md_path):
            if _should_skip_target(raw):
                continue
            target = raw.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1].strip()
            target_path_part = target.split("#", 1)[0].strip()
            if not target_path_part:
                continue
            # Skip obvious non-path protocols
            if "://" in target_path_part:
                continue
            resolved = (base / target_path_part).resolve()
            try:
                resolved.relative_to(repo_root.resolve())
            except ValueError:
                rows.append(
                    (
                        str(md_path.relative_to(repo_root)),
                        raw,
                        f"{resolved} (outside repo)",
                    )
                )
                continue
            if not resolved.exists():
                rows.append(
                    (
                        str(md_path.relative_to(repo_root)),
                        raw,
                        str(resolved.relative_to(repo_root)),
                    )
                )
    for md_rel, raw, detail in sorted(rows):
        errors.append(f"{md_rel}:{raw}->{detail}")
    return errors


def warn_long_lines(paths: list[Path], repo_root: Path = REPO_ROOT, limit: int = LONG_LINE_WARN_CHARS) -> list[str]:
    """Return warning lines (already prefixed); does not imply failure."""
    warnings: list[str] = []
    for md_path in sorted(paths):
        if not md_path.is_file():
            continue
        rel = md_path.relative_to(repo_root)
        lines = md_path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, start=1):
            if len(line) > limit:
                warnings.append(f"WARNING: long line ({len(line)} chars): {rel}:{i}")
    return sorted(warnings)


def critical_markdown_paths(repo_root: Path = REPO_ROOT) -> list[Path]:
    return sorted(repo_root / p for p in CRITICAL_MARKDOWN_PATHS)


def main() -> int:
    repo_root = REPO_ROOT
    failures: list[str] = []

    # JSON
    json_errors, artifact_skipped = validate_json_globs(repo_root)
    failures.extend(json_errors)
    if artifact_skipped:
        print(
            f"Note: skipped {artifact_skipped} artifact JSON file(s) over "
            f"{MAX_ARTIFACT_JSON_BYTES} bytes",
            file=sys.stderr,
        )

    # TOML
    py_err = validate_pyproject(repo_root)
    if py_err:
        failures.append(py_err)

    yaml_note = "skipped"
    try:
        import yaml  # noqa: F401

        y_err = validate_pre_commit_yaml(repo_root)
        if y_err:
            failures.append(y_err)
            yaml_note = "fail"
        else:
            yaml_note = "ok"
    except ImportError:
        print(
            "Skip: PyYAML not installed — .pre-commit-config.yaml not parsed "
            "(install requirements-dev.txt for full checks)",
            file=sys.stderr,
        )

    md_paths = critical_markdown_paths(repo_root)
    md_errors = validate_markdown_links(md_paths, repo_root)
    failures.extend(md_errors)

    for w in warn_long_lines(md_paths, repo_root):
        print(w, file=sys.stderr)

    if failures:
        for msg in sorted(failures):
            print(msg, file=sys.stderr)
        print(
            f"validate_structured_files: failed ({len(failures)} issue(s))",
            file=sys.stderr,
        )
        return 1

    print(
        "validate_structured_files: OK "
        f"(schema-registry + workflow examples JSON + "
        f"artifacts<={MAX_ARTIFACT_JSON_BYTES}b cap, "
        f"pyproject.toml, "
        f"pre-commit YAML={yaml_note}, "
        f"{len(md_paths)} markdown files)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())