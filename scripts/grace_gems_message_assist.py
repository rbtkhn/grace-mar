#!/usr/bin/env python3
"""
Grace Gems message assist — draft-only reply for Etsy customer messages (Wu insight: BPA).

Minimal v1: input = customer message (paste); prompt = Record excerpt (policies, agent-encoding)
+ message; output = draft reply. Human copies into Etsy and sends. No Etsy API, no auto-send.

Knowledge boundary: uses only documented Record content (agent-encoding, skill-work README).
See docs/skill-work/skill-work-grace-gems/agent-encoding.md for meta-rules.

Usage:
    python scripts/grace_gems_message_assist.py --message "Do you ship to Canada?"
    echo "Do you ship to Canada?" | python scripts/grace_gems_message_assist.py
    python scripts/grace_gems_message_assist.py -m "Is this stone natural or lab-grown?"
"""

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_WORK_DIR = REPO_ROOT / "docs" / "skill-work" / "skill-work-grace-gems"


def _load_context() -> str:
    """Load agent-encoding and Grace Gems policies for prompt context."""
    parts: list[str] = []

    # Grace Gems business context (from README)
    readme = SKILL_WORK_DIR / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        # Extract Purpose / policies
        if "Grace Gems" in content and "Policies:" in content:
            idx = content.find("Policies:")
            if idx >= 0:
                excerpt = content[idx : idx + 400]
                parts.append("## Grace Gems (from Record)\n" + excerpt)
                parts.append("")

    # Agent-encoding meta-rules, glossary, example drafts
    encoding = SKILL_WORK_DIR / "agent-encoding.md"
    if encoding.exists():
        content = encoding.read_text(encoding="utf-8")
        # Extract Meta-Rules (includes tone guidelines)
        meta_start = content.find("## 3. Meta-Rules for Drafts")
        if meta_start >= 0:
            meta_end = content.find("## 4. Handback Semantics")
            if meta_end < 0:
                meta_end = len(content)
            meta_section = content[meta_start:meta_end].strip()
            parts.append("## Agent encoding (meta-rules)\n" + meta_section)
            parts.append("")
        # Brief glossary excerpt
        gloss_start = content.find("### Cut forms")
        if gloss_start >= 0:
            gloss_end = content.find("## 3. Meta-Rules")
            if gloss_end < 0:
                gloss_end = len(content)
            gloss = content[gloss_start:gloss_end].strip()[:800]
            parts.append("## Glossary (excerpt)\n" + gloss)
            parts.append("")
        # Example drafts (exposure to quality)
        ex_start = content.find("## 5. Example Drafts")
        if ex_start >= 0:
            ex_end = content.find("## 6. Usage")
            if ex_end < 0:
                ex_end = len(content)
            ex_section = content[ex_start:ex_end].strip()[:1200]
            parts.append("## Example drafts (reference)\n" + ex_section)
            parts.append("")

    # Calibration notes (Lazar: "how can I prompt you better?" loop)
    calibration = SKILL_WORK_DIR / "message-assist-calibration.md"
    if calibration.exists():
        content = calibration.read_text(encoding="utf-8")
        cal_start = content.find("## Calibration Notes")
        if cal_start >= 0:
            cal_section = content[cal_start:].strip()
            # Include if there are actual calibration entries (bullet with date)
            if "- [" in cal_section and len(cal_section) > 120:
                parts.append("## Calibration (operator feedback)\n" + cal_section[:800])
                parts.append("")

    return "\n".join(parts) if parts else "Grace Gems: custom fine jewelry, natural untreated gemstones, solid 14k/18k gold, handmade in Denver. Policies: free worldwide shipping, 30-day returns (excl. custom), 1-year repair warranty, layaway."


def _draft_reply(message: str, context: str) -> str:
    """Call OpenAI to draft a reply."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "[Error: OPENAI_API_KEY not set. Set it in .env or environment.]"

    try:
        from openai import OpenAI
    except ImportError:
        return "[Error: openai package not installed. Run: pip install openai]"

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    system = """You are drafting a reply for Grace Gems (Etsy shop: GraceGemsUS) — custom fine jewelry with natural, untreated gemstones; solid 14k/18k gold; handmade in Denver.

Use ONLY the documented context below. Do not invent policies, provenance, or verification methods. Include at least one concrete fact per reply (provenance, treatment status, metal, or policy). Match the tone an informed customer expects — friendly, accurate, helpful.

Output ONLY the draft reply. No preamble, no "Here's a draft:", no explanation."""

    user = f"""Context:
{context}

---
Customer message:
{message}

---
Draft reply:"""

    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=500,
            temperature=0.6,
        )
        raw = (resp.choices[0].message.content or "").strip()
        # Trim any accidental preamble
        for prefix in ("Here's a draft:", "Draft reply:", "Draft:"):
            if raw.lower().startswith(prefix.lower()):
                raw = raw[len(prefix):].strip()
        return raw
    except Exception as e:
        return f"[Error calling API: {e}]"


def main() -> int:
    parser = argparse.ArgumentParser(description="Grace Gems message assist — draft-only reply")
    parser.add_argument("-m", "--message", help="Customer message text")
    args = parser.parse_args()

    if args.message:
        message = args.message.strip()
    else:
        message = sys.stdin.read().strip()

    if not message:
        print("Usage: --message \"text\" or pipe message to stdin", file=sys.stderr)
        return 1

    context = _load_context()
    draft = _draft_reply(message, context)
    print(draft)
    return 0


if __name__ == "__main__":
    sys.exit(main())
