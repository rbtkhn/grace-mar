#!/usr/bin/env python3
"""
Test the checkpoint function: pattern match, transcript formatting, and optional full flow.

Usage:
  python scripts/test_checkpoint.py              # unit-style tests (no API)
  python scripts/test_checkpoint.py --live       # one live get_response("checkpoint") if OPENAI_API_KEY set
  python scripts/test_checkpoint.py --live --user grace-mar
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Set user before importing core (core reads GRACE_MAR_USER_ID at import)
def _parse_args():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="Run one live get_response('checkpoint') with mock history")
    ap.add_argument("--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"), help="User id")
    return ap.parse_args()


def test_pattern():
    """Test CHECKPOINT_REQUEST_PATTERN matches 'checkpoint' and variants (pattern is applied to stripped message)."""
    from bot.core import CHECKPOINT_REQUEST_PATTERN
    assert CHECKPOINT_REQUEST_PATTERN.search("checkpoint"), "checkpoint"
    assert CHECKPOINT_REQUEST_PATTERN.search("checkpoint!"), "checkpoint!"
    assert CHECKPOINT_REQUEST_PATTERN.search("Checkpoint."), "Checkpoint."
    assert CHECKPOINT_REQUEST_PATTERN.search("  checkpoint  ".strip()), "stripped checkpoint"
    assert not CHECKPOINT_REQUEST_PATTERN.search("we did a checkpoint"), "sentence should not match"
    assert not CHECKPOINT_REQUEST_PATTERN.search("checkpoint something else"), "extra words should not match"
    print("  CHECKPOINT_REQUEST_PATTERN: ok")


def test_format_checkpoint_transcript_empty():
    """Empty history -> empty transcript."""
    from bot.core import _format_checkpoint_transcript
    out = _format_checkpoint_transcript([])
    assert out == "", out
    out = _format_checkpoint_transcript([{"role": "user", "content": ""}])
    assert out == "", out
    print("  _format_checkpoint_transcript([]): ok")


def test_format_checkpoint_transcript_short():
    """Short history -> USER/GRACE-MAR lines."""
    from bot.core import _format_checkpoint_transcript
    history = [
        {"role": "user", "content": "What do you know about space?"},
        {"role": "assistant", "content": "I know the planets! Jupiter has a Great Red Spot."},
    ]
    out = _format_checkpoint_transcript(history)
    assert "USER: What do you know" in out, out
    assert "GRACE-MAR: I know the planets" in out, out
    assert out.count("\n\n") >= 1
    print("  _format_checkpoint_transcript(short): ok")


def test_format_checkpoint_transcript_truncate_exchanges():
    """Over MAX_CHECKPOINT_EXCHANGES user messages -> keep last N."""
    from bot.core import _format_checkpoint_transcript, MAX_CHECKPOINT_EXCHANGES
    # Build history with more than 25 user turns
    history = []
    for i in range(MAX_CHECKPOINT_EXCHANGES + 5):
        history.append({"role": "user", "content": f"user message {i}"})
        history.append({"role": "assistant", "content": f"assistant reply {i}"})
    out = _format_checkpoint_transcript(history)
    # Should contain only the last MAX_CHECKPOINT_EXCHANGES exchanges (most recent)
    assert f"user message {MAX_CHECKPOINT_EXCHANGES + 4}" in out, out
    assert "user message 0" not in out, "oldest should be dropped"
    print("  _format_checkpoint_transcript(truncate exchanges): ok")


def test_format_checkpoint_transcript_truncate_chars():
    """Over MAX_CHECKPOINT_TRANSCRIPT_CHARS -> abridged prefix."""
    from bot.core import _format_checkpoint_transcript, MAX_CHECKPOINT_TRANSCRIPT_CHARS
    long_content = "x" * 300  # 300 chars per message
    history = [{"role": "user", "content": long_content}, {"role": "assistant", "content": long_content}] * 20
    out = _format_checkpoint_transcript(history)
    assert len(out) <= MAX_CHECKPOINT_TRANSCRIPT_CHARS + 100, "should be capped (with small slack)"
    assert "abridged" in out or len(out) <= MAX_CHECKPOINT_TRANSCRIPT_CHARS, out[:200]
    print("  _format_checkpoint_transcript(truncate chars): ok")


def run_live_checkpoint(user_id: str) -> None:
    """Run one live get_response with message 'checkpoint' and mock history."""
    os.environ["GRACE_MAR_USER_ID"] = user_id
    # Re-import so core picks up user
    import importlib
    import bot.core as core
    importlib.reload(core)
    channel_key = "test:checkpoint"
    # Seed conversation so transcript is non-empty
    core.conversations[channel_key] = [
        {"role": "user", "content": "What's your favorite planet?"},
        {"role": "assistant", "content": "Jupiter! It has a Great Red Spot — a giant storm."},
        {"role": "user", "content": "checkpoint"},
    ]
    # Remove the "checkpoint" we're about to send so history passed to _format_checkpoint_transcript is the prior exchange
    core.conversations[channel_key] = core.conversations[channel_key][:-1]
    reply = core.get_response(channel_key, "checkpoint")
    print("  get_response('checkpoint') reply:", reply[:120] + "..." if len(reply) > 120 else reply)
    # Check session transcript was written (optional)
    st = core.SESSION_TRANSCRIPT_PATH
    if st.exists():
        text = st.read_text()
        if "checkpoint" in text.lower() or "USER:" in text:
            print("  session-transcript contains checkpoint/user: ok")
    print("  live checkpoint: ok")


def main():
    args = _parse_args()
    os.environ["GRACE_MAR_USER_ID"] = args.user
    print("Testing checkpoint (user=%s)" % args.user)
    test_pattern()
    test_format_checkpoint_transcript_empty()
    test_format_checkpoint_transcript_short()
    test_format_checkpoint_transcript_truncate_exchanges()
    test_format_checkpoint_transcript_truncate_chars()
    if args.live:
        if not os.getenv("OPENAI_API_KEY"):
            print("  --live skipped: OPENAI_API_KEY not set")
        else:
            run_live_checkpoint(args.user)
    print("Done.")


if __name__ == "__main__":
    main()
