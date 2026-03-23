#!/usr/bin/env python3
"""
Parse and validate META_INFRA candidates in recursion-gate.md; optional sandbox apply + perf.

Phase A (default): list META blocks, validate allowlist + diff presence, optionally write JSON reports
under users/<id>/artifacts/meta-reports/.

Phase B (--sandbox): copy repo to a temp directory, git apply --check / apply, run
run_perf_suite tier 1-2 with --check-baseline and validate-integrity; write reports and
copy unified diff to users/<id>/artifacts/meta-patches/ for manual git apply on the real tree.

Does NOT modify recursion-gate.md. Does NOT commit. See docs/meta-class-proposals.md.

Usage:
  python3 scripts/process_meta_candidates.py -u grace-mar
  python3 scripts/process_meta_candidates.py -u grace-mar --write-report
  python3 scripts/process_meta_candidates.py -u grace-mar --only CANDIDATE-0090 --sandbox
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from recursion_gate_review import split_gate_sections
    from repo_io import fork_root
except ImportError:
    from scripts.recursion_gate_review import split_gate_sections
    from scripts.repo_io import fork_root

# Repo-relative path prefixes allowed for META diffs and meta_targets
ALLOWLIST_PREFIXES: tuple[str, ...] = (
    "scripts/",
    "config/",
    "bot/",
    "integrations/",
    "apps/",
)

_CANDIDATE_RE = re.compile(
    r"### (CANDIDATE-\d+)(?:\s*\(([^)]*)\))?\s*\n\s*```yaml\n(.*?)```",
    re.DOTALL,
)


def _norm_rel(p: str) -> str:
    return p.replace("\\", "/").strip().lstrip("/")


def is_allowlisted_path(rel: str) -> bool:
    """True if rel is under allowed infra dirs (or meta-diff artifact under users/.../artifacts/meta-diffs/)."""
    r = _norm_rel(rel)
    if ".." in r or r.startswith("/"):
        return False
    if r.startswith("users/") and "/artifacts/meta-diffs/" in r:
        return True
    return any(r.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)


def paths_in_unified_diff(diff_text: str) -> set[str]:
    """Collect paths from a unified diff (best-effort)."""
    out: set[str] = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:].split("\t")[0].strip()
            if path != "/dev/null":
                out.add(path)
    return out


def _yaml_scalar(body: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.+)$", body, re.MULTILINE)
    return (m.group(1).strip().strip('"\'')) if m else ""


def _extract_pipe_block(body: str, key: str) -> str:
    """Content after `key: |` until next top-level `word:` key."""
    m = re.search(rf"^{key}:\s*\|\s*\n", body, re.MULTILINE)
    if not m:
        return ""
    rest = body[m.end() :]
    out_lines: list[str] = []
    for line in rest.splitlines():
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*", line):
            break
        out_lines.append(line)
    return "\n".join(out_lines).strip()


def _targets_from_body(yaml_body: str) -> list[str]:
    """meta_targets as pipe block or bullet list."""
    pipe = _extract_pipe_block(yaml_body, "meta_targets")
    if pipe:
        return [ln.strip() for ln in pipe.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    m = re.search(r"^meta_targets:\s*\n((?:  - .+\n)+)", yaml_body, re.MULTILINE)
    if m:
        lines = []
        for ln in m.group(1).splitlines():
            ln = ln.strip()
            if ln.startswith("- "):
                lines.append(ln[2:].strip())
        return lines
    return []


def _load_diff_text(yaml_body: str) -> tuple[str, str]:
    """
    Return (diff_text, source_label).
    Prefer meta_artifact_path, then meta_diff pipe block.
    """
    art = _yaml_scalar(yaml_body, "meta_artifact_path") or _yaml_scalar(yaml_body, "artifact_path")
    if art:
        path = REPO_ROOT / _norm_rel(art)
        if path.is_file():
            return path.read_text(encoding="utf-8"), f"artifact:{art}"
        return "", f"missing artifact: {art}"

    diff_block = _extract_pipe_block(yaml_body, "meta_diff")
    if diff_block:
        return diff_block, "inline:meta_diff"
    return "", "none"


def extract_meta_candidates(gate_text: str) -> list[dict[str, Any]]:
    """Return one dict per ### CANDIDATE block with proposal_class META_INFRA."""
    active, _ = split_gate_sections(gate_text)
    out: list[dict[str, Any]] = []
    for m in _CANDIDATE_RE.finditer(active):
        cid = m.group(1)
        title = (m.group(2) or "").strip()
        yaml_body = m.group(3)
        pc = _yaml_scalar(yaml_body, "proposal_class").upper()
        if pc != "META_INFRA":
            continue
        diff_text, diff_src = _load_diff_text(yaml_body)
        targets = _targets_from_body(yaml_body)
        out.append({
            "id": cid,
            "title": title,
            "yaml_raw": yaml_body,
            "meta_risk": _yaml_scalar(yaml_body, "meta_risk"),
            "meta_targets": targets,
            "diff_text": diff_text,
            "diff_source": diff_src,
            "full_match": m.group(0),
        })
    return out


def validate_meta_candidate(c: dict[str, Any], user_id: str) -> tuple[bool, list[str]]:
    """Return (ok, errors)."""
    errs: list[str] = []
    if not c.get("meta_targets"):
        errs.append("meta_targets missing or empty")
    for t in c.get("meta_targets") or []:
        if not is_allowlisted_path(t):
            errs.append(f"target not allowlisted: {t}")

    diff = (c.get("diff_text") or "").strip()
    if not diff:
        errs.append("no diff (meta_diff or meta_artifact_path)")
    else:
        for p in paths_in_unified_diff(diff):
            if not is_allowlisted_path(p):
                errs.append(f"diff touches non-allowlisted path: {p}")

    return (len(errs) == 0, errs)


def _write_report(user_id: str, c: dict[str, Any], ok: bool, errors: list[str], extra: dict[str, Any]) -> Path:
    out_dir = fork_root(user_id) / "artifacts" / "meta-reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "candidate_id": c["id"],
        "title": c.get("title"),
        "valid": ok,
        "validation_errors": errors,
        "meta_risk": c.get("meta_risk"),
        "meta_targets": c.get("meta_targets"),
        "diff_source": c.get("diff_source"),
        "diff_sha256": hashlib.sha256((c.get("diff_text") or "").encode("utf-8")).hexdigest(),
        **extra,
    }
    path = out_dir / f"{c['id']}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _ignore_sandbox(dirpath: str, names: list[str]) -> list[str]:
    skip = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache"}
    return [n for n in names if n in skip]


def _run_sandbox(
    user_id: str,
    c: dict[str, Any],
    diff_text: str,
) -> dict[str, Any]:
    """Apply diff in temp copy and run perf + integrity."""
    result: dict[str, Any] = {"sandbox": True}
    with tempfile.TemporaryDirectory(prefix="meta-sandbox-") as tmp:
        sand = Path(tmp) / "repo"
        shutil.copytree(REPO_ROOT, sand, ignore=_ignore_sandbox)
        patch_file = Path(tmp) / "proposal.patch"
        patch_file.write_text(diff_text, encoding="utf-8")

        chk = subprocess.run(
            ["git", "apply", "--check", str(patch_file)],
            cwd=sand,
            capture_output=True,
            text=True,
        )
        if chk.returncode != 0:
            result["git_apply_check"] = False
            result["git_apply_stderr"] = (chk.stderr or chk.stdout or "")[:2000]
            return result

        ap = subprocess.run(
            ["git", "apply", str(patch_file)],
            cwd=sand,
            capture_output=True,
            text=True,
        )
        if ap.returncode != 0:
            result["git_apply"] = False
            result["git_apply_stderr"] = (ap.stderr or ap.stdout or "")[:2000]
            return result

        result["git_apply_check"] = True
        result["git_apply"] = True

        py = sys.executable
        perf_out = Path(tmp) / "perf.json"
        perf = subprocess.run(
            [
                py,
                str(sand / "scripts" / "run_perf_suite.py"),
                "--tier",
                "1",
                "2",
                "-u",
                user_id,
                "-o",
                str(perf_out),
                "--check-baseline",
            ],
            cwd=sand,
            capture_output=True,
            text=True,
            timeout=600,
        )
        result["perf_exit_code"] = perf.returncode
        result["perf_stderr_tail"] = (perf.stderr or "")[-1500:]
        if perf_out.is_file():
            try:
                result["perf_json"] = json.loads(perf_out.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                result["perf_json_error"] = True

        vi = subprocess.run(
            [py, str(sand / "scripts" / "validate-integrity.py"), "--user", user_id, "--json"],
            cwd=sand,
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["integrity_exit_code"] = vi.returncode
        try:
            result["integrity_json"] = json.loads(vi.stdout or "{}")
        except json.JSONDecodeError:
            result["integrity_stdout"] = (vi.stdout or "")[:2000]

    return result


def _write_patch_artifact(user_id: str, cid: str, diff_text: str) -> Path:
    out_dir = fork_root(user_id) / "artifacts" / "meta-patches"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{cid}.patch"
    path.write_text(diff_text, encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="META_INFRA gate candidate validation and optional sandbox checks.")
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    ap.add_argument("--write-report", action="store_true", help="Write meta-reports/*.json per candidate")
    ap.add_argument("--sandbox", action="store_true", help="Run git apply + perf + integrity in temp copy (slow)")
    ap.add_argument("--only", default="", help="Process only this CANDIDATE id (e.g. CANDIDATE-0090)")
    args = ap.parse_args()
    user_id = args.user.strip() or "grace-mar"
    gate_path = fork_root(user_id) / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"No gate file: {gate_path}", file=sys.stderr)
        return 1

    gate_text = gate_path.read_text(encoding="utf-8")
    candidates = extract_meta_candidates(gate_text)
    if args.only.strip():
        want = args.only.strip().upper()
        if not want.startswith("CANDIDATE-"):
            want = f"CANDIDATE-{want.replace('CANDIDATE-', '')}"
        candidates = [c for c in candidates if c["id"].upper() == want]

    if not candidates:
        print("No META_INFRA candidates found in active (pre-Processed) section.")
        return 0

    exit_code = 0
    for c in candidates:
        ok, errors = validate_meta_candidate(c, user_id)
        print(f"{c['id']}: {'OK' if ok else 'FAIL'} — {c.get('title', '')[:60]}")
        if errors:
            for e in errors:
                print(f"  - {e}")
            exit_code = 1

        extra: dict[str, Any] = {}
        if args.sandbox and ok and (c.get("diff_text") or "").strip():
            print(f"  Running sandbox checks for {c['id']} …")
            extra = _run_sandbox(user_id, c, c["diff_text"])
            if extra.get("git_apply_check") and extra.get("git_apply"):
                patch_path = _write_patch_artifact(user_id, c["id"], c["diff_text"])
                extra["patch_written"] = str(patch_path.relative_to(REPO_ROOT))
            if extra.get("perf_exit_code") not in (0, None):
                exit_code = 1
            if extra.get("integrity_exit_code") not in (0, None):
                exit_code = 1

        if args.write_report or args.sandbox:
            report_path = _write_report(user_id, c, ok, errors, extra)
            print(f"  Report: {report_path.relative_to(REPO_ROOT)}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
