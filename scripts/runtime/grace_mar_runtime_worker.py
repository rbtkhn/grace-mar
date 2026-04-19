#!/usr/bin/env python3
"""
Grace-Mar runtime worker — disposable inspect_work_area for work-strategy (WORK only).

Writes only under runtime/runtime-worker/ (or GRACE_MAR_RUNTIME_WORKER_HOME).
Never writes SELF, EVIDENCE, SKILLS, recursion-gate, or prompt surfaces.

Usage:
  python3 scripts/runtime/grace_mar_runtime_worker.py --task inspect_work_area --dry-run
  python3 scripts/runtime/grace_mar_runtime_worker.py --task inspect_work_area  # needs OPENAI_API_KEY for summary
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Import adapter from same package directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents_sdk_adapter import summarize_inspection  # noqa: E402

DEFAULT_SCOPE = "docs/skill-work/work-strategy/strategy-notebook"
DEFAULT_MAX_FILES = 400
DEFAULT_MAX_CHARS = 200_000


@dataclass(frozen=True)
class Lens:
    """Preset for inspect_work_area (scope, caps, optional compose)."""

    scope: str
    max_files: int
    max_chars: int
    compose_with: str | None = None
    description: str = ""


# Preset lenses — use --lens <name>; override any field with explicit flags / --no-compose.
LENSES: dict[str, Lens] = {
    "notebook-health": Lens(
        scope=DEFAULT_SCOPE,
        max_files=400,
        max_chars=200_000,
        compose_with="scripts/validate_strategy_expert_threads.py",
        description="Full notebook tree + expert-thread journal validator.",
    ),
    "inbox-day": Lens(
        scope=DEFAULT_SCOPE,
        max_files=80,
        max_chars=80_000,
        compose_with="scripts/verify_strategy_inbox_accumulator.py",
        description="Notebook scope + daily-strategy-inbox Accumulator date check.",
    ),
    "quick-scan": Lens(
        scope=DEFAULT_SCOPE,
        max_files=25,
        max_chars=24_000,
        compose_with=None,
        description="Small caps, no compose — fast file list + excerpt.",
    ),
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".csv",
    ".mdc",
}

COMPOSE_ALLOWLIST = frozenset(
    {
        "scripts/validate_strategy_expert_threads.py",
        "scripts/verify_strategy_inbox_accumulator.py",
    }
)

def _forbidden_repo_write(rel: str) -> bool:
    """True if repo-relative path must never receive worker writes (plan denylist)."""
    rel = rel.replace("\\", "/")
    if rel in ("bot/prompt.py", "bot/bot.py", "bot/wechat_bot.py"):
        return True
    if not rel.startswith("users/"):
        return False
    name = rel.rsplit("/", 1)[-1]
    return name in (
        "self.md",
        "self-archive.md",
        "self-skills.md",
        "self-library.md",
        "recursion-gate.md",
    )


def _utc_run_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    h = hashlib.sha256(f"{ts}:{uuid.uuid4().hex}".encode()).hexdigest()[:12]
    return f"rw_{ts}_{h}"


def _worker_home(repo_root: Path) -> Path:
    raw = os.environ.get("GRACE_MAR_RUNTIME_WORKER_HOME", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (repo_root / "runtime" / "runtime-worker").resolve()


def _ensure_worker_writable(path: Path, repo_root: Path) -> None:
    """Refuse writes outside worker home or on canonical Record / gate surfaces."""
    rp = repo_root.resolve()
    wh = _worker_home(repo_root).resolve()
    path_r = path.resolve()
    try:
        path_r.relative_to(wh)
    except ValueError as e:
        raise SystemExit(f"refusing write outside worker home {wh}: {path}") from e
    try:
        rel = str(path_r.relative_to(rp))
    except ValueError:
        return
    if _forbidden_repo_write(rel):
        raise SystemExit(f"refusing write on canonical or gated path: {rel}")


def _collect_files(scope: Path, max_files: int) -> list[Path]:
    if not scope.is_dir():
        raise SystemExit(f"scope is not a directory: {scope}")
    out: list[Path] = []
    for p in sorted(scope.rglob("*")):
        if not p.is_file():
            continue
        suf = p.suffix.lower()
        if suf and suf not in TEXT_SUFFIXES:
            continue
        out.append(p)
        if len(out) >= max_files:
            break
    return out


def _read_bundle(files: list[Path], scope: Path, max_chars: int) -> tuple[str, int]:
    parts: list[str] = []
    used = 0
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(scope)
        header = f"### {rel}\n\n"
        budget = max_chars - used - len(header)
        if budget <= 0:
            break
        chunk = txt[:budget]
        if len(txt) > budget:
            chunk += "\n\n… [truncated per --max-chars]\n"
        parts.append(header + chunk)
        used += len(header) + len(chunk)
        if used >= max_chars:
            break
    return "\n".join(parts), used


def _compose_argv(repo_root: Path, script_rel: str, scope_path: Path) -> list[str]:
    """Build argv for a whitelisted compose script (each script has its own CLI)."""
    if script_rel not in COMPOSE_ALLOWLIST:
        raise SystemExit(f"--compose-with not allowlisted: {script_rel} (allowed: {sorted(COMPOSE_ALLOWLIST)})")
    script = repo_root / script_rel
    if not script.is_file():
        raise SystemExit(f"compose script missing: {script}")
    py = sys.executable
    if script_rel == "scripts/validate_strategy_expert_threads.py":
        return [py, str(script), "--dir", str(scope_path)]
    if script_rel == "scripts/verify_strategy_inbox_accumulator.py":
        inbox = scope_path / "daily-strategy-inbox.md"
        return [py, str(script), "--inbox", str(inbox)]
    raise SystemExit(f"compose dispatch missing for {script_rel}")


def _run_compose(repo_root: Path, script_rel: str, scope_path: Path) -> tuple[str, int]:
    argv = _compose_argv(repo_root, script_rel, scope_path)
    proc = subprocess.run(
        argv,
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=180,
    )
    out = ""
    if proc.stdout:
        out += proc.stdout
    if proc.stderr:
        out += "\n--- stderr ---\n" + proc.stderr
    return out[:12_000], proc.returncode


def task_inspect_work_area(
    *,
    repo_root: Path,
    scope_rel: str,
    max_files: int,
    max_chars: int,
    dry_run: bool,
    compose_with: str | None,
    lens_name: str | None = None,
) -> int:
    scope = (repo_root / scope_rel).resolve()
    try:
        scope.relative_to(repo_root.resolve())
    except ValueError:
        raise SystemExit("scope must be inside repo root") from None
    run_id = _utc_run_id()
    worker_home = _worker_home(repo_root)
    prop_dir = worker_home / "proposals"
    trace_dir = worker_home / "traces"
    prop_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    proposal_path = prop_dir / f"{run_id}.md"
    trace_path = trace_dir / "index.jsonl"

    _ensure_worker_writable(proposal_path, repo_root)
    _ensure_worker_writable(trace_path, repo_root)

    files = _collect_files(scope, max_files)
    rel_paths = [str(p.relative_to(repo_root)) for p in files]
    bundle, used_chars = _read_bundle(files, scope, max_chars)

    tools_used: list[str] = ["filesystem.read", "pathlib.rglob"]
    compose_stdout = ""
    compose_exit = 0
    if compose_with:
        compose_stdout, compose_exit = _run_compose(repo_root, compose_with, scope)
        tools_used.append(f"compose:{compose_with}")

    summary, stools = summarize_inspection(
        rel_paths=rel_paths,
        bundle_excerpt=bundle,
        dry_run=dry_run,
    )
    tools_used.extend(stools)

    lines = [
        "<!-- NON-CANONICAL / WORK ONLY — not SELF, EVIDENCE, or gate truth -->",
        "",
        f"# Runtime worker proposal — `{run_id}`",
        "",
        f"- **task:** `inspect_work_area`",
        f"- **scope:** `{scope_rel}`",
        f"- **files listed:** {len(files)} (cap {max_files})",
        f"- **bundle chars (approx):** {used_chars} (cap {max_chars})",
        f"- **dry_run:** {dry_run}",
        "",
    ]
    if lens_name:
        lines.extend([f"- **lens:** `{lens_name}`", ""])
    lines.extend(
        [
            "## File paths (relative to repo)",
            "",
        ]
    )
    for rp in rel_paths:
        lines.append(f"- `{rp}`")
    lines.extend(["", "## Compose (optional)", ""])
    if compose_with:
        lines.append(f"- **script:** `{compose_with}` (exit {compose_exit})")
        lines.extend(["", "```", compose_stdout[:8000], "```", ""])
    else:
        lines.append("_No compose step._\n")

    lines.extend(["## Bundle excerpt (for operator / model context)", "", bundle, ""])
    lines.extend(["## Summary", "", summary, ""])

    body = "\n".join(lines)
    proposal_path.write_text(body, encoding="utf-8")

    trace = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_mode": "inspect_work_area",
        "scope": scope_rel,
        "tools_used": tools_used,
        "approvals_requested": [],
        "outputs": [
            (
                str(proposal_path.relative_to(repo_root))
                if proposal_path.resolve().is_relative_to(repo_root.resolve())
                else str(proposal_path)
            )
        ],
        "boundary_checks": {
            "canonical_write_attempted": False,
            "worker_home": str(worker_home),
            "compose_exit": compose_exit if compose_with else None,
        },
        "status": "ok" if compose_exit == 0 or not compose_with else "partial",
        "provenance": {
            "script": "scripts/runtime/grace_mar_runtime_worker.py",
            "adapter": "scripts/runtime/agents_sdk_adapter.py",
            "compose_with": compose_with,
            "lens": lens_name,
        },
    }

    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False) + "\n")

    print(f"wrote proposal {proposal_path}", file=sys.stderr)
    print(f"appended trace {trace_path}", file=sys.stderr)
    return 0


def _resolve_lens_args(args: argparse.Namespace) -> tuple[str, int, int, str | None, str | None]:
    """Merge --lens preset with explicit flags (--no-compose clears compose)."""
    lens_name: str | None = args.lens
    if lens_name:
        le = LENSES[lens_name]
        scope = args.scope.strip().lstrip("/") if args.scope is not None else le.scope
        max_files = le.max_files if args.max_files is None else args.max_files
        max_chars = le.max_chars if args.max_chars is None else args.max_chars
        if args.no_compose:
            compose: str | None = None
        elif args.compose_with is not None:
            c = args.compose_with.strip()
            compose = c if c else None
        else:
            compose = le.compose_with
    else:
        scope = (args.scope or DEFAULT_SCOPE).strip().lstrip("/")
        max_files = DEFAULT_MAX_FILES if args.max_files is None else args.max_files
        max_chars = DEFAULT_MAX_CHARS if args.max_chars is None else args.max_chars
        if args.no_compose:
            compose = None
        elif args.compose_with is not None:
            c = args.compose_with.strip()
            compose = c if c else None
        else:
            compose = None
    return scope, max(1, max_files), max(1000, max_chars), compose, lens_name


def main() -> int:
    lens_choices = sorted(LENSES.keys())
    lens_help = "; ".join(f"{k}: {LENSES[k].description}" for k in lens_choices)
    ap = argparse.ArgumentParser(
        description=__doc__,
        epilog=f"Preset lenses (--lens): {lens_help}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--task", default="inspect_work_area", choices=("inspect_work_area",))
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--scope",
        default=None,
        help=f"Repo-relative directory to inspect (default: {DEFAULT_SCOPE}, or lens default)",
    )
    ap.add_argument(
        "--max-files",
        type=int,
        default=None,
        metavar="N",
        help=f"Cap file count (default: {DEFAULT_MAX_FILES}, or lens default)",
    )
    ap.add_argument(
        "--max-chars",
        type=int,
        default=None,
        metavar="N",
        help=f"Cap total excerpt chars (default: {DEFAULT_MAX_CHARS}, or lens default)",
    )
    ap.add_argument(
        "--lens",
        choices=lens_choices,
        default=None,
        metavar="NAME",
        help="Preset scope/caps/compose (override with --scope / --max-* / --compose-with / --no-compose)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip LLM summary; still write proposal + trace (CI-safe).",
    )
    ap.add_argument(
        "--compose-with",
        default=None,
        metavar="REL_PATH",
        help=(
            "Optional single script under repo root "
            f"(allowlist: {', '.join(sorted(COMPOSE_ALLOWLIST))})"
        ),
    )
    ap.add_argument(
        "--no-compose",
        action="store_true",
        help="Do not run a compose step (overrides --lens compose).",
    )
    args = ap.parse_args()
    repo_root = args.repo_root.resolve()

    if args.task == "inspect_work_area":
        scope, max_files, max_chars, compose_with, lens_name = _resolve_lens_args(args)
        return task_inspect_work_area(
            repo_root=repo_root,
            scope_rel=scope,
            max_files=max_files,
            max_chars=max_chars,
            dry_run=args.dry_run,
            compose_with=compose_with,
            lens_name=lens_name,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
