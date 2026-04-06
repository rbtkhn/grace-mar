#!/usr/bin/env python3
"""Mechanical blind prefix for skill-jiang forward-chain runs.

Only reads episodes 1..K (inclusive). Never opens K+1 until ``reveal`` — avoids
accidental spoilers from globbing the whole series or opening ``sources.yaml``.

Examples::

    # Predict gt-03: emit prefix gt-01..gt-02 only (writes bundle file)
    python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \\
        --series game-theory --prefix-end 2 -o /tmp/gt-prefix-2.md

    # Closed loop (K>=2): require prior round advanced + non-empty series model
    python3 scripts/work_jiang/forward_chain_blind_bundle.py advance \\
        --completed-round 1
    python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \\
        --closed-loop --prefix-end 2 -o scratch/gt-prefix-2.md

    # After prediction packet is saved, reveal gt-03 for scoring (H1 + At a glance)
    python3 scripts/work_jiang/forward_chain_blind_bundle.py reveal \\
        --series game-theory --episode 3

    # Token-saving: stop each lecture before ## Full transcript
    python3 scripts/work_jiang/forward_chain_blind_bundle.py bundle \\
        --series game-theory --prefix-end 5 --trim-at-full-transcript
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_LECTURES = _ROOT / "research" / "external" / "work-jiang" / "lectures"
_DEFAULT_SCRATCH = (
    _ROOT
    / "research"
    / "external"
    / "work-jiang"
    / "prediction-tracking"
    / "scratch"
)
_DEFAULT_CLOSED_LOOP_STATE = _DEFAULT_SCRATCH / "gt-closed-loop-state.yaml"
_DEFAULT_SERIES_MODEL = _DEFAULT_SCRATCH / "gt-series-model.md"

_TRIM_MARKER = "## Full transcript"

_STATE_KEY = "last_completed_blind_round"
_STATE_HEADER = (
    "# skill-jiang closed-loop state (local; gitignored with scratch/)\n"
    "# After scoring the round with prefix-end N, run: advance --completed-round N\n"
)


def read_closed_loop_state(path: Path) -> int | None:
    """Return last completed prefix-end round, or None if missing/invalid."""
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("---"):
            continue
        m = re.match(rf"^{re.escape(_STATE_KEY)}\s*:\s*(\d+)\s*$", line)
        if m:
            return int(m.group(1))
    return None


def write_closed_loop_state(path: Path, completed_round: int) -> None:
    if completed_round < 1:
        sys.exit(
            "error: --completed-round must be >= 1 (prefix-end of the round you "
            "finished). For a fresh calibration start, use: advance --reset"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    body = f"{_STATE_HEADER}{_STATE_KEY}: {completed_round}\n"
    path.write_text(body, encoding="utf-8")
    print(path, file=sys.stderr)


def enforce_closed_loop_bundle(
    *,
    prefix_end: int,
    state_path: Path,
    series_model_path: Path,
    force: bool,
) -> None:
    if prefix_end < 2:
        return
    if force:
        print(
            "warning: bypassing closed-loop checks (--force)",
            file=sys.stderr,
        )
        return
    prev = prefix_end - 1
    last = read_closed_loop_state(state_path)
    if last is None:
        sys.exit(
            f"error: closed-loop state missing or invalid: {state_path}\n"
            f"  fix: after finishing round with --prefix-end {prev}, run:\n"
            f"  python3 scripts/work_jiang/forward_chain_blind_bundle.py advance "
            f"--completed-round {prev}"
        )
    if last != prev:
        sys.exit(
            f"error: closed-loop expects {_STATE_KEY}=={prev} before "
            f"bundle --prefix-end {prefix_end}; got {last}\n"
            f"  fix: run advance --completed-round {prev} (after scoring that round)"
        )
    if not series_model_path.is_file():
        sys.exit(
            f"error: closed-loop requires non-empty series model file: {series_model_path}"
        )
    sm = series_model_path.read_text(encoding="utf-8", errors="replace").strip()
    if not sm:
        sys.exit(
            f"error: closed-loop requires non-empty series model file: {series_model_path}"
        )


def cmd_advance(args: argparse.Namespace) -> None:
    path = args.closed_loop_state
    if getattr(args, "reset", False):
        if path.is_file():
            path.unlink()
            print(f"removed {path}", file=sys.stderr)
        else:
            print(f"no state file at {path}", file=sys.stderr)
        return
    write_closed_loop_state(path, args.completed_round)


def resolve_lecture(lectures_dir: Path, series: str, episode: int) -> Path:
    pat = f"{series}-{episode:02d}-*.md"
    matches = sorted(lectures_dir.glob(pat))
    if len(matches) == 0:
        sys.exit(f"error: no file matching {lectures_dir}/{pat}")
    if len(matches) > 1:
        sys.exit(f"error: ambiguous {pat}: {matches}")
    return matches[0]


def _maybe_trim(text: str, trim_at_full_transcript: bool) -> str:
    if not trim_at_full_transcript:
        return text
    idx = text.find(_TRIM_MARKER)
    if idx == -1:
        return text
    return text[:idx].rstrip() + "\n\n<!-- trimmed at Full transcript -->\n"


def extract_reveal_snippet(text: str) -> str:
    """H1 through metadata + ``## At a glance`` block (stop at first ``---`` fence)."""
    marker = "## At a glance"
    if marker not in text:
        lines = text.splitlines()
        return "\n".join(lines[:80]).strip() + "\n"
    before, rest = text.split(marker, 1)
    lines_b = before.splitlines()
    start = next((i for i, ln in enumerate(lines_b) if ln.startswith("# ")), 0)
    header = "\n".join(lines_b[start:]).rstrip()
    glance_block = marker + rest.split("\n---", 1)[0]
    return f"{header}\n\n{glance_block.strip()}\n"


def cmd_bundle(args: argparse.Namespace) -> None:
    lectures_dir: Path = args.lectures_dir
    series: str = args.series
    k: int = args.prefix_end
    if k < 1:
        sys.exit("error: --prefix-end must be >= 1")

    if args.closed_loop:
        enforce_closed_loop_bundle(
            prefix_end=k,
            state_path=args.closed_loop_state,
            series_model_path=args.series_model,
            force=args.force,
        )

    chunks: list[str] = []
    for ep in range(1, k + 1):
        path = resolve_lecture(lectures_dir, series, ep)
        raw = path.read_text(encoding="utf-8", errors="replace")
        body = _maybe_trim(raw, args.trim_at_full_transcript)
        chunks.append(
            f"<!-- episode {ep:02d} | source: {path.relative_to(_ROOT)} -->\n{body}"
        )

    banner = (
        f"<!-- skill-jiang blind bundle | series={series} | prefix_end={k} | "
        f"predict_episode={k + 1} | DO NOT add later episodes without a new bundle -->\n\n"
    )
    output = banner + "\n\n---\n\n".join(chunks) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output, file=sys.stderr)
    else:
        sys.stdout.write(output)


def cmd_reveal(args: argparse.Namespace) -> None:
    lectures_dir: Path = args.lectures_dir
    series: str = args.series
    m: int = args.episode
    if m < 1:
        sys.exit("error: --episode must be >= 1")

    if args.require_prediction_path:
        p = args.require_prediction_path
        if not p.is_file() or p.stat().st_size == 0:
            sys.exit(
                f"error: --require-prediction-path must be a non-empty file: {p}"
            )

    path = resolve_lecture(lectures_dir, series, m)
    text = path.read_text(encoding="utf-8", errors="replace")
    snippet = extract_reveal_snippet(text)
    sys.stdout.write(
        f"<!-- reveal episode {m:02d} | {path.relative_to(_ROOT)} -->\n{snippet}"
    )


def cmd_paths(args: argparse.Namespace) -> None:
    """Print resolved paths for episodes 1..K only (audit)."""
    lectures_dir: Path = args.lectures_dir
    series: str = args.series
    k: int = args.prefix_end
    for ep in range(1, k + 1):
        p = resolve_lecture(lectures_dir, series, ep)
        print(p)


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--lectures-dir",
        type=Path,
        default=_DEFAULT_LECTURES,
        help=f"curated lectures dir (default: {_DEFAULT_LECTURES})",
    )
    p.add_argument(
        "--series",
        default="game-theory",
        help="filename prefix, e.g. game-theory (default)",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_bundle = sub.add_parser("bundle", help="emit concatenated prefix 1..K")
    _add_common(p_bundle)
    p_bundle.add_argument("--prefix-end", type=int, required=True, metavar="K")
    p_bundle.add_argument(
        "-o",
        "--output",
        type=Path,
        help="write bundle to file (recommended for audit trail)",
    )
    p_bundle.add_argument(
        "--trim-at-full-transcript",
        action="store_true",
        help="omit ## Full transcript and below per lecture (smaller bundle)",
    )
    p_bundle.add_argument(
        "--closed-loop",
        action="store_true",
        help="for prefix-end K>=2: require advance state + non-empty series model",
    )
    p_bundle.add_argument(
        "--force",
        action="store_true",
        help="with --closed-loop, skip state/model checks (maintenance only)",
    )
    p_bundle.add_argument(
        "--closed-loop-state",
        type=Path,
        default=_DEFAULT_CLOSED_LOOP_STATE,
        help=f"YAML one-liner {_STATE_KEY} (default: {_DEFAULT_CLOSED_LOOP_STATE})",
    )
    p_bundle.add_argument(
        "--series-model",
        type=Path,
        default=_DEFAULT_SERIES_MODEL,
        help=f"rolling bullets file, non-empty when --closed-loop (default: {_DEFAULT_SERIES_MODEL})",
    )
    p_bundle.set_defaults(func=cmd_bundle)

    p_adv = sub.add_parser(
        "advance",
        help="record completed blind round (prefix-end N) for closed-loop bundle",
    )
    g = p_adv.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--completed-round",
        type=int,
        metavar="N",
        help="prefix-end K of the round you just finished scoring",
    )
    g.add_argument(
        "--reset",
        action="store_true",
        help="remove closed-loop state file (fresh prefix-only calibration start)",
    )
    p_adv.add_argument(
        "--closed-loop-state",
        type=Path,
        default=_DEFAULT_CLOSED_LOOP_STATE,
        help=f"state file path (default: {_DEFAULT_CLOSED_LOOP_STATE})",
    )
    p_adv.set_defaults(func=cmd_advance)

    p_rev = sub.add_parser(
        "reveal", help="print H1 + At a glance for episode M (usually K+1)"
    )
    _add_common(p_rev)
    p_rev.add_argument("--episode", type=int, required=True, metavar="M")
    p_rev.add_argument(
        "--require-prediction-path",
        type=Path,
        metavar="FILE",
        help="refuse to reveal unless this file exists and is non-empty",
    )
    p_rev.set_defaults(func=cmd_reveal)

    p_paths = sub.add_parser("paths", help="list paths for episodes 1..K")
    _add_common(p_paths)
    p_paths.add_argument("--prefix-end", type=int, required=True, metavar="K")
    p_paths.set_defaults(func=cmd_paths)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
