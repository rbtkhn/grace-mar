from __future__ import annotations

import json
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import export_emulation_bundle as emulation_module  # noqa: E402
import export_runtime_bundle as runtime_bundle_module  # noqa: E402


def test_build_emulation_envelope_points_to_existing_surfaces() -> None:
    payload = emulation_module.build_emulation_envelope(
        user_id="grace-mar",
        runtime_mode="portable_bundle_only",
        generated_at="2026-04-24T16:00:00Z",
    )
    assert payload["format"] == "grace-mar-emulation-bundle"
    assert payload["references"]["prpPath"] == "record/grace-mar-llm.txt"
    assert payload["references"]["forkExportPath"] == "record/fork-export.json"
    assert payload["references"]["authorityMapPath"] == "policy/authority-map.json"
    assert payload["proposalReturn"]["canonicalSurfacesTouched"] is False
    assert payload["runtimeObservationReturn"]["importScript"] == (
        "scripts/runtime/import_runtime_observation.py"
    )


def test_export_emulation_bundle_writes_envelope_and_policy_refs(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(runtime_bundle_module, "append_harness_event", lambda *args, **kwargs: None)
    monkeypatch.setattr(emulation_module, "append_harness_event", lambda *args, **kwargs: None)
    fake_ledger = types.SimpleNamespace(append_integration_ledger=lambda *args, **kwargs: None)
    monkeypatch.setitem(sys.modules, "emit_compute_ledger", fake_ledger)

    payload = emulation_module.export_emulation_bundle(
        user_id="grace-mar",
        output_dir=tmp_path,
        runtime_mode="portable_bundle_only",
    )

    assert payload["format"] == "grace-mar-emulation-bundle"
    envelope_path = tmp_path / "emulation-bundle.json"
    authority_path = tmp_path / "policy" / "authority-map.json"
    proposal_schema_path = tmp_path / "policy" / "change-proposal.v1.json"
    runtime_bundle_path = tmp_path / "bundle.json"

    assert envelope_path.is_file()
    assert authority_path.is_file()
    assert proposal_schema_path.is_file()
    assert runtime_bundle_path.is_file()

    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    runtime_bundle = json.loads(runtime_bundle_path.read_text(encoding="utf-8"))
    assert envelope["runtimeBundlePath"] == "bundle.json"
    assert runtime_bundle["format"] == "grace-mar-runtime-bundle"
