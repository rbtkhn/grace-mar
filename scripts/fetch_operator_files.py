#!/usr/bin/env python3
"""
Fetch session-transcript.md and pending-review.md from the bot running on Render (or any host).

Use this from Cursor so your local repo has the latest Telegram chat and pipeline state.
Requires OPERATOR_FETCH_SECRET to be set on the server (Render env) and passed here.

Usage:
  export OPERATOR_FETCH_SECRET=your-secret
  export GRACE_MAR_RENDER_URL=https://your-app.onrender.com
  python scripts/fetch_operator_files.py

  # Or with args:
  python scripts/fetch_operator_files.py --url https://grace-mar-miniapp.onrender.com --secret YOUR_SECRET --user grace-mar
"""

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch SESSION-TRANSCRIPT and PENDING-REVIEW from Render (or bot host).")
    ap.add_argument("--url", "-u", default=os.getenv("GRACE_MAR_RENDER_URL", "").strip(), help="Base URL of the bot (e.g. https://grace-mar-miniapp.onrender.com)")
    ap.add_argument("--secret", "-s", default=os.getenv("OPERATOR_FETCH_SECRET", "").strip(), help="OPERATOR_FETCH_SECRET (or set env)")
    ap.add_argument("--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar", help="User id (for local output path)")
    args = ap.parse_args()

    if not args.url:
        print("Error: Set GRACE_MAR_RENDER_URL or pass --url", file=sys.stderr)
        sys.exit(1)
    if not args.secret:
        print("Error: Set OPERATOR_FETCH_SECRET or pass --secret", file=sys.stderr)
        sys.exit(1)

    base = args.url.rstrip("/")
    headers = {"Authorization": f"Bearer {args.secret}"}
    out_dir = REPO_ROOT / "users" / args.user
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from urllib.request import Request, urlopen
    except ImportError:
        import urllib.request
        Request = urllib.request.Request
        urlopen = urllib.request.urlopen

    for name, path in (
        ("SESSION-TRANSCRIPT", f"{base}/operator/session-transcript"),
        ("PENDING-REVIEW", f"{base}/operator/pending-review"),
    ):
        out_file = out_dir / f"{name}.md"
        try:
            req = Request(path, headers=headers)
            with urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8")
            out_file.write_text(body, encoding="utf-8")
            print(f"Written {out_file} ({len(body)} chars)")
        except Exception as e:
            print(f"Failed {name}: {e}", file=sys.stderr)
            if hasattr(e, "code"):
                print(f"  HTTP {e.code}", file=sys.stderr)
            if hasattr(e, "read"):
                try:
                    print(f"  Body: {e.read().decode()[:500]}", file=sys.stderr)
                except Exception:
                    pass

    print("Done. Open users/{}/session-transcript.md and pending-review.md in Cursor.".format(args.user))


if __name__ == "__main__":
    main()
