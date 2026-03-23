"""Generate evidence pack for every chapter in book-architecture.yaml."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"


def main() -> int:
    arch = yaml.safe_load((WORK_DIR / "metadata" / "book-architecture.yaml").read_text(encoding="utf-8"))
    chapters = (arch.get("book") or {}).get("chapters") or []
    script = ROOT / "scripts" / "work_jiang" / "build_evidence_pack.py"
    for ch in chapters:
        cid = ch.get("id")
        if not cid:
            continue
        r = subprocess.run(
            [sys.executable, str(script), "--chapter", cid],
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            return r.returncode
    # Refresh STATUS counts
    status_script = ROOT / "scripts" / "work_jiang" / "render_status_dashboard.py"
    subprocess.run([sys.executable, str(status_script)], cwd=str(ROOT), check=False)
    print("Done. STATUS.md refreshed via render_status_dashboard.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
