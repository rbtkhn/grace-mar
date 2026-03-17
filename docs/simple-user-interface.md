# Simple User Interface — Families Without GitHub

**Purpose:** How to use Grace-Mar when you don't use GitHub or technical tools. The Telegram (or WeChat) bot is the main interface.

**See also:** [ARCHITECTURE](architecture.md) (pipeline), [PORTABILITY](portability.md) (school transfer).

---

## What You Need

- **Telegram** (or WeChat) on your phone **or** a **family web link** (if your host turned it on)
- Access to the Grace-Mar bot or the family app (ask the person who set it up)
- That’s it — no GitHub, no code, no command line

---

## Optional: Family web app (no Telegram for chat/log)

If your operator gives you a link like **https://…/app** with a **family code**, you can:

- **Chat** — talk with Grace-Mar in the browser (same idea as the bot).
- **Log** — type what you did (e.g. *We read The Wild Robot*) so it goes to the review queue.
- **Review** — a grown-up enters a separate **operator** code to approve items and update the permanent record.

Telegram is still supported; the web app is an extra channel. Technical setup: [MINIAPP-SETUP](miniapp-setup.md) (Family hub).

---

## Adding Activities ("We did X")

**The ritual:** When something worth recording happens — a drawing, a story, something learned, a new interest — send a message that starts with **"we"** and an activity verb. Grace-Mar adds it to the review queue. You approve what enters the Record. That’s how the Record grows and how the companion gets recognition for what they do.

**How to do it:**

- *We drew a volcano at school today*
- *We wrote a story about dinosaurs*
- *We learned about the water cycle*
- *We read The Wild Robot*
- *We painted a picture of the moon*

Send the message in the bot. The bot will treat it as an activity report, analyze it, and add it to the review queue. It will reply with something like: *"got it! i added that to your record. you have 3 things to review — type /review to see them."*

---

## Reviewing What’s Waiting

Type **/review** in the bot. You’ll see a list of things waiting for your approval, with buttons:

- **Approve** — add this to the permanent record
- **Reject** — do not add this

Each item is a short summary (e.g., *"new interest in volcanoes"*, *"learned about black holes"*). Tap the button to approve or reject.

**What happens after Approve:** Some items **merge right away** (quick merge — low-risk, operator chat). Others are marked approved first; a grown-up then finishes the job in the **Operator Console** (browser): open the **Gate** tab and tap **Merge approved (companion)** so the permanent record updates. That path needs the Mini App server running against a real copy of the Grace-Mar repo (see technical docs if merge fails on hosting).

---

## Chatting With Grace-Mar

The main use is still **chat** — ask questions, talk about stories, look things up. Grace-Mar will answer in the Record's voice using only what's in the record. You can also send **voice messages** in Telegram; they are transcribed and processed like typed text (including "we did X" activity reports) — ask questions, talk about stories, look things up. Grace-Mar will answer in the child’s voice using only what’s in the record.

Other useful commands:

- **/start** — reset the conversation, show menu
- **/reset** — clear chat history and start over
- **/prp** — download the Portable Record Prompt (.txt) to paste into ChatGPT, Claude, or any LLM
- **/profile** — open the fork profile (if configured) in a browser

---

## Who Processes the Record?

If someone else runs Grace-Mar for you, they use the Operator Console (or command line) to **merge** approved items into the record. You still approve in Telegram; they tap **Merge approved (companion)** when ready.

If you run everything yourself, see [operator-console.md](operator-console.md), [agents.md](../agents.md), and [PIPELINE-MAP](pipeline-map.md).

---

## School Transfer

When the user switches schools, the record belongs to you. Use **"we did X"** and **/review** as before. For handing the record to the new school, see [PORTABILITY](portability.md).

---

*Document version: 1.2*
*Last updated: March 2026*
