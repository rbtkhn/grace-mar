#!/usr/bin/env python3
"""
A/B voice fidelity test: run N prompts through get_response, optionally judge with LLM, store in users/<id>/metrics/.

Usage:
    OPENAI_API_KEY=... python scripts/ab_test_voice.py -u grace-mar
    python scripts/ab_test_voice.py -u grace-mar -n 5 --judge
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Pilot prompts that should elicit in-character replies
DEFAULT_PROMPTS = [
    "What's your favorite planet?",
    "Why do you like stories?",
    "What do you like to do for fun?",
    "What did you learn at school recently?",
    "Do you have a favorite animal?",
    "What's your favorite food?",
    "Tell me about something you drew.",
    "What do you know about space?",
    "Who is your favorite character from a story?",
    "What makes you happy?",
]


def get_response(channel_key: str, message: str) -> str:
    from bot.core import get_response as _get_response
    return _get_response(channel_key, message)


def judge_reply(prompt: str, reply: str) -> dict:
    """Use LLM to score voice fidelity (1-5) and optional short reason. Returns {score, reason}."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": "You are a rater. Reply with exactly two lines: first line 'SCORE: N' (N 1-5, 5=perfectly in-character for a 6-year-old). Second line 'REASON: one short sentence'."},
                {"role": "user", "content": f"Prompt: {prompt}\n\nReply: {reply}\n\nRate in-character fidelity."},
            ],
            max_tokens=80,
        )
        text = (result.choices[0].message.content or "").strip()
        score = 3
        reason = text
        for line in text.splitlines():
            if "SCORE:" in line.upper():
                try:
                    score = int(line.split(":")[-1].strip().split()[0])
                    score = max(1, min(5, score))
                except (ValueError, IndexError):
                    pass
            if "REASON:" in line.upper():
                reason = line.split(":", 1)[-1].strip()
        return {"score": score, "reason": reason}
    except Exception as e:
        return {"score": None, "reason": str(e)}


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="A/B voice test: run prompts, optional LLM judge, save to metrics/")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("-n", "--num", type=int, default=10, help="Number of prompts (default 10)")
    ap.add_argument("--judge", action="store_true", help="Run LLM-as-judge on each reply")
    ap.add_argument("-o", "--output", default=None, help="Output JSON path (default users/<id>/metrics/ab_voice_<date>.json)")
    args = ap.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY required", file=sys.stderr)
        return 1
    prompts = DEFAULT_PROMPTS[: args.num]
    metrics_dir = REPO_ROOT / "users" / args.user / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output) if args.output else metrics_dir / f"ab_voice_{datetime.now().strftime('%Y-%m-%d_%H%M')}.json"
    results = []
    channel_prefix = "test:ab_voice"
    for i, prompt in enumerate(prompts):
        key = f"{channel_prefix}:{i}"
        try:
            reply = get_response(key, prompt)
        except Exception as e:
            results.append({"prompt": prompt, "reply": None, "error": str(e), "judge": None})
            continue
        judge_out = None
        if args.judge:
            judge_out = judge_reply(prompt, reply)
        results.append({"prompt": prompt, "reply": reply, "error": None, "judge": judge_out})
    payload = {
        "user_id": args.user,
        "generated_at": datetime.now().isoformat(),
        "llm_provider": os.getenv("LLM_PROVIDER", "openai"),
        "n_prompts": len(prompts),
        "results": results,
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
