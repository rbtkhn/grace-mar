# BrewMind FAQ — ingest summary (WORK)

**Captured:** 2026-04-05  
**Territory:** work-xavier **evidence** — not Xavier’s Record; not a gate merge.  
**Sources:** Gemini mobile session (screenshot) + PDF export of the same conversation thread ([`brewmind-faq-gemini-transcript-2026-04-05.pdf`](brewmind-faq-gemini-transcript-2026-04-05.pdf)). Original download filename: `Brewmind FAQ transcipt.pdfs=1.pdf` (typo preserved in history only).

## What was produced

- **User ask:** “Make a FAQ page for my BrewMind website.”
- **Deliverable:** Draft FAQ copy + **HTML `<details>` / `<summary>` accordion** section + **CSS** aligned to existing `index.html` tokens (`var(--cream)`, `var(--green)`, `.section-inner`, `.reveal`, etc.).
- **Placement:** Instructions to insert FAQ **between Membership and Contact**; optional **nav** link `#faq`.

## FAQ content outline (headings)

1. **General** — What is BrewMind Café; location (Cebu City, opening soon); hours (Mon–Fri 7–10, Sat 8–11, Sun 9–8).  
2. **Learning & earning** — Learn-to-earn steps (drink → micro-lesson → BrewPoints → tracks → income paths); no prior tech required (Track 1); **₱0** start / Brew tier; Mind **₱799/mo**, Elite **₱1,599/mo**.  
3. **Memberships** — Tier table (continued on transcript p.2).  
4. **Menu & café** — Drink names (“The Prompt”, “Neural Latte”, “Zero-Shot Soda”); food (croissants, “Mind Sandwich”, overnight oats, Basque cheesecake).  
5. **Follow-up UX** — Smooth-scroll question; user OK’d; Gemini confirms theme match to BrewMind CSS variables and fonts.

## Files in this folder

| File | Role |
|------|------|
| [brewmind-faq-gemini-transcript-2026-04-05.pdf](brewmind-faq-gemini-transcript-2026-04-05.pdf) | Full transcript (5 pages, Skia/Google Docs PDF). |
| [brewmind-faq-gemini-mobile-2026-04-05.png](brewmind-faq-gemini-mobile-2026-04-05.png) | Mobile screenshot (draft header + first Q&As). |
| This file | Operator-facing summary for search and handoff. |

## Next (operator / Xavier — outside this ingest)

- Paste HTML/CSS into **her** site repo or deployment pipeline; **verify** pricing and hours against [brewmind-business-plan.md](../brewmind-business-plan.md) before publish.  
- No **recursion-gate** action unless she wants durable **IX** lines about the business as **Record** (separate decision).
