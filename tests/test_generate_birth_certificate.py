"""Tests for scripts/generate-birth-certificate.py (genesis hash + optional signing)."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Golden vector: SCHEMA_BY_FILE order + sha256_newline_joined_canonical_json_v1
VALID_MINIMAL_GENESIS_HASH = (
    "afbb7a39863359eb86333351b17457605662608f7d3797f1287613011bfa03b7"
)

GENESIS_ALGORITHM = "sha256_newline_joined_canonical_json_v1"


def _load_birth_cert_module():
    scripts = REPO_ROOT / "scripts"
    sys.path.insert(0, str(scripts))
    try:
        path = scripts / "generate-birth-certificate.py"
        spec = importlib.util.spec_from_file_location("generate_birth_certificate_mod", path)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        sys.modules["generate_birth_certificate_mod"] = mod
        spec.loader.exec_module(mod)
        return mod
    finally:
        try:
            sys.path.remove(str(scripts))
        except ValueError:
            pass


def test_genesis_hash_valid_minimal_fixture(tmp_path) -> None:
    mod = _load_birth_cert_module()
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "tests/fixtures/seed-phase/valid-minimal", target)
    assert mod.compute_genesis_hash(target) == VALID_MINIMAL_GENESIS_HASH


def test_subprocess_birth_certificate_insecure(tmp_path) -> None:
    pytest.importorskip("cryptography")
    from tests.conftest import repo_python, run_cmd

    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "tests/fixtures/seed-phase/valid-minimal", target)
    result = run_cmd(
        [
            repo_python(),
            "scripts/generate-birth-certificate.py",
            str(target),
            "--insecure-generate-ephemeral-key",
        ],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    cert_path = target / "seed_birth_certificate.json"
    sig_path = target / "seed_birth_certificate.sig"
    assert cert_path.is_file() and sig_path.is_file()
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert["genesis_hash"] == VALID_MINIMAL_GENESIS_HASH
    assert cert["genesis_algorithm"] == GENESIS_ALGORITHM

    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(cert["public_key_hex"]))
    payload = json.dumps(cert, sort_keys=True, separators=(",", ":")).encode("utf-8")
    pub.verify(sig_path.read_bytes(), payload)
