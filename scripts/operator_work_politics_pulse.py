#!/usr/bin/env python3
"""
Work-politics operator pulse — **preferred script name**.

Delegates to `operator_wap_pulse.py` (implementation module; legacy filename).
"""

from __future__ import annotations

import sys

from operator_wap_pulse import main

if __name__ == "__main__":
    raise SystemExit(main())
