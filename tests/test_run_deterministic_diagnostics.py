from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "run_deterministic_diagnostics.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "run_deterministic_diagnostics_mod",
        SCRIPT,
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_fake_repo(root: Path) -> None:
    _write(
        root / "scripts" / "audit_doctrine_drift.py",
        "print('doctrine ok')\n",
    )
    _write(
        root / "scripts" / "work_dev" / "audit_agent_sprawl.py",
        "print('sprawl ok')\n",
    )
    _write(
        root / "scripts" / "simulate_counterfactual_fork.py",
        (
            "from __future__ import annotations\n"
            "import argparse\n"
            "import json\n"
            "from pathlib import Path\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--proposal', required=True)\n"
            "parser.add_argument('--output', required=True)\n"
            "args = parser.parse_args()\n"
            "out = Path(args.output)\n"
            "out.parent.mkdir(parents=True, exist_ok=True)\n"
            "out.write_text(json.dumps({'ok': True}, indent=2) + '\\n', encoding='utf-8')\n"
            "print(out)\n"
        ),
    )
    _write(
        root / "examples" / "diagnostics" / "counterfactual-proposal.example.json",
        json.dumps({"proposal_id": "example"}, indent=2) + "\n",
    )


def test_runner_exists_and_can_be_invoked(tmp_path: Path) -> None:
    _build_fake_repo(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Doctrine Drift Radar" in result.stdout
    assert "Agent Sprawl Control Plane" in result.stdout
    assert "Counterfactual Fork Simulator" in result.stdout
    smoke_output = (
        tmp_path
        / "artifacts"
        / "counterfactual-simulations"
        / "deterministic-diagnostics-smoke.json"
    )
    assert not smoke_output.exists()


def test_runner_returns_zero_and_prints_sections_on_success(
    monkeypatch,
    capsys,
    tmp_path: Path,
) -> None:
    mod = _load_module()
    calls: list[list[str]] = []
    smoke_output = (
        tmp_path
        / "artifacts"
        / "counterfactual-simulations"
        / "deterministic-diagnostics-smoke.json"
    )

    def fake_run(command, **kwargs):
        calls.append(command)
        if "simulate_counterfactual_fork.py" in command[1]:
            smoke_output.parent.mkdir(parents=True, exist_ok=True)
            smoke_output.write_text('{"ok": true}\n', encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(mod.subprocess, "run", fake_run)
    exit_code = mod.run_diagnostics(tmp_path)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Doctrine Drift Radar" in captured.out
    assert "Agent Sprawl Control Plane" in captured.out
    assert "Counterfactual Fork Simulator" in captured.out
    assert calls
    assert all(call[0] == sys.executable for call in calls)
    assert not smoke_output.exists()


def test_runner_returns_nonzero_if_subprocess_fails(
    monkeypatch,
    capsys,
    tmp_path: Path,
) -> None:
    mod = _load_module()
    calls: list[list[str]] = []

    def fake_run(command, **kwargs):
        calls.append(command)
        if "audit_agent_sprawl.py" in command[1]:
            return subprocess.CompletedProcess(
                command,
                1,
                stdout="",
                stderr="sprawl failed\n",
            )
        return subprocess.CompletedProcess(command, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(mod.subprocess, "run", fake_run)
    exit_code = mod.run_diagnostics(tmp_path)
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "deterministic diagnostics failed during: Agent Sprawl Control Plane" in captured.err
    assert len(calls) == 2
    assert all(call[0] == sys.executable for call in calls)
