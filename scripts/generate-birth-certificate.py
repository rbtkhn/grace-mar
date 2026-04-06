#!/usr/bin/env python3
"""
Generate a signed seed birth certificate after strict validation.

Genesis hash: SHA-256 of UTF-8 newlines joining canonical JSON (sort_keys, compact)
for each file in seed_phase_artifacts.SCHEMA_BY_FILE order.

Usage:
  python3 scripts/generate-birth-certificate.py users/demo/seed-phase
  python3 scripts/generate-birth-certificate.py users/demo/seed-phase \\
      --private-key path/to/ed25519.pem

Env:
  SEED_BIRTH_CERT_PRIVATE_KEY_PATH — PEM path if --private-key omitted

Demo only:
  --insecure-generate-ephemeral-key  (new key each run; not verifiable across runs)

Outputs in seed-phase dir:
  seed_birth_certificate.json
  seed_birth_certificate.sig  (raw Ed25519 signature bytes)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

from seed_phase_artifacts import SCHEMA_BY_FILE


GENESIS_ALGORITHM = "sha256_newline_joined_canonical_json_v1"


def _canonical_json_bytes(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_genesis_hash(seed_dir: Path) -> str:
    parts: list[bytes] = []
    for jname in SCHEMA_BY_FILE:
        path = seed_dir / jname
        if not path.is_file():
            raise FileNotFoundError(f"Missing seed artifact for genesis: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        parts.append(_canonical_json_bytes(data))
    joined = b"\n".join(parts)
    return hashlib.sha256(joined).hexdigest()


def _read_template_version() -> str:
    p = REPO_ROOT / "template-manifest.json"
    if not p.is_file():
        return "unknown"
    meta = json.loads(p.read_text(encoding="utf-8"))
    return str(meta.get("templateVersion") or "unknown")


def _load_ed25519_private_key(pem_path: Path):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    pem = pem_path.read_bytes()
    key = serialization.load_pem_private_key(pem, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError(f"Expected Ed25519 private key in {pem_path}, got {type(key).__name__}")
    return key


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate signed seed birth certificate.")
    ap.add_argument("directory", type=Path, help="seed-phase directory, e.g. users/demo/seed-phase")
    ap.add_argument(
        "--private-key",
        type=Path,
        help="PEM file with Ed25519 private key (or set SEED_BIRTH_CERT_PRIVATE_KEY_PATH)",
    )
    ap.add_argument(
        "--insecure-generate-ephemeral-key",
        action="store_true",
        help="Generate a throwaway key (demo only; signatures are not durable).",
    )
    ap.add_argument(
        "--readiness-gate",
        type=str,
        default="",
        help="Override readiness label (default: read from seed_readiness.json readiness.decision)",
    )
    args = ap.parse_args()

    seed_dir = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    if not seed_dir.is_dir():
        print(f"Not a directory: {seed_dir}", file=sys.stderr)
        return 1

    try:
        genesis_hash = compute_genesis_hash(seed_dir)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e, file=sys.stderr)
        return 1

    manifest_path = seed_dir / "seed-phase-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    readiness_path = seed_dir / "seed_readiness.json"
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    rd = readiness.get("readiness") or {}

    readiness_gate = args.readiness_gate.strip() or str(rd.get("decision") or "unknown").upper()

    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError:
        print(
            "cryptography is required. pip install -r scripts/requirements-seed-phase-signing.txt",
            file=sys.stderr,
        )
        return 1

    private_key: Ed25519PrivateKey
    if args.insecure_generate_ephemeral_key:
        private_key = Ed25519PrivateKey.generate()
        print(
            "WARNING: --insecure-generate-ephemeral-key — private key is ephemeral; "
            "verify cannot reproduce later.",
            file=sys.stderr,
        )
    else:
        key_path = args.private_key or os.environ.get("SEED_BIRTH_CERT_PRIVATE_KEY_PATH")
        if not key_path:
            print(
                "Provide --private-key, set SEED_BIRTH_CERT_PRIVATE_KEY_PATH, "
                "or use --insecure-generate-ephemeral-key for demos.",
                file=sys.stderr,
            )
            return 1
        private_key = _load_ed25519_private_key(Path(key_path).expanduser().resolve())

    public_key = private_key.public_key()
    pub_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    cert_core = {
        "genesis_algorithm": GENESIS_ALGORITHM,
        "genesis_hash": genesis_hash,
        "instance_id": manifest.get("user_slug"),
        "template_version": _read_template_version(),
        "schema_version": manifest.get("schema_version"),
        "seed_phase_version": manifest.get("seed_phase_version"),
        "manifest_status": manifest.get("status"),
        "seed_phase_completed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "readiness_gate": readiness_gate,
        "public_key_hex": pub_raw.hex(),
    }

    sign_payload = _canonical_json_bytes(cert_core)
    signature = private_key.sign(sign_payload)

    cert_out = seed_dir / "seed_birth_certificate.json"
    sig_out = seed_dir / "seed_birth_certificate.sig"

    cert_out.write_text(json.dumps(cert_core, indent=2) + "\n", encoding="utf-8")
    sig_out.write_bytes(signature)

    try:
        display = cert_out.relative_to(REPO_ROOT)
    except ValueError:
        display = cert_out
    print(f"Wrote {display} and {sig_out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
