#!/usr/bin/env python3
"""Run performance tier 1 only (local micro-benchmarks, CI-friendly). Delegates to run_perf_suite.py."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
suite = REPO_ROOT / "scripts" / "run_perf_suite.py"
argv = [sys.executable, str(suite), "--tier", "1"] + sys.argv[1:]
raise SystemExit(subprocess.call(argv, cwd=str(REPO_ROOT)))
