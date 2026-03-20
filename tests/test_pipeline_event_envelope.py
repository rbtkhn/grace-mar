"""pipeline_event_envelope: stable ids and version constant."""

import re

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from pipeline_event_envelope import ENVELOPE_VERSION, new_pipeline_event_id  # noqa: E402


def test_envelope_version_is_positive_int():
    assert isinstance(ENVELOPE_VERSION, int)
    assert ENVELOPE_VERSION >= 1


def test_new_pipeline_event_id_format():
    eid = new_pipeline_event_id("grace-mar")
    assert re.match(r"^evt_\d{8}_\d{6}_[0-9a-f]{8}$", eid), eid


def test_new_pipeline_event_id_unique():
    ids = {new_pipeline_event_id("grace-mar") for _ in range(200)}
    assert len(ids) == 200
