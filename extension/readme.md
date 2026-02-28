# Grace-Mar Browser Extension

One-click capture from any URL to your Grace-Mar Record. LLM transcript handback for ChatGPT/Grok/Claude. Local only; stages to RECURSION-GATE (user approves via /review in Telegram).

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
   - **Toolbar** — Click the extension icon:
     - "Save to Record" — stage the current page
     - "Save transcript" — paste LLM transcript or "We did [X]" lines → POST to /handback
   - **Context menu** — Right-click:
     - "Save to Record" — page/link/selection (stages to /stage)
     - "Save transcript to Record" — selected transcript text → POST to /handback (selection only)

## What it does

- **Save to Record** — Builds activity report: `we read "[page title]"` + URL (+ optional selected text/snippet). POSTs to `/stage`. Pipeline: stage → RECURSION-GATE → user approves in Telegram via /review.
- **Save transcript** — LLM lesson transcript handback. Paste full transcript or "We did [X]" lines → POST to `/handback`. Analyst stages candidates to RECURSION-GATE. One install, one paste: user is in the recursive loop.
- **Context menu (selection)** — "Save transcript to Record" sends selected text directly to `/handback` (no paste needed when transcript is visible).
- Stage payloads: if server is unavailable, capture is queued locally and retried. Transcript handback does not queue; shows error if server down.

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
