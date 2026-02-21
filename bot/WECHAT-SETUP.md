# WeChat Integration Setup

Grace-Mar can run as a WeChat Official Account (公众号) bot alongside Telegram. Both use the same emulation core and share the same profile, archive, and pipeline.

## Prerequisites

1. A WeChat Official Account (subscribe account 订阅号 or service account 服务号)
2. A server with a public HTTPS URL (WeChat requires HTTPS for callbacks)
3. Python 3.10+

## Step 1: Register a WeChat Official Account

1. Go to [https://mp.weixin.qq.com](https://mp.weixin.qq.com) and register
2. Complete verification (required for callback configuration)
3. In **Development** → **Basic Configuration**:
   - Note your **AppID** and **AppSecret**
   - Set **Server URL** to `https://your-domain/wechat` (must be HTTPS)
   - Set **Token** to a random string you choose (e.g. `grace-mar-callback-2024`)
   - For **Encoding Mode**, choose **Plain** (明文) for simplicity, or **Compatible** if you need encryption
4. Click **Submit** to verify — WeChat will send a GET request; the bot must return the `echostr` parameter

## Step 2: Configure Environment

Add to your `.env`:

```bash
WECHAT_TOKEN=your-callback-token    # Must match the Token in WeChat console
WECHAT_APP_ID=wx1234567890abcdef    # From Basic Configuration
WECHAT_APP_SECRET=your-app-secret   # From Basic Configuration

# Optional: bind host and port (default: 0.0.0.0:5000)
WECHAT_HOST=0.0.0.0
WECHAT_PORT=5000
```

## Step 3: Run the WeChat Server

```bash
pip install -r requirements.txt
python wechat_bot.py
```

The server listens on port 5000 by default. You must expose it via HTTPS. Use a reverse proxy (nginx, Caddy) with TLS, or a tunnel like ngrok for local testing.

## Step 4: Point WeChat to Your Server

Set **Server URL** in the WeChat console to your public URL, e.g.:

- Production: `https://grace-mar.example.com/wechat`
- Local (ngrok): `https://abc123.ngrok.io/wechat`

WeChat will verify the URL by sending a GET request. The bot responds with `echostr` to confirm.

## Commands (WeChat has no slash commands)

Users can type these to emulate `/start` and `/reset`:

- **Start**: `start`, `开始`, `hello`, `hi`, `你好`
- **Reset**: `reset`, `重置`, `forget`

## Architecture

- **Same core**: Both Telegram and WeChat use `bot/core.py` — identical emulation, lookup, and analyst behavior
- **Separate conversations**: Telegram and WeChat users have isolated conversation history (scoped by `telegram:{id}` vs `wechat:{openid}`)
- **Shared archive**: All exchanges are logged to `TELEGRAM-ARCHIVE.md` with channel tags
- **Shared pipeline**: Analyst-staged candidates from either channel go to the same `PENDING-REVIEW.md`

## Limitations

- **5-second reply timeout**: WeChat requires a response within 5 seconds. Long LLM calls may cause WeChat to retry. Consider a faster model or async push (customer service API) for production.
- **Plain mode recommended**: Encrypted mode adds complexity; use plain mode unless you need it.
- **HTTPS required**: WeChat will not callback to HTTP URLs.
