#!/usr/bin/env python3
"""Operator command **``thread``**: rebuild per-expert rolling corpus from inbox.

After **``thread:<expert_id>``** paste-ready lines are in
``docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md``,
run::

    python3 scripts/strategy_thread.py

This delegates to ``scripts/strategy_expert_corpus.py`` with the **same**
CLI (``--inbox``, ``--threads``, ``--out``, ``--days``, ``--today``,
``--dry-run``). **Not** **``weave``**: **``thread``** updates
``strategy-expert-<expert_id>.md`` rolling blocks only; it does **not**
merge into ``days.md`` or knot pages. **Seed** sections in those files
stay operator-edited; do not hand-edit the script-delimited corpus block
expecting it to persist across runs.

WORK-only; not Record.

Spec: ``docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md``
§ *Thread (terminology)*.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    corpus = REPO_ROOT / "scripts" / "strategy_expert_corpus.py"
    if not corpus.is_file():
        print("error: strategy_expert_corpus.py not found", file=sys.stderr)
        return 1
    return subprocess.call(
        [sys.executable, str(corpus), *sys.argv[1:]],
        cwd=str(REPO_ROOT),
    )


if __name__ == "__main__":
    raise SystemExit(main())
