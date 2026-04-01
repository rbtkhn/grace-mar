#!/usr/bin/env python3
"""
Append a cadence event (coffee / dream / bridge) to work-cadence-events.md.

One line per run. Not Record truth; not self-memory; not a replacement for
last-dream.json or session-transcript.md. See docs/skill-work/work-cadence/.

Usage:
  python3 scripts/log_cadence_event.py --kind dream -u grace-mar --ok --mode default \
      --kv integrity=pass governance=pass mem_changed=true
  python3 scripts/log_cadence_event.py --kind coffee -u grace-mar --ok --mode work-start \
      --kv gate_pending=0
  python3 scripts/log_cadence_event.py --kind bridge -u grace-mar --ok \
      --kv refs=aacec9e,4eaf1f4
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"
ANCHOR = "_(Append below this line.)_"
KINDS = ("coffee", "dream", "bridge")

HEADER = (
    "# Cadence events\n"
    "\n"
    "> Append-only audit of **coffee**, **dream**, and **bridge** runs.\n"
    "> **Not** Record truth. **Not** self-memory. **Not** a replacement for "
    "`last-dream.json` or `session-transcript.md`.\n"
    ">\n"
    "> **Format:** `- **YYYY-MM-DD HH:MM UTC** — kind (user) key=value ...`\n"
    ">\n"
    "> See [work-cadence README](README.md) and "
    "[work-modules-history-principle](../work-modules-history-principle.md).\n"
    "\n"
    f"{ANCHOR}\n"
)

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def append_cadence_event(
    kind: str,
    user_id: str,
    *,
    ok: bool = True,
    mode: str | None = None,
    kv: dict[str, str] | None = None,
    events_path: Path = EVENTS_PATH,
) -> Path:
    """Append one cadence event line. Returns the path written to."""
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [f"- **{ts}** — {kind} ({user_id}) ok={'true' if ok else 'false'}"]
    if mode:
        parts.append(f"mode={mode}")
    for k, v in (kv or {}).items():
        safe = str(v).replace("\n", " ")[:200]
        parts.append(f"{k}={safe}")
    line = " ".join(parts) + "\n"

    events_path.parent.mkdir(parents=True, exist_ok=True)

    if not events_path.is_file():
        events_path.write_text(HEADER + line, encoding="utf-8")
    else:
        with open(events_path, "a", encoding="utf-8") as f:
            f.write(line)
    return events_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", required=True, choices=KINDS, help="Cadence type")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    ap.add_argument("--ok", action="store_true", default=False, help="Run succeeded")
    ap.add_argument("--no-ok", dest="ok", action="store_false", help="Run failed")
    ap.add_argument("--mode", default=None, help="Run mode (e.g. work-start, strict, default)")
    ap.add_argument("--kv", nargs="*", default=[], metavar="KEY=VALUE", help="Extra key=value pairs")
    args = ap.parse_args()

    kv_dict: dict[str, str] = {}
    for item in args.kv:
        if "=" in item:
            k, v = item.split("=", 1)
            kv_dict[k] = v
        else:
            kv_dict[item] = "true"

    path = append_cadence_event(
        args.kind,
        args.user.strip(),
        ok=args.ok,
        mode=args.mode,
        kv=kv_dict,
    )
    print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
