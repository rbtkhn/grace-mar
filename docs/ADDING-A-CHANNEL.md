# Adding a Channel (Skill pattern)

This doc is a **skill**: instructions to add a new messaging or interface channel (e.g. Discord, Slack, SMS bridge) without growing a single config monster. Pattern: one new entrypoint that calls the shared core; env-based config; no "if channel X" branches in core.

**Governance:** [IMPLEMENTABLE-INSIGHTS](IMPLEMENTABLE-INSIGHTS.md) §4 — config via skills that modify code.

---

## Pattern (reference: Telegram and WeChat)

1. **Core is shared.** All channels use `bot/core.py`: `get_response`, `archive`, `reset_conversation`, `get_greeting`, `get_reset_message`, and any pipeline/operator helpers you need. Do not duplicate emulation or analyst logic.

2. **One entrypoint per channel.** e.g. `bot/bot.py` (Telegram), `bot/wechat_bot.py` (WeChat). Each entrypoint:
   - Loads env for that channel (e.g. `TELEGRAM_BOT_TOKEN`, `WECHAT_TOKEN`).
   - Maps incoming messages to a stable `channel_key` (e.g. `telegram:{chat_id}`, `wechat:{openid}`) so core can track conversation and archive per user.
   - Calls `get_response(user_id, channel_key, message_text, ...)` and sends the result back.
   - Optionally calls `archive(...)` for logging.

3. **No channel logic in core.** `core.py` does not branch on "if Telegram" or "if WeChat". It takes `user_id`, `channel_key`, and message content; it returns response and optional pipeline side effects. Channel-specific transport (HTTP, WebSocket, long polling) stays in the entrypoint.

4. **Config = env + one place.** Each channel has its own env vars (see `.env.example`). No single mega-config file that lists every channel with if-then-else.

5. **Optional: router.** If you run multiple channels in one process, a thin router can dispatch by URL or protocol to the right entrypoint or handler. Still no channel logic inside core.

---

## Checklist for a new channel (e.g. "Discord")

1. Add `bot/discord_bot.py` (or similar):
   - Dependencies: Discord SDK + `from core import get_response, archive, ...`.
   - Env: `DISCORD_TOKEN`, `GRACE_MAR_USER_ID` (or derive from context).
   - Map Discord user/server to `channel_key`, e.g. `discord:{guild_id}:{user_id}`.
   - On message → `get_response(user_id, channel_key, content)` → send reply; optionally `archive(...)`.
2. Add to `bot/requirements.txt` any channel-specific deps.
3. Document in a short `bot/DISCORD-SETUP.md`: env vars, how to run, optional webhook vs polling.
4. Update `.env.example` with the new keys (no secrets, just names).
5. Do **not** add `if channel == "discord"` (or similar) inside `core.py`; keep core channel-agnostic.

---

## Why this is a "skill"

Adding a channel is a **bounded code change** guided by a doc (this one + channel-specific setup). An agent or human can follow the same pattern for the next channel without touching core logic or a central config schema. That keeps the repo maximally forkable and avoids config/if-then-else sprawl. See [PORTABILITY](PORTABILITY.md) and [IMPLEMENTABLE-INSIGHTS](IMPLEMENTABLE-INSIGHTS.md).
