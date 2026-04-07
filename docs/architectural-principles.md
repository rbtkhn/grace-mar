# Architectural Principles

**Companion-Self template -- Named design patterns already in use**

---

These five principles name the architectural patterns that already govern how companion-self and its instances are built. They are not aspirational; they describe what exists. Naming them provides a shared vocabulary for evaluating proposals and avoiding accidental violations.

---

## 1. Minimal core, extensible edge

> Keep the center lean enough that its logic stays legible.

The core is small: state separation, authority classes, promotion law, knowledge boundary, gated pipeline. Everything else — lanes, modes, dashboards, integrations — lives at the edge. The edge can grow without changing the core.

**Already implemented as:**
- `AGENTS.md` (core doctrine, Layer 1) — trimmed to ~200 lines of constitutional rules
- `template-manifest.json` sections — each feature set (`seed_registry`, `change_review`, `record_diff_queue`, `layer_architecture`) is a self-contained package with its own schemas, scripts, and docs
- Lane overlays (`docs/skill-work/work-*/`) and mode overlays (`.cursor/skills/*/SKILL.md`) extend without modifying the core

**Test:** If adding a feature requires editing `AGENTS.md` core doctrine rather than an overlay, pause and ask whether the core actually needs to change or whether the feature should live at the edge.

---

## 2. Branch / fork / mainline

> Not all inquiry belongs on the mainline.

The system distinguishes provisional observations from durable governed state. Seed claims, draft proposals, and exploratory thought stay on branches until evidence, recurrence, and human review earn them a place on the mainline.

**Already implemented as:**
- Seed registry lifecycle: `observed` → `weak_signal` → `recurring` → `candidate` → `cross_evidenced` → `stable` → `promoted`
- Mainline = governed state (`self.md`, `self-archive.md`)
- Branch = seed claim in `seed-registry.jsonl` (provisional, revocable)
- Fork = contradiction pair (preserved, not collapsed)
- Merge = gated promotion only after human review

**Test:** Can you point to the status field that distinguishes this data from governed truth? If not, it might be leaking into the mainline.

---

## 3. Reloadable overlays

> Modify non-core layers and re-apply without rebuilding everything.

Lane overlays, mode overlays, configuration files, and presentation surfaces can be changed independently of core doctrine. Skills reload on read. Config files are parsed at runtime.

**Already implemented as:**
- `.cursor/skills/` — each skill is a reloadable mode overlay (coffee, dream, bridge, harvest, gate-review)
- `config/*.json` — adjustable without core changes (seed-promotion-rules, authority-map, context-budgets, source-of-truth)
- `docs/skill-work/work-*/` — lane overlays load when the lane is active

**Constraint:** Core doctrine and constitutional rules (`AGENTS.md`, authority classes, gated pipeline law) are never silently reloaded. Changes to governed state surfaces require explicit human review.

---

## 4. Transparency

> Every important object should answer: what is this, where did it come from, who can change it, what evidence supports it, what status is it in, what depends on it.

The system favors visible, inspectable state over hidden abstraction. Governance works because stakeholders can see what happened, why, and who authorized it.

**Already implemented as:**
- `config/authority-map.json` — declares who can modify each surface
- `config/source-of-truth.json` — declares canonical location for each concept
- Nursery "why still a seed" surface (`seed_nursery_report.py`) — explains why each claim hasn't promoted
- Provenance on IX entries (`provenance: human_approved`, `source:`, `scope:`)
- `pipeline-events.jsonl` — append-only audit trail for all pipeline transitions
- `session_observability.py` — real-time metrics for session awareness

**Test:** If an object exists in the system but no surface shows its provenance, authority, or status, that's a transparency gap.

---

## 5. Composable packages

> Major capabilities attach as coherent kits, not loose files.

Each feature set is a package: schema, scripts, documentation, tests, and manifest entry. Packages can be installed, audited, and removed without affecting other packages.

**Already implemented as:**
- `template-manifest.json` sections: `seed_phase`, `change_review`, `record_diff_queue`, `seed_registry`, `layer_architecture`
- Each section declares its entrypoint, schemas, scripts, config, and docs
- Instance-specific additions (e.g. `seed_to_gate.py` in grace-mar) are separate from template-portable packages
- Demo data (`users/demo/`) provides working examples for each package

**Test:** When adding a new feature, does it register in `template-manifest.json` as a named section? If it's scattered across files with no manifest entry, it's not yet a package.

---

## What these principles do not include

- **Extension marketplace or install lifecycle.** `template-manifest.json` already serves as the package registry. No new abstraction until the current pattern proves insufficient.
- **Overlay versioning.** Skills reload on read; adding version tracking is low-value until overlays change frequently enough to cause drift.
- **YOLO permission model.** These principles borrow structural elegance from modular agent systems while explicitly rejecting ungoverned power. Companion-self is as minimal and extensible as the best agent frameworks, but governed where they are permissive.

---

## Cross-references

- [layer-architecture.md](layer-architecture.md) — The four-layer instruction model (principle 1 and 3 in action)
- [seed-registry.md](seed-registry.md) — Branch/fork/mainline lifecycle (principle 2)
- [seed-phase-doctrine.md](seed-phase-doctrine.md) — Constitutional formation rules
- [session-observability.md](session-observability.md) — Transparency metrics (principle 4)
- [AGENTS.md](../AGENTS.md) — Core doctrine
