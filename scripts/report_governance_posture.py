#!/usr/bin/env python3
"""
Emit a partner- and operator-facing governance posture one-pager (Markdown).

Read-only with respect to Record: only writes the output file. See
docs/skill-work/work-dev/safety-story-ux.md and AGENTS.md.

  python3 scripts/report_governance_posture.py -u grace-mar
  python3 scripts/report_governance_posture.py -u grace-mar -o artifacts/governance-posture.md
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import profile_dir  # noqa: E402


def _git_short_hash(cwd: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return "unknown"


def _file_status(root: Path, rel: str) -> str:
    p = root / rel
    if p.is_file():
        return "present"
    if p.is_dir():
        return "present (dir)"
    return "missing"


def build_governance_posture_markdown(
    repo_root: Path,
    user_id: str,
    *,
    generated_at_utc: str | None = None,
    git_ref: str | None = None,
    profile_override: Path | None = None,
) -> str:
    """Build Markdown body for the governance posture one-pager.

    If ``profile_override`` is set (e.g. in tests), file-presence rows use that directory
    instead of ``users/<user_id>/`` under the real repo.
    """
    uid = user_id.strip() or "grace-mar"
    base = f"users/{uid}"
    prof = profile_override if profile_override is not None else profile_dir(uid)
    ts = generated_at_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    gref = git_ref if git_ref is not None else _git_short_hash(repo_root)

    audit_files: list[tuple[str, str]] = [
        (f"{base}/recursion-gate.md", "Gate queue and candidate YAML"),
        (f"{base}/self.md", "Record profile (canonical identity)"),
        (f"{base}/self-archive.md", "EVIDENCE (dated spine)"),
        (f"{base}/merge-receipts.jsonl", "Merge batch receipts (append-only)"),
        (f"{base}/pipeline-events.jsonl", "Pipeline staged vs applied"),
        (f"{base}/harness-events.jsonl", "Harness / audit-lane events"),
        (f"{base}/session-log.md", "Session and merge footnotes"),
        (f"{base}/self-evidence.md", "Optional ACT pointer / alternate evidence entry"),
    ]

    lines: list[str] = [
        "# Governance posture (generated)\n\n",
        "_Technical operations summary for this repository instance. **Not** legal, regulatory, or medical "
        "compliance advice; for operational visibility and partner conversations only._\n\n",
        f"- **User id:** `{uid}`\n",
        f"- **Generated (UTC):** {ts}\n",
        f"- **Repo `HEAD` (short):** `{gref}`\n\n",
        "## Triad (where authority sits)\n\n",
        "- **Mind (human):** holds merge authority and meaning.\n",
        "- **Record:** documented self in `self.md`, evidence in `self-archive.md` — updated **only** through the "
        "gated pipeline after companion approval.\n",
        "- **Voice:** `bot/` renders the Record when queried; it does **not** replace the pipeline. "
        "See [docs/conceptual-framework.md](../docs/conceptual-framework.md) for the full distinction.\n\n",
        "## No silent merge\n\n",
        "1. Proposals land as **`### CANDIDATE-…`** blocks in `recursion-gate.md` (staging).\n",
        "2. The **companion** approves; the operator runs "
        "`python3 scripts/process_approved_candidates.py --apply` (see [AGENTS.md](../AGENTS.md)).\n",
        "3. **OpenClaw and assistants stage only** — they do not write SELF, EVIDENCE, or `bot/prompt.py` without "
        "that merge. Chat is not proof of Record truth.\n\n",
        "## Inspectability (what “safe” means here)\n\n",
        "Same dimensions as [safety-story-ux.md](../docs/skill-work/work-dev/safety-story-ux.md), with paths "
        f"for **`{base}/`**:\n\n",
        "| Dimension | Question | Where |\n",
        "|-----------|----------|-------|\n",
        "| **Pending vs approved** | Waiting on a human, or already processed? | "
        f"`{base}/recursion-gate.md` |\n",
        "| **Staged vs merged** | Staged only, or written to the Record? | Staging → gate; merge → "
        "`process_approved_candidates.py` ([AGENTS.md](../AGENTS.md)) |\n",
        "| **Receipts** | What batch landed? | "
        f"`{base}/merge-receipts.jsonl` |\n",
        "| **Pipeline events** | Staged vs applied linked? | "
        f"`{base}/pipeline-events.jsonl` |\n",
        "| **Last merge footprint** | Evidence / session line? | "
        f"`{base}/self-evidence.md` (if used), `{base}/session-log.md` |\n",
        "| **Harness / replay** | Explain a candidate or event? | "
        f"`{base}/harness-events.jsonl` + `python3 scripts/replay_harness_event.py` "
        "([harness-replay.md](../docs/harness-replay.md)) |\n\n",
        "**Partner-facing line:** *We separate “suggested” from “committed” — receipts and gate state are "
        "inspectable on disk.*\n\n",
        f"## Audit file presence (`{uid}`)\n\n",
        "| Path | Status | Note |\n",
        "|------|--------|------|\n",
    ]
    for rel, note in audit_files:
        relp = rel.removeprefix(f"{base}/")
        st = _file_status(prof, relp)
        lines.append(f"| `{rel}` | {st} | {note} |\n")
    lines.append("\n")

    lines.extend(
        [
            "## Verification (copy-paste)\n\n",
            "Replace the user id if needed.\n\n",
            "```bash\n",
            f"python3 scripts/validate-integrity.py --user {uid}\n",
            f"python3 scripts/run_voice_benchmark.py -o users/{uid}/artifacts/voice_benchmark_results.json\n",
            f"python3 scripts/replay_harness_event.py -u {uid} --candidate CANDIDATE-0000   # example; use a real id\n",
            f"python3 scripts/report_governance_posture.py -u {uid}\n",
            "```\n\n",
            "Further reading: [voice-benchmark-suite.md](../docs/voice-benchmark-suite.md), "
            "[openclaw-integration.md](../docs/openclaw-integration.md).\n\n",
            "---\n\n",
            "_Operator / audit lane only. For identity truth, use approved Record files under `users/`. "
            "This file is derived and safe to regenerate._\n",
        ]
    )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Write governance-posture.md (generated operator summary).")
    ap.add_argument("-u", "--user", default="grace-mar", help="User id (fork under users/)")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "governance-posture.md",
        help="Output Markdown path (default: artifacts/governance-posture.md)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (for path resolution; default: repo containing this script)",
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()
    uid = args.user.strip() or "grace-mar"
    out: Path = args.output
    if not out.is_absolute():
        out = (root / out).resolve()
    md = build_governance_posture_markdown(root, uid)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
