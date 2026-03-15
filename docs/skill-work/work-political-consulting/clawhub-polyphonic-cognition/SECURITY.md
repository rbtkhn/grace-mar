# Security — Polyphonic cognition protocol skill

This skill is **instructions-only**. It does not:

- Execute any code (no TypeScript, shell, or other runnable assets).
- Access the network (no HTTP, no APIs).
- Read or write the filesystem.
- Use browser, shell, notifications, vault, or other runtime permissions.

The manifest specifies `permissions: []`. All behavior is driven by the natural-language prompt and the text in SKILL.md. The agent interprets the protocol; no data leaves the session unless the user explicitly asks to save or record.

No secrets, API keys, or config are required. No external services are called.
