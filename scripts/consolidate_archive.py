#!/usr/bin/env python3
"""
One-off: Merge SELF-ARCHIVE.md and TELEGRAM-ARCHIVE.md (if present) into a single SELF-ARCHIVE.md
with human-readable channel labels (Telegram, Test, WeChat).
"""
import re
from pathlib import Path

USER_DIR = Path(__file__).resolve().parent.parent / "users" / "grace-mar"
ARCHIVE = USER_DIR / "SELF-ARCHIVE.md"
TELEGRAM_ARCHIVE = USER_DIR / "TELEGRAM-ARCHIVE.md"


def normalize_channel(raw: str) -> str:
    raw = (raw or "").strip().lower()
    if raw.startswith("telegram:") or raw.startswith("chat "):
        return "Telegram"
    if raw.startswith("test:"):
        return "Test"
    if raw.startswith("wechat:"):
        return "WeChat"
    if raw.startswith("miniapp:") or raw.startswith("miniapp_"):
        return "Mini App"
    return raw or "Unknown"


def parse_archive(path: Path) -> list[tuple[str, str, str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if "---" in text:
        text = text.split("---", 1)[1]
    entries = []
    blocks = re.split(r"\n\n(?=\*\*\[)", text.strip())
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        first_line, _, body = block.partition("\n")
        m = re.match(r"^\*\*\[([^\]]+)\]\*\* `([^`]+)` \(([^)]+)\)", first_line)
        if not m:
            continue
        ts, speaker, channel = m.groups()
        body = "\n".join(
            (line[1:].lstrip() if line.startswith("> ") else line[1:] if line.startswith(">") else line)
            for line in body.splitlines()
        ).strip()
        channel = normalize_channel(channel)
        entries.append((ts, speaker, channel, body))
    return entries


def format_entry(ts: str, speaker: str, channel: str, body: str) -> str:
    lines = [f"**[{ts}]** `{speaker}` ({channel})\n"]
    for line in (body or "").strip().splitlines():
        lines.append(f"> {line}\n")
    lines.append("\n")
    return "".join(lines)


def main() -> str:
    a_entries = parse_archive(ARCHIVE)
    t_entries = parse_archive(TELEGRAM_ARCHIVE)
    combined = [(i, *e) for i, e in enumerate(a_entries + t_entries)]
    combined.sort(key=lambda x: (x[1], x[0]))  # ts, then original index
    seen: set[tuple[str, str, str]] = set()
    merged: list[tuple[str, str, str, str]] = []
    for _idx, ts, speaker, channel, body in combined:
        key = (ts, speaker, body[:200])
        if key in seen:
            continue
        seen.add(key)
        merged.append((ts, speaker, channel, body))
    header = """# SELF-ARCHIVE

> Append-only log of approved activity for the self (voice and non-voice) across channels (Telegram, WeChat, Mini App today; eventually email, X, and other platform channels). Machine-written — do not edit manually.

---

"""
    return header + "".join(format_entry(ts, speaker, channel, body) for ts, speaker, channel, body in merged)


if __name__ == "__main__":
    out = main()
    USER_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(out, encoding="utf-8")
    print(f"Wrote {ARCHIVE}", file=__import__("sys").stderr)
