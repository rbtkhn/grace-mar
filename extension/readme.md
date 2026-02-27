# Grace-Mar Browser Extension

One-click capture from any URL to your Grace-Mar Record. Local only; stages to RECURSION-GATE (user approves via /review in Telegram).

## Setup

1. **Run the handback server** (local):
   ```bash
   cd grace-mar
   python scripts/handback_server.py
   ```
   Listens on `http://127.0.0.1:5050` by default.
   Unauthenticated requests are accepted only from local loopback.

2. **Load the extension** (Chrome/Edge):
   - Open `chrome://extensions`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `extension/` folder

3. **Use**:
   - **Toolbar** — Click the extension icon, then "Save to Record" to stage the current page
   - **Context menu** — Right-click on a page or link → "Save to Record"

## What it does

- Builds activity report: `we read "[page title]"` + URL (+ optional selected text/snippet)
- POSTs to configurable `/stage` endpoint (default `http://localhost:5050/stage`)
- Shows confirmation: "Saved! X items to review" (if staged) or "Added to log. X items to review"
- Pipeline: stage → RECURSION-GATE → user approves in Telegram via /review
- If server is unavailable, capture is queued locally and retried

## Requirements

- Python handback server running locally
- OPENAI_API_KEY set (analyst needs it)
- Pilot user configured (default: grace-mar)
- Optional for remote/non-loopback staging: set `HANDBACK_API_KEY` and pass `X-Api-Key`

## Settings

Open extension settings (popup "Settings" link or extension options page) to configure:

- Stage URL
- Optional API key (`X-Api-Key`)
- Optional `user_id` payload field
- Queue retry interval

## Popup actions

- **Save to Record**: stage current page with optional snippet
- **Retry Queue**: resend offline-queued captures
- **Refresh Status**: query `/status` for pending pipeline count
