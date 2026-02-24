#!/usr/bin/env python3
"""
OpenClaw integration hook: export Record for session continuity.

Usage:
    python integrations/openclaw_hook.py --user pilot-001
    python integrations/openclaw_hook.py -u pilot-001 -o ../openclaw/
    python integrations/openclaw_hook.py -u pilot-001 --format json+md --emit-event
"""

import argparse
import base64
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Delegate to unified export hook
from export_hook import run_export

REPO_ROOT = Path(__file__).resolve().parent.parent


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _collect_export_files(out_dir: Path, fmt: str) -> list[Path]:
    candidates = {
        "USER.md",
        "USER.json",
        "manifest.json",
        "llms.txt",
        "OPENCLAW-PRP.txt",
        "fork-export.json",
    }
    files = []
    for name in sorted(candidates):
        p = out_dir / name
        if p.exists() and p.is_file():
            files.append(p)
    return files


def _emit_openclaw_event(user_id: str, out_dir: Path, fmt: str, files: list[Path], status: str, error: str = "") -> None:
    hashes = ",".join(f"{p.name}:{_sha256(p)}" for p in files)
    extras = [
        f"target=openclaw",
        f"status={status}",
        f"format={fmt}",
        f"output_dir={str(out_dir)}",
        f"file_count={len(files)}",
    ]
    if hashes:
        extras.append(f"file_hashes={hashes}")
    if error:
        extras.append(f"error={error[:240]}")
    subprocess.run(
        [
            sys.executable,
            "scripts/emit_pipeline_event.py",
            "--user",
            user_id,
            "openclaw_export",
            "none",
            *extras,
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def _post_export(post_url: str, user_id: str, files: list[Path], api_key: str = "") -> None:
    payload_files = []
    for path in files:
        raw = path.read_bytes()
        payload_files.append(
            {
                "name": path.name,
                "sha256": _sha256(path),
                "content_base64": base64.b64encode(raw).decode("ascii"),
            }
        )
    payload = json.dumps({"user_id": user_id, "files": payload_files}).encode("utf-8")
    req = Request(post_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("X-Api-Key", api_key)
    urlopen(req, timeout=30)


def run_openclaw_export(
    user_id: str,
    output: Path | None,
    fmt: str,
    destination: str,
    post_url: str,
    api_key: str,
    emit_event: bool,
) -> int:
    out_dir = output or (REPO_ROOT / "users" / user_id)
    rc = run_export("openclaw", out_dir, user_id, openclaw_format=fmt)
    files = _collect_export_files(out_dir, fmt)
    if rc != 0:
        if emit_event:
            _emit_openclaw_event(user_id, out_dir, fmt, files, status="failed", error=f"export_exit={rc}")
        return rc
    if destination == "post":
        if not post_url.strip():
            err = "post destination requires --post-url"
            if emit_event:
                _emit_openclaw_event(user_id, out_dir, fmt, files, status="failed", error=err)
            print(err, file=sys.stderr)
            return 2
        try:
            _post_export(post_url, user_id, files, api_key=api_key.strip())
        except (HTTPError, URLError, TimeoutError, OSError) as e:
            err = f"post_export_error: {e}"
            if emit_event:
                _emit_openclaw_event(user_id, out_dir, fmt, files, status="failed", error=err)
            print(err, file=sys.stderr)
            return 3
    if emit_event:
        _emit_openclaw_event(user_id, out_dir, fmt, files, status="ok")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Grace-Mar Record for OpenClaw")
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    parser.add_argument(
        "--format",
        choices=["md", "md+manifest", "json+md", "full-prp", "fork-json"],
        default="md+manifest",
        help="Export shape",
    )
    parser.add_argument(
        "--destination",
        choices=["local", "post"],
        default="local",
        help="Write locally or POST exported payload",
    )
    parser.add_argument("--post-url", default="", help="POST destination URL when --destination post")
    parser.add_argument("--api-key", default="", help="Optional API key for post destination (X-Api-Key)")
    parser.add_argument("--emit-event", action="store_true", help="Emit openclaw_export event to pipeline log")
    args = parser.parse_args()
    out = Path(args.output) if args.output else None
    return run_openclaw_export(
        user_id=args.user,
        output=out,
        fmt=args.format,
        destination=args.destination,
        post_url=args.post_url,
        api_key=args.api_key,
        emit_event=args.emit_event,
    )


if __name__ == "__main__":
    sys.exit(main())
