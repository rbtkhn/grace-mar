#!/usr/bin/env python3
"""
Record write policy for commit-msg hooks (fork lifecycle).

Delegates to check_gated_record_commit_msg (gated paths + MERGE-RECEIPT / SNAPSHOT tokens).
Install alongside the gated-record hook or use as the single commit-msg entry.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_gated_record_commit_msg import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
