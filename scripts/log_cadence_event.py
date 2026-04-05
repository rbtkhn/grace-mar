#!/usr/bin/env python3
"""
Append a cadence event (coffee / dream / bridge / harvest / coffee_pick / thanks) to work-cadence-events.md.

One line per run. Not Record truth; not self-memory; not a replacement for
last-dream.json or session-transcript.md. See docs/skill-work/work-cadence/.

Usage:
  python3 scripts/log_cadence_event.py --kind dream -u grace-mar --ok --mode default \
      --kv integrity=pass governance=pass mem_changed=true
  python3 scripts/log_cadence_event.py --kind coffee -u grace-mar --ok --mode work-start \
      --kv gate_pending=0
  python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok \
      --kv picked=E steward=gate
  python3 scripts/log_cadence_event.py --kind bridge -u grace-mar --ok \
      --kv refs=aacec9e,4eaf1f4
  python3 scripts/log_cadence_event.py --kind harvest -u grace-mar --ok \
      --mode default --kv packet=chat
  python3 scripts/log_cadence_event.py --kind thanks -u grace-mar --ok \
      --kv park=Rome-pass-draft

**Agent surface (audit parity with bridge/harvest packets):** every line includes
``cursor_model=…``. Resolution order: ``--cursor-model`` CLI / ``cursor_model=``
``--kv`` / ``CURSOR_MODEL`` env / ``unknown``. Model names with spaces are
written with spaces replaced by underscores so the line stays token-safe.
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
KINDS = ("coffee", "dream", "bridge", "coffee_pick", "harvest", "thanks")

HEADER = (
    "# Cadence events\n"
    "\n"
    "> Append-only audit of **coffee**, **coffee_pick**, **dream**, **bridge**, **harvest**, and **thanks** runs.\n"
    "> **Not** Record truth. **Not** self-memory. **Not** a replacement for "
    "`last-dream.json` or `session-transcript.md`.\n"
    ">\n"
    "> **Format:** `- **YYYY-MM-DD HH:MM UTC** — kind (user) ok=… [mode=…] cursor_model=… …`\n"
    ">\n"
    "> See [work-cadence README](README.md) and "
    "[work-modules-history-principle](../work-modules-history-principle.md).\n"
    "\n"
    f"{ANCHOR}\n"
)

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def resolve_cursor_model(
    explicit: str | None = None,
    kv: dict[str, str] | None = None,
) -> str:
    """Label for the Cursor chat model (bridge **Agent surface** parity).

    Used in cadence lines and ``last-dream.json`` ``agent_surface.cursor_model``.
    Prefer the model name shown in the Cursor UI; not Record truth.
    """
    if explicit is not None and str(explicit).strip():
        return str(explicit).strip()[:200]
    if kv:
        v = kv.get("cursor_model")
        if v is not None and str(v).strip():
            return str(v).strip()[:200]
    env = os.environ.get("CURSOR_MODEL", "").strip()
    return env[:200] if env else "unknown"


def _format_cursor_model_token(cm: str) -> str:
    """Space-safe for space-delimited key=value cadence lines."""
    return str(cm).replace("\n", " ").strip().replace(" ", "_")[:200]


def append_cadence_event(
    kind: str,
    user_id: str,
    *,
    ok: bool = True,
    mode: str | None = None,
    cursor_model: str | None = None,
    kv: dict[str, str] | None = None,
    events_path: Path = EVENTS_PATH,
) -> Path:
    """Append one cadence event line. Returns the path written to."""
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")

    base = dict(kv or {})
    cm = resolve_cursor_model(explicit=cursor_model, kv=base)
    merged: dict[str, str] = {"cursor_model": cm}
    for k, v in base.items():
        if k == "cursor_model":
            continue
        merged[k] = v

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [f"- **{ts}** — {kind} ({user_id}) ok={'true' if ok else 'false'}"]
    if mode:
        parts.append(f"mode={mode}")
    for k, v in merged.items():
        if k == "cursor_model":
            val = _format_cursor_model_token(v)
        else:
            val = str(v).replace("\n", " ")[:200]
        parts.append(f"{k}={val}")
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
    ap.add_argument(
        "--cursor-model",
        default=None,
        help="Cursor UI model label (overrides CURSOR_MODEL env and cursor_model= in --kv)",
    )
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
        cursor_model=(args.cursor_model.strip() if args.cursor_model else None),
        kv=kv_dict,
    )
    print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
