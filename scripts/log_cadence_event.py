#!/usr/bin/env python3
"""
Append a cadence event (coffee / dream / bridge / harvest / thanks) to work-cadence-events.md.

One line per run. Not Record truth; not self-memory; not a replacement for
night-handoff.json or session-transcript.md. See docs/skill-work/work-cadence/.
Skills summarize recent lines for the companion as **Recent rhythm** in plain language (no
clock times in that prose); the lines below remain machine-audit format.

Usage:
  python3 scripts/log_cadence_event.py --kind dream -u demo --ok --mode standard \
      --kv integrity=pass governance=pass
  python3 scripts/log_cadence_event.py --kind coffee -u demo --ok --mode standard
  python3 scripts/log_cadence_event.py --kind bridge -u demo --ok \
      --kv refs=abc1234
  python3 scripts/log_cadence_event.py --kind harvest -u demo --ok \
      --mode default --kv packet=chat

**Agent surface (audit parity with bridge/harvest packets):** every line includes
``cursor_model=…`` and ``model_tier=…`` (frontier / fast / unknown).
Resolution for cursor_model: ``--cursor-model`` CLI / ``cursor_model=``
``--kv`` / ``CURSOR_MODEL`` env / ``unknown``. Model names with spaces are
written with spaces replaced by underscores so the line stays token-safe.
Resolution for model_tier: ``--model-tier`` CLI / ``model_tier=`` ``--kv`` /
auto-inferred from cursor_model string / ``unknown``.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"
ANCHOR = "_(Append below this line.)_"
KINDS = ("coffee", "dream", "bridge", "harvest", "thanks")

HEADER = (
    "# Cadence events\n"
    "\n"
    "> Append-only audit of **coffee**, **dream**, **bridge**, **thanks**, and optional **harvest** runs.\n"
    "> **Not** Record truth. **Not** self-memory. **Not** a replacement for\n"
    "> handoff artifacts or `session-transcript.md`.\n"
    ">\n"
    "> **Format:** `- **YYYY-MM-DD HH:MM UTC** — kind (user) key=value …` (machine-audit line).\n"
    "> **Companion-facing:** Skills read this file and speak **Recent rhythm** in chat — plain\n"
    "> language, concrete specifics, no clock times in that prose. See [work-cadence README](README.md).\n"
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
    """Label for the Cursor chat model (bridge **Agent surface** parity)."""
    if explicit is not None and str(explicit).strip():
        return str(explicit).strip()[:200]
    if kv:
        v = kv.get("cursor_model")
        if v is not None and str(v).strip():
            return str(v).strip()[:200]
    env = os.environ.get("CURSOR_MODEL", "").strip()
    return env[:200] if env else "unknown"


_EMPTY_PARK = frozenset({"", "none", "—", "-"})


def _auto_park(repo: Path | None = None) -> str:
    """Fallback park text from the last git commit subject when the caller omits it.

    Returns ``auto:<slug>`` or ``auto:no-recent-commit`` on failure.
    """
    cwd = str(repo) if repo else str(REPO_ROOT)
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1", "--format=%s"],
            capture_output=True, text=True, timeout=5, cwd=cwd,
        )
        subject = (result.stdout or "").strip()[:60]
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        subject = ""
    if not subject:
        return "auto:no-recent-commit"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", subject).strip("-").lower()
    return f"auto:{slug}" if slug else "auto:no-recent-commit"


def _format_cursor_model_token(cm: str) -> str:
    """Space-safe for space-delimited key=value cadence lines."""
    return str(cm).replace("\n", " ").strip().replace(" ", "_")[:200]


_FRONTIER_PATTERNS = ("opus", "sonnet-4", "o3", "o4", "pro", "deep-research")
_FAST_PATTERNS = ("haiku", "flash", "mini", "fast", "gpt-4o-mini", "lite")


def infer_model_tier(cursor_model: str) -> str:
    """Derive a capability tier from the cursor_model string.

    Returns 'frontier', 'fast', or 'unknown'. The operator can override
    via --model-tier or model_tier= in --kv.
    """
    cm = cursor_model.lower().replace("_", "-")
    if cm in ("", "unknown"):
        return "unknown"
    for pat in _FAST_PATTERNS:
        if pat in cm:
            return "fast"
    for pat in _FRONTIER_PATTERNS:
        if pat in cm:
            return "frontier"
    return "unknown"


def resolve_model_tier(
    explicit: str | None = None,
    kv: dict[str, str] | None = None,
    cursor_model: str = "unknown",
) -> str:
    """Model tier resolution: explicit > kv > inferred from cursor_model."""
    if explicit is not None and str(explicit).strip():
        return str(explicit).strip()
    if kv:
        v = kv.get("model_tier")
        if v is not None and str(v).strip():
            return str(v).strip()
    return infer_model_tier(cursor_model)


# Match first segment of a cadence line (aligned with audit_cadence_rhythm.parse_events).
_LAST_EVENT_LINE_RE = re.compile(
    r"^- \*\*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\*\* — (\w+) \(([^)]+)\)"
)


def _last_event_ts_kind_user(events_path: Path) -> tuple[datetime, str, str] | None:
    """Parse the most recent cadence event line from the file, if any."""
    if not events_path.is_file():
        return None
    for line in reversed(events_path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        m = _LAST_EVENT_LINE_RE.match(line)
        if not m:
            continue
        date_str, time_str = m.group(1), m.group(2)
        kind, user = m.group(3), m.group(4).strip()
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            return None
        return dt, kind, user
    return None


def append_cadence_event(
    kind: str,
    user_id: str,
    *,
    ok: bool = True,
    mode: str | None = None,
    cursor_model: str | None = None,
    model_tier: str | None = None,
    kv: dict[str, str] | None = None,
    events_path: Path = EVENTS_PATH,
    no_auto_park: bool = False,
    dedupe_seconds: int | None = 60,
    now: datetime | None = None,
) -> Path:
    """Append one cadence event line. Returns the path written to.

    If dedupe_seconds is a positive int and the last line in the file is the same
    kind and user within that many seconds of ``now``, the append is skipped (no
    write). Pass dedupe_seconds=None or 0 to disable. ``now`` is for tests; default
    is current UTC time.
    """
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")

    uid = user_id.strip()
    now_dt = now if now is not None else datetime.now(timezone.utc)

    base = dict(kv or {})

    if kind == "thanks" and not no_auto_park:
        park_val = base.get("park", "").strip()
        if park_val.lower() in _EMPTY_PARK:
            base["park"] = _auto_park(events_path.parent)
    cm = resolve_cursor_model(explicit=cursor_model, kv=base)
    mt = resolve_model_tier(explicit=model_tier, kv=base, cursor_model=cm)
    merged: dict[str, str] = {"cursor_model": cm, "model_tier": mt}
    for k, v in base.items():
        if k in ("cursor_model", "model_tier"):
            continue
        merged[k] = v

    if dedupe_seconds is not None and dedupe_seconds > 0:
        prev = _last_event_ts_kind_user(events_path)
        if prev is not None:
            last_dt, last_kind, last_user = prev
            if last_kind == kind and last_user == uid:
                delta = (now_dt - last_dt).total_seconds()
                if 0 <= delta < dedupe_seconds:
                    print(
                        f"cadence dedupe: skipped duplicate {kind} ({uid}) within {dedupe_seconds}s",
                        file=sys.stderr,
                    )
                    return events_path

    ts = now_dt.strftime("%Y-%m-%d %H:%M UTC")
    parts = [f"- **{ts}** — {kind} ({uid}) ok={'true' if ok else 'false'}"]
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
    ap.add_argument("-u", "--user", default=os.getenv("COMPANION_USER_ID", "demo"))
    ap.add_argument("--ok", action="store_true", default=False, help="Run succeeded")
    ap.add_argument("--no-ok", dest="ok", action="store_false", help="Run failed")
    ap.add_argument("--mode", default=None, help="Run mode (e.g. standard, strict, default)")
    ap.add_argument(
        "--cursor-model",
        default=None,
        help="Cursor UI model label (overrides CURSOR_MODEL env and cursor_model= in --kv)",
    )
    ap.add_argument(
        "--model-tier",
        default=None,
        choices=["frontier", "fast", "unknown"],
        help="Capability tier (overrides auto-inference from cursor_model; default: inferred)",
    )
    ap.add_argument("--kv", nargs="*", default=[], metavar="KEY=VALUE", help="Extra key=value pairs")
    ap.add_argument(
        "--no-auto-park",
        action="store_true",
        default=False,
        help="Suppress auto-park fallback for thanks events (keep park=none as-is)",
    )
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
        model_tier=args.model_tier,
        kv=kv_dict,
        no_auto_park=args.no_auto_park,
    )
    print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
