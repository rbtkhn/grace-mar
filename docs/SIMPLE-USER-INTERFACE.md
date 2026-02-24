# Simple User Interface — Families Without GitHub

**Purpose:** How to use Grace-Mar when you don't use GitHub or technical tools. The Telegram (or WeChat) bot is the main interface.

**See also:** [ARCHITECTURE](ARCHITECTURE.md) (pipeline), [PORTABILITY](PORTABILITY.md) (school transfer).

---

## What You Need

- **Telegram** (or WeChat) on your phone
- Access to the Grace-Mar bot (ask the person who set it up for the link)
- That’s it — no GitHub, no code, no command line

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

**Important:** Approving in the bot updates the status. The full merge into the record (SELF, EVIDENCE, etc.) happens when the system is next processed — usually by whoever runs Grace-Mar for you (or on a schedule). If you run the bot yourself, you’ll need to run the review-queue process separately (see technical docs).

---

## Chatting With Grace-Mar

The main use is still **chat** — ask questions, talk about stories, look things up. Grace-Mar will answer in the Record's voice using only what's in the record. You can also send **voice messages** in Telegram; they are transcribed and processed like typed text (including "we did X" activity reports) — ask questions, talk about stories, look things up. Grace-Mar will answer in the child’s voice using only what’s in the record.

Other useful commands:

- **/start** — reset the conversation, show menu
- **/reset** — clear chat history and start over
- **/prp** — download the Portable Record Prompt (.txt) to paste into ChatGPT, Claude, or any LLM
- **/dashboard** — open the fork dashboard (if configured) in a browser

---

## Who Processes the Record?

If you’re using a **hosted** setup (someone else runs the bot), they usually handle processing. You add activities and approve/reject; they make sure changes are applied and the record stays up to date.

If you run the bot yourself, see [AGENTS.md](../AGENTS.md) and [PIPELINE-MAP](PIPELINE-MAP.md) for how to process the review queue.

---

## School Transfer

When the user switches schools, the record belongs to you. Use **"we did X"** and **/review** as before. For handing the record to the new school, see [PORTABILITY](PORTABILITY.md).

---

*Document version: 1.0*
*Last updated: February 2026*
