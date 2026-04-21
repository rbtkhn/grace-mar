"""
Runtime-only model tier policy (non-canonical).

Resolves allowed tier, preferred provider/model from env, and fallback chain from YAML.
Does not invoke providers or change Record / RECURSION-GATE.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

_MODEL_TIERS_REL = Path("config/model_routing/model_tiers.yaml")
_TASK_POLICY_REL = Path("config/model_routing/task_policy.yaml")


def _norm_token(s: str | None) -> str | None:
    if s is None:
        return None
    t = str(s).strip().lower()
    return t if t else None


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except ImportError as e:  # pragma: no cover
        raise SystemExit("PyYAML is required to load model routing config") from e
    if not path.is_file():
        raise FileNotFoundError(f"model routing config missing: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def load_model_tiers(repo_root: Path) -> dict[str, Any]:
    return _load_yaml((repo_root / _MODEL_TIERS_REL).resolve())


def load_task_policy(repo_root: Path) -> dict[str, Any]:
    return _load_yaml((repo_root / _TASK_POLICY_REL).resolve())


def _resolve_provider_model(tiers_doc: dict[str, Any], allowed_tier: str) -> tuple[str | None, str | None]:
    tiers_map = tiers_doc.get("tiers")
    if not isinstance(tiers_map, dict):
        return None, None
    block = tiers_map.get(allowed_tier)
    if not isinstance(block, dict):
        return None, None
    providers = block.get("providers") or []
    if not providers or not isinstance(providers, list):
        return None, None
    row = providers[0]
    if not isinstance(row, dict):
        return None, None
    provider = row.get("provider")
    env_name = row.get("model_env")
    prov = str(provider).strip() if provider else None
    if not env_name:
        return prov or None, None
    raw = os.environ.get(str(env_name).strip(), "")
    model = raw.strip() if raw else None
    return prov, model if model else None


def resolve_model_policy(
    *,
    repo_root: Path,
    task_type: str | None,
    task_subtype: str | None = None,
    action: str | None = None,
) -> dict[str, Any]:
    """
    Return allowed_tier, resolved_provider, resolved_model, fallback_chain, requires_human_review.

    - Forbidden ``action`` → tier X, empty fallback chain, requires_human_review True.
    - Unknown or missing ``task_type`` → tier A, defaults fallback_chain.
    """
    tt = _norm_token(task_type)
    st = _norm_token(task_subtype)
    act = _norm_token(action)

    tiers_doc = load_model_tiers(repo_root)
    policy_doc = load_task_policy(repo_root)

    forbidden_raw = policy_doc.get("forbidden_actions") or []
    forbidden_set = {str(x).strip().lower() for x in forbidden_raw if x is not None and str(x).strip()}
    if act and act in forbidden_set:
        return {
            "allowed_tier": "X",
            "resolved_provider": None,
            "resolved_model": None,
            "fallback_chain": [],
            "requires_human_review": True,
        }

    defaults = policy_doc.get("defaults") or {}
    fallback_chain = list(defaults.get("fallback_chain") or ["B", "A"])
    if not all(isinstance(x, str) and x for x in fallback_chain):
        fallback_chain = ["B", "A"]

    tasks = policy_doc.get("tasks") or {}
    requires_human_review = False
    if not tt or not isinstance(tasks, dict) or tt not in tasks:
        allowed_tier = "A"
    else:
        tdef = tasks[tt]
        if not isinstance(tdef, dict):
            allowed_tier = "A"
        else:
            allowed_tier = str(tdef.get("default_tier") or "B").strip().upper()
            subtypes = tdef.get("subtypes") or {}
            if st and isinstance(subtypes, dict) and st in subtypes:
                sdef = subtypes[st]
                if isinstance(sdef, dict):
                    if "default_tier" in sdef:
                        allowed_tier = str(sdef["default_tier"]).strip().upper()
                    requires_human_review = bool(sdef.get("requires_human_review", False))

    if allowed_tier == "X":
        return {
            "allowed_tier": "X",
            "resolved_provider": None,
            "resolved_model": None,
            "fallback_chain": [],
            "requires_human_review": True,
        }

    rprov, rmodel = _resolve_provider_model(tiers_doc, allowed_tier)
    return {
        "allowed_tier": allowed_tier,
        "resolved_provider": rprov,
        "resolved_model": rmodel,
        "fallback_chain": list(fallback_chain),
        "requires_human_review": requires_human_review,
    }
