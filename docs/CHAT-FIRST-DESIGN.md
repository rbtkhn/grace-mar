# Chat-First Design Principles

**Purpose:** Design principles for delivering the full Grace-Mar experience within the constraint of a Telegram (or WeChat) text chat. The user interface is messages and buttons — no native app, no custom UI. These principles guide how we build.

**Governed by:** [GRACE-MAR-CORE v2.0](GRACE-MAR-CORE.md)

**See also:** [ARCHITECTURE](ARCHITECTURE.md), [SIMPLE-USER-INTERFACE](SIMPLE-USER-INTERFACE.md)

---

## The Constraint

Grace-Mar must work entirely within a messaging app:
- Text messages
- Inline buttons (tap to respond)
- Reply keyboards (persistent buttons)
- Voice input (transcribed)
- Push notifications
- Persistent chat thread

No custom app shell. No dashboards. No wizards. The chat *is* the interface.

---

## Aspiration: Alternative, Not Imitation

The system should feel like an **alternative** to:
- **Infinite scroll** (TikTok, feeds) — bounded, completable, meaningful
- **Addictive mobile games** — rewarding without endless grind, progress that accrues

Not by imitating those experiences, but by offering something different that *competes for attention*: quick, satisfying, bounded, and grounded in real growth.

---

## System-Wide Principles

### 1. The Chat Is the Product

When the user opens the bot, they are *in* the product. No splash screen, no onboarding flow. The conversation *is* the experience. Every mode (chat, lookup, homework, curiosity) lives in the same thread.

### 2. One Primary Action Per Moment

Each interaction has one clear action:
- **Chat** — type, get reply
- **Lookup** — ask, get answer
- **Homework** — tap A/B/C/D
- **Pipeline** — type "we did X", or tap /review

No nested menus. No "where do I go?" The reply keyboard and inline buttons surface the paths.

### 3. The Record Is Felt, Not Seen

The Record (SELF, SKILLS, EVIDENCE) is the core of the system, but the user never *sees* it in chat. They experience it through:
- What the Voice says (grounded in the Record)
- Homework questions (sourced from the Record)
- Lookup answers (or "I don't know" + offer to look up)
- Pipeline flows ("we did X" → staging → approval)

The magic is in *answers that reflect who they are*. The Record's value is demonstrated, not displayed.

### 4. The Chat Is the Relationship

The persistent thread is the shared history. Every session accumulates. The chat becomes a trophy case: scroll up to see past homework completions, past conversations, past approvals. No separate app needed. Loyalty comes from continuity in one place.

### 5. Growth Is Noticeable Over Time

The user should *feel* the Record growing: better answers, more relevant homework, "she knows more about me." Quality of response and personalization prove the system is working. Abstract progress (dashboards, stats) is optional; the chat itself should reveal growth.

### 6. Constraint Forces Clarity

Limitations (text only, buttons, no animations) are not excuses — they force focus. Complexity must be absorbed by the system, not dumped on the user. One thing per message. One tap where possible. The narrow channel demands clarity.

---

## Engagement-Specific Principles

### Bounded Sessions

Any activity with a clear start and end (homework, a lookup, a "we did X") should have **closure**:
- Explicit completion: "all done!"
- Optional "want more?" — user chooses to continue
- No infinite continuation; each session is a complete unit

### One Thing at a Time

Do not dump multiple questions, options, or steps in one message. One question → one response → next. The rhythm matches attention: one unit of work per unit of attention.

### One-Tap When Possible

If the user can tap instead of type, offer it. Inline buttons (A, B, C, D) for homework. Approve/Reject for pipeline. Reduce friction; match the "quick fire" feel of addictive apps but with meaning.

### Immediate Feedback

Response should follow action within a second. "Yes!" or "not quite — it's B because…" — then next. No loading screens, no "please wait." The loop is: act → see result → act again.

### Milestones, Not Endlessness

Give the user a target: "30 correct = champ," "8 questions this round." Progress accrues; there is a finish line. The system offers *completion*, not infinite engagement.

### Voice in Character

Every response should sound like the Record — Grace-Mar's voice, vocabulary, enthusiasm. The personality is the differentiator. Generic assistant tone breaks the spell.

---

## What We Don't Do

- **No hidden complexity** — If it requires explanation, simplify or remove it
- **No dashboards as requirement** — The chat must stand alone; dashboards are optional enhancements
- **No endless flows** — Sessions have endpoints
- **No mimicking flash** — We don't compete on animations or sound; we compete on meaning and relationship
- **No abstraction without payoff** — "The Record" is invisible, but its effects (better answers, personalized homework) must be obvious

---

## Invariants

When designing new features or modes:

1. **Fits in one message** — Can the prompt and options fit without overwhelming?
2. **One action per response** — What is the single thing the user does next?
3. **Bounded or completable** — Is there a natural end?
4. **Record-grounded** — Does it use or feed the Record?
5. **In character** — Does it sound like the Voice, not a generic bot?

---

## Success Criteria

The design works if:
- A 6-year-old can use it without explanation
- The operator can hand the device to the user and step back
- The user *chooses* to open Grace-Mar over another app in a moment of boredom
- The chat history, scrolled months later, feels like a relationship

---

*Last updated: February 2026*
