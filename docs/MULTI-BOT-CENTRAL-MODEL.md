# Multiple Bots, One Central Model

**Purpose:** Support multiple Grace-Mar Telegram bots—one per person (Record)—all backed by the same codebase, shared LLM, and shared pipeline logic. Each bot is the Voice for one Record; "central" means one repo, one model (API), one set of rules.

**Status:** Design. Current codebase is already one-user-per-process; this doc describes how to scale that without changing architecture.

**Aligns with:** [INSTANCES-AND-RELEASE](INSTANCES-AND-RELEASE.md) §8 "Family mesh" (Mom, Dad, Child each have a Record and a Voice); [CONCEPTUAL-FRAMEWORK](CONCEPTUAL-FRAMEWORK.md) invariant 34 (canonical instance, user consent).

---

## 1. What “central model” means here

| Central | Meaning |
|--------|---------|
| **One codebase** | Same repo, same `bot/`, same prompts and pipeline. No fork of the app per person. |
| **One LLM API** | Shared OpenAI (or other) key and model. Each bot uses the same API; prompts differ by user (SELF, SKILLS, EVIDENCE). |
| **One pipeline** | Same analyst, lookup, rephrase, PENDING-REVIEW, merge flow. Per-user data lives under `users/<id>/`. |
| **Optional: one operator view** | Profile and operator tools can later support multiple users (e.g. grace-mar.com?user=abby vs ?user=dad). Today the profile is single-user (grace-mar). |

Each **bot** is still the Voice for **one** Record. There is no shared “brain” across people—only shared infrastructure and rules.

---

## 2. Current design (one bot per process)

The app already keys everything by **user ID**:

- `GRACE_MAR_USER_ID` (env, default `grace-mar`) → `users/<id>/` for SELF, SKILLS, EVIDENCE, PENDING-REVIEW, archive, etc.
- `TELEGRAM_BOT_TOKEN` → one Telegram bot per process.

So: **one process = one bot = one Record.** To run a second bot for a second person you run a second process with different env.

---

## 3. Option A — Multiple processes (recommended)

Run **N** instances of the same app, each with its own bot token and user ID.

**Steps:**

1. **Create N bots in BotFather** (e.g. @GraceMarAbby_bot, @GraceMarDad_bot). Get a token per bot.
2. **Create N user profiles** under `users/`: e.g. `users/abby/`, `users/dad/` with SELF.md, SKILLS.md, EVIDENCE.md, etc. (Copy from grace-mar or use templates.)
3. **Deploy N times**, each with its own env:
   - Instance 1: `TELEGRAM_BOT_TOKEN=<token_abby>`, `GRACE_MAR_USER_ID=abby`
   - Instance 2: `TELEGRAM_BOT_TOKEN=<token_dad>`, `GRACE_MAR_USER_ID=dad`
   - Same `OPENAI_API_KEY` (or per-instance if you want to meter separately).

**Where to run:**

- **Render / Railway / Fly:** One service per bot; each service has its own env and webhook URL. Set each bot’s webhook in BotFather to its service URL (e.g. `https://grace-mar-abby.onrender.com/telegram/webhook`).
- **Single machine:** Run N processes (e.g. N systemd units or Docker containers), each with its own env. Use a reverse proxy (nginx, Caddy) to route by hostname or path to the right process, and set each bot’s webhook to the corresponding URL.
- **Local dev:** Run `python -m bot.bot` (or miniapp_server) in two terminals with different `.env` files (or `GRACE_MAR_USER_ID=abby TELEGRAM_BOT_TOKEN=... python -m bot.bot`).

**Pros:** No code changes. Same codebase, same “central” logic; only config differs per bot.  
**Cons:** N deployments to operate; profile today is single-user (you’d open one profile per user or add multi-user later).

---

## 4. Option B — Single process, multiple webhook routes (future)

One server, multiple webhook paths, e.g.:

- `POST /telegram/webhook/abby` → bot token for Abby, user_id = abby  
- `POST /telegram/webhook/dad` → bot token for Dad, user_id = dad  

Each bot is registered in BotFather with its own webhook URL. The server would:

1. Route the request by path to the right (token, user_id).
2. Build or select a Telegram `Application` per bot (or reuse one and pass context).
3. Call the same handlers, but with **request-scoped** user_id so that `core` and `prompt` load `users/<user_id>/` for that request.

Today `bot/core.py` and `bot/prompt.py` use **module-level** `USER_ID` and `PROFILE_DIR`. To support Option B you’d refactor so that:

- Profile paths and prompt content are resolved from a **user_id** passed into the call chain (e.g. `get_response(..., user_id=...)`), not from a global.
- The webhook handler determines `user_id` from the URL (or a token→user_id map) and passes it through.

That’s a larger change; Option A is enough to get “multiple bots, central model” with zero code changes.

---

## 5. Governance

- **One canonical Record per person.** Each bot is the canonical Voice for that person’s Record (invariant 34). No “released” instance acting without the user’s gate.
- **Consent and sovereignty.** Each user (or their delegate) controls their bot’s deployment and their Record. Family mesh = multiple Records, each with its own gate.
- **No cross-Record merge.** Data from one person’s conversation does not merge into another’s Record unless you explicitly build a cross-query feature (e.g. “what does Dad’s Record say about the trip?”) with consent and clear boundaries.

---

## 6. Dashboard and operator experience

- **Today:** Profile and scripts are single-user (e.g. `generate_profile.py` reads `users/grace-mar/`). For multi-bot you can either:
  - Run one profile per user (e.g. pass user in env or query param and generate for that user), or
  - Extend the profile to list users and switch context (future).
- **Operator:** If one operator oversees multiple bots, they can set `GRACE_MAR_OPERATOR_CHAT_ID` per process so reminders go to the same Telegram chat, or use different operator chats per bot.

---

## 7. Summary

| Goal | Approach |
|------|----------|
| Multiple bots, one codebase / one “model” | Use **Option A**: N processes, each with its own `TELEGRAM_BOT_TOKEN` and `GRACE_MAR_USER_ID`. Same repo, same API key, same pipeline. |
| Single deployment for all bots | **Option B** later: refactor core to be user_id-scoped per request and add multiple webhook routes. |
| Family mesh (e.g. Mom, Dad, Child) | Option A today: three bots, three `users/<id>/` profiles, three deployments. |

**Cross-references:** [INSTANCES-AND-RELEASE](INSTANCES-AND-RELEASE.md) §8, [ARCHITECTURE](ARCHITECTURE.md), [CONCEPTUAL-FRAMEWORK](CONCEPTUAL-FRAMEWORK.md) invariant 34.
