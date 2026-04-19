"""
Optional LLM summary for runtime worker — not Record, not continuity.

Prefer OpenAI Chat Completions when OPENAI_API_KEY is set. A future revision may
swap internals for the OpenAI Agents SDK without changing the worker CLI.

Does not import bot/ or write canonical surfaces.
"""

from __future__ import annotations

import os
from typing import Any

# Max chars sent to the model for summarization (bounded execution).
DEFAULT_MAX_PROMPT_CHARS = 12000


def summarize_inspection(
    *,
    rel_paths: list[str],
    bundle_excerpt: str,
    dry_run: bool,
) -> tuple[str, list[str]]:
    """
    Return (summary_markdown_section, tools_used_labels).

    When dry_run or no API key: returns placeholder text and tools_used ['dry_run'] or ['no_api_key'].
    """
    tools: list[str] = []
    if dry_run:
        return (
            "_Summary skipped (`--dry-run`): file list above is the full mechanical output._\n",
            ["dry_run"],
        )

    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not key:
        return (
            "_No `OPENAI_API_KEY` in environment: add a key for an optional LLM summary section._\n",
            ["no_api_key"],
        )

    excerpt = bundle_excerpt[:DEFAULT_MAX_PROMPT_CHARS]
    if len(bundle_excerpt) > DEFAULT_MAX_PROMPT_CHARS:
        excerpt += "\n\n… (truncated for model context)"

    try:
        from openai import OpenAI
    except ImportError:
        return (
            "_`openai` package not installed: pip install openai (see bot/requirements or miniapp stack)._\n",
            ["openai_missing"],
        )

    client = OpenAI(api_key=key)
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    sys_msg = (
        "You are a bounded work-strategy assistant. Summarize the file list and excerpts "
        "for an operator: what to read next, notable clusters, no claims of Record truth. "
        "Keep under 400 words. Plain markdown."
    )
    user_msg = f"Relative paths ({len(rel_paths)} files):\n" + "\n".join(rel_paths[:200])
    if len(rel_paths) > 200:
        user_msg += f"\n… and {len(rel_paths) - 200} more paths"
    user_msg += "\n\n---\n\nExcerpts / snippets:\n" + excerpt

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
    )
    text = (resp.choices[0].message.content or "").strip()
    tools.append(f"openai.chat.completions:{model}")
    return text + "\n", tools


def agents_sdk_available() -> dict[str, Any]:
    """Diagnostic for docs / --version."""
    try:
        import openai  # noqa: F401

        return {"openai": True, "openai_agents_sdk": False}
    except ImportError:
        return {"openai": False, "openai_agents_sdk": False}
