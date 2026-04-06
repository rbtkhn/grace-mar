#!/usr/bin/env python3
"""
Sandbox adapter — governance wrapper for external sandbox runtimes.

Wraps external sandboxes (E2B, Daytona, Docker, or dry-run) with
authority checks, pre/post receipts, and compute-ledger integration.

See: docs/skill-work/work-dev/sandbox-adapter-spec.md

Usage (dry-run):
  python scripts/work_dev/sandbox_adapter.py -u grace-mar --backend dry_run --command "echo hello"
  python scripts/work_dev/sandbox_adapter.py -u grace-mar --backend dry_run --command "ls" --task-id TASK-001 --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


# ── Data shapes ─────────────────────────────────────────────────────────

@dataclass
class SandboxRequest:
    command: str
    caller: str = "operator"
    authority_class: str = "operator"  # operator | agent_supervised | agent_autonomous
    task_id: str = ""
    task_type: str = ""
    files_in: list[dict[str, str]] = field(default_factory=list)
    timeout_ms: int = 0
    backend: str = "dry_run"
    backend_config: dict[str, Any] = field(default_factory=dict)
    record_access: str = "none"  # none | read_only | read_write
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])


@dataclass
class SandboxResult:
    request_id: str
    backend: str
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    files_out: list[dict[str, Any]] = field(default_factory=list)
    wall_ms: int = 0
    backend_cost: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    @property
    def success(self) -> bool:
        return self.exit_code == 0 and not self.error


# ── Authority ───────────────────────────────────────────────────────────

AUTHORITY_CLASSES = frozenset({"operator", "agent_supervised", "agent_autonomous"})
RECORD_ACCESS_LEVELS = frozenset({"none", "read_only", "read_write"})

_AUTHORITY_ALLOWED_ACCESS: dict[str, frozenset[str]] = {
    "operator": frozenset({"none", "read_only", "read_write"}),
    "agent_supervised": frozenset({"none", "read_only"}),
    "agent_autonomous": frozenset({"none"}),
}


def check_authority(request: SandboxRequest) -> str | None:
    """Return an error string if the request violates authority rules, else None."""
    if request.authority_class not in AUTHORITY_CLASSES:
        return f"unknown authority_class: {request.authority_class!r}"
    if request.record_access not in RECORD_ACCESS_LEVELS:
        return f"unknown record_access: {request.record_access!r}"
    allowed = _AUTHORITY_ALLOWED_ACCESS[request.authority_class]
    if request.record_access not in allowed:
        return (
            f"authority_class {request.authority_class!r} cannot request "
            f"record_access {request.record_access!r} (allowed: {sorted(allowed)})"
        )
    return None


# ── Backend protocol ────────────────────────────────────────────────────

@runtime_checkable
class SandboxBackend(Protocol):
    name: str

    def execute(
        self,
        command: str,
        files_in: list[dict[str, str]],
        timeout_ms: int,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        """Run command; return {exit_code, stdout, stderr, files_out, wall_ms, cost}."""
        ...

    def health(self) -> dict[str, Any]:
        """Return {ok: bool, notes: str}."""
        ...


# ── DryRunBackend ───────────────────────────────────────────────────────

class DryRunBackend:
    """Logs the request and returns a mock result. For testing governance without real compute."""

    name = "dry_run"

    def execute(
        self,
        command: str,
        files_in: list[dict[str, str]],
        timeout_ms: int,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "exit_code": 0,
            "stdout": f"[dry_run] would execute: {command}",
            "stderr": "",
            "files_out": [],
            "wall_ms": 0,
            "cost": {},
        }

    def health(self) -> dict[str, Any]:
        return {"ok": True, "notes": "dry_run backend always healthy"}


# ── LocalDockerBackend (stub) ───────────────────────────────────────────

class LocalDockerBackend:
    """Wraps `docker run`. Stub — not yet implemented."""

    name = "docker"

    def execute(
        self,
        command: str,
        files_in: list[dict[str, str]],
        timeout_ms: int,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError("LocalDockerBackend not yet implemented")

    def health(self) -> dict[str, Any]:
        try:
            result = subprocess.run(
                ["docker", "info"], capture_output=True, timeout=5, check=False,
            )
            return {"ok": result.returncode == 0, "notes": "docker daemon check"}
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return {"ok": False, "notes": "docker not available"}


# ── Backend registry ────────────────────────────────────────────────────

_BACKENDS: dict[str, SandboxBackend] = {
    "dry_run": DryRunBackend(),
    "docker": LocalDockerBackend(),
}


def get_backend(name: str) -> SandboxBackend | None:
    return _BACKENDS.get(name)


def register_backend(backend: SandboxBackend) -> None:
    _BACKENDS[backend.name] = backend


# ── Receipt emission ────────────────────────────────────────────────────

def _emit_receipt(
    user_id: str,
    request: SandboxRequest,
    result: SandboxResult,
    phase: str,
) -> None:
    """Emit a sandbox receipt to pipeline-events.jsonl."""
    try:
        from emit_pipeline_event import append_pipeline_event
    except ImportError:
        return

    extras = {
        "request_id": request.request_id,
        "caller": request.caller,
        "authority_class": request.authority_class,
        "backend": request.backend,
        "record_access": request.record_access,
        "phase": phase,
    }
    if request.task_id:
        extras["task_id"] = request.task_id
    if request.task_type:
        extras["task_type"] = request.task_type

    if phase == "post":
        extras["exit_code"] = str(result.exit_code)
        extras["wall_ms"] = str(result.wall_ms)
        extras["success"] = str(result.success).lower()
        extras["files_in_count"] = str(len(request.files_in))
        extras["files_out_count"] = str(len(result.files_out))
        if result.error:
            extras["error"] = result.error[:240]
        if result.files_out:
            extras["files_out_sha256"] = ",".join(
                f.get("sha256", "?") for f in result.files_out
            )

    append_pipeline_event(
        user_id,
        f"sandbox_execution_{phase}",
        None,
        extras=extras,
    )


def _emit_ledger(
    user_id: str,
    request: SandboxRequest,
    result: SandboxResult,
) -> None:
    """Append compute-ledger row for the sandbox execution."""
    try:
        from emit_compute_ledger import append_integration_ledger
    except ImportError:
        return

    total_bytes = sum(
        int(f.get("size_bytes", 0)) for f in result.files_out
    )
    for f_in in request.files_in:
        p = Path(f_in.get("path", ""))
        if p.is_file():
            try:
                total_bytes += p.stat().st_size
            except OSError:
                pass

    confidence: float | None = None
    if result.success:
        confidence = 1.0 if result.exit_code == 0 and not result.error else 0.5

    append_integration_ledger(
        user_id,
        operation="sandbox_execution",
        runtime=request.backend,
        success=result.success,
        wall_ms=result.wall_ms,
        bytes_processed=total_bytes,
        task_id=request.task_id,
        task_type=request.task_type,
        outcome_confidence=confidence,
        repo_root=REPO_ROOT,
    )


# ── Adapter core ────────────────────────────────────────────────────────

def execute(
    user_id: str,
    request: SandboxRequest,
    *,
    emit_receipts: bool = True,
) -> SandboxResult:
    """
    Run a sandbox request through the governance loop:
    1. Authority check
    2. Pre-execution receipt
    3. Delegate to backend
    4. Post-execution receipt
    5. Compute ledger row
    6. Return result
    """
    auth_error = check_authority(request)
    if auth_error:
        return SandboxResult(
            request_id=request.request_id,
            backend=request.backend,
            exit_code=1,
            error=f"authority_denied: {auth_error}",
        )

    backend = get_backend(request.backend)
    if backend is None:
        return SandboxResult(
            request_id=request.request_id,
            backend=request.backend,
            exit_code=1,
            error=f"unknown_backend: {request.backend!r}",
        )

    empty_result = SandboxResult(
        request_id=request.request_id, backend=request.backend,
    )
    if emit_receipts:
        _emit_receipt(user_id, request, empty_result, "pre")

    t0 = time.monotonic()
    try:
        raw = backend.execute(
            request.command,
            request.files_in,
            request.timeout_ms,
            request.backend_config,
        )
    except NotImplementedError as e:
        result = SandboxResult(
            request_id=request.request_id,
            backend=request.backend,
            exit_code=1,
            error=f"backend_not_implemented: {e}",
            wall_ms=int((time.monotonic() - t0) * 1000),
        )
        if emit_receipts:
            _emit_receipt(user_id, request, result, "post")
            _emit_ledger(user_id, request, result)
        return result
    except Exception as e:
        result = SandboxResult(
            request_id=request.request_id,
            backend=request.backend,
            exit_code=1,
            error=f"backend_error: {type(e).__name__}: {e}"[:300],
            wall_ms=int((time.monotonic() - t0) * 1000),
        )
        if emit_receipts:
            _emit_receipt(user_id, request, result, "post")
            _emit_ledger(user_id, request, result)
        return result

    wall = int((time.monotonic() - t0) * 1000)
    result = SandboxResult(
        request_id=request.request_id,
        backend=request.backend,
        exit_code=int(raw.get("exit_code", 0)),
        stdout=str(raw.get("stdout", "")),
        stderr=str(raw.get("stderr", "")),
        files_out=raw.get("files_out", []),
        wall_ms=raw.get("wall_ms", wall),
        backend_cost=raw.get("cost", {}),
    )

    if emit_receipts:
        _emit_receipt(user_id, request, result, "post")
        _emit_ledger(user_id, request, result)

    return result


# ── CLI ─────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sandbox adapter — governance-wrapped sandbox execution.",
    )
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--backend", default="dry_run", help="Backend name (dry_run, docker, …)")
    ap.add_argument("--command", required=True, help="Command to execute in sandbox")
    ap.add_argument("--caller", default="operator")
    ap.add_argument("--authority", default="operator", help="Authority class")
    ap.add_argument("--task-id", default="")
    ap.add_argument("--task-type", default="")
    ap.add_argument("--record-access", default="none")
    ap.add_argument("--timeout-ms", type=int, default=0)
    ap.add_argument("--no-receipts", action="store_true", help="Skip receipt/ledger emission")
    ap.add_argument("--json", action="store_true", dest="emit_json", help="Output JSON result")
    args = ap.parse_args()

    req = SandboxRequest(
        command=args.command,
        caller=args.caller,
        authority_class=args.authority,
        task_id=args.task_id,
        task_type=args.task_type,
        backend=args.backend,
        record_access=args.record_access,
        timeout_ms=args.timeout_ms,
    )

    result = execute(args.user, req, emit_receipts=not args.no_receipts)

    if args.emit_json:
        print(json.dumps(asdict(result), indent=2))
    else:
        status = "OK" if result.success else "FAIL"
        print(f"[{status}] request_id={result.request_id} backend={result.backend} exit={result.exit_code} wall={result.wall_ms}ms")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.error:
            print(f"error: {result.error}", file=sys.stderr)

    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
