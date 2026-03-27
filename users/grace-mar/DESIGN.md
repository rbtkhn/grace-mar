# DESIGN.md — Grace-Mar companion interface system (operator draft)

**Status:** Operator / creative-pipeline draft. **Not** SELF or Voice canon until merged through [recursion-gate.md](recursion-gate.md) per [AGENTS.md](../../AGENTS.md).  
**Pipeline:** [creative-pipeline.md](../../docs/skill-work/work-dev/creative-pipeline.md)  
**Revision:** v1.3 (2026-03-27) — workspace panel token, spacing and layout spec, component patterns, version history.

---

## Principles

- Maximum clarity with minimal cognitive load.
- Dark-first, high-contrast aesthetic suited to **long recursive sessions** (calm over visual noise).
- **Two-tier accents:** one color for durable / high-importance actions; a second, used **only** for transient UI (hover, focus, live state). See Color Palette.
- Prefer **clarity-first surfaces** and **structured artifact panels** when designing tools and exports so long reads and diffs stay scannable.
- Creative and UI work stays aligned with recursion-gate and identity-diff discipline when outputs touch the Record or public presentation.

---

## Color Palette

**Core**

- Background: `#0F0F0F`
- Surface: `#1A1A1A`
- Surface elevated: `#252525` — sidebars, modals, active rows, cards that must read above base surface
- **Workspace panel:** `#1F1F1F` — dedicated shell for editor-style, timeline, or multi-pane work areas (distinct from card/surface elevated when separation matters)
- Text primary: `#E0E0E0`
- Text secondary: `#A0A0A0`
- Text muted: `#666666` — timestamps, metadata, de-emphasized labels

**Accents (two-tier)**

- Primary accent: `#0A84FF` — primary buttons, permanent high-importance actions, strong links
- Subtle accent: `#40C4FF` — **transient only:** hover, focus rings, live indicators, active nav hint; **not** for primary chrome or default button fill

**Semantic**

- Success: `#22C55E`
- Warning / drift signal: `#F59E0B`
- Error: `#EF4444`

**Rules**

- Do not add new hex colors without updating this file and operator/gate agreement for anything Record- or product-facing.

---

## Typography

- Headings: Inter Bold (or SemiBold for subheads)
- Body: Inter Regular
- Navigation / UI labels: Inter Medium where hierarchy helps
- Code: JetBrains Mono

**Line height (long sessions)**

- Body and long-form prose: **~1.65**
- Dense surfaces (identity-diff, validation logs, recursion-gate tables): **~1.5**

---

## Spacing & Layout

**Grid**

- Base unit: **8px**
- Allowed multiples: 8, 16, 24, 32, 40, 48, 64
- Default section gap: 32px

**Layout**

- Align major blocks to the 8px grid; avoid arbitrary odd margins that break rhythm.
- Prefer consistent **max readable width** for prose-heavy panels (operator tools may use fixed side rails + fluid center).
- Use **16px** as the default inner padding for cards and list rows unless a denser table view is explicitly specified.
- Reserve **24px+** between unrelated regions (e.g. nav rail vs. main) so hierarchy reads without extra chrome.

---

## Navigation (information architecture)

Recommended **order** for app-style shells (dashboards, internal tools); not every channel (e.g. chat) uses all of these.

1. Self — identity + quick context  
2. Recursion-Gate — pending reviews, status  
3. Skills and Evidence  
4. Creative pipeline / artifacts  
5. Journal / memory  
6. Settings and export  

---

## Workspace panels

- Use **`#1F1F1F`** as the default workspace panel background when the main task is reading, editing, or comparing artifacts inside a shell (not for global app background).
- Pair workspace panels with **surface elevated** (`#252525`) for nested cards, popovers, and sticky headers so depth stays obvious in dark mode.
- Keep **one** primary accent action visible per panel focus; use subtle accent only for transient states inside the panel.
- Split layouts (e.g. list + detail) should share the same panel background token unless the secondary pane is explicitly a modal or drawer.

---

## Component Patterns

**Actions**

- **Primary button:** primary accent fill, primary text contrast; one per logical view where possible.
- **Secondary button:** outline or ghost on surface elevated; no subtle-accent fill.
- **Danger:** semantic error color; reserve for destructive or irreversible actions.

**Data and status**

- **Cards:** surface elevated, 16px padding, 8px radius optional; metadata in text muted.
- **Badges:** compact; semantic colors for state; avoid subtle accent as a permanent badge fill.
- **Recursion-gate indicators:** subtle accent allowed for live / active state only; stable states use primary or semantic tokens.
- **Identity-diff panels:** monospace; use warning color to highlight drift, not decoration.

**Forms and inputs**

- Default input background at or one step above workspace panel; visible focus ring using subtle accent.
- Help text and validation: text secondary for hints; error color for blocking issues only.

Treat this list as the agreed pattern set; new recurring UI shapes should be added here when they become part of the system.

---

## Rules for Agents

- Read this file before generating UI that represents Grace-Mar or the gate.
- Prefer **primary accent** for committed importance; **subtle accent** only for transient feedback and navigation hints.
- Do not invent new colors, fonts, shadows, or spacing outside this file’s tokens and 8px grid.
- Use **`#1F1F1F`** for workspace-style panels when spec calls for a dedicated work surface, not as a replacement for global `#0F0F0F` background without reason.
- Deviations for one-off mocks must be labeled in the creative brief and kept out of merged Record until approved.

---

## Version History

| Version | Date | Notes |
|--------|------|--------|
| v1.3 | 2026-03-27 | Workspace panel `#1F1F1F`; `Spacing & Layout` and `Component Patterns` sections; workspace panel guidance; neutral principle wording. |
| Quick wins | 2026-03-27 | Two-tier accents, elevated surface, text muted, line-height guidance, nav IA order. |

---

**Operator note:** This document is the **operator canonical spec** for UI and creative outputs in this instance. Record-facing or public presentation changes still require companion approval through the gate.
