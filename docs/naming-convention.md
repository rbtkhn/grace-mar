# Naming convention (repository)

**Purpose:** Single place for filename and path conventions in grace-mar and how they relate to the **companion-self** template. Aligns with [canonical-paths.md](canonical-paths.md) (lowercase `users/[id]/` files).

---

## Default preference

- **New docs and operator files:** Prefer **lowercase** names with **hyphens** (e.g. `identity-fork-protocol.md`, `openclaw-user.md`).
- **Repo root:** Avoid piling generic names at the root when a scoped path exists (e.g. instance exports under `users/grace-mar/`).

---

## Reserved exceptions (do not rename casually)

### `AGENTS.md` (root)

- Kept as **`AGENTS.md`** (capitalized) for **assistant and tooling discovery** (Cursor and common ecosystem practice).
- Renaming to `agents.md` would require a **large link sweep** (~90+ references) and may **reduce** automatic loading depending on product version.
- **Policy:** Treat `AGENTS.md` as a **stable, reserved** root filename unless you run a dedicated migration and verify assistant behavior.

### Legacy UPPERCASE docs under `docs/`

- Some long-lived files remain uppercase (e.g. historical audit filenames). **Rename only when already editing** or as a focused cleanup PR—not drive-by churn.

---

## Python packages (`src/`)

- Use valid Python identifiers: **`snake_case`** for packages and modules (e.g. [`src/grace_mar/`](../src/grace_mar)).
- **Do not** use hyphens in import paths; `grace-mar` is not a legal module name.

---

## JSON Schema and stable IDs

- Paths such as [`schemas/work_dev/`](../schemas/work_dev/) and JSON `$id` URLs are **contract surfaces**. Renaming directories or `$id` values is a **breaking, versioned** change—not a cosmetic rename.
- Same for [`scripts/work_dev/`](../scripts/work_dev/) (lane globs in [`lanes.yaml`](../lanes.yaml), CI, dashboards).

---

## VS Code / Cursor workspaces

### Grace-mar (this repo)

- Multi-root workspace file: **[`grace-mar.code-workspace`](../grace-mar.code-workspace)** at the repo root (roots: this repo + optional `companion-self/`).

### Companion-self (template upstream)

- If the template still ships **`companion-self-and-grace-mar.code-workspace`**, rename it in the **companion-self repository** to **`companion-self.code-workspace`** or **`template.code-workspace`** for clarity. That rename is **not** performed inside grace-mar; grace-mar only consumes the clone path `companion-self/`.
- See [merging-from-companion-self.md](merging-from-companion-self.md) for opening `grace-mar.code-workspace` and template layout.

---

## OpenClaw identity export path

- Canonical committed export for the grace-mar instance: **`users/grace-mar/openclaw-user.md`** (regenerated from `self.md` via `scripts/export_user_identity.py`).
- Example:  
  `python scripts/export_user_identity.py -u grace-mar -o users/grace-mar/openclaw-user.md`

---

## Contributing doc

- Root contributor guide: **`contributing.md`** (lowercase), linked from the README.
