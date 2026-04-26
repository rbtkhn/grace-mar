from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "work_dev" / "render_agent_surfaces_table.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("render_agent_surfaces_table_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _run_cli(
    *,
    registry: Path | None = None,
    output: Path | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(SCRIPT)]
    if registry is not None:
        cmd.extend(["--registry", str(registry)])
    if output is not None:
        cmd.extend(["--output", str(output)])
    if check:
        cmd.append("--check")
    return subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)


def _full_surface(sid: str, **overrides: object) -> dict:
    base = {
        "id": sid,
        "name": f"Name {sid}",
        "status": "implemented",
        "category": "external_runtime",
        "reads": ["r1"],
        "writes": ["w1"],
        "canonical_record_access": "read-only",
        "merge_authority": "none",
        "gate_effect": "none",
        "receipt_required": True,
        "capability_contract": "docs/c.yaml",
        "owner_lane": "work-dev",
        "notes": "n",
    }
    base.update(overrides)
    return base


def test_renderer_writes_markdown_from_temp_registry(tmp_path: Path) -> None:
    mod = _load_module()
    reg = {
        "schemaVersion": "1.0.0",
        "surfaces": [
            _full_surface("alpha"),
        ],
    }
    path = tmp_path / "agent-surfaces.v1.json"
    path.write_text(json.dumps(reg) + "\n", encoding="utf-8")
    out = tmp_path / "out.md"
    proc = _run_cli(registry=path, output=out)
    assert proc.returncode == 0
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "# Agent Surfaces Table" in text
    assert "alpha" in text
    reg2 = json.loads(path.read_text(encoding="utf-8"))
    assert mod.build_markdown(reg2) == text


def test_warning_phrases_present() -> None:
    mod = _load_module()
    md = mod.build_markdown(
        {"surfaces": [_full_surface("x")]}
    )
    assert "not Record" in md
    assert "not approval" in md
    assert "not a merge path" in md
    assert "grants no authority" in md


def test_rows_sorted_by_id() -> None:
    mod = _load_module()
    md = mod.build_markdown(
        {
            "surfaces": [
                _full_surface("zebra"),
                _full_surface("alpha"),
            ]
        }
    )
    pos_a = md.find("| alpha |")
    pos_z = md.find("| zebra |")
    assert pos_a != -1 and pos_z != -1
    assert pos_a < pos_z


def test_list_fields_use_br() -> None:
    mod = _load_module()
    md = mod.build_markdown(
        {
            "surfaces": [
                _full_surface(
                    "ls",
                    reads=["first", "second"],
                    writes=["a", "b", "c"],
                )
            ]
        }
    )
    assert "first <br> second" in md
    assert "a <br> b <br> c" in md


def test_pipe_characters_escaped_in_cells() -> None:
    mod = _load_module()
    md = mod.build_markdown(
        {
            "surfaces": [
                _full_surface("p", name="a|b", notes="x|y"),
            ]
        }
    )
    assert r"a\|b" in md
    assert r"x\|y" in md


def test_check_exits_zero_when_current(tmp_path: Path) -> None:
    reg = {"schemaVersion": "1.0.0", "surfaces": [_full_surface("u")]}
    reg_path = tmp_path / "reg.json"
    reg_path.write_text(json.dumps(reg) + "\n", encoding="utf-8")
    out = tmp_path / "t.md"
    mod = _load_module()
    out.write_text(mod.build_markdown(reg), encoding="utf-8")
    proc = _run_cli(registry=reg_path, output=out, check=True)
    assert proc.returncode == 0
    assert proc.stderr == ""


def test_check_exits_nonzero_when_stale(tmp_path: Path) -> None:
    reg = {"schemaVersion": "1.0.0", "surfaces": [_full_surface("u")]}
    reg_path = tmp_path / "reg.json"
    reg_path.write_text(json.dumps(reg) + "\n", encoding="utf-8")
    out = tmp_path / "t.md"
    out.write_text("# stale\n", encoding="utf-8")
    proc = _run_cli(registry=reg_path, output=out, check=True)
    assert proc.returncode == 1
    assert "stale" in proc.stderr.lower() or "missing" in proc.stderr.lower()


def test_check_exits_nonzero_when_missing(tmp_path: Path) -> None:
    reg = {"schemaVersion": "1.0.0", "surfaces": [_full_surface("u")]}
    reg_path = tmp_path / "reg.json"
    reg_path.write_text(json.dumps(reg) + "\n", encoding="utf-8")
    out = tmp_path / "nope.md"
    proc = _run_cli(registry=reg_path, output=out, check=True)
    assert proc.returncode == 1
    assert "missing" in proc.stderr.lower()


def test_null_and_omitted_fields_render_em_dash() -> None:
    mod = _load_module()
    row = _full_surface("om", name="Has name")
    del row["notes"]
    row["capability_contract"] = ""
    row["receipt_required"] = None  # type: ignore[assignment]
    md = mod.build_markdown({"surfaces": [row]})
    # notes column last; should contain em dash for missing notes
    assert "\u2014" in md
    # receipt required wrong type -> em dash
    assert "| — |" in md or "\u2014" in md.split("Has name")[1]


def test_summary_counts() -> None:
    mod = _load_module()
    surfaces = [
        _full_surface("i1", status="implemented", receipt_required=True, capability_contract="c1"),
        _full_surface("i2", status="implemented", receipt_required=False, capability_contract=""),
        _full_surface("part", status="partial", receipt_required=True, capability_contract="c2"),
        _full_surface("doc", status="documented_only", receipt_required=False, capability_contract=""),
        _full_surface("plan", status="planned", receipt_required=True, merge_authority="merge", capability_contract=""),
    ]
    md = mod.build_markdown({"surfaces": surfaces})
    assert "- Total surfaces: 5" in md
    assert "- Implemented: 2" in md
    assert "- Partial: 1" in md
    assert "- Documented-only: 1" in md
    assert "- Planned: 1" in md
    assert "- Surfaces requiring receipts: 3" in md
    assert "- Surfaces with capability contracts: 2" in md
    assert "- Surfaces with merge authority: 1" in md
