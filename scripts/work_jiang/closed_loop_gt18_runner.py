#!/usr/bin/env python3
"""One-shot: complete closed-loop rounds 6–17 (predict → reveal → advance → bundle).

BLIND.md replay blocks are injected separately (see inject script). This only handles
scratch artifacts + subprocess calls. Operator lane; not CI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / "research/external/work-jiang/prediction-tracking/scratch"
BUNDLE_PY = ROOT / "scripts/work_jiang/forward_chain_blind_bundle.py"


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, cwd=str(ROOT))
    if r.returncode != 0:
        sys.exit(r.returncode)


def main() -> None:
    for r in range(6, 18):
        ep = r + 1
        pred = SCRATCH / f"gt-predict-{ep}.md"
        if not pred.is_file() or pred.stat().st_size == 0:
            sys.exit(f"missing prediction: {pred}")
        run(
            [
                sys.executable,
                str(BUNDLE_PY),
                "reveal",
                "--episode",
                str(ep),
                "--require-prediction-path",
                str(pred),
            ]
        )
        run(
            [
                sys.executable,
                str(BUNDLE_PY),
                "advance",
                "--completed-round",
                str(r),
            ]
        )
        next_k = r + 1
        if next_k > 17:
            break
        out = SCRATCH / f"gt-prefix-{next_k}.md"
        bundle_cmd = [
            sys.executable,
            str(BUNDLE_PY),
            "bundle",
            "--closed-loop",
            "--prefix-end",
            str(next_k),
            "-o",
            str(out),
        ]
        if next_k >= 10:
            bundle_cmd.append("--trim-at-full-transcript")
        run(bundle_cmd)


if __name__ == "__main__":
    main()
