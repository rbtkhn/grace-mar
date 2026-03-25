#!/usr/bin/env python3
"""If a PR has no primary lane/* label, post or update a comment with inferred lane (friendly CI).

Uses GITHUB_TOKEN and GITHUB_EVENT_PATH (pull_request). Idempotent: one comment per PR,
updated on new pushes while labels are still missing.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_lane_scope import LANES_PATH, load_lanes  # noqa: E402
from infer_lane_from_paths import infer_dominant  # noqa: E402

MARKER = "<!-- grace-mar-lane-hint -->\n"
CROSS_LABEL = "lane/cross"


def _primary_lane_ids(label_names: list[str]) -> list[str]:
    out: list[str] = []
    for raw in label_names:
        s = raw.strip()
        if s.lower() == CROSS_LABEL:
            continue
        if s.lower().startswith("lane/"):
            out.append(s[len("lane/") :].strip())
    return out


def _github_json(method: str, url: str, token: str, data: dict | None = None) -> Any:
    payload = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"GitHub HTTP {e.code}: {err_body}") from e
    if not raw:
        return None
    return json.loads(raw)


def main() -> int:
    token = (os.getenv("GITHUB_TOKEN") or "").strip()
    event_path = (os.getenv("GITHUB_EVENT_PATH") or "").strip()
    if not token or not event_path:
        print("pr_lane_label_hint: skip (no GITHUB_TOKEN or GITHUB_EVENT_PATH)", file=sys.stderr)
        return 0

    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr = event.get("pull_request")
    if not isinstance(pr, dict):
        return 0

    label_names = [
        str(x.get("name", "")).strip()
        for x in (pr.get("labels") or [])
        if isinstance(x, dict) and str(x.get("name", "")).strip()
    ]
    if _primary_lane_ids(label_names):
        return 0

    base = str((pr.get("base") or {}).get("sha") or "").strip()
    head = str((pr.get("head") or {}).get("sha") or "").strip()
    if not base or not head:
        return 0

    proc = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", f"{base}...{head}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return 0
    files = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if not files:
        return 0

    doc = load_lanes(LANES_PATH)
    dom = infer_dominant(files, doc)
    lanes_cfg = doc.get("lanes") or {}
    lane_keys = sorted(lanes_cfg.keys())

    repo = event.get("repository")
    full = str((repo or {}).get("full_name") or "").strip()
    num = pr.get("number")
    if not full or not isinstance(num, int):
        return 0

    lines = [
        MARKER.rstrip(),
        "### Lane label needed for CI",
        "",
        "This PR has no **`lane/...`** GitHub label. The **Lane scope** check on `main` needs one.",
        "",
    ]
    if dom in lanes_cfg:
        lines.append(f"**Inference from changed files:** `{dom}` → add label **`lane/{dom}`**.")
        if dom == "work-jiang":
            lines.append(
                "- Jiang lane reference: **`docs/skill-work/work-jiang/LANE-CI.md`** "
                "(PR labels vs `### CANDIDATE-*` paste shape into the gate)."
            )
        if dom == "work-politics":
            lines.append(
                "- Work-politics reference: **`docs/skill-work/work-politics/LANE-CI.md`** "
                "(PR labels, `territory: work-politics`, `operator:wap:*` channel_key, paste helpers)."
            )
        if dom == "work-strategy":
            lines.append(
                "- Work-strategy reference: **`docs/skill-work/work-strategy/LANE-CI.md`** "
                "(PR labels; gate paste defaults: `territory: work-politics` + `channel_key: operator:work-strategy`)."
            )
    elif dom == "mixed":
        lines.append(
            "**Inference:** the diff likely **spans multiple lanes**. Add **`lane/cross`** plus a "
            "justification in the PR body, or **split** the PR."
        )
    else:
        lines.append(
            f"**Inference:** could not map paths to one lane (result `{dom}`). Pick the closest **`lane/<id>`** below."
        )
    lines.extend(
        [
            "",
            "**Lane ids:** " + ", ".join(f"`{n}`" for n in lane_keys) + ".",
            "",
            "See `.github/pull_request_template.md` for the table and cross-lane rules.",
        ]
    )
    body = "\n".join(lines) + "\n"

    list_url = f"https://api.github.com/repos/{full}/issues/{num}/comments"
    try:
        existing = _github_json("GET", list_url + "?per_page=100", token)
    except RuntimeError as e:
        print(f"pr_lane_label_hint: {e}", file=sys.stderr)
        return 0

    comment_id: int | None = None
    if isinstance(existing, list):
        for c in existing:
            if not isinstance(c, dict):
                continue
            if MARKER.strip() in str(c.get("body") or ""):
                cid = c.get("id")
                if isinstance(cid, int):
                    comment_id = cid
                break

    try:
        if comment_id is not None:
            patch_url = f"https://api.github.com/repos/{full}/issues/comments/{comment_id}"
            _github_json("PATCH", patch_url, token, {"body": body})
            print(f"pr_lane_label_hint: updated comment {comment_id}")
        else:
            _github_json("POST", list_url, token, {"body": body})
            print("pr_lane_label_hint: posted new comment")
    except RuntimeError as e:
        print(f"pr_lane_label_hint: {e}", file=sys.stderr)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
