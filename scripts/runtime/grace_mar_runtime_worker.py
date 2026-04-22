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
from types import SimpleNamespace
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Import adapter from same package directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents_sdk_adapter import summarize_inspection  # noqa: E402
from worker_overlays import (  # noqa: E402
    OVERLAY_NAMES,
    OverlayConfigError,
    UnknownOverlayError,
    apply_overlay_defaults,
    emphasis_flags,
    get_overlay,
)
from model_policy import resolve_model_policy  # noqa: E402
from scope_verification import build_scope_verification_block  # noqa: E402
from worker_router import (  # noqa: E402
    TASK_TYPE_TO_ROUTED,
    UnknownTaskTypeError,
    resolve_routing,
    routing_receipt_payload,
)

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


def _read_bundle(files: list[Path], scope: Path, max_chars: int) -> tuple[str, int, int, int, list[str]]:
    """Return bundle text, used chars, files opened successfully, chunk count, warnings."""
    parts: list[str] = []
    used = 0
    files_opened = 0
    warnings: list[str] = []
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            warnings.append(f"read failed for {p}: {e}")
            continue
        rel = p.relative_to(scope)
        header = f"### {rel}\n\n"
        budget = max_chars - used - len(header)
        if budget <= 0:
            warnings.append("bundle truncated: max_chars reached before reading remaining files")
            break
        chunk = txt[:budget]
        if len(txt) > budget:
            chunk += "\n\n… [truncated per --max-chars]\n"
        parts.append(header + chunk)
        files_opened += 1
        used += len(header) + len(chunk)
        if used >= max_chars:
            if files_opened < len(files):
                warnings.append("bundle truncated: max_chars reached; not all files included in bundle")
            break
    chunks_read = len(parts)
    return "\n".join(parts), used, files_opened, chunks_read, warnings


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


def _repo_rel_or_abs(path: Path, repo_root: Path) -> str:
    pr = path.resolve()
    rr = repo_root.resolve()
    try:
        return str(pr.relative_to(rr))
    except ValueError:
        return str(pr)


def build_execution_receipt(
    *,
    run_id: str,
    timestamp: str,
    task_mode: str,
    task_subtype: str | None,
    scope_root: str,
    max_files: int,
    max_chars: int,
    routing_payload: dict[str, Any] | None,
    trace_path: str,
    proposal_path: str,
    status: str,
    error: str | None,
    model_policy: dict[str, Any],
    scope_verification: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Projected non-canonical summary for one worker run (schema: execution-receipt.v1)."""
    if routing_payload:
        worker_route: dict[str, Any] = {
            "resolved": True,
            "task_type": routing_payload.get("task_type"),
            "shared_workers": list(routing_payload.get("shared_workers") or []),
            "routed_worker": routing_payload.get("routed_worker"),
            "entrypoints": dict(routing_payload.get("entrypoints") or {}),
        }
    else:
        worker_route = {
            "resolved": False,
            "task_type": None,
            "shared_workers": [],
            "routed_worker": None,
            "entrypoints": {},
        }
    return {
        "run_id": run_id,
        "timestamp": timestamp,
        "task_mode": task_mode,
        "task_subtype": task_subtype,
        "scope": {
            "root": scope_root,
            "max_files": max_files,
            "max_chars": max_chars,
        },
        "worker_route": worker_route,
        "epistemic": {
            "decision": "allow_with_review" if status == "ok" else "hold",
            "abstained": False,
            "evidence_state": None,
            "notes": None,
        },
        "artifacts": {
            "trace_path": trace_path,
            "proposal_path": proposal_path,
        },
        "outcome": {
            "status": status,
            "error": error,
        },
        "model_policy": model_policy,
        "scope_verification": scope_verification,
        "non_canonical": True,
    }


def write_execution_receipt(worker_home: Path, repo_root: Path, run_id: str, receipt: dict[str, Any]) -> Path:
    receipts_dir = worker_home / "receipts"
    receipts_dir.mkdir(parents=True, exist_ok=True)
    out = receipts_dir / f"{run_id}.json"
    _ensure_worker_writable(out, repo_root)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def task_inspect_work_area(
    *,
    repo_root: Path,
    scope_rel: str,
    max_files: int,
    max_chars: int,
    dry_run: bool,
    compose_with: str | None,
    lens_name: str | None = None,
    task_type: str | None = None,
    task_subtype: str | None = None,
    overlay_name: str | None = None,
    overlay_defaults_applied: list[str] | None = None,
    overlay_emphasis: dict[str, bool] | None = None,
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
    files_seen = len(files)
    rel_paths = [str(p.relative_to(repo_root)) for p in files]
    bundle, used_chars, files_opened, chunks_read, bundle_warnings = _read_bundle(files, scope, max_chars)

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
    if overlay_name or overlay_emphasis:
        lines.extend(
            [
                "## Worker overlay (non-canonical)",
                "",
            ]
        )
        if overlay_name:
            lines.append(f"- **overlay:** `{overlay_name}`")
        if overlay_defaults_applied:
            lines.append(f"- **defaults applied:** {', '.join(f'`{k}`' for k in overlay_defaults_applied)}")
        if overlay_emphasis:
            lines.append(
                "- **emphasis:** "
                + ", ".join(f"`{k}`" for k in sorted(overlay_emphasis.keys()))
            )
        lines.append("")
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

    sv_warn = list(bundle_warnings)
    if files_opened < files_seen:
        sv_warn.append(f"files_opened ({files_opened}) is less than files_seen ({files_seen})")
    scope_verification: dict[str, Any] = build_scope_verification_block(
        files_seen=files_seen,
        rel_paths=rel_paths,
        files_opened=files_opened,
        chunks_read=chunks_read,
        proposal_body=body,
        base_warnings=sv_warn,
    )

    provenance: dict[str, object] = {
        "script": "scripts/runtime/grace_mar_runtime_worker.py",
        "adapter": "scripts/runtime/agents_sdk_adapter.py",
        "compose_with": compose_with,
        "lens": lens_name,
    }
    if overlay_name is not None:
        provenance["overlay"] = overlay_name
    if overlay_defaults_applied:
        provenance["overlay_defaults_applied"] = list(overlay_defaults_applied)
    if overlay_emphasis:
        provenance["overlay_emphasis"] = dict(overlay_emphasis)

    routing_payload: dict[str, Any] | None = None
    if task_type:
        try:
            rr = resolve_routing(task_type, repo_root)
            routing_payload = routing_receipt_payload(run_id=run_id, result=rr)
            provenance["worker_routing"] = routing_payload
            provenance["runtime_receipt"] = {
                "overlay": overlay_name,
                "overlay_defaults_applied": list(overlay_defaults_applied or []),
                "task_type": rr.task_type,
                "routed_worker": rr.routed_worker_id,
                "shared_workers": list(rr.shared_worker_ids),
                "emphasis": dict(overlay_emphasis or {}),
                "non_canonical": True,
            }
        except (UnknownTaskTypeError, FileNotFoundError, KeyError, ValueError) as e:
            print(f"error: worker routing failed: {e}", file=sys.stderr)
            return 2

    ts_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    trace_status = "ok" if compose_exit == 0 or not compose_with else "partial"
    trace = {
        "run_id": run_id,
        "timestamp": ts_iso,
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
        "status": trace_status,
        "provenance": provenance,
    }

    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(trace, ensure_ascii=False) + "\n")

    model_policy = resolve_model_policy(
        repo_root=repo_root,
        task_type=task_type,
        task_subtype=task_subtype,
        action=None,
    )
    receipt = build_execution_receipt(
        run_id=run_id,
        timestamp=ts_iso,
        task_mode="inspect_work_area",
        task_subtype=task_subtype,
        scope_root=scope_rel,
        max_files=max_files,
        max_chars=max_chars,
        routing_payload=routing_payload,
        trace_path=_repo_rel_or_abs(trace_path, repo_root),
        proposal_path=_repo_rel_or_abs(proposal_path, repo_root),
        status=trace_status,
        error=None,
        model_policy=model_policy,
        scope_verification=scope_verification,
    )
    receipt_path = write_execution_receipt(worker_home, repo_root, run_id, receipt)

    print(f"wrote proposal {proposal_path}", file=sys.stderr)
    print(f"appended trace {trace_path}", file=sys.stderr)
    print(f"wrote receipt {receipt_path}", file=sys.stderr)
    return 0


def _resolve_inspect_with_overlay(
    args: argparse.Namespace,
    repo_root: Path,
    overlay_block: dict[str, object] | None,
) -> tuple[str, int, int, str | None, str | None, str | None, list[str], dict[str, bool]]:
    """
    Resolve scope/caps/compose/lens and effective task_type.

    Precedence: explicit CLI (--scope, --max-*, --task-type) > overlay defaults >
    built-in defaults. If ``--lens`` is set, it wins over overlay for scope/caps;
    overlay may still set ``task_type`` when ``--task-type`` is omitted.
    """
    emphasis = emphasis_flags(overlay_block) if overlay_block else {}
    overlay_name: str | None = args.overlay

    if args.lens:
        scope, mf, mc, compose, lens_name = _resolve_lens_args(args)
        applied: list[str] = []
        tt = args.task_type
        if overlay_block and tt is None and overlay_block.get("default_task_type"):
            tt = str(overlay_block["default_task_type"]).strip().lower()
            applied.append("task_type")
        return scope, mf, mc, compose, lens_name, tt, applied, emphasis

    s, mf, mc, tt, ov_applied = apply_overlay_defaults(
        overlay=overlay_block,
        scope=args.scope,
        max_files=args.max_files,
        max_chars=args.max_chars,
        task_type=args.task_type,
    )
    eff = SimpleNamespace(
        scope=s,
        max_files=mf,
        max_chars=mc,
        compose_with=args.compose_with,
        no_compose=args.no_compose,
        lens=None,
    )
    scope, mf2, mc2, compose, lens_name = _resolve_lens_args(eff)
    return scope, mf2, mc2, compose, lens_name, tt, ov_applied, emphasis


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
    ap.add_argument(
        "--task-type",
        default=None,
        choices=tuple(sorted(TASK_TYPE_TO_ROUTED.keys())),
        metavar="TYPE",
        help=(
            "Optional routed worker hint (strategy|tacit|moonshot|contradiction|research); "
            "records shared+routed entrypoints in trace provenance — does not invoke them"
        ),
    )
    ap.add_argument(
        "--task-subtype",
        default=None,
        metavar="NAME",
        help=(
            "Optional task subtype for model-tier policy (e.g. quick_scan, contradiction_review); "
            "see config/model_routing/task_policy.yaml"
        ),
    )
    ap.add_argument(
        "--overlay",
        default=None,
        choices=tuple(sorted(OVERLAY_NAMES)),
        metavar="NAME",
        help=(
            "Optional pass overlay (config/runtime_workers/overlays.yaml): default scope/caps/task_type "
            "when not overridden by explicit CLI; with --lens, only default task_type may apply"
        ),
    )
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
        overlay_block: dict[str, object] | None = None
        if args.overlay:
            try:
                overlay_block = get_overlay(args.overlay, repo_root)
            except (UnknownOverlayError, OverlayConfigError, FileNotFoundError) as e:
                print(f"error: overlay: {e}", file=sys.stderr)
                return 2
        (
            scope,
            max_files,
            max_chars,
            compose_with,
            lens_name,
            effective_task_type,
            overlay_applied,
            overlay_emphasis,
        ) = _resolve_inspect_with_overlay(args, repo_root, overlay_block)
        ts_raw = (args.task_subtype or "").strip()
        effective_subtype = ts_raw if ts_raw else None
        return task_inspect_work_area(
            repo_root=repo_root,
            scope_rel=scope,
            max_files=max_files,
            max_chars=max_chars,
            dry_run=args.dry_run,
            compose_with=compose_with,
            lens_name=lens_name,
            task_type=effective_task_type,
            task_subtype=effective_subtype,
            overlay_name=args.overlay,
            overlay_defaults_applied=overlay_applied,
            overlay_emphasis=overlay_emphasis,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
