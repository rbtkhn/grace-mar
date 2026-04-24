#!/usr/bin/env python3
"""Deprecated entrypoint: forwards to cici_journal_ob1_digest (same argv)."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    here = Path(__file__).resolve().parent / "cici_journal_ob1_digest.py"
    sys.argv[0] = str(here)
    runpy.run_path(str(here), run_name="__main__")
