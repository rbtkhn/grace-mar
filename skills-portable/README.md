# Portable skills (grace-mar)

**Purpose:** Vendor-neutral **skill cores** you can copy into other hosts (ChatGPT custom instructions, Copilot skill packs, another Cursor repo) without dragging grace-mar-only paths into the default body.

**Canonical layout**

| Path | Role |
|------|------|
| `skills-portable/<skill-name>/SKILL.md` | Portable core: frontmatter + methodology (minimal instance paths) |
| `.cursor/skills/<skill-name>/CURSOR_APPENDIX.md` | **grace-mar only:** repo paths, script commands, internal doc links |
| `.cursor/skills/<skill-name>/SKILL.md` | **Generated** — do not hand-edit; run sync (see below) |

**In-repo examples:** `politics-massie` (content skill) · `jurisdiction-campaign-history` (work-politics framing) · `portable-skills-sync` (pipeline skill — use when changing this layout).

**Regenerate Cursor skill files**

```bash
python3 scripts/sync_portable_skills.py
python3 scripts/sync_portable_skills.py --dry-run
python3 scripts/sync_portable_skills.py --verify
```

**Consume outside grace-mar**

1. Copy `skills-portable/<skill>/SKILL.md` (and optional `examples/` if present).
2. Add your own appendix: paths to *your* policy docs, account rules, and compliance notes.
3. Keep `description` as **one line** (many hosts break multi-line YAML).

**Spec:** [_schema.md](_schema.md) · **Manifest:** [manifest.yaml](manifest.yaml) · **Validate:** `python3 scripts/validate_skills.py` (default check after skill edits).

---

## Discovery ladder (capture → ship)

Goal: **skills are discovered** from repeated success; the repo makes capture **low cost**.

| Step | Where | Action |
|------|--------|--------|
| **1 — Pointer** | [skill-candidates.md](skill-candidates.md) | One table row: date, working name, trigger phrase, pointer (commit / “this thread”). |
| **2 — Draft** | [_drafts/](_drafts/) | Full near-final portable `SKILL.md`; no manifest yet. |
| **3 — Listed** | `skills-portable/<skill>/` + `manifest.yaml` | Portable core + appendix path; run `sync_portable_skills.py`. |

**Triggers (assistant):** After a substantive **EXECUTE** / **EXECUTE_LOCAL** / **DOCSYNC** ship (commit, push when requested), offer **one optional** skill-capture line unless a **fixed session menu** (e.g. **`coffee`** **A–E**; legacy **hey**) applies or the operator said **no menu**. **Skills / meta:** say **skills** or **meta** with **coffee B — Build** (or after **Build**), not a separate menu letter. See [.cursor/rules/operator-style.mdc](../../.cursor/rules/operator-style.mdc) and [docs/operator-agent-lanes.md](../docs/operator-agent-lanes.md).
