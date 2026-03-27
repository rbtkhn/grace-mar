# DESIGN.md — Grace-Mar Companion Interface System

**Version:** 1.4  
**Last Updated:** 2026-03-27  
**Governed By:** Recursion-Gate — see [recursion-gate.md](recursion-gate.md)  
**Purpose:** The single canonical, agent-readable design system for all Grace-Mar interfaces, creative outputs, and generated UIs.

**Status:** Operator / creative-pipeline draft. **Not** SELF or Voice canon until merged through [recursion-gate.md](recursion-gate.md) per [AGENTS.md](../../AGENTS.md).  
**Pipeline:** [creative-pipeline.md](../../docs/skill-work/work-dev/creative-pipeline.md)  
**Revision:** v1.4 (2026-03-27) — full Workspace Panel interactions; artifact paths aligned with [canonical EVIDENCE](../../docs/canonical-paths.md).

---

## Principles

- Cognition-first: Every visual decision must reduce cognitive load during deep recursive work
- Dark-first aesthetic optimized for 2+ hour focused sessions
- Strict intention preservation: All visual changes require recursion-gate approval
- Calm discipline with purposeful micro-affordances (inspired by Grok’s clarity and Claude’s structured workspace)
- Agent-readable and version-controlled: This DESIGN.md is the authoritative source
- Evidence-grounded sovereignty: The interface must accurately reflect the governed Record

---

## Color Palette

- Background:          `#0F0F0F`
- Surface:             `#1A1A1A`
- Surface Elevated:    `#252525`          ← Sidebars, modals, active panels
- Workspace Panel:     `#1F1F1F`          ← Dedicated area for artifacts and structured outputs
- Text Primary:        `#E0E0E0`
- Text Secondary:      `#A0A0A0`
- Text Muted:          `#666666`

- Primary Accent:      `#0A84FF`          ← Primary actions, buttons, approvals
- Subtle Accent:       `#40C4FF`          ← Hover states, navigation highlights, live indicators (use sparingly)
- Success:             `#22C55E`
- Warning / Drift:     `#F59E0B`
- Error:               `#EF4444`

**Usage Rules:**

- Primary Accent is reserved for high-importance permanent actions
- Subtle Accent is reserved for transient feedback only
- Workspace Panel color is used exclusively for artifact/output areas
- No new colors may be introduced without updating this file and passing recursion-gate review

---

## Typography

- Headings: Inter Bold / SemiBold (1.125rem – 2.25rem)
- Body: Inter Regular (1rem base, line-height: 1.65)
- Navigation / Labels: Inter Medium
- Code / Monospace: JetBrains Mono

**Reading optimizations:**

- Long-form text: line-height 1.65
- Dense technical content (identity-diff, validation logs, recursion-gate): line-height 1.5
- Letter-spacing: -0.01em on headings

---

## Spacing & Layout

- Base unit: 8px (strict multiples only: 8, 16, 24, 32, 40, 48, 64)
- Sidebar width: 280px (expanded) / 64px (collapsed)
- Main content padding: 24px
- Section vertical rhythm: 32–40px
- Micro-interactions: 200ms ease-out transitions (subtle and non-distracting)

---

## Navigation

- Persistent left sidebar (collapsible via Ctrl/Cmd + B)
- Ordered sections:
  1. Self (identity + quick stats)
  2. Recursion-Gate (pending reviews + status)
  3. Skills & Evidence
  4. Creative Pipeline / Artifacts
  5. Journal / Memory
  6. Settings & Export

- Active item: Subtle Accent color + left border highlight
- Hover: Surface Elevated background + subtle accent

---

## Workspace Panel (Artifacts Style)

The Workspace Panel is Grace-Mar’s dedicated, resizable structured output area, inspired by Claude Artifacts. It transforms conversation into tangible, previewable, and governable artifacts while enforcing strict recursion-gate governance.

### Activation

- Automatically opens when a generation produces structured content (UI mocks, code, identity-diffs, validation reports, creative artifacts, etc.)
- Can be manually triggered with “Show in workspace”, “Preview as artifact”, or “Open workspace panel”
- Default: Right-side split-view (resizable); supports bottom panel for wider content
- Keyboard shortcut: `Ctrl/Cmd + Shift + P` to toggle — **implementation:** choose a combo that does not conflict with the host app command palette (e.g. VS Code)

### Visual Design

- Background: Workspace Panel color (`#1F1F1F`)
- Subtle 1px border separating main content from workspace panel
- Resizable with 200ms ease-out transition
- Minimum width: 320px (right) / 280px (bottom)

### Interaction Patterns

**Artifact Display**

- Single artifact: Full panel with title, metadata, and live preview
- Multiple artifacts: Tabbed interface at the top of the panel
- Supported preview types:
  - Live UI rendering (Stitch-style)
  - Syntax-highlighted code
  - Rendered Markdown and identity-diffs
  - Validation reports
  - Video thumbnails with controls (Remotion)

**Action Bar (fixed at bottom of panel)**

- Dismiss → Close current artifact
- Save as Draft → Store in `users/grace-mar/artifacts/drafts/`
- Preview Changes → Show diff against current DESIGN.md
- **Apply to Record** → Submit formal change proposal to recursion-gate (Primary Accent button; disabled until validation passes)

**Status Indicators**

- Top-right corner shows:
  - “Draft” (muted)
  - “Validation Passed” (Success color)
  - “Drift Detected” (Warning color)
- Prominent warning banner if validation fails, with direct link to validation report

**Keyboard & Accessibility**

- `Esc` → Collapse or dismiss current artifact
- `Ctrl/Cmd + Enter` → Trigger “Apply to Record” when focused
- Full keyboard navigation support
- High-contrast mode compliant

**State Management**

- Draft artifacts saved locally in `users/grace-mar/artifacts/drafts/` (non-canonical working copies; see [artifacts/drafts/README.md](artifacts/drafts/README.md))
- After recursion-gate approval: promote durable creative outputs under `users/grace-mar/artifacts/creative/` per [artifacts/creative/README.md](artifacts/creative/README.md). **Record** integration is only through the gated pipeline into [`self-archive.md`](self-archive.md) — do not use `self-evidence/` as a parallel evidence tree ([canonical-paths.md](../../docs/canonical-paths.md))
- Panel remembers last open artifact across sessions (non-Record state)

### Purpose

Enable fluid movement from conversation → live preview → validation → governed integration into the Record, without breaking focus or introducing intention drift.

---

## Component Patterns

- Cards: Rounded 12px, subtle elevation or border
- Buttons:
  - Primary: Filled with Primary Accent
  - Secondary: Outline style
  - Workspace Action: Subtle Accent for preview/apply buttons
  - Danger: Error color
- Status Indicators: Subtle Accent for live states, Success/Warning colors for recursion-gate
- Identity-Diff Panels: Monospace font with clear before/after highlighting (Warning color for drift)
- Recursion-Gate Elements: High-contrast status labels with Success/Warning colors

---

## Rules for Agents

- Read the full current DESIGN.md before any UI generation or modification
- Use Workspace Panel color exclusively for artifact areas
- Reserve Subtle Accent for transient states only
- Never introduce new colors, fonts, spacing, or visual effects
- Prioritize long-session readability and calm over visual interest
- Support keyboard navigation and high-contrast mode
- Always export a DESIGN.md diff when visual changes are proposed
- Any deviation requires explicit recursion-gate approval and identity-diff review

---

## Version History

- v1.0 — Initial dark minimal system
- v1.1 — Grok-inspired subtle accents and navigation improvements
- v1.2 — Claude-inspired Workspace Panels and structured output handling
- v1.3 — Language tightened, governance emphasis strengthened
- v1.4 (2026-03-27) — Full Workspace Panel interactions (triggers, actions, keyboard, governance flow); artifact paths aligned with canonical EVIDENCE

---

**Canonical scope:** This file is the **operator canonical spec** for interfaces, creative pipelines, Stitch/Remotion/Blender outputs, and generated UIs. **Record-facing or public presentation** changes still require companion approval through the recursion-gate. Changes to this document should be proposed and reviewed like any other operator-facing canon that touches the gate.
