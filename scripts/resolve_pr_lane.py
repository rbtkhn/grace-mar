#!/usr/bin/env python3
"""Resolve declared PR lane from GitHub pull_request event (labels + body).

Reads GITHUB_EVENT_PATH. Writes PR_LANE, ALLOW_CROSS_LANE, LANE_CROSS_JUSTIFICATION
to GITHUB_ENV when set; otherwise prints assignments for local debugging.

Label convention:
  - Exactly one primary lane label: lane/<id> where <id> matches lanes.yaml keys
    (e.g. lane/work-dev, lane/work-jiang).
  - Optional lane/cross: requires one primary lane label and non-empty justification
    in the PR body (fenced block under ### Cross-lane justification).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LANE_PREFIX = "lane/"
CROSS_LABEL = "lane/cross"


def _primary_lane_from_label(name: str) -> str | None:
    n = name.strip()
    if n.lower() == CROSS_LABEL:
        return None
    if not n.lower().startswith(LANE_PREFIX):
        return None
    return n[len(LANE_PREFIX) :].strip()


def parse_cross_lane_justification(body: str) -> str:
    """Extract text from the first fenced code block after '### Cross-lane justification'."""
    if not (body or "").strip():
        return ""
    idx = body.find("### Cross-lane justification")
    if idx < 0:
        return ""
    tail = body[idx:]
    m = re.search(r"```(?:text)?\s*\n(.*?)```", tail, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    return m.group(1).strip()


def _write_github_env(key: str, value: str, fh) -> None:
    """Append one var to GITHUB_ENV (multiline-safe delimiter form)."""
    if "\n" in value or "\r" in value:
        delim = "LANE_RESOLVE_EOF"
        fh.write(f"{key}<<{delim}\n")
        fh.write(value.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n")
        fh.write(f"{delim}\n")
    else:
        fh.write(f"{key}={value}\n")


def resolve(
    pr: dict,
) -> tuple[str, bool, str] | tuple[None, None, str]:
    """Return (pr_lane, allow_cross, justification) or (None, None, error_message)."""
    labels = pr.get("labels") or []
    names = []
    for x in labels:
        if isinstance(x, dict):
            n = str(x.get("name", "")).strip()
            if n:
                names.append(n)

    cross = any(n.lower() == CROSS_LABEL for n in names)
    lane_labels: list[str] = []
    for n in names:
        lid = _primary_lane_from_label(n)
        if lid:
            lane_labels.append(lid)

    body = str(pr.get("body") or "")
    justification = parse_cross_lane_justification(body)

    if cross:
        if len(lane_labels) != 1:
            return (
                None,
                None,
                "lane/cross requires exactly one primary lane label (e.g. lane/work-dev)",
            )
        if not justification:
            return (
                None,
                None,
                "lane/cross requires a non-empty fenced justification under "
                "### Cross-lane justification in the PR body",
            )
        return lane_labels[0], True, justification

    if len(lane_labels) == 0:
        return (
            None,
            None,
            "add exactly one lane label (e.g. lane/work-dev); use lane/cross + justification if needed",
        )
    if len(lane_labels) > 1:
        return None, None, f"multiple primary lane labels: {lane_labels!r}; keep one"

    return lane_labels[0], False, ""


def main() -> int:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        print("error: GITHUB_EVENT_PATH not set (run in GitHub Actions)", file=sys.stderr)
        return 2

    data = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr = data.get("pull_request")
    if not isinstance(pr, dict):
        print("error: pull_request missing from event", file=sys.stderr)
        return 2

    out = resolve(pr)
    if out[0] is None:
        print(f"error: {out[2]}", file=sys.stderr)
        return 2

    pr_lane, allow_cross, justification = out
    gh_env = os.getenv("GITHUB_ENV")
    if gh_env:
        with open(gh_env, "a", encoding="utf-8") as f:
            _write_github_env("PR_LANE", pr_lane, f)
            _write_github_env("ALLOW_CROSS_LANE", "true" if allow_cross else "false", f)
            _write_github_env("LANE_CROSS_JUSTIFICATION", justification, f)
        print(f"resolve_pr_lane: PR_LANE={pr_lane!r} allow_cross={allow_cross}")
    else:
        print(f"PR_LANE={pr_lane}")
        print(f"ALLOW_CROSS_LANE={'true' if allow_cross else 'false'}")
        print(f"LANE_CROSS_JUSTIFICATION={justification!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
