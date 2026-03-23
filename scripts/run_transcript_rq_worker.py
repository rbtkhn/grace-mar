#!/usr/bin/env python3
"""RQ worker for transcript_fetch queue. REDIS_URL defaults to redis://localhost:6379/0."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


def _register_jobs_module() -> None:
    """Ensure RQ can unpickle job functions."""
    import youtube_transcripts.jobs  # noqa: F401


def main() -> int:
    _register_jobs_module()
    try:
        import redis
        from rq.worker import Worker
    except ImportError:
        print("Install: pip install -e '.[transcript-pipeline]'", file=sys.stderr)
        return 1

    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    conn = redis.from_url(url)
    Worker(["transcript_fetch"], connection=conn).work(with_scheduler=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
