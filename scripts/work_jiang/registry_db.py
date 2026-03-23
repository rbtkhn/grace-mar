"""SQLite materialized view for predictions/divergences JSONL (query layer; JSONL remains canonical)."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = ROOT / "research" / "external" / "work-jiang" / "registry" / "work_jiang_metrics.sqlite"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id TEXT PRIMARY KEY,
            video_id TEXT,
            lecture_ref TEXT,
            resolution_status TEXT,
            claim_type TEXT,
            upload_date TEXT,
            payload TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_pred_video ON predictions(video_id);
        CREATE INDEX IF NOT EXISTS idx_pred_status ON predictions(resolution_status);

        CREATE TABLE IF NOT EXISTS divergences (
            divergence_id TEXT PRIMARY KEY,
            video_id TEXT,
            lecture_ref TEXT,
            divergence_type TEXT,
            strength TEXT,
            payload TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_div_video ON divergences(video_id);
        CREATE INDEX IF NOT EXISTS idx_div_type ON divergences(divergence_type);
        """
    )
    conn.commit()


def rebuild_from_jsonl(
    *,
    predictions_path: Path | None = None,
    divergences_path: Path | None = None,
    db_path: Path | None = None,
) -> None:
    pred_p = predictions_path or (
        ROOT / "research/external/work-jiang/prediction-tracking/registry/predictions.jsonl"
    )
    div_p = divergences_path or (
        ROOT / "research/external/work-jiang/divergence-tracking/registry/divergences.jsonl"
    )
    conn = connect(db_path)
    init_schema(conn)
    conn.execute("DELETE FROM predictions")
    conn.execute("DELETE FROM divergences")

    if pred_p.exists():
        with pred_p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                pid = row.get("prediction_id") or ""
                conn.execute(
                    """INSERT INTO predictions
                    (prediction_id, video_id, lecture_ref, resolution_status, claim_type, upload_date, payload)
                    VALUES (?,?,?,?,?,?,?)""",
                    (
                        pid,
                        row.get("video_id"),
                        row.get("lecture_ref"),
                        row.get("resolution_status"),
                        row.get("claim_type"),
                        row.get("upload_date"),
                        json.dumps(row, ensure_ascii=True),
                    ),
                )

    if div_p.exists():
        with div_p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                did = row.get("divergence_id") or ""
                conn.execute(
                    """INSERT INTO divergences
                    (divergence_id, video_id, lecture_ref, divergence_type, strength, payload)
                    VALUES (?,?,?,?,?,?)""",
                    (
                        did,
                        row.get("video_id"),
                        row.get("lecture_ref"),
                        row.get("divergence_type"),
                        row.get("strength"),
                        json.dumps(row, ensure_ascii=True),
                    ),
                )

    conn.commit()
    conn.close()


def _env_prefer_sqlite() -> bool:
    import os

    v = os.environ.get("WORK_JIANG_REGISTRY_PREFER_SQLITE", "").strip().lower()
    return v in ("1", "true", "yes")


def load_predictions_for_link(*, prefer_sqlite: bool | None = None) -> list[dict]:
    """Load prediction rows for link_supporting_registries (JSONL canonical; optional SQLite read)."""
    prefer = _env_prefer_sqlite() if prefer_sqlite is None else prefer_sqlite
    pred_p = ROOT / "research/external/work-jiang/prediction-tracking/registry/predictions.jsonl"
    if prefer and DEFAULT_DB.exists():
        conn = connect()
        out: list[dict] = []
        for row in conn.execute("SELECT payload FROM predictions"):
            out.append(json.loads(row[0]))
        conn.close()
        return out
    if not pred_p.exists():
        return []
    out = []
    with pred_p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def load_divergences_for_link(*, prefer_sqlite: bool | None = None) -> list[dict]:
    """Load divergence rows for link_supporting_registries (JSONL canonical; optional SQLite read)."""
    prefer = _env_prefer_sqlite() if prefer_sqlite is None else prefer_sqlite
    div_p = ROOT / "research/external/work-jiang/divergence-tracking/registry/divergences.jsonl"
    if prefer and DEFAULT_DB.exists():
        conn = connect()
        out: list[dict] = []
        for row in conn.execute("SELECT payload FROM divergences"):
            out.append(json.loads(row[0]))
        conn.close()
        return out
    if not div_p.exists():
        return []
    out = []
    with div_p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
