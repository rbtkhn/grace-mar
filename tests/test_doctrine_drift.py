from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "audit_doctrine_drift.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("audit_doctrine_drift_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _base_config() -> dict:
    return {
        "schemaVersion": "1.0.0",
        "rules": [
            {
                "id": "approved-canonical-writers",
                "kind": "python_canonical_writer_allowlist",
                "targets": ["scripts/**/*.py"],
                "protectedNames": ["recursion-gate.md", "self-archive.md"],
                "protectedExactPaths": ["bot/prompt.py"],
                "approvedWriters": ["scripts/approved_writer.py"],
            },
            {
                "id": "interface-artifact-non-authority",
                "kind": "json_field_const",
                "targets": ["artifacts/**/*.json"],
                "appliesWhen": {
                    "allKeys": ["artifactId", "artifactKind", "recordAuthority", "gateEffect"]
                },
                "expected": {"recordAuthority": "none", "gateEffect": "none"},
            },
            {
                "id": "portable-emulation-no-merge-authority",
                "kind": "json_field_const",
                "targets": ["docs/portability/emulation/emulation-bundle-schema.v1.json"],
                "expected": {"properties.authority.properties.mergeAuthority.const": "none"},
            },
            {
                "id": "workbench-receipts-no-evidence-truth",
                "kind": "json_forbidden_text",
                "targets": ["artifacts/**/*.json"],
                "appliesWhen": {"fieldEquals": {"receiptKind": "workbench"}},
                "forbiddenSubstrings": ["proof of external facts", "evidence truth"],
            },
            {
                "id": "work-docs-no-canonical-merge-authority",
                "kind": "text_forbidden_regex",
                "targets": ["docs/skill-work/**/*.md"],
                "forbiddenRegex": "\\b(?:can|may|has|have|grants?|with)\\b[^\\n]{0,80}\\b(?:canonical )?merge authority\\b",
                "ignoreIfLineContainsAny": ["must not", "does not", "do not", "not ", "no ", "never", "without"],
            },
            {
                "id": "proposal-envelopes-require-human-review",
                "kind": "text_required_regex",
                "targets": ["docs/portability/emulation/behavior-spec/v1-proposal-envelope.md"],
                "requiredAllRegex": ["requires_human_review\"\\s*:\\s*true", "human review"],
            },
        ],
    }


def _build_repo(root: Path) -> Path:
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    (root / "artifacts" / "work-dev" / "interface-artifacts").mkdir(parents=True, exist_ok=True)
    (root / "artifacts" / "work-dev" / "workbench-receipts").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "portability" / "emulation" / "behavior-spec").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "skill-work" / "work-dev").mkdir(parents=True, exist_ok=True)
    (root / "config").mkdir(parents=True, exist_ok=True)

    (root / "scripts" / "approved_writer.py").write_text(
        'gate_path = user_dir / "recursion-gate.md"\n'
        'gate_path.write_text("ok", encoding="utf-8")\n',
        encoding="utf-8",
    )

    _write_json(
        root / "artifacts" / "work-dev" / "interface-artifacts" / "artifact.json",
        {
            "artifactId": "iface-1",
            "artifactKind": "html-visualizer",
            "recordAuthority": "none",
            "gateEffect": "none",
        },
    )
    _write_json(
        root / "artifacts" / "work-dev" / "workbench-receipts" / "receipt.json",
        {
            "receiptKind": "workbench",
            "revisionSummary": "pilot inspection only",
            "recordAuthority": "none",
            "gateEffect": "none",
        },
    )
    _write_json(
        root / "docs" / "portability" / "emulation" / "emulation-bundle-schema.v1.json",
        {
            "properties": {
                "authority": {
                    "properties": {
                        "mergeAuthority": {
                            "const": "none"
                        }
                    }
                }
            }
        },
    )
    (root / "docs" / "portability" / "emulation" / "behavior-spec" / "v1-proposal-envelope.md").write_text(
        '# Proposal Envelope\n\n'
        '```json\n'
        '{"requires_human_review": true}\n'
        '```\n\n'
        'Importing a proposal envelope still requires human review.\n',
        encoding="utf-8",
    )
    (root / "docs" / "skill-work" / "work-dev" / "README.md").write_text(
        "WORK docs do not have canonical merge authority.\n",
        encoding="utf-8",
    )
    config_path = root / "config" / "doctrine-rules.v1.json"
    _write_json(config_path, _base_config())
    return config_path


@pytest.fixture
def tmp_repo(tmp_path: Path) -> tuple[Path, Path]:
    config_path = _build_repo(tmp_path)
    return tmp_path, config_path


def test_doctrine_drift_clean_repo(tmp_repo: tuple[Path, Path]) -> None:
    repo_root, config_path = tmp_repo
    mod = _load_module()
    report = mod.audit_repo(repo_root, config_path)
    assert report["ok"] is True
    assert report["violations"] == []


@pytest.mark.parametrize(
    ("mutator", "rule_id"),
    [
        (
            lambda root: (root / "scripts" / "rogue_writer.py").write_text(
                'gate_path = user_dir / "recursion-gate.md"\n'
                'gate_path.write_text("bad", encoding="utf-8")\n',
                encoding="utf-8",
            ),
            "approved-canonical-writers",
        ),
        (
            lambda root: _write_json(
                root / "artifacts" / "work-dev" / "interface-artifacts" / "artifact.json",
                {
                    "artifactId": "iface-1",
                    "artifactKind": "html-visualizer",
                    "recordAuthority": "draftable",
                    "gateEffect": "none",
                },
            ),
            "interface-artifact-non-authority",
        ),
        (
            lambda root: _write_json(
                root / "docs" / "portability" / "emulation" / "emulation-bundle-schema.v1.json",
                {
                    "properties": {
                        "authority": {
                            "properties": {
                                "mergeAuthority": {
                                    "const": "review-required"
                                }
                            }
                        }
                    }
                },
            ),
            "portable-emulation-no-merge-authority",
        ),
        (
            lambda root: _write_json(
                root / "artifacts" / "work-dev" / "workbench-receipts" / "receipt.json",
                {
                    "receiptKind": "workbench",
                    "revisionSummary": "This is proof of external facts.",
                    "recordAuthority": "none",
                    "gateEffect": "none",
                },
            ),
            "workbench-receipts-no-evidence-truth",
        ),
        (
            lambda root: (root / "docs" / "skill-work" / "work-dev" / "README.md").write_text(
                "This WORK page has canonical merge authority.\n",
                encoding="utf-8",
            ),
            "work-docs-no-canonical-merge-authority",
        ),
        (
            lambda root: (root / "docs" / "portability" / "emulation" / "behavior-spec" / "v1-proposal-envelope.md").write_text(
                "# Proposal Envelope\n\nNo review clause here.\n",
                encoding="utf-8",
            ),
            "proposal-envelopes-require-human-review",
        ),
    ],
)
def test_doctrine_drift_reports_each_requested_rule(
    tmp_repo: tuple[Path, Path], mutator, rule_id: str
) -> None:
    repo_root, config_path = tmp_repo
    mutator(repo_root)
    mod = _load_module()
    report = mod.audit_repo(repo_root, config_path)
    assert report["ok"] is False
    assert any(item["ruleId"] == rule_id for item in report["violations"])


def test_doctrine_drift_cli_json_reports_violations(tmp_repo: tuple[Path, Path]) -> None:
    repo_root, config_path = tmp_repo
    (repo_root / "scripts" / "rogue_writer.py").write_text(
        'gate_path = user_dir / "recursion-gate.md"\n'
        'gate_path.write_text("bad", encoding="utf-8")\n',
        encoding="utf-8",
    )
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(repo_root),
            "--config",
            str(config_path),
            "--json",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    payload = json.loads(proc.stdout)
    assert payload["ok"] is False
    assert payload["violationCount"] >= 1
    assert any(item["ruleId"] == "approved-canonical-writers" for item in payload["violations"])
