# Canva Integration

**Purpose:** Explore integrating Canva's design capabilities with Grace-Mar for creative output, newsletters, and shareable content.

**Status:** Design-stage. Not yet implemented.

**See also:** [DESIGN-ROADMAP](design-roadmap.md), [JOURNAL-SCHEMA](journal-schema.md)

---

## Canva APIs Overview

| API | Purpose |
|-----|---------|
| **Connect API** | Integrate design into web apps — sync assets, designs, comments; embed Canva in workflows |
| **App SDK** | Build apps that import content, add design elements, or automate design tasks; distribute via Apps Marketplace or privately |
| **Admin API** | Manage users, teams, and groups within a Canva organization |
| **SCIM API** | Automate user provisioning and deprovisioning |

With Canva's APIs you can:
- Integrate Canva into existing workflows
- Insert data from applications into Canva templates
- Retrieve user data and designs
- Manage user details and access

---

## Grace-Mar Use Cases

| Use case | Canva API | Flow |
|----------|-----------|------|
| **WORK (creation) evidence** | Connect API | User creates design in Canva → export/retrieve → "we designed X" → pipeline stages → EVIDENCE creation log |
| **Newsletter layout** | Connect API / App SDK | Outbound digest (IX-B, LIBRARY) → populate Canva template → render as image/PDF → email or JOURNAL |
| **Template + Record** | App SDK | IX-B curiosity, LIBRARY titles, or JOURNAL highlights → insert into Canva template → parent-approved output |
| **Shareable content** | Connect API | Designs as JOURNAL daily highlights; shareable portfolio for admissions/family |

---

## Principles

- **Gated:** Canva outputs do not auto-ingest. User invokes "we designed X" or approves template population.
- **Child-safe:** Parent manages Canva account; COPPA/PII considerations apply if user is under 13.
- **Evidence grounding:** Designs reference Record (interests, LIBRARY) — template content matches profile.

---

## Requirements (Future)

- Canva developer account and API credentials
- OAuth flow for user/org access (parent-managed)
- Template design and variable mapping (e.g. curiosity topics → template slots)

---

## 2027 Vision: Brainstormed Ideas

Projecting technology trends (AI-assisted design, personalization, multimodal creation, embedded integrations, child-safe tiers) into Grace-Mar + Canva ideas for 2027.

### 1. Record-Aware AI Design Assistant

**Assumption:** Canva's AI understands user context and design preferences.

- **Voice-to-design** — Child says "I learned about Jupiter's red spot" → AI suggests a simple "fact card" layout (image + text)
- **Profile-aware templates** — IX-B curiosity, LIBRARY, SKILLS edge feed template selection (e.g. space interests → space-themed layouts)
- **Lexile-aware copy** — AI generates caption text within the fork's Lexile ceiling
- **Style memory** — Learns aesthetic preferences (colors, layout density) and reuses them

### 2. "Today I…" Auto-Cards

**Assumption:** Programmatic design generation and quick iterations.

- **Daily prompt** — After activity, system generates a draft design: "Today I learned about the Nutcracker"
- **Source** — EVIDENCE (ACT-*, WRITE-*, CREATE-*), JOURNAL highlights
- **Flow** — Draft card → parent reviews in Canva → approves → JOURNAL or share
- **Output** — Fact cards, "This week" summary cards, shareable with family or school

### 3. Reading & Story Response Cards

**Assumption:** Better text understanding and template mapping.

- **Post-LIBRARY** — "I read Little Red Riding Hood" → Canva suggests story-response templates (character, favorite scene, one sentence)
- **Read-along prompts** — Templates tied to LIBRARY stories (Grimm, Andersen, ballet)
- **Skills edge** — Slightly harder tasks ("compare two stories") mapped to simple comparison templates

### 4. Collaborative Family Design Sessions

**Assumption:** Real-time co-editing and child-safe collaboration modes.

- **Parent + child** — Parent in Canva, child contributes via voice or simple drag-and-drop
- **Artifact flow** — Result exported → "we designed X together" → pipeline → EVIDENCE creation log
- **Roles** — Parent controls layout/complexity; child controls content (words, images, choices)

### 5. Growth Portfolios & Timeline Views

**Assumption:** Programmatic portfolio assembly.

- **Quarterly summary** — Auto-assemble from JOURNAL + EVIDENCE → Canva template → "First grade highlights" PDF
- **Admissions portfolio** — Best WRITE + CREATE + LEARN entries → school-ready portfolio
- **Timeline view** — Chronological growth (writing samples, fact cards) in a Canva layout

### 6. Curiosity → Content Packs

**Assumption:** AI content generation and template personalization.

- **Topic packs** — IX-B topic (e.g. reptiles, gemstones) → Canva generates a mini "curiosity pack" (facts, prompts, visuals)
- **LIBRARY extensions** — "If you liked X…" prompts with suggested designs ("Design a poster for your favorite scene")
- **Output** — Printable activity kits or shareable links

### 7. Design-as-Expression (WORK creation)

**Assumption:** Canvas as creative tool, not just templates.

- **Sketch-to-design** — Child draws on tablet → Canva suggests polished layout or refines composition
- **Mood boards** — Child selects images/colors → AI suggests layouts ("my favorite things," "what I learned")
- **Evidence** — Export → "we made a mood board about space" → EVIDENCE creation log (parallel to physical art)

### 8. Embedded in Future Channels

**Assumption:** Canva embedded in Notion, Slack, messengers, OpenClaw.

- **Inline creation** — From OpenClaw/agent: "Want to turn today's highlights into a card?" → Canva opens in-place
- **One-tap JOURNAL cards** — After a rich day, "Create today's card" opens Canva with JOURNAL highlights pre-filled
- **Shared workspace** — Family workspace where Record drives suggestions ("Based on what Grace-Mar learned this week…")

### 9. Child-Safe & Age-Gated Modes

**Assumption:** Education/child tier, stricter controls.

- **Education tier** — Filtered templates, limited sharing, no open web search
- **COPPA alignment** — No PII collection, parent-managed account, no ads
- **Lexile/age bands** — Templates and copy constrained to age-appropriate levels

### 10. Multimodal Capture (Photo, Voice, Scan)

**Assumption:** Seamless import from photos, scans, voice.

- **Photo → design** — Photo of drawing/worksheet → auto-crop, place in Canva layout ("My art this week")
- **Voice note → card** — "Today I learned that reptiles are cold-blooded" → draft fact card with placeholders
- **Scanned writing** — WRITE samples scanned → placed in "writing portfolio" template

---

## 2027 Prioritization

| Priority | Idea | Rationale |
|----------|------|-----------|
| 1 | Today I… Auto-Cards | Highest value-to-effort; directly feeds JOURNAL and evidence |
| 2 | Reading & Story Response Cards | Aligns with LIBRARY; supports READ + BUILD |
| 3 | Growth Portfolios | Clear parent/school value; uses existing data |
| 4 | Record-Aware Templates | Differentiator; makes Canva "for this child" |
| 5 | Collaborative Family Sessions | Habit-forming; strong WORK creation evidence |

---

*Last updated: February 2026*
